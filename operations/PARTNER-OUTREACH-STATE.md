# Status: Partneranfrage Lifta über Awin

## Durchbruch am 15.10.2026 (nachmittags)
- Awin-Konto des Betreibers existiert: tobias.batke@gmail.com, Publisher-ID **3124891**, Name „Zuhausebleiben-Kompass". Passwort wurde vom Betreiber per Reset selbst neu gesetzt; Login läuft über die Browsersitzung. Kein Vault-Eintrag bisher (geschützter Dialog kann nachgeholt werden, nie ein Chat-Passwort).
- Erstmail an koop@liftstar-marketing.de am 15.10. versendet (Himalaya/SMTP; Gesendet-Beleg id 36): Bewerbungskontext, rein organischer Traffic ohne SEM/Brand-Bidding, vier Klärungsfragen (T&C, Pinterest, Leadübernahme, Datenschutz/AVV).
- **Lifta-Bewerbung im Awin-Login ist draußen:** Bewerbungsdialog (Merchant 40988) ausgefüllt — Promotion „Content" mit zuhausebleiben-kompass.de, 975-Zeichen-Nachricht (Zielgruppe, Quellenansatz, kein SEM, Verweis auf die vier Mailfragen), AGB-Checkbox bestätigt, abgesendet. Readback auf der Profilseite: Status **„Bewerbung offen"** (vorher „Nicht beworben").

## Konditionen laut Awin-Profil (15.10. gelesen)
- 50 € pro validem Lead oder 500 € pro Auftrag; Cookie 30 Tage; Autobestätigungszeitraum 60 Tage; Programm online seit 23.01.2023; Risikostufe 2 (Advertiser-Zahlungsverhalten); mobil optimiert; kein Produktfeed.
- SEM/Brand-Bidding verboten (Listing 2023, Kontext); Bewerbung nur auf freigegebenen Werbeplätzen.

## Bad-Cluster-Kandidat: Aroundhome DE (23.10., Cron-Lauf 3)
- **Awin-Advertiser 68536, öffentliches Profil ohne Login gelesen:** Umsatzbeteiligung „im Regelfall 30 %“ (kein Fix-CPL), 30-Tage-Cookie, Lead-Validierung ~8 Tage; Lead-Kriterien: echte/exklusive Kontaktdaten, keine Test-/Auslandsanfragen. Kategoriebeleg erste Partei: aroundhome.de „Badezimmer“ + „Treppenlift“ als „Beliebte Services“, /badezimmer/ = barrierefreier Badumbau mit Angebotsanfrage.
- **Status: noch nicht beworben** — Bewerbung über bestehendes Publisher-Konto 3124891, aber durch denselben Awin-Login-Blocker gestoppt wie die Status-Readbacks von Lifta/Malteser. Einträge in `data/partner-links.json` vorbereitet (approved=false, placements=[] — Renderer inaktiv, Gate 22/22 PASS).
- Verwerfungen: Badumbauheld + Seniovo (beides Fachbetriebs-Netzwerke ohne Publisher-Route). Aroundhomes alternatives Triple-A-Tracking (Artefact/easy.affiliate) nicht genutzt — ein Netzwerk, ein Reporting.
- Vollständig: `research/partner-scan-badumbau-231026.md` (Ledger 24/24 verbatim). Entwurf Erstmail: `operations/aroundhome-enquiry-draft.txt` (nicht gesendet, keychain-blockiert).

## Warteschleifen
1. Programmzusage im Awin-Login („Bewerbung offen" → zugelassen/abgelehnt) UND substanzielle Antwort von Genc Kashtanjeva (koop@liftstar-marketing.de; laut Auto-Antwort ab 22.10.2026 erreichbar, Posteingang id 11232). Beides abwarten; Nachfassen ab 22.10. geplant.
2. Erst nach Zusage: aktuelle T&C im Login lesen, Werbemittel/Links nur aus dem Programm, Leadformular-Weg laut Frage-3-Antwort bauen, Pinterest nur mit Kanalfreigabe. Kein Leadformular, keine Partnerlinks vorher.
3. Awin-Profil ist laut Dashboard-Hinweis unvollständig — Vervollständigung erst mit Betreiber-Rücksprache/Zusage, keine Datenerfindung.
4. Projektpostfach: IMAP/SMTP aktiv (Himalaya, Schlüsselbund); Eingang regelmäßig prüfen. Gesendet-Stempel zeigt 1970 (Server-Anzeigebug, Inhalt korrekt).
5. Stape service.zuhausebleiben-kompass.de: gültiges TLS, /healthy 200; Messkette in Abnahme (MEASUREMENT-HANDOFF.md), GA4-ToS-Freigabe offen.
