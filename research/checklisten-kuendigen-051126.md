# Checklisten-Batch: hausnotruf-kuendigen (7. druckbare Checkliste) — 05.11.2026, Nachmittag

## Arbeitseinheit
Nächster Produktionsschritt laut Stand (memory + launch-state): druckbare Checkliste „Hausnotruf kündigen & wechseln" aus dem 28. Ratgeber (Briefing 17, live seit 05.11. früh). Link-Magnet-Workstream, keine neue Artikel-Produktion.

## Umsetzung
- `scripts/build-checklists.mjs`: neuer CHECKLISTS-Eintrag `hausnotruf-kuendigen` ( pageTitle „Checkliste: Hausnotruf kündigen", 31 Zeichen + Suffix 57 ≤ 65), Blöcke: table sec 1 (Vertragslage: 5 Situationen × Bedeutung), ul sec 4 (7 Brief-Bausteine), ul sec 7 (7 Absenden-Checks). Reihenfolge = Artikel-Logik (erst Vertrag, dann Schreiben, dann Absenden).
- Hub-Prosa 3× gebumpt: „Sieben Arbeitsblätter", JSON-LD-CollectionPage-Desc „Sieben druckbare Checklisten zu …, Hausnotruf kündigen, …", Meta-Desc der Hub-Seite (154 Zeichen ≤ 160).
- `tests/checklists.spec.mjs`: Map-Eintrag → Playwright testet die neue Seite automatisch voll (Content-Integrität gegen Article-JSON, Print-CSS, Consent-Contract, Mobile-Overflow).
- `research/verify_checklists_build.py`: Sitemap-Zähler 7→8 (inkl. Slug-Set), JSON-LD 6→7, Consent-Loop + blocks_cfg erweitert.

## Verifikation
- `npm run build:launch`: 48 Seiten, Sitemap 8 Checklist-URLs, 8 Checklisten-Seiten (7 + Übersicht).
- `research/verify_checklists_build.py` gegen LAUNCH-Dist: **ALL PASS** (inkl. neuer Consent-Contract-Check und 3 Content-Integritäts-Checks für hausnotruf-kuendigen; RSS 28 unverändert).
- `npm test` Exit 0 (beide Build-Modi, test_site, test_articles **28**, cross_links, titles_meta, Measurement, Playwright-Consent, Partner A–F).
- `npx playwright test tests/checklists.spec.mjs`: **8 passed** inkl. `hausnotruf-kuendigen: renders complete extracted content …` (61 ms).
- Visuell (Playwright-Chromium gegen lokalen Dist, Screenshots in cache/scratch, nicht committed): h1 korrekt, 3 Blöcke, 14 Abhak-Punkte, **Overflow 0 px** Desktop (1280) und Mobile (390); Vision-Kontrolle: Tabelle 2-spaltig vollständig, Kästchen sauber, keine Überlappungen, Consent-Banner mit gleichwertigen Buttons (Standard-Overlay über Hero, kein Defekt).

## Deploy + Live
- Commit gepusht; CI-Run: siehe launch-state-Eintrag (head_sha-Check über api.github.com).
- Live-Readback `research/verify_checklisten_kuendigen_live_051126.py`: robots index,follow, Canonical, 3 Blöcke, Quellen-Rücklink, Stand 2026-11-05, Hub 7 Karten + ItemList 7 Items, Sitemap 8 Checklist-URLs, RSS 28 unverändert, kein Tracking-Loader.
- IndexNow: 2 URLs (neue Checkliste + Hub) über api.indexnow.org, HTTP 200, Key-Datei live.

## Abgrenzung
- Keine neuen Zahlen, keine neuen Quellen — extrahiert ausschließlich aus dem freigegebenen 28. Ratgeber (Ledger 24/24 verbatim, Briefing 17). Zitations-Marker [1]–[9] fließen als Superscripts mit (verweisen auf die Quellenliste des Ratgebers).
- Kein Partner-Placement auf Checklisten-Seiten (druckbare Assets sammeln nichts; Consent-Contract-Assert).
