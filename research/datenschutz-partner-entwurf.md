# Datenschutz-Amendment-Entwurf: Partnerprogramme / ausgehende Empfehlungslinks

Status: **ENTWURF — nicht in die Live-Seite gemischt, keine Rechtsfreigabe, keine anwaltliche Prüfung.**
Erstellt: 2026-10-30 (Cron-Lauf 4). Zitations-Ledger: `research/datenschutz-partner-301026-ledger.json`
(14/14 Zitate maschinell verbatim verifiziert gegen Evidenz in `research/evidence/datenschutz-partner-301026/`).
Zweck: Die in `operations/AFFILIATE-LINK-STATUS.md` angekündigte Präzisierung des Abschnitts
„Keine Profilbildung, keine Weitergabe" ist hier textfertig vorbereitet — **separat vom Live-Text**,
solange kein Partnerlink tatsächlich geschaltet ist (Vorgabe: nur tatsächlich implementierte
Verarbeitung beschreiben; geplante Klauseln getrennt halten).

## 1. Ausgangslage (heute live)

- `datenschutz.html` Abschnitt 5 sagt aktuell: „Wir verkaufen keine Daten, schalten keine Werbung
  und erstellen keine Nutzungsprofile. Solange keine Vermittlung eingerichtet ist, gibt es keine
  Weitergabe von Daten durch uns." (Quelle: `generate.mjs`, Datenschutz-Pages-Block, Stand 30.10.2026)
- Optional-Messung ist consent-gated (GA4, Web-GTM v5, Whitelist: Seitenaufrufe + anonyme Klicks
  auf vier dokumentierte Schaltflächenarten). Partner-Klick-Events sind **nicht** Teil der
  aktuellen Whitelist.
- Renderer für Partnerlinks ist implementiert, aber inaktiv (`data/partner-links.json`:
  `active=false`, alle Programme `approved=false`, keine URLs; Gate `test_partner_links.py`
  bricht den Build bei sichtbaren Markern im Inaktiv-Modus).

## 2. Was technisch passiert, sobald ein Partnerlink live geht

Klickfluss (belegte Grundlage: Netzwerk-Eigendokumente, Abschnitte 3–4):

1. Leser*in klickt auf einen als Anzeige gekennzeichneten Link auf unserer Seite.
2. Der Klick verlässt unsere Seite über die Redirect-/Tracking-Infrastruktur des Netzwerks.
   Dabei setzt das **Netzwerk in eigener bzw. gemeinsamer Verantwortung** Cookies auf seinen
   eigenen Domains — nicht wir (Awin: Cookies der Awin-eigenen Domain nach Klick[1];
   ADCELL: Tracking-Cookies nach Klick auf ein Werbemittel[3]). Wir übermitteln selbst keine
   Daten und erhalten aus dem Prozess keine Bestände.
3. Die Zielseite des Advertisers (HIRO, Lifta, Malteser, Aroundhome, Pflegehase) unterliegt
   deren eigener Datenschutzerklärung.
4. Lead-/Anfragedaten entstehen **ausschließlich beim Advertiser** — nie auf unserer Seite,
   nie in unseren Systemen. Auf unserer Seite bleibt es bei dem bereits dokumentierten,
   consent-gated Klick-Event (nur `content_id`/`partner_id`/`placement_id`, ohne Personenbezug),
   und nur wenn dieses Event-Modell aktiviert wird (Abschnitt 6, Amendment C).

## 3. Belegte Netzwerk-Grundlagen: Awin (Lifta 40988, Malteser 112616, Aroundhome 68536)

- Technologien: „Die wichtigsten Technologien, die für das Tracking von Awin verwendet werden,
  sind Tracking-Domain-Cookies, Journey-Tags und Geräte-Fingerprinting."[1]
- Cookie-Setzung nach Klick: „Hierbei handelt es sich um Cookies, die von Awins eigener Domain
  verwendet werden, wenn ein Nutzer auf eine vom Publisher angezeigte Werbung klickt. Wir
  verwenden diese Informationen, um nachzuvollziehen, welcher Nutzer von welchem Publisher an
  welchen Advertiser weitergeleitet wurde."[1]
- Rolle und Speicherdauer: „Grundsätzlich werden über die Awin-Technologie erhobene Tracking-Daten
  bis zu drei (3) Jahre gespeichert und anschließend gelöscht oder anonymisiert. In begrenzten
  Fällen kann Awin bestimmte Tracking-Daten in pseudonymisierter Form für bis zu fünf (5) Jahre
  aufbewahren, sofern dies für interne Analysezwecke erforderlich ist. Für diese Verarbeitungen
  handelt Awin als eigenständiger Verantwortlicher auf Grundlage seiner berechtigten Interessen,
  die gegen die Rechte und Erwartungen der Nutzer abgewogen wurden."[1]
  → Awin ist für sein Tracking **eigenständiger Verantwortlicher**; wir sind nicht
  Verantwortliche der Netzwerk-Cookies. Der Entwurfstext benennt Awin deshalb transparent
  als eigenen Anbieter, nicht als „unsere Auftragsverarbeiter".
- Transparenzrahmen: „Awin nimmt am IAB Europe Transparency & Consent Framework teil und hält
  dessen Spezifikationen und Richtlinien ein. Die Identifikationsnummer von Awin im Rahmen
  lautet: 907."[1]

## 4. Belegte Netzwerk-Grundlagen: ADCELL (HIRO 9440, Pflegehase 10690)

- Verantwortlicher des Netzwerks: Firstlead GmbH, Rosenfelder Straße 15–16, 10315 Berlin
  (AGB VI, Abschnitt „I. Informationen über uns als Verantwortliche").[3]
- Gemeinsame Verantwortlichkeit mit uns als Publisher (Art.-26-Anlage zum Hauptvertrag):
  „Beide Vertragspartner, das Netzwerk und seine Partner, gelten als gemeinsame Verantwortliche
  in Bezug auf die Verarbeitung und Speicherung von personenbezogenen Daten, die im Zuge der
  Zusammenarbeit im Rahmen des Hauptvertrages erhoben werden."[2] Diese Anlage wird mit der
  Registrierung akzeptiert — deshalb ist die ADCELL-Registrierung ein Betreiber-Akt (GO).
- Hinweispflicht: „Der Hinweis auf das eingebundene Tracking von ADCELL ist sowohl für Publisher
  als auch Partnerprogrammbetreiber (Advertiser und Agenturen) eine Pflichtangabe im Sinne der
  DSGVO."[2] — die Aufzählung der Daten verweist auf AGB VI.[2]
- Tracking-Cookies: „Cookies, die für das ADCELL-Tracking verwendet werden: ADCELLpidX Dieser
  Cookie wird gesetzt nach dem Klick auf ein ADCELL Werbemittel und enthält Informationen über
  Publisher, Werbemittel, SubID, Referrer und Zeitstempel." sowie „Die Gültigkeitsdauer des
  Cookies ist abhängig vom entsprechenden Programm."[3]
- Pseudonymität: „Bei der von uns verwendeten Online-Kennungen der Nutzer, handelt es sich um
  pseudonyme Werte. D.h. die Online-Kennungen enthalten selbst keine personenbezogenen Daten
  wie Namen oder E-Mailadressen."[3]
- Widerspruch/Opt-out: ADCELL bietet Datenschutzeinstellungen; Widerspruch „wird über Cookies in
  Ihrem Browser gespeichert"; die Daten lassen „weder für ADCELL noch für die Anbieter der
  Website einen unmittelbaren Personenbezug" zu.[4]
- Consent-Empfehlung des Netzwerks (für den offenen Punkt in Abschnitt 7): „Es wird empfohlen,
  dass der Gebrauch von Tracking-Technologien erst nach vorheriger Zustimmung (Opt-in), bspw.
  durch die Abfrage beim Nutzer über einen Consent-Layer (IAB Consent Framework konform)
  erfolgt."[2]

## 5. Entwurfstexte (fertig zum Einfügen, pro Programm geschaltet — nie vorher)

### Amendment A — Abschnitt 5 wird ersetzt, sobald der ERSTE Partnerlink live geht

```text
5. Keine Profilbildung, keine Weitergabe — ausgehende Empfehlungslinks
Wir verkaufen keine Daten und erstellen keine Nutzungsprofile. Bei den als „Anzeige" bzw.
„Partner-Link" gekennzeichneten Verweisen gilt: Der Klick führt Sie auf eine externe Website
(Netzwerk-Weiterleitung, dann Anbieter). Wir übermitteln dabei selbst keine Daten an Dritte.
Erst nach dem Verlassen unserer Seite setzen das jeweilige Netzwerk und der Anbieter eigene
Cookies und verarbeiten dort technische Daten zur Zuordnung der Vermittlung (Einwilligung,
Zuordnung der Vergütung). Für diese Verarbeitung sind das Netzwerk und der Anbieter jeweils
selbst verantwortlich; Einzelheiten stehen in Abschnitt [Partnerlinks] und in den dort
verlinkten Erklärungen der Anbieter. Auf unserer Seite entsteht daraus kein Datenbestand.
```

### Amendment B — neuer Abschnitt „Partnerprogramme (ausgehende Links)", pro Netzwerk ein Absatz

```text
[X]. Partnerprogramme (ausgehende Links)
Auf dieser Website verwenden wir gekennzeichnete Empfehlungslinks zu Anbietern von Treppenliften,
Hausnotruf und Badumbau. Klicken Sie einen solchen Link, verlassen Sie unsere Website; es gelten
danach die Datenschutzangaben des Netzwerks und des Anbieters.

Awin (Awin AG): Nach dem Klick auf einen Empfehlungslink setzt Awin Cookies auf der
Awin-Tracking-Domain, um zuordnen zu können, über welche Website ein Nutzer zu welchem Anbieter
weitergeleitet wurde. Awin verarbeitet hierfür in eigener Verantwortung Tracking-Daten und
speichert sie in der Regel bis zu drei Jahre (in Ausnahmefällen pseudonymisiert bis zu fünf
Jahre, interne Analysezwecke). Awin nimmt am IAB-Transparency-&-Consent-Framework teil (ID 907).

ADCELL (Firstlead GmbH): Nach dem Klick auf einen Empfehlungslink setzt ADCELL
Tracking-Cookies (u. a. „ADCELLpid…"), die Angaben zu Publisher, Werbemittel, Sub-ID, Referrer
und Zeitpunkt enthalten; die Laufzeit richtet sich nach dem jeweiligen Programm. Die verwendeten
Online-Kennungen sind pseudonym. Für das Tracking von ADCELL und seiner Publisher-Partner besteht
eine Vereinbarung zur gemeinsamen Verantwortlichkeit (Art. 26 DSGVO). Widerspruch gegen das
ADCELL-Tracking ist über die Datenschutzeinstellungen von ADCELL möglich.

Anbieter nach Netzwerk (Stand der Programmangaben, geprüft am jeweiligen Datum):
- Awin: Lifta (Cookie 30 Tage, Profil geprüft 30.10.2026), Malteser (30 Tage, 30.10.2026),
  Aroundhome (30 Tage, 23.10.2026)
- ADCELL: HIRO Lift (90 Tage, 30.10.2026), Pflegehase Hausnotruf (60 Tage, 23.10.2026)
Die Cookie-Laufzeiten entstammen den jeweiligen Programmprofilen (Forschungsstand:
research/check_partner_status_301026.py, research/partner-scan-231026.md,
research/direct-partner-scan-281026.md). Bei Aktivierung wird je Programm die aktuelle
Datenschutzerklärung des Anbieters verlinkt und das Datum neu geprüft.
```

Kennzeichnung/Pflichtangabe bleibt im Renderer gelöst („Anzeige"-Label, Vergütungshinweis,
`rel="sponsored noopener"` — bereits Gate-getestet, `test_partner_links.py`).

### Amendment C — nur falls Partner-Klick-Messung in GA4 aktiviert wird

Abschnitt 2 der Live-Seite enumeriert die Whitelist aktuell als „nur Seitenaufrufe und anonyme
Klick-Ereignisse … auf eine der vier dokumentierten Schaltflächenarten". Wird die
Partner-Klick-Messung (`partner_cta`) aktiviert, ist die Enumeration in demselben Commit zu
erweitern (fünfte Schaltflächenart, gleiche Statistik-Einwilligung, gleiche Feldbegrenzung).
Kein separater Consent-Category-Wechsel: Es entstehen keine neuen Erstanbieter-Cookies und keine
neuen Empfänger auf unserer Seite. Wird die Partner-Klick-Messung NICHT aktiviert, bleibt
Abschnitt 2 unverändert.

## 6. Aktivierungsregeln (Gates)

1. **Pro-Programm-Granularität:** Amendment-Texte werden nur für Netzwerke mit tatsächlich
   geschaltetem Link eingemischt (Awin-Absatz erst bei erster Awin-Zusage, ADCELL-Absatz erst
   nach Registrierung + Programmfreigabe). Nicht-Freigegebenes wird nicht beschrieben.
2. **Gleicher Commit:** Datenschutz-Textänderung landet im selben Commit wie die
   `partner-links.json`-Aktivierung des Programms — nie davor, nie danach.
3. **Stand-Zeile:** Die „Stand dieser Erklärung"-Zeile in `datenschutz.html` wird nur bei
   tatsächlich überarbeitetem Text aktualisiert (keine automatische Datierung).
4. **Tests:** `test_partner_links.py` erzwingt Inaktivität bis zur Zusage; nach Aktivierung
   prüft es Kennzeichnung und Link-Attribute. Neuer Gate-Fall: keine Aktivierung ohne den
   zugehörigen Datenschutzabschnitt (Kontradiktionsregel analog URL-ohne-Zusage).
5. **Kein Consent-Banner-Umbau:** Netzwerk-Cookies setzen nach Verlassen unserer Seite ein;
   unser CMP kontrolliert sie nicht. Der Text beansprucht genau das — keine Kontrolle, die wir
   nicht haben.

## 7. Offene Punkte (bewusst nicht entschieden, Betreiber/rechtliche Prüfung)

- **Einwilligung vor dem ausgehenden Klick?** [unverified — bewusst nicht entschieden] ADCELL
  empfiehlt Opt-in über einen Consent-Layer für das eigene Tracking,[2] Awin nimmt am IAB-TCF
  teil.[1] Ob das TDDDG/ePrivacy einen vorherigen Consent für die nach dem Verlassen der Seite
  gesetzten Netzwerk-Cookies verlangt oder die Pflichtangabe genügt, ist hier **nicht
  entschieden**;[unverified] die konservative Option (Partnerlinks erst nach
  Statistik-/Marketing-Einwilligung aktiv schalten oder zumindest dokumentieren, warum nicht)
  bleibt Betreiber-Entscheid. Kein Rechtsrisiko-Abschirmungstext.
- ADCELL-Registrierung (Joint-Controller-Zustimmung) = Betreiber-Akt — GO ausstehend.
- Endgültige E-Mail-Löschfrist (Abschnitt 4 der Live-Seite) weiterhin offen.
- Bei Aktivierung: Datenschutzerklärungs-URLs der fünf Anbieter je live verifizieren und
  verlinken (jetzt bewusst nicht vorab verlinkt, da Links erst bei geschaltetem Partnerlink
  relevant werden).

## 8. Abgleich mit der Programme-Wahrheit (Anti-Drift)

Alle Programmkonditionen in Abschnitt 5 sind Forschungsstand mit Prüfdatum und führen ihre
Quelle auf (Scans vom 23./28./30.10.2026, jeweils verbatim-Ledger in `research/`). Vor dem
Einfügen von Amendment B ist der Programmstand erneut gegen die öffentlichen
Netzwerkprofile zu prüfen (Awin-Profile ohne Login lesbar, ADCELL-Programmseiten ohne Login
lesbar); Netzwerk-Eigenseite schlägt Verzeichnis-Echo.

## Sources

[1] https://www.awin.com/de/datenschutzerklarung — Awin Datenschutzerklärung
    > "Die wichtigsten Technologien, die für das Tracking von Awin verwendet werden, sind Tracking-Domain-Cookies, Journey-Tags und Geräte-Fingerprinting."
    > "Hierbei handelt es sich um Cookies, die von Awins eigener Domain verwendet werden, wenn ein Nutzer auf eine vom Publisher angezeigte Werbung klickt. Wir verwenden diese Informationen, um nachzuvollziehen, welcher Nutzer von welchem Publisher an welchen Advertiser weitergeleitet wurde."
    > "Grundsätzlich werden über die Awin-Technologie erhobene Tracking-Daten bis zu drei (3) Jahre gespeichert und anschließend gelöscht oder anonymisiert. In begrenzten Fällen kann Awin bestimmte Tracking-Daten in pseudonymisierter Form für bis zu fünf (5) Jahre aufbewahren, sofern dies für interne Analysezwecke erforderlich ist. Für diese Verarbeitungen handelt Awin als eigenständiger Verantwortlicher auf Grundlage seiner berechtigten Interessen, die gegen die Rechte und Erwartungen der Nutzer abgewogen wurden."
    > "Awin nimmt am IAB Europe Transparency & Consent Framework teil und hält dessen Spezifikationen und Richtlinien ein. Die Identifikationsnummer von Awin im Rahmen lautet: 907."
[2] https://www.adcell.de/datenverarbeitung — ADCELL Vereinbarung zur gemeinsamen Verantwortung (Joint Controller)
    > "Beide Vertragspartner, das Netzwerk und seine Partner, gelten als gemeinsame Verantwortliche in Bezug auf die Verarbeitung und Speicherung von personenbezogenen Daten, die im Zuge der Zusammenarbeit im Rahmen des Hauptvertrages erhoben werden."
    > "Der Hinweis auf das eingebundene Tracking von ADCELL ist sowohl für Publisher als auch Partnerprogrammbetreiber (Advertiser und Agenturen) eine Pflichtangabe im Sinne der DSGVO."
    > "Daten die vom Netzwerk ADCELL erhoben werden sind in den Allgemeinen Geschäftsbedingungen unter VI. Datenschutzerklärung aufgeführt"
    > "Es wird empfohlen, dass der Gebrauch von Tracking-Technologien erst nach vorheriger Zustimmung (Opt-in), bspw. durch die Abfrage beim Nutzer über einen Consent-Layer (IAB Consent Framework konform) erfolgt."
[3] https://www.adcell.de/agb — ADCELL AGB — VI. Datenschutzerklärung (Firstlead GmbH)
    > "Cookies, die für das ADCELL-Tracking verwendet werden: ADCELLpidX Dieser Cookie wird gesetzt nach dem Klick auf ein ADCELL Werbemittel und enthält Informationen über Publisher, Werbemittel, SubID, Referrer und Zeitstempel."
    > "Bei der von uns verwendeten Online-Kennungen der Nutzer, handelt es sich um pseudonyme Werte. D.h. die Online-Kennungen enthalten selbst keine personenbezogenen Daten wie Namen oder E-Mailadressen."
    > "Hierzu werden die Publisher-Links und unsere Angebote um bestimmte Werte ergänzt, die ein Bestandteil des Links oder anderweitig, z.B. in einem Cookie, gesetzt werden können."
    > "Die Gültigkeitsdauer des Cookies ist abhängig vom entsprechenden Programm."
[4] https://www.adcell.de/datenschutz — ADCELL Datenschutzeinstellungen/Opt-out
    > "Die Daten ermöglichen es weder für ADCELL noch für die Anbieter der Website einen unmittelbaren Personenbezug herzuleiten."
    > "Hiermit widersprechen Sie der Analyse von themenbasierten nicht personenbezogenen Daten Ihres Surfverhaltens. Dieser Widerspruch wird über Cookies in Ihrem Browser gespeichert."
