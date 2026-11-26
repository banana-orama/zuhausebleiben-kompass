# Region-Screen Hessen (2026-11-26) — Belege Wohnraumanpassungs-Förderung (NUR Recherche, kein Content)

Subagent-Lauf: Offizielle Primärquellen für Wohnraumanpassungs-/Barrierereduzierungs-Förderung in Hessen.
Schema wie NRW/Bayern/Sachsen/BW: Weg 1 Pflegekasse (bundesweit, keine Beträge auf der Region-Seite),
Weg 2 Landesprogramm, Weg 3 Eingliederungshilfe, Weg 4 KfW-Stand. Evidenz:
`research/evidence/region-screen-261126/hessen/` (raw + Extrakt je Quelle, PDFs via pdftotext).
Ledger: `research/region-screen-261126-hessen-ledger.json` (20 Quellen, 22 abgerufene URLs).
Maschineller Verbatim-Check: `research/check_quotes_region_screen_261126_hessen.py` —
**155/155 PASS (110 Zitate, 19 Needle-Checks inkl. Absenzen, 26 EGH-Entities), 0 FAIL**
(Normalisierung: U+00AD-Strip, Zeilenumbruch-Hyphens, Tausendertrennzeichen „4 180"/„4.180");
Ausgabe-Protokoll: `research/evidence/region-screen-261126/hessen/QUOTES.md`.

## VERDICT

**Belegbar.** Hessen trägt die fünfte Region-Seite nach dem 4-Wege-Schema: Weg 2 ist ein amtlich
vollständig dokumentiertes, laufendes Landesprogramm (Kostenzuschuss „Behindertengerechter Umbau von
Wohneigentum" über die WIBank, Richtlinie + Produktseite + Ministeriums-Seite + Land-Fachstelle alle
live gezogen), Weg 3 hat mit LWV Hessen sogar eine Leistungsseite mit expliziter Treppenlift-Nennung.

## Weg 2 — Landesprogramm (Kernquelle)

**Programm:** „Behindertengerechter Umbau von Wohneigentum" — *Richtlinie des Landes Hessen zur
Förderung des behindertengerechten Umbaus von selbstgenutztem Wohneigentum* (Fassung
Wiesbaden, den 14.12.2021/01.09.2023, Druck Dezember 2024; Rechtsgrundlage HWoFG 13.12.2012, zuletzt
geändert 11.12.2020). Herausgeber: Hessisches Ministerium für Wirtschaft, Energie, Verkehr, Wohnen und
ländlichen Raum (HMWEVW). Bewilligungsbehörde: **Wirtschafts- und Infrastrukturbank Hessen (WIBank)**,
Kaiserleistr. 29-35, 63067 Offenbach am Main.

**Träger-Struktur empirisch geklärt (IB/Helaba):** „Die WIBank ist die Förderbank des Landes Hessen."
/ „Die WIBank entstand im Jahr 2009 aus der Zusammenführung der Investitionsbank Hessen und der
LTH – Bank für Infrastruktur." (wibank-diewibank.txt) — Hessens Landesförderbank ist also die WIBank
(Rechtsnachfolgerin der IB), die unter Helaba-Konzern-Vorgaben operiert („konzernweiten Nachhaltigkeits-
und Risikovorgaben der Helaba"); Helaba selbst ist keine Bewilligungsbehörde des Programms.

**Art:** Zuschuss, kein Darlehen — „Die Förderung (Zuwendung) wird als Projektförderung im Wege der
Anteilfinanzierung als nicht rückzahlbarer Zuschuss in Höhe von bis zu 50 Prozent der zuwendungsfähigen
Ausgaben gewährt." Konditionen verbatim (Richtlinie + WIBank-Produktseite):
- „Förderfähig sind Ausgaben in Höhe von bis zu 30.000 Euro je Wohneinheit, auch wenn die Ausgaben der
  baulichen Maßnahmen insgesamt höher sind. Dies entspricht einem Zuschuss in Höhe von maximal
  15.000 Euro je Wohneinheit."
- Höchstbeträge: „• Bad: Um-/Einbau 5.500 Euro · • Küche: Um-/Einbau 5.500 Euro · • Lift-/Aufzugeinbau
  6.500 Euro · • Alle anderen förderungsfähigen Einzelmaßnahmen je 3.000 Euro"
- „Maßnahmen mit Ausgaben in Höhe von unter 1.500 Euro werden nicht gefördert." / Eigenleistungen
  werden nicht gefördert (beide Quellen).
- „Es wird ein einmaliges Bearbeitungsentgelt von 1 Prozent des bewilligten Zuschusses, mindestens
  jedoch 25 Euro." (§ 13 HWoFG)
- „Der Zuschuss wird in einer Summe nach Abschluss der Maßnahmen und Vorlage der Schlussabrechnung
  ausgezahlt."
- Normbezug: „Die Maßnahmen sollen nach Möglichkeit den Anforderungen der Norm DIN 18040 Teil 2
  entsprechen." (Produktseite: DIN 18040 Teil 2 „mit und ohne ‚R'-Anforderungen")
- Personenbezug: „Ein Mensch mit Behinderung im Sinne dieser Richtlinie ist eine Person, die einen Grad
  der Behinderung von 50 Prozent oder mehr bzw. eine Einstufung in den Pflegegrad 2 oder höher
  aufweist." (Nachweis: Schwerbehindertenausweis oder Pflegegradnachweis)
- 5-Jahres-Obergrenze (Fachstelle): „Innerhalb von fünf Jahren können auch nur bis zu dieser Höhe
  Zuschüsse pro Wohnung bzw. Antragstellerin oder Antragsteller gewährt werden."

**Status (26.11.2026):** offen, kein Antragsstopp, KEINE offizielle Wartezeit-Botschaft (anders als
L-Bank BW). Aber: kein Rechtsanspruch („Ein Rechtsanspruch auf Gewährung der Förderung besteht nicht."),
jährliches Fördermittelkontingent je Wohnungsbauförderstelle, und bei knappem Kontingent „ist eine
Auswahl nach sozialer Dringlichkeit vorzunehmen. Hierbei werden insbesondere der Grad der Behinderung
und weitere soziale Kriterien (z. B. finanzielle Situation, zeitliche Dringlichkeit) berücksichtigt."
Programmvolumen 2025: „4,0 Mio. Euro behindertengerechter Umbau bestehender Wohnungen" (HMWEVW-Bilanz
auf der Ministeriums-Seite). Die PM „Hessen verbessert die soziale Wohnraumförderung" (01.07.2026)
ändert nur Neubau/Studierende/Modernisierung — behindertengerechter Umbau wird nicht erwähnt,
Richtlinie unverändert.

**Treppenlift-Nennung auf Produktseite (Count auf gestripptem Text):** **0×** (wibank-umbau.txt,
gleicher Count in der Richtlinie: 0×). Benannt sind „Treppenschrägaufzug" (1×, als Aufzugsbeispiel:
„Einbau von geeigneten Aufzügen (z.B. Treppenschrägaufzug), Küchen, Toilettenräumen und Bädern")
und der Höchstbetrag „Lift-/Aufzugseinbau 6.500 Euro". Richtlinie zusätzlich: „Plattformlift" (1×)
und Bad doppelt belegt: „barrierefreier Badumbau" + „barrierereduzierender Badumbau, z. B. Austausch
der Badewanne gegen eine Dusche". → Region-Seite: Treppenlift über die Lift-/Aufzugeinbau-Zeile
begründen, kein erfundenes „Treppenlift"-Zitat des Landesprogramms.

**Antragsweg:** „Bitte stellen Sie den Antrag ... bei der Wohnungsbauförderstelle des Kreises oder der
kreisfreien Stadt, in der der umzubauende Wohnraum liegt." (WIBank-Seite) — Richtlinie präzisiert:
„beim Magistrat der kreisfreien Stadt, beim Magistrat von kreisangehörigen Städten mit mehr als
50.000 Einwohnerinnen und Einwohnern oder beim Kreisausschuss des Landkreises"; die Stelle prüft und
„leitet ... den Antrag an die WIBank weiter"; „Die Bewilligungsbehörde erteilt die Förderzusage durch
einen Zuwendungsbescheid." Stellenliste: WIBank-PDF (Quelle 18). **Vorhabensbeginn streng:** „Es
werden nur Baumaßnahmen gefördert, für die vor Bewilligung ... noch keine Aufträge erteilt wurden und
mit deren Arbeiten nicht begonnen wurde." + „Als Vorhabenbeginn ist grundsätzlich der Abschluss eines
der Ausführung zuzurechnenden Lieferungs- und Leistungsvertrages zu werten" + Refinanzierungsverbot.

**Einkommensgrenzen:** NICHT belegbar — es gibt keine: „Einkommen" kommt **0×** in der Richtlinie vor
(Absenz-Needle maschinell geprüft). Bei Mittelknappheit wirkt stattdessen die soziale Dringlichkeits-
auswahl (finanzielle Situation als Kriterium). Kontrast zu BW (Bezugsgröße 71.000 €). Region-Seite:
als Abwesenheit formulieren, nicht als „geprüfte Grenze".

**Kumulation (wichtig):** „Zuschüsse anderer Stellen (zum Beispiel Pflegekasse, Rehabilitationsträger,
Stiftungen, Versicherungen) werden auf die zuwendungsfähigen Ausgaben angerechnet (Teil II Nr. 13)." +
„... wird der Zuschuss des Landes durch Anrechnung auf die zuwendungsfähigen Ausgaben reduziert
(Teil I Nr. 5)." → keine Addier-Beispiele mit Pflegekasse auf der Region-Seite (anders als KfW-159-
Kombinausnahme, die getrennt gilt).

## Weg 3 — Eingliederungshilfe

**Träger-Struktur:** Hessen-Spezifik: „Für Leistungen nach Abschluss der Schulausbildung ist der
Landeswohlfahrtverband Hessen zuständig." (Verwaltungsportal-Leistungsseite, HMSI-Freigabe 06.03.2026;
vor Schulabschluss Landkreis/kreisfreie Stadt). „Der LWV Hessen ist ein Zusammenschluss der hessischen
Landkreise und kreisfreien Städte mit sozialen Aufgaben." (LWV). Örtliche Organisationsübersicht
(HMSI, Stand August 2022): **21 Landkreise + 5 kreisfreie Städte = 26 Organisationseinheiten** —
maschinell als Entities-Check verifiziert (26/26 Namen im Evidenztext; „Hessen hat 26" bestätigt).
§ 113/77 SGB IX-Route fresh (gesetze-im-internet): „Leistungen zur Sozialen Teilhabe sind insbesondere
1. Leistungen für Wohnraum," (§ 113) / § 77 Wortlaut (Beschaffung, Umbau, Ausstattung, Erhaltung).
Handlungsgrundlage der Leistungsseite: „§§ 90 fortfolgende Sozialgesetzbuch Neuntes Buch (Teil 2,
SGB IX)".

**Offizielle Leistungsseite mit Treppenlift-Nennung:** LWV Hessen „Leistungen für Wohnraum" —
„Dies kann z. B. ein behindertengerechter Bad- und/oder Küchenumbau oder der Einbau eines Treppenlifts
sein." (Treppenlift 1× auf gestripptem Text). Subsidiarität: „Bevor Leistungen der Eingliederungshilfe
bewilligt werden können, ist vorrangig zu klären, ob andere Personen oder Leistungsträger (zum Beispiel
Vermieter, Pflegekasse, KfW-Förderbank oder Wirtschafts- und Infrastrukturbank Hessen) die Finanzierung
der Wohnraum-Anpassung übernehmen." Kosten des Verfahrens: „Es fallen keine Kosten an."; Beteiligung:
„... grundsätzlich einen Beitrag aus Ihrem Einkommen sowie aus Ihrem Vermögen, sofern es eine
festgesetzte Grenze überschreitet, zahlen." Verfahrensfristen (Verwaltungsportal): Weiterleitung 2
Wochen, Entscheidung 3 Wochen ohne / 2 Wochen nach Gutachteneingang.

## Weg 1 — Pflegekasse (Bundesweit, wie gehabt KEINE Beträge aufs Region-Layout)

§ 40 SGB XI fresh („4 180"/„16 720" mit geschützten Tausendertrennzeichen, 3/5-Wochen-Frist,
Genehmigungsfiktion) + Hessen-Leistungsseite des Verwaltungsportals (BMG-Freigabe 04.09.2026) mit
expliziter Nennung: „Dazu gehören zum Beispiel das Einbauen eines Treppenlifts, verbreiterte Türen und
Schwellen statt Stufen." — Treppenlift 3× auf gestripptem Text. NUR Kontext für die Region-Seite.

## Weg 4 — KfW-Stand (26.11.2026, frisch gezogen)

455-B weiter gestoppt: „Diesen Zuschuss können Sie nicht mehr beantragen." / „Wegen der hohen Nachfrage
sind die Fördermittel für Maßnahmen zur Barrierereduzierung bereits ausgeschöpft." / „Sollten im Jahr
2027 erneut Bundesmittel für barrierereduzierende Maßnahmen bereitgestellt werden, wird eine
Antragstellung wieder möglich sein." Kredit 159 läuft: „Kreditbetrag: bis zu 50.000 Euro je
Wohneinheit", „Treppenlifte, Senkrecht-, Hebe- oder Plattformlifte installieren" (Treppenlift 2× +
Treppenlifte 1×) + Kombi-Ausnahme wörtlich („z. B. Treppenlift" neben Pflegekassen-Badumbau). Zins-
Platzhalter „-,-- % p.a." (2×) — keine Zinszahlen übernehmen.

## Beratung — Pflegestützpunkte

Land-Hessen-Portal „Pflege in Hessen": „In Hessen gibt es 26 Pflegestützpunkte - in jedem Landkreis
und in jeder kreisfreien Stadt einen." / „Die Kranken- und Pflegekassen betreiben deshalb gemeinsam
mit kommunalen Trägern vor Ort so genannte Pflegestützpunkte." / „neutral zum Thema Pflege zu
informieren, zu beraten und zu vermitteln" / „... für die gesetzlich Versicherten und ihre Angehörigen
kostenlos". Ministeriums-Seite (HMSFSG, familie.hessen.de): „Die Beratung ist kostenlos, neutral und
vertraulich." (© Land Hessen-Portale.)

## Kommunales Treppenlift-Beispiel — GEKENNZEICHNET (Einzelfall, nicht flächendeckend)

**Kein eigenes kommunales Treppenlift-Programm gefunden** (anders als Friedrichshafen in BW). Belegbar
ist nur kommunale *Vermittlung* des Landesprogramms: Stadt Bad Homburg (Pressemitteilung 07.07.2026,
Wohnungsamt als Antragsstelle) mit expliziter Zeile „• Treppenlift oder Aufzug: bis zu 6.500 Euro"
(Treppenlift 1×) — die Stadt widerspiegelt die Landes-Höchstbeträge, stellt keine eigenen Mittel bereit
und nennt kein eigenes Budget. Nur mit dieser Kennzeichnung verwendbar; als echtes kommunales Beispiel
→ offene Frage unten.

## VERWORFENE Kandidaten (mit Begründung)

1. **Verwaltungsportal-Leistungsseite KfW 455** (B100019_101338702): beschreibt den 455-Zuschuss ohne
   den seit KfW geltenden Antragsstopp („nicht mehr beantragen" 0×) — veraltet; Status nur aus kfw.de.
   Nur Antragsweg-Kontext im Ledger (Quelle 20).
2. **Verwaltungsportal „Soziale Wohnraumförderung"** (L100001_8960248): HTTP 404 — Antragsweg über
   WIBank-Produktseite + Richtlinie belegt, Seite verworfen.
3. **HMWEVW-Richtlinien Mietwohnungsbau / selbstgenutztes Wohneigentum / Erwerb Belegungsrechte:**
   betreffen Vermieter-/Neubau-/Erwerbsprogramme, nicht den barrierefreien Selbstnutzer-Umbau im
   Bestand; nicht relevant für das Schema.
4. **„Modernisierung zum Passivhaus im Bestand" (WIBank/HEG):** energetisches Programm, keine
   Barrierereduzierung — verworfen.
5. **Werra-Meißner-Kreis-Wohnungsbauförderungsseite:** kommunale Wiedergabe des Landesprogramms
   (inkl. „Zusatzformular der Wohnbauförderstelle") — kommunale Sekundär-Verpackung, nicht als
   Primärbeleg verwendet; Formular-Zweistufen-Workflow daher nur als „unverified" geführt.
6. **Sekundärportale (hiro.de, pflege-panorama.de, treppenlifte-foerderung.de, leadwerke, openpr,
   baufiquadrat, nullbarriere.de, vdek):** Interessenkonflikt-Kontext (Treppenlift-Anbieter/
   Vermittler), nicht als Primärbeleg; zudem widersprüchlich („455-B Antragstopp seit 31.07.2026" —
   Datum nicht amtlich belegt; vdek „33" PSP vs. Land „26").
7. **Wikipedia (WIBank):** nur Kontext; Förderbank-Fakten über wibank.de selbst belegt.

## Offene Fragen / URLs für den Parent (Browser-Render nötig)

1. **frankfurt.de — „Frankfurter Programm zur Modernisierung des Wohnbestandes"** (kommunales
   Beispiel-Kandidat: „ergänzende Maßnahmen zur Barrierefreiheit ... können zusätzlich gefördert
   werden"): Cloudflare-Challenge („Just a moment..."), 403 auf curl und Challenge im Agent-Browser
   nicht überwunden. URL: https://frankfurt.de/themen/planen-bauen-und-wohnen/wohnen/gefoerderte-wohnungen-foerderprogramme/frankfurter-programm-zur-modenisierung-des-wohnbestandes
   → Frage: nennt das Programm Treppenlift/Bad mit Beträgen? (dann echtes kommunales Beispiel, mit
   Frankfurt-Begrenzung kennzeichnen).
2. Existiert irgendwo in Hessen ein **eigenes kommunales Treppenlift-/Umbau-Zuschussprogramm** einer
   Stadt/eines Kreises (analog Friedrichshafen)? Erste Durchsicht (Suche + Landkreis-Seiten) gefunden:
   nein; nur Bad Homburg-Kommunikation des Landesprogramms. Falls Parent weitere Kandidaten prüft:
   Anlaufstellen sind die Wohnungsämter/Wohnungsbauförderstellen der 26 Kreise/kreisfreien Städte.
3. **Antragsvordrucke WIBank** (Excel-/PDF-Antrag + ggf. Förderstellen-Zusatzformular): Dateien
   verlinkt und RAW gesichert, aber inhaltlich nicht geprüft (Felder/Fristen im Formular).
4. **Auslegung Höchstbeträge:** Kombination mehrerer Maßnahmen (z. B. Lift 6.500 € + Bad 5.500 €) im
   selben Antrag innerhalb der 50 %-/15.000-€-Deckel — Richtlinie liest sich als je-Maßnahme-Höchstbetrag
   unter dem Gesamtdeckel; keine kombinierte Beispielrechnung publizieren, solange unbestätigt.

## Evidenz-Bestand (research/evidence/region-screen-261126/hessen/, 26.11.2026)

20 Quellen, alle amtlich bzw. klar gekennzeichnet: wibank.de ×4 (Produktseite, Richtlinie-PDF
[-raw-Extrakt + -layout-Referenz], Förderstellen-PDF, „Förderbank für Hessen") + wirtschaft.hessen.de
×2 (Ministeriums-Seite, PM 01.07.2026) + wohnen-im-alter.hessen.de (Land-Fachstelle) + verwaltungsportal
.hessen.de ×3 (EGH-Leistung, Pflegekasse-Wohnumfeld, KfW-455-Leistung) + soziales.hessen.de (EGH-Organisationsübersicht, 26/26 verifiziert) + lwv-hessen.de (Wohnraum-Leistungsseite, Treppenlift 1×) + gesetze-im-
internet ×3 (§ 113/§ 77 SGB IX, § 40 SGB XI) + pflege-in-hessen.de + familie.hessen.de + kfw.de ×2
(455-B gestoppt, 159 läuft) + bad-homburg.de (gekennzeichnet kommunal). Hinzu: 2 Fehlschlag-Belege
(vp-404-Stub, frankfurt-Cloudflare-HTML) und Fetch-Skripte. Ledger:
`research/region-screen-261126-hessen-ledger.json` — 155/155 Checks PASS.
