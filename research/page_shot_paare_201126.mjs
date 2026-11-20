// Screenshot the figure SVG inside the BUILT article page (real render context) + mobile check.
import { chromium } from 'playwright';
import path from 'node:path';

(async () => {
  const url = 'file://' + path.resolve('dist/hausnotruf-fuer-paare.html');
  const browser = await chromium.launch();
  // desktop figure shot
  const page = await browser.newPage({ viewport: { width: 1280, height: 1000 } });
  await page.goto(url, { waitUntil: 'load' });
  await page.waitForTimeout(500);
  const fig = page.locator('figure').first();
  await fig.screenshot({ path: 'research/evidence/paare-191126/svg-in-page-201126.png' });
  console.log('figure shot saved');
  // mobile full page
  const mob = await browser.newPage({ viewport: { width: 390, height: 844 } });
  await mob.goto(url, { waitUntil: 'load' });
  await mob.waitForTimeout(500);
  const overflow = await mob.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  console.log('mobile horizontal overflow px:', overflow);
  await mob.screenshot({ path: 'research/evidence/paare-191126/mobile-artikel-201126.png', fullPage: false });
  console.log('mobile shot saved');
  await browser.close();
})();
