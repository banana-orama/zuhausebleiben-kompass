# Batch 6: Promotion Briefing 1 — treppenlift-angebote-vergleichen (2026-10-23, Cron-Lauf)

## Was dieser Lauf getan hat

Der vollständig gegatete Entwurf von 2026-10-14 (content-drafts/treppenlift-angebote-vergleichen.*,
Preview-only, noindex) wurde nach Re-Verifikation gegen die Live-Originale als 20. Ratgeber
freigegeben. Er war der einzige Phase-1-Briefing, der nie promoviert wurde (Briefings 2–9 live);
Geld-Intent („Treppenlift-Angebote vergleichen") lag damit 9 Tage als toter Draft herum.

## Re-Verifikation (2026-10-23, alle Quotes maschinell im Seiten-Text bestätigt)

Skript: Scratch `verify-briefing1-sources.py` (Fetch + Entity-Decode + Whitespace-Normalize + Asserts).
- § 40 SGB XI (gesetze-im-internet): PASS — 4 180 € / 16 720 €, „können subsidiär", 3 Wochen,
  5 Wochen (MD). [ISO-8859-1 + Entities dekodiert, geschützte Leerzeichen normalisiert]
- Verbraucherzentrale Treppenlifte: 13/13 Artikel-Claims PASS (Festpreis/20 %, „zahlen Sie erst,
  wenn … eingebaut und funktionstüchtig", Wartung versteckte Kosten, Notrufnummer, Vergleichsangebote,
  kostenloser Kostenvoranschlag, Sitzlift für Gehbehinderte, Notabsenkung, 12 Monate + 14 Tage,
  40 % Steuerersparnis, Umbau erst nach Bewilligung, Nacherfüllung kostenfrei).
- Verbraucherzentrale BGH I ZR 96/20: PASS (individuell gefertigter Kurventreppenlift, Werkverträge,
  außerhalb von Geschäftsräumen, Az.).
- Arithmetik PASS (Skript `check-briefing1-math.py`): 4.670 / 17.290 / 21.960 / 340 / 2.140 / 4×4.180=16.720.
- Quellenstand in sources[].checked_at: 2026-10-23 (nur die heute tatsächlich abgerufenen Quellen).

## Konversion Draft → content-ready

- Alle `[unverified]`-Marker entfernt (Renderer-Ausgabe wäre Literaltext); Citations [1][2][3] unverändert.
- `ol`-Blöcke → Bullets („Schritt 1–5" mit Präfix; Fragenliste als unnummerierte Liste — Renderer kennt kein ol).
- Tabellen-Caps in Absatztexte integriert (Attribution + Citation erhalten).
- `img`-Block → article-level `image` (Renderer platziert die Figure nach dem TOC).
- Section „Sieben Fragen…" → „Fragenliste: Sieben Fragen …" (checklistIndex-Regex greift → Early-CTA
  „Zur Checkliste" zeigt auf die echte Fragenliste, kein generisches Ziel).
- Preview-Prosa korrigiert (Index-Flip-Pflicht): Grenzen-Bullet „Diese Seite ist ein Entwurf in einer
  Vorschau … bis zum regulären Start noindex" → truthful Launch-Formulierung (Angebotsvermittlung
  nicht eingerichtet, keine Kontaktdaten). Transparenz: Prüfdatum 23.10.2026.
- SVG `angebot-aufbau.svg` (git mv) → assets/images/; Manifest-Eintrag ergänzt;
  Fußzeilen-Quellenstand der Grafik 14.10. → 23.10.2026 (heutige Re-Verifikation).

## Renderer/Generator

- generate.mjs: DRAFT_PAGES-Konstante + kompletter Preview-Draft-Block entfernt; obsolete
  Draft-SVG-Kopie entfernt (CNAME-Write erhalten). Damit existiert die URL in beiden Modi als Artikel.
- article-renderer.mjs: specialMap-Eintrag `treppenlift-angebote-vergleichen → /treppenlift-zuschuss.html
  „Förderung prüfen"` (Artikel hat eigene Förder-Sektion; Lift-Cluster). Related-Links automatisch
  Lift-Cluster (firmen-vergleich, gebraucht-oder-neu, kosten).

## Gates (alle 2026-10-23 lokal, Launch-Dist)

- test_site: PASS 44 Seiten (1 H1 je Seite, 0 Formulare, interne Links, XML).
- test_articles: PASS 20/20 (Zähler 19→20 im selben Changeset; Bilder, Anker, JSON-LD).
- verify_checklists_build: ALL PASS (Sitemap enthält Artikel, RSS 20 Items, llms.txt deckt alle
  content-ready-Slugs ab — SUMMARIES-Eintrag + SECTION_MAP ergänzt).
- test_partner_links: ALL PASS (inactive Build null Partner-Marker; A2 ≥ 20).
- Playwright consent+measurement: 13 passed. (checklists.spec.mjs des Parallel-Runs weiter außen vor —
  bekannt unfertig, nicht Teil von CI.)
- PREVIEW-Modus: Artikel noindex,follow, Sitemap leer (0 <loc>) — Vorschau-Vertrag intakt.
- Mobil 390 px: horizontaler Overflow 0 px; Tabellen im Scroll-Container; Early-CTAs sichtbar.
- SVG-Sichtkontrolle (Playwright-Chromium-Screenshot): kein Textüberlauf, Werte als „frei erfunden"
  gelabelt, KI-Kennzeichnung sichtbar. (Chrome-headless segfaultet in dieser Session; Playwright
  übernommen.)

## Abgrenzung

- treppenlift-firmen-vergleich (Anbieterwahl, Entscheidungsmatrix, Grafik ohne Beispielwerte) und
  treppenlift-kosten (Kostenstruktur) unangetastet; Intent-Abgrenzung wie im Briefing dokumentiert.
- Root citations-ledger.json (Draft-Ledger) bleibt als historische Evidenz liegen; kein Code liest es.
- Keine Formulare, keine Partnerlinks, keine Preis-Marktangaben; Alle Beträge als erfunden gekennzeichnet.
