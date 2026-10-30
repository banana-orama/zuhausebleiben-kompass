# Affiliate-Link-Status: Warum noch keine Partnerlinks live sind

Stand: 23.10.2026 (Partner-Scan: Rückfalloption dokumentiert, Awin-Fensterdaten öffentlich re-verifiziert)

## Kurze Antwort
Nein — **Awin-Erlaubnis ist pro Programm nötig**. Ein Publisher-Konto allein reicht nicht; jeder Advertiser muss die Bewerbung freigeben, erst dann erzeugt Awin Tracker/Links für uns. Vorzeitige Direktlinks ohne Freigabe würden weder tracken noch vergütet werden und verstoßen gegen Liftas Bedingungen (Historie: nur freigegebene Websites, SEM-Verbot; Verstoß = Ausschluss + Storno).

# Programmstatus (23.10. öffentliche Profile re-verifiziert; Bewerbungsstand: Awin-Login 15./17.10.)
| Advertiser | Netzwerk/ID | Konditionen (öffentlich, 23.10.) | Unser Status | Nächster Schritt |
|---|---|---|---|---|
| Lifta DE | Awin 40988 | 50 €/validem Lead, 500 €/Auftrag, 30 d Cookie (23.10. öffentlich unverändert) | **Bewerbung offen** (15.10.) | Zusage abwarten; Follow-up sendefertig, keychain-blockiert |
| Malteser DE | Awin 112616 | 10 € CPL Vor-Ort-Beratungstermin; **1 € CPL Infomaterial nur bis 31.10.2026** (23.10. öffentlich bestätigt); 30 d Cookie | **Bewerbung offen** (17.10.) | Zusage abwarten; dann Infomaterial-/Beratungstermin-Links in die 2 Hausnotruf-Artikel |
| **Pflegehase Hausnotruf** (Backup, antragsfertig) | **ADCELL 10690** | 25,00 €/Lead (Lead = von der Pflegekasse genehmigter Antrag), 60 d Cookie, Freigabe 28/56 Tage | **Noch nicht beworben** — braucht einmalig ADCELL-Publisher-Registrierung (Joint-Controller-Checkbox = Betreiber-Akt) | Betreiber-GO → Registrierung → Bewerbung → Freigabe → partner-links.json + Gate erweitern |
| **Aroundhome DE** (Bad-Cluster, antragsfertig, 23.10.) | **Awin 68536** | Umsatzbeteiligung „im Regelfall 30 %“ (kein Fix-CPL), 30 d Cookie, Lead-Validierung ~8 Tage; Lead-Kriterien: echte, exklusive Kontaktdaten, keine Test-/Auslandsanfragen (öffentliches Profil 23.10.) | **Noch nicht beworben** — gleicher Awin-Login-Blocker wie oben; Bewerbung läuft über das bestehende Publisher-Konto | Awin-Login (Vault/Sitzung) → Bewerbung 68536 (Promotion „Content“) → Freigabe → Bad-Cluster-Placements in partner-links.json |

Details + Verwerfungen (Libify tot, Treppenlift-Angebotsvergleich ohne Programm, Treppenlift-ME-Modell passt nicht, lifeo Vor-Ort-Modell, Smartversorgt nur via drittem Netzwerk, Acorn DE als unabhängige Treppenlift-Option dokumentiert): `research/partner-scan-231026.md` (Ledger 43/43 verbatim verifiziert). Bad-Cluster-Scan (Aroundhome-Kandidat; Badumbauheld/Seniovo verworfen — Fachbetriebs-Netzwerke ohne Publisher-Route): `research/partner-scan-badumbau-231026.md` (Ledger 24/24 verbatim verifiziert).

## Malteser-Fenster bewusst nutzen
1-€-CPL (Informationsmaterial) läuft nur bis 31.10.2026 — jede Woche Zögerung kostet das billigste Einstiegsprodukt. Hausnotruf-Artikel (2× live, gut gerankt auf Long-Tail) passen 1:1 auf die Infomaterial-/Beratungstermin-URLs.

## Vorbereitung (parallel, ohne Zusage legitim)
- Ratgeber bleiben unverändert echt (keine Link-Platzhalter im Text — Leser täuschen ist tabu).
- **Renderer-Vorbereitung umgesetzt (22.10.):** zentrale `data/partner-links.json` (active=false, alle Partner approved=false, keine URLs) + `partner-cta`-Renderpfad in article-renderer.mjs. Rendert NUR bei active=true UND approved=true UND echter Tracker-URL aus dem zugelassenen Programm; vorher null Marker im Build. Kontradiktionen (URL ohne Zusage, Zusage ohne URL, unbekannte Slugs, doppelte placement_ids) brechen den Build. Gate: `python3 test_partner_links.py` (22 Checks, in `npm test` + CI). Jede Platzierung rendert mit rel="sponsored noopener", target=_blank, Anzeige-Kennzeichnung, Vergütungshinweis, stabiler nicht-personaler placement_id. Aktivierung nach Zusage = eine Config-Änderung + `npm run test:partner` + Deploy.
- Datenschutz: Partnerlink-Klicks sind PII-frei (nur content_id/partner_id/placement_id ins eigene GA4); Tracking des Klicks selbst läuft consent-gated wie alle Events. **Amendment textfertig vorbereitet (30.10., Cron-Lauf 4):** `research/datenschutz-partner-entwurf.md` — Amendment A (§5-Ersatz), B (Netzwerk-Absätze Awin/ADCELL mit Cookie-Details, Speicherfristen, Rollen), C (GA4-Enumeration nur falls Partner-Klick-Messung aktiviert wird) + Aktivierungsregeln (Pro-Programm-Mischung erst bei geschaltetem Link, gleicher Commit wie partner-links.json-Aktivierung). Belegt aus Netzwerk-Eigendokumenten, 14/14 Zitate verbatim (`research/datenschutz-partner-301026-ledger.json`): Awin = eigenständiger Verantwortlicher, Tracking-Domain-Cookies, 3/5 Jahre; ADCELL = gemeinsame Verantwortung Netzwerk+Publisher (Art.-26-Anlage), ADCELLpidX-Cookies, Pflichtangabe. Offener Rechtspunkt (Consent vor ausgehendem Klick) deklariert, nicht entschieden. Live-Text unangetastet, bis ein Link tatsächlich geschaltet ist.

## Zugangsstand (22.10., Cron-Lauf)
- **Awin-Login-Sitzung tot:** ui.awin.com leitet auf die Login-Seite; kein Vault-Eintrag für Awin (nur webgo-Panel). Status-Check beider Bewerbungen (Lifta 40988, Malteser 112616) aus dem Cron nicht möglich — nötig wäre einmalig: Betreiber-Login in einer Nutzer-Session ODER Awin-Login als Vault-Eintrag (geschützter Dialog). Kein Passwort-Raten.
- **Keychain weiterhin im Cron gesperrt** (security exit 36): Liftstar-Follow-up (Draft fertig, Tippfehler bereinigt) weiterhin nicht versendbar aus dem Cron.

## Freigabebedarf
Keiner für die Malteser-Bewerbung selbst (gleiche Kategorie wie die bereits freigegebene Lifta-Bewerbung: sachliche Content-Plattform, kein SEM). Absenden jetzt, Zusage abwarten, dann Links bauen.
