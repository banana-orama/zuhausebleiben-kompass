// Sichtkontrolle Schmale-Treppe-Artikel (26.10.2026): Mobile 390px Overflow-Check + Struktur + Checklisten-Anker.
// Muster: browser_check_steuer_261026.mjs. Lädt lokal gebaute dist-Seite in echtem Chromium.
import { chromium } from 'playwright-core';
import { pathToFileURL } from 'node:url';
import path from 'node:path';

const ROOT = process.cwd();
const pageFile = path.join(ROOT, 'dist', 'treppenlift-schmale-treppe.html');

const browser = await chromium.launch({ headless: true });
let fail = 0;

const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
await page.goto(pathToFileURL(pageFile).href, { waitUntil: 'load' });
const m = await page.evaluate(() => {
  const doc = document.documentElement;
  const checklist = [...document.querySelectorAll('a[data-cta-id="checklist_top"]')].pop();
  const target = checklist ? document.querySelector(checklist.getAttribute('href')) : null;
  return {
    scrollW: doc.scrollWidth, innerW: window.innerWidth,
    h1: document.querySelector('h1')?.textContent?.slice(0, 60),
    sources: document.querySelectorAll('.sources ol li').length,
    img: !!document.querySelector('figure img'),
    faq: document.querySelectorAll('.faq details').length,
    compareCta: document.querySelector('a[data-cta-id="compare_top"]')?.getAttribute('href'),
    checklistHref: checklist?.getAttribute('href') || null,
    checklistTargetExists: !!target,
    related: [...document.querySelectorAll('.related a')].map(a => a.getAttribute('href')),
  };
});
console.log('mobile:', JSON.stringify(m, null, 1));
if (m.scrollW > m.innerW) { console.log(`FAIL mobile overflow: scrollW ${m.scrollW} > ${m.innerW}`); fail++; }
else console.log('PASS mobile kein Overflow');
if (m.sources !== 5 || !m.img || m.faq !== 6) { console.log('FAIL mobile Struktur (erwarte 5 Quellen, Grafik, 6 FAQs)'); fail++; }
else console.log('PASS mobile Struktur (5 Quellen, Grafik, 6 FAQs)');
if (!m.compareCta || !m.compareCta.includes('treppenlift-firmen-vergleich.html')) { console.log('FAIL Early-CTA-Ziel'); fail++; }
else console.log('PASS Early-CTA -> treppenlift-firmen-vergleich');
if (!m.checklistHref || !m.checklistTargetExists) { console.log('FAIL Checklisten-Anker'); fail++; }
else console.log('PASS Checklisten-Anker: ' + m.checklistHref);
const relOk = m.related.length === 3 && m.related.every(h => h.includes('treppenlift'));
if (!relOk) { console.log('FAIL related links: ' + JSON.stringify(m.related)); fail++; }
else console.log('PASS related 3x lift-cluster');

await page.screenshot({ path: 'research/evidence/schmale-treppe-261026/mobile-artikel.png', fullPage: false });

const figWidth = await page.evaluate(() => Math.round(document.querySelector('figure img')?.getBoundingClientRect().width || 0));
console.log('figure image width @390px:', figWidth);
if (figWidth < 100) { console.log('FAIL Grafik zu schmal'); fail++; }

console.log(fail === 0 ? 'SICHTKONTROLLE: alle PASS' : `SICHTKONTROLLE: ${fail} FAIL`);
await browser.close();
process.exit(fail === 0 ? 0 : 1);
