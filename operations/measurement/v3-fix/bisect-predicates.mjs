// Per-predicate bisect: which of predicates 0..6 evaluates FALSE at match time?
import {chromium} from 'playwright';
import {readFileSync} from 'node:fs';

const V4 = readFileSync('operations/measurement/v3-fix/gtm-v4.js', 'utf8');
const RULES_ORIG = '"rules":[[["if",0,1,2,3,4,5,6,7],["add",0]],[["if",0,1,2,3,4,5,7,8],["add",1]]]';

const NAMES = {
  0: 'analytics_allowed eq true',
  1: 'consent_version eq 2',
  2: 'consent.analytics_storage eq granted',
  3: 'consent.ad_storage eq denied',
  4: 'consent.ad_user_data eq denied',
  5: 'consent.ad_personalization eq denied',
  6: 'measurement.event_name eq page_view',
  7: '_event eq zbk_measurement (control)',
};

const browser = await chromium.launch();

async function runSingle(pid) {
  const rules = `"rules":[[["if",${pid}],["add",0]]]`;
  const body = V4.replace(RULES_ORIG, rules);
  const page = await (await browser.newContext()).newPage();
  const reqs = [];
  page.on('request', r => { const u = r.url(); if (/gtag\/js|g\/collect/.test(u)) reqs.push(u.slice(0, 100)); });
  await page.route('**//www.googletagmanager.com/gtm.js*', r => r.fulfill({contentType: 'text/javascript', body}));
  await page.goto('data:text/html,<html><body>probe</body></html>');
  await page.evaluate(() => {
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('consent', 'default', {analytics_storage: 'denied', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied'});
    window.gtag('consent', 'update', {analytics_storage: 'granted', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied'});
    window.dataLayer.push({event: 'zbk_consent_update', consent_version: 2, consent: {analytics_storage: 'granted', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied'}});
    const s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtm.js?id=GTM-M9TZZPLQ';
    document.head.appendChild(s);
    window.dataLayer.push({event: 'zbk_measurement', analytics_allowed: true, consent_version: 2,
      consent: {analytics_storage: 'granted', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied'},
      measurement: {event_name: 'page_view', content_id: 'p', cta_id: ''}});
  });
  await page.waitForTimeout(9000);
  const fired = reqs.length > 0;
  // also read the macros directly from the model for comparison
  const macroVals = await page.evaluate((pid_) => {
    const g = window.google_tag_manager['GTM-M9TZZPLQ'];
    const names = ['analytics_allowed', 'consent_version', 'consent.analytics_storage', 'consent.ad_storage', 'consent.ad_user_data', 'consent.ad_personalization', 'measurement.event_name'];
    const out = {};
    for (const n of names) {
      try { const v = g.dataLayer.get(n); out[n] = v === undefined ? 'UNDEF' : `${typeof v}:${String(v)}`; }
      catch (e) { out[n] = 'ERR'; }
    }
    return out;
  }, pid);
  await page.close();
  return {pid, desc: NAMES[pid], fired, reqs: reqs.length, macroVals};
}

const results = [];
for (const pid of [0, 1, 2, 3, 4, 5, 6, 7]) {
  const r = await runSingle(pid);
  results.push(r);
  console.log(JSON.stringify({pid: r.pid, desc: r.desc, fired: r.fired}));
}
console.log('--- macro values (from last run):', JSON.stringify(results[results.length - 1].macroVals, null, 1));
await browser.close();
