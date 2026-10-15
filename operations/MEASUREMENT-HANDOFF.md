# Measurement integration handoff — 2026-10-15

## Outcome, not a launch claim
**Not end-to-end complete and not activated.** Own Web/Server GTM drafts exist, and the strict server client was exercised on the real Stape built-in endpoint through GTM Quick Preview. No GA4 account/property/stream was created, no forwarding tag exists, no container was published, and no site commit/push/deploy was performed.

### Actual blockers
1. Parent verified custom `service.zuhausebleiben-kompass.de` DNS but TLS still serves self-signed `TRAEFIK DEFAULT CERT`; Stape status Verifying, up to 72h automatic verification. Do not bypass TLS or enable public loaders. No further DNS changes indicated.
2. Separate GA4 account creation reaches an explicit **Google Analytics Terms of Service Agreement** + GDPR Data Processing Terms checkbox. Left unaccepted. An authenticated browser tab remains on `analytics.google.com/analytics/web/#/a410349349p556924905/admin/account/create`; the URL retains the previous account context but this is the separate **new account wizard**, not a modification of that client. Prepared account/property name ZuhauseBleiben Kompass, all four data-sharing options unchecked, Germany reporting timezone and EUR, Home & Garden, small business, traffic objective, terms country Germany. No property/stream ID yet. Needs a bounded decision allowing these free-service terms/DPA, or operator completion. Do not touch existing EQUILEX or other-client properties.

## Real GTM changes, exact authorized scope
Account `572865630` (Eigene Websites), workspace `2` in each:
- Web `accounts/572865630/containers/267198165` / **GTM-M9TZZPLQ**:
  - six DLVs, variable IDs 3–8: `analytics_allowed`, `consent_version`, and the four `consent.*` states, Data Layer v2.
  - trigger **9**: custom `zbk_measurement`, explicit analytics_allowed=true, consent_version=2, analytics granted, all three ad states denied.
  - Custom HTML tag **10**: dispatches the already-sanitized queue through `window.zbkMeasurement.flush()`; no Google Analytics tag and no All Pages trigger.
- Server `accounts/572865630/containers/267197767` / **GTM-M6SDZCN4**:
  - custom client template **4**, type `cvt_267197767_4`.
  - client **5**, priority100: `/zbk/collect`, exact site Origin, POST, bounded body, strict keys/event/ID/placement/consent whitelist. No cookies, logging, forwarding, raw query/referrer ingestion into event data.
  - six event-data variables, IDs6–11, same fields; trigger **12** with analytics-only complete consent and current revision.
  - Existing GA4 client1 untouched. No GA4 forwarding tag exists, so native GA4-client traffic cannot currently forward anywhere either.
- Own server container's empty Server container URLs setting was set to **https://jsyqolvb.euh.stape.net** solely to make secure Preview possible; saved and independently reopened/read back. Keep public transport configured only for the service hostname. Switch Preview URL to service after real TLS works.
- Exact entity readbacks: `operations/measurement/exact-draft-readback.json`. Scoped provisioning: `operations/measurement/provision-drafts.py`; JSONL mutation/read log alongside it. Never uses or changes global CLI context. Initial bounded batch timed out after420s during quota waits; idempotent rerun completed.

## Real Stape server Preview verification
Used QUICK_PREVIEW (not a published version) on **https://jsyqolvb.euh.stape.net**, with UI-provided manual Preview header; no TLS bypass. Header is not stored in repository artifacts.
- **9 actual correctly-routed requests**, all204.
- Exactly **2 generated events**, counted from actual Preview message DOM: `page_view` and `cta_click` / `editorial_contact`.
- Remaining **7 requests create no event**: analytics_allowed=false, missing consent object, unexpected email key (synthetic diagnostic address only), analytics_storage denied despite flag, ad_storage granted, stale revision1, malformed JSON.
- Both accepted events show claimed client5, `analytics_allowed: true`, revision2, analytics granted, ad_storage/ad_user_data/ad_personalization denied in **actual server Event Data**.
- No event named lead/generate_lead. Editorial contact is only a click, not a successful enquiry.
- Evidence: `preview-http-results.json`, `preview-event-data.{txt,png}`, `preview-cta-event-data.{txt,png}` in `operations/measurement/`.
- Five early additional requests returned400 due to a test-harness empty-header selection mistake (Preview Event Data creates extra empty textareas). These are retained and marked in HTTP evidence, then retried with the exact nonempty header; **not counted among the9 client-received requests**.
- **No Google Analytics collection verified.** Server-received synthetic diagnostic events are not visitor traffic or proof of GA4 collection.

## Browser artifact and privacy contract
`measurement.mjs` exports `installMeasurement`; default config disabled and all readiness attestations false. It is copied by the build to `dist/assets/measurement.mjs` but **not imported/invoked by production CMP**. No production behavior changed; existing revision1 banner truthfully says analytics inactive.

Candidate path after deliberate activation: current analytics opt-in → one GTM loader with no-referrer policy → intentional sanitized dataLayer event → own Web GTM dispatch tag → POST only to service `/zbk/collect` with all four consent states → strict server client → a still-to-be-created explicitly gated/sanitized own GA4 forwarding tag.

Payloads have bounded event_name/event_id/client_id/content_id/cta_id, analytics_allowed, revision and four states only. No page_location/title/referrer, raw URLs/query/hash, DOM text, mailto addresses, contact values, free-text, diagnoses, user_id, ad IDs or raw headers. Page-scoped random UUID only, no analytics cookies/localStorage; this deliberately cannot provide cross-page returning-user/session attribution. Raw IP is necessarily seen by GTM script hosting and Stape transport, so provider disclosure is still required; do not describe the whole path as anonymous or EU-only simply because Stape is in Holland.

Content mapping: c01 bad-umbau-barrierefrei, c02 treppenlift-firmen-vergleich, c03 treppenlift-gebraucht-oder-neu, c04 treppenlift-kosten, c05 treppenlift-mieten, c06 treppenlift-zuschuss, c07 wanne-zur-dusche. Other pages currently use generic `site` rather than collecting an arbitrary path. Valid placements: checklist_top, compare_top, print_bottom, editorial_contact. Existing CTA navigation/printing is not prevented by listeners.

## Tests actually run
`npm test` passed:25 HTML pages +7 articles, **2 Node policy tests**, **13 Playwright/Chromium tests** (10 existing CMP +3 new candidate/inactive/failure cases). `git diff --check` passed.
- Local candidate acceptance test uses a clearly labelled minimal **GTM stand-in and intercepted transport sink**. It tests actual CMP interactions, no requests by default/denied, one page_view on repeated acceptance, click navigation, consent payload, URL/PII exclusion, no-referrer headers, withdrawal suppression. It is **not real Web GTM or real GA4 verification**.
- Candidate fixture explicitly uses revision1 to exercise the current CMP; shipped config/server client require revision2. Do not silently change the latter to reuse preview consent.
- New package script `test:measurement` rebuilds template artifacts and runs Node policy tests. Playwright testMatch restricted to `**/*.spec.mjs` to keep Node tests out of Playwright.

## Remaining activation work (do not conflate with done)
1. Resolve free GA4 terms/DPA boundary, then own account/property/stream with Germany/EUR; disable enhanced measurement, all sharing, Signals, user-provided data, ads links/personalization. Set/read back actual event retention (target shortest2months) and no reset-on-new-activity where applicable. Record IDs. Do not invent them.
2. Add a destination-fixed GA4 forwarding tag to own server container, gated again on complete analytics consent and strict event allowlist. Forward only rebuilt sanitized event data, never raw request/body/headers or unknown default event parameters. Test no forwarding from missing/denied/contradictory requests including native GA4-client routes. Until then server trigger12 is deliberately unattached.
3. Verify real service-host public TLS normally. Add actual provider identities, purposes, IP processing/transfer and confirmed retention to banner/privacy. **Bump CMP revision and bootstrap consent_version/version to2** before enabling; invalidate old revision1 selections. Current inactive text and revision1 are intentionally unchanged.
4. Import/invoke `installMeasurement` before CMP callbacks (e.g. from consent module), then set readiness flags only after corresponding evidence and enable only for the verified acceptance artifact. No automatic TLS ping or optional request under denied consent.
5. Real Web GTM + service Server Preview plus GA4 DebugView/Realtime must show exactly intended permitted page_view/CTA events; test default/reject/reload/accept/withdraw, revised consent, failed scripts, duplicate prevention, query redaction and all four CTA behaviors on all7 articles. Publish own containers only after this acceptance; parent controls website commit/deploy.

## Files changed/created by this work
Modified: `generate.mjs`, `package.json`, `playwright.config.mjs`.
Created: `measurement.mjs`, `measurement-policy.mjs`, `build-measurement.mjs`, `dist/assets/measurement.mjs`, `tests/measurement.spec.mjs`, `tests/measurement-policy.test.mjs`, this handoff and `operations/measurement/*` generated templates/provisioning/readbacks/evidence.
No edits to consent banner/bootstrap, privacy generator text, articles, existing unrelated operations/research files, Mail/Awin/Stape UI, git index or other client containers.
