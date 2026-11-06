# ADCELL-GO-Pack: Ein GO schaltet zwei Partnerprogramme frei

Stand: 06.11.2026 (beide Programmseiten + Registrierungsseite heute ohne Login frisch re-verifiziert, Evidenz: `research/evidence/adcell-refresh-061126/`)
Autor: milo (agentenseitig vorbereitet; Registrierung selbst = Betreiber-Akt)

## Was das eine GO umfasst (drei Akte in einem Durchgang)

1. **ADCELL-Publisher-Registrierung** auf Tobias Batke (Kleingewerbe) — Betreiber-Akt, weil zwei
   Zustimmungen persönlich zu bestätigen sind:
   - „Ich habe die Allgemeinen Geschäftsbedingungen und Datenschutzerklärung gelesen und akzeptiere diese."
   - „Ich stimme der Vereinbarung zur gemeinsamen Verantwortung (Joint Controller) zu."
   Beide Checkbox-Wortlaute heute live verifiziert (Signup-Extrakt, s. Evidence).
2. **HIRO Lift (Programm 9440) bewerben** — Bewerbungsformular mit Freitext (unten fertig
   formuliert); Freischaltung durch HIRO. Wortlaut der Seite: „Bewerben Sie sich einfach –
   wir schalten Sie dann für unser Partnerprogramm frei."
3. **Pflegehase Hausnotruf (Programm 10690) beitreten** — offenes Programm, Seitenwortlaut:
   „Nach Ihrer Anmeldung können Sie direkt loslegen."

Danach läuft alles agentenseitig: Tracker-URLs bauen, `data/partner-links.json` erweitern,
`test_partner_links.py` erweitern, DSE-Amendment B (liegt textfertig in
`research/datenschutz-partner-entwurf.md`) im selben Commit aktivieren, Deploy + Live-Readback.

## Verifizierte Konditionen (Netzwerk-Eigenseiten, 06.11.2026)

| | **HIRO Lift (9440)** | **Pflegehase Hausnotruf (10690)** |
|---|---|---|
| Vergütung | „Standard-Lead 50,00 €" / „50,00 EUR pro erfolgreichem Lead" | „Standard-Lead 25,00 €" / „25,00 Euro pro erfolgreichen Lead" |
| Lead-Definition | Kontaktanfrage Beratung/Termin | „Ein Lead ist ein von der Pflegekasse genehmigter Antrag"; valide bei „richtigen Personen … Anspruch auf die Leistungen" |
| Cookie | 90 Tage | 60 Tage |
| Freigabezeit | ø 56 / max 56 Tage (Stornoquote 0 %) | ø 28 / max 56 Tage (Stornoquote n.a.) |
| Werbemittel | 5 (3 Banner, 1 DeepLink, 1 Textlink) | 7 (5 Banner, 1 Textlink, 1 DeepLink) |
| Bedingungstabelle (06.11. live) | SEM „eingeschränkt auf Anfrage"; PLA/Cashback/Gutscheinmarketing „erlaubt"; **incentivierter Traffic „nicht erlaubt"**; Direct Linking „erlaubt" | SEM/PLA/Cashback/Gutscheinmarketing/**incentivierter Traffic** je „erlaubt"; Direct Linking „erlaubt" |
| Cluster-Fit | Treppenlift-Kerncluster | Hausnotruf-Artikel (Backup zu Malteser) |

**Änderung gegenüber früheren Scans:** Pflegehase hatte am 23.10. keine sichtbare
SEM/Traffic-Tabelle; seit heute ist sie explizit (inkl. „incentivierter Traffic erlaubt").
Unser eigener Standard bleibt davon unberührt: **rein redaktionell, rein organischer Traffic,
kein SEM/PLA/Cashback/Gutschein/Incentive/Retargeting** — egal was das Programm zuließe.
HIROs „incentivierter Traffic nicht erlaubt" treffen wir ohnehin. Pflegehase warnt zusätzlich:
Gutscheine als Gegenleistung für Registrierungen „strengstens untersagt".

Konsistenz-Historie: HIRO-Konditionen identisch zum 28.10./30.10.-Scan
(`research/direct-partner-scan-281026.md`); Pflegehase identisch zum 23.10.-Scan
(`research/partner-scan-231026.md`) — nur die Bedingungstabelle ist neu sichtbar.

## Fertige Formulareinträge (Registrierung, adcell.de/affiliates)

| Feld | Eintrag |
|---|---|
| Anrede* | Herr |
| Sie betreiben* | **„Webseite (Content, Blog, SEO)" — ausschließlich diese Option** (nicht SEM/SMM/Retargeting) |
| Land* | Deutschland |
| Name / Firma | Tobias Batke (Kleingewerbe — Feldbezeichnung im Formularverlauf ablesen) |
| Webseite | https://zuhausebleiben-kompass.de |
| E-Mail | anfragen@zuhausebleiben-kompass.de (Projektpostfach, lesbar durch milo) — oder Tobias' eigene Adresse, wenn er Postfall-Kontrolle will (GO-Unterpunkt) |
| Auszahlung | Bankverbindung im Konto hinterlegen (Betreiber-Akt, kann nachgereicht werden) |

## Fertige Bewerbungstexte

**HIRO 9440 (Bewerbungsfreitext, ‚individuelle Informationen für Ihre Bewerbung'):**

> Inhaltliche Ratgeber-Plattform zu Treppenlift und barrierearmer Wohnraumanpassung für
> ältere Menschen und Angehörige (zuhausebleiben-kompass.de, ca. 30 quellenbasierte
> Ratgeber, geprüfte Primärquellen, Sie-Ansprache). Rein redaktioneller, organischer
> Traffic — kein SEM, kein Brand-Bidding, kein Incentive, kein Cashback. Empfehlungslinks
> ausschließlich kontextpassend in bestehende Treppenlift-Artikel, gekennzeichnet als
> Anzeige. Bitte um Freischaltung.

**Pflegehase 10690 (offen; Join-Notiz falls Notizfeld erscheint):**

> Redaktionelle Hausnotruf-Ratgeber mit belegten Pflegekassen-/Hilfsmittel-Quellen;
> rein organischer Traffic, kein SEM/Incentive/Cashback. Links nur kontextpassend in
> bestehende Hausnotruf-Artikel, Anzeige-Kennzeichnung. Achtung Buchhaltung: Lead =
> genehmigter Pflegekassen-Antrag — langsame, aber hochwertige Pipeline.

## Aktivierungs-Pfad nach Freischaltung (agentenseitig, Reihenfolge)

1. Tracker-/Deeplink-URLs aus dem Programm holen (kein Link-Bau vor Freischaltung).
2. `data/partner-links.json`: `hiro-lift` (Treppenlift-Cluster-Zielseiten festlegen) und
   `pflegehase-hausnotruf` (nur hausnotruf-kosten-anbieter-vergleich wie Malteser-Pfad;
   schluesselhinterlegung/kuendigen bewusst ohne Placement).
3. `test_partner_links.py` um beide Slugs + aktive Zustände erweitern.
4. DSE-Amendment B (ADCELL-Absätze aus `research/datenschutz-partner-entwurf.md`) im
   SELBEN Commit — Gate F erzwingt das.
5. `npm test` + `build:launch` + Deploy + Live-Readback (Placements, rel=sponsored,
   Anzeige-Kennzeichnung, DSE-Abschnitte).

## Was das GO NICHT umfasst

Kein Vertrag mit Lead-Abnehmern, keine Budget-/Ausgabenfreigabe (Registrierung ist
kostenlos), keine Übernahme von Pflegehase-Marktclaims („gesetzlicher Anspruch" bleibt
unserseits unbelegt und wird nicht übernommen), kein SEM-Opt-in bei ADCELL-Kanalfeld.
