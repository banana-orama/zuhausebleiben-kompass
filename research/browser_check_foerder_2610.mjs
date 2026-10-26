// Browser-Check KfW 455-B (26.10.2026): gerenderten Seitentext im echten Chromium
// laden und die Kernsätze des Antragstopps nachweisen. Ergänzt den curl-Abruf
// (research/evidence/foerder-261026-kfw455b.html) um die gerenderte Sicht.
import { chromium } from 'playwright-core';

const URL = 'https://www.kfw.de/inlandsfoerderung/Privatpersonen/Bestandsimmobilie/F%C3%B6rderprodukte/Altersgerecht-Umbauen-Investitionszuschuss-(455)/';
const NEEDLES = [
  ['Antragstopp', 'können Sie nicht mehr beantragen'],
  ['Mittel ausgeschöpft', 'ausgeschöpft'],
  ['Laufende Anträge nicht betroffen', 'Laufende Anträge nicht betroffen'],
  ['Zusage reserviert', 'reserviert'],
  ['2027 Bundesmittel', '2027'],
  ['nicht begonnen', 'noch nicht mit Ihrem Vorhaben begonnen'],
];

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();
await page.goto(URL, { waitUntil: 'domcontentloaded', timeout: 60000 });
await page.waitForTimeout(3000);
const text = await page.evaluate(() => document.body.innerText.replace(/\u00ad/g, ''));
let fail = 0;
for (const [label, needle] of NEEDLES) {
  const i = text.indexOf(needle);
  if (i < 0) { fail++; console.log(`FAIL  ${label}: NOT FOUND`); continue; }
  console.log(`PASS  ${label}: …${text.slice(Math.max(0, i - 80), i + needle.length + 120).replace(/\s+/g, ' ')}…`);
}
console.log(fail === 0 ? 'BROWSER-CHECK 455-B: alle PASS' : `BROWSER-CHECK 455-B: ${fail} FAIL`);
await browser.close();
process.exit(fail === 0 ? 0 : 1);
