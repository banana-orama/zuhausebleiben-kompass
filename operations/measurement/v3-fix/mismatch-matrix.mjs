// Mismatch matrix for predicate 6 (measurement.event_name) and predicate 0 (analytics_allowed):
// push variants to find exactly which shape satisfies each predicate.
import {chromium} from 'playwright';
import {readFileSync} from 'node:fs';

const V4 = readFileSync('operations/measurement/v3-fix/gtm-v4.js', 'utf8');
const RULES_ORIG = '"rules":[[["if",0,1,2,3,4,5,6,7],["add",0]],[["if",0,1,2,3,4,5,7,8],["add",1]]]';

const VARIANTS = [
  {label: 'site shape (nested measurement object, boolean analytics_allowed)', push: {
    event: 'zbk_measurement', analytics_allowed: true, consent_version: 2,
    consent: {analytics_storage: 'granted', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied'},
    measurement: {event_name: 'page_view', content_id: 'p', cta_id: ''}}},
  {label: 'flat dotted keys, string values', push: {
    event: 'zbk_measurement', analytics_allowed: 'true', consent_version: '2',
    'consent.analytics_storage': 'granted', 'consent.ad_storage': 'denied', 'consent.ad_user_data': 'denied', 'consent.ad_personalization': 'denied',
    'measurement.event_name': 'page_view', 'measurement.content_id': 'p', 'measurement.cta_id': ''}},
];

const browser = await chromium.launch();

async function runPred(pid, push) {
  const rules = `"rules":[[["if",${pid}],["add",0]]]`;
  const body = V4.replace(RULES_ORIG, rules);
  const page = await (await browser.newContext()).newPage();
  const reqs = [];
  page.on('request', r => { const u = r.url(); if (/gtag\/js|g\/collect/.test(u)) reqs.push(1); });
  await page.route('**//www.googletagmanager.com/gtm.js*', r => r.fulfill({contentType: 'text/javascript', body}));
  await page.goto('data:text/html,<html><body>probe</body></html>');
  await page.evaluate((p) => {
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('consent', 'default', {analytics_storage: 'denied', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied'});
    const s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtm.js?id=GTM-M9TZZPLQ';
    document.head.appendChild(s);
    window.dataLayer.push(p);
  }, push);
  await page.waitForTimeout(9000);
  const fired = reqs.length > 0;
  await page.close();
  return fired;
}

for (const v of VARIANTS) {
  const r6 = await runPred(6, v.push);   // measurement.event_name eq page_view
  const r0 = await runPred(0, v.push);   // analytics_allowed eq true
  const r1 = await runPred(1, v.push);   // consent_version eq 2
  console.log(JSON.stringify({variant: v.label, pred6_measurement_event_name: r6, pred0_analytics_allowed: r0, pred1_consent_version: r1}));
}
await browser.close();
