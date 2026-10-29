# Findings: XML Sitemap — zuhausebleiben-kompass.de

Evidence: sitemap.xml (snapshot 2026-10-19), crawl diff against 34 captured pages.

## Score: Sitemap 82/100

## Structure
- 34 URLs, exact 1:1 match with the 34 crawled pages (no orphans, no crawl-misses inside the set). XML valid, correct namespace, UTF-8.
- URL set: home (1), articles (18), region hub (1), region pages (12), impressum (1), plus stub `pflegegrad-beantragen.html` (1).
- Referenced from robots.txt (`Sitemap:` directive) — discoverable.

## Findings
| # | Severity | Finding | Evidence |
|---|----------|---------|----------|
| S1 | High | **6 checklisten pages absent.** No `/checklisten/*` URL in sitemap; additionally zero `<a href>` to any checklisten URL across all 34 crawled pages (the word "Checklisten" appears only as print-button/CTA copy). If those pages exist in the repo, they are **complete orphans**: not in sitemap, not linked, not crawlable in practice. | sitemap diff; href scan = 0 hits in 34 files |
| S2 | High | `datenschutz.html` missing (footer-linked from every page). | footer href vs sitemap |
| S3 | Medium | No `<lastmod>` on any URL. Google explicitly reads lastmod; without it, recalculation of crawl priority is left to guesses. | sitemap.xml (0 lastmod tags) |
| S4 | Low | No `priority`/`changefreq` — acceptable (Google ignores changefreq; priority is weak) — informational only. | sitemap.xml |
| S5 | Info | Thin placeholders (12 regions + regional + pflegegrad-beantragen) are submitted for indexing while holding 152–281 words — quality-gate risk on a young domain. | word counts |

## Recommendations
1. (S1, S) Generate sitemap from the build so new sections (checklisten) are included automatically; wire checklisten pages into article CTAs ("Fragenliste zum Ausdrucken" → checklisten page) before submission.
2. (S2, S) Add datenschutz.html.
3. (S3, S) Emit real `<lastmod>` from git/file mtimes at build time; update only on content change, never on rebuild.
4. (S5, M) Apply the quality gate: no URL enters the sitemap until it has substantive unique content (or set noindex until then).

## Limitations
- Crawl was sitemap+seed based (34/34 match) — sitemap-absent URLs (datenschutz, checklisten) were only found via href scan; their live status is unknown, not proven missing.
