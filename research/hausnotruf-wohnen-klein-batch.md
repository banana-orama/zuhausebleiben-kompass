# Batch 2: Cluster „Hausnotruf" und „Wohnraum-Anpassung klein" — Rechercheprotokoll

Prüfdatum: 15. Oktober 2026 (Systemdatum CEST). Auftrag: vier vollständige content-ready-Ratgeber in zwei Clustern plus je ein Batch-Dokument mit Evidenzdateien; Status review-required. Kein Build, kein Deploy, keine Änderung an article-renderer.mjs, generate.mjs, design.css, cta.css, Tests oder bestehenden Ratgebern.

## Clusterwahl: Suchnachfrage-Hypothese und warum Vermittler hier rangieren

Beide Cluster wurden gegen die bestehenden sieben Artikel (treppenlift-kosten, treppenlift-zuschuss, bad-umbau-barrierefrei, treppenlift-firmen-vergleich, treppenlift-gebraucht-oder-neu, treppenlift-mieten, wanne-zur-dusche) abgegrenzt; kein Thema doppelt bedient.

### Cluster A „Hausnotruf"

Suchnachfrage-Hypothese (qualitativ, aus SERP-Struktur am 15.10.2026, keine Suchvolumendaten): Die Abfragen „Hausnotruf Kosten Anbieter monatlich" und „Hausnotruf mit Sturzerkennung" lieferten dichte Ergebnislisten mit mehreren dedizierten Vergleichs- und Ratgeberdomains (pflegekompass.de, hausnotruf-ratgeber.de, deinpflegevergleich.de, notrufsysteme.de, hauspflege-24.de, meinpflegefinder.de, hausnotruf-kosten.de, liva-pflege.de) sowie starker Anzeigendurchdringung (Malteser, pflege.net-Werbung, senioren-beratung-deutschland, gardia, patronus, senioren-beratung). Zahlreiche spezialisierte Vergleichsseiten und Affiliate-Sites in den organischen Treffern sind das klassische Muster einer transaktionsnahen, verzweigten Nachfrage, bei der Vermittler und Ratgeber-Portale rangieren, weil die Suchintention „Anbieter einordnen, Kosten einordnen, Vertrag prüfen" auf redaktionelle Sammlung zielt, nicht auf eine einzelne Herstellerseite. Ergänzend: operations/HORIZONTALE-EXPANSION.md führt Hausnotruf bereits als angrenzendes Cluster mit Markenfit (Referenz Malteser, Awin-Programm öffentlich bewerbbar). Der nötige Nutzen ist kein weiterer Preisvergleich, sondern eine Entscheidungs- und Vertragshilfe: Welche Leistungsbausteine muss ein Angebot benennen, was übernimmt die Pflegekasse unter welchen Voraussetzungen, welche Vertrags- und Kündigungsfragen sind vor der Unterschrift offen, und was leistet automatische Sturzerkennung realistisch — inklusive Grenzen und Fehlalarmthema. Genau diese zwei Seiten decken zwei getrennte Suchintentionen (Kosten/Anbieter/Vertrag vs. Funktionsprinzip/Eignung), ohne die bestehenden Treppenlift-Artikel zu kanibalisieren.

### Cluster B „Wohnraum-Anpassung klein"

Suchnachfrage-Hypothese: Die Abfragen zu Türbreiten/Schwellen/Rampe und zu Beleuchtung im Alter zeigen heterogene Treffermengen aus Fachportalen (nullbarriere.de, din18040.de, online-wohn-beratung.de, barrierefrei.de), Bau-/DIY-Märkten (toom Selbstmach-Seite) und Branchenshops (thiele-shop, dema.nrw) — kein dominanter redaktioneller Standardartikel für die Zielgruppe ältere Menschen und Angehörige. Für „Beleuchtung Orientierung im Alter" rangieren Demenz-Fachquellen (desideria.org, demenzwiki, lichtatlas, Alzheimer-Gesellschaft Düsseldorf), ein Branchenportal (licht.de) und Pflegeportale; die Intention ist Orientierungswissen mit konkreter Einkaufshilfe, keine Hersteller- oder Shoppingsuche im engeren Sinn. Intermediärs-Ranking ist hier erklärbar durch fragmentierte Nachfrage zwischen Norm-, DIY- und Pflegesicht; ein Ratgeber, der Messen, Normorientierung, Mietrecht, Pflegekasse und Einkaufskategorien verbindet, füllt eine Lücke zwischen Bauhandwerker-Inhalten und Demenz-Fachtexten. Abgrenzung nach innen: bestehende Artikel behandeln große Maßnahmen (Treppenlift, Badumbau, Wannentausch); die beiden neuen Seiten bedienen die kleinen, schnell umsetzbaren Maßnahmen und verlinken dorthin weiter — Upsell-Pfad statt Kanibalisierung.

## SERP-/Konkurrenzcheck je Artikel (Websuche 15.10.2026, keine Google-Rangfolge, keine Volumendaten)

1. hausnotruf-kosten-anbieter-vergleich — Query „Hausnotruf Kosten Anbieter monatlich Vertrag". Treffer u. a. pflegekompass.de, hausnotruf-ratgeber.de, deinpflegevergleich.de, notrufsysteme.de, hauspflege-24.de, meinpflegefinder.de, liva-pflege.de. Suchintention: Kostenrahmen, Pflegekassenzuschuss, Anbieterauswahl, Vertragsdetails. Eigene Verbesserung: Leistungsbausteine-Tabelle statt Preistabelle, Vertrags-/Kündigungsblock, druckbare Vergleichscheckliste, Anbieterangabe (Malteser) nur als Beispiel mit Grenzen.
2. hausnotruf-sturzerkennung-oder-knopf — Query „Hausnotruf mit Sturzerkennung automatische Erkennung". Treffer: pflegekompass (7-Modelle-Vergleich), pflege.net Sturzsensor, pflege-einstieg, Bing-Anzeigen (Malteser Notarmband, gardia, Patronus, PATRIOT/Uhr-Anbieter). Suchintention: Funktionsprinzip, Zuverlässigkeit, Aufpreis, Eignung. Eigene Verbesserung: Systemlogik mit Vorlauf/Abbruch, ausdrückliche Erkennungsgrenzen ohne Quote, Fehlalarm-Kostenfrage, Entscheidungsmatrix, DSGVO/Notrufdaten-Bewusstsein.
3. tuerbreiten-schwellen-schnellcheck — Query „Türbreite Schwelle Rampe barrierefrei Umbau Kosten". Treffer: nullbarriere.de, din18040.de, online-wohn-beratung.de, barrierefrei.de, toom, thiele-shop, dema.nrw, konstruktionsfuhrer (Preisspanne 400–3.000 Euro, bewusst NICHT übernommen, da unsourced). Suchintention: Selbstmessen, Schwellenlösung, Kostenfaktoren, Mietwohnung. Eigene Verbesserung: Messbogen-Checkliste, Normorientierung mit Quellenpfad (Fachportaldarstellung der DIN 18040-2), Rampen-Dreistufenlogik, § 554 BGB, Pflegekasse vor Bau.
4. beleuchtung-orientierung-im-alter — Query „Beleuchtung Orientierung im Alter Demenz Nachtlicht". Treffer: desideria.org, demenzwiki, lichtatlas.de, alzheimer-duesseldorf (404 beim Abruf), pflege-panorama, nullbarriere Beleuchtungsseite, licht.de-PDF. Suchintention: Verständnis, konkrete Produktkategorien, Energiefrage. Eigene Verbesserung: Raum-Kategorien-Tabelle (keine Marken), Nachtlicht/Bewegungsmelder mit Vorbehalten, Energie-/Kostenstruktur ohne erfundene Preise, Einkaufscheckliste.

## Primärquellen: direkte Abrufe, Belege und Grenzen

Methode: curl/urllib-Liveabrufe am 15.10.2026 (CEST), gespeichert unter /Users/mac/.hermes/profiles/milo/cache/scratch/batch2-clusters/ (rohe HTML/PDF und bereinigte .txt). Keine Archivkopien. web_extract blieb, wie im vorherigen Batch, im Such-only-Backend stecken (Fehlermeldung „search-only backend and cannot extract URL content"); Extraktion erfolgte deshalb direkt, nicht vorgetäuscht.

1. Verbraucherzentrale „Hausnotrufsysteme erklärt" (Stand 29.07.2026, Abruf 15.10.2026): Basistarif meist 27–40 Euro/Monat; seit 1. April 2026 bis zu 27 Euro/Monat Übernahme bei Pflegegrad plus Voraussetzungen (fast ganztägig allein, keine Hilfe per handelsüblichem Telefon möglich), MD-Prüfung; Anbieter muss Vertragspartner der Pflegekasse sein; Basistarif enthält Gerät, Funksender, Installation/Einweisung, 24h-Zentrale; Zusatzleistungen inkl. Falldetektoren 30–50 Euro oder mehr; Demenz-Grenze des Knopfsystems; Telefon-/IP-Anschluss, SIM/Akku 10–20 h, Funkreichweite meist bis 50 m; Notrufdaten (Adresse, Gesundheitszustand, Medikamente, Kontakte) DSGVO-konform zu speichern. Wörtliche Belege im Evidenzfile.
2. BMG „Pflegehilfsmittel": Notrufsystem ausdrücklich als Beispiel technischer Pflegehilfsmittel; Antragsweg und Fristen. Wörtliche Belege im Evidenzfile.
3. Malteser Hausnotruf-Seite (Abruf 15.10.2026): Anbieterangaben — Fixpreis ohne versteckte Kosten, Installation und Wartung inklusive, Kündigung monatlich zum Monatsende, Stufen Grundsicherheit/Komplettsicherheit/Komplettsicherheit Plus, Zuschuss 27,00 € ab Pflegegrad 1 laut Anbieterdarstellung, Funktion auch über Mobilfunk. Nur als verbatim gekennzeichnete Anbieteraussage verwendet, kein Preisvergleich daraus gebaut.
4. Verbraucherzentrale „Widerruf: Verträge rückgängig machen": Grundlagen Widerrufsrecht Verbraucherverträge (nur allgemeine Grundlagen verwendet, keine Fristbehauptung über den konkreten Hausnotrufvertrag hinaus).
5. pflege.net „Hausnotruf Sturzsensor" (Redaktionsratgeber, Abruf 15.10.2026): Sensorik Beschleunigungssensoren/Gyroskope; Grenzen — langsames Zusammensacken/Abrutschen oft nicht erkannt; Fehlalarme durch heftige Armbewegungen/Klatschen/schnelles Hinsetzen; Kostenangabe Systeme mit Automatik 35–85 Euro/Monat, Aufpreis nicht pflegekassengedeckt; RKI-nannte Sturzstatistik (23,8 % ab 65, > 4 Mio./Jahr) nur als Redaktionsangabe zitiert mit Urhebernennung; Anbietersystematik (Sturzsensor vs. Falldetektor, Bodenmatten, Radar). Nicht übernommen: konkrete Anbieter-Preisliste als Marktdaten (nur Redaktionsangabe mit Grenzen genannt).
6. BeWo TeleHealthcare „Sturzerkennung beim HausNotruf" (Herstellerangaben, Abruf 15.10.2026): Ablauf Mustererkennung → Vorlauf 10–30 Sek. → Abbruchsignal → automatischer Notruf ohne Reaktion; Situationstabelle (Reglosigkeit ausgelöst, Bewegung nach 20 s kein Alarm, Hinsetzen kein Alarm, Sensor auf Tisch kein Alarm); „Kein 100%iger Schutz", sehr langsame Stürze seltener erkannt, manueller Knopf bleibt; Zielgruppenliste. Herstellerperspektive im Text gekennzeichnet.
7. nullbarriere.de DIN 18040-2 Türen (Fachportaldarstellung, Abruf 15.10.2026): lichte Breite innerhalb von Wohnungen ≥ 80 cm, für Rollstuhlfahrer ≥ 90 cm; Schwellen grundsätzlich nicht zulässig, unvermeidbar innerhalb ≤ 1 cm, abgeschrägt/abgerundet, leicht überrollbar; Drückerhöhe 85 cm-Bereich. Fachportaldarstellung gekennzeichnet, keine Normprüfung durch uns.
8. din18040.de „Eingang, Türen, Fenster" (Fachportaldarstellung): Eingangstüren ≥ 90 cm lichte Breite, ≥ 205 cm Höhe; Außenschwellen unvermeidbar ≤ 2 cm; Sicherheitsmarkierungen (Wechselkontrast) an großflächig verglasten Türen; kontrastreiche, gut beleuchtete Zugänge.
9. BMG „Zuschüsse zur Wohnungsanpassung": Türverbreiterungen und fest installierte Rampen als Beispiele bezuschusster Maßnahmen; bis zu 4.180 Euro, Pflegegrade 1–5, zweite Gewährung möglich. Konsistent mit bestehendem Batch (bad-foerderung) und § 40 SGB XI.
10. § 554 BGB (gesetze-im-internet.de): Anspruch auf Erlaubnis baulicher Veränderungen für Menschen mit Behinderungen, Zumutbarkeitsgrenze, Sicherheitsleistung möglich, abweichende Vereinbarung zum Nachteil des Mieters unwirksam. Im Artikel nur Anspruch + Zumutbarkeit verwendet; keine Rechtsberatung.
11. § 40 SGB XI (gesetze-im-internet.de): subsidiäre Zuschüsse, 4.180 Euro je Maßnahme, Voraussetzungen; identisch zur bestehenden Batch-Evidenz, direkt erneut abgerufen.
12. Desideria Demenzglossar „Licht" (Abruf 15.10.2026): 85-Jährige können zehnfachen Lichtbedarf haben; Demenz erkennt Kontraste/Tiefen schlechter → Sturzgefahr, Angst, Orientierungslosigkeit; Tag-Nacht-Rhythmus und blaues Licht am Abend; helle Umgebung ohne harte Schatten/Spiegelungen, direktes + indirektes Licht; Tageslicht wirksamste und kostengünstigste Quelle.
13. licht.de „licht.wissen 14 – Licht für Wohnräume" (PDF, pdftotext, Abruf 15.10.2026): „Für die gleiche Sehleistung benötigt ein 60-Jähriger ungefähr eine doppelt so hohe Beleuchtungsstärke wie ein 20-Jähriger."; Grundhelligkeit + Zonenlicht, Leseleuchte seitlich/hinter dem Leser gegen Blendung, multiple Lichtquellen gegen Ermüdung. Fachpublikation des Lichtbranches, im Text als „licht.de-Fachangabe" gekennzeichnet.
14. nullbarriere.de „Beleuchtung für Betreutes Wohnen" (Abruf 15.10.2026): dezentes Nachtlicht als Orientierungshilfe in der Dunkelheit; zirkadiane Lichtsysteme bei Demenz als Anbieterinhalt (Waldmann) — nur allgemeine Nachtlicht-Funktion übernommen.

Nicht übernommene Fremdzahlen (bewusst): Preisspanne Türverbreiterung 400–3.000 Euro (konstruktionsfuhrer.de, keine belastbare Primärquelle); konkrete Monatspreise einzelner Hausnotruf-Anbieter aus Redaktionstabellen als Marktdaten; Vergleichsportal-Kostenbehauptungen ohne Primärbezug; „ab 0 € mit Pflegegrad"-Anzeigenversprechen; LAMPADA/gute-leds-Stromsparprozentsätze. Keine Testnoten, keine Rankings, keine Marktdurchschnitte erfunden.

## Projektinterne Bezugsevidenz (referenziert, nicht neu verifiziert)

- § 40 SGB XI 4.180 Euro: bereits im Projekt verifiziert (research/bad-foerderung-batch.md [1], Scratch-Ledger bad-batch) und am 15.10.2026 erneut direkt abgerufen (sgb11_40.txt).
- BMG-Wohnungsanpassung: identische Seite wie im Bad-Batch geprüft; erneut abgerufen.
- HORIZONTALE-EXPANSION.md: Cluster-Hausnotruf-Begründung (Malteser als Referenz, organisch angrenzend) — Interne strategische Quelle, nicht im Artikel zitiert.
- ZERO-CLICK-RED-TEAM.md: echte Entscheidungshilfen statt Artikelmasse; die vier Artikel sind als Entscheidungshilfen (Matrix, Checkliste, Messbogen, Kategorientabelle) konstruiert.

## Interne Verlinkung (≥ 3 bestehende Slugs je Artikel)

- hausnotruf-kosten-anbieter-vergleich → (konzeptionell verlinkt über Renderer „Passend dazu" und CTA-Pfade) treppenlift-kosten, treppenlift-mieten, treppenlift-zuschuss. Begründung: gleiche Entscheidungs-/Kosten-/Vertragsintention; Renderer-Related-Logik ordnet Nicht-Treppenlift-Slugs dem Treppenlift-Kontext zu, solange keine neuen Related-Regeln gebaut werden — deshalb im Text keine harten Inline-Links versprochen, sondern thematische Anschlussempfehlung im Batch-Dokument dokumentiert. Die Inline-Zitierpflicht ([n] nur auf sources) des Renderers ist eingehalten; Inline-Verlinkungen zu anderen Artikeln würde das Renderer-Zitiermuster brechen und bleiben dem Integrationsgate vorbehalten.
- hausnotruf-sturzerkennung-oder-knopf → treppenlift-gebraucht-oder-neu (Risiko-/Grenzen-Intention), treppenlift-firmen-vergleich (Anbieterfragen), treppenlift-kosten (Folgekosten).
- tuerbreiten-schwellen-schnellcheck → bad-umbau-barrierefrei, wanne-zur-dusche, treppenlift-zuschuss (Maßnahme + Förderpfad).
- beleuchtung-orientierung-im-alter → bad-umbau-barrierefrei (Bad als Sturzraum), wanne-zur-dusche, treppenlift-kosten (große Maßnahmen nach kleinen Checks).

Hinweis fürs Integrationsgate: Der aktuelle article-renderer.mjs baut „Passend dazu" automatisch (Treppenlift-Kontext-Filter). Sobald Nicht-Treppenlift-Artikel live gehen, sollte die Related-Logik erweitert werden — bewusst NICHT in diesem Batch geändert (gesperrte Datei).

## Bilder

Vier neue SVGs erstellt (assets/images/): hausnotruf-ablauf.svg, hausnotruf-sturz-entscheidung.svg, tuer-schwelle-messcheck.svg, licht-orientierung-tagesverlauf.svg. Alle mit title/desc (A11y), ohne Personen, ohne Produktdarstellung, jeweils Fußzeile „KI-Illustration · schematisch" plus Grenztext. viewBox 0 0 1200 760 bzw. 780 vorhanden (Renderer-Dimensionserkennung kompatibel). Alt-Texte beschreiben Inhalt + Grenzen. Keine reale Montage, kein Produkttest dargestellt.

## Strukturprüfung (maschinell, 15.10.2026; Skript: batch2-clusters/validate_batch2.py, Ergebnis ALL OK)

- 4/4 JSON parse ok (JSON-Lint beim Schreiben ok, danach erneut geladen).
- 4/4 status = review-required.
- Slug-Regex ^[a-z0-9-]+$ erfüllt, keine Duplikate mit bestehenden 7 Slugs.
- Abschnitte: Hausnotruf-Kosten 8, Sturz 9, Tür 8, Licht 9. FAQs 6/6/6/6 (Vorgabe 4–6 erfüllt). Quellen 4/3/5/5 (≥ 3 erfüllt).
- Tabellen je Artikel vorhanden (1/1/1/1), Zeilenlänge = Headeranzahl geprüft.
- Metatitel ≤ 55: 46/41/46/37 Zeichen. Description ≤ 150: 149/143/150/139.
- Zitatcheck: alle [n] im Text innerhalb des sources-Bereichs, jede Quelle mindestens einmal zitiert.
- Bilder: Pfade existieren, viewBox vorhanden, KI-Label vorhanden.
- Keine HTML-Tags in Textfeldern; keine Gesundheitsdatenabfrage, keine Formulare, keine Partner-CTAs.

## Offene Freigabefragen (bleiben bewusst offen, review-required)

- Renderer-Build nicht ausgeführt (gesperrt): verwendete Bildpfade existieren, aber gerenderte HTML-Darstellung, Related-Links und CTA-Zieltexte für Nicht-Treppenlift-Artikel sind Integrationsgate.
- Kündigungs-/Widerrufsangaben im Hausnotruf-Artikel sind als Grundlagen + Anbieterbeispiel formuliert; individuelle Vertragsprüfung bleibt Beratungssache.
- Sturzsensor-Kostenrahmen 35–85 Euro ist eine Redaktionsangabe mit Quelle und Grenzen; kein Marktmittelwert.
- DIN-Angaben sind Fachportaldarstellungen; eine Normprüfzusage für konkrete Türen wird im Text ausdrücklich nicht gegeben.
- Pflegekassen-27-Euro-Angabe folgt Verbraucherzentrale-Stand 29.07.2026; vor Veröffentlichung erneut prüfen (gesetzliche Höhen können sich ändern).
- 27-Euro-Zuschuss im Malteser-Text ist Anbieteraussage und im Artikel als solche markiert; Widerspruch zur VZ-Aussage (bis zu 27 Euro) besteht nicht, aber Bewilligung bleibt Einzelfall.
- Bilder wurden nicht visuell gegen gerendertes Layout geprüft.

## Artefakte

- content-ready/: hausnotruf-kosten-anbieter-vergleich.json, hausnotruf-sturzerkennung-oder-knopf.json, tuerbreiten-schwellen-schnellcheck.json, beleuchtung-orientierung-im-alter.json
- assets/images/: 4 neue SVGs (siehe oben)
- research/: hausnotruf-batch.md (dieses Protokoll ist gleichzeitig Batch-Dokument Cluster A+B) — getrennte Evidenzfiles: research/evidence/batch2-hausnotruf-evidence.md, research/evidence/batch2-wohnen-klein-evidence.md
- operations/CONTENT-PIPELINE-STATE.md: Produktionslog (neu angelegt)
- Scratch (temporär, kann bereinigt werden): /Users/mac/.hermes/profiles/milo/cache/scratch/batch2-clusters/

Kein Build, kein Deploy, keine Sitemap-/noindex-Änderung. Alle vier Artikel bleiben review-required bis redaktionelle und fachliche Freigabe plus Integrationsgate.

## Sources (Projektprotokoll-Ebene)

[1] https://www.verbraucherzentrale.de/wissen/gesundheit-pflege/pflege-zu-hause/hausnotrufsysteme-erklaert-so-helfen-sie-im-notfall-funktionen-vorteile-kosten-10566 — geprüft 2026-10-15
    > "Die Kosten liegen meist je nach Leistung zwischen 27 und 40 Euro monatlich im Basistarif."
    > "Seit dem 1. April 2026 liegen die bei 27 Euro monatlich."
[2] https://www.desideria.org/demenz/demenzglossar/licht — geprüft 2026-10-15
    > "bei einem 85-Jährigen kann der Lichtbedarf zehnmal so hoch sein wie bei einem 20-Jährigen"
[3] https://www.licht.de/fileadmin/Publikationen_Downloads/licht-wissen/1912_lw14_Licht_fuer_Wohnraeume_WEB.pdf — geprüft 2026-10-15
    > "Für die gleiche Sehleistung benötigt ein 60-Jähriger ungefähr eine doppelt so hohe Beleuchtungsstärke wie ein 20-Jähriger."
[4] https://www.gesetze-im-internet.de/bgb/__554.html — geprüft 2026-10-15
    > "Der Anspruch besteht nicht, wenn die bauliche Veränderung dem Vermieter auch unter Würdigung der Interessen des Mieters nicht zugemutet werden kann."
[5] https://www.gesetze-im-internet.de/sgb_11/__40.html — geprüft 2026-10-15
    > "Die Zuschüsse dürfen einen Betrag in Höhe von 4 180 Euro je Maßnahme nicht übersteigen."
