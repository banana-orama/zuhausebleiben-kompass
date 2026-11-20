// Wrap SVG in an HTML page (page.screenshot on raw SVG documents hangs) and capture.
import { chromium } from 'playwright';
import path from 'node:path';

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1040, height: 900 } });
  const html = `<!doctype html><meta charset="utf-8"><body style="margin:0"><img src="file://${path.resolve('assets/images/hausnotruf-paare-konstellationen.svg')}" width="1000" style="display:block"></body>`;
  await page.setContent(html, { waitUntil: 'load' });
  await page.waitForTimeout(400);
  await page.screenshot({ path: 'research/evidence/paare-191126/svg-render-201126.png', fullPage: true });
  console.log('saved research/evidence/paare-191126/svg-render-201126.png');
  await browser.close();
})();
