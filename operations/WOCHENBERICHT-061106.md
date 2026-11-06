# Wochenbericht ZuhauseBleiben Kompass — 06.11.2026 (Zeitraum 24.10.–06.11.)

Erstellt: 06.11.2026, 16:48 CET (Cron). Alle Zahlen mit Abrufdatum; fehlende Metriken ausdrücklich „nicht verfügbar", keine Nullen als Messung, keine Prognosen als Ergebnis.

## Produktion

- **Ratgeber: 20 → 30** (Briefings 10–19 dieses Zeitraums, u. a. treppenlift-schmale-treppe 26.10., aussentreppen-aussenlift 27.10., wohnumfeldverbesserung 02.11., hausnotruf-mobil-gps 04.11., hausnotruf-kuendigen 05.11., sitzlift-oder-stehlift 06.11., hausnotruf-schluesselhinterlegung 06.11.) — jeder Artikel mit Verbatim-Ledger (40–99 Checks), Content-/SVG-/Mobile-Gates, CI success und öffentlichem Live-Readback.
- **Checklisten: 6 → 7 druckbare Blätter + Hub** (neu: „Hausnotruf kündigen", 05.11. — Link-Magnet aus Ratgeber 28, keine neuen Zahlen/Quellen).
- **Live-Readback heute 06.11. 16:48:** Homepage HTTP 200, robots `index,follow`, Sitemap 41 URLs, RSS 30 Items, llms.txt 200, robots.txt mit Sitemap-Direktive. Domain zuhausebleiben-kompass.de via GitHub Pages (Server-Header GitHub.com), Mail-DNS unangetastet.
- Qualitäts-Fixes im Zeitraum: 24 Artikel-Titel/Descriptions gekürzt (Gate neu), 13 Region-Platzhalter noindex + aus Sitemap, pflegegrad-Stub in Antrag-Ratgeber gefoldet, og:image PNG 1200×630 sitewide + Twitter-Cards, VZ-Zusatzspanne-Refresh 30–50 → 30–80 € auf der monetisierten Hausnotruf-Seite (Quellenstand 04.11.), IndexNow-Integration (Bing/Yandex/Ecosia, HTTP 200), Press-Mailing Oberberg-Nachrichten versendet (KfW-455-B-Story).

## Startblocker Partnerprogramme — Malteser DURCHGEBROCHEN, ADCELL-GO-Pack fertig

- **Malteser (Awin 112616): ZUGELASSEN + 2 Placements LIVE seit 02.11.** — die erste monetarisierte Route. Heute re-verifiziert: beide Tracker-URLs (`awin1.com/cread.php?awinmid=112616&awinaffid=3124891`) mit `data-partner-placement` auf hausnotruf-kosten-anbieter-vergleich, `rel="sponsored"`, Anzeige-Kennzeichnung + Vergütungshinweis. 10 €-CPL-Beratungstermin; das 1-€-Infomaterial-Fenster lief am 31.10. aus (wäre vor der Zusage verfallen — Vorbereitung kam rechtzeitig).
- **Datenschutz nachgezogen:** Partner-Amendment live seit 02.11. (9 Abschnitte, dynamisch aus partner-links.json, Gate F erzwingt Same-Commit-Regel) — Lücke aus der Malteser-Aktivierung war im Vormittags-Commit entstanden und am selben Tag geschlossen.
- **ADCELL-GO-Pack heute fertiggestellt (dieser Lauf):** HIRO Lift 9440 und Pflegehase Hausnotruf 10690 ohne Login frisch re-verifiziert (Evidenz `research/evidence/adcell-refresh-061126/`):
  - HIRO: 50,00 €/Lead, 90 Tage Cookie, Freigabe 56/56 Tage, SEM nur auf Anfrage, incentivierter Traffic nicht erlaubt — identisch zum 28.10.-Scan.
  - Pflegehase: 25,00 €/Lead (Lead = genehmigter Pflegekassen-Antrag), 60 Tage Cookie, Freigabe 28/56 Tage; **neu seit 23.10.: explizite Bedingungstabelle** (SEM/PLA/Cashback/Incentive „erlaubt") — eigener Standard bleibt rein organisch/redaktionell; Programm offen („Nach Ihrer Anmeldung können Sie direkt loslegen").
  - Registrierungsformular verifiziert (Kanal „Webseite (Content, Blog, SEO)", AGB/DSE-Checkbox + Joint-Controller-Checkbox = Betreiber-Akt). Formulareinträge, Bewerbungstexte, Aktivierungs-Pfad (Config + Gates + DSE-Amendment B, Same-Commit) fertig: `operations/ADCELL-GO-PACK.md`.
  - **Wirkung: ein einziger GO öffnet zwei Programme** (Treppenlift-Kerncluster 50 €/Lead + Hausnotruf-Backup 25 €/Lead).
- AFFILIATE-LINK-STATUS.md war veraltet („Malteser offen") — auf 06.11.-Stand korrigiert.

## Messung

- **GA4 aktiv:** consent-gated clientseitig (Web-GTM v5 → G-5738T8FHWW), Empfangsnachweis vom 16.10.-Fix (`/g/collect` 204 + Realtime-Screenshot) weiter gültig. Dormanter Stape-Host produktionsneutral (404, 0 Referenzen).
- **Search Console: nicht verfügbar** — im Cron weiterhin keine autorisierte Google-Sitzung; GSC-Queries/Index-Diagnose warten auf einmalige Nutzer-Session. Keine Null als Messung ausgegeben.

## Leads / Umsätze

- **Nicht nachweisbar.** Malteser-Placements sind seit 02.11. live, aber Lead-Zahlen/Freigaben/Ertrag sind nur im Awin-Login sichtbar (Cron blockiert); kein akzeptierter Lead, kein Zahlungseingang belegt. Keine Erlösprognose.

## Token-/Toolkosten

- **Nicht verfügbar** (kein Verbrauchsmesszugang). Keine Ausgaben, keine Verträge, keine Budgets berührt.

## Einmalig erforderliche Freigaben

1. **GO ADCELL-Registrierung** (inkl. HIRO-Bewerbung + Pflegehase-Join; Joint-Controller-Checkbox = Betreiber-Akt; kostenlos) — Pack: `operations/ADCELL-GO-PACK.md`.
2. **Awin-Login** (einmalige Nutzer-Session oder Vault-Eintrag, geschützter Dialog) — löst: Malteser-Lead-Readback, Lifta-40988-Status, Aroundhome-68536-Absendung.
3. **Keychain-/Session-Freigabe** — Liftstar-Follow-up senden (fällig seit 22.10., Draft 03.11. aktualisiert) + Posteingang prüfen.

## Nächste Priorität

1. ADCELL-GO → beide Programme frei → Treppenlift-Cluster erstmals über HIRO monetarisierbar.
2. Awin-Session → drei Status-Readbacks + Aroundhome-Absendung.
3. Danach Phase 2: GSC-Queries auswerten (sobald Session) und bestehende Seiten verbessern statt neue Cluster.
