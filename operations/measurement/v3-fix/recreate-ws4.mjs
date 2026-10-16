#!/usr/bin/env node
// Delete tags 14/16 + triggers 9/15 in the fresh Default Workspace (ws4), then recreate
// them with IDENTICAL parameters (v2/v3 config as source of truth, incl. value-less
// parameterValue entries that the CLI normalizer cannot express).
import { getAuthenticatedClient } from '/Users/mac/projects/Google-Tag-Manager-Hilfe/gtm-cli/dist/auth/oauth.js';
import { google } from '/Users/mac/projects/Google-Tag-Manager-Hilfe/gtm-cli/node_modules/googleapis/build/src/index.js';
import { writeFileSync } from 'node:fs';

const WS = 'accounts/572865630/containers/267198165/workspaces/4';
const EV = '/Users/mac/agentic-business/barrierefrei-leads/operations/measurement/v3-fix';

const CONFIG = {
  tags: [
    {
      tagId: '14', name: 'ZBK — GA4 client-side (consent-gated)', type: 'googtag', firingTriggerId: ['9'],
      notes: 'ZBK client-side GA4 (consent-gated). Recreated 2026-10-16 in ws4 after v2+v3 runtimes never fired.',
      parameter: [
        { type: 'template', key: 'tagId', value: 'G-5738T8FHWW' },
        { type: 'list', key: 'configSettingsTable', list: [
          { type: 'map', map: [{ type: 'template', key: 'parameter', value: 'send_page_view' }, { type: 'template', key: 'parameterValue', value: 'true' }] },
          { type: 'map', map: [{ type: 'template', key: 'parameter', value: 'page_location' }, { type: 'template', key: 'parameterValue', value: 'https://zuhausebleiben-kompass.de/' }] },
          { type: 'map', map: [{ type: 'template', key: 'parameter', value: 'page_referrer' }, { type: 'template', key: 'parameterValue' }] },
          { type: 'map', map: [{ type: 'template', key: 'parameter', value: 'page_title' }, { type: 'template', key: 'parameterValue' }] },
        ]},
      ],
    },
    {
      tagId: '16', name: 'ZBK — GA4 cta_click (consent-gated)', type: 'gaawe', firingTriggerId: ['15'],
      notes: 'ZBK cta_click GA4 (consent-gated). Recreated 2026-10-16 in ws4 after v2+v3 runtimes never fired.',
      parameter: [
        { type: 'list', key: 'eventSettingsTable', list: [
          { type: 'map', map: [{ type: 'template', key: 'parameter', value: 'content_id' }, { type: 'template', key: 'parameterValue', value: '{{ZBK DLV - measurement.content_id}}' }] },
          { type: 'map', map: [{ type: 'template', key: 'parameter', value: 'cta_id' }, { type: 'template', key: 'parameterValue', value: '{{ZBK DLV - measurement.cta_id}}' }] },
        ]},
        { type: 'template', key: 'eventName', value: 'cta_click' },
        { type: 'template', key: 'measurementIdOverride', value: 'G-5738T8FHWW' },
      ],
    },
  ],
  triggers: [
    {
      triggerId: '9', name: 'ZBK — sanitized analytics-only events', type: 'customEvent',
      notes: 'zbk_measurement page_view, 7 consent predicates. Recreated 2026-10-16 in ws4 after v2+v3 never fired.',
      customEventFilter: [{ type: 'equals', parameter: [
        { type: 'template', key: 'arg0', value: '{{_event}}' }, { type: 'template', key: 'arg1', value: 'zbk_measurement' } ]}],
      filter: ['analytics_allowed,true', 'consent_version,2', 'consent.analytics_storage,granted',
        'consent.ad_storage,denied', 'consent.ad_user_data,denied', 'consent.ad_personalization,denied',
        'measurement.event_name,page_view'].map((pair) => {
        const [v, a] = pair.split(',');
        return { type: 'equals', parameter: [
          { type: 'template', key: 'arg0', value: `{{ZBK DLV - ${v}}}` }, { type: 'template', key: 'arg1', value: a } ]};
      }),
    },
    {
      triggerId: '15', name: 'ZBK — cta_click only (consent-gated)', type: 'customEvent',
      notes: 'zbk_measurement cta_click, 7 consent predicates. Recreated 2026-10-16 in ws4 after v2+v3 never fired.',
      customEventFilter: [{ type: 'equals', parameter: [
        { type: 'template', key: 'arg0', value: '{{_event}}' }, { type: 'template', key: 'arg1', value: 'zbk_measurement' } ]}],
      filter: ['analytics_allowed,true', 'consent_version,2', 'consent.analytics_storage,granted',
        'consent.ad_storage,denied', 'consent.ad_user_data,denied', 'consent.ad_personalization,denied',
        'measurement.event_name,cta_click'].map((pair) => {
        const [v, a] = pair.split(',');
        return { type: 'equals', parameter: [
          { type: 'template', key: 'arg0', value: `{{ZBK DLV - ${v}}}` }, { type: 'template', key: 'arg1', value: a } ]};
      }),
    },
  ],
};

const rows = (parameter) => parameter.flatMap((p) => p.key === 'configSettingsTable' || p.key === 'eventSettingsTable'
  ? p.list.map((row) => {
      const k = row.map.find((e) => e.key === 'parameter');
      const v = row.map.find((e) => e.key === 'parameterValue');
      return [k.value, v && 'value' in v ? v.value : ''];
    })
  : [[p.key, p.value]]);

const auth = await getAuthenticatedClient();
if (!auth) { console.error('NO_AUTH'); process.exit(1); }
const tm = google.tagmanager({ version: 'v2', auth });
const log = {};

// 1. delete
for (const kind of ['tag', 'trigger']) {
  for (const cfg of CONFIG[kind + 's']) {
    try {
      await tm.accounts.containers.workspaces[kind + 's'].delete({ path: `${WS}/${kind}s/${cfg.triggerId || cfg.tagId}` });
      log[`deleted ${kind} ${cfg.triggerId || cfg.tagId}`] = 'ok';
    } catch (e) {
      log[`deleted ${kind} ${cfg.triggerId || cfg.tagId}`] = 'FAIL: ' + e.message.slice(0, 120);
    }
  }
}

// 2. recreate triggers first (tags reference them)
for (const cfg of CONFIG.triggers) {
  const created = (await tm.accounts.containers.workspaces.triggers.create({
    parent: WS, requestBody: {
      name: cfg.name, type: cfg.type, notes: cfg.notes,
      filter: cfg.filter, customEventFilter: cfg.customEventFilter,
    },
  })).data;
  log[`created trigger (was ${cfg.triggerId})`] = { newId: created.triggerId, fingerprint: created.fingerprint };
}

// 3. recreate tags
for (const cfg of CONFIG.tags) {
  const created = (await tm.accounts.containers.workspaces.tags.create({
    parent: WS, requestBody: {
      name: cfg.name, type: cfg.type, notes: cfg.notes,
      parameter: cfg.parameter, firingTriggerId: cfg.firingTriggerId,
    },
  })).data;
  log[`created tag (was ${cfg.tagId})`] = { newId: created.tagId, fingerprint: created.fingerprint };
}

// 4. verify readbacks vs CONFIG
let allOk = true;
const readback = { triggers: [], tags: [] };
for (const cfg of CONFIG.triggers) {
  const list = (await tm.accounts.containers.workspaces.triggers.list({ parent: WS })).data.trigger || [];
  const ent = list.find((t) => t.name === cfg.name);
  if (!ent) { allOk = false; log[`verify trigger ${cfg.triggerId}`] = 'NOT FOUND'; continue; }
  const okFilter = JSON.stringify(ent.filter) === JSON.stringify(cfg.filter);
  const okCef = JSON.stringify(ent.customEventFilter) === JSON.stringify(cfg.customEventFilter);
  readback.triggers.push({ oldId: cfg.triggerId, newId: ent.triggerId, filterOk: okFilter, cefOk: okCef });
  allOk &= okFilter && okCef;
}
const tagList = (await tm.accounts.containers.workspaces.tags.list({ parent: WS })).data.tag || [];
for (const cfg of CONFIG.tags) {
  const ent = tagList.find((t) => t.name === cfg.name);
  if (!ent) { allOk = false; log[`verify tag ${cfg.tagId}`] = 'NOT FOUND'; continue; }
  const okParams = JSON.stringify(rows(ent.parameter)) === JSON.stringify(rows(cfg.parameter));
  readback.tags.push({ oldId: cfg.tagId, newId: ent.tagId, paramsOk: okParams, firing: ent.firingTriggerId });
  allOk &= okParams;
}

writeFileSync(`${EV}/recreate-ws4-result.json`, JSON.stringify({ log, readback, allOk }, null, 1));
console.log(JSON.stringify({ log, readback, allOk }, null, 1));
process.exit(allOk ? 0 : 1);
