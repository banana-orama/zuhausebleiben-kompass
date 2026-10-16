// HOOK-FREE decisive test on live site: consent -> container loads -> fresh zbk_measurement push
// -> does ANY gtag/js request appear (GTM-initiated)? Then direct-inject gtag/js (plain and &l= variants).
import {chromium} from 'playwright';

const LIVE = 'https://zuhausebleiben-kompass.de/treppenlift-kosten.html';
const reqs = [];
const browser = await chromium.launch();
const page = await (await browser.newContext({viewport: {width: 1280, height: 800}})).newPage();
page.on('request', r => {
  const u = r.url();
  if (/googletagmanager\.com|google-analytics\.com|\/g\/collect/.test(u)) reqs.push({t: Date.now(), url: u.slice(0, 170)});
});

await page.goto(LIVE, {waitUntil: 'domcontentloaded', timeout: 45000});
const t0 = Date.now();
await page.getByRole('button', {name: 'Alle akzeptieren', exact: true}).click({timeout: 15000});
await page.waitForTimeout(9000);
const state1 = await page.evaluate(() => ({
  gtmInstalled: !!window.google_tag_manager?.['GTM-M9TZZPLQ'],
  zbk: (window.dataLayer || []).filter(x => x.event === 'zbk_measurement').length,
}));

// fresh push, GTM-initiated path
await page.evaluate(() => window.dataLayer.push({
  event: 'zbk_measurement', analytics_allowed: true, consent_version: 2,
  consent: {analytics_storage: 'granted', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied'},
  measurement: {event_name: 'page_view', content_id: 'probe_clean', cta_id: ''}
}));
await page.waitForTimeout(7000);

// direct injection plain URL (post-container)
const directPlain = await page.evaluate(() => new Promise((res) => {
  const s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=G-5738T8FHWW';
  s.onload = () => res('LOADED');
  s.onerror = () => res('ERROR');
  document.head.appendChild(s);
  setTimeout(() => res('TIMEOUT'), 15000);
}));
await page.waitForTimeout(5000);

// direct injection with &l= param (post-container)
const directL = await page.evaluate(() => new Promise((res) => {
  window.zbkDirectLayer = window.zbkDirectLayer || [];
  const s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=G-5738T8FHWW&l=zbkDirectLayer';
  s.onload = () => res('LOADED');
  s.onerror = () => res('ERROR');
  document.head.appendChild(s);
  setTimeout(() => res('TIMEOUT'), 15000);
}));
await page.waitForTimeout(8000);

const state2 = await page.evaluate(() => ({
  gtagKeys: Object.keys(window.google_tag_manager || {}).filter(k => /^(G-|GT-)/.test(k)),
  directLayerLen: (window.zbkDirectLayer || []).length,
  gtmStillInstalled: !!window.google_tag_manager?.['GTM-M9TZZPLQ'],
}));

console.log(JSON.stringify({
  state1, directPlain, directL, state2,
  requests: reqs.map(r => ({dt: r.t - t0, url: r.url})),
}, null, 1));
await browser.close();
