# Recherche und Freigabegrenzen: drei Treppenlift-Ratgeber

Geprüft am 2026-10-14 (Systemdatum: CEST). Auftrag: ausschließlich drei JSON-Artikel und dieses Rechercheprotokoll; keine Veröffentlichung, keine Änderung an Renderer, Design, Daten, Cron oder Git.

## Ergebnis und Arbeitsteilung

- content-ready/treppenlift-kosten.json: vollständiger Kostenratgeber mit konkreten, begrenzten TK-Hersteller-Ab-Preisen, Angebotspositionen, toolgeprüfter eigener Modellrechnung und druckbarer Fragenliste.
- content-ready/treppenlift-firmen-vergleich.json: vollständige sachliche Einordnung von Lifta, HIRO LIFT und TK Home Solutions; kein Testsieger, keine Sterne, kein objektiv behauptetes Qualitätsranking. Ausfüllbare Matrix für Eignung, Vertrag, Kosten und Service.
- content-ready/treppenlift-gebraucht-oder-neu.json: vollständige Entscheidungshilfe zu Gerät/Schiene, Aufbereitung, Privatkauf, Ersatzteilen und Service; Komponentencheck, Gesamtkostentabelle und Entscheidungsmatrix.
- Alle drei Dateien: status review-required. Zielgruppe ältere Menschen und Angehörige; Sie-Ansprache. Betreiber Tobias Batke, KI-Unterstützung und fehlende physische Tests im Text ausdrücklich benannt. Keine Versicherungsvermittlung und keine Partnerzusage.

## Bestehender Entwurf und Abgrenzung der Suchintentionen

Gelesen: content-drafts/treppenlift-angebote-vergleichen.briefing.json (205 Zeilen). Das ist bereits ein ausführlicher Vergleichsentwurf, kein bloßer Titel. Seine sinnvollen Bausteine wurden weiterentwickelt: schriftliche Leistungsliste, Schienenzeichnung, Festpreisfrage, Wartungs-/Störungsdienst und druckbare Fragen. Es wurde kein zweiter Artikel mit dem Slug treppenlift-angebote-vergleichen erzeugt. Der vorhandene Entwurf blieb unverändert.

Nicht übernommen: die Addition zweier verschiedener Anlagen zu einem für Leser wenig hilfreichen Gesamtwert; Vergleich gerade gegen kurvig als vermeintlicher Angebotsvergleich; pauschale 20-Prozent-Regel für Kostenvoranschläge; allgemeine Widerrufsfrist ohne individuelle Vertragsprüfung; pauschale Steuerersparnis; unbelegte Sicherheits-/Ausstattungsbehauptungen und Aussagen zur derzeitigen Portalvermittlung. Die neue Rechnung nimmt dieselbe geplante Nutzung an und vergleicht Anschaffung plus fünf Wartungen. Der Firmenratgeber konzentriert sich auf Verantwortlichkeiten und Anbieterwahl. Der Kostenratgeber erklärt Beträge und Angebotsbestandteile. Der Gebrauchtratgeber prüft Komponenten und Kaufwege. Gemeinsame Checkfragen sind funktional, nicht drei Kopien derselben Suchabsicht.

## Aktuelle SERP-Prüfung vor den Texten

Recherche über web_search am 2026-10-14. Ergebnisse sind die vom Retrieval-Werkzeug zurückgegebenen Treffer, kein vollständiges personalisiertes deutsches Google-Ranking. Bing-Anzeigen kamen teilweise mit zurück. Positionsnummern und Anzeigen wurden daher nicht als objektive organische Rangfolge oder Marktanteil interpretiert. Keine Suchvolumina oder Einnahmen behauptet.

### Kosten

Query: Treppenlift Kosten Preise Einbau Wartung.

Treffer u. a. treppenlifter.me/treppenlift-preisliste.html, ts-treppenlifte.de/preise-kosten/, pflanz-homelift.de/treppenlift/treppenlift-preise-kosten und ein Handelsblatt-Advertorial. Suchintention: schnelle Preiserwartung mit Einbau und Zuschuss, anschließend Angebotsanfrage. Die Resultate enthalten Preislisten, Ab-Preise und Anbieterwerbung. Verbesserung: keine unsourced Marktspanne; konkrete Hersteller-Modellkarten nur als Ab-Preise mit Grenzen; gleiche Ausgangsplanung in zwei erfundenen Modellangeboten; Anschaffung und Folgekosten getrennt.

### Firmenvergleich

Query: Treppenlift Firmen Vergleich Anbieter Lifta HIRO TK Home Solutions.

Suchtool lieferte mehrere Anzeigen und die Treffer https://www.treppenliftwissen.de/anbieter/ sowie https://www.aroundhome.de/treppenlift/anbieter/. Suchintention: Markennamen einordnen, Preise/Service vergleichen und eventuell Anfrage stellen. Snippets enthalten Test-/Vergleichs- und Vermittlungsbegriffe; sie wurden nicht als tatsächliche Tests gelesen. Verbesserung: Rollen von Hersteller, Verkäufer und Monteur trennen; nur Original-Sortimentsangaben; Service-Erreichbarkeit nicht mit Reparaturzeit verwechseln; keine erdachte Rangfolge.

### Gebraucht oder neu

Query: Treppenlift gebraucht oder neu Schiene Garantie Hersteller.

Treffer: https://www.seniorenrat.de/ratgeber/treppenlift-gebraucht/, https://ts-treppenlifte.de/service/treppenlift-garantie/, https://www.regional-treppenlift.de/glossar/gebrauchtkauf-und-garantie/, https://www.stufen-los.de/blog/treppenlift-gebraucht-vorfuehrmodell-oder-neu/ und https://www.wunschtreppenlift.de/treppenlift-gebraucht/. Suchintention: Ersparnis gegen technische und vertragliche Risiken abwägen. Ein Snippet nennt 30–50 Prozent Ersparnis; ohne gleichwertige aktuelle Komplettangebote wurde diese Zahl nicht übernommen. Verbesserung: Komponenten statt Etikett gebraucht, gebrauchte Fahreinheit von passender Schiene unterscheiden, Montagezusage vor Privatkauf und Ersatzteilfragen für konkrete Seriennummer.

Diese Wettbewerbstreffer wurden als SERP-Snippets untersucht, nicht vollständig inhaltlich verifiziert. Alle tragenden Artikelbehauptungen beruhen dagegen auf direkt abgerufenen Originalseiten unten.

## Originalquellen: Abruf, Aussagen und Grenzen

web_extract scheiterte technisch mit: „DuckDuckGo (ddgs) is a search-only backend and cannot extract URL content.“ Keine Extraktion vorgetäuscht. Die Seiten wurden danach parallel direkt mit urllib.request abgerufen. Die ursprüngliche bs4-Probe scheiterte an fehlendem Paket; stattdessen erfolgte eine stdlib-Textbereinigung der HTML-Antworten. Texte, Roh-HTML und endgültige Ziel-URLs sind im profilbezogenen Scratch-Verzeichnis gesichert. Es handelte sich um Live-HTTP-Antworten, nicht Archivkopien. Herstellerseiten enthalten teils Navigation und Template-Reste; nur zusammenhängende lesbare Sachpassagen wurden verwendet.

1. Verbraucherzentrale: direkte Verbraucherhinweise zu mehreren Angeboten, Leistungen einzeln, Schienenzeichnung, Festpreis, Wartung, Ansprechpartner, Abschlussdruck und Garantiebedingungen. Originalquelle für ihre eigenen Empfehlungen, keine Labortestquelle. Enthaltene breite Preis-/Wartungsspannen wurden absichtlich nicht als aktueller Marktmittelwert übernommen.
2. § 40 SGB XI: Absatz 4 nennt bis 4.180 Euro je Maßnahme und die Voraussetzungen. Der Artikel erklärt den Höchstbetrag nicht als persönliche Bewilligung. Die Empfehlung zur Antragstellung vor Umbau stammt aus der Verbraucherzentrale. Keine aktuelle KfW-Verfügbarkeit oder Kombinationszusage recherchiert bzw. behauptet.
3. HIRO Produktseite: HIRO 160 ECO/NEO/FLEX für innen, AIR für außen; eigene Produktion und Serviceteam als Selbstaussage. Keine Bestätigung einer regionalen Reaktionszeit, Sicherheitsüberlegenheit oder Verfügbarkeit. Die zusätzliche abgerufene NEO-Modellseite war Kontext, wird aber nicht als separate tragende Quelle benötigt.
4. Lifta Produktseite: Modelle für gerade/kurvige Treppen und außen; passgenaue Schienen; Hinweis auf Der Treppenlift als Gebrauchtpartner. Allgemeine Mindestbreiten und pauschale Machbarkeitsversprechen nicht übernommen.
5. TK Home Solutions Startseite: S100 gerade „Ab 5.300 EUR“, S200 kurvig „Ab 10.000 EUR“, S100 Outdoor „Ab 5.800 EUR“. Das sind konkrete beworbene Modell-Einstiegspreise, keine Endpreise für eine beliebige Treppe. Die kurzen Karten klären den vollständigen Umfang, Umsatzsteuer und Zusatzarbeiten nicht abschließend; Artikel verlangt schriftlichen Gesamtpreis. Kein Zuschuss davon automatisch abgezogen. Keine historischen Flow-X-Angaben übernommen: die live gelesene Startseite zeigt S100/S200.
6. HIRO Gebrauchtseite: Abruf https://hiro.de/gebrauchte-treppenlifte/ leitete auf https://hiro.de/gebrauchte-treppenlifte-jahreslifte/ weiter. Finale URL steht im JSON. Individuelle Fahrbahn, Probleme bei Kurvenschienen, Anpassungsbedarf auch gerade, Aus-/Einbau, letzte Wartung. Pauschale juristische Aussage zur Mindestgewährleistung nicht übernommen. Hinweise auf eigene Hindernistests wurden nicht als Anleitung wiedergegeben.
7. Der Treppenlift GmbH: beschreibt Aufbereitung mit Originalteilen, individuell angepasste Schienen und „bis zu 3 Jahren Garantie“. Nur als Anbieterangaben verwendet. Keine Aussage, dass jede gebrauchte Anlage drei Jahre Garantie besitzt oder auf jede Treppe passt. Keine aus Marketingzahlen abgeleiteten Installations-/Marktanteilswerte.

## Quellenkette je Artikel

In jedem Artikel sind [1], [2] usw. lokal nummeriert und entsprechen der Reihenfolge im sources-Array. Jede Quelle hat mindestens einen wörtlichen, gegen den abgerufenen Text geprüften Evidence-Beleg im eigenen Scratch-Ledger. Der JSON-Schema-Vorgabe entsprechend gibt es keine zusätzlichen ID-/HTML-Felder. Die folgenden Quellenblöcke wurden mechanisch aus den Ledgers erzeugt.

### treppenlift-kosten – eigene Nummerierung

## Sources

[1] https://www.verbraucherzentrale.de/wissen/gesundheit-pflege/pflege-zu-hause/treppenlifte-das-muessen-sie-ueber-planung-und-umsetzung-wissen-10711 — Treppenlifte: Das müssen Sie über Planung und Umsetzung wissen | Verbraucherzentrale.de Direkt zum I
    > "Vereinbaren Sie möglichst einen Festpreis für den Einbau."
[2] https://www.gesetze-im-internet.de/sgb_11/__40.html — § 40 SGB 11
    > "Die Zuschüsse dürfen einen Betrag in Höhe von 4 180 Euro je Maßnahme nicht übersteigen."
[3] https://www.tke-homesolutions.de — TK Home Solutions ✔ Ihr Treppenlift-Hersteller seit 1957 Zum Inhalt springen Jetzt kostenlosen Berat
    > "Ab 5.300 EUR"


### treppenlift-firmen-vergleich – eigene Nummerierung

## Sources

[1] https://www.verbraucherzentrale.de/wissen/gesundheit-pflege/pflege-zu-hause/treppenlifte-das-muessen-sie-ueber-planung-und-umsetzung-wissen-10711 — Treppenlifte: Das müssen Sie über Planung und Umsetzung wissen | Verbraucherzentrale.de Direkt zum I
    > "Vereinbaren Sie möglichst einen Festpreis für den Einbau."
[2] https://hiro.de/treppenlift — --> Treppenlift » Unterstützung für zu Hause | hiro Treppenlifte von HIRO LIFT: maßgefertigt, Made i
    > "ECO, NEO, FLEX (innen), AIR (außen)"
[3] https://www.lifta.de/treppenlift — Lifta Treppenlifte: Mobilität für Ihr Zuhause { this.isMainNavigationOpen = !this.isMainNavigationOp
    > "Da die Schienen passgenau für Ihre Treppe angefertigt werden, gibt es für jeden Treppenverlauf ein passendes Modell."
[4] https://www.tke-homesolutions.de — TK Home Solutions ✔ Ihr Treppenlift-Hersteller seit 1957 Zum Inhalt springen Jetzt kostenlosen Berat
    > "Ab 5.300 EUR"


### treppenlift-gebraucht-oder-neu – eigene Nummerierung

## Sources

[1] https://www.verbraucherzentrale.de/wissen/gesundheit-pflege/pflege-zu-hause/treppenlifte-das-muessen-sie-ueber-planung-und-umsetzung-wissen-10711 — Treppenlifte: Das müssen Sie über Planung und Umsetzung wissen | Verbraucherzentrale.de Direkt zum I
    > "Vereinbaren Sie möglichst einen Festpreis für den Einbau."
[2] https://hiro.de/gebrauchte-treppenlifte-jahreslifte — --> Gebrauchte Treppenlifte: Jahreslifte von HIRO LIFT Gebrauchte Treppenlifte: Jahresauszüge von HI
    > "Die Fahrbahn eines Treppenlifts ist jedoch in der Regel ein Unikat, das speziell an die jeweilige Treppe angepasst wird."
[3] https://www.der-treppenlift.de — Treppenlift gebraucht von der Nr. 1
    > "Denn bei uns werden die Schienen jeweils individuell auf Ihr Treppenhaus angepasst."


## Toolgeprüfte Modellrechnung (keine Marktdaten)

Alle Zahlen sind ausdrücklich frei gewählte Annahmen inklusive Umsatzsteuer. Es handelt sich nicht um eine fehlgeschlagene Herstellerrecherche mit erfundenen Ersatzdaten. Das tatsächliche Herstellerpreisbeispiel steht separat und ist direkt abgerufen.

- A: 5.200 + 1.600 + 900 + 300 = 8.000 Euro.
- B: 5.700 + 1.400 + 1.000 + 200 = 8.300 Euro.
- Fünf jährliche Wartungen A: 5 × 260 = 1.300 Euro; B: 5 × 180 = 900 Euro.
- Teilkosten nach fünf Wartungen A: 9.300 Euro; B: 9.200 Euro. Abstand: 100 Euro zugunsten B.
- Nur hypothetisch bewilligte 3.000 Euro: A 8.000 − 3.000 = 5.000; B 8.300 − 3.000 = 5.300 Euro verbleibende Anschaffung.
- Bewilligungssumme nicht vorausgesetzt; Reparatur, Akkuwechsel, Strom, Rückbau und Preisänderungen bewusst nicht quantifiziert. Fehlende Preise sollen als offen, nicht als null behandelt werden.

Berechnet mit Python und durch erneute Gleichheitsprüfungen im abschließenden Strukturcheck bestätigt.

## Tatsächlich ausgeführte Prüfungen

- Alle drei Dateien erfolgreich mit write_file geschrieben; verified:true und JSON-Lint status ok.
- Drei Dateien erneut als JSON geladen: erlaubte Top-Level-Felder, korrekter Slug, review-required, mindestens zwei Quellen, exakt vorgegebene Caption.
- Tabellen: jede Zeile hat genauso viele String-Zellen wie die Header; Abschnitte und FAQs als vollständige Texte vorhanden.
- Plain-Text-Check: keine HTML-Tags gefunden.
- Quellenprüfung: sämtliche numerischen Inline-IDs entsprechen genau den lokalen sources-Positionen; kein unbekannter Beleg und keine unzitierte Quelle.
- sources.py verify --evidence: alle drei Artikel exit 0, citations OK; jede zitierte Quelle mit wörtlicher Evidenz. Automatische Zitierabdeckung wird durch Checklisten, Tabellen und eigene Rechnungen künstlich niedrig ausgewiesen; keine Mindestabdeckungsquote oder vollständige automatische Sachprüfung behauptet.
- Kosten: 9 Abschnitte, 4 FAQs, 3 Quellen. Firmen: 10 Abschnitte, 5 FAQs, 4 Quellen. Gebraucht: 10 Abschnitte, 5 FAQs, 3 Quellen.
- Beide angegebenen lokalen Bildpfade existieren beim Prüflauf. Bildinhalt, Barrierefreiheit im gerenderten Layout und Lizenz-/Entstehungsnachweis wurden in dieser reinen Content-Aufgabe nicht überprüft; keine Bilddatei verändert.

## Offene Freigabefragen

- Kein Publishing-Gate-PASS: review-required beibehalten. Renderer-Integration, tatsächliche HTML-Quellenverlinkung, Canonicals, noindex/Sitemap, responsive Layout und Druckdarstellung müssen durch die zuständige Hauptarbeit geprüft werden. Kein Build oder Deployment ausgeführt.
- Herstellerpreise können sich ändern. Vor Veröffentlichung erneut die TK-Modellkarten lesen und Bedingungen im Angebot prüfen. Keine Garantie, dass ein persönliches Angebot diese Einstiegspreise erreicht.
- Regionale Serviceabdeckung, Einsatzfristen, Ersatzteilversorgung und konkrete Garantien sind schriftlich im individuellen Angebot zu klären. Kein Anbieter kontaktiert.
- Persönlicher Förderanspruch, bewilligte Summe und weitere geplante Maßnahmen bleiben offen; keine Versicherungs-/Fördervermittlung.
- Bilddateien vorhanden, aber nicht physisch/visuell gegen die Artikel geprüft. Vor Veröffentlichung korrekte schematische Darstellung und Herkunft bestätigen.
- Bestehender Angebotsvergleichsentwurf bleibt bestehen. Bei späterer Veröffentlichung prüfen, ob eine eigenständige Seite wirklich erforderlich ist oder ihre Nutzteile in Kosten-/Firmenratgebern aufgehen. Keine neue vierte Seite erstellt.

## Rechercheartefakte außerhalb des Repositories

Profil-Scratch: /Users/mac/.hermes/profiles/milo/cache/scratch/treppenlift-batch/
Dort: retrieval.json mit Live-Antworten, source-0.txt bis source-7.txt, drei lokale Belegledgers, daraus generierte Prüffassungen und verification.json. Diese temporären Dateien können vom regulären Scratch-Cleanup entfernt werden. Dauerhafte Kernaussagen, URLs, wörtliche Belege und Grenzen sind deshalb in diesem Protokoll enthalten.
