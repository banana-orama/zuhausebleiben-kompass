# SEO Audit Summary — zuhausebleiben-kompass.de

- **Audit date:** 2026-10-19 (evidence snapshot; analysis completed 2026-10-29)
- **Scope:** static GitHub Pages lead portal, live since 2026-10-15 · 18 articles · 12 region pages + regional hub · home · impressum · 34 URLs crawled = 34 sitemap URLs (1:1)
- **Method:** analysis of the existing evidence pack only (no re-crawl, no site changes). Role findings in `findings/*.md` (technical, sitemap, performance, content, schema, visual, geo, agentic, sxo).
- **Business type:** national informational lead portal (pre-launch: no lead capture, declared "Ratgeber im Aufbau" sitewide)

## SEO Health Score: **70 / 100**

| Category (weight) | Score | Basis |
|---|---|---|
| Technical SEO (22%) | 80 | technical 78 · sitemap 82 |
| Content Quality (23%) | 71 | content.md |
| On-Page / SXO (20%) | 66 | sxo.md (SXO Gap Score 66) |
| Schema (10%) | 42 | FAQPage gap, minimal Article |
| Performance (10%) | 80 | lab-only, 2 pages |
| AI Search Readiness (10%) | 66 | geo 58 · agentic 74 |
| Images/Visual (5%) | 84 | visual.md |

A technically excellent, honestly labeled young site. The score is capped by four fixable things: the missing FAQPage layer, a failed llms.txt deployment, orphaned checklisten pages, and indexable thin placeholders.

## Top 10 prioritized fixes

| # | Fix | Impact | Effort | Where |
|---|-----|--------|--------|-------|
| 1 | **FAQPage JSON-LD for the 101 article FAQs** — generate from existing `<details>/<summary>` at build (summaries are already question-form) | High (rich results, AI answers) | M | schema.md SC1 |
| 2 | **Deploy /llms.txt — currently HTTP 404.** The dist file was never published; the "llms.txt" evidence file is the GitHub 404 page. Publish to root, verify 200/text-plain | High (GEO + Lighthouse agentic fraction) | S | geo.md G1 |
| 3 | **Un-orphan the 6 checklisten pages**: zero `<a href>` to them on any of 34 pages + absent from sitemap. Link them from the article CTAs that already promise "Checklisten" | High (funnel + discovery) | S | sitemap.md S1, sxo.md X1 |
| 4 | **Add datenschutz.html to sitemap + verify it resolves** — footer-linked from all 34 pages, absent from sitemap and crawl | High (legal/GDPR) | S | technical.md T1 |
| 5 | **Region pages: expand or noindex** — 12 pages at exactly 152 words, indexed on a 2-week-old domain. Real content (Landesprogramme, Pflegestützpunkte) or `noindex,follow` until ready | High (quality-threshold risk) | M | content.md C1 |
| 6 | **Enrich Article schema**: datePublished/dateModified, author, and a PNG/WebP image ≥1200px (current SVG not thumbnail-eligible) | Med-High | S | schema.md SC2 |
| 7 | **Trim 17/18 titles to ≤65 chars; fix 4 over-long meta descs** (incl. pflegegrad-beantragen's 242-char disclaimer-as-snippet) | Medium | S | sxo.md X3/X4 |
| 8 | **Sitewide Organization + WebSite JSON-LD on home** (index currently has zero structured data) | Medium | S | schema.md SC3 |
| 9 | **pflegegrad-beantragen.html stub (281 words)**: expand into the Antrag journey or fold into pflegegrad-antrag-ablauf-fristen | Medium | S | content.md C1 |
| 10 | **Performance polish + headers**: defer consent script (TBT 380–580 ms, SI 3.9–4.4 s), add referrer meta / HSTS via Cloudflare front, og:image/twitter cards | Medium | M | performance.md P1, visual.md V2, technical.md T2 |

## Quick wins (≤1 day combined)
1. Publish llms.txt (fix #2) — minutes, restores an entire audit dimension.
2. FAQPage generator on the details/summary pattern (fix #1) — one template change, 101 FAQs.
3. Sitemap regeneration with datenschutz + checklisten + `<lastmod>` from build timestamps (fixes #4, #3-half, S3).
4. Title/meta trims (fix #7) — pure copy edits on 18 files.
5. og:image + twitter card sitewide (fix #6/10 overlap) — one shared asset.

## What the evidence cannot prove (honesty box)
- **No real-user CWV exists**: PSI API call failed (rate limit — psi-treppenlift-kosten.json holds only the error) and the domain is too new for CrUX. All performance conclusions are Lighthouse lab data from **2 of 34 pages**; INP unmeasured (TBT is a proxy).
- **Index status unverifiable**: no GSC/API data in evidence. The 6 checklisten pages and datenschutz.html were never crawled — their live existence is unknown (the audit proves only that they are unreachable from sitemap and internal links).
- **SERP analysis**: 2 probes × 5 results, ads-dominated money SERP — directional, not statistical.
- **Content accuracy** (4.180 €, KfW conditions): not re-verified against primary sources; article source lists carry "geprüft" dates only.
- llms.txt **quality** unassessable — the URL served a 404; the task's assumption that it was integrated is contradicted by the snapshot.

## Insurance-adjacent risk flags (operator context)
- Disclaimers are already strong and specific ("keine Versicherungsberatung", "keine Verbindung zu einem Versicherungsunternehmen") — preserve verbatim as content scales; GKV/Pflegekasse topics must stay Leistungsrecht-orientation, never policy recommendation.
- Pre-launch claims ("Es werden noch keine Angebote vermittelt") appear on every page; when Angebotsvermittlung launches, update **all** of them simultaneously + label partner forwarding as advertising — stale disclaimers are a consumer-law risk.
- Amount-based FAQ claims ("4.180 € Zuschuss") keep "bis zu"-capping and dated Quellenstand — already implemented, keep it mandatory in the content checklist.

## Phase plan
- **Phase 1 (week 1):** fixes #2, #3, #4, #7, #8 (all S) → llms.txt live, sitemap complete, checklisten linked, SERP snippets clean.
- **Phase 2 (weeks 2–3):** #1 FAQPage generator, #6 Article enrichment + og:image, #5 region decision, #9 stub merge, consent-script deferral.
- **Phase 3 (month 2):** re-run PSI per template + first CrUX readout, agentic probe after llms.txt, author/methodology page (E-E-A-T), cluster cross-linking, WebMCP when the lead form ships.
- **Phase 4 (ongoing):** monthly evidence refresh (GSC coverage, CrUX, AI-citation spot checks); keep "0 unnamed interactive elements" at 0.

## Score caveat
70/100 reflects **verified static-site hygiene** with deliberate deductions for unproven areas (field CWV unknown, thin pages indexed, discovery files 404). If Phase 1–2 lands, the realistic near-term ceiling on this evidence base is ~85.
