// Local bisect rig: serve edited v4 bytes with progressively relaxed rule sets to find
// whether predicate evaluation or tag execution is the failing stage.
import {chromium} from 'playwright';
import {readFileSync} from 'node:fs';

const V4 = readFileSync('operations/measurement/v3-fix/gtm-v4.js', 'utf8');
const RULES_ORIG = '"rules":[[["if",0,1,2,3,4,5,6,7],["add",0]],[["if",0,1,2,3,4,5,7,8],["add",1]]]';

const VARIANTS = {
  T0_orig: RULES_ORIG,
  T1_event_only: '"rules":[[["if",7],["add",0]],[["if",7,8],["add",1]]]',
  T2_unconditional: '"rules":[[["add",0]],[["add",1]]]',
};

const browser = await chromium.launch();

async function runVariant(name, rules) {
  const body = V4.replace(RULES_ORIG, rules);
  if (body === V4 && rules !== RULES_ORIG) throw new Error('rule replace failed for ' + name);
  const page = await (await browser.newContext()).newPage();
  const reqs = [];
  page.on('request', r => { const u = r.url(); if (/gtag\/js|g\/collect/.test(u)) reqs.push(u.slice(0, 140)); });
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
      measurement: {event_name: 'page_view', content_id: name, cta_id: ''}});
  });
  await page.waitForTimeout(10000);
  const state = await page.evaluate(() => ({
    gtagKeys: Object.keys(window.google_tag_manager || {}).filter(k => /^(G-|GT-)/.test(k)),
    runtimeInstalled: !!window.google_tag_manager?.['GTM-M9TZZPLQ'],
  }));
  await page.close();
  return {name, reqs, ...state};
}

const out = [];
for (const [name, rules] of Object.entries(VARIANTS)) {
  out.push(await runVariant(name, rules));
  console.log(JSON.stringify(out[out.length - 1]));
}
await browser.close();
