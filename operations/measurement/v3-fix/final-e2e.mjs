// FINAL live E2E: consent -> zbk_measurement -> gtag/js -> /g/collect, on https://zuhausebleiben-kompass.de
import {chromium} from 'playwright';

const LIVE = 'https://zuhausebleiben-kompass.de/treppenlift-kosten.html';
const gtm = [], gtagJs = [], collect = [], errors = [];
const browser = await chromium.launch();
const page = await (await browser.newContext({viewport: {width: 1280, height: 800}})).newPage();
page.on('console', m => { if (m.type() === 'error') errors.push(m.text().slice(0, 160)); });
page.on('request', r => {
  const u = r.url();
  if (u.includes('googletagmanager.com/gtm.js')) gtm.push(u);
  if (u.includes('/gtag/js')) gtagJs.push(u.slice(0, 180));
  if (u.includes('/g/collect')) collect.push(u.slice(0, 200));
});
page.on('requestfinished', async r => {
  if (r.url().includes('/g/collect')) {
    try { const b = r.postData(); if (b) collect.push('BODY ' + b.slice(0, 400)); } catch {}
  }
});

await page.goto(LIVE, {waitUntil: 'domcontentloaded', timeout: 45000});
await page.getByRole('button', {name: 'Alle akzeptieren', exact: true}).click({timeout: 15000});
await page.waitForTimeout(15000);

// CTA click -> second event via trigger 19/tag 21
await page.locator('[data-cta-id="checklist_top"]').click().catch(() => {});
await page.waitForTimeout(8000);

const state = await page.evaluate(() => ({
  gtmKeys: Object.keys(window.google_tag_manager || {}).filter(k => /^(G-|GT-|GTM-)/.test(k)),
  zbkEvents: (window.dataLayer || []).filter(x => x.event === 'zbk_measurement').map(x => x.measurement),
}));

console.log(JSON.stringify({gtm, gtagJs, collect, state, errors: errors.slice(0, 5)}, null, 1));
await page.screenshot({path: 'operations/measurement/v3-fix/probe-v5-live.png'});
await browser.close();
