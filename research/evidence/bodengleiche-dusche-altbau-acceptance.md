# Batch-4 Acceptance: bodengleiche-dusche-altbau (2026-10-19)

## Behauptungen → Belege (stichprobenartig jede Kopfzahl gegen Live-Original)

| Behauptung im Artikel | Originalquelle | Verbatim-Check |
|---|---|---|
| Pflegekasse: Ermessen, 4.180 € je Maßnahme, 16.720 € Gemeinschaftsdeckel | gesetze-im-internet.de/sgb_11/__40.html (ISO-8859-1, 4 180 mit geschütztem Leerzeichen) | OK (Ledger [1]) |
| BMG: PG 1–5, bis zu 4.180 € | bundesgesundheitsministerium.de …wohnungsanpassung | OK ([2]) |
| KfW 455-B: Antragstopp, Mittel ausgeschöpft, Laufende reserviert | kfw.de …455)/ (Abruf 19.10.) | OK ([3]) |
| KfW 159: 50.000 €, Haushaltsmittelvorbehalt, Fachunternehmen-Bestätigung | kfw.de …159 | OK ([4]) |
| Kombinationsverbot gleiche Maßnahme + Badumbau/Treppenlift-Ausnahme | kfw.de …159 FAQ | OK ([4], wörtlich) |
| DIN 18040-2 (Fachportal): niveaugleich, max. 2 cm abgeschrägt; Gefälle 0,5–1,5 %, 2 % nicht wesentlich überschreiten; abgehängte Decke; Membranpumpe | nullbarriere.de/din18040-2-bad.htm | OK ([5]) |
| 120×120 / 150×150; Altersgerecht kein Normbegriff; Restschwelle 7–15 cm | barrierefreies-bad.de/bodengleiche-dusche | OK ([6]) |
| ZVSHK: Schlauchbad < 5 qm Altbau-Mustergrundriss; Kostenordnung 25/15 Tsd. € | zvshk.de Zusammenfassung_Studie_final.pdf | OK ([7]) |
| haustec: Wanne ca. 20 cm über Boden, Ablauf min. 5 cm darunter, ca. 25 cm Hub, 1,3 m Förderhöhe, 30 l/min | haustec.de (24.06.2019) | OK ([8], als Produkt-/Fallbeispiel gekennzeichnet) |
| § 554 BGB: Anspruch + Zumutbarkeitsgrenze | gesetze-im-internet.de/bgb/__554.html | OK ([9]) |
| Extraflach ab ca. 6,5 cm; Holzbalkendecke konstruktive Prüfung; flache Alternative | fliesenwerker.de FAQ | OK ([10], Anbieterangabe gekennzeichnet) |

Alle 29 Ledger-Zitate maschinell verifiziert (verify_quotes FAILS: 0). Quellen-URLs
alle HTTP 200 am 19.10.2026 (curl-Log in Scratch altbau-batch).

## Build-/Deploy-Acceptance

- npm run build (PREVIEW) → 38 Seiten; npm run build:launch → 37 Seiten, beide PASS
- python3 test_site.py: PASS (LAUNCH via env INDEX + PREVIEW-Lauf im npm script)
- python3 test_articles.py: PASS, Zähler 17
- Playwright consent: 13/13 PASS; measurement: PASS
- Key-Content-Assertion: alle 55 Absätze/Bullets/Zellen, 8 Überschriften, 6 FAQs, 10
  Quellen, Bild (src/alt/caption), Anker [1]–[10], Sitemap-Aufnahme, robots index,follow —
  0 FAILS
- Cluster-Check: „Passend dazu" nur Bad-Cluster (bad-umbau, wanne-zur-dusche, treppenlift-zuschuss);
  Early-CTA-Ziel treppenlift-mietwohnung.html „Mietwohnung: Zustimmungen klären →" (artikelbezogen)
- SVG-Sichtkontrolle (Chromium 1000×780): 4 Karten vollständig, kein Overflow
- Mobile 390 px: Typo/CTA/TOC sauber; H1-Umbruchverhalten identisch zur Live-Baseline
  (treppenlift-mietwohnung.html im selben Build)

## Deploy-Readback (nach Push)

→ siehe operations/CONTENT-PIPELINE-STATE.md (Batch 4 Eintrag) und finale Cron-Nachricht:
öffentliche URL, HTTP-Status, robots, Sitemap-Zählung, Artikel-Datum 2026-10-19 auf Live.
