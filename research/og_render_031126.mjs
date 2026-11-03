// Rendert das OG-Design (1200x630) nach PNG — Audit #6b.
import { chromium } from '@playwright/test';

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1200, height: 630 } });
await page.goto('file:///Users/mac/agentic-business/barrierefrei-leads/assets/images/og-zuhausebleiben-kompass.svg');
await page.waitForTimeout(400);
await page.screenshot({ path: 'research/evidence/perf-og-031126/og-render.png', clip: { x: 0, y: 0, width: 1200, height: 630 } });
await browser.close();
console.log('PNG geschrieben');
