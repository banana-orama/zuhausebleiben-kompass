# Batch-Protokoll: hausnotruf-smartwatch-als-ersatz (Briefing 27, 2026-11-16)

## Topic-Gate (SERP-basiert, GSC im Cron weiter ohne Google-Sitzung)

**Gewählt:** „Smartwatch oder Handy statt Hausnotruf?" — die Ersatz-/Objection-Intent der Care-Journey.

- **SERP-Feld:** 5 dedizierte Seiten, fast alle mit Interessenkonflikt: pflege.net (07.06.2026, Leadgen; 403/WAF bei Abrufversuch — nur Snippet-Beleg, kein Zitat), pflege-helfer24 (16.10.2026, Anbieter-Magazin), helfi-ruf (13.05.2026, Anbieter), notfallknopf.de (Anbieter-Ratgeber), pflegekompass (13.07.2026, Leadgen) + 1 Technik-Blog (smartwatch-fitnesstracker 30.09.2026) + 3 Shopping-Ads davor. Institutional Coverage dünn: VZ 1 Smartwatch-Hinweis, gesund.bund 1 Notruf-App-Satz, ADAC 0× Smartwatch.
- **Bestand-Lücke:** grep über alle 37 Ratgeber — „Smartwatch" 4× nur als Grenze im Mobil-Artikel, kein Ersatz-Intent abgedeckt (0 Abschnitte).
- **Verworfen mit Beleg: „Hausnotruf bei Demenz"** — institutionell dicht (VZ-Absatz „weniger geeignet", VdK „ungeeignet", Deutsche Alzheimer eigene Seite „Technische Hilfen", pflege.de GPS-Tracker-Demenz) + Ortungs-/Demenz-Inhalt bereits in hausnotruf-mobil-gps (8 Demenz-Mentions) → Kannibalisierung.
- **Kanibalisierungs-Gate:** intent-distinct gegen mobil-gps (Gerätewahl unterwegs/GPS) und sturzerkennung-oder-knopf (Sensor-vs-Knopf am klassischen System); dieses Artikel = Gesamt-Ersatz-Entscheidung (Zentrale vs. keine Zentrale).
- **Payable-Pfad:** Early-CTA → hausnotruf-kosten-anbieter-vergleich (dort einziges aktives Placement-Cluster, Malteser beratungstermin). Kein Partner-Placement auf dem Artikel (Cluster-Regel).

## Quellen (alle 16.11.2026 frisch geprüft, Ledger 96/96 verbatim + Absenzen)

1. **Verbraucherzentrale 10566** — Basistarif „27 und 40 Euro", Zusatzleistungen „30 bis 80 Euro" **UND** im Zusatzleistungs-Absatz derselben Seite „rund 30 bis 50 Euro (oder auch mehr)" → **intra-page Divergenz dokumentiert** (beide Spannen im Artikel; Fortsetzung der D3-Divergenz aus dem Angehörigen-Batch); Pflegekasse „bis zu 27 Euro monatlich" + weitere Voraussetzungen; Akku 10–20 h; Demenz „weniger geeignet"; **Smartwatch-Hinweis** („mit GPS und Sturzprophylaxe, … unter bestimmten Voraussetzungen von der Pflegekasse finanziert").
2. **gesund.bund.de** — Zielgruppe + Telefon-Grenze; Notruf-App auf „eigenem Smartphone oder der Smartwatch"; Sturzsensoren-Ablauf; Demenz-Ausnahme-Pfad „Ortungsfunktion und automatischer Sturzerkennung".
3. **ADAC (Artikel 13.10.2026)** — Geräte „einfacher in der Bedienung als ein Telefon oder Handy"; Pauschale „27 Euro (seit 1. April 2026)", „mindestens Pflegegrad 1"; vorübergehende Einrichtung; Fehlersignale; **Absenz 0× „Smartwatch"** (dokumentiert).
4. **VdK Hamburg** — Demenz „ungeeignet" + Begründung; **Stale-Echo dokumentiert**: „um die 20 bis 25 Euro" / „30 und 50 Euro" / „25,50 Euro monatlich" = Stand vor 1.4.2026, gegen VZ-aktuell abgewogen. (Schreibfehler „bestimmen" im Original verbatim belassen.)
5. **Deutsche Alzheimer Gesellschaft** — Notruf „bei einer Notrufzentrale oder bei Angehörigen bzw. dem Pflegedienst"; Kauf ohne Zentrale; Sturz-/Falldetektor; Ortungs-Sender-Formen; Freiheits-Warnung („Manche Produkte können die Freiheit einschränken"); **Absenz 0× „Smartwatch"**.
6. **pflege.de (Portalangabe)** — Sturzsensoren in „Armband, … Smartwatch oder als Extragerät"; Apple/Galaxy/Senioren-Uhren; Kopplung oder eigene SIM + Mobilfunkkosten; „ab bereits 50 Euro … bis zu mehreren hundert Euro"; „Akku muss regelmäßig geladen werden" / „Fehlalarme können ausgelöst werden"; „Geeignet für technisch versierte Nutzer"; Zusatzservice „nicht immer … im Monatsbeitrag enthalten".

**Absenz-Checks (skriptgeprüft):** ADAC/Alzheimer/VdK je 0× „smartwatch"; VZ je 1× „30 bis 50" + 1× „30 bis 80" (intra-page Divergenz); alle 6 Evidenzen 0× Förderbeträge (4.180/4 180/16.720).

## Artefakte

- Artikel: `content-ready/hausnotruf-smartwatch-als-ersatz.json` (10 Abschnitte, 6 FAQs, 6 Quellen, Tabelle 3 Wege, 8-Punkte-Checkliste, Grenzen-Abschnitt; 0 Partner-Marker, 0 Förderbeträge).
- Grafik: `assets/images/hausnotruf-smartwatch-entscheidung.svg` (3 Karten + Prüfband + Quellenzeile; getBBox 0 Overflows, Pairwise 0, Chip 0; Vision-Sichtkontrolle sauber; Mobile 390 px 0 px).
- Ledger: `research/smartwatch-161126-ledger.json` + `research/verify_smartwatch_161126.py` (96/96 PASS).
- Content-Gate: `research/verify_smartwatch_content_161126.py` (120/120 PASS gegen LAUNCH-dist).
- SVG/Mobile: `research/verify_smartwatch_svg_mobile_161126.py` (ALL PASS).
- Evidenz: `research/evidence/smartwatch-161126/` (6 Raw-HTML + 6 txt + Screenshots; pflege.net 403/WAF dokumentiert, kein Zitat daraus).
- Renderer: specialMap +1 („Kosten & Anbieter vergleichen" → hausnotruf-kosten-anbieter-vergleich); cross-links.json links+rationale (kosten-vergleich, sturzerkennung, mobil-gps — care-intern); llms SUMMARIES + SECTION_MAP +1; isCare trifft via hausnotruf-Präfix (keine Regex-Änderung).
- Zähler: test_articles 37→38; verify_checklists_build RSS 37→38; test_partner_links A3 ≥35→≥36.

## Gate-Ergebnisse

- `npm test` EXIT 0 (58 Seiten je Modus, test_articles 38, cross_links 38/8, titles, Playwright, measurement, Partner A–F ALL PASS), danach `build:launch` (Sitemap 50 locs).
- Ledger 96/96 · Content-Gate 120/120 · SVG/Mobile ALL PASS · Sitemap exakt 50 locs (49+1) · RSS 38.

## Refresh-Trigger

- VZ-Zahlen (27–40 / 30–80 vs. 30–50 intra-page) und ADAC-27-€-Stand bei nächster Pflege-Reform oder VZ-Update re-prüfen.
- VdK-Stale-Echo: beim nächsten Durchlauf gegen aktuellere VdK-Fassung re-prüfen (kann behoben sein).
- pflege.net 403 (WAF): nur wenn Content-Bedarf — residential-context re-check, kein Datei-Bump ohne echten Abruf.
- Reformen: PNOG/§-40-Änderungen betreffen den Artikel indirekt (Pflegekassen-Absatz) — geht aus den bestehenden PNOG-Refresh-Triggern hervor.
