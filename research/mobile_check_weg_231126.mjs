// Mobile 390px overflow + screenshot for the new WEG article (LAUNCH dist build).
import { chromium } from 'playwright';
const path = await import('path');

(async () => {
  const file = 'file://' + path.resolve('/Users/mac/agentic-business/barrierefrei-leads/dist/treppenlift-eigentumswohnung-weg.html');
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
  await page.goto(file);
  await page.waitForTimeout(600);
  const r = await page.evaluate(() => {
    const doc = document.documentElement;
    const overflowX = Math.max(doc.scrollWidth - window.innerWidth, 0);
    const widest = [...document.querySelectorAll('body *')].map(e => {
      const b = e.getBoundingClientRect();
      return { tag: e.tagName, cls: (e.className || '').toString().slice(0, 30), right: Math.round(b.right) };
    }).filter(e => e.right > window.innerWidth + 1).slice(0, 5);
    const h2s = [...document.querySelectorAll('h2')].map(h => h.textContent.trim()).slice(0, 8);
    const fig = document.querySelector('.editorial-figure img');
    return { overflowX, widest, h2s, figOk: !!fig && fig.naturalWidth === 0 ? 'not-loaded' : 'ok', consent: !!document.querySelector('#cookie-consent, .cc-banner, [class*="consent"]') };
  });
  console.log(JSON.stringify(r, null, 2));
  await page.screenshot({ path: '/Users/mac/.hermes/profiles/milo/cache/scratch/weg_mobile_231126.png', timeout: 20000 });
  await browser.close();
  process.exit(r.overflowX > 0 ? 1 : 0);
})();
