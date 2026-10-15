# Tracking-Abnahmevertrag: sGTM über Stape

## Betreiberentscheidung
Tobias hat sGTM über Stape als gewünschte Architektur benannt und bietet die gemeinsame einmalige Einrichtung an. Die Vorbereitung von Awin-Publisherregistrierung und Versand einer sachlichen Partneranfrage sind freigegeben. Keine Gebühren-/AGB-Freigabe, keine Aktivierung nicht beschriebener Tracker.

## Zielarchitektur
Webseite -> Consent Management -> Web-GTM/eng begrenzte Eventschicht -> eigene Tracking-Subdomain -> sGTM auf Stape -> ausdrücklich freigegebene Ziele.

Separate Vergütungskette: Besucher -> gekennzeichneter Awin-Link -> Advertiser-Formular -> Advertiser/Awin-Attribution -> Publisherreport. Unser sGTM beweist ausgehende Interaktionen, nicht den späteren gültigen Lead. Awin-ClickRef für Artikel/Kanal ohne personenbezogene Werte; keine künstlich selbst erzeugten Conversions.

## Einmalige technische Inputs
- Stape-Konto und freigegebener Tarif/Region; kein kostenpflichtiger Abschluss ohne Budget.
- Web-GTM-Container-ID und Server-GTM-Containerzugriff für Umsetzung/Debug, bevorzugt minimal erforderliche Rechte.
- Stape-sGTM-Endpunkt und die vom Konto generierten DNS-Werte für die Custom Domain; keine DNS-Werte raten. Gewünschter Host service.zuhausebleiben-kompass.de, noch nicht angelegt.
- Entscheidung über CMP und vorgesehene Messziele (zum Beispiel GA4); Providerliste/Regionen/AVV-Konstellation prüfen. Nicht automatisch GA4 oder Awin-Tags installieren.
- Später Publisher-ID und freigegebene Partnerlinks. Kein Geheimnis in Git, Screenshots oder Chat veröffentlichen.

## Lean-Consent- und Datengrenzen
- Zunächst Basic-Verhalten: keine Analyse-/Marketingereignisse vor entsprechender Einwilligung; auch keine vermeintlich anonymen cookieless Pings auf Verdacht.
- Consent Mode ist ein technischer Signalweg, keine Einwilligungsquelle und keine rechtliche Freigabe.
- Keine Diagnose, Pflegegrade, Kontaktformulardaten, Telefon/E-Mail oder Angehörigendaten an GTM, Stape, GA4, Awin oder Ads. Keine vollständigen URL-Querystrings/Referrer weiterreichen.
- Randomisierte Event-ID nur nach zulässiger Messung; keine serverseitige Entschlüsselung oder Umgehung von Trackingverweigerung. IP-/UA-Weitergabe und Logs auf Endpunktebene gesondert prüfen/minimieren.
- Awin-Conversionnachweise aus Partnerreports mit aggregierten Messwerten abgleichen; keine doppelte Abrechnung via Lead-ID/AWC.

## Initiale Events
page_view: content_id, channel (nur freigegebene Kategorien)
guide_interaction: content_id, action_id (checklist_print / source_open)
partner_click: content_id, partner_id (lifta), placement_id
lead_received / lead_accepted / commission_paid: später ausschließlich serverseitig aus verifiziertem Backend oder Partnerreport, nicht durch Webseitenklick behaupten.

## Abnahmetests vor Aktivierung
1. Default denied: Netzwerkrequests, Cookies und Storage prüfen; keine unerlaubte Messung.
2. Analytics ja / Marketing nein: nur erlaubte Messzwecke; keine Awin-/Ads-Aktivierung durch Analytics-Consent.
3. Entsprechende Zustimmung: genau ein Event, korrektes content_id/placement_id, transport über konfigurierte Subdomain.
4. Ablehnen und Widerruf: weitere optionale Erfassung stoppt; separate Partnernavigation und deren Regeln verständlich kommunizieren.
5. Keine PII: Test mit Beispiel-Kontakt-/Querywerten muss zeigen, dass sie den Messendpunkt nicht erreichen.
6. Partnerclick versus Lead: Reporting weist beides getrennt aus. Echte Partner-Testconversion nur nach zulässigem Testverfahren.
7. Mobile und Content-Security/Adblock-Fälle, Offline-/Fehlerverhalten; Trackingausfall blockiert keine Ratgeber-Navigation.
8. Datenschutz-/Cookiehinweise vor Veröffentlichung auf die tatsächlich getesteten Technologien anpassen. Aktuelle 'kein Tracking'-Aussage bleibt wahr, solange keine Eventschicht eingebunden ist.

## Stand dieses Schritts
Noch keine Stape-Ressource gebucht, kein Tag installiert, kein Datenversand aktiviert. Awin-Registrierungsweg für Merchant 40988 geöffnet; Account-Passwortdialog nicht bestätigt, deshalb noch kein Konto erzeugt. Projektadresse ist bisher Weiterleitung, kein bestätigter SMTP-Sendezugang. Existierender anderer Outreach-Sender wird nicht ohne passende Absenderentscheidung verwendet.

## Originaldokumentation
- https://stape.io/blog/consent-mode-server-google-tag-manager
- https://stape.io/blog/how-to-add-a-custom-domain-to-the-google-tag-manager-server-container
- https://help.awin.com/developers/docs/click-appends-dyn-params
- https://help.awin.com/developers/docs/direct-s2s
