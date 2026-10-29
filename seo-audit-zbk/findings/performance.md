# Findings: Performance (Core Web Vitals) — zuhausebleiben-kompass.de

Evidence: 2× full Lighthouse JSON (unlighthouse): `hausnotruf-sturzerkennung-oder-knopf`, `hilfsmittel-pflegekasse-uebernahme`. **PSI run FAILED** (API rate limit — psi-treppenlift-kosten.json contains only an error), so there is **no CrUX field data** (site too new regardless) and lab data covers only 2 of 34 pages.

## Score: Performance 80/100 (lab-only confidence)

## Lab results (mobile emulation, Lighthouse)
| Metric | hausnotruf… | hilfsmittel… | Assessment |
|--------|------------|--------------|------------|
| Performance score | 0.89 | 0.83 | good |
| LCP | 1.1 s | 1.0 s | green (target ≤2.5 s) |
| CLS | 0 | 0 | perfect |
| FCP | 1.0 s | 1.0 s | green |
| TBT | **380 ms** | **580 ms** | the weak metric (proxy for INP) |
| Speed Index | 3.9 s | 4.4 s | moderate |
| TTI | 1.5 s | 1.7 s | green |
| Server response | 10 ms | 10 ms | CDN-fast |
| Total byte weight | 38 KiB | 40 KiB | excellent (static, no webfont bloat, no analytics pre-consent) |

Passing everywhere: render-blocking resources (savings 0 ms), unused CSS/JS, image sizing/formats, font-display, main-thread work ≤1.6 s.

## Findings
| # | Severity | Finding | Evidence |
|---|----------|---------|----------|
| P1 | Medium | TBT 380–580 ms on a 38–40 KiB page = nearly all blocking from inline JS + consent module; likely the same on all 18 article pages (identical template). INP risk for older users with slow devices. | lighthouse.json audits |
| P2 | Medium | Speed Index 3.9–4.4 s while FCP is 1.0 s → late visual completion, consistent with the full-viewport consent dialog rendering over content. | lighthouse.json |
| P3 | High (data) | **No field data exists** — new domain, empty CrUX; PSI fetch failed. CWV status for real users is unknown. | psi-*.json error |
| P4 | Info | LCP element is text (~1.0–1.1 s) — no image-LCP risk. | lcp-element audit |

## Recommendations
1. (P1, S) Defer the consent script until interaction or `requestIdleCallback`; split inline JS; target TBT < 200 ms.
2. (P4, —) Keep text-LCP; preload nothing, current setup is close to optimal.
3. (P3, S) Re-run PSI after rate-limit reset for the 3 template representatives (home, one article, one region) to capture lab + confirm empty-CrUX status; repeat monthly once traffic accrues. This audit cannot state real-user CWV.

## Limitations
- 2 pages only (same template → likely representative, but unproven).
- Lab-only: no INP, no real-user distributions. Any "CWV green" claim would be premature.
