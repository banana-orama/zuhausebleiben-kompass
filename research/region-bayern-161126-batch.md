# Batch 25 (2026-11-16): Region Bayern als zweite Region live — Protokoll

## Was diese Einheit ist (und was nicht)
Region-Ausbau nach dem expand-or-noindex-Muster (wie NRW, 13.11.) — kein neuer Ratgeber. Vorher liefen die üblichen SERP-Gates für Ratgeber-Kandidaten; alle vier Kandidaten fielen durch (mit Beleg dokumentiert in `research/serp-gates-161126.md`-Abschnitt unten und launch-state).

## Pipeline
1. **SERP-Gates (Artikel-Kandidaten):** treppenlift-kurve (8/10 Preisvergleichsseiten), badewanne-oder-dusche (dedizierter pflege-panorama-Guide + Aroundhome-Eigenseite), hausnotruf-ohne-vertrag (1 dedizierter Artikel + 8 Shops; steht zudem quer zur Malteser-Abo-Route), rollstuhlrampe (3 dedizierte Seiten auf dem §40-Pfad + Bestand-Overlap türen/hilfsmittel) — alle verworfen.
2. **Subagent-Recherche Bayern** (bounded): 34 Roh-Extrakte + QUOTES.md, selbstlaufender Verbatim-Check 141/141.
3. **Eltern-Verifikation (dieser Lauf, gegen Live-Originale):**
   - StMB-Programmseite live: „leistungsfreien Baudarlehen von bis zu 10.000 Euro“ + Auswahl „nach der sozialen Dringlichkeit der Anträge“ ✓ (curl)
   - Art. 11 BayWoFG: 28 300/43 200/10 700/3 200 € wörtlich (raw-05); Achtung: Gesetzestext mit Leerziffern — `grep "28.300"` matcht regex-wildcard und gibt falsche Treffer (bekannter SGB-Pitfall); Seite nutzt gepunktete Prosa, Gate-Nadeln = Prosa-Schreibweise
   - § 113 Abs. 2 Nr. 1 + § 77 SGB IX wörtlich (raw-27/28) ✓; EH-Antrag formlos (BayernPortal raw-11) ✓
   - WFB 2022 Teil 4: Darlehen ≤ 10 000 €/Fehlbedarfsfinanzierung/Bagatellgrenze 1 000 €/1 v. H./5 Jahre Belegungsbindung/Pflegegeld+Blindengeld/nur-prioritäre-Finanzierung (QUOTES 335–351, maschinell verbatim) ✓
   - **Korrektur des Subagent-Berichts:** „Erlass nach 5 Jahren Belegungsbindung“ ist NICHT belegt (raw-26 hat nur Belegungsbindung) → Seite schreibt nur die Belegungsbindung; „Stufe III“-Glossierung entfernt; „anrechenfreie Beträge“-NRW-Pendant als nicht gefunden dokumentiert (eigener FAQ-Absatz)
   - SeLA live: „bis zu 40.000 Euro über maximal zwei Jahre“ ✓ (curl); Pflegestützpunkte „kostenlose Beratung … offen“ ✓ (raw-30); „rund 100 Wohnberatungsangebote, … unterschiedlich ausgestaltet“ ✓ (raw-29) — **kein „kostenlos“-Claim für die 100 Angebote** (nicht belegt), kostenlos nur für Pflegestützpunkte
   - KfW 455-B Stopp-Wortlaut + 2027-Bedingung (raw-19, konsistent mit dem KfW-Refresh-Lauf 16.11. vormittags) ✓; Kredit 159: 50.000 €, Treppenlifte im Maßnahmenkatalog, Kombinations-Hinweis wörtlich übernommen (raw-20) ✓; **0 Zinszahlen auf der Seite** (Volatilitäts-Politik wie NRW)
   - LfA Förderbank = Wirtschaftsförderung, kein Wohnraumprogramm → bewusst nicht als Weg dargestellt
4. **Renderer:** REGION_CONTENT lädt jetzt data/region-*.json-Liste (neue Region = nur JSON-Datei); hubTeaser datengetrieben über `teaser`-Feld (NRW-Teaser in die NRW-JSON migriert); Hub-Prosa auf zwei Regionen aktualisiert; 10 Platzhalter-Regionen + Hub bleiben noindex,follow außerhalb der Sitemap.
5. **Gates:** test_site auf generisches expand-or-noindex-Gate umgestellt (alle data/region-*.json indexierbar-pflichtig, Sitemap = genau die ausgebaute Menge); Content-Gate `verify_region_bayern_content_161126.py` 73/73 (Kernzahlen, §-Wortlaute, KfW-Zitate, Treppenlift-Absenz-Transparenz, 0× §40-Beträge/Partnermarker/LVR/LWL/NRW.BANK, 17 Quellen checked 16.11., CTA/Related-Ziele, Hub-Spiegel, Sitemap 51 locs, keine Platzhalter-Prosa); Mobile 390 px 0 px Overflow + Tabelle scrollt im Container + FAQ toggelt (`verify_region_bayern_mobile_161126.py`); npm test EXIT 0 (63 Seiten LAUNCH/51 locs, 38 Artikel, cross-links, titles, Playwright 21, Partner A–F).
6. **Deploy + Live-Readback + IndexNow:** siehe launch-state-Eintrag dieses Laufs.

## Grenzen der Seite (bewusst)
- Keine Zinssätze (KfW-Volatilität), keine §40-Beträge (nur Verweise auf die Ratgeber), kein „anrechenfreie Beträge“-Analogon (nicht belegbar), keine Treppenlift-Zusage im Landesprogramm (nicht namentlich genannt), Bezirks-Höhen als Einzelfall, Digitale Wohnberatung Bayern nur als gekennzeichnete Kontextquelle.
