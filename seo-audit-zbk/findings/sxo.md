# Findings: SXO (Search Experience Optimization) — zuhausebleiben-kompass.de

Evidence: 34 crawled pages (titles/H1/structure), 2 live SERP probes (2026-10-29, Bing-backed, 5 results each), Lighthouse UX metrics, screenshot.

## SXO Gap Score: 66/100 (separate from the SEO Health Score)

## SERP reality check
- "treppenlift kosten": top-5 are **paid vendor/lead-broker landing pages** (Angebot-Anforderung funnels). The organic set below is informational: price-guide articles with tables, example calculations, and lead forms.
- "treppenlift zuschuss 4180 euro": organic leaders are editorial guides (pflegekompass.de, pflege.net, sign-med.de) with exact-amount headlines, §40 SGB XI framing, Antrag step-by-step and KfW context.

## Page-type match: ALIGNED (no critical mismatch)
Both sampled money pages are **informational guides** competing against informational organic results — the right page type. The gap is depth of decision support, not type:
| SERP expectation | Site today |
|---|---|
| Cost table + concrete example numbers | ✅ real manufacturer price example + model calculation (stronger than most) |
| Zuschuss amount + Antrag steps + KfW | ✅ present, dated sources; ❌ no step-by-step Antrag CTA to a checklist |
| Interactive elements (cost calculator, form) | ❌ none — declared pre-launch, no lead capture |
| Content depth 1.5–3k words | ✅ 1.7–2.9k words on articles |

## Persona scoring (0–25 each: Relevance / Clarity / Trust / Action)
| Persona | R | C | T | A | Σ | Weakest link |
|---|---|---|---|---|---|---|
| Ältere Person mit kleiner Treppe (75+, researches alone) | 22 | 21 | 23 | 14 | **80** | Action: no next step beyond print — no consultation path, no phone |
| Angehörige/r organisiert den Umbau (40–60, does the research, shares links) | 22 | 20 | 21 | 15 | **78** | Action + shareability: no og:image, no WhatsApp-friendly snippet |
| Pflegegrad-Haushalt plant Finanzierung | 21 | 19 | 22 | 14 | **76** | Antrag journey broken across stub page (pflegegrad-beantragen) + missing checklisten |
| Regionale Suche („Treppenlift München") | 15 | 12 | 18 | 8 | **53** | 152-word placeholder pages answer nothing regional — current worst persona |

## Findings
| # | Severity | Finding | Evidence |
|---|----------|---------|----------|
| X1 | High | The decision journey ends in nothing: every article's CTA is a print button and "Worauf Sie bei Anbietern achten sollten →". For the 6 checklisten pages that should be the destination: **no links, no sitemap entry** (sitemap.md S1). The best-intent funnel leaks at the last step. | article CTAs + href scan |
| X2 | High | Regional persona unserved: 12 indexed placeholders, no regional facts, no providers — worse than not ranking. | region pages |
| X3 | Medium | Titles are keyword-first and intent-true but 17/18 exceed 65 chars → truncation eats the differentiator exactly where SERP competitors put "2026", "bis 4.180 €" hooks. | title lengths vs SERP titles |
| X4 | Medium | pflegegrad-beantragen.html uses its meta description (242 chars) as a pure disclaimer — the SERP snippet will show a refusal instead of a reason to click. | meta census |
| X5 | Low | No conversion telemetry possible pre-launch (consent-gated, no GA4 yet) — once launched, define persona KPIs (scroll depth, checklist downloads, print events) before enabling analytics. | no gtag in HTML |

## User stories (from SERP signals)
1. "Ich habe eine Kurventreppe und will wissen, ob 6.000 € realistisch sind" → model-calculation section answers this; add a variant table (gerade/kurven/outdoor) to fully cover it. [Signal: ad+organic titles promise price anchors]
2. "Wer bezahlt wie viel — Pflegekasse, KfW, Steuer?" → covered with dated sources; add one comparison table with amounts+conditions. [Signal: pflege.net/pflegekompass tables]
3. "Ich will 3 Angebote vergleichen, ohne abgezockt zu werden" → comparison-checklist content exists, but the checklisten destination is missing/unlinked. [Signal: lead-broker USP "bis zu 3 Angebote"]
4. "Gibt es das auch in meiner Stadt?" → region pages are empty. [Signal: regional ad targeting in SERP]

## Recommendations (weakest persona first)
1. (X2, M) Either ship real regional content or noindex placeholders; add "Fachbetriebe in [Region]" only when actually researched.
2. (X1, M) Wire every article CTA to its checklisten page; give checklists an on-page anchor (download/print) so Action ≠ 14/25.
3. (X3, S) Rewrite titles to ≤60–65 chars keeping the keyword head ("Treppenlift-Kosten 2026: Beispiele, Zuschuss, Planung").
4. (X4, S) Meta descriptions: benefit-first ≤155 chars; move the disclaimer into the page body.

## Limitations
- SERP sample = 5 results × 2 queries, one engine backend, ads-dominated money SERP — page-type consensus is directional, not statistical.
- No click/behavior data exists (pre-launch, no analytics) — persona scores are evidence-informed judgment, not measured.
- Competitor content depth estimated from result descriptions, not full-page crawls (out of scope: no re-crawling).
