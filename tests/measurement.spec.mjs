import {test, expect} from '@playwright/test';

const service = 'https://service.zuhausebleiben-kompass.de';
test('shipped integration stays inactive even after consent',async({page})=>{
 const requests=[];page.on('request',r=>{if(/googletagmanager|google-analytics|stape|service\.zuhausebleiben/.test(r.url()))requests.push(r.url());});
 await page.goto('/treppenlift-kosten.html');
 await page.evaluate(async()=>{const m=await import('/assets/measurement.mjs');m.installMeasurement();});
 await page.getByRole('button',{name:'Alle akzeptieren',exact:true}).click();
 await page.waitForTimeout(100);expect(requests).toEqual([]);
});
test('failed GTM loader never falls back to direct analytics and navigation remains functional',async({page})=>{
 const hits=[];await page.route('https://www.googletagmanager.com/**',r=>r.abort());
 await page.route(service+'/**',async r=>{hits.push(r.request());await r.fulfill({status:204});});
 await page.goto('/treppenlift-kosten.html');await install(page);
 await page.getByRole('button',{name:'Alle akzeptieren',exact:true}).click();
 await page.locator('[data-cta-id="checklist_top"]').click();
 await page.waitForTimeout(100);expect(hits).toEqual([]);expect(new URL(page.url()).hash).toMatch(/abschnitt/);
 await page.getByRole('button',{name:'Einwilligung widerrufen',exact:true}).click();
 await page.evaluate(()=>window.zbkMeasurement.flush());expect(hits).toEqual([]);
});
async function install(page) {
  await page.evaluate(async () => {
    const {installMeasurement} = await import('/assets/measurement.mjs');
    installMeasurement({enabled:true, webContainer:'GTM-M9TZZPLQ', endpoint:'https://service.zuhausebleiben-kompass.de/zbk/collect', consentRevision:1, tlsVerified:true, serverGateVerified:true, destinationVerified:true});
  });
}
test('candidate measurement denies by default, opts in once and withdraws without more requests', async ({page}) => {
  const loaders=[], hits=[];
  await page.route('https://www.googletagmanager.com/gtm.js**', async route => {
    loaders.push(route.request());
    // Deliberate local GTM stand-in only; this test does not verify real GTM or GA4.
    await route.fulfill({contentType:'text/javascript',body:`window.zbkMeasurement.flush(); const push=window.dataLayer.push.bind(window.dataLayer); window.dataLayer.push=function(v){const n=push(v);if(v.event==='zbk_measurement')window.zbkMeasurement.flush();return n;};`});
  });
  await page.route(service+'/**', async route => {hits.push(route.request()); await route.fulfill({status:204});});
  await page.goto('/treppenlift-kosten.html?email=person@example.org&diagnose=private#private');
  await install(page);
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
