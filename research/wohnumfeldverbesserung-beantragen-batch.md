# Batch 12 (02.11.2026, Cron-Lauf): Briefing 15 — Wohnumfeld-Zuschuss beantragen

## Topic-Wahl (SERP-basiert, GSC im Cron weiter nicht abrufbar)
- **Gewählt:** Wohnumfeldverbesserung beantragen (§ 40 Abs. 4 SGB XI) — transactional-nah
  (Antrag vor dem Umbau = direkt vor der Kaufentscheidung), intent-distinct gegen
  treppenlift-zuschuss (Förderlandschaft/Beträge), hilfsmittel-pflegekasse (§ 33-Hilfsmittel-Weg,
  Wohnumfeld nur in Abgrenzungs-Sektion) und pflegegrad-antrag (Einstufung). Grep-Befund vor
  Start: „formular“ 1×/„frist“ 0× im treppenlift-zuschuss, 0 Antragsstrecken-Content im Bestand.
- **SERP (02.11.):** Kassen-Eigenseiten (AOK/DAK/MKK), kassen-lotse-Formulargenerator,
  pflege.de, Bundesportal, VZ-Musterbrief-PDF. Verbesserungslücke: neutrale Querschnitts-Antragsstrecke
  (Zeitpunkt + gesetzliche Fristen/Fiktion + Unterlagen + Ablehnungsgründe + „eine Maßnahme“-Falle)
  statt kassengebundener Formularseiten.
- **Verworfen:** Treppenlift-Wartung (Batch-8-Befund Post-purchase/Konkurrenzdichte hält),
  Haltegriff-Bad (kein bestätigter Partner, Distanz zur Monetarisierung), Kurventreppe
  (Kannibalisierung treppenlift-kosten), Kurzzeitpflege (driftet Richtung allgemeines Pflegeportal,
  strategie-widrig).

## Kernbefunde (alle 46 Ledger-Quotes verbatim, research/wohnumfeld-021126-ledger.json)
1. **§ 40 Abs. 7 SGB XI nennt die Entscheidungsfrist/Fiktion ausdrücklich für „Zuschüsse zu
   wohnumfeldverbessernden Maßnahmen“** (3 Wochen; 5 Wochen bei Beteiligung von Pflegefachperson/MD
   nach Abs. 1 Satz 2; ohne hinreichenden Grund = genehmigt). Wettbewerber schreiben die Fiktion
   meist nur Hilfsmitteln zu — Hauptdifferenzierung des Artikels.
2. **§ 40 Abs. 4 ist Ermessensleistung („können subsidiär“)** mit Zweckformel — nicht der oft
   behauptete feste 4.180-€-Anspruch. 4.180 je Maßnahme / 16.720 WG-Deckel / anteilige Aufteilung.
3. **„Eine Maßnahme oder mehrere?“:** mkk-Kassenformular (Stand 03|26): parallel genehmigte
   Maßnahmen gelten als EINE Maßnahme — die 4.180-Grenze ist nicht pro Handwerkerposition.
4. Antrag VOR dem Umbau: AOK („vor dem Umbau“), DAK („vor der Umsetzung genehmigen müssen“,
   Stand 01.10.2026), mkk („vor Beginn mit einem Kostenvoranschlag“), pflege.de („unbedingt vor
   den Umbaumaßnahmen“).
5. Abgrenzung Hilfsmittel: 33.40.05.0 Toilettenaufsätze mit Wascheinrichtung (GKV-SV-Fortschreibung
   11.12.2025) + gelistetes Produkt 33.40.05.0006 (REHADAT, Verzeichnisstand Bundesanzeiger
   28.09.2026) laufen über § 33; komplette Umbauten über § 40 Abs. 4.
6. Eigenleistung nur Material (pflege.de) — als Kassen-/Verbraucherpraxis gekennzeichnet, nicht als Gesetz.
7. BMG: Pflegegrade 1–5, WG-Durchrechnung (8 Personen → 2.090 € je), Zweitzuschuss bei veränderter
   Pflegesituation. VZ-Musterbrief (Stand 09/2021, bewusst datiert zitiert): formloser Briefweg +
   Begründungsformulierungen nach Zweckformel.

## Artikel
- content-ready/wohnumfeldverbesserung-beantragen.json — 10 Abschnitte (inkl. Unterlagen-Checkliste
  als Anker #abschnitt-6), Tabelle „Zahlen auf einen Blick“, 6 FAQs, 10 Quellen, 1 fiktives
  Rechenbeispiel (9.400 → 4.180 → 5.220, skriptgeprüft), Titel 30 Zeichen, Desc 141.
- Grafik assets/images/wohnumfeld-antrag-wegweiser.svg (6-Schritte-Wegweiser, nummerierte Kreise,
  Step-4-Highlight + Badge, Hinweisbox) — getBBox 0 Overflows + Badge-im-Rect + Vision-Check sauber.
- Verweise namentlich (Renderer erlaubt keine Inline-Links): hilfsmittel-pflegekasse-uebernahme,
  treppenlift-mietwohnung, pflegegrad-antrag-ablauf-fristen, treppenlift-steuerlich-absetzen.

## Renderer/Tests
- article-renderer.mjs: isCare-Regex + „wohnumfeld“, specialMap +1 (Early-CTA
  „Förderlandschaft im Überblick“ → treppenlift-zuschuss). test_cross_links.py: is_care-Regex synchron.
- data/cross-links.json: wohnumfeld → [hilfsmittel-pflegekasse, pflegegrad-antrag] (care-intern).
- llms-txt.py: SUMMARIES + SECTION_MAP erweitert. Testzähler: test_articles 25→26,
  verify_checklists_build RSS 25→26, test_partner_links A2 ≥ 26.
- Neu: research/verify_wohnumfeld_021126.py (Ledger 46/46 + Arithmetik 6/6),
  research/verify_wohnumfeld_content_021126.py (Content-Support-Gate, Lessons: sup.cite-<a>-Markup
  statt nacktem [n] strippen, &-escapete Quell-URLs doppelt prüfen),
  research/verify_wohnumfeld_svg_021126.py, research/verify_wohnumfeld_mobile_021126.py,
  research/fetch_wohnumfeld_021126.sh (10 Quellen, alle HTTP 200 am 02.11.; REHADAT beim Retry).

## Teststand
npm test grün inallen Teilen: build beide Modi, test_site 50 Seiten/37 locs, test_articles 26,
test_cross_links 26/7 Whitelist, test_titles_meta 0 Verletzungen, test:measurement, Playwright 20/20
(1 Flaky-Keyboard-Fail im ersten Lauf, 2× grün im Re-Run), test:partner ALL PASS.
Content-Gate ALL PASS, Mobile 390 px 0 px Overflow, Desktop-/Mobil-Screenshots in
research/evidence/wohnumfeld-021126/. Deploy+Live-Readback: siehe launch-state 02.11.

## Offene Punkte
- GSC-Queries weiter blockiert (keine Google-Sitzung im Cron) — Topic-Wahl weiter SERP-basiert.
- Nächste Einheiten laut Audit: #6b PNG ≥1200 px (og:image-Dimensionen), #9 pflegegrad-beantragen-Stub,
  #10 Performance/og; danach Region-Ausbau als recherchierter Batch.
