# Wochenbericht ZuhauseBleiben Kompass — 14.11.–20.11.2026

Erstellt: 20.11.2026, 16:47 CET (Cron). Alle Zahlen mit Abrufdatum; Fehlendes explizit „nicht verfügbar".

## Produktion diese Woche (committed, CI success, live verifiziert)

| Artefakt | Commit / CI | Live-Readback |
|---|---|---|
| Region **Bayern** als zweite Region live (4 Wege, 31 offizielle Quellen, 141 Verbatim-Checks) | 0bb66f1, CI 43884616458 | ALL PASS + IndexNow 200 (16.11.) |
| Briefing 27: hausnotruf-smartwatch-als-ersatz (**38.** Ratgeber, Ledger 96/96) | 8d134d4, CI 43834963958 | 38/38 ALL PASS, IndexNow 200 (16.11.) |
| Briefing 28: badumbau-kosten (**39.** Ratgeber, Bad-Kosten-Journey, Ledger 58/58) | 6f454a2, CI 44050727181 | 37/37 ALL PASS, IndexNow 200 (17.11.) |
| Money-Page-Refresh treppenlift-zuschuss **Phase 1** (Förderstatus-Tabelle, Region-Inlinks, Ledger 22/22) | a1d03a2, CI 44269951299 | 25/25 ALL PASS, IndexNow 200 (18.11.) |
| Money-Page **Phase 2** (5 Money-Anchor-Links + unslop-Pass, Gate 23/23) | 1226382, CI 44315045849 | 20/20 ALL PASS, IndexNow 200 (18.11.) |
| **Aroundhome-Fix-Kette**: Impressum USt-IdNr DE305157036 (bd370dd) + wording (1a1a712, 7a1039f) + Reject dokumentiert (79134ba, 19.11.) | — | Live-Legal-Seiten 200 (20.11.) |
| **Aroundhome-Aktivierungs-Playbook + Dry-Run 22/22** (Tracker ohne Deeplink bewiesen: 302 + awc-Attribution; Build bricht ohne DSE_META kontrolliert ab) | 53afd37 (19.11.) | kein Live-Change (Approved-Sites-Klausel) |
| Adoption: hausnotruf-fuer-paare (**40.** Ratgeber, Quelle im Repo) | 2fafb93 (20.11.) | 13/13 ALL PASS, IndexNow 200/5 URLs (8606b2d) |
| **dist-Clean zu Build-Beginn** (Orphan-Fehlerklasse des paare-Incidents geschlossen, ROOT-Guard, Gates 18/18) | 5a18bf9, CI 44745003782 | 19/19 ALL PASS auf öffentlicher URL (223075d, 20.11.) |
| ADCELL-GO-Pack 20.11. re-verifiziert (HIRO 9440 + Pflegehase 10690, **0 Drift** zu 06.11.) | 5a18bf9 | Evidenz research/evidence/adcell-refresh-201126/ |

## Website/Domain (live geprüft 20.11. 16:50)

- Homepage, NRW, Bayern, treppenlift-zuschuss, hausnotruf-fuer-paare, badumbau-kosten, Datenschutz, Impressum: je **HTTP 200, robots `index,follow`**.
- Sitemap.xml: **53 locs**, davon 8 Checklisten-URLs (Hub `/checklisten/` + 7 druckbare Checklisten); robots.txt mit Sitemap-Direktive.
- RSS `/rss.xml`: **40 Items** (200).
- DNS/HTTPS: unverändert GitHub Pages; Mail-DNS unangetastet.

## Partner-/Vertriebsstatus (Postfach frisch geprüft 20.11. 16:50: **keine neuen Partner-Antworten** seit 17.11. — letzte Mail = OOO-Autoreply 11237)

- **Malteser 112616**: zugelassen, 5 Placements live. Terms (Beleg 11235, 17.11.): 10 € wahrgenommener Beratungstermin; Infomaterial für Premium-Partner **0,25 € CPL**, „im Programm hinterlegt".
- **Aroundhome 68536 (Awin)**: Test zugesagt (30 % RevShare, Textlink, iFrame abgelehnt); formale Bewerbung im System offen (6c17fb4), Publisher-ID 3124891 nachgereicht (Sent 1027). **Agency (Artefact) zurück ab 23.11.** → Freischalt-Readback → Aktivierung = 1 Commit nach Playbook (partner-links.json + DSE_META im selben Commit; Dry-Run 22/22 grün). Fallback, falls keine Freischaltung: **Reapply ab 20.12.** (USt-IdNr jetzt im Impressum live).
- **Liftstar 40988 (Awin)**: „offen" seit 15.10., Follow-up 13.11. (Sent-Beleg 37), weiter unbeantwortet.
- **ADCELL-GO**: Registrierungs-Pack textfertig + 20.11. re-verifiziert (0 Drift); GO bleibt Betreiber-Akt (Joint-Controller-Checkbox) — schnellster zweiter Partner-Hebel (HIRO 50 €/Lead, 90 T. Cookie; Pflegehase 25 €/Lead).
- **Treppenlift-Lotse**: Enquiry 12.11., unbeantwortet.

## Messung — nicht verfügbar (Zugang fehlt, nicht Messung=0)

- **Search Console: nicht verfügbar** — `gcloud auth list` leer (20.11. 16:50 verifiziert). Keine Query-/Abdeckungszahlen.
- **GA4-Zahlen: nicht verfügbar** — Sammelkette steht (Web-GTM v5 → G-5738T8FHWW, Empfangsnachweis 16.10.); Report braucht Google-Sitzung.
- **Leads/Umsätze: nicht verfügbar** — kein Awin-Report-Zugang, keine Zahlungseingänge nachweisbar. Keine Prognose.
- **Token/Toolkosten: nicht verfügbar** (kein Verbrauchsmesszugang). Keine Ausgaben, Verträge, Budgets getätigt.

## Nächste Priorität

1. **23.11. Agency-Rückkehr** → Aroundhome-Freischalt-Readback (Agency-Mail oder Netzwerk) → 1-Commit-Aktivierung nach Playbook → Gates + Live-Readback.
2. **ADCELL-GO** (Betreiber-Akt, Pack fertig) parallel Richtung HIRO/Pflegehase.
3. Awin-Login (Liftstar-Status, Malteser-Kommissionliste) und Google-Sitzung (GSC-Queries/Sitemap-Status) — jeweils einmalige Nutzer-Akte.
4. Danach GSC-gestützt: Rest blitz-seo Phase 2 (2 reale Queries), Titel-Matching, nächste Region/Cluster erst nach Kompakt-Check.
