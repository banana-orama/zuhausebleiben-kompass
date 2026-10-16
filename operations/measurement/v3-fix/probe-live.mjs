// End-to-end probe of the LIVE site with the real published container (no stubs).
// Consent -> zbk_measurement -> does gtm.js runtime register googtag -> gtag/js request -> /g/collect hit?
import {chromium} from 'playwright';

const LIVE = process.env.PROBE_URL || 'https://zuhausebleiben-kompass.de/treppenlift-kosten.html';
const collect = [], gtagJs = [], loaders = [], errors = [];

const browser = await chromium.launch();
const ctx = await browser.newContext({viewport: {width: 1280, height: 800}});
const page = await ctx.newPage();
page.on('console', m => { if (m.type() === 'error') errors.push(m.text().slice(0, 200)); });
page.on('request', r => {
  const u = r.url();
  if (u.includes('/g/collect')) collect.push(u);
  if (u.includes('/gtag/js')) gtagJs.push(u);
  if (u.includes('googletagmanager.com/gtm.js')) loaders.push(u);
});
page.on('requestfinished', async r => {
  const u = r.url();
  if (u.includes('/g/collect')) {
    try { collect.push('BODY:' + (r.postData() || '').slice(0, 300)); } catch {}
  }
});

await page.goto(LIVE, {waitUntil: 'domcontentloaded', timeout: 45000});
await page.getByRole('button', {name: 'Alle akzeptieren', exact: true}).click({timeout: 15000});

// wait for gtm.js load + runtime registration + potential hits
await page.waitForTimeout(12000);

const state = await page.evaluate(() => {
  const gtm = window.google_tag_manager || {};
  const keys = Object.keys(gtm);
  const gtagKeys = keys.filter(k => /^(G-|GT-|GTM-)/.test(k));
  let dlm = null;
  try { dlm = gtm['GTM-M9TZZPLQ']?.dataLayer?.get?.() ? 'present' : 'absent'; } catch { dlm = 'err'; }
  return {
    gtmKeys: keys,
    gtagKeys,
    dataLayerModel: dlm,
    zbkEvents: (window.dataLayer || []).filter(x => x.event === 'zbk_measurement').length,
    consentEvents: (window.dataLayer || []).filter(x => x.event === 'zbk_consent_update').length,
    gtmJs: (window.dataLayer || []).filter(x => x.event === 'gtm.js').length,
    dom: (window.dataLayer || []).some(x => x.event === 'gtm.dom'),
    load: (window.dataLayer || []).some(x => x.event === 'gtm.load'),
  };
});

console.log(JSON.stringify({
  url: page.url(),
  loaders, gtagJs, collect,
  zbkEvents: state.zbkEvents, consentEvents: state.consentEvents, gtmJs: state.gtmJs,
  gtm_dom: state.dom, gtm_load: state.load,
  gtmKeys: state.gtmKeys, gtagKeys: state.gtagKeys, dataLayerModel: state.dataLayerModel,
  consoleErrors: errors.slice(0, 5),
}, null, 1));

await page.screenshot({path: 'operations/measurement/v3-fix/probe-live-after-consent.png'});
await browser.close();
