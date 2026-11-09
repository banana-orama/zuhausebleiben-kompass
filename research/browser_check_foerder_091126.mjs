// Browser-Check KfW 455-B + 159 (09.11.2026): gerenderten Seitentext im echten
// Chromium laden und die Kernsätze nachweisen. Ergänzt den curl-Abruf
// (research/evidence/foerder-091126-*.html) um die gerenderte Sicht.
// 159 wird in der KANONISCHEN Form (Umlaut + trailing slash) geprüft — genau
// die Form, auf die der heutige Content-Zitier-Fix normalisiert.
import { chromium } from 'playwright-core';

const CHECKS = [
  {
    name: '455-B',
    url: 'https://www.kfw.de/inlandsfoerderung/Privatpersonen/Bestandsimmobilie/F%C3%B6rderprodukte/Altersgerecht-Umbauen-Investitionszuschuss-(455)/',
    needles: [
      ['Antragstopp', 'können Sie nicht mehr beantragen'],
      ['Mittel ausgeschöpft', 'ausgeschöpft'],
      ['Laufende Anträge nicht betroffen', 'Laufende Anträge nicht betroffen'],
      ['Zusage reserviert', 'reserviert'],
      ['2027 Bundesmittel', '2027'],
      ['nicht begonnen', 'noch nicht mit Ihrem Vorhaben begonnen'],
    ],
  },
  {
    name: '159 (Kanonikalform)',
    url: 'https://www.kfw.de/inlandsfoerderung/Privatpersonen/Bestehende-Immobilie/Förderprodukte/Altersgerecht-Umbauen-(159)/',
    needles: [
      ['50.000/WE', 'bis zu 50.000 Euro je Wohneinheit'],
      ['Haushaltsvorbehalt', 'Vorbehalt verfügbarer Haushaltsmittel'],
      ['Fachunternehmen', 'von einem Fachunternehmen durchgeführt'],
      ['Treppenlifte', 'Treppenlifte, Senkrecht-, Hebe- oder Plattformlifte'],
      ['Kombination ausgeschlossen', 'Kombination der Förderungen für die gleiche Maßnahme ist nicht möglich'],
    ],
  },
];

const browser = await chromium.launch({ headless: true });
let totalFail = 0;
for (const { name, url, needles } of CHECKS) {
  const page = await browser.newPage();
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(3000);
  const text = await page.evaluate(() => document.body.innerText.replace(/\u00ad/g, ''));
  let fail = 0;
  for (const [label, needle] of needles) {
    let i = text.indexOf(needle);
    if (i >= 0) {
      console.log(`PASS  ${name} ${label} [sichtbar]: …${text.slice(Math.max(0, i - 80), i + needle.length + 120).replace(/\s+/g, ' ')}…`);
      continue;
    }
    // Fallback: eingeklappte Akkordeons/FAQs tauchen in innerText NICHT auf,
    // stehen aber im ausgelieferten DOM (textContent).
    const full = await page.evaluate(() => document.body.textContent.replace(/\u00ad/g, '').replace(/\s+/g, ' '));
    const j = full.indexOf(needle);
    if (j >= 0) {
      console.log(`PASS  ${name} ${label} [eingeklappt, im DOM]: …${full.slice(Math.max(0, j - 80), j + needle.length + 120)}…`);
      continue;
    }
    fail++; console.log(`FAIL  ${name} ${label}: weder sichtbar noch im DOM`);
  }
  totalFail += fail;
  console.log(fail === 0 ? `BROWSER-CHECK ${name}: alle PASS (${needles.length}/${needles.length})` : `BROWSER-CHECK ${name}: ${fail} FAIL`);
  await page.close();
}
await browser.close();
process.exit(totalFail === 0 ? 0 : 1);
