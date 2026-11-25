# QUOTES.md — Region Baden-Württemberg (region-bw-251126)

Recherche: offizielle Primärquellen Baden-Württemberg für Wohnraumanpassung
(Treppenlift, barrierearmes Bad). **Kein Content-Entwurf — nur Belege.**
Abrufdatum aller Quellen: **25.11.2026** (curl bzw. Browser-Render; Roh-Extrakte
und PDF-Originale im selben Verzeichnis). Nicht-staatliche Quellen sind nicht
verwendet; das Kommunale-Beispiel (Nr. 8) ist eine gekennzeichnete
Einzelfall-Quelle des Landeserviceportals.

Schema-Vorbild: NRW/Bayern/Sachsen-Regionen mit 4 Wegen:
1. Pflegekasse (Bundesrecht, keine Beträge auf der Region-Seite),
2. Landesprogramm (L-Bank „Zusatzfinanzierung Barrierefreiheit“),
3. Eingliederungshilfe (§ 113/§ 77 SGB IX, Träger: Stadt-/Landkreise),
4. KfW-Stand (455-B gestoppt, Kredit 159).

Verbatim-Check: `research/check_quotes_region_bw_251126.py` (lernt die
„…“-Zitate aus dieser Datei, normalisiert Soft-Hyphen/U+200b/U+2060 und
prifft jedes Zitat als Substring gegen die referenzierte Evidenz-Datei).

---

## Weg 2 (Kern): L-Bank „Zusatzfinanzierung Barrierefreiheit“ (Produktseite)

- **URL:** https://www.l-bank.de/produkte/wohnimmobilien/eigentumsfinanzierung-bw-zusatzfinanzierung-barrierefreiheit.html
- **Abrufdatum:** 25.11.2026 (curl, HTTP 200)
- **Roh-Extrakt:** `lbank-barrierefreiheit.html` / `.txt`
- **Wörtliche Zitate:**
  1. „Die Zusatzfinanzierung – Barrierefreiheit unterstützt Sie, wenn Sie eine gebrauchte Immobilie so umbauen, dass sie hinterher weniger Barrieren hat. Sie können Schwellen entfernen, Wände und Durchgänge versetzen, Bad umbauen, Terrassen und Balkone gestalten und vieles mehr.“
  2. „Sie erwerben oder besitzen eine gebrauchte Immobilie, die Sie zum Abbau von Barrieren und Erhöhung des Wohnkomforts umbauen möchten.“
  3. „Sie haben durch eine Schwerbehinderung spezielle Wohnbedürfnisse und möchten bestehenden, selbst genutzten Wohnraum unabhängig von einer vorherigen oder gleichzeitigen Förderung altersgerecht umbauen (Anpassungsförderung).“
  4. „Sie halten die Bedingungen der DIN 18040-2 ein.“
  5. „Kredithöhe: bis zu 50.000 €“
  6. „Sollzinssatz: 1,00 %“
  7. „Sollzinsverbilligung und -bindung: 10 Jahre“
  8. „Tilgung: 3,00 %“ / „mit 2 tilgungsfreien Anlaufjahren“
  9. „Ergänzender Tilgungszuschuss bei Herstellung von Barrierefreiheit eines altersgerechten Hauses durch die vollständige Umsetzung der DIN 18040-2: 3 % der förderfähigen Kosten, maximal 1.500 €.“
  10. Maßnahmenliste: „Einzelmaßnahmen zur Barriere-Reduzierung nach DIN 18040-2“ — „Umbau von Wegen zu Gebäuden und Wohn­umfeld­maßnahmen“ — „Umbau Eingangsbereich und Wohnungs­zugang“ — „Überwindung von Treppen und Stufen“ — „Anpassung der Raum­aufteilung und Schwellenabbau“ — „Maßnahmen an Sanitär­räumen“ — „und vieles mehr (siehe hierzu den Maßnahmen- und Anforderungskatalog)“
  11. „In einem altersgerechten Haus oder einer altersgerechten Wohnung müssen Zugang, Wohn- und Schlafzimmer, Küche und Bad barrierereduziert sein und bestimmte Bedienelemente aufweisen.“
  12. „Das können Sie nicht finanzieren: Gebrauchte Immobilien, die Sie mit der Basisförderung der Eigentumsfinanzierung BW (Z15-Darlehen) vor mehr als 10 Jahren gekauft haben (Datum der Zusage).“
  13. „Den Antrag stellen Sie zusammen mit der Basisförderung bei Ihrer Wohnraumförderungsstelle. Wenn Sie die Zusatzförderung später beantragen, wenden Sie sich direkt an uns.“
  14. „Ihre Wohnraumförderungsstelle finden Sie im Landratsamt oder im Bürgermeisteramt des Ortes, in dem Sie bauen oder kaufen wollen.“
  15. „Sie finden die aktuellen Voraussetzungen der DIN 18040-2 zusammengefasst als Maßnahmen- und Anforderungskatalog unter Dokumente und Formulare auf dieser Seite.“
  16. „Damit können Sie die Förderung kombinieren:“ … „Altersgerecht-Umbauen-Kredit 159 oder Barrierereduzierung-Investionszuschuss 455-B“
  17. Zeitbanner: „Aufgrund der hohen Nachfrage und begrenzten Subventionsmitteln kann es derzeit zu Verzögerungen kommen.“ / „Nach aktuellem Stand ist jedoch von einer Wartezeit von mindestens einem Jahr bis zur Bewilligung auszugehen.“
  18. Merkblatt-Änderungslog: „12/2025 | Anpassung von Punkt 5 aufgrund der Einführung der Online-Antragstellung ab dem 01.12.2025“
- **Absenz-Needle:** `Treppenlift` kommt auf dieser Seite **0×** vor (`grep -c Treppenlift` = 0); benannt ist nur „Überwindung von Treppen und Stufen“.
- **Nicht gefunden / offen:** Download-URL des „Merkblatt Zusatzförderung Barrierefreiheit“ und des „Maßnahmen- und Anforderungskatalog der DIN 18040-2“ ist weder im statischen HTML noch im gerenderten DOM als href vorhanden (nur Produktinformationsblatt + Konditionenübersicht sind direkte Links); der indexierte binaries-Link führt auf die L-Bank-Fehlerseite 404. → Katalog-Inhalt (Treppenlift namentlich?) **unverified**, dokumentiert in ledger.warnings.

## Weg 2: L-Bank Produktinformationsblatt (PDF, 01/25)

- **URL (direkter Link der Produktseite):** https://www.l-bank.de/download/version/c839977e-52f9-4d92-aece-a672d24ad3f9/20250205_zusatzfinanzierung-barrierefreiheit_05-02-2025.pdf
- **Roh-Extrakt:** `lbank-produktblatt-barrierefreiheit.pdf` / `.txt`
- **Wörtliche Zitate:**
  1. „Zusatzfinanzierung für Haushalte, die ein Z15-Darlehen der Basisförderung erhalten“
  2. „Kredithöhe: bis zu 50 TEUR“
  3. „Tilgungssatz: 3 %“ / „Tilgungsfreie Anlaufjahre: 2“ / „Sollzinsverbilligung und -bindung: 10 Jahre“
  4. „Ergänzender Tilgungszuschuss: bis zu 1.500 EUR bei Herstellung einer vollständigen Barrierefreiheit nach DIN 18040-2“
  5. „Den Antrag stellen Sie zusammen mit dem für die Basisförderung bei der Wohnraumförderungsstelle des Landratsamts bzw. Bürgermeisteramts. Wenn Sie die Zusatzförderung später beantragen, wenden Sie sich direkt an die L-Bank.“
  6. „Immobilien, deren Bewilligung der Basisförderung mehr als 10 Jahre zurückliegt“ (nach der Überschrift „Nicht geeignet für:“)
  7. „Aktuelle Zinsen und Konditionen unter: l-bank.de/z15“

## Weg 2: L-Bank Konditionenübersicht Eigentumsförderung (PDF, Stand 20.11.2026)

- **URL (direkter Link der Produktseite):** https://www.l-bank.de/download/version/d1992237-d9e0-41ca-8ed8-193d8301acbe/wi-konditionen_eigentum20112026_20-11-2026.pdf
- **Roh-Extrakt:** `lbank-konditionen-eigentum-20261120.pdf` / `.txt`
- **Wörtliche Zitate:**
  1. „Zusatzfinanzierung - Energieeffizienz / Barrierefreiheit“ / „mit 10-jähriger Sollzinsbindung, zwei tilgungsfreien Anlaufjahren und 10-jähriger Zinsverbilligung“
  2. „Zusatzförderung – Barrierefreiheit nach DIN 18040-2“ / „Einzelmaßnahmen (bis max. 50.000 Euro)“ / „Vollständige Barrierefreiheit (bis max. 50.000 Euro)“
  3. „3,0 % (bis max. 1.500 Euro)“ (mit Fußnote 15)
  4. „Der Tilgungszuschuss beträgt 3 % des Förderdarlehensbetrages und ist auf 1.500 Euro bzw. 3.600 Euro begrenzt.“
  5. „Die Angaben in dieser Übersicht sind freibleibend und haben nur Gültigkeit für das Neugeschäft. Die Darlehensbedingungen im Einzelnen entnehmen Sie bitte den jeweiligen Merkblättern oder der VwV zum jeweiligen Landeswohnraumförderungsprogramm.“
  6. „Stand: 20.11.2026“ / „Wohnungsbau BW 2022“
- **Warnung:** PDF-Spaltenlayout → beim Textexport Spalten-Interleave; die Zuordnung Einzelmaßnahmen vs. Vollständige Barrierefreiheit zum Zuschusswert ist aus dem TXT allein nicht eindeutig. Maßgeblich für die Semantik ist das Produktseiten-Zitat Nr. 9 (Tilgungszuschuss nur bei vollständiger Barrierefreiheit). Beträge als Tabellen-Nadeln verwendbar (`74.550 €` etc. siehe Erlass-Anlage), Prosa-Claims daraus nicht ableiten.

## Weg 2: L-Bank Z15-Darlehen für schwerbehinderte Menschen (Basisförderung, Kontext Anpassungsförderung)

- **URL:** https://www.l-bank.de/produkte/wohnimmobilien/eigentumsfinanzierung-bw-z-15-darlehen-schwerbehinderte.html
- **Abrufdatum:** 25.11.2026 (curl, HTTP 200)
- **Roh-Extrakt:** `lbank-z15-schwerbehinderte.html` / `.txt`
- **Wörtliche Zitate:**
  1. „Eigentumsfinanzierung BW – Z15-Darlehen (Basisförderung) für schwerbehinderte Menschen mit speziellen Wohnbedürfnissen“
  2. „Als schwerbehinderter Mensch mit speziellen Wohnbedürfnissen erhalten Sie von uns Unterstützung in Form von besonders günstigen Darlehen auf dem Weg ins barrierefreie Eigenheim.“
  3. „Anpassungsförderung bei bereits vorhandenem Wohnraum:“ / „Kredithöhe: bis 50.000 €“
  4. „Bei vollständiger Barrierefreiheit nach Ausführung der DIN 18040-2 erhalten Sie zusätzlich einen Tilgungszuschuss von bis zu 1.500 €.“
  5. „Die Einkommensgrenze wird regelmäßig angepasst und ist im Merkblatt unter Dokumente und Formulare ersichtlich.“
  6. „Wenn der bestehende Wohnraum Ihren speziellen Wohnbedürfnissen aufgrund Ihrer Schwerbehinderung nicht angemessen ist, ist eine Förderung trotz bestehenden Wohneigentums möglich.“

## Weg 2: service-bw Wohnraumförderung (Förderung von selbst genutztem Wohneigentum beantragen)

- **URL:** https://www.service-bw.de/zufi/leistungen/553 (JS-gerendert; Textsicherung `live-servicebw-wohneigentum-553-rendered.txt`)
- **Freigabevermerk:** „05.03.2026 Ministerium für Landesentwicklung und Wohnen Baden-Württemberg“
- **Wörtliche Zitate:**
  1. „Privatpersonen können im Rahmen des geltenden Landeswohnraumförderungsprogramms eine Förderung erhalten.“
  2. „altersgerechter Umbau selbst genutzten Wohnraums (eigenständige sogenannte \“Anpassungsförderung\“; auch als zusätzliche Förderung möglich)“
  3. „Eine zusätzliche Förderung ist insbesondere möglich bei:“ … „Herstellung von Barrierefreiheit des selbstgenutzten Wohnraums“ … „baulichen Maßnahmen aufgrund schwerer Behinderung und speziellen Wohnbedürfnissen beziehungsweise altersgerechtem Umbau des selbst genutzten Wohnraums.“
  4. „Die Förderung erfolgt durch zinsverbilligte Darlehen und durch Zuschüsse.“
  5. „schwerbehinderte Menschen mit speziellen Wohnbedürfnissen. Die Schwerbehinderung bestimmt sich nach dem Sozialgesetzbuch, wonach ein Grad der Behinderung von wenigstens 50 erforderlich ist. Die speziellen Wohnbedürfnisse hinsichtlich des Grundrisses oder der Ausstattung müssen von der Schwerbehinderung herrühren.“
  6. Zuständigkeit: „in Landkreisen: die Wohnraumförderungsstelle im Landratsamt“ / „in Stadtkreisen: die Wohnraumförderungsstelle im Bürgermeisteramt des Bauortes“
  7. Verfahren: „Die zuständige Stelle (Wohnraumförderungsstelle) prüft im Portal Ihren Antrag auf Vollständigkeit und Förderfähigkeit. Vollständige und förderfähige Anträge leitet die Wohnraumförderungsstelle der L-Bank zur weiteren Bearbeitung zu.“
  8. „Achtung: Ein vorzeitiger Vorhabenbeginn führt zur Ablehnung der Förderung. Sie können mit dem Vorhaben auf eigenes Risiko beginnen, wenn Ihnen der Eingang des vollständigen und prüffähigen, unterschriebenen Antrags von der zuständigen Stelle (Wohnraumförderungsstelle) bestätigt wurde.“
  9. „Es besteht grundsätzlich keine Antragsfrist.“
  10. „Es ist eine Eigenleistung erforderlich. Die Eigenleistung beträgt mindestens 25 Prozent der Gesamtkosten des förderfähigen Vorhabens. Bei erstrangiger Absicherung des Darlehens beträgt die Eigenleistung mindestens 15 Prozent der Gesamtkosten.“
  11. „Das Gesamtjahreseinkommen darf die für Ihren Haushalt maßgebliche Einkommensgrenze nicht überschreiten.“

## Weg 2: MLW — Förderprogramm „Wohnungsbau BW 2022“ (Programmseite Ministerium)

- **URL:** https://mlw.baden-wuerttemberg.de/de/bauen-wohnen/wohnungsbau/wohnungsbau-bw/
- **Abrufdatum:** 25.11.2026 (curl, HTTP 200)
- **Roh-Extrakt:** `mlw-wohnungsbau-bw.html` / `.txt`
- **Wörtliche Zitate:**
  1. „Das aktuelle Wohnraumförderprogramm des Landes \“Wohnungsbau BW 2022\“ ist seit 2022 in Kraft.“
  2. „Ziel ist es, einkommensschwächeren Haushalten zu ermöglichen, angemessenen Wohnraum zu mieten oder Wohneigentum zur eigenen Nutzung zu bilden.“
  3. „Die Förderanträge sind bei den zuständigen Wohnraumförderungsstellen einzureichen (Ausnahme siehe unten). Die Wohnraumförderungsstellen legen geprüfte und förderfähige Anträge der L-Bank zur Entscheidung vor.“
  4. „Eine umfassende Beratung erhalten Sie durch die Wohnraumförderungsstelle des für Sie zuständigen Landratsamts oder Bürgermeisteramts Ihres Stadtkreises.“
  5. Rechtsgrundlagen-Liste: „Verwaltungsvorschrift zum Förderprogramm Wohnungsbau Baden-Württemberg 2022 (VwV Wohnungsbau BW 2022), redaktionelle Neufassung vom 1. April 2025 (PDF)“ + „VwV-Wohnungsbau BW 2022 – Erlass Änderung Einkommensgrenzen vom 1. Dezember 2025 (PDF)“

## Weg 2: MLW-Erlass „Einkommensgrenzen in der Wohnraumförderung“ v. 01.12.2025 (+ Anlage)

- **URLs:**
  - Erlass: https://mlw.baden-wuerttemberg.de/fileadmin/redaktion/m-mlw/intern/Dateien/03_Bauen-Wohnen/Wohnungsbau/Wohnraumfoerderung/2025_12_VwV-Wohnungsbau_BW_2022_-_Erlass_Aenderung_Einkommensgrenzen.pdf
  - Anlage (Tabelle): https://mlw.baden-wuerttemberg.de/fileadmin/redaktion/m-mlw/intern/Dateien/03_Bauen-Wohnen/Wohnungsbau/Wohnraumfoerderung/2025_12_VwV-Wohnungsbau_BW_2022_Anlage_zum_Erlass_vom_01.12.2025_ge.pdf
- **Roh-Extrakte:** `mlw-erlass-einkommensgrenzen-20251201.pdf/.txt`, `mlw-erlass-einkommensgrenzen-anlage-20251201.pdf/.txt`
- **Wörtliche Zitate (Erlass):**
  1. „Förderprogramm Wohnungsbau BW 2022 (VwV-Wohnungsbau BW 2022) Einkommensgrenzen in der Wohnraumförderung“
  2. „bleiben auch weiterhin als maßgebliche Fördergrundlage wirksam“ (Kontext: Satz beginnt mit 'Die Förderbestimmungen der zum 1. April 2025 als redaktionelle Neufassung in Kraft getretenen Verwaltungsvorschrift …'; im TXT durch Seitenfußzeile unterbrochen, daher Fragment-Nadel)
  3. „Die Bezugsgröße beträgt jetzt 71 000 Euro (bislang: 68 000 Euro) als gerundeter durchschnittlicher Bruttojahresverdienst der Arbeitnehmerschaft im Jahr 2024. Aufgrund der gesetzlich verankerten Dynamisierung der Einkommensgrenzen (§ 10 Abs. 3 Satz 1 Landeswohnraumförderungsgesetz – LWoFG) sind diese entsprechend fortzuschreiben.“
  4. „Diese Einkommensgrenzen sind ab sofort anzuwenden.“
- **Wörtliche Zitate (Anlage):**
  1. „Einkommensgrenzen des Förderprogramms Wohnungsbau BW 2022 – Anpassung der Bezugsgröße auf 71.000 Euro“
  2. Spalten-/Zeilenmarken: „Minderung des Abzugs je schwerbehinderte Person (ab der 2. Person) gemäß Abschnitt I Nummer 10“ — „Berechnungsbeispiele (mit schwerbehinderte/r Person)“ — „Anpassung der Bezugsgröße auf 71.000 Euro“
  3. Betrags-Nadeln (Spalten-Interleave! siehe Warnung): „71.000 €“, „74.550 €“, „78.100 €“, „84.050 €“, „93.550 €“, „103.050 €“, „106.600 €“, „80.500 €“, „90.000 €“
- **Warnung:** Die zeilengenaue Zuordnung Personenzahl → Grenzbetrag ist aus dem PDF-Textexport wegen Spalten-Interleave nicht abschließend gesichert. Die Zahlengruppe 74.550/78.100/84.050/87.600/93.550/97.100/103.050/106.600 steht im Anlagen-Text unter den Berechnungsbeispielen mit schwerbehinderter Person; die Sekundärquelle deutschewohnhilfe.de liest sie als Eigentumsförderungs-Grenzen bei 2/3/4/5-Personen-Haushalten mit bzw. mit 2 schwerbehinderten Personen — **für die Region-Seite nur als Verweis auf Anlage 3/Erlass verwenden, keine zugeordneten Betrags-Paare publizieren** (oder Parent verifiziert visuell im PDF).

## Weg 2 (Beispiel, gekennzeichnet): service-bw „Senioren- und behindertengerechtes Wohnen“ — Stadt Friedrichshafen

- **URL:** https://www.service-bw.de/zufi/leistungen/531 (JS-gerendert; `live-servicebw-kommunal-friedrichshafen-531-rendered.txt`)
- **Freigabevermerk:** „Stadt Friedrichshafen, 01.11.2025“
- **Wörtliche Zitate:**
  1. „Die Stadt Friedrichshafen fördert im Rahmen der zur Verfügung stehenden Haushaltsmittel den barrierefreien Umbau von bestehenden Gebäuden oder Wohnungen.“
  2. „Die Zuschüsse sind eine freiwillige Sozialleistung, auf die kein Rechtsanspruch besteht.“
  3. „Sie sind keine öffentlichen Mittel im Sinne des Landeswohnraumförderungsgesetzes (LWoFG).“
  4. „Alternativ: Treppenlift“ / „Der Treppenlift Innerhalb eines Einfamilienhauses oder einer Maisonettwohnung muss problemlos mit einem Rollstuhl benutzt werden können.“ [„Innerhalb“ sic — Großschreibung der Seite]
  5. „Aufzug / Treppenlift – Maximale Förderung 2.500 Euro“
  6. „Sanitär – Maximale Förderung 1.500 Euro“
  7. „Eingangs- und Zimmertüren – Maximale Förderung 500 Euro“ / „Hauszugang: Rampe – Maximale Förderung 500 Euro“
- **Einordnung:** Kommunales Einzelfallprogramm (nur Friedrichshafen), NICHT flächendeckend, kein LWoFG-Mittel. Auf der Region-Seite höchstens als gekennzeichnetes Beispiel; Pflicht-Kontext-Zitat: „Eigentümer und Vermieter von bestehenden Gebäuden in Friedrichshafen sowie von Eigentumswohnungen in einem Mehrfamilienhaus in Friedrichshafen sind antragsberechtigt.“

## Weg 3: Eingliederungshilfe — Bundesrecht

- **§ 113 SGB IX:** https://www.gesetze-im-internet.de/sgb_9_2018/__113.html (`sgb9-113.txt`)
  - „Leistungen zur Sozialen Teilhabe sind insbesondere 1. Leistungen für Wohnraum“ (Aufzählung Abs. 2; im Gesetzestext folgt die Nummernliste)
- **§ 77 SGB IX:** https://www.gesetze-im-internet.de/sgb_9_2018/__77.html (`sgb9-77.txt`)
  - „Leistungen für Wohnraum werden erbracht, um Leistungsberechtigten zu Wohnraum zu verhelfen, der zur Führung eines möglichst selbstbestimmten, eigenverantwortlichen Lebens geeignet ist. Die Leistungen umfassen Leistungen für die Beschaffung, den Umbau, die Ausstattung und die Erhaltung von Wohnraum, der den besonderen Bedürfnissen von Menschen mit Behinderungen entspricht.“
  - „(2) Aufwendungen für Wohnraum oberhalb der Angemessenheitsgrenze nach § 42a des Zwölften Buches sind zu erstatten, soweit wegen des Umfangs von Assistenzleistungen ein gesteigerter Wohnraumbedarf besteht.“

## Weg 3: Sozialministerium BW — „Eingliederungshilfe“ (Trägerstruktur)

- **URL:** https://sozialministerium.baden-wuerttemberg.de/de/soziales/bundesteilhabegesetz/eingliederungshilfe/
- **Roh-Extrakt:** `smbw-egh.html` / `.txt`
- **Wörtliches Zitat:**
  1. „Das Land Baden-Württemberg hat die 44 Stadt- und Landeskreise als Träger der Eingliederungshilfe bestimmt.“
  2. „Der Rahmenvertrag regelt das Nähere dazu, wie die Leistungen der Eingliederungshilfe nach dem SGB IX in Baden-Württemberg erbracht und vergütet werden sollen.“

## Weg 3: service-bw „Eingliederungshilfe für Menschen mit Behinderungen beantragen“

- **URL:** https://www.service-bw.de/zufi/leistungen/1179 (JS-gerendert; `live-servicebw-egh-1179-rendered.txt`)
- **Freigabevermerk:** „08.01.2026 Sozialministerium Baden-Württemberg“
- **Wörtliche Zitate:**
  1. Zuständigkeit: „Ihr Sozialamt.“ / „wenn Sie in einem Stadtkreis wohnen: die Stadtverwaltung (Rathaus)“ / „wenn Sie in einem Landkreis wohnen: das Landratsamt.“
  2. „Hinweis: Teilweise haben die Landkreise die Zuständigkeit auf größere Städte in ihrem Kreisgebiet übertragen.“
  3. Verfahren: „Vereinbaren Sie zunächst einen Termin mit dem zuständigen Sozialamt des Stadt- oder Landkreises, in dem Sie wohnen.“
  4. „Nach der konkreten Feststellung der Leistungen, erstellt das Sozialamt mit Ihnen gemeinsam einen Gesamtplan, der regelmäßig, spätestens alle zwei Jahre, überprüft und fortgeschrieben wird.“
  5. Unterlagen: „Einkommensnachweise (zum Beispiel Rentenbescheide, Verdienstbescheinigungen)“ / „Vermögensnachweise (zum Beispiel Sparbücher, Bausparverträge)“ / „ärztliche Gutachten und Unterlagen.“
  6. Kosten: „keine“ + „Bei entsprechendem Einkommen und Vermögen kann, je nachdem, um welche Leistung es geht, ein Beitrag zu den Aufwendungen beziehungsweise der Einsatz des Vermögens verlangt werden.“
  7. Rechtsgrundlage: „Neuntes Buch Sozialgesetzbuch (SGB IX)“ „: Teil 2 Eingliederungshilferecht“
- **Absenz-Needle:** `Treppenlift` 0× auf dieser Seite; die Leistungsbeispiele nennen EGH-Bereiche, aber Wohnraum-Umbau nur über §§ 113/77 SGB IX-BVerweis erschließbar (wie Sachsen: namentliche Nennung der Wohnraum-Umbaubeispiele fehlt auf Portal-Ebene).

## Weg 1 (bundesweit): § 40 SGB XI + BMG

- **§ 40 Abs. 4 SGB XI:** https://www.gesetze-im-internet.de/sgb_11/__40.html (`sgb11-40.txt`)
  1. „Die Pflegekassen können subsidiär finanzielle Zuschüsse für Maßnahmen zur Verbesserung des individuellen Wohnumfeldes des Pflegebedürftigen gewähren, beispielsweise für technische Hilfen im Haushalt, wenn dadurch im Einzelfall die häusliche Pflege ermöglicht oder erheblich erleichtert oder eine möglichst selbständige Lebensführung des Pflegebedürftigen wiederhergestellt wird.“
  2. „Die Zuschüsse dürfen einen Betrag in Höhe von 4 180 Euro je Maßnahme nicht übersteigen.“
  3. „Der Gesamtbetrag je Maßnahme nach Satz 3 ist auf 16 720 Euro begrenzt und wird bei mehr als vier Anspruchsberechtigten anteilig auf die Versicherungsträger der Anspruchsberechtigten aufgeteilt.“
  4. Fristen (Abs. 7): „spätestens bis zum Ablauf von drei Wochen nach Antragseingang oder in Fällen, in denen eine Pflegefachperson oder der Medizinische Dienst nach Absatz 1 Satz 2 beteiligt wird, innerhalb von fünf Wochen nach Antragseingang zu entscheiden.“ + „Erfolgt keine Mitteilung eines hinreichenden Grundes, gilt die Leistung nach Ablauf der Frist als genehmigt.“
- **BMG „Zuschüsse zur Wohnungsanpassung“:** https://www.bundesgesundheitsministerium.de/pflege-zu-hause/zuschuesse-zur-wohnungsanpassung (`bmg-wohnanp.txt`)
  1. „Die Pflegekasse kann für Pflegebedürftige der Pflegegrade 1 bis 5 auf Antrag bis zu 4.180 Euro als Zuschuss für Anpassungsmaßnahmen zahlen, die die häusliche Pflege in der Wohnung ermöglichen, erheblich erleichtern oder eine möglichst selbstständige Lebensführung der pflegebedürftigen Person wiederherstellen.“
  2. „fest installierte Rampen und Treppenlifte“ (Beispielmaßnahmen)
  3. „Wohnen mehrere Anspruchsberechtigte zusammen, kann der Zuschuss bis zu viermal 4.180 Euro, also bis zu 16.720 Euro, betragen.“
  4. „Ein Zuschuss zur Wohnungsanpassung kann auch ein zweites Mal gewährt werden, wenn die Pflegesituation sich so verändert hat, dass erneute Maßnahmen nötig werden.“
  5. „Die gesetzlich vorgegebene Bearbeitungsfrist für Anträge auf bauliche Anpassungsmaßnahmen in der Wohnung beträgt drei Wochen nach Antragseingang. Sie verlängert sich auf fünf Wochen, wenn für die Leistungsentscheidung ein medizinisches Gutachten notwendig ist.“

## Weg 1: Pflegestützpunkte / Beratung BW

- **Sozialministerium BW „Beratung“:** https://sozialministerium.baden-wuerttemberg.de/de/gesundheit-pflege/pflege/beratung (`smbw-pflege-beratung.txt`)
  1. „Pflegestützpunkte in Baden-Württemberg leisten koordinierte Hilfe“
  2. „Zur wohnortnahen Beratung, Versorgung und Betreuung der Bevölkerung wurden in Baden-Württemberg Pflegestützpunkte errichtet.“ / „Ein Pflegestützpunkt berät unabhängig, neutral und kostenlos rund um das Thema Pflege, koordiniert Hilfs- und Unterstützungsangebote bei der wohnortnahen Betreuung und Versorgung und trägt zur besseren Vernetzung der pflegerischen und sozialen Versorgungs- und Betreuungsangebote bei.“ (Seite listet die drei Leistungen als Aufzählung unter der Überschrift „Ein Pflegestützpunkt“)
  3. „Einen Überblick über die in Baden-Württemberg eingerichteten Pflegestützpunkte erhalten Sie auf der Website „Pflegestützpunkt Baden-Württemberg““ [im Original folgt nach dem Schlusszeichen noch ein Leerzeichen vor dem Punkt]
- **Pflegestützpunkte-Portal:** https://www.bw-pflegestuetzpunkt.de/ (`bw-pflegestuetzpunkt.txt`)
  1. „Alle Stadt- und Landkreise in Baden-Württemberg haben Pflegestützpunkte mit regionalen Standorten und bieten eine wohnortnahe Beratung an.“
  2. „Wir beraten individuell, trägerneutral und kostenfrei.“
  3. „Träger der Pflegestützpunkte Baden-Württemberg:“ + „AOK Baden-Württemberg, BKK Landesverband Süd, BARMER, DAK-Gesundheit, Hanseatische Krankenkasse, HKK Bremen, IKK Classic, Kaufmännische Krankenkasse - KKH, KNAPPSCHAFT, Sozialversicherung für Landwirtschaft, Forsten und Gartenbau, Techniker Krankenkasse, Örtliche Träger. der Sozialhilfe (Stadtkreise und Landkreise BW)“ [Punktierung sic]

## Weg 4: KfW-Stand (25.11.2026)

- **455-B Produktseite:** https://www.kfw.de/inlandsfoerderung/Privatpersonen/Bestandsimmobilie/F%C3%B6rderprodukte/Altersgerecht-Umbauen-Investitionszuschuss-(455)/ (`kfw-455b.txt`)
  1. „Diesen Zuschuss können Sie nicht mehr beantragen.“
  2. „Wegen der hohen Nachfrage sind die Förder­mittel für Maßnahmen zur Barriere­reduzierung bereits ausgeschöpft. Ab sofort können Sie daher keine Anträge mehr im Produkt \“Altersgerecht Umbauen – Barriere­reduzierung\“ (455-B) stellen.“
  3. „Sollten im Jahr 2027 erneut Bundes­mittel für barriere­reduzierende Maßnahmen bereit­gestellt werden, wird eine Antrag­stellung wieder möglich sein.“
- **Kredit 159:** https://www.kfw.de/159 (`kfw-159.txt`)
  1. „Kreditbetrag: bis zu 50.000 Euro je Wohneinheit“
  2. Maßnahmenkatalog nennt: „Treppenlifte, Senkrecht-, Hebe- oder Plattform­lifte installieren“
  3. Kombi mit Pflegekasse: „Ausnahme: Wird eine Maßnahme (z. B. Badumbau) mit dem Zuschuss der Pflege­versicherung gefördert, können andere Maßnahmen (z. B.­ Treppenlift) mit dem Kredit der KfW gefördert werden.“
  4. „Die Förderung steht unter dem Vorbehalt verfügbarer Haushalts­mittel. Ein Rechts­anspruch hierauf besteht grund­sätzlich nicht.“
  5. Konditionen-Fallback der Seite: Zins-Platzhalter „-,-- % p.a.“ (KfW blendet Zinsen dynamisch ein — keine Zinszahlen von der Seite übernehmen)

## Dokumentierte Lücken (unverified)

1. **L-Bank Merkblatt „Zusatzförderung Barrierefreiheit“ (gültig ab 01.05.2026)** und **Maßnahmen- und Anforderungskatalog DIN 18040-2**: auf der Produktseite gelistet, aber Download-URL weder statisch noch gerendert exponiert; indexierter binaries-Link → 404-Fehlerseite. Frage „Nennt der Katalog Treppenlifte namentlich?“ **offen**.
2. **VwV-Wohnungsbau BW 2022 (Volltext, landesrecht-bw.de)**: React-SPA, Rendering in dieser Session nicht gelungen; Treppenlift-Absenz/Präsenz im VwV-Text **nicht geprüft**. Fundstelle der Neufassung: GABl. 2025, S. 501 (Dokumentkopf via Suchauszug; Seite selbst nicht gesichert).
3. **Zeilengenaue Einkommensgrenzen-Zuordnung** (Personenzahl → Betrag, Eigentumsförderung): PDF-Spalten-Interleave, nur Betrags-Nadeln gesichert (s. o.).
4. Wartezeit-Banner („mindestens einem Jahr“) ist seitenweiter L-Bank-Hinweis — Programmbezug folgt aus der Platzierung auf der Produktseite, aber eine programm-spezifische Wartezeitangabe existiert nicht.
