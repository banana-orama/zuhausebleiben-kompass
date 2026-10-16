// Local repro: serve the REAL v4 gtm.js bytes via route interception on a local page,
// replay the site's exact dataLayer sequence, and watch for googtag registration + gtag/js.
import {chromium} from 'playwright';
import {readFileSync} from 'node:fs';

const V4 = readFileSync('operations/measurement/v3-fix/gtm-v4.js', 'utf8');
const reqs = [], errors = [];
const browser = await chromium.launch();
const page = await (await browser.newContext()).newPage();
page.on('request', r => { const u = r.url(); if (/googletagmanager|google-analytics|g\/collect/.test(u)) reqs.push(u.slice(0, 150)); });
page.on('console', m => { if (m.type() === 'error') errors.push(m.text().slice(0, 200)); });
page.on('pageerror', e => errors.push('PAGEERROR ' + String(e).slice(0, 300)));

await page.route('**//www.googletagmanager.com/gtm.js*', async route => {
  await route.fulfill({contentType: 'text/javascript', body: V4});
});

// minimal replica of the site's consent-default.js + measurement.mjs sequence
await page.goto('data:text/html,<html><head></head><body><h1>probe</h1></body></html>');
await page.evaluate(() => {
  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { window.dataLayer.push(arguments); };
  window.gtag('consent', 'default', {analytics_storage: 'denied', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied'});
  window.gtag('consent', 'update', {analytics_storage: 'granted', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied'});
  window.dataLayer.push({event: 'zbk_consent_update', consent_version: 2, consent: {analytics_storage: 'granted', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied'}});
  // loader injection like the site (script appended after consent)
  const s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtm.js?id=GTM-M9TZZPLQ';
  document.head.appendChild(s);
  // site pushes zbk_measurement AFTER loader insertion (measurement.mjs does it on consent)
  window.dataLayer.push({
    event: 'zbk_measurement', analytics_allowed: true, consent_version: 2,
    consent: {analytics_storage: 'granted', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied'},
    measurement: {event_name: 'page_view', content_id: 'localprobe', cta_id: ''}
  });
});
await page.waitForTimeout(12000);
const state = await page.evaluate(() => {
  const gtm = window.google_tag_manager || {};
  const g = gtm['GTM-M9TZZPLQ'];
  let model = null;
  try {
    model = {
      analytics_allowed: String(g.dataLayer.get('analytics_allowed')),
      consent_version: String(g.dataLayer.get('consent_version')),
      event: String(g.dataLayer.get('_event')),
      measurement_event: String(g.dataLayer.get('measurement.event_name') ?? g.dataLayer.get('measurement')?.event_name),
    };
  } catch (e) { model = 'ERR ' + e.message; }
  return {
    gtmKeys: Object.keys(gtm),
    gtagKeys: Object.keys(gtm).filter(k => /^(G-|GT-)/.test(k)),
    runtimeKeyset: g ? Object.keys(g) : null,
    model,
    events: (window.dataLayer || []).map(x => x.event || 'arg'),
  };
});
console.log(JSON.stringify({reqs, errors: errors.slice(0, 8), state}, null, 1));
await browser.close();
