// Audit #10 Nachweis v2: exakte Zeiten für CMP-DOM-Insert + Sichtbarkeit vs. load-Event.
import { chromium } from '@playwright/test';
import { spawn } from 'node:child_process';

const PORT = 4183;
const server = spawn('python3', ['-m', 'http.server', String(PORT), '--bind', '127.0.0.1', '--directory', 'dist'], { stdio: 'ignore' });
await new Promise(r => setTimeout(r, 800));

const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
const page = await ctx.newPage();

await page.addInitScript(() => {
  window.__marks = { loadAt: null, domAt: null, ricFiredAt: null };
  window.addEventListener('load', () => { window.__marks.loadAt = performance.now(); });
  if (window.requestIdleCallback) {
    const orig = window.requestIdleCallback.bind(window);
    window.requestIdleCallback = (cb, opts) => orig(deadline => { window.__marks.ricFiredAt = performance.now(); cb(deadline); }, opts);
  }
  const timer = setInterval(() => {
    const el = document.querySelector('#cc-main .cm__btns');
    if (el && window.__marks.domAt === null) {
      const r = el.getBoundingClientRect();
      window.__marks.domAt = performance.now();
      window.__marks.rectH = Math.round(r.height);
      clearInterval(timer);
    }
  }, 8);
  setTimeout(() => clearInterval(timer), 15000);
});

const t0 = Date.now();
await page.goto(`http://127.0.0.1:${PORT}/index.html`, { waitUntil: 'load' });
await page.waitForSelector('#cc-main .cm__btns', { state: 'visible', timeout: 8000 });
const visibleWallMs = Date.now() - t0;
await page.waitForTimeout(300);
const m = await page.evaluate(() => window.__marks);

console.log(JSON.stringify({
  ricFiredAtMs: m.ricFiredAt === null ? null : Math.round(m.ricFiredAt),
  loadEventAtMs: m.loadAt === null ? null : Math.round(m.loadAt),
  bannerDomAtMs: m.domAt === null ? null : Math.round(m.domAt),
  bannerRectHeightPx: m.rectH ?? null,
  bannerVisibleWallMsAfterGoto: visibleWallMs,
  domAfterLoadEvent: m.domAt !== null && m.loadAt !== null && m.domAt > m.loadAt,
  ricAfterLoadEvent: m.ricFiredAt !== null && m.loadAt !== null && m.ricFiredAt > m.loadAt
}, null, 2));

await browser.close();
server.kill();
