# Batch-Protokoll: treppenlift-finanzierung (Briefing 20, 31. Ratgeber)

Prüfdatum: 2026-11-09 · Cron-Lauf · SERP-basierte Topic-Wahl (GSC im Cron weiter ohne Google-Sitzung).

## Topic-Gates

**Gewählt: Treppenlift-Finanzierung/Ratenzahlung.**
- SERP (10 Treffer): 8/10 Hersteller-/Händler-Selbstauskunft (TK, Lifta, Sanitätshaus Klein, gebrauchttreppenlifte, Ellmers, Nord-Ostsee Liftteam, Krone, SANIMED), 1 Vermittler (der-treppenlift.de), 1 Ratgeber (ideal-treppenlift.de, Du-Form, „Zahlen sind Richtwerte" ohne Primärquellen). Verbesserungslücke belegt: keine geprüfte Seite nennt den Gesetzeswortlaut, das 20.11.2026-Kredit-Reform-Datum oder verifizierbare Divergenzen.
- Kaufnah (Zahlungsentscheid = Aufmaß-Schwelle), Kern-Cluster Lift (isLift-Regex automatisch), Monetarisierungspfad Treppenlift (Lifta 40988 offen, HIRO 9440 via ADCELL-GO) bleibt intakt — Artikel benötigt keine Placements, CTA-Route „Förderung zuerst prüfen" → treppenlift-zuschuss.
- Intent-distinct (grep Bestand): „Finanzierung" nur Streu-Mentions (bad-umbau, zuschuss im Förderkontext); „Ratenzahlung" 1 Satz im mieten-Artikel („Nach der letzten Rate eines Kaufs gehört die Anlage Ihnen"). Keine Kannibalisierung.

**Verworfen mit Beleg:**
- Pflegegrad-Höherstufung: 10/10 SERP dicht besetzt (DAK/AOK-Eigenseiten, pflege.de, juraforum ×2, heimkompass Stand 22.09.2026, eteros 16.07.2026, kompass-der-pflege 10.07.2026) — Muster wie die verworfenen Entlastungsbetrag/Pflegezeit-Topics; zusätzlich Kannibalisierungsrisiko mit pflegegrad-antrag-ablauf-fristen (gleiche Antrag-Maschinerie, anderer Trigger).
- Duschsitz/Duschhocker Kassenübernahme: dünner SERP, aber Small-Ticket (≈30–100 €) ohne Payable-Event und ohne Partnerprodukt — verfehlt den Commercial-Hypothesis-Gate; Hilfsmittel-Grundlagen schon durch 2 Artikel abgedeckt.

## Quellenkette (20 Quellen, alle 09.11.2026 live gerufen)

Hersteller-/Händlerangaben (1–6): TK Home Solutions (50/50 zinsfrei 1 Jahr, „Keine zusätzlichen Gebühren", Bank-Hinweise, KfW-Zins-Echo „ab 2,35 % p.a." = historisch), HIRO (easyCredit/TeamBank, 2–60 Monate, „Im selben Termin ... Ratenzahlung und Zuschüsse", Restbetrag-nach-Zuschuss-Wortlaut), Lifta (individuelle Vereinbarung, Anzahlung+Raten, **Absenz skriptgeprüft: gerenderter Text 0× „zinsfrei"/„zinslos"/„0 %"/„0%"/„ohne Zinsen"**), Nord-Ostsee Liftteam (easyCredit 12–60 Raten, max. 10.000 € inkl. nach Pflegekassenzuschuss-Abzug), Der Treppenlift („Zinslose Ratenzahlung 0 % Effektivzins 12 bis 60 Monate" neben „Anzahlung von mind. 50 % ... auf 11 Teilzahlungen" = **Intra-Seiten-Widerspruch dokumentiert**), gebrauchttreppenlifte („individuelle Laufzeiten und Sondertilgungen ohne Zinsen", „bis zu 4.180 Euro").

Verbraucherquellen (7–9): VZ Kreditverträge-Rechte (14 Tage; 0 % ab 200 € widerrufbar; „keine Vorfälligkeitsentschädigung" bei 0-%-Ablösung), vzhh (§ 356d BGB 1J+14T. bei falscher Belehrung), vzbv-Urteil (0 % = „unentgeltlicher Darlehensvertrag mit eingeschränktem Widerrufsrecht").

Reform (10–12): evz.de (aktualisiert 30.10.2026: Stichtag 20.11.2026, erfasste Formen, Bonitätsprüfung, Datenschutz, Dispo-Widerruf), Bundestag-Textarchiv kw16/2026 (Entwurfs-Einbeziehung Kleinkredite ≤200 €/zins- und gebührenfreie/≤3 Monate/BNPL), BGBl 2026 I Nr. 139 (Gesetzstitel auf der amtlichen Verkündungsseite).

Gesetzestexte (13–20, gesetze-im-internet, ISO-8859-1/Entities gescrapt): BGB § 491 (entgeltlich, <200-€-Ausnahme, ≤3-Monate-Ausnahme), § 492 (Schriftform, Abschrift, Tilgungsplan), § 495 (Widerruf § 355), § 500 Abs. 2 (vorzeitige Erfüllung jederzeit), § 502 (Vorfälligkeit nur bei gebundenem Sollzins, max. 1 %/0,5 %), § 312g (Haustür-Widerruf + Abs. 2 Nr. 1 maßgefertigte-Waren-Ausnahme), § 356b (Fristbeginn erst mit Vertragsurkunde, 1-Monats-Frist bei Nachholung); SGB XI § 40 Abs. 4 („4 180 Euro je Maßnahme").

## Dokumentierte Divergenzen (Kern des Artikels)

D1 Laufzeiten: TK 50/50-in-12-Monaten vs. HIRO 2–60 vs. Liftteam 12–60 vs. der-tl intra-seitig 12–60 vs. 11 vs. Lifta „individuell".
D2 Betragsgrenze: nur Liftteam nennt 10.000 €; TK/Lifta/der-tl keine.
D3 Zinsausweis: TK/der-tl „0 %" beworben, gebrauchtl „ohne Zinsen", Lifta ohne jede Zinsangabe.
D4 Rechtsstand: keine geprüfte Seite nennt die 20.11.2026-Reform (11 Tage nach unserem Prüfdatum) — Artikeldokumentation inkl. Refresh-Trigger.
D5 Stale-Echo: TK bewirbt KfW-Zins „ab 2,35 % p.a." — die KfW rendert heute erstmals „ab 3,19 %" (Beobachtung aus dem Morgen-Prüflauf 1279a39); Artikel warnt generisch, Beträge bleiben im zuschuss-Ratgeber.
D6 Snippet-Stale-Falle: das SERP-Snippet von gebrauchttreppenlifte zeigte eine „4000,- Euro"-Zeile; die LIVE-Seite nennt 4.180 Euro (konsistent mit § 40). Zitate ausschließlich aus dem Live-Text; Snippet als Falle im Ledger notiert.

## Rechenbeispiel (fiktiv, im Artikel deklariert)

8.000 € Anschaffung → 4.180 € Zuschuss → 3.820 € Restbetrag → 24 Monate zinsfrei = 159,17 €/Monat; ohne Zuschuss 48 × 166,67 €/Monat. Arithmetik skriptgeprüft (Ledger, 3 Checks).

## Gates und Tests

- Ledger research/verify_finanzierung_091126.py: **70/70 PASS** (60 verbatim Zitate über 20 Quellen + 5 Lifta-Absenz-Patterns + 3 Arithmetik + BGBl-Titel + evz-Stand). Neu: norm() entfernt Strip-Artefakt-Leerzeichen vor Satzzeichen.
- Content-Support-Gate research/verify_finanzierung_content_091126.py: **ALL PASS** — jeder Article-Key (Abschnitte/Paragraphen/Bullets/Tabelle/FAQs/Quellen-URLs+checked_at/Anker 1–20) im LAUNCH-dist; Related 3× Lift-Cluster ohne Self; Early-CTA „Förderung zuerst prüfen" → treppenlift-zuschuss; 0 Partner-Marker; SVG; Kernzahlen inkl. Reform-Datum. Lektion: citation-Regex auf `\[\d+\]` erweitert (Quellen >9 brachen den `\[\d\]`-Strip).
- SVG getBBox 0 Overflows + Pairwise-Overlap 0 + Vision-Inspektion sauber (research/verify_finanzierung_svg_mobile_091126.py; Screenshots svg-screenshot.png, mobile-390-finanzierung.png).
- Mobile 390 px: 0 px Overflow.
- npm test komplett grün: beide Build-Modi, test_site 51 Seiten, test_articles **31**, test_cross_links, test_titles_meta ALL PASS (nach Desc-Kürzung 164→141 Zeichen), Playwright **21 passed**, test:measurement, Partner-Gates A–F ALL PASS (A3 ≥ 30).
- llms.txt: SUMMARIES + SECTION_MAP (Lift-Sektion) +1. Renderer specialMap +1. Zähler: articles 30→31, RSS 30→31, A3 ≥29→≥30.
- Bewusst NICHT wiederholt: Förderbeträge (nur §-40-Zitat als Grenze + Verweis auf zuschuss-Ratgeber), KfW-Zinssätze als eigene Angabe, medizinische/steuerliche Details (Verweis auf steuer-Ratgeber im Textbestand über clusters).

## Offene Punkte / Refresh-Trigger

- **Nach dem 20.11.2026**: Abschnitt „Kredit-Reform" und die §-491-Zitate neu prüfen (neuer Wortlaut gilt für Verträge ab dem Stichtag; VZ-Übergangsfragen dann gegen die neue Rechtslage re-verifizieren). Ledger-Note.
- ADCELL-GO (HIRO 9440) betrifft diesen Artikel nicht (keine Placements); bei künftiger Aktivierung bleibt der Artikel frei von Trackern, sofern placement-Config ihn nicht adressiert (Gate B4).
