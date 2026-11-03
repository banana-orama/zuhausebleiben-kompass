# Audit #9 — pflegegrad-beantragen-Stub-Fold (03.11.2026)

## Finding und Re-Derivation gegen die LIVE-Site

- Quelle: seo-audit-zbk/SUMMARY.md Finding #9: „pflegegrad-beantragen.html stub (281 words):
  expand into the Antrag journey or fold into pflegegrad-antrag-ablauf-fristen."
- Live-Re-Check 03.11.2026 (curl, /tmp/pg-stub-live.html, /tmp/kosten-live.html):
  - Stub live: Titel „Pflegegrad: Wo Sie Unterstützung finden", robots **index,follow**, in der
    öffentlichen Sitemap, **3 kurze Generik-Abschnitte** (Anlaufstelle/Beratung/Keine-Einstufung),
    **vor-Launch-Prosa live sichtbar**: „Entwurf zur ersten Orientierung · Inhalte werden vor dem
    regulären Start fachlich und auf Quellen geprüft" + „Hinweis zum Entwurf"-Box. Genau der
    Flip-Prosa-Pitfall: die Launch-Umschaltung (15.10.) hat diese Legacy-Seite nie umgeschrieben.
  - Ziel-Guide pflegegrad-antrag-ablauf-fristen.html (content-ready, 26 Ratgeber-Bestand):
    Titel „Pflegegrad beantragen: Ablauf & Fristen", 8 Abschnitte über die komplette
    Antrag-Journey (formloser Antrag → Fristen/Fahrplan → Begutachtung → 5 Pflegegrade →
    Bescheid/Gutachten/Höherstufung → Widerspruch/Klage), 10 Quellen.
  - Inlinks: grep über alle dist-HTML → **0 interne Verweise** auf pflegegrad-beantragen.html
    (echte Orphan-Seite mit Sitemap-Slot, wie vorher die Region-Hubs).
  - Die 4 übrigen Legacy-Slugs (treppenlift-kosten/-zuschuss, bad-umbau-barrierefrei,
    treppenlift-firmen-vergleich) sind content-ready-Artikel und ersetzen ihren Zeile-31-Legacy-
    Körper per Pfad-Match (generate.mjs, completeArticles-Loop) — live ohne Entwurfs-Banner
    verifiziert. Der Stub ist die **einzige** Seite, die den Legacy-Körper behält.

## Entscheidung: Fold (nicht Expand)

Ein zweiter Antrag-Artikel unter dem Legacy-Slug würde dieselbe Suchabsicht (Head-Term
„pflegegrad beantragen") kanibalisieren; der Guide besitzt das Intent-Feld vollständig.
Der Stub hat 0 Backlinks/0 Inlinks — kein Equity-Verlust. Fold = Weiterleitungsseite:
`noindex,follow` + `<meta http-equiv="refresh" content="0; url=…/pflegegrad-antrag-ablauf-fristen.html">`
+ `rel=canonical` auf das Ziel + kurzer sichtbarer Handoff-Text (No-JS-Fallback) mit Button-Link.
Der strukturelle Sitemap-Filter („noindex kommt nie in die Sitemap") nimmt die URL automatisch
heraus — kein Sitemap-Handgriff nötig. Datenschutz-Notice der Seite unverändert bewusst entfernt
(Seite ist kein Artikel mehr); datenschutz.html behält seinen ehrlichen Entwurfs-Hinweis (keine
Rechtsfreigabe-Imitation), davon nicht berührt.

## Umsetzung (ein Commit)

- generate.mjs: `layout()` um `canonicalOverride`/`metaRefresh`-Parameter erweitert (Default null —
  alle anderen Seiten unverändert); `editorial`-Eintrag pflegegrad-beantragen entfernt; beide
  content.json-Artikel-Loops filtern den Slug; neue Weiterleitungsseite mit Handoff-Body.
- test_site.py: neuer Robots-Fall (Stub **muss** noindex bleiben), Sitemap-Exclusions-Assert,
  Meta-Refresh-/Canonical-Asserts gegen den Ziel-URL aus content.json, Launch-weites Verbot der
  Flip-Prosa „Entwurf zur ersten Orientierung".
- research/llms-txt.py: LEGACY_PAGES + load_legacy() + SECTION_MAP-Eintrag entfernt (Stub ist
  kein Content mehr); Hinweiskommentar mit Datum.
- research/verify_checklists_build.py: llms-Check gedreht (Stub muss **nicht** mehr in llms stehen).
- data/content.json unverändert (Legacy-Rohdaten bleiben Historie, Renderer nutzt sie für diesen
  Slug nicht mehr).

## Lokale Verifikation vor Push

- npm run build (PREVIEW) + build:launch: Exit 0.
- Stub LAUNCH: robots noindex,follow; refresh 0 → Ziel; canonical → Ziel; 1 H1; 0 Formulare;
  Flip-Prosa absent.
- Sitemap 36 locs (vorher 37), 0× pflegegrad-beantragen; llms.txt 0× pflegegrad-beantragen.
- npm test (volle Kette: beide Builds, test_site, test_articles 26, cross_links, titles_meta,
  measurement, Playwright consent, partner): Ergebnis im Commit-Text/launch-state.

## Offen / bewusst nicht getan

- GSC-Diagnose, ob Google den Stub bereits indexiert hat: weiterhin blockiert (keine
  Google-Sitzung im Cron). Egal wie der Index-Stand ist, lösen noindex+Refresh+Canonical beide
  Fälle; Re-Crawl-Kontrolle bleibt Teil des künftigen GSC-Zugangs.
- Rest-Audit-Einheiten: #6b (PNG ≥1200 px), #10 (Performance/og), danach Region-Ausbau als
  recherchierter Batch.
