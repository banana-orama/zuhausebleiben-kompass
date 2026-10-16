# Measurement pivot: consent-gated client-side GA4 (2026-10-16)

Operator decision: **skip server-side tracking**. The Stape/sGTM path is NOT enabled and must
not be republished. Standard GA4 via Web GTM only, consent-gated by the existing
vanilla-cookieconsent revision 2.

## Why

- Stape Free quota exhausted: 18,432/10,000 requests. On Free tier a reached limit disables the
  container permanently; only a paid upgrade re-enables it. No paid upgrade approved.
- Container disablement imminent; server-side acceptance testing itself burned quota.
- Client-side GA4 needs no Stape quota at all: the browser talks to Google directly.

## Target architecture (implemented)

`Browser --(only after analytics consent)--> gtm.js GTM-M9TZZPLQ --> GA4 G-5738T8FHWW`
(account 412126546, property 559120219, stream 16133899442). No server container, no proxy,
no first-party transport host in the path.

- Site injects exactly ONE Web-GTM loader (`measurement.mjs`), only after a valid revision-2
  analytics consent, with `referrerPolicy='no-referrer'`.
- All events flow as the custom event `zbk_measurement` into dataLayer; the container fires
  only on strictly filtered triggers (see below). Payload discipline: `page_view` (once per
  page) and `cta_click` with `content_id`/`cta_id` only. No URLs, referrer, titles, query
  inputs, PII. GA4 settings unchanged: enhanced measurement OFF, retention 2 months no-reset,
  signals OFF, user-provided data OFF, no product links.

## Web container GTM-M9TZZPLQ (accounts/572865630/containers/267198165, workspace 2) — DRAFT

Changed via gtm CLI (explicit workspace paths; evidence readback:
`operations/measurement/gtm-draft-readback-client-side-2026-10-16.json`):

- **Tag 10 "ZBK — dispatch permitted queue to Stape" (html): DELETED** from the draft.
- **Tag 14 "ZBK — GA4 client-side (consent-gated)" (googtag, NEW)**: tagId `G-5738T8FHWW`,
  config `send_page_view=true` (single page_view at consent), static redaction overrides
  `page_location=https://zuhausebleiben-kompass.de/`, `page_referrer=""`, `page_title=""`
  (suppress URL-derived fields for the session's hits). Fires on trigger 9 only.
  Note: the googtag type has no `eventName` parameter (the API silently drops it) — hence the
  two-tag design below.
- **Tag 16 "ZBK — GA4 cta_click (consent-gated)" (gaawe, NEW)**: `eventName=cta_click`,
  `measurementIdOverride=G-5738T8FHWW`, event params `content_id`/`cta_id` from DLVs.
  Fires on trigger 15 only.
- **Trigger 9 (updated)**: custom event `zbk_measurement` + 7 filters: `analytics_allowed=true`,
  `consent_version=2`, `consent.analytics_storage=granted`, ad_* `denied`,
  `measurement.event_name=page_view`.
- **Trigger 15 (new)**: same filters but `measurement.event_name=cta_click`.
- **Variables**: existing DLVs 3–8 unchanged; NEW DLV 11 `measurement.content_id`,
  12 `measurement.event_name`, 13 `measurement.cta_id` (data layer variable names
  `measurement.*`).
- `server_container_url` was intentionally NOT set on tag 14 (an empty value is dropped by the
  GTM API; absence = pure client-side). Verify in the UI before publish that no
  `server_container_url` appears in the tag's configuration settings.

Both tags fire ONLY on the consent event with the strict allowlist; there is no
all-pages trigger, no Consent-Mode-only fallback, and no ad consent involved.

## Server container GTM-M6SDZCN4 (267197767) — DORMANT, UNTOUCHED

Draft client 5, trigger 12, forwarding tag 14 remain exactly as accepted in
`operations/STAPE-SGTM-ABNAHME.md` but stay **unpublished**. They are quota-blocked on the
Stape Free tier. Revisit ONLY after an explicit paid-upgrade decision by the operator; if that
happens, re-verify `/healthy`, quota state and the whole consent chain before any publish.

## Site code and texts (this repo)

- `measurement.mjs`: rewritten client-side. Config `mode:'client'`, loader after consent,
  minimal events, no fetch, no endpoint, page_view once, strict allowlist mirroring the
  trigger filters.
- `consent.mjs`: banner/settings texts now describe direct browser→Google transfer, IP
  truncation by Google at collection, 2-month deletion, no analytics cookies, immediate stop
  on withdrawal. No Stape/server claims. CMP mechanics (zbk_consent cookie, guiOptions,
  autoClear of `_ga*`) unchanged; revision stays 2.
- `consent-default.js`: comment updated (web trigger 9 is the gate now).
- `generate.mjs` (datenschutz section): truthful client-side disclosure — Google Ireland,
  single Web-GTM container, direct browser→Google transfer, no proxy/server service, strict
  allowlist, IP truncation at collection (last IPv4 octet), no URLs/referrer/titles/inputs,
  2-month retention, rev-2 re-consent note.
- Tests: `tests/measurement.spec.mjs` rewritten for client-side expectations (zero loaders and
  zero `zbk_measurement` before consent, exactly one `gtm.js?id=GTM-M9TZZPLQ` after accept,
  no-referrer loader, exact minimal payloads, withdrawal silence, no request EVER to
  `service.zuhausebleiben-kompass.de` or Stape hosts, no fallback direct analytics when the
  loader fails). `tests/consent.spec.mjs`: comment updates only (its existing tripwire that no
  dist HTML mentions googletagmanager/google-analytics/stape domains still holds — the privacy
  prose deliberately avoids the hostnames).
- Full `npm test` green (build + build:launch + test_site.py + test_articles.py + 2 policy
  tests + 13 Playwright tests).

## Explicitly NOT done (owner: operator / parent task)

- No GTM container published (web or server). Publish web container 267198165 together with the
  site deploy; keep server container 267197767 unpublished.
- No git commit/push, no site deploy.

## Remaining receipt verification (after deploy + web publish, no Stape involved)

1. Accept analytics consent on the live site in a normal browser; GA4 Admin → Realtime
   (`properties/559120219`) should show 1 user / page_view within ~30 min.
2. For per-event verification use GTM Preview on the WEB container only (Quick Preview sends
   GA4 DebugView hits directly to Google; it consumes no Stape quota) — check tag 14 fires once
   on `zbk_measurement` (page_view) and tag 16 on cta_click, and that `page_location` shows the
   fixed homepage override, not the real URL.
3. Do NOT enable GA4 `debug_mode` permanently; do not route anything through Stape hosts.
4. If Realtime stays empty ~60 min after consented traffic: check tag firing in Preview first,
   then the property/stream IDs, before touching site code.
