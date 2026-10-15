# Cookiebanner / Consent — lokale Implementierung

## Status und Abgrenzung
- Selbst gehostetes **vanilla-cookieconsent 3.1.0**, per `npm view vanilla-cookieconsent version` tatsächlich ermittelt, exakt in package.json und package-lock.json fixiert; MIT-Lizenz wird mit ausgeliefert. `npm audit`: 0 bekannte Schwachstellen. Das ist keine unabhängige Sicherheitsprüfung oder Rechtsfreigabe.
- Auf allen 25 generierten HTML-Seiten eingebunden. Keine Veröffentlichung, kein Commit/Staging/Push durch diese Implementierung. Bestehende noindex-/Lead-Sperren bleiben erhalten.
- **Keine GTM-/GA4-/Stape-Loader, keine externe CMP, keine Cookieless-Pings.** Eine Zustimmung startet derzeit ausdrücklich noch keine Messung. Web GTM-M9TZZPLQ und Server GTM-M6SDZCN4 bleiben für die Website inaktiv. Serverbereitstellung nicht Teil dieses Arbeitspakets.

## Bedienung und Speicherung
- Deutsche Sie-Ansprache; gleich gestaltete Annehmen/Ablehnen-Schaltflächen (gleiche Farben, Mindesthöhe 48 px), Einstellungen auf erster Ebene. Ratgeber ohne Entscheidung weiter nutzbar.
- Footer: `Datenschutzeinstellungen` und sofortiger `Einwilligung widerrufen` mit Statusrückmeldung. Auswahl speichern, wieder öffnen, ändern und Widerruf getestet.
- Nur notwendiges First-Party-Cookie `zbk_consent`, erstmals nach Auswahl, 180 Tage, Pfad `/`, SameSite=Lax, Secure auf HTTPS, kein localStorage. Enthält Kategorien, Revisionsstand, zufällige Consent-ID und Zeitpunkte. Keine externe CMP-Übertragung/Consent-Datenbank; Cookie wird bei Requests technisch an den statischen Host mitgesendet.
- Opt-in, Revision 1; beschädigte oder veraltete Einwilligung führt zu denied und erneuter Auswahl. Analytics-Cookies `_ga*`, `_gid`, `_gat*` werden bei späterem Abwählen automatisch bereinigt; aktuell legt kein Messdienst sie an. Künftige echte Cookie-Namen/Domains erneut prüfen.
- Datenschutzgenerator korrigiert: keine falsche Behauptung „setzt keine Cookies ein“; CMP-Speicherung, Laufzeit, Zwecke, Widerruf und noch deaktivierte Messdienste erklärt. Datenschutzerklärung bleibt rechtlich ungeprüfter Entwurf.

## Vertrag für spätere GTM-/sGTM-Anbindung
`consent-default.js` wird synchron inline im Head vor dem lokalen CMP-Modul ausgegeben. Consent Mode `default` ist zunächst bei allen vier Feldern `denied`, ohne Netzwerkrequest:

```js
window.zbkConsent.state // eingefrorener Snapshot
// {analytics_storage, ad_storage, ad_user_data, ad_personalization}
window.zbkConsent.analyticsAllowed // boolean, standardmäßig false
```

Mapping: nur die individuelle Kategorie `analytics` darf `analytics_storage` auf `granted` setzen. `ad_storage`, `ad_user_data`, `ad_personalization` bleiben **auch bei „Alle akzeptieren“ denied**; es gibt keine Marketing-Kategorie. Auch notwendige Speicherung lädt keine Google-Sicherheitsbibliotheken.

Reihenfolge bei erster Auswahl, wiederhergestellter gültiger Auswahl und Änderung:
1. Browser-Snapshot aktualisieren.
2. `gtag('consent', 'update', snapshot)` in lokale dataLayer.
3. Custom Event `{event:'zbk_consent_update', consent_version:1, consent:snapshot}` in dataLayer.
4. DOM-Event `zbk:consent` mit demselben Snapshot.

Später im Webcontainer den Eventnamen `zbk_consent_update` sowie `consent.analytics_storage` usw. als Data-Layer-Variablen nutzen. Erst **nach** realer Aktivierungsfreigabe einen idempotenten Loader hinzufügen, der den aktuellen Snapshot **und** zukünftige Änderungen berücksichtigt und ausschließlich nach Analytics-Opt-in lädt. Nicht auf einer All-Pages-Regel oder nur auf dem Consent-Mode-Standardverhalten aufbauen: keine Advanced-Mode-Pings bei Ablehnung. Google-Tag-/sGTM-Requests müssen consentabhängig sein; Marketing bleibt gesperrt. Bei Widerruf alle zukünftigen Messereignisse unterbinden, tatsächliche Cookies bereinigen und ggf. Bibliotheken entladen/Seite sicher neu laden. Consent wird nicht dadurch serverseitig empfangen, dass es in der lokalen dataLayer steht: der spätere Google-Tag muss die korrekten Signale an den echten sGTM-Endpunkt übertragen, im Server-Preview und per Netzwerkprüfung nachweisen. First-Party-Transport ist kein Consent-Ersatz.

**Vor echter Aktivierung erforderlich:** konkrete GA4-/Stape-Ziele und Anbieter/Verarbeitungen/Speicherfristen dokumentieren, Datenschutzhinweise und Bannertexte aktualisieren, CMP-Revision erhöhen (erneute Zustimmung statt Verwertung der Vorschau-Auswahl), tatsächlichen Loader samt Widerruf testen, GTM-/sGTM-Empfang und denied-Netzwerk erneut verifizieren. Keine Aussage, dass GTM/sGTM bereits Consent empfangen.

## Dateien / Build
- `consent-default.js`, `consent.mjs`: Bootstrap und reale CMP-Konfiguration.
- `generate.mjs`: Einbindung, Footer, Datenschutzhinweise, lokale Bibliothekskopie einschließlich Lizenz.
- `design.css`: CMP-Design, gleiche Auswahlbuttons, Footer-Steuerelemente, Druckausblendung.
- `package.json`, `package-lock.json`: exakte Bibliothek und Playwright-Devdependency; `npm test` als vollständiger Check.
- `playwright.config.mjs`, `tests/consent.spec.mjs`, `.gitignore`: reproduzierbare Tests; lokale Testartefakte ignoriert.
- `dist/`: 25 neu generierte HTML-Dateien; `dist/assets/consent.mjs`, `dist/assets/vendor/{cookieconsent.esm.js,cookieconsent.css,cookieconsent-LICENSE.txt}`.
- `article-renderer.mjs` und `cta.css` nicht verändert; bereits vorhandene parallele Änderungen nicht zurückgesetzt.

## Verifikation
```sh
npm ci
npx playwright install chromium  # einmalige Testbrowser-Installation
npm test
npm audit
git diff --check
```

Ausgeführt: Build meldet 28 Dateien/Seiten insgesamt; `python3 test_site.py`: **25 HTML-Seiten** mit Links, Einzel-H1, ohne Formulare, noindex, XML bestanden. `python3 test_articles.py`: **7 Artikel** einschließlich Assets/Abmessungen, Quellen-/TOC-Ankern, JSON-LD und SVG bestanden. Playwright/Chromium: **10 Tests bestanden**:
1. Einbindung/early denied/kein Trackingloader auf allen generierten HTML-Seiten.
2. Erstbesuch denied, gleichwertige sichtbare Auswahl, noch kein Cookie, keine Drittanbieterrequests.
3. Ablehnung über Seitenwechsel und Reload gespeichert, keine Drittanbieterrequests.
4. Zustimmung nur Analytics, korrekt geordnete Events, Reload und persistenter Widerruf; auch nach Zustimmung noch keine Drittanbieterrequests.
5. Individuelle Auswahl, Tastatur-Space, Escape, Fokusrückgabe, erneutes Abwählen.
6. Beschädigte und alte Revision fail closed.
7. CMP-Skript blockiert: denied, Inhalt nutzbar, kein Tracking.
8. HTTPS Secure-/SameSite-Cookie, kein localStorage, aktualisierter Datenschutztext.
9. JavaScript deaktiviert: Inhalt/Noscript verfügbar, keine Cookies/Trackingrequests.
10. Mobile 375×812: Auswahlknöpfe im Viewport, Mindesthöhe, Einstellungen/Speichern sichtbar, kein horizontaler Überlauf.

Für Netzwerktests werden nur bestehende absolute First-Party-URLs auf den lokalen Build geroutet; fremde Domains werden beobachtet, nicht verdeckt blockiert. Screenshots: lokale ignorierte `test-results/consent-mobile-{banner,settings}.png`. Keine Aussage über andere Browser oder tatsächliche zukünftige Messrequests.
