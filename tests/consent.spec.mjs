import {test, expect} from '@playwright/test';
import {readdirSync, readFileSync} from 'node:fs';
import {join} from 'node:path';
test('every generated HTML page includes local CMP, early deny and withdrawal without a tracking loader', () => {
  function htmlFiles(dir) { return readdirSync(dir, {withFileTypes: true}).flatMap(e => e.isDirectory() ? htmlFiles(join(dir, e.name)) : e.name.endsWith('.html') ? [join(dir, e.name)] : []); }
  const files = htmlFiles('dist'); expect(files.length).toBeGreaterThan(0);
  for (const file of files) {
    const html = readFileSync(file, 'utf8');
    expect(html, file).toContain("window.gtag('consent', 'default'");
    expect(html, file).toContain('src="/assets/consent.mjs"');
    expect(html, file).toContain('data-consent-settings'); expect(html, file).toContain('data-consent-withdraw');
    expect(html.indexOf("window.gtag('consent', 'default'")).toBeLessThan(html.indexOf('src="/assets/consent.mjs"'));
    expect(html, file).not.toMatch(/<(?:script|iframe)[^>]+src=["']https?:/i);
    expect(html, file).not.toMatch(/(?:googletagmanager\.com|google-analytics\.com|stape\.io)/i);
  }
});
const denied = {analytics_storage: 'denied', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied'};
const analyticsOnly = {...denied, analytics_storage: 'granted'};
test.beforeEach(async ({page}) => {
  // Existing absolute first-party URLs must exercise the local build, not production.
  await page.route('https://zuhausebleiben-kompass.de/**', async route => {
    const u = new URL(route.request().url());
    await route.fulfill({response: await route.fetch({url: 'http://127.0.0.1:4179' + u.pathname + u.search})});
  });
});
function observe(page) {
  const external = [], errors = [];
  page.on('request', r => {if (!['http://127.0.0.1:4179', 'https://zuhausebleiben-kompass.de'].includes(new URL(r.url()).origin)) external.push(r.url());});
  page.on('pageerror', e => errors.push(e.message));
  return {external, errors};
}
async function assertState(page, expected) {
  await expect.poll(() => page.evaluate(() => window.zbkConsent?.state)).toEqual(expected);
  const entries = await page.evaluate(() => window.dataLayer.map(x => x.event ? x : Array.from(x)));
  expect(entries[0]).toEqual(['consent', 'default', denied]);
  for (let i = 0; i < entries.length; i++) {
    if (entries[i].event === 'zbk_consent_update') {
      expect(entries[i - 1]).toEqual(['consent', 'update', entries[i].consent]);
    }
  }
}
async function quiet(page, observed) {
  await page.waitForTimeout(250);
  expect(observed).toEqual({external: [], errors: []});
}
test('first visit offers equal choices, denies by default and makes no third-party requests', async ({page, context}) => {
  const observed = observe(page);
  await page.goto('/');
  const reject = page.getByRole('button', {name: 'Alle ablehnen', exact: true});
  const accept = page.getByRole('button', {name: 'Alle akzeptieren', exact: true});
  await expect(reject).toBeVisible(); await expect(accept).toBeVisible();
  await expect(page.getByRole('button', {name: 'Einstellungen', exact: true})).toBeVisible();
  const style = locator => locator.evaluate(e => {const s = getComputedStyle(e); return [s.backgroundColor,s.color,s.borderColor,e.getBoundingClientRect().height];});
  expect(await style(reject)).toEqual(await style(accept));
  expect((await style(reject))[3]).toBeGreaterThanOrEqual(48);
  await assertState(page, denied);
  expect(await context.cookies()).toEqual([]);
  await quiet(page, observed);
});
test('reject is persisted across pages and reload without optional traffic', async ({page, context}) => {
  const observed = observe(page);
  await page.goto('/'); await page.getByRole('button', {name: 'Alle ablehnen', exact: true}).click();
  await assertState(page, denied);
  const cookies = await context.cookies();
  expect(cookies.map(c => c.name)).toEqual(['zbk_consent']);
  expect(cookies[0].sameSite).toBe('Lax'); expect(cookies[0].path).toBe('/');
  expect(cookies[0].expires - Date.now()/1000).toBeGreaterThan(179 * 86400);
  await page.goto('/region/nordrhein-westfalen.html');
  await expect(page.getByRole('button', {name: 'Alle ablehnen', exact: true})).not.toBeVisible();
  await assertState(page, denied); await page.reload(); await assertState(page, denied);
  await quiet(page, observed);
});
test('accept grants only analytics, ordered GTM event observes updated state, withdrawal persists', async ({page}) => {
  const observed = observe(page);
  await page.goto('/');
  await page.evaluate(() => {window.seenConsent = []; window.addEventListener('zbk:consent', e => window.seenConsent.push({detail: e.detail, state: {...window.zbkConsent.state}}));});
  await page.getByRole('button', {name: 'Alle akzeptieren', exact: true}).click();
  await assertState(page, analyticsOnly);
  expect(await page.evaluate(() => window.seenConsent)).toEqual([{detail: analyticsOnly, state: analyticsOnly}]);
  await page.reload(); await assertState(page, analyticsOnly);
  await page.getByRole('button', {name: 'Einwilligung widerrufen', exact: true}).click();
  await assertState(page, denied);
  await expect(page.getByRole('status')).toContainText('widerrufen');
  await page.reload(); await assertState(page, denied);
  await quiet(page, observed);
});
test('individual settings are keyboard usable and restore focus', async ({page}) => {
  const observed = observe(page);
  await page.goto('/'); await page.getByRole('button', {name: 'Einstellungen', exact: true}).click();
  const toggle = page.getByRole('checkbox', {name: 'Optionale Statistik (noch nicht aktiv)'});
  await expect(toggle).not.toBeChecked();
  await toggle.focus(); await page.keyboard.press('Space'); await expect(toggle).toBeChecked();
  await page.getByRole('button', {name: 'Auswahl speichern', exact: true}).click();
  await assertState(page, analyticsOnly);
  const settings = page.getByRole('button', {name: 'Datenschutzeinstellungen', exact: true});
  await settings.click(); await expect(toggle).toBeChecked();
  await page.keyboard.press('Escape'); await expect(settings).toBeFocused();
  await settings.click(); await toggle.uncheck();
  await page.getByRole('button', {name: 'Auswahl speichern', exact: true}).click();
  await assertState(page, denied); await quiet(page, observed);
});
test('invalid or outdated preferences fail closed and ask again', async ({page, context}) => {
  await context.addCookies([{name: 'zbk_consent', value: 'invalid-json', domain: '127.0.0.1', path: '/'}]);
  await page.goto('/'); await expect(page.getByRole('button', {name: 'Alle akzeptieren', exact: true})).toBeVisible();
  await assertState(page, denied);
  await page.getByRole('button', {name: 'Alle akzeptieren', exact: true}).click();
  const cookie = (await context.cookies()).find(c => c.name === 'zbk_consent');
  const value = JSON.parse(decodeURIComponent(cookie.value)); value.revision = 0;
  await context.addCookies([{...cookie, value: encodeURIComponent(JSON.stringify(value))}]);
  await page.reload(); await assertState(page, denied);
  await expect(page.getByRole('button', {name: 'Alle ablehnen', exact: true})).toBeVisible();
});
test('local library failure stays denied with usable content', async ({page}) => {
  const observed = observe(page);
  await page.route('**/assets/vendor/cookieconsent.esm.js', r => r.abort());
  await page.goto('/'); await assertState(page, denied);
  await expect(page.getByRole('heading', {level: 1})).toBeVisible();
  expect(await page.evaluate(() => window.dataLayer.length)).toBe(1);
  expect(observed.external).toEqual([]);
});
test('HTTPS cookie is secure and no localStorage is used', async ({page, context}) => {
  const observed = observe(page);
  await page.goto('https://zuhausebleiben-kompass.de/datenschutz.html');
  await page.getByRole('button', {name: 'Alle ablehnen', exact: true}).click();
  const cookie = (await context.cookies()).find(c => c.name === 'zbk_consent');
  expect(cookie.secure).toBe(true); expect(cookie.sameSite).toBe('Lax');
  expect(await page.evaluate(() => localStorage.length)).toBe(0);
  await expect(page.locator('main')).toContainText('zbk_consent');
  await expect(page.locator('main')).not.toContainText('setzt keine Cookies ein');
  await assertState(page, denied); await quiet(page, observed);
});
test('JavaScript disabled leaves content available and never requests tracking', async ({browser}) => {
  const context = await browser.newContext({javaScriptEnabled: false});
  const page = await context.newPage(); const observed = observe(page);
  await page.goto('http://127.0.0.1:4179/datenschutz.html');
  await expect(page.getByRole('heading', {level: 1})).toBeVisible();
  await expect(page.locator('noscript')).toBeVisible();
  expect(await context.cookies()).toEqual([]);
  await quiet(page, observed); await context.close();
});
test('mobile banner and settings fit viewport with large equal controls', async ({page}) => {
  await page.setViewportSize({width: 375, height: 812});
  await page.goto('/treppenlift-kosten.html');
  const reject = page.getByRole('button', {name: 'Alle ablehnen', exact: true});
  await expect(reject).toBeVisible();
  for (const name of ['Alle ablehnen', 'Alle akzeptieren', 'Einstellungen']) {
    const b = await page.getByRole('button', {name, exact: true}).boundingBox();
    expect(b.x).toBeGreaterThanOrEqual(0); expect(b.x + b.width).toBeLessThanOrEqual(375); expect(b.height).toBeGreaterThanOrEqual(48);
  }
  await page.waitForTimeout(500);
  await page.screenshot({path: 'test-results/consent-mobile-banner.png'});
  await page.getByRole('button', {name: 'Einstellungen', exact: true}).click();
  await expect(page.getByRole('button', {name: 'Auswahl speichern', exact: true})).toBeInViewport();
  await page.waitForTimeout(500);
  await page.screenshot({path: 'test-results/consent-mobile-settings.png'});
  expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBeLessThanOrEqual(375);
});
