// Mobile 390px overflow + screenshot for the new SACHSEN region page (LAUNCH dist build).
import { chromium } from 'playwright';
const path = await import('path');

(async () => {
  const file = 'file://' + path.resolve('/Users/mac/agentic-business/barrierefrei-leads/dist/region/sachsen.html');
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
    const h2s = [...document.querySelectorAll('h2')].map(h => h.textContent.trim()).slice(0, 12);
    const tbl = [...document.querySelectorAll('.table-scroll')].length;
    const faqs = document.querySelectorAll('details').length;
    const sources = document.querySelectorAll('.sources ol li').length;
    return { overflowX, widest, h2s, tables: tbl, faqs, sources };
  });
  console.log(JSON.stringify(r, null, 2));
  await page.screenshot({ path: '/Users/mac/.hermes/profiles/milo/cache/scratch/sachsen_mobile_241126.png', fullPage: true, timeout: 20000 });
  await browser.close();
  process.exit(r.overflowX > 0 ? 1 : 0);
})();
