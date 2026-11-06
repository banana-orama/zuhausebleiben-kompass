# Batch-Protokoll: hausnotruf-schluesselhinterlegung (Briefing 19, 30. Ratgeber)

Datum: 2026-11-06 · Commit d6e95a3 · CI 42190782682 success · Live-Readback 41/41 ALL PASS · IndexNow 200

## Topic-Gates (SERP-basiert, GSC im Cron weiterhin ohne Google-Sitzung)

| Kandidat | Befund | Urteil |
|---|---|---|
| Kurzzeitpflege (beantragen/Kosten 3.539 €) | 7 dedizierte Ratgeber + Verwaltungsportal, alle frisch (2026) | verworfen: dicht besetzt |
| Entlastungsbetrag (broad + übertragen/rückwirkend) | 10+ Content-Seiten + BMG/Länder-Seiten; Sub-Winkel (übertragen, rückwirkend) ebenfalls 6+ Anbieter | verworfen: Dichte + fehlender Verbesserungs-Hebel |
| Pflegezeit/Familienpflegezeit | 6+ dedizierte 2026-frische Ratgeber | verworfen: dicht besetzt |
| **Hausnotruf-Schlüsselhinterlegung** | organische Konkurrenz ~5–6 Seiten, davon 3 Anbieter-Magazine (easierlife/provita/vitalknopf = Interessenkonflikt); Corpus deckt Intent nur mit 1 Satz (kosten-vergleich) + 1 Erwähnung (mobil) | **gewählt**: intent-distinct, kaufnah (Frage vor Vertragsabschluss im monetisierten Hausnotruf-Cluster), Neutralitäts-Lücke als Verbesserungslücke |

## Kernbefunde (99/99 Ledger-Pässe: 78 Zitate verbatim + 6 Absenz + 15 Artikel-Checks)

- **Kosten-Divergenz dokumentiert statt Einzahl:** Schlüsseltresor einmalig „etwa 30 Euro" (pflege-helfer24) vs. „etwa zwischen 35 bis 100 Euro" (easierLife); Zentrale-Hinterlegung „monatliche Kosten von etwa 15 Euro" (pflege-helfer24) vs. VZ-Einordnung „Zusatzleistungen … um weitere 30 bis 80 Euro"; VZ-Basistarif 27–40 € unverändert. **Absenz-Checks: VZ nennt 0× „15 Euro" und 0× „Tresor"** — die Divergenz ist echt, nicht Zitatsplitter.
- **Pflegekasse ehrlich ohne Abgrenzungs-Fiktion:** zwei Portalangaben wiedergegeben („wird auch nicht von der Pflegekasse bezuschusst", „müssen privat finanziert werden"); die Gerät-vs.-Dienstleistung-Abgrenzung nach SGB XI bleibt **bewusst unbeantwortet** (kein Quellenbeleg — ausdrücklich im Artikel markiert).
- **Notfall-Strecke ohne Schlüssel:** Feuerwehr-Faustregel „Kernarbeit … auf Kosten der Staatskasse" + Kommune-Divergenz + VG Gießen 2 K 2103/23.GI (test.de); AG Hildburghausen 21 C 133/23 — **das Vermieter-Argument „hätte die Tür mit einem hinterlegten Schlüssel öffnen können", kein Generalschlüssel vor Ort, 2.957,21 € Tauschkosten** (Haufe); AG Berlin-Mitte (epileptischer Anfall); Schlüsseldienst: VZ-Fall „fast 800 Euro" + Rechnung „frei erfunden" + Tageszeit-Divergenz.
- **Malteser nur als Herstellerangabe** („auf Wunsch auch der Wohnungsschlüssel", Bereitschaft 365/24); **Absenz skriptgeprüft: Malteser-Seite 0× Tresor / 0× Schlüsseldienst / 0× Hinterlegung** — der Artikel stellt den Tresor NICHT als Malteser-Option dar. KEIN Partner-Placement auf dem Artikel (Placements leben weiter exklusiv auf hausnotruf-kosten-anbieter-vergleich); CTA-Route über specialMap auf den Kosten-/Anbieter-Vergleich.
- Erreichbarkeits-Grenzen + Kombinations-Empfehlung (2 Wege), Code-/Schlosswechsel-Disziplin, Einrichtungsgespräch-Checkliste, Datenschutz-Abschnitt (kleiner Eingeweihten-Kreis).
- Urteilsberichte als Berichte gekennzeichnet, keine Rechtsberatung; alle 8 Quellen checked_at 2026-11-06.

## Integration

- article-renderer.mjs specialMap +1 („Kosten & Anbieter vergleichen" → hausnotruf-kosten-anbieter-vergleich); care-Cluster trifft via hausnotruf-Präfix (keine Regex-Änderung).
- data/cross-links.json: links + rationale +1 (kosten-vergleich, sturzerkennung — care-intern).
- research/llms-txt.py SUMMARIES + SECTION_MAP +1.
- Testzähler im selben Commit: test_articles 29→30 (Assert + RSS-Check), verify_checklists_build RSS 29→30, test_partner_links A3 ≥28→≥29.
- Grafik assets/images/hausnotruf-schluessel-entscheidung.svg: 4 Weg-Bänder + Kosten-Chips + Kombi-Band + Notöffnungs-Footer; getBBox 0 Overflows, Pairwise-Overlap 0, Chip-Kontext-Check 0, **Vision-Probe sauber** (Chips komplett, keine Kollisionen), Mobile 390 px 0 px Overflow.

## Test- und Deploy-Kette

- npm test EXIT 0 (Partner-Gates A–F ALL PASS; 1 bekannter Flaky-Consent-Keyboard-Test solo re-geprüft: PASS).
- verify_schluessel_061126.py **99/99 ALL PASS** (verbatim + Absenz + Artikel-Integrität + Kernzahlen).
- verify_schluessel_content_061126.py ALL PASS gegen LAUNCH-dist (alle JSON-Keys im HTML, Related 3× care mit Cross-Zielen Position 1/2, CTA, 0 Partner-Marker, Anker 1–8).
- Commit d6e95a3, CI Run 42190782682 success; **Pages-Deploy-Lag ~2 min beobachtet** (Artikel 404 → 200 nach Poll) — der Deploy-Readback kam NACH dem Live-Gate.
- Live-Readback 41/41 ALL PASS auf https://zuhausebleiben-kompass.de/hausnotruf-schluesselhinterlegung.html (robots, Kernzahlen, SVG absolut+200, Anker, Sitemap ≥37 locs, RSS 30, llms, Homepage).
- IndexNow HTTP 200 (Artikel + Homepage).

## Bewusst NICHT übernommen

- Preiszahlen der Anbieter-Magazine als Marktwahrheit (Streuung dokumentiert, „verbindlich ist nur das Angebot").
- Behauptung zur Kassen-Übernahme der Dienstleistung (kein Beleg).
- Tresor als Malteser-Angebot (Absenz belegt das Gegenteil).
- Rechtsauskunft zur Notöffnungs-Kostentragung im Einzelfall (Urteilsberichte als Einzelfälle gekennzeichnet).
