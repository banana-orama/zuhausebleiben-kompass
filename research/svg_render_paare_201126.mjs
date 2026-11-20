// True render check: load the paare SVG (file URL), assert element extents inside viewBox, screenshot.
import { chromium } from 'playwright';
import path from 'node:path';

(async () => {
  const file = 'file://' + path.resolve('dist/assets/images/hausnotruf-paare-konstellationen.svg');
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1040, height: 900 } });
  await page.goto(file);
  await page.waitForTimeout(300);
  const report = await page.evaluate(() => {
    const svg = document.querySelector('svg');
    const vb = svg.viewBox.baseVal;
    const out = [];
    svg.querySelectorAll('text, rect, circle, line, path').forEach(el => {
      try {
        const b = el.getBBox();
        if (b.x < -1 || b.y < -1 || b.x + b.width > vb.width + 1 || b.y + b.height > vb.height + 1) {
          out.push({ tag: el.tagName, text: (el.textContent || '').slice(0, 40), box: [Math.round(b.x), Math.round(b.y), Math.round(b.width), Math.round(b.height)] });
        }
      } catch (e) { /* skip non-renderable */ }
    });
    return { viewBox: `${vb.width}x${vb.height}`, overflows: out };
  });
  console.log('viewBox:', report.viewBox);
  console.log('out-of-viewBox elements:', report.overflows.length ? JSON.stringify(report.overflows, null, 1) : 'NONE');
  await page.screenshot({ path: 'research/evidence/paare-191126/svg-render-201126.png', fullPage: true });
  console.log('screenshot saved: research/evidence/paare-191126/svg-render-201126.png');
  await browser.close();
})();
