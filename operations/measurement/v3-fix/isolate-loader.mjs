// Isolate the gtag/js load failure: neutral page vs live site; service worker detection;
// same-origin vs cross-origin script fetch behavior in this exact browser.
import {chromium} from 'playwright';

const browser = await chromium.launch();
const results = {};

// --- 1) neutral page (example.com) ---
{
  const page = await (await browser.newContext()).newPage();
  const reqs = [];
  page.on('request', r => { if (r.url().includes('googletagmanager.com')) reqs.push(r.url().slice(0, 140)); });
  await page.goto('https://example.com', {waitUntil: 'domcontentloaded', timeout: 30000});
  const load = await page.evaluate(() => new Promise((res) => {
    const s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=G-5738T8FHWW';
    s.onload = () => res('LOADED');
    s.onerror = () => res('ERROR');
    document.head.appendChild(s);
    setTimeout(() => res('TIMEOUT'), 15000);
  }));
  await page.waitForTimeout(4000);
  results.neutralPage = {load, reqs, gtagKeys: await page.evaluate(() => Object.keys(window.google_tag_manager || {}).filter(k => /^(G-|GT-|GTM-)/.test(k)))};
  await page.close();
}

// --- 2) live site: SW check + script load + fetch() comparison ---
{
  const page = await (await browser.newContext()).newPage();
  const reqs = [], failures = [];
  page.on('request', r => { if (r.url().includes('googletagmanager.com')) reqs.push(r.url().slice(0, 140)); });
  page.on('requestfailed', r => { if (r.url().includes('googletagmanager.com')) failures.push({url: r.url().slice(0, 140), err: r.failure()?.errorText}); });
  await page.goto('https://zuhausebleiben-kompass.de/treppenlift-kosten.html', {waitUntil: 'domcontentloaded', timeout: 45000});
  const sw = await page.evaluate(async () => ({
    controller: navigator.serviceWorker?.controller?.scriptURL || null,
    registrations: await navigator.serviceWorker?.getRegistrations?.().then(rs => rs.map(r => ({scope: r.scope, active: !!r.active}))) || [],
  }));
  const load = await page.evaluate(() => new Promise((res) => {
    const s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=G-5738T8FHWW';
    s.onload = () => res('LOADED');
    s.onerror = () => res('ERROR');
    document.head.appendChild(s);
    setTimeout(() => res('TIMEOUT'), 15000);
  }));
  await page.waitForTimeout(4000);
  const fetchTest = await page.evaluate(async () => {
    try {
      const r = await fetch('https://www.googletagmanager.com/gtag/js?id=G-5738T8FHWW', {mode: 'no-cors'});
      return {fetchStatus: r.status, fetchType: r.type};
    } catch (e) { return {fetchError: String(e).slice(0, 120)}; }
  });
  results.liveSite = {sw, load, reqs, failures, fetchTest};
  await page.close();
}

console.log(JSON.stringify(results, null, 1));
await browser.close();
