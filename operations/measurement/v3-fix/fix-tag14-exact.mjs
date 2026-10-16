#!/usr/bin/env node
// Restore tag 14 parameter rows exactly as in live version 2 (incl. empty page_referrer/page_title),
// using the gtm-cli's own stored OAuth credentials and the raw googleapis client
// (the CLI's gtm_update_tag normalizer cannot express value-less parameterValue entries).
import { getAuthenticatedClient } from '/Users/mac/projects/Google-Tag-Manager-Hilfe/gtm-cli/dist/auth/oauth.js';
import { google } from '/Users/mac/projects/Google-Tag-Manager-Hilfe/gtm-cli/node_modules/googleapis/build/src/index.js';
import { writeFileSync } from 'node:fs';

const WS = 'accounts/572865630/containers/267198165/workspaces/3';
const TAG14 = `${WS}/tags/14`;
const EV = '/Users/mac/agentic-business/barrierefrei-leads/operations/measurement/v3-fix';

// Exact parameter array from the live v2 container version export (gtm_export_version).
const V2_PARAMETER = [
  { type: 'template', key: 'tagId', value: 'G-5738T8FHWW' },
  { type: 'list', key: 'configSettingsTable', list: [
    { type: 'map', map: [
      { type: 'template', key: 'parameter', value: 'send_page_view' },
      { type: 'template', key: 'parameterValue', value: 'true' },
    ]},
    { type: 'map', map: [
      { type: 'template', key: 'parameter', value: 'page_location' },
      { type: 'template', key: 'parameterValue', value: 'https://zuhausebleiben-kompass.de/' },
    ]},
    { type: 'map', map: [
      { type: 'template', key: 'parameter', value: 'page_referrer' },
      { type: 'template', key: 'parameterValue' },
    ]},
    { type: 'map', map: [
      { type: 'template', key: 'parameter', value: 'page_title' },
      { type: 'template', key: 'parameterValue' },
    ]},
  ]},
];

const rows = (parameter) => parameter.flatMap((p) => p.key === 'configSettingsTable'
  ? p.list.map((row) => {
      const k = row.map.find((e) => e.key === 'parameter');
      const v = row.map.find((e) => e.key === 'parameterValue');
      return [k.value, v && 'value' in v ? v.value : ''];
    })
  : [[p.key, p.value]]);

const auth = await getAuthenticatedClient();
if (!auth) { console.error('NO_AUTH'); process.exit(1); }
const tm = google.tagmanager({ version: 'v2', auth });

const cur = (await tm.accounts.containers.workspaces.tags.get({ path: TAG14 })).data;
console.log('current fingerprint:', cur.fingerprint);

const requestBody = {
  name: cur.name,
  type: 'googtag',
  parameter: V2_PARAMETER,
  firingTriggerId: ['9'],
  notes: 'ZBK client-side GA4 (consent-gated). Resaved 2026-10-16 to regenerate v3 runtime (v2 never fired).',
};
const updated = (await tm.accounts.containers.workspaces.tags.update({
  path: TAG14, fingerprint: cur.fingerprint, requestBody,
})).data;
console.log('updated fingerprint:', updated.fingerprint);

const rb = (await tm.accounts.containers.workspaces.tags.get({ path: TAG14 })).data;
writeFileSync(`${EV}/tag-14-after-resave.json`, JSON.stringify(rb, null, 1));
const same = JSON.stringify(rows(rb.parameter)) === JSON.stringify(rows(V2_PARAMETER));
console.log('readback rows:', JSON.stringify(rows(rb.parameter)));
console.log('EXACT_RESTORE:', same ? 'OK' : 'MISMATCH');
process.exit(same ? 0 : 1);
