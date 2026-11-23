# Batch: treppenlift-eigentumswohnung-weg (Briefing 29, 23.11.2026, Cron 14:23)

**41. Ratgeber:** Treppenlift in der Eigentumswohnung — der Weg zum Beschluss nach § 20 WEG.

## Topic-Wahl (SERP-Gates, 23.11.)

Verworfen mit Beleg:
1. **Hilfsmittel-Ablehnung/Widerspruch** — VZ-Direktartikel + 6–7 dedizierte Seiten (sozialrecht-experten, pflege.de, bfs-ev-PDF, advocura, agito, neurocasemanagement); dieselbe institutionelle Dichte wie der bereits verworfene Pflegegrad-Widerspruch (26.10.).
2. **Badumbau-Mietwohnung (§ 554/554a BGB)** — 5 dedizierte Seiten (pflege.net 05/2026, pflegedusch mit Musterbrief 01/2026, anwalt.de 06/2026, ra-kotz Urteilsaufbereitung, barrierefreie-immobilie 11/2026) + § 554 bereits im Bestand (mietwohnung 9×, tuerbreiten 4×, wohnumfeld, wanne, bodengleiche-dusche).

Gewählt: **WEG/Eigentumswohnung** — Zielgruppe Eigentümer (nicht Mieter), eindeutig intent-distinct zum Schwester-Artikel treppenlift-mietwohnung (WEG dort nur als 2-Satz-Teaser „dann gilt das Wohnungseigentumsgesetz"). SERP-Dichte (23.11., Such-API): „treppenlift eigentumswohnung beschluss" 7 dediziert (davon 3 frisch < 6 Wochen: checkfox 16.11., siemer 23.10., tlgurus 25.09.), „treppenlift WEG zustimmung" 5, „badumbau eigentumswohnung WEG" 5, **„barrierefreier umbau eigentumswohnung" 1 (dünnster Cluster)**. Belegte Lücke: kein Wettbewerber kombiniert BGH-2024-Standards + copy-paste-Beschlussantrag + Förder-/Reihenfolge-Kette + Rückbau/Versicherung + Mieter-Pfad; Herstellerseiten stalen (HIRO basiert auf DDIVaktuell 06/2017 = vor der Reform, TKE zitiert altes § 22 WEG, weg-wissen empfiehlt ärztliche Atteste entgegen BGH 09.02.2024). Kaufnähe: Beschluss vor Aufmaß/Angebot; payable events beider Cluster (Lift + Bad).

## Recherche

Zwei Subagents (legal + market), Evidenz `research/evidence/weg-231126/`:
- **Ledger legal:** 35 Zitate über 7 offizielle Dokumente, 35/35 maschinell verbatim (`raw/verify_extracts.py`).
- **Ledger market:** 25 Zitate über 10 Quellen, verbatim-geprüft (`raw/market/verify_ledger.py`).

**Shortcode-Korrektur:** WEG auf gesetze-im-internet = `woeigg` (nicht `wegg`/`weg`, beides 404); Fassung Bek. v. 12.01.2021 (WEMoG, ab 01.12.2020), zuletzt geändert Art. 1 G v. 10.10.2024 (Nr. 5 „Steckersolargeräte").
**V ZR 244/22 offizielles PDF:** Namensschema `V_ZR_244-22.pdf` (EIN Unterstrich) nur über die BGH-Entscheidungssuche auffindbar; Doppel-Unterstrich-Varianten → 404/Soft-404 (200 mit text/html).

## Eltern-Verifikation (Pflicht, gegen Live-Originale)

`research/verify_weg_parent_231126.py`: 35/35 Ledger-Zitate literal in den bereinigten Rohdateien + Live-Needles heute auf § 20/21/44 (woeigg) und BGH-PM 026/2024. Erster PM-Fetch rc=35 (SSL, transient) → Retry HTTP 200 mit allen 3 Needles (Ein-Retry-Regel).
**Nicht verwendet:** V ZR 140/22 („Beschlusszwang") und VIII ZR 234/23 („70 dB") — von checkfox zitiert, von uns NICHT primär verifiziert (Entscheidungssuche ohne PDF-Treffer in diesem Lauf) → 0 Vorkommen im Artikel, dokumentiert als Absenz (Content-Gate assertet 0×).

## Artikel

7 Abschnitte, 6 FAQs, Tabelle (beide BGH-Verfahren), 14 Quellen (alle checked_at 2026-11-23), SVG-Entscheidungspfad (`treppenlift-weg-entscheidung.svg`, KI-Illustration). Kernverbesserungen ggü. Feld:
1. BGH-Leitsätze wörtlich aus den offiziellen PDFs (kein Portal-Echo): einfache Mehrheit, Mehrheit darf trotz Zweifel gestatten, Stattgebungsbeschluss nur über § 20 Abs. 4 angreifbar, Regel-Ausnahme-Verhältnis, persönliche Angewiesenheit „ohne Belang" (V ZR 244/22 Rn. 18), Kosten ohne Einfluss auf den Anspruch (Rn. 24), Bauordnungs-Grenze (Rn. 33/35), Grundlagen-/Ausführungs-Split (Rn. 8/34).
2. Beschlussantrag-Checkliste, die diese Standards direkt in den Mustertext übersetzt (Dauerhaftigkeit der Gestattung, Ob/Wie-Trennung, § 21-Abs.-1-Kosten+Rückbau, Bauordnungs-Vorbehalt).
3. Dokumentierte Divergenzen: weg-wissen-Attest-Empfehlung (10/2026) vs. BGH 02/2024; HIRO-Beitrag als vor-Reform-Stand gekennzeichnet (Quellenlinie); checkfox-150–300-€-Wartung nur als Portalangabe mit Interessenkennzeichnung.
4. Ehrliche Grenze: beide BGH-Entscheidungen betrafen Aufzug/Terrasse, keinen Treppenlift (im Artikel markiert).

## Renderer-Fix (Nebenfund, Fehlerklasse geschlossen)

`table.note` wurde im Artikel-Renderer stillschweigend gedroppt (nur regionBody renderte es) — dieser Batch war der erste Artikel mit Tabellen-Note; ohne Fix wäre der Artikel truncatet bei grünen Gates gegangen. Fix: `<span class="tbl-cap">` nach dem table-scroll (Same-Commit), Content-Gate assertet die Note jetzt.

## Gates

- Content-Gate `research/verify_weg_content_231126.py`: **130/130 PASS** (Needles tag-/citation-normalisiert, Coverage aller JSON-Keys inkl. paragraphs_after/Tabellenzellen/FAQ-Antworten, [1]–[14] Marker ↔ Anker, Related-Reihenfolge mietwohnung→wohnumfeld→kosten, Early-CTA → firmen-vergleich „Anbieter für den Einbau vergleichen", Absenzen: V ZR 140/VIII ZR/4.180/16.720/6.250/awin/Partner-Marker/Entwurf-Prosa/Em-dash im JSON).
- SVG: getBBox-vs-viewBox 0 Overflows, text-pairwise 0, **neu: Box-Pairwise 0** (`research/svg_check_weg_231126.mjs`) — der Box-Check wurde NACH dem ersten Vision-Fund ergänzt (Box B/C kollidierten mit D2/E; Layout umgebaut, zweite Vision-Prüfung: keine Fehler). Screenshot-Hang von SVG-Dokumenten in Playwright → qlmanage-Fallback.
- Mobile 390 px: **0 px Overflow** (`research/mobile_check_weg_231126.mjs`), Tabelle im scroll-Wrapper, Consent-DOM vorhanden.
- `npm test` komplett **Exit 0**: 66 Seiten, Sitemap **54 locs**, **41 Artikel** (Counter-Bump im selben Commit), RSS 41, test_cross_links 3 Related je Artikel, titles/meta, Playwright 21 ✓, Partner-Gates A–F ALL PASS.
- llms.txt: neuer Eintrag SUMMARIES + SECTION_MAP (Build-Throw-Regel: ohne Eintrag bricht der Build).

## Verifizierungen mit Datum

- § 20 WEG (woeigg): Abs. 1/2 (Nr. 1–5 inkl. Steckersolargeräte-Stand 2024)/3/4 verbatim — 23.11.2026.
- § 21 WEG: Abs. 1 Satz 1+2, Abs. 2 (⅔-Stimmen + ½ MEA / Amortisation), Abs. 5 — 23.11.2026.
- § 44 WEG: Anfechtungs-/Beschlussersetzungsklage — 23.11.2026.
- BGH V ZR 244/22 + V ZR 33/23 (offizielle PDFs) + PM 026/2024: Leitsätze und Rn. 8/15/18/24/33/34/35 bzw. LS a–c/Rn. 15/18/19/22 — 23.11.2026.
- Hersteller/Portal-Angaben (Lifta, HIRO, TKE, VZ Stand 20.01.2026, checkfox 16.11.2026, weg-wissen 27.10.2026, siemer 23.10.2026, nullbarriere 02.11.2026): 23.11.2026, Interessenkennzeichnung im Artikel.

## Deploy

Commit `e68a9d6` (volle SHA e68a9d6aefd2c51dba7fc82d1a24b7c370718705), Push e415497..e68a9d6 fast-forward, **CI-Run 45191006551 success**, **Live-Readback 34/34 ALL PASS** auf der öffentlichen URL (`research/verify_weg_live_231126.py`: 200 ab Poll 1, robots index,follow, Canonical, Kernwortlaute inkl. BGH-Verbatim live, Related-Reihenfolge mietwohnung→wohnumfeld→kosten, CTA → treppenlift-firmen-vergleich, SVG 200 mit „WEG-Beschluss nach § 20", Sitemap exakt 54 locs inkl. Artikel, RSS 41, llms.txt, Homepage-Verlinkung, Absenzen 0× (V ZR 140/VIII ZR/4.180/6.250/Partner-Marker/Entwurf-Prosa), Impressum-USt-IdNr. live), **IndexNow HTTP 200** (2 URLs: Artikel + Homepage).
