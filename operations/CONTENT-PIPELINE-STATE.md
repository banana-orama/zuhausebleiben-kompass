# Content-Pipeline-State — ZuhauseBleiben Kompass

Letzte Aktualisierung: 2026-10-16 (Batch 3). Diese Datei ist das Produktionslog der Content-Pipeline. Sie ersetzt keine Freigabe; Launch-Modus ist aktiv (index), Formular bleibt deaktiviert.

## Bestand

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

- Alle 4 Batch-2-Artikel: status „review-required". Kein Build, kein Deploy, keine Sitemap-Änderung, noindex-Status unangetastet.
- Renderer/Generate/Design/CTA/Tests: nicht angefasst (Sperrliste beachtet).
- Offene Integrationsfragen für das Gate:
  1. article-renderer.mjs „Passend dazu"-Logik ordnet Nicht-Treppenlift-Slugs derzeit dem Treppenlift-Kontext zu (related-Filter auf slug.startsWith('treppenlift')). Sobald Hausnotruf/Wohn-Klein-Artikel freigegeben werden, sollte die Related-Zuordnung erweitert werden (z. B. thematische Cluster-Map). Bewusst nicht selbst geändert.
  2. Early-CTA-Zieltexte des Renderers sind treppenlift-spezifisch („Anbieter prüfen", „Kosten vergleichen"); für die neuen Cluster prüfen, ob eigene CTA-Ziele (z. B. Hausnotruf-Checkliste) sinnvoll sind.
  3. Vor Veröffentlichung: Pflegekassen-27-Euro-Stand (VZ, Stand 29.07.2026) erneut gegen aktuelle Quelle prüfen; KfW-Status unverändert lassen (455-B geschlossen, 159 offen — Stand 2026-10-14, betrifft bestehende Artikel).
  4. Bildpfade existieren; visuelle Layoutprüfung bleibt Gate.
- Cluster-Historie für spätere Auswertung: Hausnotruf laut HORIZONTALE-EXPANSION.md organischer angrenzender Cluster (Malteser als Referenz, Awin 112616 öffentlich bewerbbar); Wohnraum-klein stärkt Upsell-Pfad zu Treppenlift/Bad.

## Qualitätsgate-Regeln, die in Batch 2 angewandt wurden (für künftige Batches)

- Keine Preis-/Marktmittelwerte ohne verifizierbare Primärquelle; Redaktions-/Anbieterangaben stets als solche kennzeichnen.
- Fördernennungen immer mit Höchstbetrag-Logik (4.180 € je Maßnahme, Ermessen, keine Zusage).
- Medizinische Themen (Sturz, Demenz) nur als allgemeine Orientierung + explizite Grenzen; keine Diagnosen, keine individuellen Empfehlungen.
- Normangaben nur als gekennzeichnete Fachportaldarstellungen, nie als Normbestätigung für konkrete Objekte.
- Keine Gesundheitsdatenabfragen, keine Formulare, keine Partnerzusage im Text.
- Bilder: eigene schematische SVGs mit KI-Label, title/desc, Grenztext, viewBox für Renderer-Dimensionserkennung.
