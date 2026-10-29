# Zitat-Link-Rot-Audit 29.10.2026 — alle externen Quellen-URLs im Built

Umfang: 112 unique externe URLs aus 28 gebauten Seiten (dist/*.html, 25 Ratgeber + Rechts-/Meta-Seiten).
Methode: curl -L mit Browser-UA (Retry 1, 30 s Timeout); alle Nicht-200 zusätzlich im echten
Browser geprüft; Wayback-/CDX-Kreuzcheck für Sperrverdacht. Rohdaten:
`linkrot-291026-urls.json` (Extraktion), `linkrot-291026-status.tsv` (Status je URL).

## Ergebnis

| Status | n | Bewertung |
|---|---|---|
| 200 | 106 | OK |
| 404 | 1 | **echter Rot → ersetzt** |
| 403 | 3 (+ Homepage) | WAF-Sperre gegen Rechenzentrum-Ausgang, kein Rot (siehe unten) |
| 503 | 1 | transient/curl-only; im Browser 200 |
| curl ERR | 1 | transient; Retry 200 |

## Befunde und Aktionen

1. **Verbraucherzentrale „Widerruf – Verträge rückgängig machen" (…-70049): 404 für alle.**
   Zitiert in `hausnotruf-kosten-anbieter-vergleich.json` (Quelle [4], Aussage: gesetzliches
   Widerrufsrecht bei Online-/Telefonabschluss, VZ erklärt Grundlagen). Ersetzt durch
   „Verträge wirksam widerrufen per E-Mail, SMS oder Fax" (Stand 28.07.2026):
   `https://www.verbraucherzentrale.de/wissen/vertraege-reklamation/kundenrechte/vertraege-wirksam-widerrufen-per-email-sms-oder-fax-das-muessen-sie-beachten-22947`
   — unterstützt dieselbe Aussage wörtlich („Bei bestimmten Verträgen haben Sie als
   Verbraucher:in ein gesetzliches Widerrufsrecht. Wenn Sie im Internet …"; „14 Tage und
   beginnt bei Warenbestellung mit vollständigem Erhalt der Ware"). Belegtext:
   `evidence/linkrot-291026/vz22947-widerruf.txt`. Die Leicht-Sprache-Variante der alten Seite
   (de-x-simple/…-70049) existiert, ist aber als Primärquelle für die Standardformulierung
   ungeeignet. Prosa unverändert — die Sätze bleiben mit der neuen Quelle wörtlich gedeckt.
   checked_at → 2026-10-29 (Browser-Abruf heute).
2. **gesetze-im-internet WOeiGG §20** (treppenlift-mietwohnung): curl ERR/000 im Batch,
   Einzelabruf danach zweimal 200 → transient (Rate-Limit der Batch-Sequenz), kein Rot.
   checked_at → 2026-10-29.
3. **REHADAT GKV-Hilfsmittelverzeichnis Produkt 33.40.05.0006** (hilfsmittel-dusch-wc):
   curl 503, im echten Browser 200; Verzeichnisstand „Bundesanzeiger 28.09.2026" weiterhin
   im Seitentext → die Verzeichnisstand-Angabe im Artikel bleibt korrekt. checked_at → 2026-10-29.
4. **pflege.net (3 Artikelquellen + Homepage): 403 in curl UND echtem Browser.**
   Betroffen: hausnotruf-sturzerkennung-oder-knopf [1], treppenlift-mieten [3],
   treppenlift-mietwohnung [6]. Bewertung: domainweite WAF gegen Rechenzentrums-IPs, kein
   Content-Rot — Sturzsensor-Seite hat Wayback-Snapshot 200 vom 13.10.2026, alle drei Seiten
   wurden 15./16.10. redaktionell verifiziert (Evidence-Dateien in research/evidence/).
   Aktion: Links und checked_at (15./16.10.) UNVERÄNDERT gelassen — kein Datum-Refresh ohne
   tatsächliche Re-Verifikation. **Offener Punkt:** Erreichbarkeit aus Residential-Kontext
   prüfen (nächste Desktop-/GSC-Sitzung). Falls auch dort 403: Ersatz-Recherche für drei
   lasttragende Quellen (Sturzerkennungs-Grenzen, Mindestmietdauer-Warnung, Rückbaupflicht).

## Nicht geändert

- 106 intakte Quellen-URLs, darunter alle gesetze-im-internet-Einzelnormen, BMG, KfW,
  GKV-Spitzenverband, Verbraucherzentrale (übrige), hiro/lifta-Produktseiten (28.10. verifiziert).
- Alt-Historie `research/evidence/batch2-hausnotruf-evidence.md` behält die alte URL als
  dokumentierte Geschichte.

## Nachweis der Änderungen

- `content-ready/hausnotruf-kosten-anbieter-vergleich.json` — Quelle [4] ersetzt (URL, Titel, Datum)
- `content-ready/treppenlift-mietwohnung.json` — WOeiGG §20 checked_at → 2026-10-29
- `content-ready/hilfsmittel-dusch-wc-uebernahme.json` — REHADAT checked_at → 2026-10-29
- Rebuild + Gates + Live-Readback: siehe Commit (dieser Audit wird mit den JSON-Änderungen committet).

## Update 29.10., Nachmittag (zweiter Lauf)

- Der auf diesem Audit aufbauende SEO-Audit-Fix-Commit **b120a2e** (Audit-Fixes 1+8+6a aus
  seo-audit-zbk, Evidenz-Snapshot 19.10.) lag 3 h unpushed lokal und wurde vom Nachmittagslauf
  adoptiert: npm test grün, Schema-Gate ALL PASS, CI success, **Live-Readback 26/26 PASS**.
  Protokoll: `research/evidence/schema-push-291026/READBACK-LOG.md`.
- Staleness-Abgleich gegen den Live-Stand: die Audit-Findings **#2 (llms.txt 404) und
  #3 (Checklisten orphaned)** sind veraltet (llms.txt seit 21.10. live 200; Checklisten-Hub
  vom Home via absoluter href verlinkt und in der Sitemap — der Audit-Grep erfasste nur
  relative hrefs). **#4 (datenschutz.html fehlt in der Sitemap) ist weiterhin wahr.**
- pflege.net (Punkt 4 oben) unverändert: 403 = DC-WAF, Residential-Check offen,
  Ersatz-Recherche (Sturzerkennung/Mietdauer/Rückbau) bleibt bedingt zurückgestellt.
