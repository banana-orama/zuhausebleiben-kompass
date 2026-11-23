// SVG geometry + screenshot check for treppenlift-weg-entscheidung.svg
// getBBox-vs-viewBox (inside canvas) + pairwise text-on-text overlap + screenshot.
import { chromium } from 'playwright';
const path = await import('path');
const __dirname = '/Users/mac/agentic-business/barrierefrei-leads/research';

(async () => {
  const file = 'file://' + path.resolve(__dirname, '../assets/images/treppenlift-weg-entscheidung.svg');
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1100, height: 780 } });
  await page.goto(file);
  await page.waitForTimeout(400);
  const result = await page.evaluate(() => {
    const svg = document.querySelector('svg');
    const vb = svg.viewBox.baseVal;
    const els = [...svg.querySelectorAll('text, rect, circle, path.line')];
    const boxes = els.map((e, i) => {
      let b;
      try { b = e.getBBox(); } catch { return null; }
      return { i, tag: e.tagName, text: (e.textContent || '').slice(0, 40), x: b.x, y: b.y, w: b.width, h: b.height };
    }).filter(Boolean);
    const overflows = boxes.filter(b => b.x < -1 || b.y < -1 || b.x + b.w > vb.width + 1 || b.y + b.h > vb.height + 1);
    // pairwise text-on-text overlap
    const texts = boxes.filter(b => b.tag === 'text');
    const overlaps = [];
    for (let a = 0; a < texts.length; a++) {
      for (let c = a + 1; c < texts.length; c++) {
        const A = texts[a], B = texts[c];
        const ax2 = A.x + A.w, ay2 = A.y + A.h, bx2 = B.x + B.w, by2 = B.y + B.h;
        const ix = Math.min(ax2, bx2) - Math.max(A.x, B.x);
        const iy = Math.min(ay2, by2) - Math.max(A.y, B.y);
        if (ix > 2 && iy > 2) overlaps.push(`${A.text} <-> ${B.text} (${ix.toFixed(0)}x${iy.toFixed(0)})`);
      }
    }
    // pairwise BOX-on-BOX overlap (Flussdiagramm-Boxen; Hintergrund/Legende ausgeschlossen)
    const flowRects = boxes.filter(b => b.tag === 'rect' && b.w < 700 && b.w > 200 && b.y < 650);
    for (let a = 0; a < flowRects.length; a++) {
      for (let c = a + 1; c < flowRects.length; c++) {
        const A = flowRects[a], B = flowRects[c];
        const ix = Math.min(A.x + A.w, B.x + B.w) - Math.max(A.x, B.x);
        const iy = Math.min(A.y + A.h, B.y + B.h) - Math.max(A.y, B.y);
        if (ix > 2 && iy > 2) overlaps.push(`BOX ${A.x},${A.y} <-> BOX ${B.x},${B.y} (${ix.toFixed(0)}x${iy.toFixed(0)})`);
      }
    }
    return { vb: { w: vb.width, h: vb.height }, n: boxes.length, overflows, overlaps };
  });
  console.log(JSON.stringify(result, null, 2));
  await browser.close();
  process.exit(result.overflows.length || result.overlaps.length ? 1 : 0);
})();
