# Briefing 21 — Hausnotruf für Angehörige einrichten (Batch 17, 10.11.2026)

## SERP-Auswahl (GSC im Cron weiter ohne Google-Sitzung)

Query-Feld „hausnotruf für angehörige einrichten/mutter“: 5 von 8 Treffern = Bing-Ads
(pflege24-Netzwerk, senioren-beratung-deutschland, deinePflege, Vitakt, HSP);
organisch nur 2 dedizierte Seiten — beide Anbieter-Magazine mit Interessenkonflikt:
- HSP Hausnotruf „für Angehörige“ (hsp-hausnotruf.de + Zweit-Domain hausnotruf-hsp.de)
- BeWo Telehealthcare Ratgeber (Tunstall-Gruppe)
Frage „hausnotruf beantragen“: notfallknopf.de, sanivia.de, pflegekompass.de — ebenfalls
Anbieter-/Broker-Seiten; neutral (Verbraucherzentrale) deckt die Angehörigen-Journey nicht ab.

Bestand deckte den Intent mit 0 Abschnitten (grep: keine der 31 Artikel behandelt
Ansprache/Beauftragung/Vollmacht/Einrichtung aus Angehörigen-Sicht; Kosten-Artikel hat
„Wann sinnvoll“, kuendigen den Ausstieg, schluessel die Schlüsselfrage, hilfsmittel die
Kassen-Route — alles verlinkt, nichts kannibalisiert).

Verbesserung: neutraler Journeyschnitt (Erkennen → Gespräch → Rollen → Antrag → Einrichtung),
dokumentierte Divergenzen, Checkliste. Verworfen an diesem Lauf: keine neuen Kandidaten
benötigt; bestehende Verworfenliste (Wartung, Haltegriffe, Schwellenrampe, Kurzzeitpflege,
Entlastungsbetrag, Pflegezeit, Pflegegrad-Höherstufung, Duschsitz-Kasse) unverändert.

## Quellen (7, alle 10.11.2026 live abgerufen, Evidenz research/evidence/angehoerige-101126/)

1. Verbraucherzentrale: Hausnotrufsysteme erklärt (10566) — neutraler Kern
   (27–40 € Basistarif, bis 27 € Pflegekasse + Voraussetzungen + MD-Prüfung,
   „Vertragspartner der Pflegekasse“, Leistungsanforderungen, Zentrale-Daten,
   Demenz-Grenze, Technik).
2. Malteser (Herstellerangabe) — „Angehörige die treibende Kraft“, App Echtzeit,
   Pakete (Grundsicherheit „wenn Ihre Angehörigen in der Nähe sind“), Installation/Einweisung,
   Mobilfunk ohne Anschluss, 27-€-Zuschuss mit eigener Voraussetzungs-Einschränkung.
3. HSP (Anbieter-Magazin) — Gesprächs-Rahmung, „kann eine Vollmacht erforderlich sein“ (vage),
   Notfallplan-Ebene.
4. BeWo (Anbieter-Magazin) — „komplett aus der Ferne organisieren“, „Vertrag als Angehörige
   anstoßen“, funktionsfertiges Gerät per SIM.
5. Notfallknopf.de (Anbieter-Ratgeber) — Antrags-/Vollmacht-Spezifik (Vorsorgevollmacht
   Vermögenssorge/Vertragsangelegenheiten, „reine Gesundheitsvollmacht reicht nicht“,
   Betreuer-Aufgabenkreis), Versorgungsvertrag § 78 SGB XI, Fristen 3/5 Wochen,
   „innerhalb einer Woche betriebsbereit“, ohne Vorleistung.
6. Sanivia (Anbieter-Ratgeber) — „0 € im Monat“-Claim (Gegenstück zur VZ-Nüchternheit).
7. VZ-Veranstaltungsseite Vorsorgevollmacht — „weder Ehepartner noch Kinder können dies
   automatisch übernehmen“ (neutraler Vertretungs-Anker).

Ledger: research/angehoerige-101126-ledger.json — 117/117 Pässe
(research/verify_angehoerige_101126.py): 84 Verbatim-Zitate + 8 Artikel-Absenz-Checks +
Integrität (alle [n] auflösen, jede Quelle zitiert, checked_at) + Kernzahlen + 0×Treppenlift.
Zero-Arithmetik: alle Zahlen wörtliche Quellenangaben, keine Berechnungen.

## Dokumentierte Divergenzen

- D1 Vollmacht: HSP vage vs. notfallknopf spezifisch vs. BeWo „als Angehörige anstoßen“.
- D2 Einrichtungsweg: Malteser Installation+Einweisung vs. BeWo funktionsfertig per Post vs.
  VZ Leistungsanforderung.
- D3 VZ-Zusatzleistungen: „rund 30 bis 50 Euro (oder auch mehr)“ (Text) vs. „30 bis 80 Euro“
  (FAQ derselben Seite).
- D4 Kosten-Realismus: sanivia „0 €“ vs. VZ „bis zu 27 €“ + Voraussetzungen + MD vs.
  Malteser „27,00 € ab Pflegegrad 1“ mit eigener Einschränkung.

## Grafik

assets/images/hausnotruf-angehoerige-wegweiser.svg — 5 nummerierte Schritte + Zeitfenster-Band
+ Footer. Gates: getBBox-Overflow + Pairwise + Chip-Kontext 0 Issues
(research/verify_angehoerige_svg_mobile_101126.py, Chromium), Mobile 390 px 0 px Overflow.
VITATION: 1. Sichtkontrolle fand echten Fehler (Schritt-3-Zeile lief hinter den Chip) →
gekürzt, 2. Screenshot-Inspektion sauber. KI-unterstützt gekennzeichnet.

## Renderer/Infra

- article-renderer.mjs specialMap +1 (Early-CTA „Kosten & Anbieter vergleichen“ →
  hausnotruf-kosten-anbieter-vergleich; Placements leben dort, bewusst 0 Marker auf dem Artikel).
- data/cross-links.json links+rationale +1 (kosten-vergleich, schluesselhinterlegung,
  mobil-gps — care-intern).
- research/llms-txt.py SUMMARIES + SECTION_MAP (Hausnotruf-Sektion) +1.
- isCare-Regex trifft via hausnotruf-Präfix (keine Regex-Änderung).
- Testzähler: test_articles 31→32; verify_checklists_build RSS 31→32; test_partner_links A3 ≥30→≥31.

## Gates

- research/verify_angehoerige_101126.py: 117/117 PASS
- research/verify_angehoerige_content_101126.py: 117 PASS (LAUNCH-dist; jeder JSON-Key im
  HTML, Related 3× Care-Cluster, CTA-Ziel korrekt, 0 Partner-Marker, 0 awin, kein Lift-CTA)
- research/verify_angehoerige_svg_mobile_101126.py: ALL PASS (0 Geometrie-Issues, 0 px Mobile)
- npm test: siehe CONTENT-PIPELINE-STATE Batch 17 (Ergebnis nach Lauf)
- Deploy/Live-Readback/IndexNow: siehe CONTENT-PIPELINE-STATE Batch 17
