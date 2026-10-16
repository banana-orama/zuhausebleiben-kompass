# Launch-State: ZuhauseBleiben Kompass

Aktualisiert: 2026-10-16 (Lauf 2: Related/CTA-Cluster-Fix + Footer-Wahrheit) · Verifizierte Tatsachen mit Datum; Offenes markiert.

## Phase-Übersicht

| Block | Stand | Nächste Einheit |
|---|---|---|
| Indexierung | **Launch öffentlich verifiziert (15.10., Nachmittag):** `https://zuhausebleiben-kompass.de/` robots=`index,follow`, HTTP 200 (server: GitHub.com), öffentliche Sitemap mit 23 URLs ohne Entwurf, Datenschutz indexierbar, Beispielartikel 200. robots.txt enthält jetzt die Sitemap-Direktive (Generator-Fix, Deploy folgt). | GSC-Sitemap-Einreichung blockiert: kein gcloud-Auth-Token mit Search-Console-Scope — einmaliger Nutzer-Login nötig; alternativ Discovery über robots.txt-Sitemap-Direktive (jetzt vorhanden). |
| DNS/Hosting | Gelöst: Apex/WWW auf GitHub Pages, HTTP 200, Mail-DNS unangetastet. | Keine Aktion. |
| Partnerannahme (P1) | **Erstmail an koop@liftstar-marketing.de gesendet (15.10., Beleg im Gesendet-Ordner des Projektpostfachs, id 36):** vier Klärungsfragen (T&C, Pinterest, Leadübernahme, Datenschutz/AVV). **Auto-Antwort (15.10., 10:55 UTC, INBOX id 11232):** Genc Kashtanjeva (Liftstar) ab 22.10.2026 wieder erreichbar — substanzielle Antwort frühestens dann. Awin-Registrierung noch offen: Konto existiert nicht; erster Passwort-Speicherdialog abgelehnt, Registrierung braucht einmalig geschützten Dialog. | Postfach beobachten; ab 22.10. nachfassen, falls nichts kommt. Danach Awin-Registrierung + Programm-Bewerbung. |
| Lead-Datenannahmeweg (P2) | Unverändert: keine Formulare; Frage 3 der Erstmail klärt Weg. | Nach Liftstar-Antwort. |
| Datenschutz | Launch-Text live (8 Abschnitte, CMP/zbk_consent dokumentiert, Hosting/E-Mail/Rechte/keine Gesundheitsdaten). Offen: endgültige E-Mail-Löschfrist, lit. f vs. lit. b bei späterer Vermittlung — markiert, keine Rechtsfreigabe-Imitation. | Frist mit erster echter Anfrage festlegen. |
| Messung | **GA4-Empfang blockiert (16.10., Lauf 3):** Site-Kette live verifiziert (Consent rev 2 → genau 1 GTM-Loader → vollständiger `zbk_measurement`-Push), aber die publizierten GA4-Tags (G-5738T8FHWW) feuern nie — Tag-Assistant: „No tags were evaluated in this container"; GA4-Property 559120219: 0 Events. Diagnose + nächste Schritte: GA4-RECEIPT-INCIDENT-2026-10-16.md. Cookiebanner/Consent selbst unverändert korrekt. | Tag-Level-UI-Readback (Consent-Prüfung am Tag), dann All-Pages-Kontrolltag im Preview; ggf. Trigger-Neu-Publish als Version 3. Kein Publish ohne erneute Probe-Kette. |

## Verifizierte Befunde (Abrufdaten)

- 2026-10-15: Projektmailbox anfragen@zuhausebleiben-kompass.de via Himalaya IMAP/SMTP verifiziert (Testmail round-trip; Passwort nur im macOS-Schlüsselbund, Konfiguration ~/.hermes/profiles/milo/himalaya/zuhausebleiben.toml).
- 2026-10-15: Lifta-Erstmail versendet (SMTP-Beleg Gesendet id 36). Sendeadressvermögen damit belegt; keine Zusage, keine Konditionen bestätigt.
- 2026-10-15: Launch-Build lokal geprüft: 25 HTML index,follow; Entwurf noindex; Sitemap 23 <loc> ohne Entwurf/Datenschutz; Consent 13/13 Playwright PASS.
- 2026-10-15: service.zuhausebleiben-kompass.de TLS gültig, /healthy HTTP 200 (CNAME euh.stape.net von Nutzer angelegt).
- 2026-10-15: Launch öffentlich verifiziert: Homepage robots=index,follow, HTTP 200 (server: GitHub.com), öffentliche Sitemap 23 URLs ohne Entwurf, Datenschutz indexierbar, /treppenlift-kosten.html HTTP 200. Damit Readback noindex→index abgeschlossen.
- 2026-10-15: robots.txt hatte keine Sitemap-Direktive (Google musste Sitemap selbst entdecken) — Generator-Fix in generate.mjs (Zeile robots.txt), beide Build-Modi geprüft (PREVIEW: Sitemap-Direktive ja, Sitemap leer; LAUNCH: 23 URLs). test_site LAUNCH+PREVIEW PASS. Deploy folgt.
- 2026-10-16 (Lauf 2): Öffentliche Sitemap erneut verifiziert: 33 <loc>-URLs (16 Ratgeber inkl. Batch 3, Regionen, Rechtseiten; Draft nicht enthalten); Homepage index,follow. Zähl-Artefakt (grep -c zählt Zeilen, nicht Vorkommen) korrigiert — keine Regression gewesen.
- 2026-10-16 (Lauf 2): Parent-Acceptance Batch 3 nachgeholt: Alle tragenden Rechtzahlen der 4 neuen Artikel gegen heute abgerufene Originale bestätigt — §40 SGB XI (42 €/Monat Verbrauchsmaterial, 10 % max. 25 € Zuzahlung), §41 (721 € PG2 … 2 085 € PG5 Gesamtwert), §42a (3 539 € Gemeinsamer Jahresbetrag), §39 (Ersatzpflege längstens 8 Wochen), §15 (Pflegegrad-Schwellen 12,5/27/90-100 Punkte), §84 SGG (Widerspruch binnen eines Monats). Hinweise: gesetze-im-internet liefert ISO-8859-1 + HTML-Entities (&#228;), Tausendergruppen mit geschütztem Leerzeichen — naive Stringsuche meldet fälschlich "nicht gefunden".
- 2026-10-16 (Lauf 2): Renderer-Kontextfehler behoben (article-renderer.mjs): „Passend dazu" und Early-CTA „Anbieter prüfen" schickten 9 von 16 Artikeln (Hausnotruf×2, Pflegegrad×2, Hilfsmittel, Rollator, Verhinderungspflege, Türen, Beleuchtung) ausschließlich in den Treppenlift-Trichter. Neu: Cluster-Logik (bad/care/lift), Pflege-Cluster miteinander verlinkt, kontextpassende CTA-Ziele (z. B. Hausnotruf → Pflegegrad-Antrag vorbereiten; Rollator → Hilfsmittel-Kostenübernahme), Bad/ Treppenlift-Verhalten unverändert. Beide Build-Modi geprüft (PREVIEW: Draft noindex, Sitemap leer; LAUNCH: 32 Sitemap-URLs), test_site LAUNCH + test_articles PASS.
- 2026-10-16 (Lauf 2): Footer-Unwahrheit beseitigt (generate.mjs layout()): „Dieser Internetauftritt ist eine Vorschau. Datenschutzinformationen … noch nicht eingerichtet." stimmte seit Launch nicht mehr; jetzt „befindet sich im weiteren Aufbau; Angebotsvermittlung noch nicht eingerichtet" mit direktem Datenschutz-Link. Vermittlung bleibt korrekt als nicht verfügbar beschrieben.
- 2026-10-15: Liftstar-Autoantwort (INBOX id 11232, 10:55 UTC): Kontakt ab 22.10.2026 wieder erreichbar. Keine substanzielle Antwort, keine Konditionsänderung.
- 2026-10-16 (Lauf 3): Website/DNS live verifiziert: Homepage HTTP 200, robots=index,follow, robots.txt mit Sitemap-Direktive, öffentliche Sitemap 32 <loc> (16 Ratgeber, Regionen, Rechtseiten), /treppenlift-mietwohnung.html 200, service.-Host /healthy 200. Postfach: weiterhin nur 2 Mails (keine Liftstar-Antwort vor 22.10.).
- 2026-10-16 (Lauf 3): GA4-Empfangsnachweis negativ: Consent-Annahme/-Widerruf/-Annahme live getestet (Cookie rev 2 korrekt), Loader 1×, Push vollständig (internes Datenmodell verifiziert), aber kein gtag/collect-Request in 4 Seitenkontexten (Live×2, lokale Mirror-Proben ×2, Boolean+String, cache-gebustet); Tag-Assistant-Preview: „No tags were evaluated in this container"; GA4: 0 Events. Volle Evidenz + Hypothesen: GA4-RECEIPT-INCIDENT-2026-10-16.md.
- 2026-10-16 (Lauf 3): Search Console autorisiert gelesen: 0 Clicks, Indexierung „Processing data, please check again in a day or so", keine Experience-/Enhancement-Daten — Zahlen zu jung für Aussagen.
- 2026-10-16 (Lauf 3): Awin-Login-Sitzung abgelaufen (Sign-in-Seite); letzter dokumentierter Stand Bewerbung 40988 = „offen" (15.10.). Kein Vault-Eintrag für Awin; kein neuer Status ohne Login behauptet.
- 2026-10-14: Lifta-Konditionen offiziell 50 €/validem Lead bzw. 500 €/Auftrag, 30-Tage-Cookie (ui.awin.com Profil 40988); SEM/Brand-Bidding verboten (Listing 2023 als Kontext).

## Betriebsregeln (aktuell)

- Launch-Build nur mit `--index`; Preview-Build ohne Flag bleibt noindex. Tests erzwingen beide Modi korrekt.
- Keine Partnerlinks/Formulare vor Liftstar-Antwort; Pinterest nur nach Kanalfreigabe.
- Keine 40–60-€-Zahlen mehr als aktuell — Referenz ist das Awin-Profil (50/500 €).
- Keine Gesundheitsdaten, keine PII in Messung; Consent-Revision bump vor jeder Aktivierung neuer Tracker.
- Vor jedem Commit fremde WIP-Dateien prüfen; nur eigene Artefakte stagen.
