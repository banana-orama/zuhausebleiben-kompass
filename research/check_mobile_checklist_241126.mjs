import {chromium} from '@playwright/test';
const pages = ['/checklisten/badumbau-kosten.html','/checklisten/index.html','/checklisten/badumbau-angebote-vergleichen.html'];
const browser = await chromium.launch();
const page = await browser.newPage({viewport:{width:390,height:844}});
for (const p of pages){
  await page.goto('http://127.0.0.1:4179'+p,{waitUntil:'networkidle'});
  const m = await page.evaluate(()=>({sw:document.scrollingElement.scrollWidth,cw:document.scrollingElement.clientWidth,h:document.scrollingElement.scrollHeight}));
  console.log(p, JSON.stringify(m), m.sw>m.cw?('OVERFLOW '+(m.sw-m.cw)+'px'):'0px overflow');
  await page.screenshot({path:'research/evidence/badumbau-kosten-checklist-241126/mobile390-'+p.replace(/\//g,'_').replace(/_/,'')+'.png',fullPage:p!=='/checklisten/index.html'});
}
await browser.close();
