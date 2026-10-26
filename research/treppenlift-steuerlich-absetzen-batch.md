# Batch 7 (26.10.2026, Cron-Lauf): Briefing 10 — Treppenlift/Badumbau steuerlich absetzen

**Artikel:** `content-ready/treppenlift-steuerlich-absetzen.json` · Slug `/treppenlift-steuerlich-absetzen.html`
**Status vor Commit:** editorial-reviewed-preview (Freigabekette in diesem Protokoll) · Grafik `assets/images/treppenlift-steuer-weg.svg`
**GSC-Hinweis:** GSC-Queries weiterhin nicht abrufbar (Cron-Browser ohne Google-Sitzung, Vault ohne Google-Login) — Topic-Wahl daher SERP-/Quellen-basiert, nicht GSC-basiert. Kein Passwort erfragt.

## Motiv und Abgrenzung (Kannibalisierungs-Check)
- SERP „treppenlift steuerlich absetzen" (26.10.2026): Treppenlift-Portale (vdbmedical, treppenlift-berater.info, aufzugsanlage.net, pflege.net, treppenliftwissen.de) + Steuerblogs; ein Badsanierungs-Anbieter behauptet fälschlich, „bestimmte Materialkosten" seien absetzbar — das Gesetz sagt das Gegenteil (nur Arbeitskosten). Unsere Verbesserung: Rechtstext-Anker (§ 35a + § 33 wörtlich), Förderverschränkung (§ 35a Abs. 3 Satz 2), Referentenentwurf-2027-Trennung, Dokumenten-Checkliste.
- `grep steuer` über alle content-ready-Dateien vor Start: nur „Umsatzsteuer"-Treffer — keine Überschneidung mit treppenlift-zuschuss (Pflegekasse/KfW) oder badumbau-angeboten. Intent-distinct: Steuer-Route vs. Sozialleistungs-Route; Artikel verlinkt Zuschuss-Ratgeber als Anschluss, nicht als Dublette.

## Kernbefunde (alle verbatim im Ledger, 41/41 PASS)
1. **Live-Rechtstext weicht vom Portal-Echo ab:** § 35a Abs. 3 EStG (Abruf 26.10.2026) lautet „Renovierungs-, **Erhaltungs- und Modernisierungsmaßnahmen**" — nicht mehr „Instandhaltungs-/Instandsetzungsarbeiten". 20 %, max. **1 200 €**.
2. **Förderverschränkung im Gesetz:** „Dies gilt nicht für öffentlich geförderte Maßnahmen, für die zinsverbilligte Darlehen oder steuerfreie Zuschüsse in Anspruch genommen werden." (§ 35a Abs. 3 Satz 2) — Kernabschnitt des Artikels, keine Einzelfallinterpretation.
3. **Reform im Blick:** Referentenentwurf Einkommensteuerreformgesetz 2027 (18.08.2026): 15 % / max 900 € ab 2027 geplant, **nicht beschlossen** (Finanztip-Darstellung, wörtlich belegt). Artikel trennt strikt geltendes Recht (20 %/1.200 €) vom Entwurf.
4. § 35a Abs. 5: nur Arbeitskosten; Rechnung + Zahlung auf Konto des Leistenden; keine Doppelbegünstigung mit § 33 (Abs. 5 Satz 1); EU/EWR-Haushalt (Abs. 4); Höchstbetrag haushaltsbezogen (Alleinstehenden-Regelung).
5. § 33 EStG: „zwangsläufig" (Abs. 2), Abzug erst oberhalb der zumutbaren Belastung (Abs. 3, 1–7 % je Einkommen/Kinder).
6. Finanztip (Stand 07.07.2026 laut Seite): max 6.000 € Arbeitskosten → 1.200 €; Anlage „Haushaltsnahe Aufwendungen" Zeile 6 (SJ 2025); Aufteilung Lohn/Material auch prozentual; Werkstatt-Anteil nicht begünstigt (BFH VI R 4/18); Mieter/Eigentumswohnung/Nebenkosten-Punkte; öffentliche Förderung → nicht begünstigt (KfW-Beispiel).
7. Pflegekassen-Verschränkung: erhaltene Zuschüsse sind keine eigenen Aufwendungen (Erstattungsprinzip, Finanztip aB); Eigenanteil zählt — Einzelfall klärt das Finanzamt.

## Beispielrechnung (tool-geprüft, research/verify_steuer_261026.py)
Fiktiv: Material 3.700 € + Arbeits-/Fahrtkosten 2.800 € = 6.500 € Rechnung → begünstigt 20 % × 2.800 = **560 €**. Konsistenz: 6.000 × 20 % = 1.200; 1.200/0,20 = 6.000; 900/0,15 = 6.000 (Entwurf). Alle Werte als erfunden gekennzeichnet.

## Quellenkette (Abrufe 26.10.2026)
- § 35a EStG: https://www.gesetze-im-internet.de/estg/__35a.html — ISO-8859-1/Entities/Soft-Hyphens gecleaned, Evidence `research/evidence/steuer-261026/estg__35a.txt`, 8 Zitate verbatim.
- § 33 EStG: https://www.gesetze-im-internet.de/estg/__33.html — Evidence `estg__33.txt`, 4 Zitate verbatim.
- Finanztip Handwerkerkosten: https://www.finanztip.de/handwerkerkosten/ — Evidence `finanztip-handwerkerkosten.txt`, 20 Zitate verbatim (inkl. Referentenentwurf-Absatz).
- Finanztip außergewöhnliche Belastungen: https://www.finanztip.de/aussergewoehnliche-belastungen/ — Evidence `finanztip-aussergewoehnliche-belastungen.txt`, 4 Zitate verbatim.
- Ledger: `research/steuer-261026-ledger.json` · Verifizierer: `research/verify_steuer_261026.py` (41/41 PASS).
- VZ hatte keinen §-35a-Artikel (Site-Suche geprüft) → Finanztip als Verbraucher-Fachquelle, Gesetzeszitate primär.

## Grafik
`assets/images/treppenlift-steuer-weg.svg` (980×740): Entscheidungsschema Weg 1/Weg 2 + Förderfalle + Fußzeile mit Stand/Entwurf. KI-unterstützt, als Schema gekennzeichnet; Umlaut-freie Texte (Projektkonvention). **Sichtkontrolle fand 2 Layoutfehler** (Badge überlappte Weg-1-Header; Weg-2-Header lief über Kartenrand) → zweizeilige Header, Badge entfernt, Re-Check: getBBox 0 Overflows, Vision-Sichtprobe „keine Auffälligkeiten". Screenshots als Evidence: `research/evidence/steuer-261026/svg-vollansicht.png`, `mobile-artikel.png`.

## Gates (alle in diesem Lauf, Launch-Build)
- npm run build (PREVIEW, 41 Seiten noindex) + build:launch (LAUNCH, Sitemap 7 Checklist-URLs) — beide PASS.
- test_site.py PASS (45 HTML-Seiten) · test_articles.py PASS (20→**21** Artikel, Anker/Bilder/JSON-LD/SVG-XML).
- verify_checklists_build.py ALL PASS (RSS 20→**21** Items; llms deckt alle ab; Content-Keys im HTML).
- test_partner_links.py ALL PASS (A2 ≥ 21).
- Playwright consent 20 passed · measurement-Policy-Tests PASS.
- Neu: `research/verify_steuer_content_261026.py` — jeder Key des Artikel-JSON (Paragraphen, Bullets, Tabellenzellen, paragraphs_after, FAQs) im gebauten HTML; [1]–[4] auflösen und alle zitiert; Related-Links 3× treppenlift-Cluster; Early-CTA compare_top → „Förderung prüfen" → treppenlift-zuschuss. ALL PASS.
- Mobile 390 px: 0 px Overflow, 4 Quellen/Grafik/6 FAQs vorhanden (Playwright-Chromium; headless Chrome segfaultet im Cron).
- Renderer: specialMap-Eintrag treppenlift-steuerlich-absetzen → treppenlift-zuschuss; llms-txt.py SUMMARIES + SECTION_MAP erweitert.

## Pflicht-Refresh
- **Nach Verabschiedung des ESt-Reformgesetzes 2027 (erwartet Ende 2026):** § 35a-Kennzahlen + Abs.-3-Wortlaut neu gegen gesetze-im-internet; Article-Claims (20 %/1.200 € vs 15 %/900 €) und FAQ 6 anpassen. Notiz steht im Ledger (`notes`).
