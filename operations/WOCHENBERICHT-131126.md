# Wochenbericht ZuhauseBleiben Kompass — 07.11.–13.11.2026

Erstellt: 13.11.2026, 16:47 CET (Cron). Alle Zahlen mit Abrufdatum; Fehlendes explizit „nicht verfügbar".

## Produktion diese Woche (verifiziert committed + live)

| Artefakt | Commit/CI | Live-Readback |
|---|---|---|
| Briefing 24: wohnung-anpassen-nach-krankenhausentlassung (35. Ratgeber) | 424d925, CI success | 54/54 ALL PASS, Sitemap 46 locs |
| Briefing 25: treppenlift-aufmass-termin (36. Ratgeber, Lift-Journey komplett) | b07a856, CI 43231174256 | 30/30 ALL PASS, Sitemap 47 locs |
| Briefing 26: hausnotruf-alarm-ablauf (37. Ratgeber) | b643b4f, CI 43396950662 | 31/31 ALL PASS, Sitemap 48 locs |
| Renderer-Fix: Intro-Arrays als eigene Lead-Absätze (6 Artikel live betroffen) | 94556ac | npm test EXIT 0 |
| **Region NRW als erste Region live** (4 Förderwege, 10 offizielle Quellen, Hub+11 Platzhalter noindex) | fe7f225, CI 43436255111 | 38/38 ALL PASS, Sitemap exakt 49 locs, NRW als einzige Region |
| Partner-Terms-Lauf: Malteser 10-€-CPL re-verifiziert, Lotse aufgelöst (GESMIK GbR, 60–120 €/Lead), 3 sendefertige Entwürfe | 5f9e0c2 | Ledger 9 Quellen/20 Zitate verbatim |

Neue SVG-Diagramme: je Batch (3-Zeiten-Wegweiser B24, Aufmaß-Strecke B25, Alarmkette B26, NRW-Regionsgrafik) — alle mit getBBox+Vision-Gate.

## Website/Domain (live geprüft 13.11. 16:50)

- Homepage + `/region/nordrhein-westfalen.html`: HTTP 200, robots `index,follow`.
- Sitemap.xml: **49 locs**, davon 8 Checklisten-URLs (Hub + 7 druckbare Checklisten), NRW als einzige Region.
- RSS `/rss.xml`: **37 Items** (200); robots.txt mit Sitemap-Direktive (200).
- DNS/HTTPS: unverändert GitHub Pages, keine Änderungen; Mail-DNS unangetastet.

## Partner-/Vertriebsstatus

- **Liftstar-Follow-up gesendet 13.11. (Gesendet-Beleg ID 37)** — Bewerbung Awin 40988 seit 15.10. „offen", Nachfassen war seit 22.10. fällig; Draft zuvor auf 37 Ratgeber/7 Checklisten aktualisiert.
- Aroundhome (Awin 68536): Qualifizierungsfragen 13.11 beantwortet (Sent 1024, Commit 8e5b64c) → **Warten auf Entscheidung**.
- Treppenlift-Lotse-Enquiry + Malteser-Terms-Enquiry: 12.11 gesendet (3× SMTP 250, Commit a38e2cc) → **bisher keine Antworten** (Posteingang 13.11 geprüft: nur die bereits beantwortete Aroundhome-Mail).
- Malteser 112616: zugelassen; Placements live (beratungstermin auf 3 Artikeln, info-material auf 2, 10 €-CPL, rel=sponsored).
- Posteingang 13.11. 16:50 geprüft: keine neuen Partner-Antworten.

## Messung — nicht verfügbar (Zugang, nicht Messung fehlt)

- **Search Console: nicht verfügbar** — kein aktives gcloud-Konto/Token im Cron (13.11 verifiziert: `gcloud auth list` leer, kein Access-Token). Keine Null als Messung ausgegeben.
- **GA4-Zahlen: nicht verfügbar** — Sammelkette ist verifiziert (Web-GTM v5 → G-5738T8FHWW, Empfangsnachweis 16.10.), aber UI-/API-Report braucht Google-Sitzung, die im Cron fehlt.
- **Leads/Umsätze: nicht verfügbar** — kein Awin-Report-Zugang (Login im Cron tot); keine Zahlungseingänge nachweisbar. Keine Prognose.
- **Token/Toolkosten: nicht verfügbar** (kein Verbrauchsmesszugang). Keine Ausgaben, Verträge oder Budgets getätigt.

## Betriebsblocker (nur Betreiber-Akte, unverändert)

1. **ADCELL-GO**: Registrierung Joint-Controller-Zustimmung = Betreiber-Akt; Formulareinträge fertig in `operations/ADCELL-GO-PACK.md` (HIRO 9440 50 €/Lead 90 T. Cookie + Pflegehase 10690 25 €/Lead).
2. **Awin-Login** (einmalige Nutzer-Session): löst Status-Readback Lifta 40988 + Malteser 112616 + Aroundhome-Bewerbung 68536 ein.
3. **Google-Sitzung** für GSC/GA4-Reports (Sitemap-Einreichung + Query-Daten).

## Nächste Priorität

1. Liftstar-/Lotse-/Malteser-Terms-Rückmeldungen abwarten (Follow-up-Frist: ~20.11. erneut prüfen).
2. Nach Aroundhome-Entscheid: Aktivierung per Config-Gate + DSE-Abschnitt im selben Commit (Gate F erzwungen).
3. Region #2 erst nach gleichem Muster (10+ offizielle Quellen verbatim, expand-or-noindex-Gate) — doorway-Regel unverändert.
4. GSC-Queries/Sitemap-Status sobald Google-Sitzung verfügbar.
