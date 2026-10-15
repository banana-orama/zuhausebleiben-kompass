# Verifizierter Zugangs-/Trackingstand

## Google
- Google Tag Manager CLI `gtm` ist authentifiziert und kann Container lesen und erstellen.
- Explizites erlaubtes Ziel: Account Eigene Websites, accountId 572865630. Andere Kundenaccounts nicht bearbeiten. Globaler CLI-Kontext kann auf einen fremden Workspace zeigen: immer Account/Container/Workspace explizit angeben, keinen fremden Default-Kontext übernehmen.
- Erstellt und per containers list zurückgelesen:
  - Web: accounts/572865630/containers/267198165 — GTM-M9TZZPLQ.
  - Server: accounts/572865630/containers/267197767 — GTM-M6SDZCN4.
- Container noch nicht auf Website eingebunden und keine Trackingversion veröffentlicht.
- GSC über bestehende Browsersitzung erreichbar, Property sc-domain:zuhausebleiben-kompass.de; Daten werden noch verarbeitet. Keine erneute GSC-Registrierung anfordern.
- Hermes-MCP-Liste im Profil milo ist leer; kein eigenes `stape`-CLI im PATH gefunden. Das belegt nicht die Unverfügbarkeit anderer Projektintegrationen. GTM-CLI liegt unter /Users/mac/.local/bin/gtm, Projektquellen unter /Users/mac/projects/Google-Tag-Manager-Hilfe/gtm-cli. Stape-Zugang/Endpunkt noch gesondert prüfen.

## Postfach
Benutzer bestätigt echtes Projektpostfach eingerichtet. Sicher erreichbarer Webmailer: https://server51.webgo24.de/webmail/ . Generische https://webmail.webgo.de/ führte im verwendeten Browser zu einem Zertifikatsfehler; nicht umgehen.

Vault-Listing enthielt keine Logins. Maskierter Speicherdialog für Projektpostfach wurde geöffnet, aber nicht bestätigt. Deshalb noch kein Login, IMAP/SMTP-Setup oder Versand. Kein Passwort im Chat erfragen, nicht wiederholt im selben Turn prompten. Origin-gebundene Browser-Vault-Füllung ist kein automatischer SMTP-Zugang; nach Speicherung passendes zugelassenes Mail-Secret-Setup prüfen.

## CTAs
Kontextuelle Artikel-CTAs sind im Renderer integriert und deployt: checklist_top, compare_top, print_bottom, editorial_contact. data-content-id ist nur der Artikelslug; keine personenbezogenen Attribute. Aktuell keine Messereignisse aktiviert.

Die CTAs führen zur tatsächlichen Checkliste, passenden Entscheidungshilfe, Druckfunktion oder redaktionellen E-Mail-Adresse. Keine 'Angebote anfordern'-Schaltfläche ohne angebundenen Anbieter. Kontakt ist keine Notfall-/Fachberatung; Hinweis keine Gesundheitsdaten senden.

## Consent/Cookiebanner-Gate
Vor GTM-/Stape-Produktivaktivierung CMP auswählen/konfigurieren. Gleichwertige Ablehnen/Annehmen-Auswahl und individuelle Einstellungen, standardmäßig keine optionalen Analyse-/Marketingrequests. Einwilligung und Widerruf respektieren. Keine Cookieless-Pings auf Verdacht. Reale Ziele/Anbieter/Speicherungen im Datenschutz beschreiben; keinen pauschalen Rechtssicherheitsstempel behaupten. Consent muss Ablehnung ohne nachgeladene optionale Tags und ohne blockierte Ratgeber-Nutzung bestehen. Banner nicht als bereits live melden.
