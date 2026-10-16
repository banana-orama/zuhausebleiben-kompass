# Measurement activation acceptance — 2026-10-16

**Status: activation-complete in drafts and site code, container publish and site deploy deliberately NOT done.** GA4-side event receipt is NOT confirmed; everything up to and including the server container's outbound GA4 forward is verified with real evidence.

## 1. GA4 property configuration (all read back from the live UI)

Account `412126546` (ZuhauseBleiben Kompass), property `559120219`, web stream `16133899442`, measurement ID `G-5738T8FHWW`, URL `https://zuhausebleiben-kompass.de`. Property timezone Germany/EUR (per creation readback in context).

| Setting | State | Evidence |
|---|---|---|
| Enhanced measurement | **Turned OFF this session** (was ON with page views, scrolls, outbound clicks +4). Turn-off dialog confirmed; after reload the stream shows only standard "Page views". | `operations/measurement/ga4-property-readback-2026-10-16.json` |
| Event data retention | 2 months | Data retention page, re-read this session (matches prior `ga4-retention-readback.json`) |
| User data retention | 2 months | same |
| Reset on new activity | **unchecked** (toggle read `false`) | same |
| Google signals | OFF | data collection page readback (`ga4-collection-readback.json`) |
| User-provided data collection | OFF (switch unchecked) | same |
| Product links (Ads, AdSense, Search Console, …) | none. Product-links detail cards are not clickable via UI automation, so this is verified indirectly: property created 2026-10-15, Home shows "No data received", no Google Ads account exists for this project. No `google Ads links` link entries appear anywhere in page text. | recorded as indirect in the readback file |

## 2. Server container forwarding tag (draft, workspace 2)

Tag **14** "ZBK — GA4 analytics-only sanitized forwarding" (`sgtmgaaw`), firing on trigger **12** only:
- destination measurement ID fixed to `G-5738T8FHWW` (parameter, not variable)
- `redactVisitorIp: true`
- event parameters limited to `event_id`, `content_id`, `cta_id` (own event-data variables), `debug_mode` (Debug Mode), `non_personalized_ads: true`; user properties: none
- trigger 12 filters: event regex `^(page_view|cta_click)$`, `analytics_allowed=true`, `consent_version=2`, `analytics_storage=granted`, `ad_storage/ad_user_data/ad_personalization=denied`, Client Name = client 5
- Exact payload readback: `forwarding-exact-readback.json`; live CLI entity list re-verified this session: `gtm-draft-readback-2026-10-16.json`
- Pre-existing GA4 client 1 untouched. Native GA4-client traffic still cannot forward (no tag attached to client 1 routes).

## 3. Live service-host preview (real transport, draft container)

TLS on `service.zuhausebleiben-kompass.de` is a valid Let's Encrypt certificate (CN matches, valid 2026-10-15 → 2027-01-13); `/healthy` returns 200. **The built-in-Stape-host fallback was NOT needed.**

- QUICK_PREVIEW started on the server container; the UI-generated debug URL now uses the service host.
- Preview header mechanism: `X-Gtm-Server-Preview` (found via Tag Assistant → ⋮ → "Send requests manually"; token read live, **not stored in the repo** per handoff policy — it is session-bound).
- Wrong-header probes (`x-gtm-preview`/`X-GTM-Preview`) → 400, consistent with the prior run's evidence; correct header → **204**.
- Valid revision-2 `page_view` (content c04, all four consent states, analytics-only) → HTTP **204** → Tag Assistant shows **"collect / 1 page_view", Tags Fired: "ZBK — GA4 analytics-only sanitized forwarding — Google Analytics: GA4 - Fired 1 time", Tags Not Fired: None**.
- Evidence: `preview-service-host-2026-10-16.json` (+ PNGs `preview-service-host-ga4-tag-fired.png`, `preview-overflow-menu.png`, `preview-manual-send-dialog.png`).

## 4. GA4-side receipt: NOT confirmed (honest gap)

GA4 Home/Realtime showed 0 active users and "No data available" ~9 minutes after the verified forward; DebugView could not be opened through browser automation (GA4 SPA kept routing to Admin). Tag Assistant proves the container sent the outbound request; it does not prove Google processed it. Two plausible causes, both requiring operator action, neither a code defect found so far:
1. **Stape request quota exhausted**: dashboard warns "Your request limit has been reached in your current billing period" — **18,432 of 10,000 requests on the Free plan, renews 2026-11-15; container can be disabled if not upgraded.** This alone can break the GA4 forward.
2. GA4 processing latency for a brand-new property's first server-side hits.

Pending: one manual DebugView check (phone/browser with `debug_mode`) or a Realtime re-check ~30 min after a fresh event, ideally after the quota issue is resolved.

## 5. CMP revision 2 + truthful disclosures (site code, built)

- `consent-default.js`: `version: 2`, `consent_version: 2` in the dataLayer event (comment explains the three-way contract with CMP revision and server gate).
- `consent.mjs`: `revision: 2` (vanilla-cookieconsent invalidates stored revision-1 selections and re-shows the banner); `installMeasurement()` now imported and called from `onConsent`/`onChange` (after the consent-mode update, exactly the handoff's required order). Banner and preferences texts now name the real providers and limits: Google Analytics 4 (Google Ireland Ltd.), own Web GTM GTM-M9TZZPLQ, own Server GTM GTM-M6SDZCN4 on Stape B.V. (NL), IP processing in transit and truncation at Google, 2-month deletion, no URLs/query/referrer/inputs, no analytics cookies, ads permanently denied, Art. 6(1)(a) DSGVO / § 25(1) TDDDG, immediate stop on withdrawal, revision-1 invalidation explained.
- `generate.mjs` privacy page §2 rewritten for the activated state (providers, allowlist, signals/user-provided OFF, no product links, enhanced measurement OFF, payload inventory, IP handling, retention, revision-2 invalidation note). Homepage trustline "Derzeit keine Datenerfassung" replaced by "Ohne Einwilligung keine Statistik" (old claim would have become false).
- `measurement.mjs`: config activated (`enabled/tlsVerified/serverGateVerified/destinationVerified: true`) with the evidence basis in a comment; endpoint remains the service host.

## 6. Tests (all green, `npm test` exit 0)

Build 32 pages PREVIEW → launch build 31 pages INDEX → `test_site.py` PASS (launch assertions) → `test_articles.py` PASS (11 renders) → policy tests 2/2 → **Playwright 13/13**, including:
- shipped integration active after consent: exactly one GTM loader + one sanitized page_view (consent_version 2, correct consent object)
- failed GTM loader → no fallback, no requests; navigation works; withdrawal suppresses flush
- default-deny, reject, one-shot opt-in, duplicate-prevention (consent re-update sends nothing), CTA click payload, query/PII redaction (`?email=…&diagnose=private#private` never appears), no-referrer headers, withdrawal stops everything
- revision invalidation asserted: banner re-appears (`Alle akzeptieren` visible on arrival with any stale state)
- consent suite made hermetic (measurement hosts blocked/observed-excluded there; their behavior lives in the measurement spec); section locator updated to the new title "Optionale Statistik"
- `package.json` test pipeline fixed to build the launch variant for the launch-mode site test, then rebuild preview for Playwright. (The pre-existing failure on unmodified HEAD was verified first: `npm test` ran site assertions against the preview build and failed on `regional.html` before any of my changes.)

## 7. Files changed / created this session

Modified: `consent-default.js`, `consent.mjs`, `measurement.mjs`, `generate.mjs`, `package.json`, `tests/measurement.spec.mjs`, `tests/consent.spec.mjs`, plus regenerated `dist/`.
Created: `operations/measurement/ga4-property-readback-2026-10-16.json`, `operations/measurement/gtm-draft-readback-2026-10-16.json`, `operations/measurement/preview-service-host-2026-10-16.json` (+3 PNG evidence), this file.

## 8. Deliberately NOT done (stopping points honored)

- **No container publish** in Web or Server GTM (QUICK_PREVIEW only; drafts).
- **No git commit/push/deploy** — parent owns the site deployment; all changes are working-tree only.
- No changes to GA4 client 1, other accounts/properties/containers, sharing settings left as found (all OFF).
- No Stape plan changes, no outgoing-log enablement (not available on Free plan).

## 9. Operator decisions / next steps

1. **Stape quota** (blocking reliable GA4 delivery): upgrade the container plan or accept disablement risk; renews 2026-11-15.
2. **GA4 receipt check**: after (1), send one preview event and confirm in DebugView/Realtime; then flip the two workspaces to Publish and re-run the browser suite against production.
3. Custom-domain TLS and transport are already on the service host — no fallback host in use, nothing to disclose about Stape beyond the NL processing location already in the texts.
