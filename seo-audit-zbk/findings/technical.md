# Findings: Technical SEO — zuhausebleiben-kompass.de

Audit date: 2026-10-19 (evidence snapshot). Evidence: robots.txt, sitemap.xml, home-headers.txt, 34 crawled HTML pages, agentic-home.json, 2× Lighthouse (unlighthouse).

## Score: Technical SEO 78/100

## What works
- robots.txt valid (RFC 9309), `User-agent: * Allow: /`, includes `Sitemap:` directive; Lighthouse "robots.txt is valid" = pass.
- All 34 crawled pages: self-referencing canonical (exact URL match), `lang="de"`, `charset`, valid viewport `width=device-width,initial-scale=1`, no `noindex` meta anywhere.
- Real 404 handling confirmed by probe (status 404, no catch-all 200) — no soft-404 risk.
- HTTP/2, served via GitHub Pages + Fastly (cache-fra), `last-modified` + `etag` present, `age/x-cache` healthy.
- Consent-gated analytics: zero `gtag`/`googletagmanager`/`dataLayer` references in any of the 34 pages; only `consent.mjs` + cookieconsent assets load. No pre-consent third-party requests (GDPR-consistent).
- Content is fully server-rendered: 1,049 words in raw HTML on home, no JS shell.

## Findings
| # | Severity | Finding | Evidence |
|---|----------|---------|----------|
| T1 | High | `datenschutz.html` linked in the footer of all 34 pages but **absent from sitemap.xml and not captured by the crawl** — cannot confirm it exists/resolves; GDPR-critical page outside discovery surface. | index footer href vs sitemap URL list (34/34 diff, no datenschutz) |
| T2 | Medium | No security hardening headers: no HSTS, no `x-content-type-options`, no referrer-policy. GitHub Pages does not allow custom headers. | home-headers.txt |
| T3 | Low | `cache-control: max-age=600` applies to HTML (fine), but no evidence of hashed-asset long-cache; assets under `/assets/` unverifiable from evidence. | home-headers.txt |
| T4 | Low | Only `Vary: Accept-Encoding`; no `Vary: Accept` markdown negotiation (see geo.md). | agentic-home.json |
| T5 | Info | 12 `/region/*.html` + `regional.html` + `pflegegrad-beantragen.html` are indexable (no noindex, in sitemap) while holding 152–281 words — indexable thin content (detail in content.md). | page analysis |

## Recommendations
1. (T1, S) Publish/verify `datenschutz.html` and add it to sitemap.xml. Legal page must resolve before launch of any lead capture.
2. (T2, M) If staying on GitHub Pages, add `<meta name="referrer" content="strict-origin-when-cross-origin">`; for HSTS + custom headers, front the site with Cloudflare (free tier) — keeps GH Pages as origin.
3. (T5, M) Until region pages have real content, either `noindex,follow` them or expand (see content.md) — do not ship indexable 152-word placeholders on a new domain.
4. Keep the consent architecture as-is (no analytics tags before consent).

## Limitations
- No response-header captures for article pages (only home); asset caching unverified.
- No crawl of `datenschutz.html`, `/checklisten/*` (6 pages), or any 404 behavior beyond the probe.
- GitHub Pages uptime/redirect behavior (www vs apex, http→https) not probed in evidence.
