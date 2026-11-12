# Batch 20 (2026-11-12, Cron-Lauf) — Briefing 24: Wohnung nach Krankenhausentlassung anpassen

**Artikel:** `content-ready/wohnung-anpassen-nach-krankenhausentlassung.json` · **Live:** https://zuhausebleiben-kompass.de/wohnung-anpassen-nach-krankenhausentlassung.html · **Grafik:** `assets/images/krankenhaus-entlassung-wegweiser.svg` · **35. Ratgeber**

## 1. Topic-Wahl (SERP-basiert, GSC im Cron weiter ohne Google-Sitzung)

- **Intent:** „nach Krankenhausentlassung Wohnung anpassen / wer hilft" — Krankenhaus-Übergangs-Journey (Entlassmanagement → Begutachtung → Förder-Anträge → Überbrückung).
- **Bestand-Lücke:** grep über alle 34 Artikel: „Entlass" nur 1 Marginahinweis (pflegegrad-antrag), „39a"/§ 18a/§ 18c 0×.
- **SERP-Feld:** organisch nur generische Barrierefrei-Portale (pflege-panorama, ADAC, gesund.bund.de, pflege-planer, regional-treppenlift) + 1 pflege-panorama-Schlaganfall-Artikel; der dedicated Krankenhaus-Einstieg fehlt. Institutionenseiten (GKV, KBV, BMG, DKG) dicht auf dem Rechtsbegriff, aber ohne Journey-Ratgeber.
- **Konkurrenz-Gap skriptgeprüft:** pflege-panorama Schlaganfall-Artikel: **0× „Entlassmanagement"**, keine Krankenhaus-Fristen (nur Förderbeträge; Evidenz `research/evidence/krankenhaus-121126/panorama-schlaganfall.html`, Ledger-Absenz x5).
- **Verworfen heute:** keine weiteren Kandidaten geprüft (Fokus dieser Unit); Backlog unverändert (ADCELL-GO, Liftstar-Follow-up, Awin-Login — Operator-abhängig).

## 2. Kernbefunde (Ledger 84/84 Pässe — 24 Verbatim-Zitate über 16 Quellen + Arithmetik + 5 Absenzen)

`research/krankenhaus-121126-ledger.json` + `research/verify_krankenhaus_121126.py`; Evidenz `research/evidence/krankenhaus-121126/` (10 Gesetz-/Portal-Extrakte + Rahmenvertrag-PDF ×2 Fassungen + Roh-HTML uncommitted):

- **§ 39 Abs. 1a SGB V:** Entlassmanagement als Teil der Krankenhausbehandlung; doppelter Anspruch (gegenüber Krankenhaus; Unterstützung durch Kasse; Kassen-Kooperation bei Pflegeleistungen); umfasst „alle dafür erforderlichen Leistungen nach dem Elften Buch"; Übergangs-Verordnungen „bis zu sieben Tagen"; Einwilligung „schriftlich oder elektronisch"; Rahmenvertrag-Rechtsbasis (Spitzenverbände + KBV + DKG).
- **Rahmenvertrag 14. ÄndVb (19.11.2025, aktueller Lesefassungs-Stand):** Anspruch des Patienten gegenüber dem Krankenhaus, während gegenüber Kasse/Pflegekasse „nur" Unterstützung geschuldet ist; standardisiertes EM in multidisziplinärer Zusammenarbeit; Kliniken informieren im Internetauftritt; Einwilligung vor dem Assessment.
- **§ 18a Abs. 5 SGB XI (Konkurrenz-Lücke Nr. 1):** Begutachtung „spätestens am fünften Arbeitstag" im Krankenhaus/Reha, wenn „zur Sicherstellung der … Weiterversorgung" erforderlich; Auftragsübermittlung binnen 3 Arbeitstagen (§ 18 Abs. 1); **verkürzt** — nur Feststellung „mindestens Pflegegrad 2", abschließende Begutachtung wird nachgeholt (Abs. 7); 10-Arbeitstage-Klausel bei Kurzzeitpflege direkt aus KH/Übergangspflege/Reha.
- **§ 18c SGB XI:** Bescheid „spätestens 25 Arbeitstage" (= etwa fünf Kalenderwochen, Arithmetik a1: 25/5=5); elektronische Mitteilung unmittelbar ans Krankenhaus zulässig.
- **§ 7a / § 32 / § 40 / § 42:** Pflegeberatungs-Anspruch (auch bei laufendem Antrag mit erkennbarem Bedarf); EUTB unabhängig „im Vorfeld der Beantragung"; § 40 Abs. 4 Wohnumfeld-Zuschuss (subsidiär/Ermessen/Zweckformel) + Abs. 7 Entscheidungsfrist 3/5 Wochen; § 42 Kurzzeitpflege **nur Pflegegrade 2–5**, Übergangszeit, acht Wochen/Kalenderjahr; § 47 SGB IX Hilfsmittel nur „getragen oder mitgeführt oder bei einem Wohnungswechsel mitgenommen" → fester Lift ist kein Hilfsmittel (Refresh-Validierung von Briefing 23s Grenz-These gegen den Live-Text).
- **Praxis-Ehrlichkeit:** VdK („weit über 100" Erfahrungsberichte, „hilflose Patientinnen", Bentele-Zitat) + AOK („benötigt es Ihre schriftliche Einwilligungserklärung"; selbst-ansprechen-Fall) + gesund.bund (frühzeitiges Gespräch, Angehörige einbeziehen) + VZ (Entlassbrief/Medikationsplan/Pflegeüberleitungsbogen, 7-Tage-Liste).
- **Kurskorrekturen im eigenen Text:** Kompetitor-Zitat mit „4.180" bewusst NICHT ins eigene HTML übernommen (Absenz-Gate x1); „KfW" 0× im Artikel (x2); Treppenlift-Preise 0× (x3); Partner-Marker 0× (x4); Wort „Anzeige" vermieden (§ 18 nutzt „Anzeige" — Artikel sagt „Antrag").

## 3. Renderer-Unit vorab (eigener Commit `94556ac`)

**Live-Fehler gefunden und behoben:** Article-Renderer komma-splizte Array-Intros in EINEN Lead-Absatz ohne Leerzeichen (live: „…nutzen kann.,Dieser Ratgeber…") — betraf 6 Artikel (angehoerige, schluessel, finanzierung, ohne-pflegegrad, sitzsteh, unserioese). Fix: Array-Intros als eigene `<p class="lead">`-Absätze + `.lead+.lead{margin-bottom:14px}`. npm test EXIT 0 vor dem Push; Junction-Check 6/6 Artikel sauber im LAUNCH-dist.

## 4. Integration

- `article-renderer.mjs`: isCare-Regex + `wohnung-anpassen` (ZWEI Stellen synchron: renderer + `test_cross_links.py`), specialMap +1 (Early-CTA „Wohnumfeld-Zuschuss beantragen" → wohnumfeldverbesserung-beantragen).
- `data/cross-links.json`: links + rationale (Whitelist: foerderung-ohne-pflegegrad, hausnotruf-kosten, mieten — 2 Lift-Crosses + care-pool-Ziel).
- `research/llms-txt.py`: SUMMARIES + SECTION_MAP (Pflegegrad/Hilfsmittel/Sicherheit-Sektion) +1.
- Testzähler: test_articles 34→35, verify_checklists_build RSS 34→35, test_partner_links A3 ≥33→≥34.

## 5. Gates

- Ledger `verify_krankenhaus_121126.py`: **84/84 ALL PASS** (24 verbatim + Integrität 1..16 + 10 Kernzahlen + Arithmetik + 5 Absenzen inkl. Konkurrenz-0×).
- Content-Support-Gate `verify_krankenhaus_content_121126.py`: **135/135 ALL PASS** gegen LAUNCH-dist (alle JSON-Keys inkl. table-cells, 2 Lead-Absätze ohne Splice, Related-Reihenfolge exakt config, CTA + Anker abschnitt-7, SVG/alt/KI-Label, 7 Absenz-Needles).
- SVG: getBBox 51 Elemente 0 Overflows + Pairwise 0 Overlaps (`verify_krankenhaus_svg_121126.py`) + Vision-Sichtkontrolle sauber (Header in Streifen, keine Kappen, Kreise 1–9 passend).
- Mobile 390 px: 0 px Overflow, SVG 346 px (`verify_krankenhaus_mobile_121126.py`).
- npm test EXIT 0 (PREVIEW+LAUNCH, 60 Seiten/46 locs, 35 Artikel, cross_links 35, titles 0 Verletzungen, Playwright 21 passed, Partner A–F ALL PASS), danach build:launch für die manuellen Gates.

## 6. Deploy

- Commit + Push: siehe launch-state; CI-Wait `wait_ci_krankenhaus_121126.py` (SHA-gepinnt), Live-Readback `verify_krankenhaus_live_121126.py` auf der öffentlichen URL, IndexNow `indexnow_submit_krankenhaus_121126.py` (Artikel + Homepage).

## 7. Refresh-Kandidaten / Offenes

- Rahmenvertrag Entlassmanagement: 14. ÄndVb vom 19.11.2025 ist die aktuelle Lesefassung — bei einer 15. Änderung Artikel-Absatz „Anspruch ggü. Krankenhaus vs. Kasse" re-prüfen (Ledger-Notiz).
- BMG-Seite nennt „Rahmenvertrag vom 1. Juli 2024" — bei Umbenennung/Neufassung den PDF-Link re-prüfen.
- Bestehende Offenen unverändert: ADCELL-GO (HIRO 9440 + Pflegehase 10690), Liftstar-Follow-up (Keychain), Awin-Login-Status, GSC nur mit Google-Sitzung.
