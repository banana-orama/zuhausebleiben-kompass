# Audit #6b + #10 (Rest) — og:image PNG ≥1200 px, twitter cards, referrer meta, Consent-Idle-Deferral

Datum: 2026-11-03 · Umsetzung: Commit 3bf52d1 · CI: 41646794446 (completed/success) · **Live-Readback: 20/20 ALL PASS (`research/verify_og_live_031126.py`)**

## Scope (aus seo-audit-zbk/SUMMARY.md, Top-10-Liste)
- **#6b (SC2-Rest):** PNG/WebP ≥1200 px als Google-taugliches Article-/OG-Bild (vorher nur SVG — nicht thumbnail-tauglich).
- **#10 agent-fähige Teile (P1/T2/V2):** Consent-Script-Deferral (TBT), `<meta name="referrer">`, og:image/twitter cards sitewide.
- **Nicht in diesem Lauf (offen, mit Grund):** HSTS/Custom-Headers via Cloudflare-Front = Betreiber-Kontoentscheidung (DNS-Änderung, keine Cron-Kompetenz); PSI-/CrUX-Felddaten (API 429 rate-limitet, wie schon im Audit); V1 „kompakter Consent-Erstbildschirm" = UX-Entscheid mit Consent-Rate-Messung; Organization-`logo` bleibt SVG (nicht audit-pflichtig, Logo-Programm erfordert ggf. Rasterformat — beobachten).

## Umsetzung
1. **OG-Asset:** `assets/images/og-zuhausebleiben-kompass.svg` (Design-Quelle, Markenpalette aus design.css) → Playwright-Render `assets/images/og-zuhausebleiben-kompass.png`. **1200×630 px verifiziert (sips + PNG-IHDR-Gate), 63,7 KB.** Inhalt: Wortmarke, Headline (Serif wie H1), Themen-Chips, schematische Treppe mit Treppenlift-Sitz auf Schiene; keine factual claims, keine KI-Foto-Imitation (Eigenzeichnung, schematisch).
   - **Vision-Kontrolle** (`research/evidence/perf-og-031126/og-render.png`): keine Textabschnitte, keine Element-Überlappungen, Sitz sitzt auf der Schiene, ruhige Typo.
2. **layout() in generate.mjs + build-checklists.mjs shell (identischer Head-Vertrag):** `referrer strict-origin-when-cross-origin`, `og:url` (= canonical), `og:type website`, `og:image` (absolut), `og:image:width/height/alt`, `twitter:card summary_large_image` — auf **allen 50 Seiten** beider Seiten-Generatoren.
3. **article-renderer.mjs:** Article-JSON-LD `image` jetzt Array `[og-PNG (absolut), Artikel-SVG]` — PNG first (Google-Thumbnail-tauglich), SVG bleibt in-situ-Illustration.
4. **consent.mjs Deferral:** CMP-Init (`CookieConsent.run`) läuft im ersten Idle-Fenster (`requestIdleCallback`, Timeout-Cap 1500 ms, `setTimeout`-250ms-Fallback für alte Safari-Versionen). Der **synchron-inlinierte Denied-Bootstrap (consent-default.js) bleibt unangetastet** — Consent-Semantik unverändert (keine optionale Messung ohne Auswahl; Measurement nur aus onConsent/onChange). Frühklicks auf die Footer-Buttons werden in der Capture-Phase gepuffert und nach der Init nachgespielt (`settings` → showPreferences, `withdraw` → withdrawConsent).

## Verifikation
- `node --check` auf generate.mjs, article-renderer.mjs, consent.mjs, build-checklists.mjs: OK.
- **Dauer-Gates erweitert:** test_site.py (50 Seiten: og:image absolut + 1200×630 + alt, twitter:card, referrer, og:url=canonical; PNG-Magic-Bytes + IHDR-Dimensionen ≥1200×630 aus dem dist-Artifact), test_articles.py (26 Artikel: Article.image = [PNG absolut, SVG]).
- `npm test` komplett Exit 0: beide Builds, test_site/test_articles/test_cross_links/test_titles_meta, Measurement-Build+Policy-Tests, **Playwright 20/20** (Consent: equal Buttons, Einstellungen, Widerruf, Persistenz, denied = 0 optionale Requests — Deferral bricht keinen Fluss), Partner-Gates A–F ALL PASS.
- **Funktionale Deferral-Probe** (`research/consent_timing_031126.mjs`): rIC feuert 96 ms, Banner-DOM 107 ms (Rect 189 px), Banner sichtbar, Buttons gleichwertig; **denied-State: 0 nicht-lokale Requests.**
- **Long-Task-Sonde** (`research/perf_probe_031126.mjs`, 4× CPU-Drossel, Mobil-Viewport): longtask ≥50 ms **0 vor und 0 nach** — keine Regression; der Audit-TBT (380–580 ms, Lighthouse-Simulation) ist lokal ohne Lighthouse-CLI nicht reproduzierbar. Die rAF-Gap-Messung ist headless unzuverlässig (Compositor-träge) und wird bewusst nicht als Delta behauptet.

## Bewusst offen (nicht als erledigt melden)
- **Lighthouse-Lab-Bestätigung der TBT-/SI-Verbesserung:** PSI-API weiter 429 (anonyme Tagesquota erschöpft, Evidenz `psi-after-home.json`); nach Deploy idealerweise 1 PSI-Lauf auf Home + 1 Artikel (oder Lighthouse in CI). CrUX bleibt bei junger Domain leer (P3-Hinweis des Audits gilt weiter).
- **HSTS/x-content-type-options:** nur via Cloudflare-Front (oder eigenem Header-fähigen Host) machbar → Betreiber-Entscheidung, unverändert.
- **Speed-Index-/V1-Thema „Consent besetzt Erstbildschirm“:** Deferral entschärft die Hauptthread-Konkurrenz, aber das modale Erstbild bleibt (UX-Entscheid, Consent-Rate vorher/nachher messen).

## Live-Readback (03.11., nach CI 41646794446 success)
`research/verify_og_live_031126.py` gegen die öffentliche URL: og.png 200 + image/png + **byte-identisch zum Repo** (sha256 4702eb28b891…, 63 680 B) + IHDR ≥1200×630; Home/Artikel/Checklisten tragen og:image (absolut), og:image:width/height/alt, twitter:card, referrer; og:url = canonical; Article-JSON-LD image[0]=PNG; `assets/consent.mjs` live enthält die Deferral-Logik (requestIdleCallback/earlyClicks) bei unverändertem Revision-2-Bootstrap; Sitemap unverändert 36 locs inkl. datenschutz. **20/20 PASS.**
