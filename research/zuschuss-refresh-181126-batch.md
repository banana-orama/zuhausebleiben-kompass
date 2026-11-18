# Batch-Protokoll: Money-Page-Refresh treppenlift-zuschuss (18.11.2026, Cron-Lauf)

**Art:** Verbesserung eines Kernartikels (blitz-seo-Plan Phase 1, Item „Proof-Upgrade: Ampel-Tabelle Antragswege"), kein neuer Artikel. 39 Ratgeber unverändert.

## Was geändert hat
1. **Neue Sektion 2 „Förderstatus heute: Was ist beantragbar?"** in content-ready/treppenlift-zuschuss.json: Intro-Absatz mit Abrufdatum (18. November 2026), Status-Tabelle über 4 Wege (Pflegekasse § 40 Abs. 4 offen/Ermessen 4.180 €; KfW 455-B gestoppt mit KfW-Wortlaut „Diesen Zuschuss können Sie nicht mehr beantragen" verbatim; KfW 159 offen als Kredit mit Fachunternehmen/Vor-Vertragsabschluss/Haushaltsmittelvorbehalt; Landesprogramme je Bundesland unterschiedlich mit Beispiel-Beträgen NRW 220.000 €/Bayern 10.000 € leistungsfrei), Absatz nach der Tabelle (Region-Ratgeber als vertiefte Quelle, bundesweiter Weg als Startpunkt).
2. **Renderer-Feature:** Inline-Links in Artikeldaten — `[Label](/pfad.html)`-Syntax in txt() (article-renderer.mjs), Regex-Pfad-Whitelist (`INLINE_LINK_HREFS`, Build-Throw bei unbekanntem Ziel oder Zitierstil-Label), läuft VOR der Zitations-Ersetzung (`[\d+]` kollidiert nicht: reine Ziffern-Labels werden verworfen). Erste Nutzung: NRW + Bayern Region-Links in der Money-Page (Region-Pages hatten zuvor nur den noindex-Hub als Inlink).
3. **Quellen:** [1] § 40 SGB XI, [2] KfW 455-B, [3] KfW 159 heute (18.11.) live re-verifiziert → checked_at 2026-11-18. Neu [6] NRW.BANK „Barrierefrei umbauen" + [7] StMB „Barrierefreies Wohnen" (je geprüft 18.11.). [4] BMG + [5] § 554 BGB unverändert (nicht neu abgerufen). Quellenstand-Meta folgt sources[0] → 2026-11-18; Article dateModified ebenfalls.
4. **Datums-Konsistenz:** 455-B-Prosa („wurde am 18. November 2026 direkt abgerufen und geprüft") + 455-B-FAQ-Antwort auf heute gestellt (tatsächlicher Re-Abruf heute, verbatim-geprüft); „16. November 2026" launch-weit 0× (Gate-Absenz).

## Live-Verifikation (18.11.2026, Ledger 22/22 PASS)
`research/verify_zuschuss_refresh_181126.py` über Evidenz `research/evidence/zuschuss-refresh-181126/` (Fetch: research/fetch_zuschuss_refresh_181126.sh, 8/8 HTTP 200, 1× Retry-Logik; Roh-HTML uncommitted):
- § 40 SGB XI (ISO-8859-1-Pipeline): „4 180" ×2, „16 720" ×1, „subsidiär", „wohnumfeldverbessernden Maßnahmen"
- KfW 455-B: „Diesen Zuschuss können Sie nicht mehr beantragen" verbatim ×1, „ausgeschöpft" ×1, „2027" ×1 — Stopp unverändert seit 13.11./16.11.
- KfW 159: „50.000 Euro" ×3, „Die Arbeiten müssen von einem Fachunternehmen durchgeführt werden", „Eigenleistungen sind nicht förderfähig", „Die Förderung steht unter dem Vorbehalt verfügbarer Haushaltsmittel", „Ein Rechtsanspruch hierauf besteht grundsätzlich nicht", „Sprechen Sie vor dem Abschluss von Lieferungs- oder Leistungsverträgen oder dem Kaufvertrag mit einem Finanzierungspartner" (alle Soft-Hyphen-normalisiert, KfW nutzt U+00AD)
- NRW.BANK: „Eigentumsförderung - Modernisierung" + „Zinsgünstige Darlehen bis 220.000 € mit einem Finanzierungsanteil von bis zu 100%" verbatim
- StMB: „leistungsfreien Baudarlehen von bis zu 10.000 Euro" verbatim + Antrag bei Landratsamt/kreisfreier Stadt
- Probe-Skripte 1–4 dokumentieren die Needle-Findung (Soft-Hyphen-Falle: roher grep meldete „Fachunternehmen" falsch).

## Gates
- Content-Gate `research/verify_zuschuss_refresh_content_181126.py`: **44/44 PASS** (LAUNCH-dist: alle JSON-Keys der neuen Sektion inkl. 12 Tabellenzellen, Inline-Links absolut, Quellen 6/7 mit Ankern, Quellenstand, 9 Abschnitts-Anker, JSON-LD parse + dateModified 2026-11-18 + FAQ-Schema-Datum, Absenzen: 0× data-partner-placement/sponsored/awin1/„4 180"/„16. November 2026")
- Mobile `research/verify_zuschuss_refresh_mobile_181126.py`: 390 px Overflow **0 px**, Status-Tabelle im Scroll-Container, 2 Region-Links; Screenshot-Sichtkontrolle (Vision) sauber — Tabelle vollständig lesbar, keine Überlappungen/Abarschnitte
- `npm test` EXIT 0 (beide Build-Modi, test_site, test_articles 39, cross_links, titles_meta, measurement, Consent-Playwright, Partner-Gates A–F ALL PASS)
- verify_checklists_build ALL PASS gegen LAUNCH-dist (RSS 39, Sitemap unverändert 52 locs)
- SVG unverändert (foerderablauf.svg)

## Deploy
Commit + Push + CI + Live-Readback + IndexNow: siehe launch-state 18.11. (dort nachtragen).
