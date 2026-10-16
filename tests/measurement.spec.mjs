import {test, expect} from '@playwright/test';

// Client-side pivot (2026-10-16): after an analytics accept the site injects exactly ONE
// Web-GTM loader (GTM-M9TZZPLQ) and pushes minimal zbk_measurement events into dataLayer.
// No request to the former server endpoint or any Stape host may ever occur.
const FORBIDDEN = /service\.zuhausebleiben-kompass\.de|stape\.|stape\.io/i;
const GTM_LOADER = u => u.startsWith('https://www.googletagmanager.com/gtm.js?id=GTM-M9TZZPLQ');
const measurementEvents = page => page.evaluate(() => window.dataLayer.filter(x => x.event === 'zbk_measurement'));

test('after consent: exactly one GTM loader, one minimal page_view, cta_click gated, no server/Stape request ever', async ({page}) => {
  const loaders = [], forbidden = [];
  await page.route('https://www.googletagmanager.com/gtm.js**', async route => {
    loaders.push(route.request());
    // Local stand-in only; container firing itself is verified post-publish via DebugView/Realtime.
    await route.fulfill({contentType: 'text/javascript', body: '/* gtm stub */'});
  });
  await page.route(FORBIDDEN, async route => {forbidden.push(route.request().url()); await route.fulfill({status: 204});});
  await page.goto('/treppenlift-kosten.html');
  await expect(page.getByRole('button', {name: 'Alle akzeptieren', exact: true})).toBeVisible();
  await page.waitForTimeout(150);
  expect(loaders).toHaveLength(0);                       // zero before consent
  expect(forbidden).toEqual([]);
  expect(await measurementEvents(page)).toEqual([]);

  await page.getByRole('button', {name: 'Alle akzeptieren', exact: true}).click();
  await expect.poll(() => measurementEvents(page)).toHaveLength(1);
  expect(loaders).toHaveLength(1);                       // exactly one loader after consent
  expect(forbidden).toEqual([]);
  const loader = loaders[0];
  expect(GTM_LOADER(loader.url())).toBe(true);
  expect(loader.headers().referer).toBeUndefined();      // no-referrer injection

  const [pageView] = await measurementEvents(page);
  expect(pageView).toEqual({
    event: 'zbk_measurement', analytics_allowed: true, consent_version: 2,
    consent: {analytics_storage: 'granted', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied'},
    measurement: {event_name: 'page_view', content_id: 'c04', cta_id: ''}
  });

  await page.locator('[data-cta-id="checklist_top"]').click();
  await expect.poll(() => measurementEvents(page)).toHaveLength(2);
  expect(new URL(page.url()).hash).toMatch(/abschnitt/);
  const [, ctaClick] = await measurementEvents(page);
  expect(ctaClick.measurement).toEqual({event_name: 'cta_click', content_id: 'c04', cta_id: 'checklist_top'});
  expect(loaders).toHaveLength(1);                       // no second loader on interaction

  await page.getByRole('button', {name: 'Einwilligung widerrufen', exact: true}).click();
  await page.waitForTimeout(150);
  await page.locator('[data-cta-id="checklist_top"]').click();
  await page.waitForFunction(() => /abschnitt/.test(location.hash));
  await page.waitForTimeout(100);
  expect(await measurementEvents(page)).toHaveLength(2); // nothing after withdrawal
  expect(loaders).toHaveLength(1);
  expect(forbidden).toEqual([]);                         // service.zuhausebleiben-kompass.de / Stape: never
});

test('failed GTM loader never falls back to any endpoint and navigation remains functional', async ({page}) => {
  const forbidden = [], loaderAttempts = [];
  await page.route('https://www.googletagmanager.com/**', async route => {loaderAttempts.push(route.request().url()); await route.abort();});
  await page.route(FORBIDDEN, async route => {forbidden.push(route.request().url()); await route.fulfill({status: 204});});
  await page.goto('/treppenlift-kosten.html');
  await page.getByRole('button', {name: 'Alle akzeptieren', exact: true}).click();
  await page.waitForTimeout(200);
  expect(loaderAttempts.filter(GTM_LOADER)).toHaveLength(1);
  // No direct-to-Google fallback and no server endpoint call: the container is the only path.
  expect(forbidden).toEqual([]);
  expect(loaderAttempts.filter(u => /google-analytics\.com|\/g\/collect|\/collect/.test(u))).toEqual([]);
  await page.locator('[data-cta-id="checklist_top"]').click();
  await page.waitForTimeout(100);
  expect(forbidden).toEqual([]);
  expect(new URL(page.url()).hash).toMatch(/abschnitt/);
});

test('activated measurement denies by default, opts in once and withdraws without more requests; URL inputs never reach dataLayer', async ({page}) => {
  const loaders = [], forbidden = [];
  await page.route('https://www.googletagmanager.com/gtm.js**', async route => {
    loaders.push(route.request());
    await route.fulfill({contentType: 'text/javascript', body: '/* gtm stub */'});
  });
  await page.route(FORBIDDEN, async route => {forbidden.push(route.request().url()); await route.fulfill({status: 204});});
  await page.goto('/treppenlift-kosten.html?email=person@example.org&diagnose=private#private');
  // Revision 2 must invalidate any stored revision-1 selection: the banner must re-appear.
  await expect(page.getByRole('button', {name: 'Alle akzeptieren', exact: true})).toBeVisible();
  await page.waitForTimeout(100);
  expect(loaders).toHaveLength(0); expect(forbidden).toEqual([]); expect(await measurementEvents(page)).toEqual([]);

  await page.getByRole('button', {name: 'Alle ablehnen', exact: true}).click();
  await page.locator('[data-cta-id="checklist_top"]').click();
  await page.waitForTimeout(100);
  expect(await measurementEvents(page)).toEqual([]); expect(loaders).toHaveLength(0);

  await page.getByRole('button', {name: 'Datenschutzeinstellungen', exact: true}).click();
  await page.getByRole('button', {name: 'Alle akzeptieren', exact: true}).click();
  await expect.poll(() => measurementEvents(page)).toHaveLength(1);
  expect(loaders).toHaveLength(1);

  await page.evaluate(() => window.zbkConsent.update(true));
  await page.waitForTimeout(100);
  expect(await measurementEvents(page)).toHaveLength(1); // no duplicate page_view

  await page.locator('[data-cta-id="checklist_top"]').click();
  await expect.poll(() => measurementEvents(page)).toHaveLength(2);
  expect(new URL(page.url()).hash).toMatch(/abschnitt/);
  const events = await measurementEvents(page);
  expect(events.map(e => e.measurement.event_name)).toEqual(['page_view', 'cta_click']);
  for (const e of events) {
    expect(e.analytics_allowed).toBe(true);
    expect(e.consent).toEqual({analytics_storage: 'granted', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied'});
    expect(Object.keys(e.measurement).sort()).toEqual(['content_id', 'cta_id', 'event_name']);
  }
  // Payload redaction: nothing derived from the poisoned URL/query/referrer/title may appear.
  const dumped = await page.evaluate(() => JSON.stringify(window.dataLayer));
  expect(dumped).not.toMatch(/person@|example|diagnose|private|mailto|page_location|page_referrer|page_title/);
  expect(loaders[0].headers().referer).toBeUndefined();

  await page.getByRole('button', {name: 'Einwilligung widerrufen', exact: true}).click();
  await page.locator('[data-cta-id="checklist_top"]').click();
  await page.waitForFunction(() => /abschnitt/.test(location.hash));
  await page.waitForTimeout(100);
  expect(await measurementEvents(page)).toHaveLength(2);
  expect(loaders).toHaveLength(1);
  expect(forbidden).toEqual([]);
});
