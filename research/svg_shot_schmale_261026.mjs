// SVG-Sichtprobe fuer schmale-treppe-messplan: Screenshot + getBBox-Overflow-Check
// (prueft JEDE Text-/Form-Box gegen die viewBox; string-Heuristik bewusst nicht genutzt).
import { chromium } from 'playwright-core';
import { pathToFileURL } from 'node:url';
import path from 'node:path';

const svgFile = path.join(process.cwd(), 'assets', 'images', 'treppenlift-schmale-treppe-messplan.svg');
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 990, height: 700 } });
await page.goto(pathToFileURL(svgFile).href, { waitUntil: 'load' });
await page.waitForTimeout(300);
await page.screenshot({ path: 'research/evidence/schmale-treppe-261026/svg-vollansicht.png', timeout: 15000 });

const overflows = await page.evaluate(() => {
  const svg = document.querySelector('svg');
  const vb = svg.viewBox.baseVal;
  const out = [];
  for (const el of svg.querySelectorAll('text, rect, circle, path, line')) {
    const bb = el.getBBox();
    if (bb.x < -1 || bb.y < -1 || bb.x + bb.width > vb.width + 1 || bb.y + bb.height > vb.height + 1) {
      out.push(`${el.tagName} "${(el.textContent || '').trim().slice(0, 40)}" bbox=[${bb.x.toFixed(1)},${bb.y.toFixed(1)},${(bb.x + bb.width).toFixed(1)},${(bb.y + bb.height).toFixed(1)}] vs viewBox ${vb.width}x${vb.height}`);
    }
  }
  return out;
});
console.log('viewBox overflow elements:', overflows.length);
for (const o of overflows) console.log('  OVERFLOW:', o);

// Kollisionsprobe: rechte Karten vs. linker Planbereich
const boxes = await page.evaluate(() => {
  const svg = document.querySelector('svg');
  const res = [];
  for (const el of svg.querySelectorAll('rect')) {
    const bb = el.getBBox();
    res.push({ tag: 'rect', x: bb.x, y: bb.y, w: bb.width, h: bb.height });
  }
  return res;
});
console.log('rect boxes:', JSON.stringify(boxes));
await browser.close();
