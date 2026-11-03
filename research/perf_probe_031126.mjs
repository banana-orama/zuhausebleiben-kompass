// Long-Task- + rAF-Gap-Baseline vor Audit #10 (Consent-Deferral).
// rAF-Lücken = Hauptsprung-Blockierspannen (sensitiver als longtask >=50ms);
// zusätzlich Zeitpunkt, wann das Consent-Modal sichtbar wird.
import { chromium } from '@playwright/test';
import { spawn } from 'node:child_process';

const PORT = 4181;
const server = spawn('python3', ['-m', 'http.server', String(PORT), '--bind', '127.0.0.1', '--directory', 'dist'], { stdio: 'ignore' });
await new Promise(r => setTimeout(r, 800));

const pages = ['/index.html', '/treppenlift-kosten.html'];
const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
const results = [];

for (const path of pages) {
  const page = await ctx.newPage();
  await page.addInitScript(() => {
    window.__rafGaps = [];
    window.__rafLast = 0;
    window.__rafStart = performance.now();
    const loop = () => {
      const now = performance.now();
      const gap = now - window.__rafLast;
      if (window.__rafLast > 0 && gap >= 40) window.__rafGaps.push(Math.round(gap));
      window.__rafLast = now;
      if (now - window.__rafStart < 5000) requestAnimationFrame(loop);
    };
    requestAnimationFrame(loop);
  });
  const cdp = await ctx.newCDPSession(page);
  await cdp.send('Emulation.setCPUThrottlingRate', { rate: 4 });
  await page.goto(`http://127.0.0.1:${PORT}${path}`, { waitUntil: 'load' });
  let bannerMs = null;
  try {
    const t0 = Date.now();
    await page.waitForSelector('#cc-main .cm__btns', { state: 'visible', timeout: 8000 });
    bannerMs = Date.now() - t0;
  } catch {}
  await page.waitForTimeout(5200);
  const gaps = await page.evaluate(() => window.__rafGaps);
  const blocked = gaps.reduce((s, g) => s + g, 0);
  results.push({ page: path, rafGaps40ms: gaps.length, blockedMsTotal: Math.round(blocked), biggestGapMs: gaps.length ? Math.max(...gaps) : 0, bannerVisibleAfterGotoMs: bannerMs });
  await page.close();
}

await browser.close();
server.kill();
console.log(JSON.stringify(results, null, 2));
