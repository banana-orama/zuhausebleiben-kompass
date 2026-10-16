# Batch 3: Cluster C „Pflegegrad & Anträge" und Cluster D „Rollatoren & Alltagshilfen" — Rechercheprotokoll

Prüfdatum: 16. Oktober 2026 (Systemdatum CEST). Auftrag: vier vollständige content-ready-Ratgeber in zwei NEUEN Clustern plus Batch-Dokument und Evidenzdatei; Status review-required. Kein Build, kein Deploy, kein Commit, keine Änderung an article-renderer.mjs, generate.mjs, design.css, cta.css, Tests oder bestehenden Ratgebern.

## Clusterwahl: Suchnachfrage-Hypothese und Abgrenzung

Beide Cluster wurden gegen die bestehenden 12 Artikel (7 Treppenlift/Bad aus Batch 1, 4 aus Batch 2: hausnotruf-kosten-anbieter-vergleich, hausnotruf-sturzerkennung-oder-knopf, tuerbreiten-schwellen-schnellcheck, beleuchtung-orientierung-im-alter, plus treppenlift-mietwohnung) abgegrenzt; kein Thema doppelt bedient.

### Cluster C „Pflegegrad & Anträge"

Suchnachfrage-Hypothese (qualitativ, aus SERP-Struktur am 16.10.2026, keine Suchvolumendaten): Die Abfrage „Pflegegrad beantragen Ablauf Fristen" lieferte eine dichte Liste dedizierter Ratgeber- und Beratungsdomains (deutscherpflegebeistand, renten.net, g-adv, bundesverbraucherhilfe, helping-home, pflegehilfe-senioren, pflegekosten-berechnen, mein-behoerdenhelfer) plus Bing-Ads von Antragsservices (deinepflege.de, pflegehilfe.org, salusmax) — das klassische Muster einer transaktionalen, beratungsnahen Nachfrage, bei der Vermittler und Antragsservices rangieren. Für „Verhinderungspflege Tagespflege" dominieren Vergleichsportale (medivital, aldor.ai, pflegekompass, meinpflegefinder, lukas-pflegeberatung, sozialrat, deutschland-rechner). Der nötige Nutzen ist kein weiterer Antragsservice, sondern eine seriöse Verfahrens-Orientierung: Ablauf und Fristen aus Primärtexten (SGB XI, SGG) und BMG statt aus Portal-Kopien, realistische Erwartung ohne Erfolgsversprechen, klare Abgrenzung zur Versicherungsberatung (Betreiber arbeitet bei AXA — deshalb bewusst keine Versicherungsnennung, keine Tarifthemen, keine „lohnt sich"-Bewertungen; siehe Transparenzabschnitt des Artikels). Die zwei Seiten decken zwei getrennte Suchintentionen: Verfahren/Fristen/Rechte (C1) versus Leistungsarten/Budgets/Entscheidung (C2). Keine Kanibalisierung: kein bestehender Artikel behandelt Pflegegrad oder Pfleidleistungen.

### Cluster D „Rollatoren & Alltagshilfen"

Suchnachfrage-Hypothese: „Rollator richtig einstellen" zeigt Fachhandel- und Shop-Magazine (sanitaetshaus.net, rollatoren-ratgeber.de mit Affiliate, lettermann SSL-gestört, basenio, rollator-freunde) und Pflegeportale (pflege-einstieg mit Affiliate-Hinweis) — fragmentiert zwischen Verkauf, DIY-Anleitung und Pflegeberatung; ein entscheidungsorientierter Ratgeber ohne Produkt Rankings füllt die Lücke zwischen Shop-Content und Kassentexten. „Pflegehilfsmittel Pflegekasse übernehmen" zeigt GKV/BMG-Offizialtexte, Verbraucherzentrale und Shop-Content mit „kostenlose Pflegehilfsmittel"-Versprechen (pflege.de-Angebote, pflegeheim-vergleichen) — genau dort setzt der Artikel an: Struktur, Anspruchslogik und Grenzen statt „gratis"-Framing. Anschluss an bestehende Cluster: bad-umbau/tuerbreiten behandeln bauliche Maßnahmen, hausnotruf das Notrufsystem; die neuen Seiten bedienen die mobilen Alltagshilfen und den Kassenantragspfad — Upsell-Pfad statt Kanibalisierung. HORIZONTALE-EXPANSION.md führt Alltagshilfen/Gehhilfen als Position 4 mit sanitaets-online.de-Partnerprogramm (Kaufprovision, nicht geprüft aktiv) — im Artikel bewusst KEIN Shop-, kein Partner- und kein Produktnaming; Vermarktung bleibt Gate-Entscheidung.

## SERP-/Konkurrenzcheck je Artikel (Websuche 16.10.2026, keine Rangfolge, keine Volumen)

1. pflegegrad-antrag-ablauf-fristen — Query „Pflegegrad beantragen Ablauf Fristen MDK Begutachtung Widerspruch". Treffer: deutscherpflegebeistand, renten.net, g-adv, bundesverbraucherhilfe, helping-home, pflegehilfe-senioren, mein-behoerdenhelfer; Ads von Antragsservices. Suchintention: Verfahrensschritte, Fristen, Vorbereitung, Ablehnungsreaktion. Eigene Verbesserung: komplette Fristentabelle aus Gesetzestext+BMG (inkl. 70-€-Verzugspauschale als BMG-Angabe), 6-Bereiche-Vorbereitung statt „Tips&Tricks"-Framing, explizite Drittanbieter-Warnung der Verbraucherzentrale, kein Erfolgsquoten-Versprechen („jeder dritte Widerspruch"-Gerücht bewusst nicht übernommen).
2. verhinderungspflege-tagespflege-ueberblick — Query „Verhinderungspflege Tagespflege § 39 § 41 SGB XI Betrag". Treffer: medivital, aldor.ai, pflegekompass, meinpflegefinder, lukas-pflegeberatung, sozialrat („3.539 €"), deutschland-rechner. Suchintention: Beträge, Anspruch, Antrag, Unterschiede. Eigene Verbesserung: Beträge ausschließlich aus § 39/§ 41/§ 42a SGB XI (live abgerufen), Erstattungslogik nahe-Angehörige vs. Dienst als Tabelle, 7-Zeilen-Entscheidungsmatrix, Reform-Ausblick (PNOG 2027) nur als gekennzeichneter Referentenentwurf-Stand mit Unsicherheitsmarkierung.
3. rollator-auswahl-passform-kosten — Query „Rollator kaufen Größe einstellen Bremsen Trommelbremse Feststellbremse". Treffer: sanitaetshaus.net, rollatoren-ratgeber.de, pflege-einstieg, basenio, rollator-freunde, lettermann. Suchintention: Passform, Bremstypen, Kosten, Kaufkriterien. Eigene Verbesserung: Passform als Messanleitung (Handgelenksfalten-Methode) statt Körpergrößen-Tabellen, Hand-/Feststellbremse als Funktionspaar mit Prüftest, Kassen-Logik sauber getrennt (Krankenkasse § 61 SGB V vs. Pflegekasse § 40 SGB XI), 10-Punkte-Einkaufscheck, kein Produkt- und Preis-Ranking (Shop-Preise aus SERP bewusst NICHT übernommen).
4. hilfsmittel-pflegekasse-uebernahme — Query „Pflegehilfsmittel Pflegekasse § 33 SGB XI 10 Prozent 40 Euro Hilfsmittelverzeichnis". Treffer: seniormegastore, GKV-Spitzenverband, pflegekompass, deutscherpflegebeistand-Merkblatt-PDF, pflegeheim-vergleichen („40 Euro"-Altstand). Suchintention: Was wird übernommen, Eigenanteil, Antrag. Eigene Verbesserung: KORREKTUR des verbreiteten Altstands — § 40 Abs. 2 SGB XI nennt aktuell 42 €/Monat (live bestätigt via gesetze-im-internet UND GKV-Spitzenverband), Genehmigungsfiktion der Verbraucherzentrale als Praxishinweis, Abgrenzungsdreieck Pflegekasse/Krankenkasse/Wohnumfeld, 10-Punkte-Antragscheckliste.

## Wichtigster Korrektur-Fund des Batches

Viele Portale nennen noch 40 €/Monat für Pflegehilfsmittel zum Verbrauch. Der am 16.10.2026 live abgerufene Gesetzestext § 40 Abs. 2 SGB XI sagt: „Die Aufwendungen der Pflegekassen für zum Verbrauch bestimmte Pflegehilfsmittel dürfen monatlich den Betrag von 42 Euro nicht übersteigen." Zweitbeleg GKV-Spitzenverband („ab dem 01.01.2025 ... 42 Euro", § 40 Abs. 2 SGB XI). Beide Artikel D1/D2 verwenden ausschließlich 42 €; BMG-Ratgeber bestätigt zusätzlich „bis zu 42 Euro pro Monat".

## Primärquellen: Live-Abrufe, Belege, Grenzen

Methode: urllib-Liveabrufe am 16.10.2026 (CEST) mit Browser-UA; rohe HTML- und bereinigte TXT-Dateien unter /Users/mac/.hermes/profiles/milo/cache/scratch/batch3-clusters/. Vollständige wörtliche Belege: research/evidence/batch3-pflegegrad-alltag-evidence.md. web_extract wurde nicht verwendet; alle Zitate stammen aus direkt geladenen Originalseiten.

1. gesetze-im-internet.de: § 33, § 14, § 15, § 18, § 30, § 34, § 37, § 39, § 40, § 41, § 42a SGB XI; § 84, § 87 SGG; § 33, § 61 SGB V — allesamt live abgerufen, Kernpassagen wörtlich in der Evidenzdatei. Verwendet für: Anspruchsstruktur, Pflegegrad-Einteilung und Modulgewichtung, Fristen (3 Arbeitstage, 20 Arbeitstage), Verhinderungspflege (8 Wochen, Jahresbetrag, Angehörigenlogik), Tagespflegebeträge, Pflegegeldbeträge, Hilfsmittelanspruch inkl. 42 €/10 %/25 €, Widerspruchs- und Klagefristen (1 Monat), Krankenkassen-Zuzahlung (10 %, min. 5 €, max. 10 €).
2. BMG-Ratgeber: „Antragsverfahren" (Stand 14.09.2026), „Pflegehilfsmittel", „Teilstationäre Tages- oder Nachtpflege" (Stand 15.09.2026), „Weitere Leistungen und Angebote zur Unterstützung im Alltag" — live abgerufen. Kernangaben: 25 Arbeitstage Bescheidfrist, verkürzte Fristen (1 Woche Klinik/Reha/Hospiz/Palliativ; 2 Wochen Pflegezeit-Freistellung; 10 Arbeitstage Kurzzeitpflege), 70-€-Verzugspauschale je Woche, Pflegeberatung binnen 2 Wochen, 3-/5-Wochen-Hilfsmittelfristen, Tagespflegetabelle 721/1.357/1.685/2.085 €, Entlastungsbetrag 131 €/Monat, Gehhilfen/Rollstühle über Krankenkassen.
3. GKV-Spitzenverband: „Pflegehilfsmittel" (Stand 17.12.2024) und „Hilfsmittelverzeichnis" — live abgerufen. 42-€-Bestätigung, Produktgruppen-Logik, Verträge zum Verbrauch nach § 78 SGB XI.
4. gesund.bund.de (BZgA): „Widerspruch und Klage gegen einen Bescheid der Pflegekasse" — live abgerufen. 1-Monats-Frist, 1-Jahr-Frist ohne Belehrung, Schriftform, Sozialgerichtsweg, Beratungsstellen.
5. Verbraucherzentrale (5 Artikel, live): Pflegegrad beantragen (Stand 10.12.2025), Pflegehilfsmittel, Hilfsmittel beantragen, Hilfsmittel kaufen Internet, Mobilitätshilfen, plus Hausnotruf-Artikel zum Crosslink-Abgleich (27-€-Regel erneut live bestätigt).
6. pflege.de: Pflegegrad beantragen und Verhinderungspflege — als gekennzeichnete Redaktionsquelle für Prozessdetails (Eilantrag, eingetragene Pflegeperson, Reformstand PNOG 30.09.2026); kommerzielle Angebote der Seite bewusst nicht übernommen und im Artikel nicht empfohlen.
7. Rollator-Fachquellen (gekennzeichnet): pflege-einstieg.de (Affiliate-Hinweis auf der Seite), sanitaetshaus.net (Firmenweb-Fachmagazin), rollatoren-ratgeber.de (Shopanteil) — nur funktionale Passform-/Bremsen-Angaben, keine Produktnamen, keine Preise.

Nicht übernommene Fremdangaben (bewusst): „ein Drittel der Widersprüche erfolgreich" (Erfahrungswert ohne Primärquelle); Shop-Preise für Rollatoren aus Affiliate-SERP (69,99 €, 76,49 €); „40 Euro"-Altstand der Verbrauchsgrenze; PNOG-Beträge aus Referentenentwurf; pauschale „kostenlos mit Pflegegrad"-Versprechen von Shop-Portalen; VZ-Tippfehler („nu") nicht wörtlich, nur Sachaussage. Keine erfundenen Preise, Quoten, Testnoten oder Marktdurchschnitte.

## AXA-/Versicherungsabgrenzung (Cluster C)

Der Betreiber ist hauptberuflich in der Versicherungswirtschaft (AXA) tätig. Konsequenz in diesem Batch, konsistent mit HORIZONTALE-EXPANSION.md („Keine AXA-Marke, Kundendaten oder Arbeitskontakte verwenden; Versicherungsvermittlung bleibt außerhalb des Vorhabens"):
- Keine Empfehlung von Versicherern, Tarifen oder Pflegezusatzversicherungen; das Thema „Pflegezusatzversicherung" kommt nicht vor.
- Pflegegrad-Antrag wird ausschließlich als Sozialleistungsverfahren der gesetzlichen Pflegeversicherung dargestellt; private Pflegepflichtversicherung nur als zuständliche Auskunft (Medicproof), ohne Bewertung.
- Transparenzabschnitt C1 nennt die berufliche Außen Tätigkeit ausdrücklich als Grund für Verzicht auf Produkt-/Anbieterempfehlungen.
- Keine Antragsservice-, Widerspruchsservice- oder Lead-Elemente im Artikel (Render-CTAs treppenlift-spezifisch, betroffen nicht).

## Interne Verlinkung (je Artikel ≥ 3 bestehende Slugs, konzeptionell)

Gleiche Konvention wie Batch 2: Der article-renderer baut „Passend dazu" automatisch (aktueller Filter ordnet Nicht-Treppenlift-Slugs dem Treppenlift-Kontext zu); Inline-Links zu anderen Artikeln würden das Zitiermuster brechen. Deshalb dokumentiert dieses Protokoll die intendierten Verbindungen fürs Integrationsgate:
- pflegegrad-antrag-ablauf-fristen → treppenlift-zuschuss (4.180 € setzt Pflegegrad voraus), treppenlift-kosten (Planung nach Bescheid), hausnotruf-kosten-anbieter-vergleich (Pflegegrad als Voraussetzung der 27-€-Übernahme).
- verhinderungspflege-tagespflege-ueberblick → pflegegrad-antrag-ablauf-fristen (neu, gleicher Batch), hausnotruf-kosten-anbieter-vergleich (Entlastung durch Technik), treppenlift-mietwohnung (Pflegegrad als Voraussetzung des Wohnraumpfads).
- rollator-auswahl-passform-kosten → hilfsmittel-pflegekasse-uebernahme (Kassenpfad), bad-umbau-barrierefrei (Sturzraum Bad), tuerbreiten-schwellen-schnellcheck (Breiten/Schwellen für Rollatornutzung).
- hilfsmittel-pflegekasse-uebernahme → hausnotruf-kosten-anbieter-vergleich (27-€-Regel im Artikel verlinkt-logisch referenziert), rollator-auswahl-passform-kosten (Krankenkassen-Zweig), bad-umbau-barrierefrei (Wohnumfeld vs. Hilfsmittel-Abgrenzung im Text).
Gate-Hinweis: Related-Logik des Renderers sollte vor Freigabe der Nicht-Treppenlift-Batches auf Cluster-Map erweitert werden (offen seit Batch 2, gesperrte Datei).

## Bilder

Vier neue SVGs (assets/images/), alle viewBox 0 0 1200 760 (Renderer-Dimensionserkennung kompatibel), title/desc (A11y), Fußzeile KI-Illustration, keine Personen, keine Produkte:
- pflegegrad-antrag-ablauf.svg — Zeitleiste Antrag→MD→Beratung→Begutachtung→Bescheid + Positiv/Negativ-Verzweigung + verkürzte Fristen.
- verhinderung-tagespflege-matrix.svg — Zwei-Spalten-Vergleich mit Budgets und Gemeinsamer Grundlage.
- rollator-passform-bremsen.svg — Schemazeichnung mit 3 Prüfboxen (Griffhöhe, Rasterstufen, Bremsen).
- hilfsmittel-antrag-weg.svg — 4-Schritt-Flow + zwei Eigenanteil-Boxen + Abgrenzungsbox.
Validierung: XML-parse OK (ElementTree), viewBox-Regex für Renderer OK, KI-Label OK, Textlaufweiten mit kalibriertem Faktor 0,60 gegen 1180-px-Grenze geprüft (nach zwei Korrekturrunden; qlmanage-Renderings visuell geprüft: keine Boxüberläufe, keine Textkollisionen; rechte Randnähe der Endanker-Linien ist text-anchor=end, kein Risiko).

## Strukturprüfung (maschinell, 16.10.2026; Skript in Scratch, Ergebnis ALL VALID)

- 4/4 JSON parse ok (Linter OK beim Schreiben, danach erneut geladen).
- 4/4 status = review-required; 12 bestehende content-ready-Dateien unangetastet.
- Slug-Regex erfüllt, keine Duplikate mit bestehenden 12 Slugs.
- Abschnitte: C1=8, C2=7, D1=7, D2=7. FAQs 6/6/6/6 (Vorgabe 4–6). Quellen 10/8/10/10 (≥ 3).
- Beschreibungen ≤ 150: 138/143/145/144. Tabellen je Artikel vorhanden, Zeilenbreite = Headeranzahl.
- Zitatcheck: alle [n] im Quellbereich, jede Quelle mindestens einmal zitiert, keine doppelten URLs je Artikel.
- Bilder: Pfade existieren, XML valide, viewBox vorhanden, KI-Label vorhanden.
- Keine Formulare, keine Gesundheitsdatenabfrage, keine Partner-CTAs, keine Fear-Selling-Phrasen.

## Offene Freigabefragen (bleiben bewusst offen, review-required)

- Renderer-Build nicht ausgeführt (gesperrt): Related-Logik und CTA-Zieltexte für Nicht-Treppenlift-Artikel sind Integrationsgate (siehe Batch-2-Hinweis).
- Slug-Kollision: generate.mjs rendert eine dünne Legacy-Seite pflegegrad-beantragen (data/content.json, noindex im Preview-Build). Der neue Artikel heißt bewusst pflegegrad-antrag-ablauf-fristen — keine Kollision. Beim Launch-Gate klären, ob die Legacy-Seite entfernt/weitergeleitet wird (gesperrte Dateien).
- Beträge (721–2.085 €, 3.539 €, Pflegegeldtabelle, 42 €, 131 €, 70 €, 25 €) sind dynamisierungsanfällig (§ 30 SGB XI, nächste Stufe 1.1.2028); vor Veröffentlichung erneut prüfen. 27-€-Hausnotruf-Regel: VZ-Stand 29.07.2026, am 16.10.2026 erneut live bestätigt.
- Reformrisiko: PNOG-Referentenentwurf (Verhinderungspflege ab 2027) ist im Artikel C2 nur als gekennzeichneter, unsicherer Ausblick.
- BMG-70-€-Pauschale und 25-Arbeitstage-Frist sind Ministerialangaben (kein direkter § im Artikeltext zitiert, da in § 18a SGB XI liegend — nicht einzeln abgerufen); falls das Gate den Paragraftext will: § 18a SGB XI nachziehen.
- Bilder wurden gegen qlmanage-Renderings visuell geprüft; endgültige Layoutprüfung im gerenderten Artikel bleibt Gate.
- Rechtliche Grenzen: Artikel C1/D2 nennen Widerspruch/Klage als Fristen-Fakten, keine Rechtsberatung; Formulierung „ohne Rechts- und Versicherungsberatung" gesetzt.

## Artefakte

- content-ready/: pflegegrad-antrag-ablauf-fristen.json, verhinderungspflege-tagespflege-ueberblick.json, rollator-auswahl-passform-kosten.json, hilfsmittel-pflegekasse-uebernahme.json
- assets/images/: 4 neue SVGs (siehe oben)
- research/: batch3-pflegegrad-alltag-batch.md (dieses Protokoll)
- research/evidence/: batch3-pflegegrad-alltag-evidence.md (wörtliche Belege G1–G13, O1–O7, V1–V6, P1–P5 + Nicht-übernommenes)
- Scratch (temporär): /Users/mac/.hermes/profiles/milo/cache/scratch/batch3-clusters/ (Rohabrufe)

Kein Build, kein Deploy, keine Sitemap-Änderung, keine Änderung an gesperrten Dateien. Alle vier Artikel bleiben review-required bis redaktionelle und fachliche Freigabe plus Integrationsgate.

## Sources (Projektprotokoll-Ebene, Auswahl der tragenden Belege)

[1] https://www.gesetze-im-internet.de/sgb_11/__40.html — geprüft 2026-10-16
    > "Die Aufwendungen der Pflegekassen für zum Verbrauch bestimmte Pflegehilfsmittel dürfen monatlich den Betrag von 42 Euro nicht übersteigen."
    > "Versicherte, die das 18. Lebensjahr vollendet haben, haben zu den Kosten der Pflegehilfsmittel mit Ausnahme der Pflegehilfsmittel nach Absatz 2 eine Zuzahlung von zehn vom Hundert, höchstens jedoch 25 Euro je Pflegehilfsmittel an die abgebende Stelle zu leisten."
[2] https://www.gesetze-im-internet.de/sgb_11/__39.html — geprüft 2026-10-16
    > "übernimmt die Pflegekasse die nachgewiesenen Kosten einer notwendigen Ersatzpflege für den Pflegebedürftigen für längstens acht Wochen je Kalenderjahr"
[3] https://www.gesetze-im-internet.de/sgb_11/__41.html — geprüft 2026-10-16
    > "für Pflegebedürftige des Pflegegrades 2 einen Gesamtwert bis zu 721 Euro, ... für Pflegebedürftige des Pflegegrades 5 einen Gesamtwert bis zu 2 085 Euro."
[4] https://www.gesetze-im-internet.de/sgb_11/__42a.html — geprüft 2026-10-16
    > "in Höhe eines Gesamtleistungsbetrages von insgesamt bis zu 3 539 Euro je Kalenderjahr (Gemeinsamer Jahresbetrag)"
[5] https://www.gesetze-im-internet.de/sgg/__84.html — geprüft 2026-10-16
    > "Der Widerspruch ist binnen eines Monats, nachdem der Verwaltungsakt dem Beschwerten bekanntgegeben worden ist, ... einzureichen"
[6] https://www.bundesgesundheitsministerium.de/pflegegrade — geprüft 2026-10-16 (Stand 14.09.2026)
    > "Die gesetzlich vorgegebene Bearbeitungsfrist für Anträge zur Feststellung der Pflegebedürftigkeit beträgt 25 Arbeitstage."
    > "... für jede begonnene Woche der Fristüberschreitung 70 Euro ... an die Antragstellerin beziehungsweise den Antragsteller zu zahlen."
[7] https://www.bundesgesundheitsministerium.de/pflege-zu-hause/pflegehilfsmittel — geprüft 2026-10-16
    > "Diese hat über den Leistungsantrag innerhalb von drei Wochen nach Antragseingang zu entscheiden. Die Frist verlängert sich auf fünf Wochen, wenn für die Leistungsentscheidung eine Pflegefachperson oder der Medizinische Dienst beteiligt werden."
[8] https://www.verbraucherzentrale.de/wissen/gesundheit-pflege/pflege-im-heim/pflegehilfsmittel-wer-bekommt-sie-wer-muss-zahlen-62315 — geprüft 2026-10-16
    > "Bekommen Sie keine Mitteilung mit Begründung, gilt die Leistung nach Ablauf der Frist als genehmigt."
[9] https://www.gkv-spitzenverband.de/service/hmv/phm/p_himi.jsp — geprüft 2026-10-16
    > "Die Aufwendungen der Pflegekassen für zum Verbrauch bestimmte Pflegehilfsmittel dürfen ab dem 01.01.2025 monatlich den Betrag von 42 Euro nicht übersteigen (§ 40 Abs. 2 SGB XI)."
[10] https://www.gesetze-im-internet.de/sgb_11/__15.html — geprüft 2026-10-16
    > "ab 12,5 bis unter 27 Gesamtpunkten in den Pflegegrad 1 ... ab 90 bis 100 Gesamtpunkten in den Pflegegrad 5"
