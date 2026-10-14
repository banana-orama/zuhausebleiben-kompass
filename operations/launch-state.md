# Launch-State: ZuhauseBleiben Kompass

Aktualisiert: 2026-10-14 (Cron-Lauf, Betreiber-Modus) · Letzte verifizierte Tatsachen mit Datum und Quelle; alles andere ist als offen markiert.

## Phase-Übersicht

| Block | Stand | Nächste Einheit |
|---|---|---|
| DNS/Hosting | **Fortschritt:** Apex-A-Records autoritativ auf GitHub-Pages-IPs (185.199.108–111.153), www-CNAME → banana-orama.github.io, MX webgo unverändert. Öffentliche Resolver (Google/Cloudflare/FritzBox) konvergiert. Lokaler macOS-Cache hielt beim Lauf noch 185.30.32.51 (TTL 3600) → öffentliche Erreichbarkeit jetzt erwarten, lokal erst nach Cache-Ablauf/Flush testbar. | Nächster Lauf: normalen Apex-HTTPS-Readback wiederholen (curl, ohne --resolve); Ziel HTTP 200 + noindex sichtbar. www→Apex-Redirect am Pages-Edge bestätigt (301, x-github-request-id). |
| Partnerannahme (P1) | **Kernblocker verkleinert:** Lifta DE Programm auf Awin (ID 40988) offiziell verifiziert: 50 €/validem Lead oder 500 €/Auftrag, 30 Tage Cookie (Abruf 2026-10-14, ui.awin.com). Detail-T&C hinter Bewerbung; 2023er-Listing als Kontext dokumentiert (SEM/Brand-Bidding verboten, nur freigegebene Websites, valider Lead = Beratungstermin-Anfrage). Altbehauptung „40–60 €" als überholt markiert. | Einmalige Tobias-Freigabe: (a) Awin-Publisher-Registrierung auf seinen Namen, (b) Mailversand an koop@liftstar-marketing.de. Beides antragsfertig in research/partner-programm-awin-lifta.md. |
| Lead-Datenannahmeweg (P2) | Kein eigenes Formular; build/seitig keine Erfassung (Test: „no forms"). Offene Frage an Liftstar: Weiterleitung vs. Beratungsfenster vs. eigenes Formular (Frage 3 der Erstmail). | Antwort abwarten; erst dann P2-Strecke (ohne sensible Felder) bauen. |
| Datenschutz (P3) | **Entwurf fertig und integriert:** Volltext (8 Abschnitte: Verantwortlicher, keine Datenerfassung, GitHub-Hosting mit DPF-Angabe, E-Mail/webgo, keine Profile, Betroffenenrechte, keine Gesundheitsdaten, Änderungen) als noindex-datenschutz.html im Renderer ersetzt den Thin-Platzhalter; offizielle Quellen (EUR-Lex DSGVO Art. 13, GitHub-Docs + Privacy Statement, webgo-Datenschutz, LDI NRW) im Ledger mit Verbatim-Evidenz. Offen: endgültige E-Mail-Löschfrist, Rechtsgrundlage lit. f vs. lit. b für spätere Vermittlung — bewusst markiert, keine Rechtsfreigabe-Imitation. | Tobias-Freigabe des Texts einholen; erst danach steht P2 (Partnerstrecke) an. |
| Indexierung | noindex aktiv geprüft im ausgelieferten HTML (meta robots noindex,follow, via Pages-IP); Sitemap leer lt. Testsuite. Startgate bleibt dokumentiert aus. | Erst nach P1-Zusage + P3-Draft: Gate-Kriterien in dieser Datei festhalten. |

## Verifizierte Befunde (mit Abrufdatum)

- 2026-10-14: Awin-Merchantprofil Lifta DE 40988 live, Bewerbungsbuttons aktiv, 50 €/Lead bzw. 500 €/Auftrag, 30-Tage-Cookie, koop@liftstar-marketing.de. [research/evidence/awin-profile-40988.txt]
- 2026-10-14: Awin-Beitrittsvoraussetzungen offiziell (18+, Werbeplatz, Steuer-/Bankdaten erst für Auszahlung, Echtzeit-Prüfung üblich, Artikelstand 14.10.2025). [research/evidence/awin-requirements-de.txt]
- 2026-10-14: Liftstar-Listing (100partnerprogramme) vom 20.05.2023: SEM verboten, nur freigegebene Websites, Leadvalider-Definition, Ausschlussklausel — als historischer Kontext, nicht als aktueller Beleg. [research/evidence/100pp-liftstar.txt]
- 2026-10-14: Treppenlift-Lotse-Programm (60–120 €) zuletzt aktualisiert 19.02.2021, Portal-Inaktivität, keine öffentliche Partnerseite → verworfen. [research/evidence/100pp-treppenlift-lotse.txt]
- 2026-10-14: DNS autoritativ (ns1.webgo.de): Apex 4× 185.199.108–111.153, www CNAME banana-orama.github.io, MX 10 server51.webgo24.de (Mail-DNS unangetastet). dig @8.8.8.8 / @1.1.1.1 / @192.168.178.1 identisch.
- 2026-10-14: Origin-Readback via --resolve 185.199.108.153: HTTP/2 200, server: GitHub.com, meta robots noindex,follow, last-modified 19:58 UTC (heutiger Build). Normaler Apex-Curl aus diesem Haushalt: noch 403 webgo nginx wegen lokalem Cache (dscacheutil lieferte 185.30.32.51; TTL 3600). Kein /etc/hosts-Override, keine AAAA-Records.
- Build/Tests lokal: 27 Seiten, Preview-Modus noindex/keine Lead-Erfassung; test_site.py PASS (24 HTML, Links, H1, keine Formulare, XML), test_articles.py PASS (6 Artikel, Assets, Anker, JSON-LD, SVG-XML).
- 2026-10-14: datenschutz.html neu gebaut: noindex,follow geprüft, nicht in sitemap.xml, 8 H2-Abschnitte, externe Links nur GitHub-Docs/Privacy + LDI NRW (Origin-Readback nach Pages-Build folgt im nächsten Lauf bzw. unten).

## Einmalige Nutzerfreigaben (konkret, nichts sonst)

1. GO: Awin-Publisher-Konto auf Tobias Batke (Kleingewerbe) registrieren; mögliche einmalige Netzwerkkaution offen ([unverified] in research/partner-programm-awin-lifta.md), Steuer-/Bankdaten erst für Auszahlung nötig.
2. GO: Versand der vorbereiteten Erstmail an koop@liftstar-marketing.de (Text im Artefakt, versandfertig, NICHT gesendet).

## Nicht vergessen

- Kein Formular, keine Indexierung, keine Pinterest-Schaltung vor schriftlicher Liftstar-Antwort (Kanalfreigabe).
- Keine 40–60-€-Zahlen mehr als „aktuell" zitieren — Awin-Profil (50/500 €) ist die Referenz.
- Vor jedem Commit fremde WIP-Dateien prüfen; nur eigene Artefakte stagen.
- Webextract-Backend in dieser Umgebung: ddgs (search-only) — Seiteninhalte via Browser lesen, evidence-Dateien dort sichern.
