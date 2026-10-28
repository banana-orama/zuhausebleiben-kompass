# Batch-Protokoll: Briefing 14 — Plattformlift (Rollstuhllift) für Rollstuhlfahrer

Datum: 2026-10-28 · Slug: `treppenlift-plattformlift-rollstuhllift` · Cluster: lift · Status: `editorial-reviewed-preview` (im Launch-Index)

## Topic-Gates (SERP-basiert, GSC im Cron weiterhin nicht abrufbar)

- **Kannibalisierungs-Grep (28.10.):** „plattformlift“ nur als Alternativen-Erwähnungen in 6 Lift-Artikeln, „treppensteiger“ nur in schmale-treppe, „haltegriff“ in 3 Care/Bad-Artikeln — intent-distinct bestätigt.
- **Kandidatenentscheidung:** Plattformlift (vorkaufsnah, 5-stelliges Budget, gleiche Vergleichspartner: HIRO/Lifta verkaufen Plattformlifte, CTA → treppenlift-firmen-vergleich) gegen Haltegriff-Bad (100–800-€-Produkt, kein bestätigter Partner, Distanz zur Monetarisierung zu groß) gewählt.
- **SERP 28.10.:** 7+ dedizierte Konkurrenzartikel — Konkurrenzdichte allein kein Kill (Muster wie bei Briefing 13), weil die Verbesserungslücken konkret belegbar sind.
- **Belegte Verbesserungslücken:** (1) Portal-Unter-Grenzen für dieselbe „gerade, innen“-Frage streuen 7.000/7.500/8.000/9.000/10.000 €, Hersteller beginnen erst ab 11.000 € — die niedrigsten Portal-Grenzen sind unterhalb des Hersteller-ab-Preises. (2) Tragkraft-Widersprüche (225–300 vs. 250 vs. 300–320 vs. 200-kg-Wechselstrom vs. 250–400 „für Rollstuhl und Begleitperson“) und Begleitperson-Widerspruch (treppenlifto „darf nicht mitfahren“ vs. kostenwelt „ausreichend für … Begleitperson“). (3) Begriffsvermischung Hublift/Senkrechtaufzug/schräger Plattformlift (lehner belegt das explizit). (4) Geschwindigkeits-Divergenz HIRO 0,1 m/s vs. treppenlifto/EN 81-40 0,15 m/s. (5) Treppenbreiten-Widerspruch (Lifta 90–110 cm vs. treppenlifto „1 m reicht“). Artikel dokumentiert alle Seiten mit Quellenlabel statt eine Zahl zu übernehmen.
- **Verworfen:** Treppensteiger als eigener Artikel (dichte SERP-Umgebung ohne eigenständige Beleglage → dünner Seitenklang); Haltegriff-Bad (s. o.).
- **Stale-Echo notiert (Ledger):** kostenwelt stellt KfW 455-B als förderfähig dar, treppenliftwissen (Okt 2026) schreibt „nimmt derzeit keine Anträge an“ — Artikel hält sich an den live-verifizierten Stand im Zuschuss-Ratgeber, keine Betrags-Wiederholung.

## Quellenkette

11 Quellen, alle am 28.10.2026 abgerufen (`research/evidence/plattformlift-281026/`, Raw-HTML + bereinigte TXT):

1. treppenliftwissen Rollstuhllift (Fachportal, Aktualisiert Okt 2026, Methodik-Tabelle Stand 07.10.2026, Werbepartner-Disclosure HIRO)
2. hiro.de/preise (Herstellerangabe)
3. hiro.de/modell/hiro-350 (Herstellerangabe)
4. hiro.de/modell/hiro-320-k (Herstellerangabe)
5. lifta.de/rollstuhllifte (Herstellerangabe)
6. personenaufzuege.com Plattformlift-Kosten (Fachportal, Stand Sept 2026, Footer 26.10.2026)
7. treppenlifte-preise.de Magazin (Fachportal, „Wo kein Preis belegt ist, steht das ausdrücklich da“)
8. treppenlifto.de (Fachportal)
9. seniorenrat.de (Ratgeber-Portal, Stand 2026)
10. kostenwelt.de (Ratgeber-Portal, aktualisiert Sept 2026)
11. lehner-lifttechnik.com (Hersteller-Blog/Marktübersicht)

**Ledger:** `research/plattformlift-281026-ledger.json` — **185/185 PASS** (`research/verify_plattformlift_281026.py`): 103 Verbatim-Zitate, 20 Tabellen-Kontext-Checks (Label↔Zahl in Zeilennähe), 12 Arithmetik-/Divergenz-Checks (u. a. Etagen-Faktoren 1,55/2,05 × Spannen, HIRO-Min/Max = 11.000/38.000, Unter-Grenzen-Kette 7.000 < … < 11.000).

## Kerninhalte

- Vier-Bauarten-Trennung (Hublift / Plattformlift gerade / Plattformlift kurvig / Homelift) als erste Entscheidung, dann Preise — Reihenfolge umgekehrt zur Portal-Konvention.
- Portal-Spannen-Tabelle (6 Quellen, mit Stand-Spalte) + Herstellertabelle (HIRO-Preisseite mit Etagenstaffel, Lifta ab-Preise) nebeneinander; kurvig außen = „Auf Anfrage“ dokumentiert statt Zahl erfinden.
- Preisfaktoren: Kurven-Maßschienen, bauliche Anpassungen, außen (Verweis auf Briefing 13), Gebraucht-Divergenz (40 % vs. „unter 6.000“), Miete kaum (Sitzlift-Referenz 50–200 €/Monat), Wartung 200–450 €/Jahr.
- Maße: HIRO-Plattformformate (800×1000–900×1250 mm; 320 K 620×750–750×840), Treppenbreiten-Widerspruch 90–110 vs. „1 m“, eigene Rollstuhl-Messregel statt Normmaß, Verweis schmale-treppe.
- Tragkraft als Gesamtgewicht-Rechnung (Nutzer + Rollstuhl 20/60/100+/99–150 kg + Zubehör, Steigungs-Abzug), Herstellerwerte 250/300 kg, Portal-Widersprüche benannt, Verweis maximalgewicht.
- Fahrt-Sicherheit: Rampe/Bügel/Notstopp/Akku (Herstellerangaben), Tempo- und Begleitperson-Divergenz als „im Angebot klären“, Rechts-Einordnung (Maschine ≠ Aufzug, Prüfpflicht >3 m/gewerblich) nur als Fachportalangabe mit Vorbehalt.
- Förderung bewusst nur als Verweis auf treppenlift-zuschuss (dort 26.10. live gegen Gesetzestext geprüft); treppenlifto-Rundung „4.000“ als Echo-Warnung erwähnt.
- 10-Punkte-Angebots-Checkliste; Transparenz-Sektion mit Betreiber, KI-Hinweis, Abrufdatum.

## Grafik

`assets/images/treppenlift-plattformlift-rollstuhllift-weg.svg` (980×680): Vier Zeilen Situation → Bauart → Preis-Richtwert (Herstellerangaben), Footer mit Richtwert-Vorbehalt. Saubere Marker-/Zeilen-Struktur (Lektion aus Briefing 13): keine gekreuzten Pfeile.

Sichtkontrolle: getBBox 0 Overflows + neuer **Box-Kontext-Check** (Text muss in seiner eigenen Zeilen-/Preisbox bleiben, nicht nur im viewBox) 0 Verstöße + Vision-Inspektion des Chromium-Screenshots ohne Befund (`research/verify_plattformlift_svg_281026.py`).

## Gates und Tests

- Ledger 185/185 (siehe oben), Commit-gebundene Skripte `fetch_plattformlift_281026.py` / `fetch_plattformlift_mfr_281026.py`.
- Content-Support-Gate `research/verify_plattformlift_content_281026.py`: **ALL PASS** gegen LAUNCH-Dist (intro, alle paragraphs/bullets/2 Tabellen/paragraphs_after, 6 FAQs, Quellenanker 1–11 inkl. aller URLs, alle 11 Zitationsnummern aufgelöst, Early-CTA-Label+Ziel, Checklisten-Anker, Related 3× lift-Cluster, SVG src/alt/KI-Caption, No-Claim-Liste, 22 Kernzahlen in Prosa-Schreibweise, robots `index,follow`).
- `npm test` (Build PREVIEW+LAUNCH, test_site 45 Seiten, test_articles **25**, test:measurement, Playwright-Consent, test_partner_links A2 ≥ **25**): Exit 0.
- `research/verify_checklists_build.py` gegen LAUNCH-Dist: ALL PASS, RSS **25 Items**, Sitemap 48 locs inkl. Artikel.
- Mobile 390 px (`research/verify_plattformlift_mobile_281026.py`): 0 px Overflow, 2 table-scroll-Regionen, Early-CTA „Anbieter für Rollstuhllifte vergleichen“ sichtbar, Checklisten-Anker springt, SVG eingebunden, Quellenanker 1/6/11.

## Renderer/Infra

- article-renderer.mjs specialMap +1 (Early-CTA „Anbieter für Rollstuhllifte vergleichen“ → treppenlift-firmen-vergleich).
- llms-txt.py SUMMARIES + SECTION_MAP erweitert.
- Testzähler: test_articles 24→**25**; verify_checklists_build RSS 24→**25**; test_partner_links A2 ≥ **25**.

## Abgrenzungen / Grenzen im Artikel

- Alle Preise als gekennzeichnete Portal-/Herstellerrichtwerte; keine Offert- oder Bewilligungszusage; Förderbeträge nicht wiederholt.
- Tragkraft/Begleitperson/Tempo/Norm-Einordnung als dokumentierte Divergenzen mit „Datenblatt + Aufmaß entscheidet“ statt eigener technischer Diagnose.
- Keine Formulare, keine Partnerlinks (Partner-Map bleibt inactive bis Zusage), keine Gesundheitsdaten.
