// LOCAL PROOF OF FIX: patch v4 resource macros for measurement.* with vtp_dataLayerVersion:2
// and verify the ORIGINAL full rule set now fires locally.
import {chromium} from 'playwright';
import {readFileSync} from 'node:fs';

const V4 = readFileSync('operations/measurement/v3-fix/gtm-v4.js', 'utf8');
const patched = V4
  .replace('{"function":"__v","vtp_name":"measurement.event_name"}', '{"function":"__v","vtp_dataLayerVersion":2,"vtp_name":"measurement.event_name"}')
  .replace('{"function":"__v","vtp_name":"measurement.content_id"}', '{"function":"__v","vtp_dataLayerVersion":2,"vtp_name":"measurement.content_id"}')
  .replace('{"function":"__v","vtp_name":"measurement.cta_id"}', '{"function":"__v","vtp_dataLayerVersion":2,"vtp_name":"measurement.cta_id"}');
if (patched === V4) { console.error('PATCH DID NOT APPLY'); process.exit(1); }

const browser = await chromium.launch();

async function run(body, label) {
  const page = await (await browser.newContext()).newPage();
  const reqs = [];
  page.on('request', r => { const u = r.url(); if (/gtag\/js|g\/collect/.test(u)) reqs.push(u.slice(0, 160)); });
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
      measurement: {event_name: 'page_view', content_id: 'c04', cta_id: ''}});
    // also simulate the CTA click event for tag 21
    setTimeout(() => window.dataLayer.push({event: 'zbk_measurement', analytics_allowed: true, consent_version: 2,
      consent: {analytics_storage: 'granted', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied'},
      measurement: {event_name: 'cta_click', content_id: 'c04', cta_id: 'checklist_top'}}), 3000);
  });
  await page.waitForTimeout(13000);
  const collect = [];
  page.on('request', r => { const u = r.url(); if (u.includes('/g/collect')) collect.push(u.slice(0, 120)); });
  await page.waitForTimeout(1500);
  const state = await page.evaluate(() => ({
    gtagKeys: Object.keys(window.google_tag_manager || {}).filter(k => /^(G-|GT-)/.test(k)),
  }));
  console.log(JSON.stringify({label, gtagJsRequests: reqs, gtagKeys: state.gtagKeys}));
  await page.close();
}

await run(V4, 'v4 original (expect NO fire)');
await run(patched, 'v4 + dataLayerVersion:2 on measurement vars (expect FIRE)');
await browser.close();
