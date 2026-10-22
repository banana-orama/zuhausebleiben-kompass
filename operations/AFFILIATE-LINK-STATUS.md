# Affiliate-Link-Status: Warum noch keine Partnerlinks live sind

Stand: 17.10.2026 (nach Betreiber-Frage „können wir nicht schon rauslinken?")

## Kurze Antwort
Nein — **Awin-Erlaubnis ist pro Programm nötig**. Ein Publisher-Konto allein reicht nicht; jeder Advertiser muss die Bewerbung freigeben, erst dann erzeugt Awin Tracker/Links für uns. Vorzeitige Direktlinks ohne Freigabe würden weder tracken noch vergütet werden und verstoßen gegen Liftas Bedingungen (Historie: nur freigegebene Websites, SEM-Verbot; Verstoß = Ausschluss + Storno).

# Programmstatus (17.10. gelesen)
| Advertiser | Awin-ID | Konditionen (öffentliches Profil) | Unser Status | Nächster Schritt |
|---|---|---|---|---|
| Lifta DE | 40988 | 50 €/validem Lead, 500 €/Auftrag, 30 d Cookie | **Bewerbung offen** (15.10.) | Zusage abwarten; Nachfassen 22.10. |
| Malteser DE | 112616 | 10 € CPL Vor-Ort-Beratungstermin; **1 € CPL Infomaterial nur bis 31.10.2026**; 30 d Cookie | **Bewerbung offen** (17.10. abgesendet, Promotion=Content, 923-Zeichen-Nachricht, AGB bestätigt; Readback „Bewerbung offen") | Zusage abwarten; dann Infomaterial-/Beratungstermin-Links in die 2 Hausnotruf-Artikel |

## Malteser-Fenster bewusst nutzen
1-€-CPL (Informationsmaterial) läuft nur bis 31.10.2026 — jede Woche Zögerung kostet das billigste Einstiegsprodukt. Hausnotruf-Artikel (2× live, gut gerankt auf Long-Tail) passen 1:1 auf die Infomaterial-/Beratungstermin-URLs.

## Vorbereitung (parallel, ohne Zusage legitim)
- Ratgeber bleiben unverändert echt (keine Link-Platzhalter im Text — Leser täuschen ist tabu).
- **Renderer-Vorbereitung umgesetzt (22.10.):** zentrale `data/partner-links.json` (active=false, alle Partner approved=false, keine URLs) + `partner-cta`-Renderpfad in article-renderer.mjs. Rendert NUR bei active=true UND approved=true UND echter Tracker-URL aus dem zugelassenen Programm; vorher null Marker im Build. Kontradiktionen (URL ohne Zusage, Zusage ohne URL, unbekannte Slugs, doppelte placement_ids) brechen den Build. Gate: `python3 test_partner_links.py` (22 Checks, in `npm test` + CI). Jede Platzierung rendert mit rel="sponsored noopener", target=_blank, Anzeige-Kennzeichnung, Vergütungshinweis, stabiler nicht-personaler placement_id. Aktivierung nach Zusage = eine Config-Änderung + `npm run test:partner` + Deploy.
- Datenschutz: Partnerlink-Klicks sind PII-frei (nur content_id/partner_id/placement_id ins eigene GA4); Tracking des Klicks selbst läuft consent-gated wie alle Events. DSGVO-Absatz „Keine Weitergabe" wird bei erstmaliger Partnerlink-Schaltung präzisiert (Klick = Weiterleitung zum Advertiser mit Awin-ClickRef).

## Zugangsstand (22.10., Cron-Lauf)
- **Awin-Login-Sitzung tot:** ui.awin.com leitet auf die Login-Seite; kein Vault-Eintrag für Awin (nur webgo-Panel). Status-Check beider Bewerbungen (Lifta 40988, Malteser 112616) aus dem Cron nicht möglich — nötig wäre einmalig: Betreiber-Login in einer Nutzer-Session ODER Awin-Login als Vault-Eintrag (geschützter Dialog). Kein Passwort-Raten.
- **Keychain weiterhin im Cron gesperrt** (security exit 36): Liftstar-Follow-up (Draft fertig, Tippfehler bereinigt) weiterhin nicht versendbar aus dem Cron.

## Freigabebedarf
Keiner für die Malteser-Bewerbung selbst (gleiche Kategorie wie die bereits freigegebene Lifta-Bewerbung: sachliche Content-Plattform, kein SEM). Absenden jetzt, Zusage abwarten, dann Links bauen.
