// Fork experiment on the LIVE site with v4 runtime:
// A) hook DOM script creation + push fresh zbk_measurement -> does the googtag body even attempt an injection?
// B) inject gtag/js directly for G-5738T8FHWW (bypassing GTM) -> does the Google side load + hit /g/collect?
import {chromium} from 'playwright';

const LIVE = 'https://zuhausebleiben-kompass.de/treppenlift-kosten.html';
const gtagJs = [], collect = [], errors = [], scripts = [];

const browser = await chromium.launch();
const page = await (await browser.newContext({viewport: {width: 1280, height: 800}})).newPage();
page.on('console', m => { if (m.type() === 'error') errors.push(m.text().slice(0, 160)); });
page.on('request', r => {
  const u = r.url();
  if (u.includes('/gtag/js')) gtagJs.push('REQ ' + u.slice(0, 180));
  if (u.includes('/g/collect')) collect.push('REQ ' + u.slice(0, 180));
});

await page.addInitScript(() => {
  window.__scriptLog = [];
  const orig = document.createElement.bind(document);
  document.createElement = function (tag) {
    const el = orig.apply(this, arguments);
    if (String(tag).toLowerCase() === 'script') {
      const rec = {t: Date.now(), src: '(set later)'};
      window.__scriptLog.push(rec);
      let s = el.src;
      Object.defineProperty(el, 'src', {get() { return s; }, set(v) { s = v; rec.src = String(v).slice(0, 180); }});
    }
    return el;
  };
  const append = Node.prototype.appendChild;
  Node.prototype.appendChild = function (child) {
    if (child && child.tagName === 'SCRIPT' && child.src) {
      window.__scriptLog.push({t: Date.now(), appended: String(child.src).slice(0, 180)});
    }
    return append.apply(this, arguments);
  };
});

await page.goto(LIVE, {waitUntil: 'domcontentloaded', timeout: 45000});
await page.getByRole('button', {name: 'Alle akzeptieren', exact: true}).click({timeout: 15000});
await page.waitForTimeout(9000);

// A) fresh push with DOM hooks in place
await page.evaluate(() => {
  window.__aMark = window.__scriptLog.length;
  window.dataLayer.push({
    event: 'zbk_measurement', analytics_allowed: true, consent_version: 2,
    consent: {analytics_storage: 'granted', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied'},
    measurement: {event_name: 'page_view', content_id: 'probe_a', cta_id: ''}
  });
});
await page.waitForTimeout(6000);
const aLog = await page.evaluate(() => ({
  totalScripts: window.__scriptLog.length,
  sinceAMark: window.__scriptLog.slice(window.__aMark),
  gtmKeys: Object.keys(window.google_tag_manager || {}).filter(k => /^(G-|GT-)/.test(k)),
  resourceEntries: performance.getEntriesByType('resource').filter(r => /gtag\/js|g\/collect/.test(r.name)).map(r => r.name.slice(0, 140)),
}));

// B) direct gtag/js injection, bypassing GTM entirely
const bLog = await page.evaluate(() => new Promise((resolve) => {
  const s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=G-5738T8FHWW&l=zbkDirectDataLayer';
  window.zbkDirectDataLayer = window.zbkDirectDataLayer || [];
  s.onload = () => resolve({loaded: true});
  s.onerror = (e) => resolve({loaded: false, error: String(e).slice(0, 120)});
  document.head.appendChild(s);
  setTimeout(() => resolve({loaded: false, error: 'timeout 15s'}), 15000);
}));
await page.waitForTimeout(8000);
const bState = await page.evaluate(() => ({
  directGtagKeys: Object.keys(window.google_tag_manager || {}).filter(k => k.startsWith('G-')),
  directLayerLen: (window.zbkDirectDataLayer || []).length,
  bScriptLog: window.__scriptLog.slice(-6),
}));

console.log(JSON.stringify({gtagJs, collect, aLog, bLog, bState, errors: errors.slice(0, 6)}, null, 1));
await browser.close();
