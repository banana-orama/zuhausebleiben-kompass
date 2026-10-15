# Stape Provisionierungsstand

## Tatsächlich eingerichtet und zurückgelesen
- Eigenständiger Container ZuhauseBleiben Kompass im bestehenden Stape-Konto, keine andere Website wiederverwendet.
- Stape-ID jsyqolvb, Dashboard https://app.eu.stape.io/container/jsyqolvb/show
- Server-GTM GTM-M6SDZCN4 (accounts/572865630/containers/267197767), Default Workspace 2.
- Region EU North (Netherlands).
- Tarif Free, 10.000 Requests/Monat, 0 EUR/Monat laut Accountoberfläche. Keine kostenpflichtige Tarifbestätigung ausgeführt. Nicht in automatisch geöffnetem Upgrade-Dialog 'Continue with Pro plan' klicken! Dessen Vorauswahl ist kein bereits aktivierter Pro-Tarif.
- Status Running im Account; GET https://jsyqolvb.euh.stape.net/healthy antwortet öffentlich HTTP 200.
- Standard-GA4-Client im Serverworkspace vorhanden (gaaw_client, clientId 1).
- Keine GA4-Forwarding-Tags erstellt oder veröffentlicht; health 200 beweist noch keinen Ende-zu-Ende-Consent-/Messpfad.

## Gespeicherte Custom Domain: noch nicht produktiv
- service.zuhausebleiben-kompass.de im Stape-Container angelegt, Readback Status Verifying.
- Tatsächlich von Stape ausgegebener DNS-Eintrag (nicht aus Containerhostname abgeleitet):
  - Typ CNAME
  - Host service.zuhausebleiben-kompass.de (bei webgo relativ: service)
  - Ziel euh.stape.net
  - CDN disabled, kein DNS-Proxy, TTL unverändert/default.
- DNS-Eintrag wurde noch NICHT bei webgo gespeichert; HTTPS/Custom-Domain-Abnahme fehlt. Keine Apex/www/MX/TXT-Änderungen notwendig.

## Rest bis tatsächlicher Messung
CMP läuft in separater Implementierung. GTM zunächst nicht auf Seite eingebunden. Nach CMP-Abnahme Web-GTM/DLV/Trigger passend zu realer Eventstruktur konfigurieren. GA4-Projektproperty/Webstream prüfen/anlegen, anonymisierte Eventschicht, Transport durch den tatsächlich bestätigten Stape-Endpunkt, serverseitiger Consent-Gate auch bei manipulierten Requests. Keine PII, Querystrings, Rohreferrer oder Gesundheitsdaten. Vor Produktivstart echten Zustimmung/Ablehnung/Widerruf-Pfad in Web- und Serverpreview prüfen. Consent Mode allein ist keine CMP und Servertransport allein kein Nachweis erhaltener Einwilligung.
