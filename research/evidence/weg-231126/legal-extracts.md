# WEG-Artikel (Treppenlift & bauliche Veränderungen, WEG) – offizielle Rechtsquellen, wörtliche Zitate

Alle Quellen am 2026-11-23 (CET) abgerufen. Umfang: 35 wörtliche Zitate aus 7 Dokumenten (3+x WEG-Einzelnormen, 2 BGH-Urteile als offizielle PDFs, 1 BGH-Pressemitteilung). Jedes Zitat ist maschinell gegen den bereinigten Quelltext verifiziert (literaler Teilstring-Nachweis); Rohdateien unter `raw/`; strukturiertes Gegenstück: `ledger-legal.json`.

**Wichtige Korrektur zum Projektwissen:** Die Shortcode-Annahme 'wegg' für das WEG auf gesetze-im-internet.de ist falsch. Die Titelsuche des Seiteneigenen Systems (`/cgi-bin/htsearch?config=Titel_bmjhome2005&words=Wohnungseigentumsgesetz`) liefert den Shortcode **`woeigg`** (Wohnungseigentumsgesetz = 'Gesetz über das Wohnungseigentum und das Dauerwohnrecht'); `wegg/` und `weg/` liefern HTTP 404. Die Einzelnormen liegen unter `/woeigg/__N.html`. Verifizierte Version: Fassung der Bekanntmachung vom 12.01.2021 (BGBl. I S. 34, WEMoG-Neufassung; Geltung ab 01.12.2020), zuletzt geändert durch Art. 1 G v. 10.10.2024 (BGBl. 2024 I Nr. 306, Steckersolargeräte in § 20 Abs. 2 Nr. 5).

**Doku Versuch V ZR 244/22 (offizielles PDF):** Direkter Zugriff scheiterte zunächst am Namensschema: `.../V_ZS/2022/V_ZR__244-22.pdf` (Doppel-Unterstrich, analog V_ZR__33-23.pdf) → HTTP 404; Varianten mit Jahr 2023/2024 im Pfad → HTTP 200 mit text/html (Soft-404-Fehlerseite, 29.958 Bytes). Über die Entscheidungssuche des BGH (`SiteGlobals/Forms/Suche/EntscheidungssucheBGH_Formular.html?templateQueryString=V+ZR+244/22`) wurde die offizielle URL mit **einem** Unterstrich gefunden: `V_ZS/2022/V_ZR_244-22.pdf?__blob=publicationFile&v=1` → HTTP 200, application/pdf, 238.872 Bytes, 27 Seiten. gesetze.co-Spiegel (nicht-offiziell) wurde daher nicht benötigt.


## 1) WEG § 20 – Bauliche Veränderungen (gesetze-im-internet.de, Shortcode woeigg)

- **URL:** https://www.gesetze-im-internet.de/woeigg/__20.html
- **Abgerufen (fetch date):** 2026-11-23
- **Rohdateien:** `raw/wegg__20.html + raw/wegg__20.txt`
- **Bereinigung (cleaning steps):** ISO-8859-1 decode; <head>/script/style entfernt; HTML-Tags entfernt; HTML-Entities decodiert (&#228;→ä, &nbsp;→Leerzeichen); geschützte Leerzeichen (U+00A0/U+202F) → Leerzeichen; Whitespace kollabiert.

### `weg-20-abs1` — § 20 Abs. 1

**Kontext:** Generalklausel: bauliche Veränderungen sind per Mehrheitsbeschluss möglich oder einem Einzelnen zu gestatten. Basis für Treppenlift-Beschlüsse.

```
§ 20 Bauliche Veränderungen (1) Maßnahmen, die über die ordnungsmäßige Erhaltung des gemeinschaftlichen Eigentums hinausgehen (bauliche Veränderungen), können beschlossen oder einem Wohnungseigentümer durch Beschluss gestattet werden.
```

### `weg-20-abs2` — § 20 Abs. 2 Satz 1 Nr. 1-5, Satz 2

**Kontext:** Kernanspruch: Individualanspruch auf angemessene bauliche Veränderungen für 5 privilegierte Zwecke; Nr. 1 'Gebrauch durch Menschen mit Behinderungen' ist die Anspruchsgrundlage für Treppenlift/Barrierefreiheit. Nr. 5 lautet in der aktuellen Fassung 'Stromerzeugung durch Steckersolargeräte' (geändert durch Art. 1 G v. 10.10.2024; WEMoG-Fassung v. 01.12.2020 hatte 'Solargeräte'). Satz 2 = Grundlagen-/Durchführungsbeschluss.

```
(2) Jeder Wohnungseigentümer kann angemessene bauliche Veränderungen verlangen, die 1. dem Gebrauch durch Menschen mit Behinderungen, 2. dem Laden elektrisch betriebener Fahrzeuge, 3. dem Einbruchsschutz, 4. dem Anschluss an ein Telekommunikationsnetz mit sehr hoher Kapazität und 5. der Stromerzeugung durch Steckersolargeräte dienen. Über die Durchführung ist im Rahmen ordnungsmäßiger Verwaltung zu beschließen.
```

### `weg-20-abs3` — § 20 Abs. 3

**Kontext:** Gestattungsanspruch bei Einverständnis aller Betroffenen (ergänzt Abs. 2).

```
(3) Unbeschadet des Absatzes 2 kann jeder Wohnungseigentümer verlangen, dass ihm eine bauliche Veränderung gestattet wird, wenn alle Wohnungseigentümer, deren Rechte durch die bauliche Veränderung über das bei einem geordneten Zusammenleben unvermeidliche Maß hinaus beeinträchtigt werden, einverstanden sind.
```

### `weg-20-abs4` — § 20 Abs. 4

**Kontext:** Absolute Grenze (2 Alt.) für Beschluss, Gestattung und Individualanspruch; zentral in BGH V ZR 33/23 und V ZR 244/22.

```
(4) Bauliche Veränderungen, die die Wohnanlage grundlegend umgestalten oder einen Wohnungseigentümer ohne sein Einverständnis gegenüber anderen unbillig benachteiligen, dürfen nicht beschlossen und gestattet werden; sie können auch nicht verlangt werden.
```


## 2) WEG § 21 – Nutzungen und Kosten bei baulichen Veränderungen

- **URL:** https://www.gesetze-im-internet.de/woeigg/__21.html
- **Abgerufen (fetch date):** 2026-11-23
- **Rohdateien:** `raw/wegg__21.html + raw/wegg__21.txt`
- **Bereinigung (cleaning steps):** wie § 20 (ISO-8859-1, Entities, Whitespace)

### `weg-21-abs1` — § 21 Abs. 1 Satz 1 und 2

**Kontext:** Kostentragung des verlangenden/privilegierten Eigentümers: bei Gestattung oder Durchführung auf § 20-Abs.-2-Verlangen trägt ER die Kosten allein; Nutzungen (z.B. Miet­einnahmen aus einem eingebauten Aufzug) stehen nur ihm zu.

```
(1) Die Kosten einer baulichen Veränderung, die einem Wohnungseigentümer gestattet oder die auf sein Verlangen nach § 20 Absatz 2 durch die Gemeinschaft der Wohnungseigentümer durchgeführt wurde, hat dieser Wohnungseigentümer zu tragen. Nur ihm gebühren die Nutzungen.
```

### `weg-21-abs2` — § 21 Abs. 2

**Kontext:** Ausnahme: Kostenumlage auf alle bei 2/3-Mehrheit (+ Mehrheit der MEA) bzw. amortisationsfähigen Maßnahmen; schafft den Rahmen für Gemeinschaftsfinanzierung.

```
(2) Vorbehaltlich des Absatzes 1 haben alle Wohnungseigentümer die Kosten einer baulichen Veränderung nach dem Verhältnis ihrer Anteile (§ 16 Absatz 1 Satz 2) zu tragen, 1. die mit mehr als zwei Dritteln der abgegebenen Stimmen und der Hälfte aller Miteigentumsanteile beschlossen wurde, es sei denn, die bauliche Veränderung ist mit unverhältnismäßigen Kosten verbunden, oder 2. deren Kosten sich innerhalb eines angemessenen Zeitraums amortisieren. Für die Nutzungen gilt § 16 Absatz 1.
```

### `weg-21-abs5` — § 21 Abs. 5

**Kontext:** Abweichende Kostenverteilung durch Beschluss möglich, aber Schutz vor Kostenüberwälzung auf nicht zahlungspflichtige Eigentümer.

```
(5) Die Wohnungseigentümer können eine abweichende Verteilung der Kosten und Nutzungen beschließen. Durch einen solchen Beschluss dürfen einem Wohnungseigentümer, der nach den vorstehenden Absätzen Kosten nicht zu tragen hat, keine Kosten auferlegt werden.
```


## 3) WEG § 44 – Beschlussklagen

- **URL:** https://www.gesetze-im-internet.de/woeigg/__44.html
- **Abgerufen (fetch date):** 2026-11-23
- **Rohdateien:** `raw/wegg__44.html + raw/wegg__44.txt`
- **Bereinigung (cleaning steps):** wie § 20 (ISO-8859-1, Entities, Whitespace)

### `weg-44-abs1` — § 44 Abs. 1 Satz 1 und 2

**Kontext:** Rechtsschutz: Anfechtungs-/Nichtigkeitsklage gegen Beschlüsse; Beschlussersetzungsklage, wenn die Versammlung eine Entscheidung unterlässt (z.B. Verweigerung eines § 20-Abs.-2-Grundlagenbeschlusses; so der Fall in V ZR 244/22).

```
(1) Das Gericht kann auf Klage eines Wohnungseigentümers einen Beschluss für ungültig erklären (Anfechtungsklage) oder seine Nichtigkeit feststellen (Nichtigkeitsklage). Unterbleibt eine notwendige Beschlussfassung, kann das Gericht auf Klage eines Wohnungseigentümers den Beschluss fassen (Beschlussersetzungsklage).
```


## 4) WEG – Vollzitat und Stand (Gesamtausgabekopf)

- **URL:** https://www.gesetze-im-internet.de/woeigg/BJNR001750951.html
- **Abgerufen (fetch date):** 2026-11-23
- **Rohdateien:** `raw/wegg-full.html + raw/wegg-full.txt`
- **Bereinigung (cleaning steps):** wie § 20 (ISO-8859-1, Entities, Whitespace)

### `weg-vollzitat` — Titelangabe

**Kontext:** Verifizierte Zitierfähigkeit: aktuelle Gesamtausgabe = WEG in der Fassung der Bek. v. 12.01.2021 (WEMoG-Neufassung, in Kraft seit 01.12.2020), zuletzt geändert Art. 1 G v. 10.10.2024 (BGBl. 2024 I Nr. 306).

```
Vollzitat: "Wohnungseigentumsgesetz in der Fassung der Bekanntmachung vom 12. Januar 2021 (BGBl. I S. 34), das zuletzt durch Artikel 1 des Gesetzes vom 10. Oktober 2024 (BGBl. 2024 I Nr. 306) geändert worden ist"
```

### `weg-stand` — Standangabe

**Kontext:** Standangabe der Gesamtausgabe; belegt, dass §§ 20/21/44 in der seit 01.12.2020 geltenden WEMoG-Fassung zitiert werden.

```
Stand: Neugefasst durch Bek. v. 12.1.2021 I 34; zuletzt geändert durch Art. 1 G v. 10.10.2024 I Nr. 306
```


## 5) BGH, Urteil vom 09.02.2024 – V ZR 244/22 (Personenaufzug, München) – offizielles BGH-PDF

- **URL:** https://www.bundesgerichtshof.de/SharedDocs/Entscheidungen/DE/Zivilsenate/V_ZS/2022/V_ZR_244-22.pdf?__blob=publicationFile&v=1
- **Abgerufen (fetch date):** 2026-11-23
- **Rohdateien:** `raw/vzr-244-22.pdf + raw/vzr-244-22.txt + raw/vzr-244-22.flat.txt`
- **Bereinigung (cleaning steps):** PDF (offizielles BGH-Dokument, %PDF-1.5, 27 Seiten) mit pdftotext -layout extrahiert; Seitenzahlen und ECLI-Zeilen entfernt; Trennstriche aufgelöst (wie V ZR 33/23); Whitespace kollabiert.

### `vzr244-ls-vorb` — Leitsatz (Vorbemerkung zu § 20 Abs. 1)

**Kontext:** Neurecht seit 01.12.2020: Beschluss (statt Vereinbarung) genügt auch bei Zuweisung ausschließlicher Nutzungsbefugnis am Gemeinschaftseigentum – zentral für Treppenlift/Aufzug am Gemeinschaftseigentum.

```
Die Wohnungseigentümer können nach dem seit dem 1. Dezember 2020 geltenden Wohnungseigentumsrecht eine bauliche Veränderung grundsätzlich auch dann beschließen, wenn die Beschlussfassung die Zuweisung einer ausschließlichen Nutzungsbefugnis an dem dafür vorgesehenen Gemeinschaftseigentum zur Folge hat; einer Vereinbarung der Wohnungseigentümer bedarf es hierfür nicht mehr (Abgrenzung zu Senat, Urteil vom 13. Januar 2017 - V ZR 96/16, ZWE 2017, 224 Rn. 30 ff.).
```

### `vzr244-ls-a` — Leitsatz a)

**Kontext:** Angemessenheitsvermutung für privilegierte Maßnahmen; Unangemessenheit nur ausnahmsweise bei außer Verhältnis stehenden Nachteilen.

```
a) Eine bauliche Veränderung, die einem der in § 20 Abs. 2 Satz 1 Nr. 1 bis 4 WEG aufgeführten Zwecke dient, ist regelmäßig angemessen. Die Angemessenheit ist nur ausnahmsweise aufgrund außergewöhnlicher baulicher Gegebenheiten oder eines außergewöhnlichen Begehrens zu verneinen, wenn die bauliche Veränderung bei der Gesamtheit der Wohnungseigentümer zu Nachteilen führt, die bei wertender Betrachtung außer Verhältnis zu ihrem Zweck stehen. Nachteile, die typischerweise aufgrund einer privilegierten baulichen Veränderung eintreten, begründen regelmäßig nicht deren Unangemessenheit.
```

### `vzr244-ls-b` — Leitsatz b)

**Kontext:** Darlegungs-/Beweislast: Verlangender trägt die primäre Last (Zweck), Gemeinschaft sekundäre Darlegungslast für atypische Nachteile.

```
b) Die Darlegungs- und Beweislast für die tatsächlichen Umstände der Angemessenheit einer baulichen Veränderung i.S.d. § 20 Abs. 2 Satz 1 Nr. 1 bis 4 WEG trägt der klagende Wohnungseigentümer; verlangt ein Wohnungseigentümer gemäß § 20 Abs. 2 Satz 1 Nr. 1 bis 4 WEG die Ersetzung eines Grundlagenbeschlusses, muss er zur Begründung des Anspruchs darlegen, dass die bauliche Veränderung einem der gesetzlich privilegierten Zwecke dient. Beruft sich die Gemeinschaft auf die Unangemessenheit der Maßnahme, trifft sie eine sekundäre Darlegungslast für nachteilige Umstände, die sich nicht bereits aus dem Begehren selbst ergeben.
```

### `vzr244-ls-alt2` — Leitsatz zu § 20 Abs. 4 Halbs. 1 Alt. 2

**Kontext:** Definition der unbilligen Benachteiligung (Abwägung Zumutbarkeit; Fortführung V ZR 64/19) – in V ZR 33/23 Rn. 21 ausdrücklich in Bezug genommen.

```
Eine unbillige Benachteiligung eines Wohnungseigentümers setzt voraus, dass die beabsichtigte Maßnahme bei wertender Betrachtung und in Abwägung mit den mit der baulichen Veränderung verfolgten Vorteilen einem verständigen Wohnungseigentümer in zumutbarer Weise nicht abverlangt werden dürfte (Fortführung von Senat, Urteil vom 15. Mai 2020 - V ZR 64/19, NJW-RR 2020, 1022 Rn. 14).
```

### `vzr244-rn8` — Rn. 8 (a)

**Kontext:** Beschlussersetzungsklage (§ 44 Abs. 1 Satz 2): Anspruch auf Grundlagenbeschluss (das 'Ob') genügt; das 'Wie' bleibt der Gemeinschaft vorbehalten.

```
Die Beschlussersetzungsklage gemäß § 44 Abs. 1 Satz 2 WEG ist begründet, wenn der klagende Wohnungseigentümer zum Zeitpunkt der letzten mündlichen Tatsachenverhandlung einen Anspruch auf den seinem Rechtsschutzziel entsprechenden Beschluss hat, weil nur eine Beschlussfassung ordnungsmäßiger Verwaltung entspricht. Das erfordert nicht, dass ein Anspruch auf Durchführung einer mit der Klage konkret verlangten Maßnahme besteht. Es ist regelmäßig ausreichend, wenn die Voraussetzungen für die Ersetzung eines so genannten Grundlagenbeschlusses vorliegen, mit dem zunächst nur über das „Ob“ der Maßnahme entschieden werden soll, während das „Wie“ der Ausgestaltung durch die Wohnungseigentümer vorbehalten bleibt (vgl. zum Ganzen Senat, Urteil vom 16. September 2022 - V ZR 69/21, NJW 2023, 63 Rn. 8 f.).
```

### `vzr244-rn18` — Rn. 18 (a)

**Kontext:** Schlüssel-Leitsatzstelle (Rn. 18): Personenaufzug dient § 20 Abs. 2 Satz 1 Nr. 1, auch wenn der Verlangende selbst nicht auf die Maßnahme angewiesen ist; persönliche Gehbehinderung der Kläger 'unerheblich' (München: nicht gehbehinderte Kläger, Außenaufzug Hinterhaus).

```
Dem Gebrauch durch Menschen mit Behinderungen dienen alle baulichen Veränderungen, die für die Nutzung durch körperlich oder geistig eingeschränkte Personen erforderlich oder auch nur förderlich sind. Dafür ist es ohne Belang, ob und in welchem Umfang der Wohnungseigentümer oder einer seiner Angehörigen auf die Maßnahme angewiesen ist (vgl. BT-Drucks. 19/18791 S. 63). Das Gesetz trägt mit der Privilegierung der in § 20 Abs. 2 Satz 1 WEG aufgeführten Veränderungen der Anlage einem gesamtgesellschaftlichen Bedürfnis Rechnung und dient nicht nur dem besonderen Interesse des einzelnen Wohnungseigentümers (vgl. Lehmann-Richter/Wobst, WEG-Reform 2020, Rn. 967). Hiervon ausgehend legt das Berufungsgericht seiner Entscheidung zutreffend und von der Revision unbeanstandet zugrunde, dass die Errichtung eines Personenaufzugs für das Hinterhaus den Zugang zu den dort gelegenen Einheiten für körperlich eingeschränkte Personen jedenfalls erleichtert. Dass die Kläger nach den für den Senat nach § 559 Abs. 1 ZPO maßgeblichen Feststellungen des Berufungsgerichts selbst nicht gehbehindert sind, ist unerheblich.
```

### `vzr244-rn15` — Rn. 15 (1)

**Kontext:** Kosten-/Nutzungslogik: § 21 Abs. 1 Satz 1 (Kosten beim Verlangenden) und Satz 2 (Nutzungen nur ihm, § 100 BGB); Reformziel: Beschlussfassung mit ausschließlicher Nutzungsbefugnis möglich.

```
Die Zuweisung einer ausschließlichen Nutzungsbefugnis ist nunmehr regelmäßige Folge eines seit dem 1. Dezember 2020 gefassten Beschlusses über bauliche Veränderungen nach § 20 Abs. 1 WEG. Dies ergibt sich aus § 21 WEG und den in dieser Vorschrift enthaltenen Regelungen über die Kosten und Nutzungen bei baulichen Veränderungen. Wird einem Wohnungseigentümer eine bauliche Veränderung gestattet oder diese auf sein Verlangen nach § 20 Abs. 2 WEG durch die GdWE durchgeführt, hat er gemäß § 21 Abs. 1 Satz 1 WEG die Kosten allein zu tragen, und nur ihm gebühren nach § 21 Abs. 1 Satz 2 WEG die Nutzungen (§ 100 BGB), sofern ein ausschließlicher Gebrauch des baulich veränderten Gemeinschaftseigentums möglich ist (vgl. dazu BT-Drucks. 19/18791 S. 67; Beispiele bei Greiner, Wohnungseigentumsrecht, § 4 Rn. 71 f.). In den übrigen Fällen haben regelmäßig allein diejenigen Wohnungseigentümer die Kosten einer baulichen Veränderung zu tragen, die sie beschlossen haben (§ 21 Abs. 3 Satz 1 WEG); nur ihnen gebühren dann nach § 21 Abs. 3 Satz 2 WEG auch die Nutzungen. In diesen Regelungen kommt zum Ausdruck, dass mit der Reform des Wohnungseigentumsrechts eine Beschlussfassung über bauliche Veränderungen gerade auch dann ermöglicht werden sollte, wenn dies eine ausschließliche Nutzungsbefugnis zur Folge hat; hierin bestand ein erklärtes Ziel der Reform des Wohnungseigentumsrechts (vgl. Abschlussbericht der Bund-Länder-Arbeitsgruppe zur Reform des Wohnungseigentumsgesetzes, ZWE 2019, 429, 445).
```

### `vzr244-rn24` — Rn. 24 (3)

**Kontext:** Kosten (§ 21 Abs. 1 Satz 1) stehen dem § 20-Abs.-2-Anspruch nicht entgegen; auch Folgekosten (Versicherung, Wartung, Kontrolle) entfallen Angemessenheit grds. nicht.

```
Die Kosten der baulichen Veränderung sind dagegen grundsätzlich ohne Bedeutung für das Bestehen eines Anspruchs nach § 20 Abs. 2 Satz 1 WEG; sie sind gemäß § 21 Abs. 1 Satz 1 WEG von dem verlangenden Wohnungseigentümer zu tragen und können daher die Angemessenheit der Maßnahme nicht entfallen lassen.
```

### `vzr244-rn33` — Rn. 33 (Ausklang)

**Kontext:** Öffentlich-rechtliche Vorgaben: bauordnungsrechtliche Unzulässigkeit → Verlangen widerspricht regelmäßig ordnungsmäßiger Verwaltung; Anspruch kann ohne Angemessenheitsprüfung ausscheiden (Bauordnungsrecht/§ 275-Kontext für Treppenlift-Genehmigungen).

```
Ist ein unter § 20 Abs. 2 Satz 1 WEG fallendes Verlangen eines Wohnungseigentümers etwa bauordnungsrechtlich unzulässig, widerspricht dieses regelmäßig auch ordnungsmäßiger Verwaltung. Ein Anspruch auf Beschlussfassung kann dann bereits aus diesem Grund ausgeschlossen sein, ohne dass es auf die Angemessenheit der baulichen Veränderung ankommt (vgl. auch Bärmann/Dötsch, WEG, 15. Aufl., § 20 Rn. 201, 361).
```

### `vzr244-rn34` — Rn. 34 (2)

**Kontext:** Grundlagenbeschluss vs. Ausführung (§ 20 Abs. 2 Satz 2): öffentlich-rechtliche Einhaltung darf der späteren Durchführungsbeschlussfassung vorbehalten bleiben, jedenfalls bei umfangreichen Maßnahmen wie einem Personenaufzug (Fachplanung).

```
Im Rahmen von § 20 Abs. 2 Satz 1 WEG ist die Einhaltung der das Gemeinschaftseigentum betreffenden öffentlich-rechtlichen Vorschriften allerdings regelmäßig (noch) nicht von Bedeutung. Zwar ist eine Beschlussersetzungsklage gemäß § 44 Abs. 1 Satz 2 WEG nur dann begründet, wenn ein Anspruch auf den begehrten Beschluss besteht, weil nur eine Beschlussfassung ordnungsmäßiger Verwaltung entspricht (vgl. oben Rn. 8). Das Berufungsgericht nimmt aber zutreffend an, dass es für den Anspruch nach § 20 Abs. 2 Satz 1 WEG regelmäßig ausreichend ist, die Einhaltung öffentlich-rechtlicher Vorschriften der späteren Prüfung im Zusammenhang mit der Beschlussfassung über die Durchführung der Maßnahme (§ 20 Abs. 2 Satz 2 WEG) vorzubehalten. Dies gilt jedenfalls dann, wenn es sich um umfangreiche bauliche Veränderungen wie die Errichtung eines Personenaufzugs handelt und - wie hier - zunächst die Ersetzung eines Grundlagenbeschlusses gemäß § 20 Abs. 2 Satz 1 WEG begehrt wird. Denn die Entscheidung der Wohnungseigentümer über die Art und Weise der Bauausführung und der baulichen Details erfordert insbesondere bei genehmigungspflichtigen Bauvorhaben eine konkrete Fachplanung (z.B. Entwurfs- und Genehmigungsplanung; vgl. etwa Bärmann/Dötsch, WEG, 15. Aufl., § 20 Rn. 191).
```

### `vzr244-rn35` — Rn. 35 (3)

**Kontext:** Absolute Grenze: Grundlagenbeschluss unzulässig, wenn Unmöglichkeit i.S.d. § 275 Abs. 1 BGB von vornherein feststeht (in jedem Fall/bei jeder Ausführung gegen öffentlich-rechtliche Vorschriften); hier von Beklagter nicht dargelegt.

```
Ein Grundlagenbeschluss darf allerdings dann nicht gefasst oder ersetzt werden, wenn ausnahmsweise bereits bei der Entscheidung, ob die bauliche Veränderung dem Grunde nach durchgeführt werden soll, feststeht, dass das Begehren in jedem Fall und bei jeder in Betracht kommenden Ausführung gegen öffentlich-rechtliche Vorschriften verstößt. Dann wäre der Anspruch nach § 20 Abs. 2 Satz 1 WEG nämlich auf eine (rechtlich) unmögliche Leistung im Sinne des § 275 Abs. 1 BGB gerichtet. Dass es sich hier so verhält, hat die für das Vorliegen einer Unmöglichkeit darlegungs- und beweisbelastete Beklagte aber nicht dargelegt.
```


## 6) BGH, Urteil vom 09.02.2024 – V ZR 33/23 (Terrasse/Rampe, Köln) – offizielles BGH-PDF

- **URL:** https://www.bundesgerichtshof.de/SharedDocs/Entscheidungen/DE/Zivilsenate/V_ZS/2023/V_ZR__33-23.pdf?__blob=publicationFile&v=1
- **Abgerufen (fetch date):** 2026-11-23
- **Rohdateien:** `raw/vzr-33-23.pdf + raw/vzr-33-23.txt + raw/vzr-33-23.flat.txt`
- **Bereinigung (cleaning steps):** PDF (offizielles BGH-Dokument, %PDF-1.5, 16 Seiten) mit pdftotext -layout extrahiert; Seitenzahlen ('- 2 -') und ECLI-Zeilen entfernt; Zeilenumbruch-Trennstriche aufgelöst (unbil‑/lig → unbillig); erhaltene Komposita-Bindestriche (Bund-Länder-Arbeitsgruppe) beibehalten; Whitespace kollabiert.

### `vzr33-ls-a` — Leitsatz a)

**Kontext:** Anfechtungsklage gegen einen § 20-Abs.-2-Stattgebungsbeschluss: nur prüfbar sind § 20 Abs. 4-Grenzen und allgemeine Beschlussmängel; NICHT die Anspruchsvoraussetzungen des § 20 Abs. 2 im Einzelnen.

```
a) Beschließen die Wohnungseigentümer die Durchführung oder Gestattung einer baulichen Veränderung, die ein Wohnungseigentümer unter Berufung auf § 20 Abs. 2 Satz 1 WEG verlangt (hier: § 20 Abs. 2 Satz 1 Nr. 1 WEG), ist der Beschluss auf die Klage eines anderen Wohnungseigentümers nur für ungültig zu erklären, wenn die beschlossene Maßnahme entgegen § 20 Abs. 4 Halbs. 1 WEG die Wohnanlage grundlegend umgestaltet bzw. einen Wohnungseigentümer ohne sein Einverständnis gegenüber anderen unbillig benachteiligt oder der Beschluss an einem anderen (allgemeinen) Beschlussmangel leidet.
```

### `vzr33-ls-b` — Leitsatz b)

**Kontext:** Die Anspruchsvoraussetzungen (inkl. Angemessenheit) sind nur relevant bei Negativbeschluss (Anfechtungs-/Beschlussersetzungsklage des Verlangenden).

```
b) Ob die Anspruchsvoraussetzungen des § 20 Abs. 2 WEG im Einzelnen vorliegen und ob die bauliche Veränderung insbesondere angemessen ist, ist bei einer Anfechtungsklage gegen einen dem Verlangen eines Eigentümers stattgebenden Beschluss ohne Bedeutung. Auf diese Voraussetzungen kommt es nur an, wenn der Individualanspruch des Wohnungseigentümers abgelehnt worden ist und sich dieser mit einer Anfechtungsklage gegen den Negativbeschluss wendet und/oder den Anspruch mit der Beschlussersetzungsklage weiterverfolgt.
```

### `vzr33-ls-c` — Leitsatz c)

**Kontext:** Regel-Ausnahme-Verhältnis: privilegierte Maßnahmen (§ 20 Abs. 2 Satz 1) sind typischerweise keine grundlegende Umgestaltung i.S.d. § 20 Abs. 4 Halbs. 1 Alt. 1.

```
c) Eine grundlegende Umgestaltung der Wohnanlage ist bei einer Maßnahme, die der Verwirklichung eines Zweckes i.S.d. § 20 Abs. 2 Satz 1 WEG dient, zumindest typischerweise nicht anzunehmen; der von dem Gesetzgeber im gesamtgesellschaftlichen Interesse erstrebten Privilegierung bestimmter Kategorien von Maßnahmen ist bei der Prüfung, ob eine grundlegende Umgestaltung vorliegt, im Sinne eines Regel-Ausnahme-Verhältnisses Rechnung zu tragen.
```

### `vzr33-rn15` — Rn. 15 (bb)

**Kontext:** Begriffsabgrenzung: 'grundlegende Umgestaltung' (§ 20 Abs. 4) ist enger als 'Änderung der Eigenart' (§ 22 Abs. 2 Satz 1 WEG aF) – wichtig für die Abgrenzung Altrecht/Neurecht im Artikel.

```
bb) In diesem Rahmen ist die Beurteilung des Berufungsgerichts zu beanstanden. Es sieht zwar richtig, dass nicht jede bauliche Veränderung, die nach § 22 Abs. 2 Satz 1 WEG aF die Eigenart der Wohnanlage änderte, auch zu einer grundlegenden Umgestaltung im Sinne des neuen § 20 Abs. 4 Halbs. 1 Alt. 1 WEG führt. Der Begriff der grundlegenden Umgestaltung ist vielmehr enger zu verstehen als der Begriff der Änderung der Eigenart im bisherigen Recht (vgl. BT-Drucks. 19/18791 S. 66).
```

### `vzr33-rn18` — Rn. 18

**Kontext:** Outcome Terrasse/Barrierefreiheit: BGH hebt Berufungsurteil auf, weist Anfechtungsklage ab; der Gestattungsbeschluss ist weder anfechtbar noch nichtig.

```
Das angefochtene Urteil kann danach keinen Bestand haben und ist aufzuheben (§ 562 Abs. 1 ZPO). Der Senat kann in der Sache selbst entscheiden, weil es keiner weiteren Feststellungen bedarf und die Sache zur Entscheidung reif ist (§ 563 Abs. 3 ZPO). Die Klage ist abzuweisen. Der Beschluss weist weder die von den Klägern geltend gemachten Anfechtungsgründe auf noch ist er nichtig.
```

### `vzr33-rn19` — Rn. 19

**Kontext:** Subsumtion Terrasse/Rampe: Barrierefreiheit (§ 20 Abs. 2 Satz 1 Nr. 1) → nur außergewöhnliche Umstände könnten grundlegende Umgestaltung begründen; 65-cm-Terrasse + Rampe = untergeordneter Anbau, terrassenrechtlich durch Teilungserklärung gedeckt.

```
Eine grundlegende Umgestaltung i.S.d. § 20 Abs. 4 Halbs. 1 Alt. 1 WEG ist mit der beschlossenen baulichen Veränderung nicht verbunden. Da die Maßnahme der Verwirklichung des in § 20 Abs. 2 Satz 1 Nr. 1 WEG aufgeführten Zwecks der Barrierefreiheit dient, müssten außergewöhnliche Umstände vorliegen, die die Annahme einer grundlegenden Umgestaltung rechtfertigten. Hieran fehlt es. Gestattet wird der Streithelferin lediglich die Errichtung eines untergeordneten Anbaus an ein bestehendes Gebäude einer Mehrhausanlage, wobei die Errichtung einer Terrasse schon nach der Teilungserklärung erlaubt ist.
```

### `vzr33-rn22` — Rn. 22 (b)

**Kontext:** Keine unbillige Benachteiligung (§ 20 Abs. 4 Halbs. 1 Alt. 2): fehlende Vergleichsmöglichkeiten der Obergeschoss-Eigentümer genügen nicht; Ungleichbehandlung durch Sondernutzungsrechte der TE angelegt.

```
b) Diese Voraussetzungen liegen auf der Grundlage der Feststellungen des Berufungsgerichts nicht vor. Der Umstand, dass die Eigentümer der im Obergeschoss gelegenen Wohnungen nicht die Möglichkeit haben, ihre Wohnungen in vergleichbarer Weise aufzuwerten, vermag eine unbillige Benachteiligung nicht zu begründen. Unabhängig davon, dass sich eine unbillige Benachteiligung grundsätzlich nicht daraus herleiten lässt, dass andere Wohnungseigentümer Vorteile erhalten, ist die Ungleichbehandlung nämlich - wie das Berufungsgericht in der Sache selbst erkennt - durch die Begründung von Sondernutzungsrechten allein zugunsten der Einheiten im Erdgeschoss bereits in der Teilungserklärung angelegt.
```


## 7) BGH Pressemitteilung Nr. 026/2024 vom 09.02.2024

- **URL:** https://www.bundesgerichtshof.de/SharedDocs/Pressemitteilungen/DE/2024/2024026.html
- **Abgerufen (fetch date):** 2026-11-23
- **Rohdateien:** `raw/pm-026-2024.html + raw/pm-026-2024.txt`
- **Bereinigung (cleaning steps):** UTF-8 HTML; Tags entfernt; Entities decodiert; Soft-Hyphen (U+00AD, 'Kon­takt') entfernt; geschützte Leerzeichen → Leerzeichen; Whitespace kollabiert.

### `pm-026-intro` — PM, Einleitung

**Kontext:** PM-Rahmen: zwei Urteile vom 09.02.2024 zur Barrierereduzierung – Personenaufzug (V ZR 244/22) und 65 cm erhöhte Terrasse nebst Zufahrtsrampe (V ZR 33/23).

```
Der unter anderem für das Wohnungseigentumsrecht zuständige V. Zivilsenat des Bundesgerichtshofs hat heute auf der Grundlage des im Jahr 2020 reformierten Wohnungseigentumsrechts in zwei Verfahren über die Voraussetzungen und Grenzen baulicher Veränderungen des Gemeinschaftseigentums entschieden, die von einzelnen Wohnungseigentümern als Maßnahmen zur Barrierereduzierung (Errichtung eines Personenaufzugs bzw. Errichtung einer 65 Zentimeter erhöhten Terrasse nebst Zufahrtsrampe) verlangt wurden.
```

### `pm-026-mehrheit` — PM, V ZR 33/23

**Kontext:** Kernaussage: Mehrheit darf privilegierte Maßnahme gestatten, obwohl sie die § 20-Abs.-2-Voraussetzungen nicht als gegeben ansieht oder Zweifel hat.

```
Infolgedessen dürfen die Wohnungseigentümer eine bauliche Veränderung auch dann durch Mehrheitsbeschluss gestatten, wenn sie die in § 20 Abs. 2 Satz 1 WEG geregelten Anspruchsvoraussetzungen im Einzelnen nicht als gegeben ansehen oder jedenfalls Zweifel hieran hegen.
```

### `pm-026-einfmehr` — PM, V ZR 33/23

**Kontext:** Einfache Stimmenmehrheit nach § 20 Abs. 1 (statt 3/4-Mehrheit nach § 22 Abs. 2 WEG aF) – Kernelement der WEMoG-Reform für den Artikel.

```
Nunmehr können die Wohnungseigentümer nach § 20 Abs. 1 WEG im Gegensatz zu der Regelung in § 22 WEG aF Maßnahmen, die über die ordnungsmäßige Erhaltung des gemeinschaftlichen Eigentums hinausgehen (bauliche Veränderungen), jeweils mit einfacher Stimmenmehrheit beschließen.
```

### `pm-026-kosten` — PM, V ZR 244/22

**Kontext:** PM-Fassung der Kostenaussage (§ 21 Abs. 1 Satz 1): hohe Kosten verhindern den Anspruch nicht, weil der Verlangende sie selbst trägt.

```
Die Kosten der baulichen Veränderung sind für das Bestehen eines Anspruchs nach § 20 Abs. 2 Satz 1 WEG grundsätzlich ohne Bedeutung, da sie gemäß § 21 Abs. 1 Satz 1 WEG von dem verlangenden Wohnungseigentümer zu tragen sind.
```

### `pm-026-umgestaltung` — PM, beide Verfahrensteile

**Kontext:** PM-Kernaussage: keine grundlegende Umgestaltung bei privilegierten Maßnahmen (in beiden Verfahrensteilen der PM in gleicher Formulierung) + Regel-Ausnahme-Verhältnis.

```
Nach nunmehr geltendem Recht ist bei einer Maßnahme, die der Verwirklichung eines Zweckes i.S.d. § 20 Abs. 2 Satz 1 WEG dient, eine grundlegende Umgestaltung der Wohnanlage zumindest typischerweise nicht anzunehmen. Der von dem Gesetzgeber im gesamtgesellschaftlichen Interesse erstrebten Privilegierung bestimmter Kategorien von Maßnahmen - unter anderem zur Förderung der Barrierefreiheit - ist bei der Prüfung, ob eine grundlegende Umgestaltung vorliegt, im Sinne eines Regel-Ausnahme-Verhältnisses Rechnung zu tragen.
```

### `pm-026-outcome33` — PM, V ZR 33/23

**Kontext:** Outcome V ZR 33/23 laut PM: Berufungsurteil aufgehoben, Anfechtungsklage abgewiesen (Gestattungsbeschluss für Terrasse/Rampe hält stand).

```
Entscheidung des Bundesgerichtshofs: Die Revision hat Erfolg gehabt. Der Bundesgerichtshof hat das Berufungsurteil aufgehoben und die Anfechtungsklage abgewiesen.
```

### `pm-026-aufzug` — PM, V ZR 244/22

**Kontext:** Personenaufzug = angemessene bauliche Veränderung i.S.d. § 20 Abs. 2 Satz 1 Nr. 1 – direkte Analogie für Treppenlift-Artikel (Aufzug/Hebetechnik als privilegierte Barrierefreiheitsmaßnahme).

```
Die von den Klägern erstrebte Errichtung eines Personenaufzugs stellt eine angemessene bauliche Veränderung dar, die dem Gebrauch durch Menschen mit Behinderungen dient (§ 20 Abs. 2 Satz 1 Nr. 1 WEG).
```
