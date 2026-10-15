# Launch-State: ZuhauseBleiben Kompass

Aktualisiert: 2026-10-15 (Launch-Freigabe durch Betreiber: „Du bestimmst das wann go ist“) · Verifizierte Tatsachen mit Datum; Offenes markiert.

## Phase-Übersicht

| Block | Stand | Nächste Einheit |
|---|---|---|
| Indexierung | **GO erteilt (autonom):** Launch-Build `node generate.mjs --index` geprüft: 25 HTML-Seiten index,follow; Entwurf Angebotsvergleich bleibt noindex und außen vor (Sitemap 23 URLs ohne Entwurf/Datenschutz). test_site LAUNCH-PASS, test_articles PASS, 13 Consent-Playwright-Tests PASS. Deploy-Workflow baut jetzt mit `build:launch`. | Nach Deploy: öffentliche Readback-Prüfung noindex→index, dann GSC-Sitemap-Einreichung (Zugriff besteht). |
| DNS/Hosting | Gelöst: Apex/WWW auf GitHub Pages, HTTP 200, Mail-DNS unangetastet. | Keine Aktion. |
| Partnerannahme (P1) | **Erstmail an koop@liftstar-marketing.de gesendet (15.10., Beleg im Gesendet-Ordner des Projektpostfachs, id 36):** vier Klärungsfragen (T&C, Pinterest, Leadübernahme, Datenschutz/AVV). Awin-Registrierung noch offen: Konto existiert nicht; erster Passwort-Speicherdialog abgelehnt, Registrierung braucht einmalig geschützten Dialog. | Antwort abwarten (Postfach via Himalaya); danach Awin-Registrierung + Programm-Bewerbung. |
| Lead-Datenannahmeweg (P2) | Unverändert: keine Formulare; Frage 3 der Erstmail klärt Weg. | Nach Liftstar-Antwort. |
| Datenschutz | Launch-Text live (8 Abschnitte, CMP/zbk_consent dokumentiert, Hosting/E-Mail/Rechte/keine Gesundheitsdaten). Offen: endgültige E-Mail-Löschfrist, lit. f vs. lit. b bei späterer Vermittlung — markiert, keine Rechtsfreigabe-Imitation. | Frist mit erster echter Anfrage festlegen. |
| Messung | Cookiebanner live (13 automatisierte Tests: Default denied, nur analytics_storage bei Zustimmung, Widerruf, keine externen Aufrufe). Stape-Container jsyqolvb (Free, EU-NL), Custom-Domain service.zuhausebleiben-kompass.de mit gültigem TLS + /healthy 200. GA4/GTM-Kette im Hintergrund in Abnahme (deleg_9ee5c742). | Ende-zu-Ende-Abnahme; erst danach productive Loader freischalten (neue Consent-Revision). |

## Verifizierte Befunde (Abrufdaten)

- 2026-10-15: Projektmailbox anfragen@zuhausebleiben-kompass.de via Himalaya IMAP/SMTP verifiziert (Testmail round-trip; Passwort nur im macOS-Schlüsselbund, Konfiguration ~/.hermes/profiles/milo/himalaya/zuhausebleiben.toml).
- 2026-10-15: Lifta-Erstmail versendet (SMTP-Beleg Gesendet id 36). Sendeadressvermögen damit belegt; keine Zusage, keine Konditionen bestätigt.
- 2026-10-15: Launch-Build lokal geprüft: 25 HTML index,follow; Entwurf noindex; Sitemap 23 <loc> ohne Entwurf/Datenschutz; Consent 13/13 Playwright PASS.
- 2026-10-15: service.zuhausebleiben-kompass.de TLS gültig, /healthy HTTP 200 (CNAME euh.stape.net von Nutzer angelegt).
- 2026-10-14: Lifta-Konditionen offiziell 50 €/validem Lead bzw. 500 €/Auftrag, 30-Tage-Cookie (ui.awin.com Profil 40988); SEM/Brand-Bidding verboten (Listing 2023 als Kontext).

## Betriebsregeln (aktuell)

- Launch-Build nur mit `--index`; Preview-Build ohne Flag bleibt noindex. Tests erzwingen beide Modi korrekt.
- Keine Partnerlinks/Formulare vor Liftstar-Antwort; Pinterest nur nach Kanalfreigabe.
- Keine 40–60-€-Zahlen mehr als aktuell — Referenz ist das Awin-Profil (50/500 €).
- Keine Gesundheitsdaten, keine PII in Messung; Consent-Revision bump vor jeder Aktivierung neuer Tracker.
- Vor jedem Commit fremde WIP-Dateien prüfen; nur eigene Artefakte stagen.
