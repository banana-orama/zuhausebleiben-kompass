# Findings: Visual / Mobile Readiness — zuhausebleiben-kompass.de

Evidence: Lighthouse mobile screenshots + full-page screenshots (2 pages: hausnotruf-sturzerkennung-oder-knopf, hilfsmittel-pflegekasse-uebernahme), viewport/a11y audits, HTML meta census on 34 pages.

## Score: Visual 84/100

## What works
- **Mobile-first rendering confirmed in the capture** (~412px viewport): single column, logo + 3-item nav (Treppenlift / Bad-Umbau / Förderung), no horizontal overflow, no truncated text, no overlapping elements.
- **Senior-readable typography**: large body text, high contrast (dark green on white), generous spacing, full-width buttons — matches the trust-first older-adult audience better than most competitors.
- Accessibility category score **1.0** on both crawled pages; `image-alt` pass, tap-target and viewport audits pass (no `user-scalable=no` — pinch-zoom stays available, important for older eyes).
- Identical template on all 34 pages (same viewport meta, same inline CSS) → visual findings generalize to the article set with high confidence.

## Findings
| # | Severity | Finding | Evidence |
|---|----------|---------|----------|
| V1 | Medium | **The consent dialog owns the entire first mobile screen** ("Ihre Privatsphäre zählt" with 3 stacked full-width buttons). GDPR-correct, but first-time mobile visitors see zero content until interaction; contributes to the slow Speed Index (3.9–4.4 s). Consider a shorter first-screen consent (2 buttons + link) with "Einstellungen" behind it. | screenshot.jpeg |
| V2 | Low | No `og:image` / twitter-card tags anywhere → links shared in WhatsApp/Facebook (a primary sharing channel for the relatives persona) render as bare text. | meta census |
| V3 | Low | Above-the-fold on desktop (full-page screenshot) is headline + intro card; the article's actual value (price example) sits below several sections — acceptable, but the fold could carry the key number or TOC. | full-screenshot.jpeg |
| V4 | Info | SVG illustrations only (e.g. treppenlift-planung.svg): crisp and lightweight, but the design has no photography of real stairs/bathrooms — on a trust portal, one real image per article would lift perceived credibility. | img census (1 image/page) |

## Recommendations
1. (V2, S) Add og:image (1200×630 PNG/WebP) + og:url, og:type, twitter:card=summary_large_image sitewide — same asset needed for schema SC2 anyway.
2. (V1, M) Compact consent first screen; remember-choice badge; measure consent-rate before/after.
3. (V4, M) Plan one authentic photo per topic cluster (can be licensed); keep SVGs for diagrams.
4. (V3, —) Optional: add an in-page TOC ("Was Sie hier erfahren") under the H1 — helps seniors and featured-snippet eligibility alike.

## Limitations
- Visual evidence = 2 pages of 34 (identical template mitigates but does not prove).
- No tablet/4K render, no real-device testing, no readability metrics (Flesch) — qualitative assessment from captures.
