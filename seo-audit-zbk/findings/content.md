# Findings: Content Quality & E-E-A-T — zuhausebleiben-kompass.de

Evidence: 34 crawled pages (word counts, structure, sources), screenshot, llms/robots probes. Site live since 2026-10-15, declared "Ratgeber im Aufbau" (pre-launch) on every page.

## Score: Content Quality 71/100

## What works (stronger than typical for a 2-week-old site)
- **18 substantial articles** (1,678–2,857 words) with concrete structure: real manufacturer price example + model calculation (treppenlift-kosten), Antrag-Ablauf/Fristen, Vergleichskriterien — not AI-fluff; every article ends in "Transparenz und Grenzen" + "Häufige Fragen" + "Quellen und Anbieterangaben".
- **Sourced journalism practice on all 18 articles**: dated source lists ("geprüft 2026-10-14", "Quellenstand: 2026-10-14") citing ~30 authoritative domains (gesetze-im-internet.de/SGB XI §40, kfw.de, verbraucherzentrale.de, gkv-spitzenverband.de, bundesgesundheitsministerium.de, din18040.de…).
- **AI transparency**: every article carries "Mit KI-Unterstützung erstellt" + author link to Impressum (Tobias Batke, §5 DDG complete with address/contact) + explicit "keine Verbindung zu … einem Versicherungsunternehmen".
- **Audience fit**: consistent Sie-form, short sentences, print button ("Ratgeber & Checklisten drucken"), consent dialog in plain German — trust-first for older adults + relatives is genuinely implemented, not claimed.
- Honest draft labeling: "Entwurf zur ersten Orientierung · Preise nicht verbindlich" banner on all pages.

## Findings
| # | Severity | Finding | Evidence |
|---|----------|---------|----------|
| C1 | High | **Thin-content cluster: 14 of 34 pages hold 120–281 words.** 12 region pages are template placeholders (all exactly 152 words: "Konkrete Landesprogramme … noch nicht recherchiert"), regional.html hub 192 words, pflegegrad-beantragen.html 281 words (no Article schema, "Entwurf"). On a new domain this invites quality-threshold/door-page classification exactly when Google is still calibrating the site. | word-count table, page__region__bayern.html |
| C2 | Medium | **No author entity beyond the footer link**: no byline, no author page, no qualifications ("warum wir das schreiben dürfen"), no visible publication date on articles (only "Quellenstand" in fine print). E-E-A-T for YMYL-adjacent care/health topics lives mostly on transparency statements. | treppenlift-kosten.html head/source section |
| C3 | Medium | Every page carries a permanent "Aufbau/Entwurf" banner. Honest, but as a sitewide element it de-differentiates finished articles from drafts and reads as unfinished to both users and quality raters — remove per-page once content is final. | 34/34 pages |
| C4 | Low | Internal linking is sparse: 10–13 unique internal links per article (nav + "Passend dazu"), no cross-links into the (missing) checklisten section, region hub links only downward. Articles form one flat tier — no pillar/cluster structure (e.g. Kosten ↔ Mieten ↔ Zuschuss ↔ Firmen-Vergleich could interlink as a Treppenlift hub). | link counts |
| C5 | Info | Index page (1,042 words) lists all 18 articles with descriptive teasers — good hub, but only 5 article links sit in main nav; the rest are one long list. | index |

## Insurance-adjacent content risks (operator works at AXA)
1. **Disclaimers are already correct and specific**: "keine Versicherungsberatung", "keine Unterstützung beim Vertragsabschluss" (pflegegrad-beantragen meta), "keine Verbindung zu einem Versicherungsunternehmen" (Impressum). Keep this separation explicit as the site grows — GKV/Pflegekasse topics (Hilfsmittel, Pflegegrad, Verhinderungspflege) are Leistungsrecht, not insurance advice; never drift into recommending private policies or naming preferred insurers.
2. The 4.180-€-Zuschuss FAQ is framed as "Kann ich sicher … rechnen?" with a model calculation — keep "bis zu"-capping and dated Quellenstand on every amount (currently done); amounts change with Pflegegrad/maßnahmenbezogener split.
3. When Angebotsvermittlung launches: affiliate/partner forwarding must be labeled (Werbekennzeichnung) and the current claim "Es werden noch keine Angebote vermittelt / keine Weiterleitung eingerichtet" must be updated everywhere simultaneously — stale disclaimers are a consumer-law risk.
4. Hausnotruf-Vertragscheck content touches contract law — stay at checklist level ("was Verträge wirklich enthalten"), no individual case advice.

## Recommendations
1. (C1, M) Decide the region strategy: either expand each region page with real researched content (Landesförderprogramme, Pflegestützpunkte, zugelassene Fachbetriebe) or `noindex,follow` until real. Do not index 152-word placeholders.
2. (C2, M) Add per-article: author byline (linked entity), "Stand"/published date in visible position, and a short "Über uns"/methodology page (nav links only to an #anchor today).
3. (C3, S) Remove the Aufbau banner page-by-page as articles pass review; keep the disclaimer in footer.
4. (C4, M) Add 2–4 contextual cross-links per article within its topic cluster; connect checklisten once published.

## Limitations
- Readability scores (Flesch-DE) not computed; judgment on sentence length is qualitative from extraction.
- No SERP-level content-gap analysis beyond the 2 SXO probes.
- Facts/claims accuracy (4.180 €, KfW conditions) not re-verified against primary sources in this audit — source lists claim "geprüft" dates only.
