# Content-Pipeline-State — ZuhauseBleiben Kompass

Letzte Aktualisierung: 2026-10-27 (Batch 10). Diese Datei ist das Produktionslog der Content-Pipeline. Sie ersetzt keine Freigabe; Launch-Modus ist aktiv (index), Formular bleibt deaktiviert.

## Bestand

### Batch 10 (2026-10-27, Cron-Lauf) — Briefing 13: Außentreppe/Außenlift
1. **Neu veröffentlicht:** treppenlift-aussentreppen-aussenlift.json — Treppenlift für die
   Außentreppe: Wetterschutz-Bausteine (verzinkte/Alu-Schiene, abgedichtete Elektronik,
   Abdeckhaube als Pflicht-Zubehör), Preisdivergenz dokumentiert (4 Fachportale: 3.500–6.500 /
   4.000–10.000 / 5.000–10.000 / ab ca. 6.000 €; Lifta-Hersteller 6.500–8.500 € inkl. Einbau,
   vollständig innerhalb der eigenen Innen-Spanne 5.500–9.900 € — Pauschal-Aufschlag widerlegbar),
   IP-Divergenz (Fachportale 54/65/67 bzw. „65+“ vs. 0 IP-Angaben auf geprüften
   Herstellerseiten HIRO/Lifta → Schutzart + Temperaturbereich aus dem Datenblatt fordern),
   HIRO 160 AIR + Lifta Allwetter GTL 320 als gekennzeichnete Herstellerangaben,
   Zusatzposten draußen (Fundament als eigene Zeile, 230-V-Außensteckdose mit FI,
   EN 81-40 im Angebot), Winter-Praxis (−10/−15 °C, Akku −⅓, kein Streusalz),
   Genehmigung/MFH-Verweis, Miete außen (~50 €/Monat gerade), Gebraucht-Divergenz
   (40-%-Abschlag vs. Privatkauf-Warnung). 12 Abschnitte, 6 FAQs, 8 Quellen,
   88/88 Ledger-Pässe (research/aussenlift-271026-ledger.json +
   research/verify_aussenlift_271026.py: 78 verbatim + 3 IP-Absenz + 7 Arithmetik),
   Grafik assets/images/treppenlift-aussentreppen-aussenlift-wetterschutz.svg
   (Marker-/Legenden-Layout nach 1. Vision-Revision; getBBox 0 Overflows + Vision sauber),
   Protokoll research/treppenlift-aussentreppen-aussenlift-batch.md. 24. Ratgeber;
   Förderbeträge bewusst nur als Verweis auf treppenlift-zuschuss.
2. **Renderer:** article-renderer.mjs specialMap +1 (Early-CTA „Anbieter für Außenlift
   vergleichen“ → treppenlift-firmen-vergleich). llms-txt.py SUMMARIES + SECTION_MAP erweitert.
3. **Testzähler:** test_articles 23→24; verify_checklists_build RSS 23→24 Items;
   test_partner_links A2 ≥ 24. Neu: research/verify_aussen_content_271026.py
   (Content-Support-Gate inkl. 8 Kernzahlen), research/verify_aussen_svg_271026.py,
   research/verify_aussen_mobile_271026.py, research/fetch_aussenlift_271026.py.
4. **Topic-Gates dokumentiert:** außenlift intent-distinct (0 Bestandsüberschneidung),
   vorkaufsnah; Verbesserungslücke = Preisstreuung + IP-Nachweispflicht aus dem Datenblatt.

### Batch 9 (2026-10-27, Cron-Lauf) — Briefing 12: Maximalgewicht/Tragkraft
1. **Neu veröffentlicht:** treppenlift-maximalgewicht.json — Treppenlift-Tragkraft: Grenze gilt für
   Person plus Zuladung (Überlastschutz startet die Fahrt nicht), belegte Herstellerwerte als
   Tabelle (HIRO 135/150/175 gerade+kurvig; Lifta Esprit 4500 Kurvenlift „bis ca. 125 kg"
   Datenblatt 01/2020; Lifta Klassik gerade 160/kurvig 135 laut Fachportal aus Datenblättern
   05/23+06/2018 bei Modellseiten-Werbung „bis 160 kg"; Handicare 115–137/160/200),
   XXL-Technik (zweirohrige Schiene, Motor, Sitzbreite 55–60 cm+), Plattformlift 250–300 kg als
   Alternative, 8-Punkte-Aufmaß-Checkliste, Preis nur als Fachportal-Schätzung 15–25 % +
   HIRO-Plattformlift-Herstellerangabe. 10 Abschnitte, 6 FAQs, 9 Quellen, 40/40 Zitate verbatim
   (research/nutzlast-271026-ledger.json), Grafik assets/images/treppenlift-maximalgewicht-
   tragkraft.svg (getBBox-Check 0 Overflows + Vision-Probe, 3 Layoutfehler gefunden und
   behoben), Protokoll research/treppenlift-maximalgewicht-batch.md. 23. Ratgeber;
   Topic SERP-basiert (GSC blockiert), Pauschalangaben-Divergenz (120 vs 125–160 kg) als
   Verbesserungslücke; keine Kannibalisierung (grep: 0 Tragkraft-Inhalte im Bestand).
2. **Renderer:** article-renderer.mjs specialMap +1 (Early-CTA „Angebote vergleichen" →
   treppenlift-angebote-vergleichen). llms-txt.py SUMMARIES + SECTION_MAP erweitert.
3. **Testzähler:** test_articles 22→23; verify_checklists_build RSS 22→23 Items;
   test_partner_links A2 ≥ 23. Neu: research/verify_nutzlast_271026.py (Ledger/Arithmetik
   40/40), research/verify_nutzlast_content_271026.py (Content-Support-Gate, 128 Checks,
   Includes Tabelle/Bullets/Kernzahlen), research/verify_nutzlast_svg_271026.py
   (getBBox-Overflow + Screenshot), research/verify_nutzlast_mobile_271026.py (390 px),
   research/verify_live_readback_nutzlast_271026.py (Live-Readback).
4. **Topic-Gates dokumentiert:** Akku/Stromausfall verworfen (commodity, kaum originär
   Belegbares); Kurventreppe verworfen (Kannibalisierungsrisiko mit treppenlift-kosten).

### Batch 8 (2026-10-26, Cron-Lauf, Abend) — Briefing 11: Schmale Treppe
1. **Neu veröffentlicht:** treppenlift-schmale-treppe.json — Treppenlift auf schmaler Treppe:
   Zwei-Fragen-Trennung (Gerätemindestbreite 61–77 cm laut Fachportal-Erhebung 07.10.2026 vs.
   verbleibende Laufbreite), Herstellerdiskrepanz dokumentiert (HIRO 70 cm vs. Lifta/TK 80 cm,
   ≤ 2 Wohneinheiten; alle 100 cm MFH), Restbreite 60 cm als MVV-TB-Musterangabe mit
   Landesfassung-Vorbehalt, DIN 18065 (800/1.000 mm) als Fachportalangabe, Messregeln +
   Aufmaß-Checkliste, Alternativen (Stehlift, Plattformlift 90–110 cm, Treppensteiger,
   Deckenlift, Hauslift), Preisdifferenzierung nach Treppenform statt Breite. 10 Abschnitte,
   6 FAQs, 5 Quellen (VZ, 2 Fachportale mit Methodik, Lifta + HIRO als Herstellerangaben),
   53/53 Zitate verbatim (research/schmale-treppe-261026-ledger.json), Grafik
   assets/images/treppenlift-schmale-treppe-messplan.svg (Sichtkontrolle: 0 viewBox-Overflows,
   Vision-Probe sauber), Protokoll research/treppenlift-schmale-treppe-batch.md. 22. Ratgeber;
   Förderbeträge bewusst nur als Verweis auf treppenlift-zuschuss.
2. **Renderer:** article-renderer.mjs specialMap +1 (Early-CTA „Anbieter für Aufmaß vergleichen“
   → treppenlift-firmen-vergleich). llms-txt.py SUMMARIES + SECTION_MAP erweitert.
3. **Testzähler:** test_articles 21→22; verify_checklists_build RSS 21→22 Items;
   test_partner_links A2 ≥ 22. Neu: research/verify_schmale_treppe_content_261026.py
   (Content-Support-Gate, 88 Checks, tags/citation-normalisierte Fließtextvergleiche —
   sup-Anker brechen naive Vergleiche) + research/verify_schmale_treppe_261026.py
   (Ledger/Arithmetik 53/53).
4. **Topic-Gates dokumentiert:** Wartung (post-purchase, 10+ Konkurrenten), Einbau-Ablauf
   (dicht besetzt), Pflegegrad-Widerspruch (VZ-Dominanz) verworfen; schmale Treppe gewählt
   (kaufnah, intent-distinct, SERP-Widersprüche als Verbesserungslücke).

### Batch 7 (2026-10-26, Cron-Lauf) — Briefing 10: Steuer-Route
1. **Neu veröffentlicht:** treppenlift-steuerlich-absetzen.json — § 35a EStG (20 % der Arbeitskosten,
   max. 1.200 €, nur Arbeitskosten, Rechnung + Konto-Zahlung, Förder-Ausnahme Abs. 3 Satz 2)
   und § 33 EStG (zumutbare Belastung, Nachweise), Referentenentwurf 2027 (15 %/900 €, nicht
   beschlossen) strikt getrennt. 10 Abschnitte, 6 FAQs, 4 Quellen, 41/41 Zitate verbatim
   (research/steuer-261026-ledger.json), Grafik assets/images/treppenlift-steuer-weg.svg
   (Sichtkontrolle mit 2 gefundenen und behobenen Layoutfehlern), Protokoll
   research/treppenlift-steuerlich-absetzen-batch.md. 21. Ratgeber; Topic-Wahl SERP-basiert,
   da GSC im Cron nicht abrufbar (keine Google-Sitzung, kein Vault-Login).
2. **Renderer:** article-renderer.mjs specialMap +1 (Early-CTA „Förderung prüfen" →
   treppenlift-zuschuss). llms-txt.py SUMMARIES + SECTION_MAP erweitert.
3. **Testzähler:** test_articles 20→21; verify_checklists_build RSS 20→21 Items;
   test_partner_links A2 ≥ 21. Neu: research/verify_steuer_content_261026.py (Content-Support-Gate
   für den Artikel) + research/verify_steuer_261026.py (Ledger/Arithmetik).
4. **Pflicht-Refresh:** nach Verabschiedung ESt-Reformgesetz 2027 § 35a-Zahlen neu prüfen (Ledger-Notiz).

### Batch 6 (2026-10-23, Cron-Lauf) — Briefing 1 promoviert
1. **Neu veröffentlicht:** treppenlift-angebote-vergleichen.json — Promotion des vollständig gegateten
   Drafts vom 14.10. nach heutiger Re-Verifikation aller Quellen (§ 40 SGB XI 4 180/16 720, 3/5 Wochen;
   VZ Treppenlifte 13 Claims; VZ BGH I ZR 96/20; Details + Gate-Ergebnisse:
   research/treppenlift-angebote-vergleichen-batch.md). 20. Ratgeber; Phase 1 damit vollständig live.
2. **Renderer:** generate.mjs — Draft-Block + DRAFT_PAGES entfernt (URL jetzt in beiden Modi als
   Artikel); article-renderer.mjs specialMap-Eintrag → treppenlift-zuschuss „Förderung prüfen".
3. **Testzähler:** test_articles 19→20; test_site-Draft-Sonderfall entfernt; verify_checklists_build
   (RSS 20 Items, Sitemap enthält Artikel, llms deckt ab); test_partner_links A2 ≥ 20; llms-txt.py
   SUMMARIES + SECTION_MAP ergänzt.

### Batch 5 (2026-10-19, Cron-Lauf, Abend) — Briefing 7
1. **Neu veröffentlicht:** badumbau-angebote-vergleichen.json — Vergleichsmechanik für Badumbau-Angebote (Vergleichsbasis: dieselbe Beschreibung für jeden Betrieb; Positionstabelle Rückbau→Logistik; Abdichtung nach DIN 18534 Neufassung 2025-10 mit W1-I/W2-I und fugenlos=Vereinbarungspflicht; Preisbindung KV vs. Festpreis mit 15–20-%-Hinweisschwelle; Zusatzarbeiten § 650b/650k BGB; Abschläge § 632a BGB; Verjährung § 634a BGB 2/5 Jahre ab Abnahme; 8-Punkte-Fragenliste pro Betrieb). 8 Abschnitte, 6 FAQs, 9 Quellen mit Verbatim-Evidenz (research/badumbau-angebote-ledger.json, 25/25 maschinell verifiziert), Grafik assets/images/badumbau-angebote-vergleich.svg (Chromium-Sichtkontrolle), Protokoll research/badumbau-angebote-vergleichen-batch.md. Keine Marktpreise erfunden; DIN-Angaben als Hersteller-/Fachdarstellung gekennzeichnet; Rechtszahlen nur mit BGB-Quellenbeleg.
2. **Renderer:** article-renderer.mjs specialMap-Eintrag +1 (Early-CTA „Badumbau planen“ → /bad-umbau-barrierefrei.html statt Bad-Cluster-Default „Förderung prüfen“ → Treppenlift-Zuschuss).
3. **Testzähler:** test_articles.py 17→18 Artikel.
4. **Abgrenzung:** wanne-zur-dusche (Produktentscheidung/Bauablauf) und bad-umbau-barrierefrei (Gesamtplanung) unangetastet; neuer Artikel deckt die dedizierte Angebotsvergleichs-Mechanik (KV/Festpreis, Abschläge, §§ 650b/650k/634a, DIN-18534-Nachfragen) — intent-distinct, Related-Links im Bad-Cluster.

### Batch 4 (2026-10-19, Cron-Lauf) — Briefing 6
1. **Neu veröffentlicht:** bodengleiche-dusche-altbau.json — Machbarkeits-Fahrplan Altbau (vier Prüfentscheidungen: Aufbauhöhe, Weg zum Fallrohr, Decke/Konstruktion, Norm als Zielgröße), flache Alternative mit Restschwelle als ehrliche Option, 10-Punkte-Fragenliste für den Vor-Ort-Termin, Förderlogik § 40 Abs. 4 SGB XI (4.180/16.720 €, Ermessen), KfW 455-B Antragstopp (19.10. verifiziert) + 159 inkl. wörtlichem Kombinationsverbot/Ausnahme, § 554 BGB-Verweis mit Link auf Mietwohnung-Ratgeber. 8 Abschnitte, 6 FAQs, ~2.390 Wörter, 10 Quellen mit Verbatim-Evidenz (research/altbau-dusche-ledger.json, 29/29 Zitate maschinell verifiziert), Grafik assets/images/bodengleiche-dusche-altbau-pruefpunkte.svg (Chromium-Sichtkontrolle), Protokoll research/bodengleiche-dusche-altbau-batch.md + Acceptance research/evidence/bodengleiche-dusche-altbau-acceptance.md.
2. **Renderer-Fix:** article-renderer.mjs isBad-Cluster erkennt jetzt auch „dusche“ im Slug (bodengleiche-dusche-altbau landete sonst im lift-Cluster mit falschen „Passend dazu“-Links). Early-CTA-Ziel für den neuen Artikel: treppenlift-mietwohnung („Mietwohnung: Zustimmungen klären“).
3. **Testzähler:** test_articles.py 16→17 Artikel.

### Live-Kern (vor Batch 1/2, status editorial-reviewed-preview)
- treppenlift-kosten
- treppenlift-zuschuss
- bad-umbau-barrierefrei
- wanne-zur-dusche
- treppenlift-mieten
- treppenlift-firmen-vergleich
- treppenlift-gebraucht-oder-neu

### Batch 3 (2026-10-16, Cron-Lauf)
1. **Neu veröffentlicht:** treppenlift-mietwohnung.json (Briefing 4 laut SEO-STRATEGIE.md) — Zustimmungs-Fahrplan Miete/Eigentum/gemeinsames Treppenhaus (§ 554 BGB, § 20 WEG, § 40 SGB XI wörtlich belegt), Brandschutz als häufigster Ablehnungsgrund, Antrags-/Rückbau-/Sicherheitsleistung-Einordnung, 6-Schritte-Checkliste, 6 FAQs, 7 Quellen mit Verbatim-Evidenz (research/mietwohnung-ledger.json), Grafik assets/images/treppenlift-mietwohnung-zustimmung.svg (visuell geprüft), Protokoll research/treppenlift-mietwohnung-batch.md + Acceptance research/evidence/treppenlift-mietwohnung-acceptance.md. Status editorial-reviewed-preview → im Launch-Index wie die übrigen Ratgeber.
2. **Renderer-Fix:** article-renderer.mjs rendert jetzt `paragraphs_after` (Feld wurde bisher gedroppt). Betraf live den Artikel treppenlift-mieten: Schlussabsatz der Beispielrechnung (Break-even 23,6 Monate) fehlte seit Deploy 15.10. Nur dieser Artikel nutzt das Feld.
3. **Testzähler:** test_articles.py 11→12 Artikel.

### Batch 1 (2026-10-14, vorherige Session; Scratch: treppenlift-batch/, bad-batch/)
- Keine neuen content-ready-Dateien in Batch 1; bestehende 7 Artikel waren Gegenstand von Verifikation/Ledgern. Protokolle: research/treppenlift-batch.md, research/bad-foerderung-batch.md.

### Batch 2 (2026-10-15, diese Session) — Cluster „Hausnotruf" + „Wohnraum-Anpassung klein"
Neue content-ready-Dateien (alle status review-required):
1. hausnotruf-kosten-anbieter-vergleich.json — Kostenrahmen, Basistarifbausteine, Pflegekasse (27 €/Monat, Voraussetzungen), Vertrags-/Kündigungsgrundlagen, Vergleichscheckliste. 8 Abschnitte, 6 FAQ, 4 Quellen, ~1.516 Wörter.
2. hausnotruf-sturzerkennung-oder-knopf.json — Funktionsprinzip, Grenzen (langsame Stürze), Fehlalarme + Vorlauf/Abbruch, Entscheidungsmatrix, Kosten des Aufpreises, Notrufdaten/DSGVO, Beratungcheckliste. 9 Abschnitte, 6 FAQ, 3 Quellen, ~1.516 Wörter.
3. tuerbreiten-schwellen-schnellcheck.json — Messanleitung + Messbogen, Normorientierung (DIN 18040-2 als Fachportaldarstellung), Rampen-Stufenlogik, Kostenfaktoren Türverbreiterung, § 554 BGB, Pflegekasse vor Bau, Schnell-Check. 8 Abschnitte, 6 FAQ, 5 Quellen, ~1.659 Wörter.
4. beleuchtung-orientierung-im-alter.json — Sehveränderung, multiple Lichtquellen, Blendung/Kontraste, Raum-Kategorientabelle, Nachtlicht, Bewegungsmelder mit Vorbehalten, Lichtfarbe/Dimmen, Energie/Kostenstruktur, Einkaufscheckliste. 9 Abschnitte, 6 FAQ, 5 Quellen, ~1.612 Wörter.

Neue Bilder (assets/images/, alle „KI-Illustration · schematisch"):
- hausnotruf-ablauf.svg
- hausnotruf-sturz-entscheidung.svg
- tuer-schwelle-messcheck.svg
- licht-orientierung-tagesverlauf.svg

Recherche-Dokumente:
- research/hausnotruf-wohnen-klein-batch.md (Batch-Dokument Cluster A+B: Clusterwahl, SERP-Check, Quellenkette, Grenzen)
- research/evidence/batch2-hausnotruf-evidence.md (wörtliche Belege Cluster A)
- research/evidence/batch2-wohnen-klein-evidence.md (wörtliche Belege Cluster B)
- Rohabrufe/Scratch (temporär): /Users/mac/.hermes/profiles/milo/cache/scratch/batch2-clusters/

## Zustand und Gates

- **Aktualisiert 2026-10-16 (Lauf 2):** Die 4 Batch-2-Artikel wurden am 16.10. nach Quellen-Verifikation veröffentlicht (Commit 5f38a01, Parallel-Lauf) und sind live/indexierbar; die beiden folgenden historischen Batch-2-Zeilen beschreiben den Stand zum Batch-Zeitpunkt. Renderer/Generate wurden im Lauf 2 gezielt geändert (Cluster-Related + CTA-Ziele + Footer), mit Tests in beiden Build-Modi.
- Alle 4 Batch-2-Artikel: status „review-required“. Kein Build, kein Deploy, keine Sitemap-Änderung, noindex-Status unangetastet.
- Renderer/Generate/Design/CTA/Tests: nicht angefasst (Sperrliste beachtet).
- Offene Integrationsfragen für das Gate: **Frage 1 und 2 am 2026-10-16 (Lauf 2) gelöst** — article-renderer.mjs hat jetzt Cluster-Logik (bad/care/lift per Slug-Präfix) für „Passend dazu" und kontextpassende Early-CTA-Ziele (specialMap + Cluster-Defaults); Pflege-Cluster-Artikel verlinken sich gegenseitig statt in den Treppenlift-Trichter. Verbleibend:
  1. Vor Veröffentlichung: Pflegekassen-27-Euro-Stand (VZ, Stand 29.07.2026) erneut gegen aktuelle Quelle prüfen; KfW-Status unverändert lassen (455-B geschlossen, 159 offen — Stand 2026-10-14, betrifft bestehende Artikel).
  2. Bildpfade existieren; visuelle Layoutprüfung bleibt Gate.
- Cluster-Historie für spätere Auswertung: Hausnotruf laut HORIZONTALE-EXPANSION.md organischer angrenzender Cluster (Malteser als Referenz, Awin 112616 öffentlich bewerbbar); Wohnraum-klein stärkt Upsell-Pfad zu Treppenlift/Bad.

## Qualitätsgate-Regeln, die in Batch 2 angewandt wurden (für künftige Batches)

- Keine Preis-/Marktmittelwerte ohne verifizierbare Primärquelle; Redaktions-/Anbieterangaben stets als solche kennzeichnen.
- Fördernennungen immer mit Höchstbetrag-Logik (4.180 € je Maßnahme, Ermessen, keine Zusage).
- Medizinische Themen (Sturz, Demenz) nur als allgemeine Orientierung + explizite Grenzen; keine Diagnosen, keine individuellen Empfehlungen.
- Normangaben nur als gekennzeichnete Fachportaldarstellungen, nie als Normbestätigung für konkrete Objekte.
- Keine Gesundheitsdatenabfragen, keine Formulare, keine Partnerzusage im Text.
- Bilder: eigene schematische SVGs mit KI-Label, title/desc, Grenztext, viewBox für Renderer-Dimensionserkennung.

## Batch: hilfsmittel-dusch-wc-uebernahme (Briefing 9, 2026-10-21)

- Artikel live/indexierbar (Commit siehe git log): Dusch-WC — Krankenkassen-Route über gelistete
  Toilettenaufsätze mit Wascheinrichtung (PG 33.40.05, enge Arm-/Hand-Indikation), Pflegekassen-
  Wohnumfeldroute als Einzelfall, Selbstkauf-Kriterien, Antrags-Checkliste. 8 Quellen, 20/20 Zitate
  verbatim (`research/dusch-wc-ledger.json`), Beweisdateien `research/evidence/dusch-wc-*`.
- Renderer: specialMap-Eintrag (Early-CTA → hilfsmittel-pflegekasse-uebernahme); Care-Cluster trifft
  via Slug-Präfix. test_articles-Zähler 18→19 im selben Commit.
- Nicht Teil des Batches: In-Flight-Arbeiten anderer Läufe (RSS-Feed, Checklisten-Build, llms.txt,
  Growth-Dokumente) bleiben unangetastet/uncommittet.
