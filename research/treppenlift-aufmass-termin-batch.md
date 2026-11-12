# Batch 21 (2026-11-12, Cron-Lauf Nachmittag) — Briefing 25: Treppenlift-Aufmaß-Termin

**Artikel:** `content-ready/treppenlift-aufmass-termin.json` · **Live:** https://zuhausebleiben-kompass.de/treppenlift-aufmass-termin.html · **Grafik:** `assets/images/treppenlift-aufmass-termin-ablauf.svg` · **36. Ratgeber**

## 1. Topic-Wahl (SERP-basiert, GSC im Cron weiter ohne Google-Sitzung)

- **Intent:** „Treppenlift Aufmaß — was passiert beim Termin / wie vorbereiten“ — Angebotsstufe der Lift-Journey (nach Firmenwahl, vor Vertrag).
- **SERP-Feld (10/10 geprüft):** 0 dedizierte Verbraucher-Guides zum Aufmaß-Termin; 5/10 Händler-/Hersteller-Seiten (Interessenkonflikt: ts-treppenlifte, baethe, sonilift, siemer, lifta), 1 VZ-Journey-Artikel (Planung gesamt, ohne Aufmaß-Protokoll), 1 CHIP-Unternehmensportrait (digitales Aufmaß), Rest Broker-Kosten-Seiten.
- **Verworfen heute mit Beleg:** Plattformlift/Rollstuhllift — bereits im Bestand (`treppenlift-plattformlift-rollstuhllift.json`, 26 Rollstuhl-Mentions) + SERP 10/10 Fachportal-/Händler-Dichte. Treppenlift verkaufen — pflege-panorama hat dedizierten 2026-Guide + 4 Teil-Sektionen (aroundhome/pflegeanteil/treppenlift-beratung) + Ankauf-Händler-Dominanz; schwaches Payable-Event (Ankauf, kein Partnerprogramm). Wohnung anpassen bei Demenz — gesund.bund.de + VZ (24.04.2026) + AOK + pflege.de + Wohnberatungs-Netz decken den Intent dicht institutionell.
- **Kanibalisierungs-Gate (grep):** „Aufmaß“ im Bestand nur als Nebenrolle (schmale-treppe: 13× Selbstmess-Winkel; firmen-vergleich: 3× Firmenwahl) — kein Artikel behandelt den Termin selbst. Letzte unbesetzte Journey-Stufe: Auswahl ✓ → **Aufmaß ✗** → Angebot/Vertrag ✓ (unserioese) → Finanzierung ✓.

## 2. Kernbefunde (Ledger 68/68 Pässe — 33 Verbatim-Zitate über 8 Quellen + 3 Arithmetik + 4 Absenzen)

`research/aufmass-121126-ledger.json` + `research/verify_aufmass_121126.py`; Evidenz `research/evidence/aufmass-121126/` (9 Extrakte .txt; Roh-HTML/PDF uncommitted):

- **Ablauf nach Händlerangabe:** Anfrage → Vorab-Angebot „innerhalb von 24 Stunden“ → Vermessung vor Ort „kostenlos“ → „Festpreis inklusive Montage“; „Aufmaß vor Ort statt Preis nach Foto oder Telefonat bei kurvigen Treppen“; Seriositäts-Checkliste (Festpreis inkl. Montage, Modell/Hersteller benannt, Lieferzeit + Einbaudauer genannt, Gewährleistung/Wartung, Elektroarbeiten ausgewiesen); „Das Angebot eignet sich als Kostenvoranschlag für die Pflegekasse“ [4, Stand November 2026].
- **Hersteller-Dauern:** Montage „zwei bis drei Stunden“ gerade / „maximal fünf Stunden“ kurvig [5]; FAQ „meist innerhalb eines halben Tages“ + Stufenmontage „nicht an der Wand“ + „kostenlose Beratung“ [6]; „Nach einem ersten unverbindlichen Termin … ausreichend Bedenkzeit“ [5]; Fachbetrieb „kostenfreier Aufmaßservice bis zum unverbindlichen Angebot“ [7].
- **Verbraucherschutz (VZ, Stand 20.01.2026):** mehrere Vergleichsangebote + kostenloser Kostenvoranschlag; „Keinesfalls … drängen lassen“; 14-tägiges Widerrufsrecht in Wohnung/Telefon; Werkvertrag (BGH-Bezug); ohne Belehrung „12 Monate und 14 Tage“; Festpreis statt Kostenvoranschlag („Überschreitung bis zu 20 Prozent ohne Anzeige“); „Vorsicht bei Hausbesuchen … nicht allein wahrnehmen“; „Unterschreiben Sie nicht vorschnell“; Zahlung erst bei Prüfbescheinigung + mängelfreier Funktion [1].
- **VZ-Umfrage 2020 (125 Bögen):** ⅓ von 120 hat sofort unterschrieben; ⅓ ohne ausreichende Widerrufs-/AGB-Info; 46/123 ohne Planungsunterlagen; „Planungsunterlagen unbedingt vor der Vertragsunterschrift“; Linienführung (Türen, Rollator-Platz) als Planungsphase-Aufgabe [2]. Chart-Arithmetik: 43+81+1=125, 83+37+5=125, 77+46=123.
- **§ 312g BGB:** Abs. 1 verbatim (außerhalb Geschäftsräumen/Fernabsatz) + Abs. 2 Nr. 1 Maßanfertigungs-Ausnahme — die Maßschiene kann darunter fallen; ehrliche Grenze wie in finanzierung/unserioese [3].
- **Digitales Aufmaß:** fotogrammetrische Erfassung + Konfiguration; „Der Vor-Ort-Termin wird nicht ersetzt“; „Rabatte, die nur am selben Abend gelten“ als dokumentiertes Druckmuster [8, Unternehmensportrait].
- **Bewusst 0×:** Förderbeträge (4.180/16.720), KfW, €-Beträge, Partner-Marker — Preise/Förderung bleiben in kosten/zuschuss/finanzierung-Artikeln (Cluster-Regel).

## 3. Integration

- `article-renderer.mjs`: specialMap +1 (`treppenlift-aufmass-termin` → `/treppenlift-firmen-vergleich.html`, „Anbieter für Aufmaß vergleichen“). Lift-Cluster läuft über den Slug-Präfix automatisch (kein isCare-Eingriff).
- `data/cross-links.json`: links + rationale (angebote-vergleichen, unserioese, schmale-treppe — lift-intern).
- `research/llms-txt.py`: SUMMARIES + SECTION_MAP (Treppenlift-Sektion) +1.
- Testzähler: test_articles 35→36, verify_checklists_build RSS 35→36, test_partner_links A3 ≥34→≥35.

## 4. Gates

- Ledger `verify_aufmass_121126.py`: **68/68 ALL PASS** (33 verbatim + Zitat-Integrität 1..8 + 9 Kernwortlaute + 3 Arithmetik + 4 Absenzen).
- Content-Support-Gate `verify_aufmass_content_121126.py`: **0 FAILS** gegen LAUNCH-dist (alle JSON-Keys inkl. table-cells, 2 Lead-Absätze, Related-Reihenfolge exakt config, Early-CTA specialMap + Anker abschnitt-8, SVG/alt/KI-Label, 7 Absenz-Needles inkl. 0× „€“).
- SVG `verify_aufmass_svg_121126.py`: **20/20 ALL PASS** (getBBox 17 Texte in viewBox, pairwise Text-Text 0, Text-Chip 0) + Vision-Sichtkontrolle sauber (Screenshot `research/evidence/aufmass-121126/svg-shot.png`).
- Mobile `verify_aufmass_mobile_121126.py`: 390 px **0 px Overflow**, SVG-Image skaliert.
- npm test **EXIT 0** (PREVIEW+LAUNCH, 56 Seiten, 36 Artikel, cross_links 36, titles, Playwright 21 passed, Partner A–F ALL PASS), danach `build:launch` für die manuellen Gates (dist-Regel).
- Build-Artefakte LAUNCH: Sitemap inkl. Artikel, RSS 36, llms.txt, Homepage-Verlinkung — alle 4 grep-positiv.

## 5. Deploy

- Commit + Push (SSH), CI-Wait `wait_ci_aufmass_121126.py` (SHA-gepinnt), Live-Readback `verify_aufmass_live_121126.py` auf der öffentlichen URL, IndexNow `indexnow_submit_aufmass_121126.py` (Artikel + Homepage).

## 6. Offenes / Nächste Einheiten

- Bestehende Offenen unverändert: ADCELL-GO (HIRO 9440 + Pflegehase 10690), Antworten auf die am 12.11. versendeten Enquiries (Lotse/Malteser-Terms/Aroundhome) abwarten, Awin-Login-Status, GSC nur mit Google-Sitzung.
- PNOG-Refresh-Trigger unverändert (1. Lesung 05.11., Anhörung 25.11., nicht beschlossen).
- Lift-Journey jetzt lückenlos: Kosten ✓ Firmen ✓ Aufmaß ✓ Angebot ✓ Widerruf/Druck ✓ Finanzierung ✓ Steuer ✓ Gebraucht ✓ Miete ✓ Förderung ✓ Außen ✓ Schmal ✓ Sitz/Steh ✓ Plattform ✓ unseriös ✓ — nächste Content-Einheiten bevorzugt Care-/Wohn-Journey (Region-Ausbau mit verifizierten Landesprogrammen als dokumentierter Kandidat).
