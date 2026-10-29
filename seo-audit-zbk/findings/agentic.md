# Findings: Agentic Readiness — zuhausebleiben-kompass.de

Evidence: agentic-home.json (Lighthouse agentic-browsing style probe, checked 2026-10-19T21:04Z), agentux-treppenlift-kosten.json (page-level agent-UX probe).

## Score: Agentic 74/100

## Page-level agent UX (agentux-treppenlift-kosten.json): 100/100
- 7 real `<button>`s, 47 anchors, 0 div-onclick widgets, 20 semantic landmarks; accessibility tree present (788 nodes, 51 interactive, **0 unnamed interactive elements**), 0 inputs without labels/aria.
- An autonomous agent can perceive and operate this page fully. This is the strongest agentic asset of the site.

## Site-level probe results (agentic-home.json summary)
| Priority | Pass | Info | n/a |
|----------|------|------|-----|
| P0 | 2 | 1 | 0 |
| P1 | 2 | 3 | 0 |
| P2 | 0 | 1 | 4 |
| P3 | 0 | 0 | 4 |

- P0 passes: server-rendered content (1,049 words no-JS), robots.txt reachable (200). P0 info: no per-agent robots groups (deliberate policy choice, not a defect).
- P1 passes: user-triggered agents unblocked, real 404s. P1 infos: no Content-Signal, **no /llms.txt (404)**, no markdown delivery.
- P2 n/a: no WebMCP (`navigator.modelContext` absent, 0 `registerTool` call sites, 0 forms on page — the pre-launch site has no transactional surface yet), no API catalog/OAuth resource metadata (correctly n/a — no matching service).

## Findings
| # | Severity | Finding | Evidence |
|---|----------|---------|----------|
| A1 | High | llms.txt 404 (see geo.md G1) — the only failing P1 that is fixable in minutes and directly counted by the Lighthouse agentic fraction. | agentic-home.json |
| A2 | Medium | No WebMCP tool registration. Correct today (zero forms), but the moment the Angebotsvermittlung form ships, register an imperative tool bound to the same handler — the lead funnel is the one transaction an agent should be able to complete. | agentic-home.json webmcp |
| A3 | Info | Single `*` robots group means every AI vendor inherits "allow". If partner-forwarding launches, re-evaluate whether ad/vendor crawlers (OAI-AdsBot etc.) should stay blanket-allowed. | robots analysis |

## Recommendations
1. (A1, S) Publish llms.txt (geo.md G1) — re-run the agentic probe after deploy; expect P1 3×info → ≥1 pass.
2. (A2, M) Backlog: WebMCP tool for the future lead form (W3C CG draft — implement behind a flag, keep the plain form working).
3. Keep agent-UX hygiene: every new interactive element must keep a name (currently 0 unnamed); add to the launch checklist.

## Limitations
- Probe covers home (site-level) + one article (page-level agent UX). Region/checklisten pages unprobed (likely identical template → same result, unproven).
- WebMCP scan is static (call-site count), not a runtime tool listing.
