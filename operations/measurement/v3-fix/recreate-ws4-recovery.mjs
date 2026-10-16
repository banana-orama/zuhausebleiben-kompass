#!/usr/bin/env node
// Recovery: ws4 currently has the two freshly created ZBK triggers (new IDs) and NO tags.
// Create both tags referencing the NEW trigger IDs, then verify all four entities.
import { getAuthenticatedClient } from '/Users/mac/projects/Google-Tag-Manager-Hilfe/gtm-cli/dist/auth/oauth.js';
import { google } from '/Users/mac/projects/Google-Tag-Manager-Hilfe/gtm-cli/node_modules/googleapis/build/src/index.js';
import { writeFileSync } from 'node:fs';

const WS = 'accounts/572865630/containers/267198165/workspaces/4';
const EV = '/Users/mac/agentic-business/barrierefrei-leads/operations/measurement/v3-fix';

const TAGS = [
  {
    was: '14', triggerWas: '9', triggerName: 'ZBK — sanitized analytics-only events',
    name: 'ZBK — GA4 client-side (consent-gated)', type: 'googtag',
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
    was: '16', triggerWas: '15', triggerName: 'ZBK — cta_click only (consent-gated)',
    name: 'ZBK — GA4 cta_click (consent-gated)', type: 'gaawe',
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
];

const EXPECT_TRIGGERS = [
  {
    was: '9', name: 'ZBK — sanitized analytics-only events',
    customEventFilter: [{ type: 'equals', parameter: [{ type: 'template', key: 'arg0', value: '{{_event}}' }, { type: 'template', key: 'arg1', value: 'zbk_measurement' }] }],
    filterPredicates: [['analytics_allowed', 'true'], ['consent_version', '2'], ['consent.analytics_storage', 'granted'], ['consent.ad_storage', 'denied'], ['consent.ad_user_data', 'denied'], ['consent.ad_personalization', 'denied'], ['measurement.event_name', 'page_view']],
  },
  {
    was: '15', name: 'ZBK — cta_click only (consent-gated)',
    customEventFilter: [{ type: 'equals', parameter: [{ type: 'template', key: 'arg0', value: '{{_event}}' }, { type: 'template', key: 'arg1', value: 'zbk_measurement' }] }],
    filterPredicates: [['analytics_allowed', 'true'], ['consent_version', '2'], ['consent.analytics_storage', 'granted'], ['consent.ad_storage', 'denied'], ['consent.ad_user_data', 'denied'], ['consent.ad_personalization', 'denied'], ['measurement.event_name', 'cta_click']],
  },
];

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
const out = { steps: [], ok: false };

const trigList = (await tm.accounts.containers.workspaces.triggers.list({ parent: WS })).data.trigger || [];
out.steps.push({ ws4Triggers: trigList.map((t) => ({ id: t.triggerId, name: t.name, type: t.type })) });

// create tags with NEW trigger ids
for (const cfg of TAGS) {
  const trig = trigList.find((t) => t.name === cfg.triggerName);
  if (!trig) { out.steps.push({ error: `trigger not found for tag ${cfg.was}: ${cfg.triggerName}` }); process.exit(1); }
  const created = (await tm.accounts.containers.workspaces.tags.create({
    parent: WS,
    requestBody: { name: cfg.name, type: cfg.type, notes: cfg.notes, parameter: cfg.parameter, firingTriggerId: [trig.triggerId] },
  })).data;
  out.steps.push({ createdTag: { was: cfg.was, newId: created.tagId, firingTriggerId: created.firingTriggerId, fingerprint: created.fingerprint } });
}

// full verification
const rbTriggers = (await tm.accounts.containers.workspaces.triggers.list({ parent: WS })).data.trigger || [];
const rbTags = (await tm.accounts.containers.workspaces.tags.list({ parent: WS })).data.tag || [];
out.triggers = EXPECT_TRIGGERS.map((exp) => {
  const ent = rbTriggers.find((t) => t.name === exp.name);
  if (!ent) return { was: exp.was, found: false };
  const expectedFilter = exp.filterPredicates.map(([v, a]) => ({
    type: 'equals', parameter: [{ type: 'template', key: 'arg0', value: `{{ZBK DLV - ${v}}}` }, { type: 'template', key: 'arg1', value: a }],
  }));
  return {
    was: exp.was, newId: ent.triggerId, found: true,
    filterExact: JSON.stringify(ent.filter) === JSON.stringify(expectedFilter),
    customEventFilterExact: JSON.stringify(ent.customEventFilter) === JSON.stringify(exp.customEventFilter),
    filterCount: (ent.filter || []).length,
  };
});
out.tags = TAGS.map((cfg) => {
  const ent = rbTags.find((t) => t.name === cfg.name);
  if (!ent) return { was: cfg.was, found: false };
  return {
    was: cfg.was, newId: ent.tagId, found: true, type: ent.type,
    paramsExact: JSON.stringify(rows(ent.parameter)) === JSON.stringify(rows(cfg.parameter)),
    firingTriggerId: ent.firingTriggerId, paused: !!ent.paused,
    consentSettings: ent.consentSettings || null,
  };
});
out.ok = out.triggers.every((t) => t.found && t.filterExact && t.customEventFilterExact)
  && out.tags.every((t) => t.found && t.paramsExact && !t.paused);

writeFileSync(`${EV}/recreate-ws4-recovery.json`, JSON.stringify(out, null, 1));
console.log(JSON.stringify(out, null, 1));
process.exit(out.ok ? 0 : 1);
