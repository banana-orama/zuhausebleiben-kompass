// Realistic-traffic probe: headed Chrome window, real UA, 45s engaged dwell, then CTA click.
// GA4 bot filtering may drop headless/short sessions; this maximizes acceptance.
import {chromium} from 'playwright';

const LIVE = 'https://zuhausebleiben-kompass.de/treppenlift-kosten.html';
const collect = [], gtagJs = [], statuses = [];
const browser = await chromium.launch({headless: false, args: ['--window-size=1366,900']});
const ctx = await browser.newContext({
  viewport: {width: 1366, height: 850},
  userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
  locale: 'de-DE', timezoneId: 'Europe/Berlin',
});
const page = await ctx.newPage();
page.on('request', r => {
  const u = r.url();
  if (u.includes('/gtag/js')) gtagJs.push(u.slice(0, 150));
  if (u.includes('/g/collect')) collect.push(u.slice(0, 150));
});
page.on('response', r => { if (r.url().includes('/g/collect')) statuses.push(r.status()); });

await page.goto(LIVE, {waitUntil: 'domcontentloaded', timeout: 45000});
await page.getByRole('button', {name: 'Alle akzeptieren', exact: true}).click({timeout: 15000});
console.log('consent given; dwelling 45s...');
await page.waitForTimeout(45000);
// engagement: scroll + CTA click
await page.evaluate(() => window.scrollTo(0, 800));
await page.waitForTimeout(1500);
await page.locator('[data-cta-id="checklist_top"]').click().catch(e => console.log('cta skip:', e.message.slice(0, 60)));
await page.waitForTimeout(20000);
const state = await page.evaluate(() => ({
  gtagKeys: Object.keys(window.google_tag_manager || {}).filter(k => /^(G-|GT-|GTM-)/.test(k)),
  zbk: (window.dataLayer || []).filter(x => x.event === 'zbk_measurement').length,
}));
console.log(JSON.stringify({gtagJs, collectCount: collect.length, statuses, state}, null, 1));
await browser.close();
