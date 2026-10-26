// Sichtkontrolle Steuer-Artikel (26.10.2026): Mobile 390px Overflow-Check + SVG-Textgrenzen.
// Muster: browser_check_foerder_2610.mjs. Lädt lokal gebaute dist-Seite + SVG in echtem Chromium.
import { chromium } from 'playwright-core';
import { pathToFileURL } from 'node:url';
import path from 'node:path';

const ROOT = process.cwd();
const pageFile = path.join(ROOT, 'dist', 'treppenlift-steuerlich-absetzen.html');
const svgFile = path.join(ROOT, 'assets', 'images', 'treppenlift-steuer-weg.svg');

const browser = await chromium.launch({ headless: true });
let fail = 0;

// --- 1) Mobile 390px ---
const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
await page.goto(pathToFileURL(pageFile).href, { waitUntil: 'load' });
const m = await page.evaluate(() => {
  const doc = document.documentElement;
  return {
    scrollW: doc.scrollWidth, innerW: window.innerWidth,
    h1: document.querySelector('h1')?.textContent?.slice(0, 60),
    sources: document.querySelectorAll('.sources ol li').length,
    img: !!document.querySelector('figure img'),
    tables: document.querySelectorAll('.table-scroll').length,
    faq: document.querySelectorAll('.faq details').length,
  };
});
console.log('mobile:', JSON.stringify(m));
if (m.scrollW > m.innerW) { console.log(`FAIL mobile overflow: scrollW ${m.scrollW} > ${m.innerW}`); fail++; }
else console.log('PASS mobile kein Overflow');
if (m.sources !== 4 || !m.img || m.faq !== 6) { console.log('FAIL mobile Struktur'); fail++; }
else console.log('PASS mobile Struktur (4 Quellen, Grafik, 6 FAQs)');
await page.screenshot({ path: 'research/evidence/steuer-261026/mobile-artikel.png', fullPage: false });

// SVG im Seitenkontext sichtbar?
const svgBox = await page.evaluate(() => {
  const img = document.querySelector('figure img');
  const r = img.getBoundingClientRect();
  return { w: Math.round(r.width), visible: r.width > 100 };
});
console.log('figure image width @390px:', JSON.stringify(svgBox));
if (!svgBox.visible) { console.log('FAIL Grafik zu schmal'); fail++; }

// --- 2) SVG-Textgrenzen (getBBox je Textknoten vs viewBox 980x740) ---
const p2 = await browser.newPage({ viewport: { width: 1000, height: 800 } });
await p2.goto(pathToFileURL(svgFile).href, { waitUntil: 'load' });
const over = await p2.evaluate(() => {
  const svg = document.querySelector('svg');
  const vb = svg.viewBox.baseVal;
  const bad = [];
  for (const t of svg.querySelectorAll('text')) {
    const b = t.getBBox();
    if (b.x < 0 || b.y < 0 || b.x + b.width > vb.width || b.y + b.height > vb.height) {
      bad.push({ text: t.textContent.slice(0, 50), x: Math.round(b.x), y: Math.round(b.y), r: Math.round(b.x + b.width), b: Math.round(b.y + b.height) });
    }
  }
  return { vw: vb.width, vh: vb.height, bad };
});
console.log('svg viewBox:', over.vw, 'x', over.vh, '| Texte außerhalb:', over.bad.length);
for (const b of over.bad) console.log('  OVERFLOW', JSON.stringify(b));
if (over.bad.length) fail++;
await p2.screenshot({ path: 'research/evidence/steuer-261026/svg-vollansicht.png', fullPage: true });

console.log(fail === 0 ? 'SICHTKONTROLLE: alle PASS' : `SICHTKONTROLLE: ${fail} FAIL`);
await browser.close();
process.exit(fail === 0 ? 0 : 1);
