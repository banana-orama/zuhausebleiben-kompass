import {test, expect} from '@playwright/test';
import {readFileSync} from 'node:fs';
import {join, dirname} from 'node:path';
import {fileURLToPath} from 'node:url';

// Printable checklist hub (dist/checklisten): render + print CSS, source-article back links,
// content integrity against the article JSONs, mode-consistent robots, consent/no-PII contract.
const ROOT = dirname(fileURLToPath(import.meta.url)) + '/..';
const BASE = 'https://zuhausebleiben-kompass.de';

// Mirrors the CHECKLISTS config in scripts/build-checklists.mjs ([type, sectionIndex] per block).
// If the builder's extraction config changes, update this map in the same change.
const CHECKLISTS = {
  'pflegegrad-antrag-ablauf-fristen': [['ol', 1], ['table', 2], ['ol', 3]],
  'hilfsmittel-pflegekasse-uebernahme': [['ol', 5], ['table', 2], ['table', 3]],
  'hausnotruf-kosten-anbieter-vergleich': [['ul', 5], ['table', 2]],
  'treppenlift-firmen-vergleich': [['table', 6], ['ol', 7], ['ul', 4]],
  'tuerbreiten-schwellen-schnellcheck': [['ul', 0], ['table', 2], ['ul', 6]],
  'badumbau-angebote-vergleichen': [['table', 2], ['ol', 7], ['ul', 0]],
};
const SLUGS = Object.keys(CHECKLISTS);

const article = slug => JSON.parse(readFileSync(join(ROOT, 'content-ready', slug + '.json'), 'utf8'));
const norm = s => String(s).replace(/_{3,}/g, ' ').replace(/\s+/g, ' ').trim();
// The checklist pages must ship the same robots state as the rest of the build (npm test
// leaves the PREVIEW dist in place; CI's build:launch leaves LAUNCH). Never hard-code a mode here.
const siteRobots = readFileSync(join(ROOT, 'dist/index.html'), 'utf8').match(/<meta name="robots" content="([^"]+)"/)[1];

// Absolute first-party URLs must hit the local build, never production (same contract as consent.spec.mjs).
test.beforeEach(async ({page}) => {
  await page.route('https://zuhausebleiben-kompass.de/**', async route => {
    const u = new URL(route.request().url());
    await route.fulfill({response: await route.fetch({url: 'http://127.0.0.1:4179' + u.pathname + u.search})});
  });
});

test('checklists hub is discoverable and lists every checklist with a working link', async ({page}) => {
  // Site-wide nav carries the hub (not an orphan).
  const home = readFileSync(join(ROOT, 'dist/index.html'), 'utf8');
  expect(home).toContain('href="https://zuhausebleiben-kompass.de/checklisten/index.html"');
  await page.goto('/checklisten/index.html');
  await expect(page.locator('h1')).toContainText('Checklisten');
  const cards = page.locator('.check-card');
  await expect(cards).toHaveCount(SLUGS.length);
  for (const slug of SLUGS) {
    await expect(page.locator(`a[href="${BASE}/checklisten/${slug}.html"]`)).toHaveCount(1);
    // Every card also links back to its source article.
    await expect(page.locator(`a[href="${BASE}/${slug}.html"]`).first()).toBeAttached();
  }
  // Structured data must parse and enumerate the checklists.
  const ld = await page.evaluate(() => JSON.parse(document.querySelector('script[type="application/ld+json"]').textContent));
  expect(ld['@context']).toBe('https://schema.org');
  const collection = ld['@graph'].find(n => n['@type'] === 'CollectionPage');
  const list = ld['@graph'].find(n => n['@type'] === 'ItemList');
  expect(collection.url).toBe(`${BASE}/checklisten/index.html`);
  expect(list.itemListElement).toHaveLength(SLUGS.length);
});

for (const slug of SLUGS) {
  test(`${slug}: renders complete extracted content with print CSS and consent contract`, async ({page}) => {
    const a = article(slug);
    await page.goto(`/checklisten/${slug}.html`);
    await expect(page.locator('h1')).toContainText('Checkliste');

    // Robots mirrors the build mode; canonical and source-back link are correct.
    await expect(page.locator('meta[name="robots"]')).toHaveAttribute('content', siteRobots);
    await expect(page.locator('link[rel="canonical"]')).toHaveAttribute('href', `${BASE}/checklisten/${slug}.html`);
    await expect(page.locator('.source-back a')).toHaveAttribute('href', `${BASE}/${slug}.html`);

    // Every configured block exists, in order, with content actually extracted from the source article.
    const blocks = page.locator('.check-block');
    await expect(blocks).toHaveCount(CHECKLISTS[slug].length);
    const normBody = norm(await page.locator('main').textContent());
    for (let i = 0; i < CHECKLISTS[slug].length; i++) {
      const [type, sec] = CHECKLISTS[slug][i];
      const section = a.sections[sec];
      const block = blocks.nth(i);
      if (type === 'ol' || type === 'ul') {
        const items = type === 'ol' ? block.locator('ol > li') : block.locator('ul.checklist > li');
        expect(await items.count()).toBe(section.bullets.length);
        // First bullet of the source section verbatim (normalized) on the sheet.
        expect(normBody).toContain(norm(section.bullets[0]));
      } else {
        expect(normBody).toContain(norm(section.table.headers[0]));
        expect(normBody).toContain(norm(section.table.rows[0][0]));
      }
    }

    // Print affordance: button + A4 print stylesheet.
    await expect(page.locator('.print-button')).toHaveCount(1);
    const styles = await page.evaluate(() => Array.from(document.querySelectorAll('style')).map(s => s.textContent).join(''));
    expect(styles).toContain('@media print');
    expect(styles).toContain('@page');

    // Consent contract: synchronous denied bootstrap, no tracking loaders, no forms
    // (printable assets collect nothing), KI disclosure in the footer.
    const state = await page.evaluate(() => window.zbkConsent?.state);
    expect(state).toEqual({analytics_storage: 'denied', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied'});
    const entries = await page.evaluate(() => window.dataLayer.map(x => Array.from(x)));
    expect(entries[0]).toEqual(['consent', 'default', {analytics_storage: 'denied', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied'}]);
    const html = await page.content();
    expect(html).not.toMatch(/googletagmanager\.com|google-analytics\.com|stape\.io/i);
    expect(html).not.toMatch(/<(?:script|iframe)[^>]+src=["']https?:/i);
    await expect(page.locator('form')).toHaveCount(0);
    expect(await page.locator('.check-footer').textContent()).toContain('KI-Unterstützung');

    // Back navigation into the hub and mobile layout without horizontal overflow.
    await expect(page.locator(`a[href="${BASE}/checklisten/index.html"]`).first()).toBeAttached();
    await page.setViewportSize({width: 390, height: 844});
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth);
    expect(overflow).toBeLessThanOrEqual(391);
  });
}
