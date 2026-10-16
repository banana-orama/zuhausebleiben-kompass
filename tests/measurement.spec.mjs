import {test, expect} from '@playwright/test';

const service = 'https://service.zuhausebleiben-kompass.de';
test('shipped integration is active after consent: exactly one GTM loader and one sanitized page_view',async({page})=>{
 const loaders=[], hits=[];
 await page.route('https://www.googletagmanager.com/gtm.js**', async route => {
   loaders.push(route.request());
   await route.fulfill({contentType:'text/javascript',body:'window.zbkMeasurement.flush(); const push=window.dataLayer.push.bind(window.dataLayer); window.dataLayer.push=function(v){const n=push(v);if(v.event==="zbk_measurement")window.zbkMeasurement.flush();return n;};'});
 });
 await page.route(service+'/**', async route => {hits.push(route.request()); await route.fulfill({status:204});});
 await page.goto('/treppenlift-kosten.html');
 await page.getByRole('button',{name:'Alle akzeptieren',exact:true}).click();
 await expect.poll(()=>hits.length).toBe(1); expect(loaders).toHaveLength(1);
 const p=JSON.parse(hits[0].postData());
 expect(p.event_name).toBe('page_view'); expect(p.consent_version).toBe(2);
 expect(p.consent).toEqual({analytics_storage:'granted',ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied'});
});
test('failed GTM loader never falls back to direct analytics and navigation remains functional',async({page})=>{
const hits=[];await page.route('https://www.googletagmanager.com/**',r=>r.abort());
await page.route(service+'/**',async r=>{hits.push(r.request());await r.fulfill({status:204});});
await page.goto('/treppenlift-kosten.html');
await page.getByRole('button',{name:'Alle akzeptieren',exact:true}).click();
 await page.locator('[data-cta-id="checklist_top"]').click();
 await page.waitForTimeout(100);expect(hits).toEqual([]);expect(new URL(page.url()).hash).toMatch(/abschnitt/);
 await page.getByRole('button',{name:'Einwilligung widerrufen',exact:true}).click();
 await page.evaluate(()=>window.zbkMeasurement.flush());expect(hits).toEqual([]);
});
// Candidate fixture retired; the third test exercises the real shipped module end-to-end.
test('activated measurement denies by default, opts in once and withdraws without more requests', async ({page}) => {
  const loaders=[], hits=[];
  await page.route('https://www.googletagmanager.com/gtm.js**', async route => {
    loaders.push(route.request());
    // Deliberate local GTM stand-in only; this test does not verify real GTM or GA4.
    await route.fulfill({contentType:'text/javascript',body:`window.zbkMeasurement.flush(); const push=window.dataLayer.push.bind(window.dataLayer); window.dataLayer.push=function(v){const n=push(v);if(v.event==='zbk_measurement')window.zbkMeasurement.flush();return n;};`});
  });
  await page.route(service+'/**', async route => {hits.push(route.request()); await route.fulfill({status:204});});
  await page.goto('/treppenlift-kosten.html?email=person@example.org&diagnose=private#private');
  // Revision 2 must invalidate any stored revision-1 selection: the banner must re-appear.
  await expect(page.getByRole('button',{name:'Alle akzeptieren',exact:true})).toBeVisible();
  await page.waitForTimeout(100); expect(loaders).toHaveLength(0); expect(hits).toHaveLength(0);
  await page.getByRole('button',{name:'Alle ablehnen',exact:true}).click();
  await page.locator('[data-cta-id="checklist_top"]').click(); expect(hits).toHaveLength(0);
  await page.getByRole('button',{name:'Datenschutzeinstellungen',exact:true}).click();
  await page.getByRole('button',{name:'Alle akzeptieren',exact:true}).click();
  await expect.poll(()=>hits.length).toBe(1); expect(loaders).toHaveLength(1);
  await page.evaluate(()=>window.zbkConsent.update(true));
  await page.waitForTimeout(100); expect(hits).toHaveLength(1);
  await page.locator('[data-cta-id="checklist_top"]').click();
  await expect.poll(()=>hits.length).toBe(2); expect(new URL(page.url()).hash).toMatch(/abschnitt/);
  const payloads=hits.map(r=>JSON.parse(r.postData()));
  expect(payloads.map(p=>p.event_name)).toEqual(['page_view','cta_click']);
  for(const p of payloads){expect(p.analytics_allowed).toBe(true);expect(p.consent).toEqual({analytics_storage:'granted',ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied'});expect(JSON.stringify(p)).not.toMatch(/person@|example|diagnose|private|mailto|page_location|page_referrer|page_title/);}
  expect(loaders[0].headers().referer).toBeUndefined();
  expect(hits[0].headers().referer).toBeUndefined();
  await page.getByRole('button',{name:'Einwilligung widerrufen',exact:true}).click();
  await page.locator('[data-cta-id="checklist_top"]').click();
  await page.evaluate(()=>window.zbkMeasurement.flush());
  await page.waitForTimeout(100); expect(hits).toHaveLength(2);
});
