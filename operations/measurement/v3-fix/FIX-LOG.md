# v3–v5 Fix Log — GA4 receipt blocker resolved (2026-10-16 evening)

Authoritative summary of the fix session. Evidence files in this directory.

## Root cause (proven, not inferred)

Variables **11/12/13** (`ZBK DLV - measurement.content_id` / `.event_name` / `.cta_id`) were
created **without the `dataLayerVersion` parameter**. GTM's Data-Layer-Variable then defaults
to **data layer version 1**, which reads only flat top-level keys and cannot resolve
dot-paths into nested objects.

The site pushes (verified in `tests/measurement.spec.mjs` and live):

```js
{event: 'zbk_measurement', analytics_allowed: true, consent_version: 2,
 consent: {analytics_storage: 'granted', ad_storage: 'denied', ...},
 measurement: {event_name: 'page_view', content_id: 'c04', cta_id: ''}}
```

→ Trigger predicates 6/8 (`measurement.event_name == page_view|cta_click`) evaluated
`undefined == "page_view"` → **false** → neither trigger 9/15 nor tags 14/16 ever fired.
The consent predicates (0–5) worked by accident of the same bug class: variables 3–8
**did** get `dataLayerVersion: 2` at creation.

Consequence: the published runtimes were never broken — they faithfully encoded a
never-matching rule. That is why re-save (v3) and delete+recreate (v4) changed nothing.

## Proof chain (local bisect against the real published bytes)

| Experiment | Result |
|---|---|
| v4 bytes, original rules | no gtag/js, no registration (repro of live failure) |
| v4 bytes, rules reduced to `_event == zbk_measurement` only | **fires** (gtag/js requested, `G-5738T8FHWW` registered) |
| v4 bytes, unconditional rules | **fires** |
| single-predicate runs p0–p5, p7 | fire |
| single-predicate run p6 (`measurement.event_name`) with site-shaped push | **no fire** |
| same p6 with flat `'measurement.event_name'` key in dataLayer | fires |
| v4 bytes + `vtp_dataLayerVersion:2` patched into the three measurement macros, original full rules | **fires** |

API readback of the variable entities (ws5) confirmed: variables 3–8 have
`{"key":"dataLayerVersion","value":"2"}`; variables 11/12/13 lack the parameter entirely.

## Production fix

- ws5 (Default Workspace): `gtm_update_variable` on variables 11/12/13 —
  added `dataLayerVersion: 2` (integer param), nothing else changed.
- Version 5 `ZBK v5: measurement variables dataLayerVersion=2 (root cause fix)` published.

## Version timeline (container 267198165 / GTM-M9TZZPLQ)

| Version | Name | Change | Outcome |
|---|---|---|---|
| 2 | ZBK v1: consent-gated client-side GA4 | original (live since 16 Oct morning) | never fired |
| 3 | ZBK v3: client-side GA4 runtime fix | re-save tags 14/16 + triggers 9/15 (config identical; `notes` touched to force a real change) | still no fire (expected — root cause untouched) |
| 4 | ZBK v4: … (delete+recreate) | triggers 9→18, 15→19 recreated (7 predicates exact), tags 14→20 (googtag), 16→21 (gaawe) in fresh ws4 | still no fire (expected) |
| 5 | ZBK v5: measurement variables dataLayerVersion=2 (root cause fix) | only variables 11/12/13 updated | **fires end-to-end** |

Entity IDs now live in v5: **tags 20 (googtag page_view) and 21 (gaawe cta_click)**,
**triggers 18 (zbk page_view) and 19 (zbk cta_click)**, variables 3–8, 11–13 (11–13 now DLv2).

## v2 vs v3 gtm.js payload diff (authorized check, performed though v3 did not fix)

- 367,365 B → 367,463 B; `resource.version` 2→3; newer loader build (runtime module shuffling).
- **Permission hash for tag 14 changed `6ae1`→`6af0`** (regeneration proof).
- Tag/trigger rules byte-equivalent (same predicates, same `[[if 0..7][add 0]],[[if 0..5,7,8][add 1]]`).
- v4 vs v2: same size class (367,365 B), new tag_ids 20/21, rules identical.
- v5 vs v4: +75 B — exactly the three `"vtp_dataLayerVersion":2` insertions.

## Final evidence (all 2026-10-16 ~19:5x–20:1x CEST)

- `final-e2e.mjs` run against https://zuhausebleiben-kompass.de/treppenlift-kosten.html:
  1× gtm.js loader → `gtag/js?id=G-5738T8FHWW&cx=c&gtm=…` → **2× `/g/collect` (HTTP 204)**
  with `gcs=G101` (analytics granted / ads denied), container id in `&gtm=` tag, events page_view + cta_click.
- `google_tag_manager` keys on live page: `GTM-M9TZZPLQ` **and** `G-5738T8FHWW`.
- `realistic-probe.mjs` (headed, real UA, 45 s dwell, scroll, CTA click): same 204 hits.
- GA4 UI property 559120219: Home banner flipped from „No data received…" to Realtime widget
  with **Germany 1 active user**; Realtime overview event snapshot:
  **first_visit 1, page_view 1, session_start 1**. Screenshot: `ga4-realtime-receipt-v5.png`.
- Site repo test suite `tests/measurement.spec.mjs`: **3 passed** (no repo changes needed).

## Tooling notes for repetition

- `gtm tool call gtm_*` named tools with explicit `containerPath`/`workspacePath`/`tagPath`
  args work correctly; the earlier GAM-Medical cross-contamination came from wrong arg names
  (`path` instead of `containerPath` etc.) which made the resolver fall back to the global
  CLI context. Readback responses return the entity at top level (not under `data`).
- The CLI's googtag normalizer (`normalizeGoogleTagParameters`) drops map rows whose
  `parameterValue` has no `value` — tag 14's empty `page_referrer`/`page_title` redaction
  rows need the raw googleapis path (see `fix-tag14-exact.mjs`) or UI edits.
- Publishing submits the workspace: GTM rotates Default Workspace after each publish
  (ws3→ws4→ws5). Post-publish entity edits must target the new workspace.
- Content-identical updates are no-ops at GTM API level (fingerprint reverts, no workspace
  change); `notes` is a real field and forces a change entry.
