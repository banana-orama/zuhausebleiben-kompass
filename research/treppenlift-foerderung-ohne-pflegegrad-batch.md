# Briefing 23: Treppenlift-Förderung ohne Pflegegrad (11.11.2026, Cron-Lauf)

## Topic-Wahl (SERP-Gates, GSC im Cron weiter ohne Google-Sitzung)

- **Gewählt:** „Treppenlift-Förderung ohne Pflegegrad" — Bestand-Lücke grep-geprüft: treppenlift-zuschuss
  deckt ausschließlich Pflegekasse (§ 40 SGB XI) + KfW ab, **0 Treffer** auf Sozialamt/Jobcenter/
  Rentenversicherung/SGB IX/Eingliederungshilfe. SERP-Feld 10/10 Anbieter-/Broker-/Affiliate-Seiten,
  mehrere mit nachweislich falschen bzw. stale KfW-Angaben („KfW-Zuschuss Altersgerecht Umbauen" =
  eingestellter 455-B; „455-B 10 %/2.500 €" = Antragstopp ignoriert; falscher Programmname „KfW 159
  Altersgerecht Umbauen"). Keine Seite dokumentiert DRV/EiH/UV/Sozialamt statutorie systematisch.
- **Verworfen mit Beleg:** Badumbau-Mietwohnung (§ 554/§ 20-WEG-Maschinerie liegt bei
  treppenlift-mietwohnung; bad-umbau-barrierefrei hat eigenen „Mietwohnung"-Abschnitt →
  Kannibalisierung wie das verworfene Höherstufungs-Muster), Umzug mit Lift (post-purchase, kein
  payable event, Ankauf-Seiten dominieren), Dusch-WC-Preisartikel (Shop-Dichte).

## Kernbefunde (28 Quellen, Ledger 108/108 = 51 verbatim + Kernzahlen + 5 Absenzen)

- **DRV-Grenze (Fehlannahme 1):** § 9 SGB VI listet keine Soziale Teilhabe; DRV-Wohnungshilfen
  existieren nur zur Teilhabe am ARBEITSleben und „erstrecken sich nur auf den Bereich vor der Haus-
  bzw. vor der Wohnungstür" (DRV-Verbatim). Lift im Treppenhaus = kein Titel über die RV.
- **KK-Grenze (Fehlannahme 2):** Hilfsmittel-Definition § 47 SGB IX („getragen oder mitgeführt oder
  bei einem Wohnungswechsel mitgenommen") schließt fest eingebaute Lifte aus → ohne Pflegegrad
  keine Kassen-Route.
- **EiH-Detailtiefe (Serien-Mehrwert):** Beitragseinkommen = Einkünfte des **Vorvorjahres** (§ 135),
  Schwellen 85/75/60 % der Bezugsgröße je Einkunftsart (§ 136), 150 %-Barvermögensschutz (§ 139),
  Leistung ggf. **als Darlehen** (§ 140). Gesamtplanverfahren mit Pflegekassen-Beteiligung bei
  Pflegebedürftigkeits-Anhaltspunkten (§ 117 Abs. 3), ICF-Bedarfsermittlung mit Mobilität/
  häuslichem Leben (§ 118), Budget mit 6-Monats-Bindung (§ 29), EUTB vor dem Antrag (§ 32).
- **UV-Weg:** § 26 SGB VII nennt Soziale Teilhabe + „Hilfen … zur Führung eines möglichst
  selbständigen Lebens"; DGUV benennt Wohnen/Mobilität; § 66 SGB XIV analog (Soziale Entschädigung).
- **Sozialamt-Weg:** § 64e SGB XII; Pflegebedürftigkeitsbegriff § 61a SGB XII mit
  „Treppensteigen" als Mobilitäts-Kriterium wörtlich; Bedürftigkeit § 61; Nachrang § 2 SGB XII.
- **Reform getrennt vom geltenden Recht:** Drs. 21/8869 (02.11.2026, Bundestag, NICHT beschlossen):
  § 15 neu „ab 15 bis unter 30 Gesamtpunkten" (PG 1), § 142b Bestandsschutz (Zuordnung nach
  31.12.2026-Recht bleibt bestehen), Inkrafttreten geplant 01.01.2027; BMG-PM („zielgenauer
  vergeben", Bestandsschutz, „Reha vor Pflege"). Übergangsregelung stellt auf Recht zur
  Antragstellung ab → 2026er Anträge nach alter Systematik.

## Dateien

- `content-ready/treppenlift-foerderung-ohne-pflegegrad.json` (10 Abschnitte, 6 FAQs, 28 Quellen)
- `assets/images/treppenlift-foerderung-ohne-pflegegrad-wegweiser.svg` (5 Bänder: Schritt 0 +
  3 Wege + Grenz-Band; KI-Illustration gekennzeichnet)
- Renderer: specialMap +1 („Pflegekasse & KfW prüfen" → treppenlift-zuschuss); cross-links +1
  (zuschuss, finanzierung, gebraucht-oder-neu — lift-intern); llms-txt SUMMARIES + SECTION_MAP +1;
  isLift trifft via treppenlift-Präfix.
- Testzähler: test_articles 33→34; verify_checklists_build RSS 33→34; test_partner_links A3 ≥32→≥33.

## Gates

- research/verify_ohne_pflegegrad_111126.py: **108/108 PASS** (51 verbatim inkl. dehyphenierter
  Drucksache-Evidenz `drucksache-21-8869.norm.txt`; Kernzahlen; Absenzen 0× 4.180/16.720, 0× „12,5")
- research/verify_ohne_pflegegrad_content_111126.py: **0 FAILS** (LAUNCH-dist; jeder JSON-Key im HTML,
  Related 3× lift-intern in Cross-Reihenfolge, CTA + Label, 0 Partner-Marker, SVG kopiert, Anker 1..28,
  0 Förderbeträge)
- research/verify_ohne_pflegegrad_svg_mobile_111126.py: **ALL PASS** (0 Geometrie-Issues,
  0 px Mobile 390 px) + Vision-Sichtkontrolle: keine Defekte
  (research/evidence/ohne-pflegegrad-111126/svg-screenshot.png)
- npm test: EXIT 0 (test_site 59 Seiten, test_articles 34, cross_links, titles_meta nach
  Desc-Kürzung 166→154, Playwright 21 passed, Partner A–F ALL PASS)
- verify_checklists_build: ALL PASS (LAUNCH-dist, RSS 34)
- 1 First-Gate-Loop behoben: description 166>160 → auf 154 gekürzt (test_titles_meta grün).

## Deploy / Live

- Commit c715267, CI-Run 42992901718 success (wait_ci_ohne_pflegegrad_111126.py),
  Live-Readback **40/40 ALL PASS** (research/verify_ohne_pflegegrad_live_111126.py): Artikel 200 +
  index,follow, 15 Kernzahl-Wortlaute, CTA, 0 Partner-Marker, SVG 200, Sitemap exakt 45 locs,
  RSS 34, Homepage, llms. IndexNow HTTP 200 (indexnow_submit_ohne_pflegegrad_111126.py).

## Refresh-Trigger / offene Punkte

- **PNOG-Verabschiedung (Bundestag/Bundesrat):** dann Schwellen-/Status-Absatz + die 4
  pflegebezogenen Bestandsartikel (treppenlift-zuschuss, wohnumfeldverbesserung-beantragen,
  pflegegrad-antrag-ablauf-fristen, verhinderungspflege-tagespflege-ueberblick) gegen das neue
  Recht re-prüfen. Bestandsschutz + „Reha vor Pflege"-Verschiebung beachten.
- Bewusst NICHT im Artikel: Pflegekassen-Beträge (0×), NBA-Punktzahlen des geltenden Rechts
  (gehören in die pflegegrad-/zuschuss-Artikel), KfW-Status (nur Verweis).
- Offen wie bisher: ADCELL-GO (HIRO 9440 + Pflegehase 10690), Liftstar-Follow-up (Keychain),
  Awin-Login-Status, GSC nur mit Google-Sitzung.
