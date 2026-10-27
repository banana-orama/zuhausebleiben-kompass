# Batch-Protokoll: Briefing 13 — Treppenlift für die Außentreppe (Außenlift)

Datum: 2026-10-27 · Slug: `treppenlift-aussentreppen-aussenlift` · Cluster: lift · Status: `editorial-reviewed-preview` (im Launch-Index)

## Topic-Gates (SERP-basiert, GSC im Cron nicht abrufbar)

- **Kannibalisierungs-Grep:** 0 Bestandsinhalte zu „außenlift/außentreppe“; „plattformlift“ nur als Alternativen-Erwähnungen in 5 Lift-Artikeln, „treppensteiger“ nur in schmale-treppe — intent-distinct bestätigt.
- **SERP 27.10.:** 10+ dedizierte Konkurrenzartikel. Anders als beim verworfenen „Wartung“ (post-purchase) ist Außentreppenlift vorkaufsnah (Eingangsschwelle vor Aufmaß/Angebot) — Konkurrenzdichte allein kein Kill.
- **Belegte Verbesserungslücke:** Preis-Unter-Grenzen streuen zwischen den Portalen (3.500 / 4.000 / 5.000 / ca. 6.000 €), Lifta-Herstellertabelle überlappt innen (5.500–9.900) und außen (6.500–8.500) vollständig — die pauschale „Aufschlag“-Behauptung von personenaufzuege ist damit für Sitzlifte nicht haltbar; wir dokumentieren beide Lesarten statt eine Zahl zu übernehmen. Zweite Lücke: IP-Klassen kursieren nur in Fachportalen (IP54/IP65/IP67 bzw. „65+“), während die geprüften Herstellerseiten HIRO/Lifta 0 IP-Angaben enthalten (skriptgeprüft) — der Artikel fordert Schutzart + Temperaturbereich aus dem Datenblatt.
- Verworfen in der Themenfindung (Batches 9–12, unverändert): Wartung (post-purchase), Einbau-Ablauf (dicht), Pflegegrad-Widerspruch (VZ-Dominanz), Akku/Stromausfall (commodity), Kurventreppe (Kannibalisierung mit treppenlift-kosten).

## Quellenkette

8 Quellen, alle am 27.10.2026 abgerufen (`research/evidence/aussenlift-271026/`, Raw-HTML + bereinigte TXT):

1. treppenliftwissen Außenlift (Fachportal, Stand Okt 2026; eigene Quellenprüfung Juli 2026 — im Artikel gekennzeichnet)
2. personenaufzuege.com (Fachportal, Stand 17.09.2026, „Marktrichtwerte“)
3. treppenlifte-preise.de Magazin (Fachportal)
4. seniorenrat.de (Ratgeber-Portal, Artikel 02.06.2026)
5. HIRO LIFT hiro.de/treppenlifte-aussen (Herstellerangabe)
6. Lifta lifta.de/treppenlift/aussenlifte (Herstellerangabe)
7. Lifta lifta.de/faq Preisspannen (Herstellerangabe, inkl. „inklusive Einbau und Inbetriebnahme“)
8. Verbraucherzentrale Planungsartikel (allgemeine Kosten-/Wartungs-/Antrags-Einordnung)

**Ledger:** `research/aussenlift-271026-ledger.json` — **88/88 PASS** (`research/verify_aussenlift_271026.py`): 78 Zitate maschinell verbatim, 3 IP-Absenz-Nachweise auf Herstellerseiten, 7 Arithmetik-/Divergenz-Checks.

## Kerninhalte

- Zwei-Fragen-Ansatz: Was macht ein Gerät „wetterfest“ (Material/Elektronik/Abdeckung) vs. was gehört in das Angebot (Lieferumfang, Fundament, Steckdose, Norm EN 81-40, Wartungsintervall).
- Preisdokumentation als Tabelle mit Stand-Daten statt einer „richtigen“ Zahl; Lifta-Innen/Außen-Überlappung als Gegenbeleg zur Aufschlags-Pauschale; treppenliftwissen-Aufpreis 1.000–4.000 € ausdrücklich als Richtwert.
- Zusatzkosten draußen: Fundament/Erdarbeiten (eigene Angebotszeile), 230-V-Außensteckdose mit FI, Akkubetrieb bei Stromausfall; Wartungsspannen aller drei Quellen nebeneinander (100–250 / 150–300 / 200–300 €) mit Quellenlabel.
- Winter-Praxis: −10 bis −15 °C (Herstellerangaben via Fachportal), Akku-Kapazitätsverlust bis ein Drittel, Ladestation-Regel, kein Streusalz (Garantierisiko), Eis freilegen.
- Genehmigung/Denkmalschutz/MFH-Zustimmung (Verweis mietwohnung), Miete außen (gerade ja ab ~50 €/Monat, Kurven kaum), Gebraucht-Divergenz dokumentiert (40-%-Abschlag üblich vs. Privatkauf-Warnung), Alternativen (Plattformlift außen, Hublift, Rampe, Homelift).
- Förderbeträge bewusst NICHT wiederholt — nur Verweis auf treppenlift-zuschuss (dort 26.10. live verifiziert).

## Grafik

`assets/images/treppenlift-aussentreppen-aussenlift-wetterschutz.svg` (980×680): Außentreppe mit Lift + 6 nummerierten Wetterschutz-Markern + Angebots-Checkliste + Warnbox „Innenmodell niemals draußen“.

Sichtkontrolle: 1. Version hatte echte Layoutfehler (Labels überlappten Lift-Zeichnung und Bodenlinie, Steckdosenlabel außerhalb der Karte, gekreuzte Pfeile — Vision-Prüfung). Komplettumbau auf Marker-/Legendensystem; danach getBBox-Check 0 Overflows (`research/verify_aussen_svg_271026.py`) + Vision-Probe sauber.

## Gates und Tests

- Content-Support-Gate `research/verify_aussen_content_271026.py`: **ALL PASS** (intro, alle paragraphs/bullets/table/paragraphs_after, 6 FAQs, Quellenanker 1–8 inkl. aller URLs, alle 8 Zitationsnummern aufgelöst, Early-CTA-Label+Ziel, Checklisten-Anker #abschnitt-10, Related 3× lift-Cluster, SVG src/alt/KI-Caption, No-Claim-Liste, 8 Kernzahlen im gebauten HTML). Lektion: Gate-Nadel muss der Prosa-Schreibweise folgen („5.500 bis 9.900 Euro“ im Fließtext vs. „5.500 – 9.900 €“ in der Quellentabelle).
- `npm test` (Build LAUNCH+PREVIEW, test_site, test_articles **24**, test:measurement, Playwright **20 passed**, test_partner_links A2 ≥ **24**): Exit 0.
- `research/verify_checklists_build.py` gegen LAUNCH-Dist: ALL PASS, RSS **24 Items** (Modus-Fallstrick erneut bestätigt: erst nach `build:launch` laufen lassen).
- Mobile 390 px (`research/verify_aussen_mobile_271026.py`): 0 px Overflow, Anker/SVG/Early-CTA korrekt.
- llms-txt.py SUMMARIES + SECTION_MAP erweitert; article-renderer.mjs specialMap +1 („Anbieter für Außenlift vergleichen“ → treppenlift-firmen-vergleich).

## Abgrenzungen / Grenzen im Artikel

- Herstellerangaben (HIRO 160 AIR, Lifta GTL 320) als Werbeangaben gekennzeichnet; kein Produkttest.
- IP-/Temperatur-/Norm-/Genehmigungsangaben als Fachportalangaben; verbindlich nur Datenblatt + Aufmaß + Bauordnung des Landes.
- Keine Gesundheitsdaten, keine Formulare, keine Partnerlinks (Partner-Map bleibt inactive bis Zusage).
