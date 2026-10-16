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
- Interne Renderer-Vorbereitung: eine zentrale `partner-link`-Map im Renderer, die erst bei Zusage per Konfiguration aktiviert wird. Vorher rendert sie NICHTS (kein sichtbarer Platzhalter).
- Datenschutz: Partnerlink-Klicks sind PII-frei (nur content_id/partner_id/placement_id ins eigene GA4); Tracking des Klicks selbst läuft consent-gated wie alle Events. DSGVO-Absatz „Keine Weitergabe" wird bei erstmaliger Partnerlink-Schaltung präzisiert (Klick = Weiterleitung zum Advertiser mit Awin-ClickRef).

## Freigabebedarf
Keiner für die Malteser-Bewerbung selbst (gleiche Kategorie wie die bereits freigegebene Lifta-Bewerbung: sachliche Content-Plattform, kein SEM). Absenden jetzt, Zusage abwarten, dann Links bauen.
