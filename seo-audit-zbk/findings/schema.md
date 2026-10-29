# Findings: Structured Data — zuhausebleiben-kompass.de

Evidence: JSON-LD extraction from all 34 pages; Lighthouse structured-data audit; details/summary census.

## Score: Schema 42/100

## Current implementation
- Exactly **1 JSON-LD block per article page** (18 pages), `@graph` with `Article` + `BreadcrumbList`. Parse-valid everywhere (0 errors).
- **Zero JSON-LD on 16 pages**: home, regional hub, all 12 region pages, pflegegrad-beantragen, impressum. No sitewide `Organization`/`WebSite` graph at all.
- No other types anywhere: no FAQPage, no WebPage, no Person, no ListItem searchAction.

## Findings
| # | Severity | Finding | Evidence |
|---|----------|---------|----------|
| SC1 | High | **FAQPage schema missing sitewide despite 104 implemented FAQs.** `<details>/<summary>` census: 104 details elements on 34 pages — 101 on the 18 articles (4–6 each), 3 on home. Extracted summaries are genuine questions ("Wie viel kostet ein Treppenlift inklusive Einbau?" — 4/4 question-form on sampled page). The content is FAQ-ready; only the schema layer is missing. This is the single largest schema gap and the easiest rich-result win. | details census; JSON-LD types |
| SC2 | Medium | `Article` nodes are **minimal**: no `datePublished`, no `dateModified`, no `author`, no `image` in Google-usable format — the image given is an SVG (not eligible for article thumbnails; Google wants JPG/PNG/WebP ≥1200px for discoverable preview). | treppenlift-kosten.jsonld |
| SC3 | Medium | No sitewide `Organization` + `WebSite` graph on home (publisher name/logo/url exist only inside Article nodes). Kills Knowledge-panel/KG-seeding and sitelinks searchbox eligibility. | index has 0 ld+json |
| SC4 | Low | `BreadcrumbList` is only 2 levels (Startseite → page) even where a hub exists (regional → region pages; Ratgeber tier). Consistent, but under-uses hierarchy; no visible breadcrumb element on region pages ("Startseite / Ratgeber" exists on articles — mismatch between visible trail and schema depth is minor here). | jsonld |
| SC5 | Low | Region pages: no `WebPage`/`BreadcrumbList`, nothing. If they stay indexable, they at least deserve WebPage+Breadcrumb; if thin, see content.md. | page analysis |
| SC6 | Info | Lighthouse "Structured data is valid" returned score=None (no validator errors detected on the 2 crawled pages) — current markup parses cleanly. | lighthouse.json |

## Recommendations
1. (SC1, M) Generate `FAQPage` JSON-LD from the existing `<details>/<summary>` pairs at build time (summary → `name`, following `<p>` → `acceptedAnswer.text`). 101 FAQs across 18 pages in one template change. Expect FAQ rich results to take weeks; validate with Rich Results Test after deploy.
2. (SC2, S) Enrich Article: `datePublished`/`dateModified` (build timestamps exist — Quellenstand dates are already in the page), `author: {"@type":"Organization"}` or a Person entity, and a PNG/WebP OG-style image ≥1200px (also fixes the missing og:image).
3. (SC3, S) Add sitewide graph on home: `Organization` (name, url, logo, sameAs when available) + `WebSite`.
4. (SC4, S) Extend BreadcrumbList to reflect the real hierarchy (Startseite → Ratgeber → article; Startseite → Regionen → Bundesland).

## Limitations
- No Rich Results Test / Schema.org validator was re-run live (only Lighthouse's built-in check on 2 pages); parse-validity is confirmed, Google-eligibility after fixes is a projection.
- SVG-as-article-image eligibility is based on Google's image guidelines; Google may still sometimes use SVG — treat as high-probability, not measured.
