# Batch 31 (24.11.2026, Cron 09:23): 8. Checkliste „Badumbau-Budget" aus badumbau-kosten

## Einordnung: kein neuer Artikel, sondern autorisierter Growth-Lever

Der Lauf hatte zunächst Briefing 30 per SERP vergeben und dabei **10 Kandidaten verworfen** (alle mit Live-SERP-Beleg am 24.11.2026):

| Kandidat | Befund SERP 24.11. | Entscheidung |
|---|---|---|
| Treppenlift Rückbau/Demontage | 6–7 dedizierte Seiten (treppenliftwissen, vergleichsportal, experte ×2, prolift, regional, engel-Abschnitt) | verworfen — dicht |
| Treppenlift selbst einbauen/Eigenleistung | ~10 Händler-FAQ-Abschnitte + heimwerker/bastelfrau/toom | verworfen — Abschnitt-Fläche |
| Treppenlift Akku/Stromausfall | **bereits dokumentiert verworfen** (Batches 9–12: „commodity-Ratgeber, wenig originär Belegbares"); eigene SERP bestätigt ~5 dedizierte | verworfen — standing rejection bestätigt |
| Bad-Maße DIN 18040-2 | 6–8 dedizierte (seniorbad, hewi, pflege.net, noa, pfeiffer-may, haus.de, pflegeheimat24 + nullbarriere-Referenz) | verworfen — dicht |
| Badezimmertür (Entriegelung außen) | nur Abschnitte überall, aber Kannibalisierung mit eigenem Magnet tuerbreiten-schwellen-schnellcheck | verworfen — interner Overlap |
| Treppenlift Lautstärke (dB) | 4 dedizierte + 1 alte (2013); dB = reine Hersteller-Selbstauskunft | verworfen — Commodity (gleiche Begründung wie Akku) |
| Vermieter verweigert Treppenlift (§ 554) | 5–7 dedizierte, mehrfach Nov-2026-frisch (checkfox ×2, mieter-magazin 07.11.) | verworfen — dicht + frisch |
| Treppenlift Stromverbrauch | regional-treppenlift dediziert; post-purchase ohne Payable-Event | verworfen — dicht + kommerziell schwach |
| Vermieter-Steuer (§ 9 EStG) | rechtskomplex (anschaffungsnahe HK), keine primär verifizierbare Entscheidungslage | verworfen — Belegrisiko |
| Haushaltshilfe § 38 SGB V | institutionell dicht (Kassen) | verworfen — dicht |

Stattdessen der im Operating Brief für Wait-States explizit vorgesehene Lever: **druckbare Checkliste aus dem eigenen Entscheidungsbestand** (kuendigen-Muster vom 05.11.: keine neuen Zahlen, keine neuen Quellen — Extraktion aus freigegebenem Article-JSON). Gewählt: **badumbau-kosten** (39. Ratgeber, 17.11. live) — Abschnitt 7 „So schützen Sie Ihr Badumbau-Budget" (10 Punkte) — als 8. Checkliste. Grund: Bad-Cluster ist der Knoten der vorbereiteten Aroundhome-Placements (Einladung seit 23.11. beim Advertiser bestätigt); das Magnet-Blatt stärkt den Cluster vor der Aktivierung.

## Änderungen (4 Dateien, gleicher Commit)

1. `scripts/build-checklists.mjs`: CHECKLISTS +1 Eintrag badumbau-kosten (Blocks: ol sec6 [10 Schritte], table sec2 [Kostenbausteine], table sec4 [Eigenanteil-Rechnung]); Hub-Prosa „Sieben→Acht Arbeitsblätter"; CollectionPage-Description Acht + Topics; Meta-Desc Acht (158 Zeichen, ≤160).
2. `research/verify_checklists_build.py`: Pins 8→9 Sitemap-Checklist-URLs, Expected-Set +badumbau-kosten, JSON-LD 7→8 Items, **stale RSS-Pin 40→41** (seit Briefing 29 wartend), Consent-Liste +badumbau-kosten, blocks_cfg +`[["ol",6],["table",2],["table",4]]`.
3. `tests/checklists.spec.mjs`: CHECKLISTS-Map +gleicher Eintrag (Same-Commit-Regel).
4. Keine Article-JSON-/Renderer-/Content-Änderung (Adoptions-Pattern).

## Gates (alle 24.11. gegen LAUNCH-dist)

- `node --check` build-checklists.mjs OK; `npm run build:launch`: 9 Checklist-URLs in Sitemap, „Built 9 checklist pages (8 + overview)".
- `research/verify_checklists_build.py` **ALL PASS** (mit neuen Pins; alte RSS-40-Spanne beseitigt).
- `test_titles_meta.py`: neue Seite Title 52/Desc 144; Hub-Desc 158 — innerhalb 65/160, eindeutig.
- `npm test` **Exit 0** (beide Build-Modi, test_site, test_articles 41, cross_links, titles_meta, measurement, Playwright, Partner A–F ALL PASS).
- Playwright checklists.spec **9 passed** inkl. badumbau-kosten (Content-Integrität gegen Article-JSON, robots, canonical, consent contract).
- Mobile 390 px: 0 px Overflow auf neuer Seite, Hub und Vergleichs-Blatt (`research/check_mobile_checklist_241126.mjs`); Fullpage-Screenshots in `research/evidence/badumbau-kosten-checklist-241126/`; Vision-Kontrolle (Tabellen im table-scroll-Muster, Spalten vollständig, keine Überlappungen, Ausfüllzeilen + Footer sichtbar).

## Nicht Teil dieses Laufs

- Aroundhome: Einladung beim Advertiser ausgelöst (Mail 11238, 24.11. 08:46, Screenshot-Beleg „ID: 3124891 · Einladung gesendet · Warten auf Antwort"). **Annahme = Awin-Login-Betreiberakt** (Vault hat kein Awin-Item); danach Aktivierung nach `operations/aroundhome-activation-prep.md` (Dry-Run 22/22 liegt bereit). Impressum-USt-IdNr. live unverändert (DE305157036).
- Kein neues Briefing (Topic-Pool nach 10 dokumentierten Verwerfungen für diesen Lauf erschöpft; GSC weiterhin ohne Google-Sitzung).
