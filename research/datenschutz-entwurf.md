# Datenschutz-Entwurf: ZuhauseBleiben Kompass

Status: **ENTWURF — keine Rechtsfreigabe, keine anwaltliche Prüfung.** Passend zum aktuellen Hosting (statischer Build auf GitHub Pages, Formular deaktiviert, kein Tracking). Quellen mit Abrufdatum 2026-10-14 im Ledger; Verbatim-Evidenz in research/evidence/.

## Faktengerüst (verifiziert)

1. Hosting: Statischer Build (27 Seiten) aus dem eigenen Repository; GitHub Pages hostet Websites „direkt aus einem Repository" auf GitHub.[11]
2. Eigene Seite: keine Cookies, keine Analyse-/Marketing-Skripte, keine externen Webfonts (grep-Prüfung über generate.mjs/design.css, 2026-10-14; test_site.py: „no forms").
3. Hostingdienst GitHub: erhebt bei Dienstnutzung u. a. IP-Adresse, Geräte-/Sitzungsinformationen sowie automatisch protokollierte Website-Interaktionsdaten (Verweiser, Datum/Uhrzeit, aufgerufene Seiten, geklickte Links).[12] GitHub ist zum EU-US-Datenschutzrahmen (DPF) zertifiziert.[12]
4. Mailpostfach: webgo (MX server51.webgo24.de, autoritativ geprüft 2026-10-14). webgo verarbeitet im eigenen Betrieb technische Abrufdaten inkl. IP-Adresse und Zeitpunkt (eigene Datenschutzerklärung).[13]
5. Verantwortlicher laut Impressum: Tobias Batke, Sängertshöhe 14, 51588 Nümbrecht; anfragen@zuhausebleiben-kompass.de (data/content.json).
6. Für Beschwerden zuständige Datenschutzaufsichtsbehörde (Sitz Nümbrecht = NRW): LDI NRW (Landesbeauftragte für Datenschutz und Informationsfreiheit).[10]
7. Informationspflichten bei direkter Erhebung von personenbezogenen Daten regelt Art. 13 DSGVO, u. a. Name/Kontaktdaten des Verantwortlichen und Verarbeitungszwecke mit Rechtsgrundlage.[9]

## Anwendungsentscheidung für den Entwurf

Die Seite erhebt **keine** personenbezogenen Daten durch uns: kein Formular, keine Cookies, kein Tracking. Server-/Sicherheitslogdaten erheben ausschließlich unsere Diensteanbieter in eigenverantwortlicher Funktion (GitHub für den Abruf[12], webgo fürs Mailpostfach[13]). Der Entwurf bestimmt daher:

- **Verantwortlicher** für diese Website: Tobias Batke (Impressum). Für Abruf-Logdaten ist GitHub eigenverantwortlich; wir benennen das transparent, statt Rechtsverhältnisse falsch darzustellen.
- **Kein berechtigtes-Interessen-Hinweis auf unsere eigene Logung** — wir loggen nichts. Fände sich künftig eigenes Serverloggen (Umzug zu webgo-Hosting), müsste der Entwurf um Art. 6 Abs. 1 lit. f, Speicherdauer und Betroffenenrechte erweitert werden. Bis dahin bewusst ausgelassen.
- **Dienstanbieter-Abschnitt**: GitHub, Inc. (Hosteaseite, DPF-zertifiziert[12]) und webgo GmbH (Mailbetrieb[13]) mit je einem Satz Zweckangabe — rein informativ, keine Auftragsverarbeitung durch uns, solange wir keine personenbezogenen Daten verarbeiten lassen.

## Entwurfstext (in die Seite integriert als datenschutz.html, noindex)

```text
Datenschutz

Stand: [NUR SETZEN, WENN TEXT FREIGEGEBEN] — dieser Entwurf ist mit noindex veröffentlicht.

1. Verantwortlicher
Tobias Batke, Sängertshöhe 14, 51588 Nümbrecht, Deutschland
E-Mail: anfragen@zuhausebleiben-kompass.de

2. Unser Grundsatz auf dieser Vorschau
Diese Website erhebt keine Kontaktdaten, keine Angaben zu Pflege oder Gesundheit und setzt keine
Cookies ein. Es gibt keine Analyse-Dienste, keine Werbe-Netzwerke und keine externen Schriften.
Die Anfragefunktion ist deaktiviert. Sie können diese Seiten besuchen, ohne sich zu identifizieren.

3. Abruf der Seiten (Hosting)
Das Angebot wird als statische Website über GitHub Pages (GitHub, Inc., 88 Colin P Kelly Jr St,
San Francisco, CA 94107, USA) ausgeliefert. Beim Aufruf verarbeitet GitHub in eigener
Verantwortung technische Verbindungsdaten (u. a. IP-Adresse) und Sicherheitslogs, um den Betrieb
und die Sicherheit des Dienstes sicherzustellen. GitHub ist nach dem EU-US-Datenschutzrahmen
zertifiziert. Wir haben auf diese Verarbeitungen keinen Einfluss und erhalten keine Bestände.
Nähere Angaben: Datenschutzerklärung von GitHub (docs.github.com).

4. E-Mail-Kontakt
Wenn Sie uns eine E-Mail an anfragen@zuhausebleiben-kompass.de senden, verarbeiten wir Ihre
Adresse und Ihre Inhalte ausschließlich zur Bearbeitung Ihrer Anfrage (Art. 6 Abs. 1 lit. f DSGVO —
Interesse an der Beantwortung). Das Postfach wird bei webgo GmbH, Germany betrieben; webgo
verarbeitet hierzu technische Daten. Wir löschen Anfrage-E-Mails, sobald sie keinem Zweck mehr
dienen, spätestens nach [X] Monaten — Endwert vor Freigabe festlegen.

5. Keine Profilbildung, keine Weitergabe
Wir verkaufen keine Daten, schalten keine Werbung und erstellen keine Nutzungsprofile. Eine
Weitergabe von Daten durch uns findet nicht statt, solange keine Vermittlung eingerichtet ist.

6. Ihre Rechte
Sie haben das Recht auf Auskunft (Art. 15 DSGVO), Berichtigung (Art. 16), Löschung (Art. 17),
Einschränkung der Verarbeitung (Art. 18), Datenübertragbarkeit (Art. 20) und Widerspruch
(Art. 21). Eine erteilte Einwilligung können Sie jederzeit widerrufen. Wenden Sie sich dafür an die
Adresse unter Abschnitt 1. Zudem können Sie sich bei einer Datenschutzaufsichtsbehörde
beschweren — für unseren Sitz zuständig ist der Landesbeauftragte für Datenschutz und
Informationsfreiheit Nordrhein-Westfalen (ldi.nrw.de).

7. Keine Entscheidungsprofilekte / kein Gesundheitsdaten-Bezug
Wir erheben keine Gesundheitsdaten. Auch nach dem geplanten Start der Angebotsvermittlung gilt:
Das Anfrageformular soll bewusst ohne Pflichtangaben zu Krankheit oder Pflegegrad auskommen;
solche Angaben sollen direkt beim fachlich zuständigen Partner entstehen.

8. Änderungen
Wir passen diese Erklärung an, wenn sich Zweck, Anbieter oder Technik ändern. Der Stand wird
nur nach tatsächlicher Prüfung aktualisiert.

Quellen der Prüfung (intern): EUR-Lex DSGVO-Konsolidierung (Art. 13: Pflichtangaben bei
Erhebung bei der betroffenen Person), GitHub-Docs/Datenschutzerklärung (Abruf 2026-10-14),
webgo-Datenschutzerklärung (Abruf 2026-10-14), LDI NRW (Beschwerdeweg).
```

Hinweise vor Freigabe (offen, bewusst nicht verschwiegen):

- **[X] Monate Löschfrist** E-Mail: von Tobias festlegen (Vorschlag: 6 Monate, orientiert an üblichen Löschfristen; [unverified] als Rechtsgrenze).
- **Rechtsgrundlage Abschnitt 4**: lit. f ist die konservative Wahl für die bloße Beantwortung; ob lit. b/Art. 6 Abs. 1 lit. b (vorvertragliche Maßnahmen) bei späterer Angebotsvermittlung zutrifft, ist mit der Partnerstrecke zu entscheiden. [unverified]
- **§-Angaben (TMG→DDG-Wechsel, Höchst-/Ordnungsrahmen)** wurden bewusst nicht zitiert: keine Rechtsfreigabe-Imitation. Der Text nennt nur Regelungen mit wörtlich geprüften Offizialquellen.
- Der Text ersetzt **keine** Prüfung durch eine rechtskundige Stelle; Veröffentlichung als „endgültig" erst nach Tobias-Freigabe.

## Sources

[9] https://eur-lex.europa.eu/legal-content/DE/TXT/HTML/?uri=CELEX:32016R0679 — DSGVO (VO (EU) 2016/679) konsolidiert, EUR-Lex DE
    > "den Namen und die Kontaktdaten des Verantwortlichen sowie gegebenenfalls seines Vertreters;"
[10] https://www.ldi.nrw.de — LDI NRW: Landesbeauftragter für Datenschutz und Informationsfreiheit
    > "LDI - Landesbeauftragte für Datenschutz und Informationsfreihei"
[11] https://docs.github.com/de/pages/getting-started-with-github-pages/what-is-github-pages — GitHub Docs: Was ist GitHub Pages?
    > "Sie können GitHub Pages verwenden, um eine Website über sich selbst, Ihre Organisation oder Ihr Projekt direkt aus einem Repository auf GitHub zu hosten."
[12] https://docs.github.com/de/site-policy/privacy-policies/github-general-privacy-statement — GitHub Datenschutzerklärung (General Privacy Statement, DE)
    > "Website-Nutzungsdaten: Wir protokollieren automatisch Daten über Ihre Website-Interaktionen, einschließlich der verweisenden Website, Datum und Uhrzeit des Besuchs, der aufgerufenen Seiten und der angeklickten Links."
    > "Weitere Informationen zum Datenschutzgrundsatz (DPF)-Programm und zum Anzeigen unserer Zertifizierung finden Sie unter https"
[13] https://webgo.de/datenschutz — webgo GmbH Datenschutzerklärung
    > "werden zunächst technische Informationen, wie Informationen zum Browser und Ihrem System, als auch Ihre IP-Adresse und Zeitpunkt des Abrufs erhoben."
