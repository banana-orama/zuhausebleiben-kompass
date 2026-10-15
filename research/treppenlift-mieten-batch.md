# Recherche- und Freigabeprotokoll: Treppenlift mieten (Briefing 3, Phase 1)

Erstellt: 2026-10-15 (Cron-Lauf, Betreiber-Modus). Umfang: ein Artikel (`content-ready/treppenlift-mieten.json`), eine Grafik, dieses Protokoll, Ledger, Testsuite-Zähler. Keine Renderer-Logikänderung, keine Formulare, keine Partnerlinks.

## SERP-Check (2026-10-15, web_search)

Query: „Treppenlift mieten monatliche Kosten Miete oder kaufen". Ergebnisse: Pflicht: SERP dominiert von Vermittlungs-/Lead-Gen-Portalen (pflege.net, deinpflegevergleich, treppenlift.io, wohnalio) mit teils widersprüchlichen Richtwerten (80–150 €, 80–200 €, 100–300 €, 50–300 €/Monat) und Anfrage-Funnels. Organisch: Anbieterblogs. Lücke: vermittlungsfreie Entscheidungshilfe mit vollständiger Miet-Positionsliste, Mindestmietdauer-Risiko, Pflegekassen-Einordnung (§ 40 SGB XI) und fairer Miete-gegen-Kauf-Rechnung mit erfundenen, als solche markierten Werten. Suchvolumina nicht behauptet.

Zweite Query (Verbraucherzentrale): traf die VZ-Ratgeberseite, die test.de-Seite zu Zuschüssen sowie die aktuelle Verbandsklage-Meldung (Mobilae) — letztere als frischer, unabhängiger Beleg für AGB-Risiken in der Branche aufgenommen.

## Suchintention und Abgrenzung

- Zielgruppe: ältere Menschen und Angehörige kurz vor der Anfrage; teils mit befristetem Bedarf (Reha), teils dauerhaft.
- Keine Kannibalisierung: `treppenlift-kosten` behandelt Kauf-/Angebotskosten, `treppenlift-gebraucht-oder-neu` den Gebrauchtkauf, `treppenlift-firmen-vergleich` die Anbieterwahl. Diese Seite behandelt ausschließlich das Mietprodukt: Vertragstyp, Laufzeit, Rückbau, Zuschuss bei Miete, Miete-gegen-Kauf-Rechnung. Interne Verlinkung über die bestehende Related-Logik des Renderers (treppenlift-Cluster).
- Monetarisierung: unverändert gesperrt (keine Formulare, keine Partnerlinks vor Liftstar-Kanalfreigabe).

## Quellenkette (Ledger: research/miete-ledger.json, alle mit Verbatim-Evidenz)

Artikel-Nummerierung → Ledger-IDs: [1]→1, [2]→2, [3]→3, [4]→5, [5]→6, [6]→4.

1. Verbraucherzentrale: Treppenlifte – Planung und Umsetzung (Festpreis, Vermieter-Zustimmung, Problemfelder, schriftliche Zusagen). Abruf 2026-10-15, HTTP 200, evidence/vz-treppenlifte-miete.html.
2. § 40 SGB XI (Abs. 4: Ermessenszuschuss, 4.180 € je Maßnahme; Abs. 7: 3/5-Wochen-Fristen). Abruf 2026-10-15, HTTP 200, evidence/sgb11-40-miete.html.
3. pflege.net: Treppenlift mieten oder kaufen (80–200 €/Monat Richtwert, Anzahlung, Wartung in der Rate, Mindestmietdauer-Warnung, Zuschuss bei Miete oft nur auf Einmalkosten). Abruf 2026-10-15, HTTP 200, evidence/pflegenet-miete.html. Vergleichsportal-Angabe, nicht als Marktmittelwert übernommen.
4. HIRO LIFT: „Lohnt es sich, einen Treppenlift zu mieten?" (Hersteller-Selbstauskunft: Miete für kurze Dauer/gerade Fahrbahn, Kurvenschiene Einzelanfertigung, Bereitstellungssumme, Warnung vor Modellrechnungen). Abruf 2026-10-15, HTTP 200, evidence/hiro-mieten.html.
5. Verbraucherzentrale: Klage gegen Mobilae (Unterlassungsklage, OLG Hamm, eingereicht 08.10.2026, 18 AGB-Klauseln zu Treppenlift-Verträgen). Abruf 2026-10-15, HTTP 200, evidence/vz-mobilae-klage.html. Als unveröffentlichte Klage eingeordnet: keine Entscheidung, kein Schluss auf andere Anbieter.
6. treppenlift.io: Treppenlift miete (zweites Vergleichsportal mit abweichendem Richtwert 50–300 € + bis zu 50 % Einmalzahlung). Abruf 2026-10-15, HTTP 200, evidence/treppenlift-io-miete.html. Wird ausschließlich als Beleg für die Spreizung der Richtwerte zitiert.

Google-Leitlinien vor Veröffentlichung geprüft (alle HTTP 200 am 2026-10-15): creating-helpful-content, ai-features, spam-policies, google-images (developers.google.com/search/docs). Keine Richtlinienänderung, die diesem Artikeltyp widerspricht.

## Eigene Werte (alle tool-geprüft 2026-10-15, erfunden und als solche gekennzeichnet)

- Annahmen: Kauf 5.120 € inkl. Montage + 130 €/Jahr Wartung; Miete 1.950 € Bereitstellung + 145 €/Monat inkl. Wartung.
- Miete gesamt: 6M 2.820 € · 12M 3.690 € · 24M 5.430 € · 36M 7.170 €.
- Kauf gesamt: 12M 5.250 € · 24M 5.380 € · 36M 5.510 € (6M: 5.185 €).
- Rechnerischer Gleichstand: 23,6 Monate („ab rund 24 Monaten").
- Mindestlaufzeit-Beispiel: 6M Raten 870 €; 2M genutzt 290 €; Differenz 580 €.
- Keiner dieser Werte wird als Marktpreis ausgegeben; die Spreizung der Portal-Richtwerte (50–300 €) wird im FAQ explizit gezeigt und nicht aufgelöst.

## Bild

`assets/images/treppenlift-miete-angebot.svg` (1000×780, XML-valide): eigene Schema-Grafik „Was in einem Mietangebot stehen muss" (8 Positionen + Beispielrechnungs-Panel). Stil wie bestehende Illustrationen (#f7f5ef/#245b47). KI-unterstützt, Werte erfunden, im Bild und Caption gekennzeichnet; keine reale Montage/Referenz. Alt-Text mit vollständiger Inhaltsbeschreibung. Datei liegt im Projekt, keine Fremdquelle, keine Lizenzkosten.

## Qualitätsgate (Ergebnisse)

- Citation-Verify: `sources.py verify research/treppenlift-mieten.draft.md --evidence --min-coverage 0.5` → PASS (47 Prosa-Sätze, 29 mit Provenienz = 62 %; 21 zitiert + 20 × [unverified]-Markierung; 6/6 Quellen mit Verbatim-Evidenz).
- Eigene Aussagen: im Artikel mit `*` markiert; Legende im Abschnitt „Transparenz und Grenzen". Im Gate-Draft als [unverified] geführt.
- Arithmetik: PASS (alle Werte oben mit Tool gerechnet).
- Build/Tests: `npm run build` → 28 Seiten; `test_site.py` PASS (25 HTML, je 1 H1, 0 Formulare, noindex, Links, XML); `test_articles.py` PASS (7 Artikel, Assets, Anker, JSON-LD, SVG). Testzähler 6→7 angepasst, Print-Text dynamisiert.
- Preview-Status: Artikel erscheint wie die anderen sechs als noindex-Vorschau; Sitemap bleibt leer; Formularteil bleibt deaktiviert.

## Grenzen / bewusst nicht behauptet

- Keine Marktpreise, keine Ersparnis-Prozent, keine Mindestmietdauer-„Regel", keine Rechtsberatung (Mobilae-Klage als unveröffentlicht eingeordnet).
- Keine Aussage zur KfW-Förderung bei Miete (nicht recherchiert → nicht behauptet).
- Steuerthemen bewusst nicht aufgenommen (VZ-40 %-Angabe betrifft Kauf-/Vertragskontext und wäre hier ohne Prüfung nicht belastbar).
