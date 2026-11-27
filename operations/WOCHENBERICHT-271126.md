# Wochenbericht ZuhauseBleiben Kompass — 21.11.–27.11.2026

Erstellt: 27.11.2026, 16:52 CET (Cron). Alle Zahlen mit Abrufdatum; Fehlendes explizit „nicht verfügbar".

## Produktion diese Woche (committed, CI success, live verifiziert)

| Artefakt | Commit / CI | Live-Readback |
|---|---|---|
| Region **Hessen** als fünfte Region live (WIBank „Behindertengerechter Umbau von Wohneigentum": Zuschuss bis 50 %/max 15.000 €, Lift-/Aufzugseinbau-Höchstbetrag 6.500 €; Ledger 155/155 + NDS-Screen 108/108) | caafa02, CI 45788202093 | 57/57 ALL PASS, IndexNow 200 (26.11.) |
| Region **Niedersachsen** als sechste Region live (NBank: Zuschuss bis 15.000 € / Darlehen-Zweig ab 15.001 €; Freibetrag 4.000 € GdB≥50; Treppenlift 0× in amtlichen NDS-Dokumenten ehrlich dokumentiert) | 334db44, CI 45969164698 | 67/67 ALL PASS, IndexNow 200 (27.11.) |
| Region **Mecklenburg-Vorpommern** als siebte Region live (RLPaBaWo M-V: reiner Zuschuss 30 %/max 15.000 € = **4.500 € für Treppenlift namentlich**, keine Einkommensgrenze, Mieter ausdrücklich antragsberechtigt; Screen 2 Subagenten, 129+129 Zitate verbatim, Parent-Live-Verify 48/48) | 5d46c13, CI success auf voller SHA | 70/70 ALL PASS, IndexNow 200 (27.11.) |
| Docs-Batches (Batch-Protokolle + launch-state/pipeline-state) | 6f73fd9, 0968882, 80d8a35 | — |
| Region-Screen Berlin/Bremen/Rheinland-Pfalz **verworfen mit Beleg** (Kredit-Route statt Landes-Zuschuss; `research/region-screen-271126-*.md`); Restkandidaten SH/Saarland/BB/TH/HH/ST | in 5d46c13/80d8a35 dokumentiert | — |

Wochenbilanz Produktion: **3 neue Landes-Regionen live** (Hessen, Niedersachsen, M-V → 7 Regionen indexiert), Sitemap 53→60 URLs.

## Website/Domain (live geprüft 27.11. 16:52)

- Homepage **HTTP 200, robots `index,follow`**; Region MV 200 `index,follow`.
- Sitemap.xml: **60 locs**; RSS: **41 Items**; robots.txt mit Sitemap-Direktive.
- Partner-Marker live verifiziert: `aroundhome_badumbau_angebote` auf badumbau-angebote-vergleichen mit `rel="sponsored noopener"` + „Anzeige · Kooperation mit Aroundhome DE"; beide Malteser-Placements auf hausnotruf-kosten-anbieter-vergleich.
- DNS/HTTPS unverändert GitHub Pages; Mail-DNS unangetastet.
- GA4-Sammelkette: Empfangsnachweis vom 06.11. dokumentiert (/g/collect 204 + Realtime); statisch heute nicht re-prüfbar (Loader konsent-gated dynamisch injiziert) — Zahlen siehe Messung.

## Partner-/Vertriebsstatus (Postfach frisch geprüft 27.11. 16:48: **keine neuen Antworten** seit Beleg 11239 vom 25.11.)

- **Blocker-Aktion heute: Lifta-Erinnerung Nr. 2 gesendet** (Sent-Beleg **1034**, 27.11. 17:00, an gkashtanjeva@liftstar.de, CC koop@; Entwurf `operations/lifta-nudge2-271126.eml`). Bewerbung 40988 (50 €/Lead bzw. 500 €/Auftrag) liegt seit 15.10. offen; Follow-up 13.11. (Sent 1025) blieb unbeantwortet. Mail fragt explizit nach Status/Absage und wiederholt die vier Erstfragen (T&C, Pinterest, Leadübernahme, Datenschutz).
- **Malteser 112616**: zugelassen + 2 Placements live. Terms belegt (11235, 16.11.): 10 € wahrgenommener Beratungstermin; Infomaterial für Premium-Partner 0,25 € CPL (Partner-Angabe, im Login prüfbar).
- **Aroundhome 68536**: zugelassen (Beleg 11239) + 2 Textlink-Placements live seit 25.11. **Weitere Placements erst nach den ersten gematchten Leads** — ablesbar nur im Awin-Login.
- **ADCELL-GO** (HIRO 9440: 50 €/Lead Treppenlift; Pflegehase 10690: 25 €/Lead Hausnotruf): Pack textfertig, Registrierung bleibt **Betreiber-Akt** (Joint-Controller-Checkbox).
- Treppenlift-Lotse: Enquiry 12.11., weiter unbeantwortet.

## Messung — nicht verfügbar (Zugang fehlt, nicht Messung=0)

- **Search Console: nicht verfügbar** — `gcloud auth list` leer (27.11. verifiziert). Keine Query-/Abdeckungszahlen.
- **GA4-Zahlen: nicht verfügbar** — Sammelkette steht (Web-GTM v5 → G-5738T8FHWW, Empfangsnachweis 06.11.); Report braucht Google-Sitzung.
- **Leads/Umsätze: nicht verfügbar** — kein Awin-Report-Zugang, keine Zahlungseingänge nachweisbar. Keine Prognose.
- **Token/Toolkosten: nicht verfügbar** (kein Verbrauchsmesszugang). Keine Ausgaben, Verträge, Budgets getätigt.

## Einmalig erforderliche Freigaben (Unverändertes — kein neues Arbeitsfeld)

1. **Awin-Login** (Nutzer-Session oder Vault-Eintrag, geschützter Dialog) — würde drei Fragen gleichzeitig auflösen: Lifta-Bewerbungsstatus, Malteser-Kommissionen, Aroundhome gematchte Leads.
2. **Google-Sitzung** (GSC + GA4) — erste reale Query-/Abdeckungszahlen nach 7 Regionen-Launch.
3. **ADCELL-GO** — Registrierung mit Joint-Controller-Zustimmung (Betreiber-Akt).

## Nächste Priorität

1. Lifta-Rückmeldung (Erinnerung Sent 1034) → bei Zusage: Aktivierung nach Playbook mit Treppenlift-Cluster-Placements (1-Commit-Pfad steht).
2. Aroundhome: erste gematchte Leads im Awin-Login prüfen → danach weitere Bad-Cluster-Placements freigeben.
3. ADCELL-GO → zweiter Netzwerk-Kanal (HIRO/Pflegehase).
4. GSC-Sitzung → datenbasiert entscheiden: weitere Region (SH/Saar/BB/TH/HH/ST) oder Phase-2-Verbesserung bestehender Seiten.
