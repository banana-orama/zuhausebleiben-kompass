# Batch 9 — Briefing 12: Treppenlift Maximalgewicht / Tragkraft (27.10.2026)

## Topic-Wahl (SERP-basiert, GSC weiter blockiert)
- Kandidaten gegen bestehenden Bestand gedeupelt (grep content-ready): Nutzlast/Maximalgewicht 0 Treffer im Lift-Cluster; Akku/Stromausfall nur passierende Erwähnungen; Kurventreppe mehrfach erwähnt (Kosten/gebraucht/schmale) — kannibalisierungsanfällig.
- SERP 27.10.: Händler-FAQs (TS-Treppenlifte, MC Seniorenprodukte, Fital) + 2 Fachportale (altersgerecht-modernisieren 17.08.2026, treppenliftwissen Juli 2026) + Infoportal treppenlifter.me. Pauschalangaben divergieren („bis 120 kg" vs „125–160 kg je Modell") — weil die Zahl je Modell/Ausführung variiert. Keine Seite dokumentiert Herstellerwerte direkt nebeneinander.
- **Verbesserung:** verbatim-Herstellerbelege (HIRO 135/150/175; Lifta Esprit 4500 Kurvenlift 125 kg PDF; Handicare-Leiter 115–200) + Lifta-Klassik-Diskrepanz selbst aus Primärquellen dokumentiert (gerade 160 vs. kurvig 135, Modellseite bewirbt pauschal 160) + Zuladung/Überlastschutz + Aufmaß-Checkliste. Kaufnah (Kauf filter-Frage), intent-distinct, keine Kannibalisierung.
- Verworfene Alternativen: Akku/Stromausfall (commodity-Ratgeber, wenig originär Belegbares), Wartung/Einbau (bereits in Batch 8 verworfen).

## Quellen (9, alle verbatim, 40/40 PASS: research/verify_nutzlast_271026.py)
1. HIRO LIFT (Hersteller): hiro.de/treppenlift/ — ECO „Trägt 135 kg", Optionstabelle (150/175), Baseline ohne 150-kg-Option
2. HIRO LIFT (Hersteller): hiro.de/modell/neo/ — „bis 135 kg Standard, bis 150 kg Optional, höhere Belastungen bis 175 kg auf Anfrage"
3. Lifta (Hersteller): Datenblatt Esprit 4500 (PDF, Stand 01/2020) — „Tragkraft bis ca. 125 kg" (Kurventreppenlift)
4. Lifta (Hersteller): lifta.de/treppenlift/ — Klassik „Höchste Belastbarkeit bis 160 kg" (Marketing ohne Ausführungsangabe)
5. Handicare GmbH (Herstellerangabe): 1000XXL — „Traglast bis zu 200 kg", Leiter 125/115–137/160/200, XXL-Ausstattung
6. Altersgerecht Modernisieren (Fachportal 17.08.2026): Tragkraft-Tabelle, Lifta-Diskrepanz (Klassik 2000 05/23 vs. 5000 06/2018), Zuladung, Überlastschutz, Garantie-Einordnung
7. Treppenliftwissen (Fachportal Juli 2026): Standard 120–160 kg, XXL-Technik, Plattformlift 250–300 kg, Aufmaß Probesitzen+Statik, Preisschätzung 15–25 %
8. Treppenlifter.me (Infoportal): „bis zu 120 kg" — dokumentiert die Spannweite der Pauschalangaben
9. HIRO LIFT (Hersteller): hiro.de/preise/ — Plattformlift „Kosten zwischen 11.000 und 38.000 Euro"

Evidence: research/evidence/nutzlast-271026/ (8 HTML→TXT + Lifta-PDF + extrahierte PDF-Textdatei + SVG-/Mobile-Screenshots). Hinweis: Lifta-PDF-Textdatei enthält die Tabellenzeilen des PDF-Textlayers; Quotes darauf geprüft.

## Artikel
content-ready/treppenlift-maximalgewicht.json — 10 Abschnitte, 6 FAQs, 9 Quellen, Wertetabelle mit 6 belegten Modellen, Beispielrechnung 118+7=125 kg (skriptgeprüft), Aufmaß-Checkliste (8 Punkte). Status editorial-reviewed-preview. Vorlage: content-drafts/treppenlift-maximalgewicht.json (review-required, verbatim-identisch bis auf Status).

## Grafik
assets/images/treppenlift-maximalgewicht-tragkraft.svg (980×680, role=img, title/desc, KI-Label in Caption). Sichtkontrolle: getBBox-Overflow-Check 0 Overflows (research/verify_nutzlast_svg_271026.py, Chromium) + Vision-Probe. Gefundene und behobene Fehler: 200-kg-Balken dark-on-dark (Label unsichtbar), „Zuladung"-Label kollidierte mit Fußstütze, Bodenleiste schnitt Feinzeile. Re-Probe sauber.

## Renderer/Tools
- article-renderer.mjs: specialMap +1 (Early-CTA „Angebote vergleichen" → treppenlift-angebote-vergleichen)
- research/llms-txt.py: SUMMARIES + SECTION_MAP +1

## Gates
- Ledger 40/40 verbatim + Arithmetik 9 Checks (research/verify_nutzlast_271026.py)
- npm test: build beide Modi, test_site PASS (47 Seiten), test_articles PASS (23 Artikel, Zähler 22→23), measurement+consent 20 passed, test_partner_links ALL PASS (A2 ≥ 23)
- verify_checklists_build ALL PASS (RSS 23, Sitemap, llms)
- Content-Support-Gate (research/verify_nutzlast_content_271026.py): 128 Checks ALL PASS (alle JSON-Keys inkl. Tabelle/Bullets im HTML, [1]–[9] lösen auf, Related 3× Lift-Cluster, Kernzahlen, keine Verkaufsclaims)
- Mobile 390 px: 0 px Overflow, Tabelle scrollbar, 1 H1 (research/verify_nutzlast_mobile_271026.py)

## Grenzen/Disziplin
- Keine Marktpreise: nur Fachportal-Schätzung 15–25 % als Anhaltspunkt [7] + HIRO-Plattformlift-Spanne als Herstellerangabe [9]
- „Kein Garantiefall" nur als gekennzeichnete Fachportalangabe; Garantiebedingungen dem Vertrag des Herstellers vorbehalten
- Herstellerwerte mit Abrufdatum; datierte Datenblätter (01/2020, 05/23, 06/2018) als Teil des Befunds ausgewiesen
- Keine Förderzahlen neu behauptet; Verweis auf treppenlift-zuschuss
