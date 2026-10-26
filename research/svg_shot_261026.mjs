// SVG-Sichtprobe: Viewport-Screenshot der Gerenderten Grafik (ohne fullPage-Hänger).
import { chromium } from 'playwright-core';
import { pathToFileURL } from 'node:url';
import path from 'node:path';

const svgFile = path.join(process.cwd(), 'assets', 'images', 'treppenlift-steuer-weg.svg');
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 990, height: 760 } });
await page.goto(pathToFileURL(svgFile).href, { waitUntil: 'load' });
await page.waitForTimeout(300);
await page.screenshot({ path: 'research/evidence/steuer-261026/svg-vollansicht.png', timeout: 15000 });
console.log('screenshot saved');
await browser.close();
