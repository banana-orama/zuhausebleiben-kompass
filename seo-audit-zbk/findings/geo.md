# Findings: GEO / AI-Search Readiness — zuhausebleiben-kompass.de

Evidence: agentic-home.json (robots AI-group analysis, discovery-file probes), llms.txt snapshot, robots.txt, article structure census.

## Score: GEO 58/100

## What works
- **robots.txt is AI-open by default**: single `*` group, nothing blocked — GPTBot, OAI-SearchBot, ClaudeBot, Claude-SearchBot, PerplexityBot etc. all resolve to root-allowed (verified per-agent in agentic-home.json). For a lead portal seeking AI citations this is the right default.
- **Server-rendered, agent-fetchable content**: 1,049 words without JS, no SPA shell; real 404s (no soft-404 noise).
- **Citation-ready content patterns**: dated source lists (~30 authoritative .de domains), question-form FAQs (104), "Transparenz und Grenzen" sections, exact figures with dates ("4.180 €", "Quellenstand: 2026-10-14"), stable semantic HTML. These are exactly the formats LLM answer engines quote.

## Findings
| # | Severity | Finding | Evidence |
|---|----------|---------|----------|
| G1 | High | **/llms.txt returns HTTP 404.** The evidence file named `llms.txt` is actually the GitHub Pages 404 HTML page (9,379 B, text/html), and agentic-home.json independently confirms `status: 404` for both `/llms.txt` and `/llms-full.txt`. The announced llms.txt integration was **not live at audit time** — either not deployed to the GH Pages branch or written to a wrong path. All downstream Lighthouse agentic-fraction credit is lost. | llms.txt content + agentic-home.json llms-txt check |
| G2 | Medium | No Content-Signal line, no AI-group differentiation. Fine as long as policy is "allow all"; if training vs. search vs. user-fetch should differ later, named groups are the mechanism. | agentic-home.json robots-ai-groups |
| G3 | Medium | No Markdown delivery path (no `Accept: text/markdown` negotiation, no `alternates` link, `/index.md` = 404). Optional per current agent practice but a cheap citability multiplier once llms.txt lands. | agentic-home.json markdown-delivery |
| G4 | Low | FAQ answers live inside closed `<details>` — fine for crawlers (content is in HTML), but answer engines favor pages where Q/A pairs are also extractable as clean text near the heading; the planned FAQPage schema (schema.md SC1) doubles as the GEO fix. | details census |

## Recommendations
1. (G1, S) Deploy the built `dist/llms.txt` to the published root and verify `200` + `content-type: text/plain`; include H1, `> ` summary, Markdown link list; regenerate from the sitemap in the same build step. Add `/llms-full.txt` later.
2. (G3, S) After G1: emit `<link rel="alternate" type="text/markdown">` or `.md` siblings for articles — static-site generators do this in a few lines.
3. (G2, —) Only add named robots groups/Content-Signal when there is an actual policy decision (e.g. `ai-train=no`); document it in llms.txt too.
4. (G4, M) Ship FAQPage schema (schema.md) and keep answers as plain `<p>` inside details — no JS-only answers.

## Limitations
- llms.txt "quality" could not be assessed — there is no llms.txt, only a 404. The task's assumption ("llms.txt was just integrated") is **contradicted by the evidence snapshot**.
- No live AI-engine citation check (ChatGPT/Perplexity probes) was in evidence; citability is inferred from structure, not measured.
