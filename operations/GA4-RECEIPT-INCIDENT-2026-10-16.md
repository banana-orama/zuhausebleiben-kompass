# GA4-Empfangsblocker: Published Container-Tags feuern nie (2026-10-16)

## RESOLUTION (2026-10-16 Abend, Version 5) — GESENDET & BESTÄTIGT

**Wurzelursache (bewiesen):** Die Variablen 11/12/13 (`ZBK DLV - measurement.*`) wurden ohne
den Parameter `dataLayerVersion` angelegt und defaulted damit auf **Data-Layer Version 1**,
die keine Dot-Paths in verschachtelte Objekte auflösen kann. Die Site pusht
`measurement:{event_name:'page_view',...}` verschachtelt → Prädikat 6/8
(`measurement.event_name == page_view|cta_click`) war immer `undefined == "…"` → **false**.
Kein Trigger-Match, kein Tag-Fire — in jeder Runtime. Konsistenz-Check: Variablen 3–8
(Consent-Prädikate) hatten `dataLayerVersion:2` und funktionierten; der Mismatch betraf
genau die measurement-Variablen. Re-Save (v3) und Delete+Recreate (v4) mussten daran
scheitern, weil sie die Konfiguration identisch reproduzierten.

**Fix (Version 5, publiziert):** `dataLayerVersion: 2` auf Variablen 11/12/13 — sonst nichts.

**End-to-Empfangsnachweis (20:0x CEST):** Live-Probe auf der echten Seite: 1× gtm.js →
`gtag/js?id=G-5738T8FHWW` → **2× `/g/collect` HTTP 204** (`gcs=G101`, page_view + cta_click);
`google_tag_manager` enthält `G-5738T8FHWW`. GA4-Property 559120219: Realtime zeigt
**1 aktiver Nutzer (Germany)**, Event-Snapshot **first_visit 1, page_view 1, session_start 1**
(Screenshot: `measurement/v3-fix/ga4-realtime-receipt-v5.png`). Der Banner
„No data received from your website yet" ist damit obsolet (Historie bis 16.10.).
Site-Tests `tests/measurement.spec.mjs`: 3/3 passed, Repo unverändert.

Vollständige Beweiskette, Versionen 3/4/5 und Tooling-Notizen:
**`operations/measurement/v3-fix/FIX-LOG.md`** (mit lokalem Runtime-Bisect gegen die
echten publizierten Bytes; neue Live-Entity-IDs: Tags 20/21, Trigger 18/19).

## Kurzfassung (historisch, vor Auflösung)

Die consent-gegatete Client-GA4-Kette ist **site-seitig funktionsfähig und verifiziert**
(Consent → genau ein GTM-Loader → vollständiger Event-Push), aber die beiden GA4-Tags im
publizierten Web-Container GTM-M9TZZPLQ (Version 2) **feuern nie**. GA4 hat Stand
16.10.2026 17:45 CEMP **null Events** empfangen („No data received from your website yet",
Event count 0, Realtime leer). Der Betrieb ist nicht datenschutztechnisch, sondern
funktional blockiert: Zustimmungen laufen ins Leere, es wird nichts gemessen.

## Verifizierte Kette ( Funktionsnachweis Site-Seite, 16.10. 15:0x–17:3x CEST )

1. Live-Homepage: Consent-Annahme („Alle akzeptieren") → Cookie `zbk_consent` rev 2 mit
   `analytics_storage granted`, ad_* denied. Widerruf + erneute Annahme über die echten
   Banner-Buttons getestet.
2. Nach Consent: genau **ein** `<script src="https://www.googletagmanager.com/gtm.js?id=GTM-M9TZZPLQ">`
   (kein gtag.js, kein Stape/Service-Host). Loader-Count 1 in allen Läufen.
3. dataLayer-Abfolge korrekt: `zbk_consent_update` (consent_version 2) → `gtm.js` →
   `zbk_measurement` mit vollständigen Filterfeldern:
   `{analytics_allowed:true, consent_version:2, consent:{analytics_storage:'granted',
   ad_storage:'denied', ad_user_data:'denied', ad_personalization:'denied'},
   measurement:{event_name:'page_view', content_id:'site', cta_id:''}}`.
4. Container-Runtime installiert sich (`google_tag_manager['GTM-M9TZZPLQ']` mit vollständigem
   Laufzeit-Keyset nach Cache-Refresh; `gtm.dom`/`gtm.load` feuern).
5. Internes Datenmodell (via `google_tag_manager[...].dataLayer.get()`): alle Filterwerte
   resolve korrekt — `analytics_allowed:"true"`, `consent_version:"2"`, consent korrekt,
   `measurement.event_name:"page_view"`, `event:"zbk_measurement"`.

## Verifizierter Fehler (Negativnachweis, 4 unabhängige Seitenkontexte)

- **Kein** `gtag/js`-Request, **kein** `/g/collect`-Hit für G-5738T8FHWW in irgendeinem Lauf —
  getestet: 2 Live-Tabs, 2 lokale Mirror-Probe-Seiten (eine mit cache-gebuster Loader
  `&z=...`), Boolean- UND String-Typisierung des Pushes, Pushes vor/nach `gtm.load`,
  Wartezeiten bis 16 s.
- `Object.keys(google_tag_manager).filter(k=>k.startsWith('G-'))` bleibt leer: die googtag-
  Runtime wird nie registriert.
- Echtes CTA-Event (`data-cta-id=checklist_top`, content c04) erzeugt ebenfalls keinen Hit.
- **Tag Assistant (Quick Preview, Web-Container, nach operator-freigegebener Diagnostik-Regel,
  kein Stape-Kontingent): „No tags were evaluated in this container"** bei verbundener
  Live-Seite mit Consent + zbk_measurement-Push. Damit serverseitig bestätigt: Die publizierten
  Trigger matchen das Event nicht ODER die Tags werden auf Tag-Ebene blockiert.
- GA4-Property 559120219 (Account 412126546): Home „No data received from your website yet",
  Event count 0, Realtime leer (19:0x CEST final geprüft).

## Publizierte Konfiguration: korrekt (Bytes verifiziert)

- `https://www.googletagmanager.com/gtm.js?id=GTM-M9TZZPLQ` abgerufen (367.365 B):
  enthält Tag 14 (`__googtag`, G-5738T8FHWW, send_page_view=true, page_location fixed
  https://zuhausebleiben-kompass.de/, page_referrer/page_title leer, tag_id 14) und Tag 16
  (`__gaawe`, eventName cta_click, measurementIdOverride G-5738T8FHWW, tag_id 16).
- Makro-Map (Index→Name): 0 analytics_allowed, 1 consent_version, 2 consent.analytics_storage,
  3 consent.ad_storage, 4 consent.ad_user_data, 5 consent.ad_personalization,
  6 measurement.event_name, 7 _event, 8 measurement.content_id, 9 measurement.cta_id.
- Trigger-Regeln: `[[if 0,1,2,3,4,5,6,7 → add 0],[if 0,1,2,3,4,5,7,8 → add 1]]` mit
  Prädikaten `analytics_allowed=="true"`, `consent_version=="2"`, analytics granted,
  ad_* denied, event_name page_view/cta_click, `_event=="zbk_measurement"`.
- Identisch zum Draft-Readback `operations/measurement/gtm-draft-readback-client-side-2026-10-16.json`
  (workspace 2/3, Version 2 „ZBK v1: consent-gated client-side GA4", Live/Latest via
  `gtm versions list`).
- Kein `server_container_url` im Tag-Setup (die 3 Stringvorkommen im Bundle sind Laufzeit-
  Schlüsselnamen, keine Tag-Parameter).

## Ausgeschlossene Ursachen

- Veralteter Container im HTTP-Cache (cache-gebusterter Loader → gleiches Ergebnis).
- Boolean/String-Mismatch der Trigger-Prädikate (beide Varianten getestet → kein Fire).
- Timing (Push nach gtm.load, bis 16 s gewartet).
- Site-seitiger Consent-/Push-Fehler (Push-Inhalt im internen Datenmodell verifiziert).
- Falsche IDs (tagId G-5738T8FHWW in beiden Tags, identisch zur GA4-Property).

## Offene Ursachen-Hypothesen (nächste Prüfschritte, in dieser Reihenfolge)

1. **Tag-Level-Einstellungen, die im gtm.js-Summary unsichtbar sind:** UI-Readback Tag 14/16 —
   „Tag-Zuordnung/Consent" (z. B. „Zusätzliche Consent-Zustimmung erforderlich" oder eine
   eingebaute Consent-Prüfung, die ohne `onConsentStateUpdate` nie granted sieht),
   „Erweiterte Einstellungen → Tag-Firing-Optionen", Sequenzierung mit Blockierung.
2. **Kontroll-Test:** minimales zweites googtag-Tag ohne Filter (All-Pages) temporär im
   Preview-Modus (nicht publizieren) — feuert es, liegt es an den Triggern; feuert es nicht,
   an der googtag-/Property-Ebene (z. B. Google-Tag-Migration GT-PJRD82QZ).
3. Falls Trigger: Trigger 9/15 im UI neu speichern und Version 3 publizieren (Re-Publish
   regeneriert die Runtime-Regeln); danach denselben Probe-Ablauf wiederholen.
4. Falls Tag-Ebene: Property-Einstellungen prüfen (Stream 16133899442 aktiv, keine
   Regionsbeschränkung) und ggf. GTM-Support/Community-Pfad mit der obigen Evidenz.

## Diagnose-Notizen für Wiederholung

- GTM-UI Preview-Button öffnet Tag Assistant per `window.open` → in automatisierten Sessions
  pop-up-geblockt; URL abfangen (patch `window.open`) oder Tag-Assistant-Connect-Dialog
  (`#/?source=TAG_MANAGER&id=GTM-M9TZZPLQ&...&gtm_preview=env-17`) direkt öffnen und im
  Connect-Dialog die Site-URL per Prototype-Setter + input-Event setzen.
- Debug-Session sauber beenden („Stop debugging" je Domain-Zeile), sonst bleibt der
  Preview-Modus am Browser hängen.
- `gtm containers info`/`analysis container` respektieren den globalen CLI-Kontext NICHT
  zuverlässig (lieferte GAM Medical ES statt ZBK) — immer `--workspace`/`--path` mit voller
  Konto-Pfad-Kette verwenden und Container-Name im Ergebnis gegenlesen.
- Preview-Antwort-JSON (POST /workspaces/3/debug) enthält `previewAuthCode` + `environmentLinkId`
  — Quelle für die manuelle Tag-Assistant-URL.

## Auswirkung

- Startfähigkeit „Messung": **blockiert**. GA4-Baselinenzahlen bleiben leer, obwohl reale
  Consent-Annahmen stattfinden (mindestens eine am 16.10. 10:01 UTC dokumentiert).
- Kein Datenschutzvorfall: es fließen keinerlei Daten (auch keine Consent-Signale) nach
  Google — die Kette bricht lokal im Container.
- Site-/Consent-Code und Datenschutzerklärung sind korrekt und brauchen keine Änderung.
