# Briefing 26: hausnotruf-alarm-ablauf — „Was nach dem Hausnotruf-Knopfdruck passiert" (37. Ratgeber)

Datum: 13.11.2026 · Cron-Lauf · Status: live (Commit folgt)

## Kandidatenentscheidung

Batch 21 dokumentierte als nächsten Schritt: Care-/Wohn-Journey bevorzugen (Lift-Cluster komplett). Gewählt:
**Hausnotruf-Alarm-Ablauf** — zwei Gründe:

1. **Revenue-Cluster**: Hausnotruf ist der Cluster mit zugelassenem Partner (Malteser, Awin 112616,
   approved 02.11., 2 Placements 10-€-CPL-Modell). Der Ablauf-Artikel bedient die Vorab-Kauf-Frage
   („Was passiert da eigentlich? Kommt dann wirklich jemand?") und trägt direkt in den Beratungstermin-Funnel.
2. **Brachliegende Recherche**: `research/hausnotruf-alarm-ablauf/` (09.11.) enthielt 12 Kompetitor-Rohdateien
   ohne Artikel; der Lauf resümiert sie mit frischer Primärverifikation.

SERP-Check (13.11., Websuche + curl): Dedizierte Konkurrenz existiert — medivato (Anbieter-Funnel),
Bundesverband Hausnotruf (schlichter 8-Schritt-Ablauf), gesund.bund.de (kurzer Ablauf-Abschnitt),
Malteser-FAQ (Hersteller), plus ein **dpa-Bericht vom 06.11.2026** (DRK-Zentrale Sachsen), der in keinem
Konkurrenz-Ratgeber integriert ist: 30-Sekunden-Annahmeziel mit 94 %-Selbstangabe, 80 % Fehl-/Probealarm-Anteil,
„Wenn sie drücken und wir nichts hören, kommt immer jemand", „weder Rettungsdienst noch Fahrdienst",
Verbandszahlen (1,2 Mio Nutzer 2024, 11.000 Rufe/Tag, 3.600 Einsätze/Tag).
**Verbesserung**: einzigartige frische Zahlen, strukturierte Alarmkette mit Verzweigung, stiller-Alarm-Fall,
Maßnahmenplan samt Daten-Sparsamkeit (Krankheitsangaben freiwillig), Fehlalarm-Entwarnung, BGH III ZR 92/16
(Leitsatz + 16-Stunden-Ausbildungsdetail) als Qualitätsfrage — kein Konkurrent zitiert das Urteil sauber.
Verworfene Alternativen: Region-Landesprogramme (doorway-Gate + Programmvolatilität, erst mit GSC-Daten),
Wohnraumanpassung Steuer (Kannibalisierung mit treppenlift-steuerlich-absetzen), weitere Lift-Long-Tails
(Cluster laut Batch 21 komplett).

## Kannibalisierungs-Check

0 Treffer auf „Ablauf/Kette/stiller Alarm" als Seitenthema im Bestand: die 5 Hausnotruf-Artikel decken
Auswahl (sturzerkennung), Kosten (kosten-anbieter-vergleich), Schlüssel (schluesselhinterlegung),
Angehörigen-Einrichtung (angehoerige), Kündigung (kuendigen) ab — die Alarmkette selbst fehlte.
Crosslinks bewusst: Schlüssel- und Kosten-Ratgeber verlinkt, kein Duplikat von deren Inhalt.

## Quellen (9, alle 13.11.2026 live abgerufen, Ledger 54/54 Zitate verbatim)

1. dpa-Bericht (n-tv) — DRK-Zentrale Sachsen: Geschwindigkeit, Fehlalarm, Verbandszahlen
2. Bundesverband Hausnotruf — Alarmkette/Beispielkette
3. Malteser-FAQ (Herstellerangabe, Kooperationspartner) — Sprechkontakt, stiller Alarm, Rettungskräfte, Tagestaste
4. gesund.bund.de (BMG-Portal) — Testrufe, Fehlalarm „kein Problem", „Hausnotruf ohne Zentrale"-Warnung
5. Sieversgruppe/autavie (Herstellerangabe) — Maßnahmenplan, Grenze des Plans, freiwillige Krankheitsangaben
6. BGH III ZR 92/16 (11.05.2017) via datenbank.nwb.de — Leitsatz, Entlastungsbeweis, 16-Stunden-Ausbildung
7. BGH-Pressemitteilung Nr. 071/2017 via stange.de — Sachverhalt (Stöhnen, Schlaganfalldiagnose)
8. medivato (Anbieter-Magazin) — Abgrenzung zur 112
9. Verbraucherzentrale 10566 — Basistarif-Inhalte, 24-Stunden-Zentrale

Bewusste Absenzen: keine Fehlalarm-Gebühr behauptet (keine Quelle nennt eine; AGB/Vertrag als
maßgeblich benannt); DRK-Zahlen als Angaben dieser einen Zentrale markiert (kein Marktdurchschnitt);
BGH-Einzelfall ohne Prognose; keine Förder-/Pflegekassen-Beträge (Route via Crosslink auf Kosten-Ratgeber).

## Integration

- `article-renderer.mjs`: specialMap +1 (Early-CTA „Kosten & Anbieter vergleichen" → hausnotruf-kosten-anbieter-vergleich)
- `data/partner-links.json`: slug in malteser_beratungstermin-Placement aufgenommen (3. Artikel dieses Placements);
  Disclosure-Prüfung: datenschutz.html nennt Malteser weiter (Partner-Gate C/D unverändert grün)
- `research/llms-txt.py`: SUMMARIES + SECTION_MAP +1 (Honest-Content-Policy: handgeschriebene Zusammenfassung)
- Zähler: test_articles 36→37, verify_checklists_build RSS 36→37; Sitemap dynamisch 47→48 Locs

## Gates (Ergebnisse)

- npm test: EXIT 0 — 62 HTML-Seiten, 37 Artikel (Anchors/Bilder/JSON-LD), Cross-Links 3/Care sauber,
  Titles ≤65/Descs ≤160: 0 Verletzungen, Playwright-Consent 21 passed, Partner A–F ALL PASS
- verify_checklists_build (Launch-Dist): ALL PASS — RSS 37 Items, llms deckt alle 37 ab, Sitemap-Set exakt
- Ledger: research/build_alarm_ledger_131126.py → 54/54 Zitate verbatim (Break auf Missmatch)
- SVG-Gate (research/verify_alarm_svg_131126.py): 33/33 — getBBox inside, Pairwise Text-Text 0,
  Chip-Check, Screenshot; Sichtkontrolle (Vision) nach Fix: Fehlalarm-Zeile vollständig im Streifen,
  Fußbereich sauber; Fix: Streifenhöhe 104→118 px (Unterkanten-Abstand)
- Artikel-Akzeptanz (research/verify_alarm_article_131126.py): 90/90 — alle JSON-Keys im HTML
  (Tag-+Citation-Strip, Unescape), 12 Kernzahl-Needles (case-normalized beidseitig), 9 Quellen-URLs,
  Partner-Placement mit rel="sponsored"+Anzeige-Label, kein Marker auf anderen Seiten, specialMap-CTA-Ziel,
  Checklisten-Anker existiert, Related-Links im Care-Cluster
- Mobile 390 px: scrollWidth 390 (0 px Overflow), Screenshot-Sichtkontrolle sauber
