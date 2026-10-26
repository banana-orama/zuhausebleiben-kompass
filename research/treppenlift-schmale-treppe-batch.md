# Batch 8 (26.10.2026, Cron-Lauf): Briefing 11 — Treppenlift für schmale Treppen

**Artikel:** `content-ready/treppenlift-schmale-treppe.json` · Slug `/treppenlift-schmale-treppe.html`
**Status vor Commit:** editorial-reviewed-preview (Freigabekette in diesem Protokoll) · Grafik `assets/images/treppenlift-schmale-treppe-messplan.svg`
**GSC-Hinweis:** GSC-Queries weiterhin nicht abrufbar (Cron-Browser ohne Google-Sitzung, Vault ohne Google-Login) — Topic-Wahl daher SERP-/Quellen-basiert.

## Topic-Wahl und Abgrenzung (Kannibalisierungs-Check)
- Kandidaten gegen die Gates geprüft: Wartung (10+ Konkurrenten, post-purchase = schwächere Lead-Economics), Einbau-Ablauf (10 Konkurrenten, umfangreich durch bestehende Cluster-Artikel abgedeckt), Pflegegrad-Widerspruch (VZ-Direktartikel als stärkster Konkurrent, von payable Events am weitesten entfernt).
- Gewählt: **schmale Treppe** — lift-Kerncluster, intent-distinct (grep über content-ready: nur eine Streuung in treppenlift-angebote-vergleichen), Leser*innen sind tief in der Kauf journey (Aufmaß-Schwelle). SERP (26.10.2026): 7+ Konkurrenten; Mindestbreiten-Angaben widersprechen sich teils (61 cm vs. 70 cm als "Mindestbreite").
- Unsere Verbesserung: Zwei-Fragen-Auflösung (Gerätemaß vs. verbleibende Laufbreite), dokumentierte Herstellerdiskrepanz (HIRO 70 cm vs. Lifta/TK 80 cm), Mess-Anleitung + Aufmaß-Checkliste, VZ-Prüfpunkte, Alternativen-Übersicht — keine der konkurrierenden Seiten trennt so sauber mit neutraler Quellenkette.

## Kernbefunde (alle verbatim im Ledger, 53/53 PASS)
1. **Gerätemaß:** Hersteller mit veröffentlichtem Wert nennen 61–77 cm (Access BDD Flow X und TK S200 je 61 cm mit Fahrt-Drehsitz); Lifta und HIRO veröffentlichen KEIN Gerätemaß, sondern nur Gebäudemaße (Fachportal-Erhebung vom 07.10.2026 über 8 Hersteller/Modellreihen, nur selbst veröffentlichte Werte, keine Schätzungen).
2. **Herstellerdiskrepanz dokumentiert:** HIRO nennt 70 cm für Wohngebäude bis 2 WE, Lifta/TK 80 cm; alle drei 100 cm für Mehr Wohneinheiten. Lifta formuliert "gesetzlich vorgeschrieben" — Artikel übernimmt die Pauschale bewusst als gekennzeichnete Herstellerangabe neben der behutsameren Fachportal-Einordnung.
3. **Restlaufbreite (Mehrfamilienhaus):** MVV TB (Muster): 100 cm nicht wesentlich einengen, 60 cm Restlaufbreite neben hochgeklapptem Sitz, Parkposition; verbindlich ist die Landesfassung. DIN 18065 (2020-08, Fachportalangabe): 800/1.000 mm.
4. **Klappmaß:** hochgeklappt 31–34 cm ab Wand (Acorn 130/180) — unterhalb der 60-cm-Referenz.
5. **Messregeln:** engste Stelle (Treppenauge, Handlauf, Heizkörper, Fensterbank, Türzarge), lichte Weite Wand → Handlauf-Innenkante; "Ein Wert, der zehn Zentimeter zu großzügig gemessen ist, kippt die ganze Planung."; Wendel: engste Stelle im Kurvenbereich.
6. **Steigung:** max. veröffentlichte Werte 70° (Lehner NEO) / 72° (Access BDD Flow X); bei Steilen wird der Ein-/Ausstieg oben zum Engpass.
7. **Platzhelfer:** Schienenseite (Freecurve 69/77 cm, Händlerangabe), Fahrt-Drehsitz, Klappschiene (Aufpreis nicht veröffentlicht → im Angebot einzeln ausweisen), Parkposition.
8. **Alternativen:** Stehlift (weniger Tiefe, nur bei sicherem Stehen → Arzt/Pflegeberatung), Plattformlift 90–110 cm + 120–140 cm Platz davor (Lifta), Preis 11.000–38.000 € (HIRO); unter 61 cm kein veröffentlichter Sitzlift-Wert; Treppensteiger/Deckenlift/Hauslift.
9. **Preise:** Preislisten differenzieren nach Treppenform/Etagen/Einbauort, NICHT nach Breite; HIRO gerade 4.000–10.000 €, kurvig 9.000–17.000 € (Stand Okt 2026); VZ-Rahmen 3.500–15.000 €.
10. **Förderung:** nur als Verweis auf den eigenen Zuschuss-Ratgeber — keine Beträge hier wiederholt (dort am 26.10. live verifiziert); VZ: Kostenvoranschlag vor der Maßnahme einreichen, Umbau erst nach Bewilligung.

## Quellenkette (Abrufe 26.10.2026)
- VZ Planung: verbraucherzentrale.de/...treppenlifte-das-muessen-sie-ueber-planung-und-umsetzung-wissen-10711 → Evidence `vz-planung.txt`, 9 Zitate.
- Treppenliftwissen (Fachportal-Erhebung 07.10.2026): treppenliftwissen.de/treppenlift/schmale-treppe/ → Evidence `tlw-schmale-treppe.txt`, 20 Zitate (inkl. Methodik-Satz "Keinen der Lifte haben wir selbst eingebaut oder gefahren").
- Altersgerecht Modernisieren (17.08.2026): altersgerecht-modernisieren.de/treppenlift/schmale-treppen/ → Evidence `am-schmale-treppen.txt`, 8 Zitate.
- Lifta (Hersteller): lifta.de/treppenlift/schmale-treppe → Evidence `lifta-schmale-treppe.txt`, 7 Zitate.
- HIRO (Hersteller): hiro.de/preise/ → Evidence `hiro-preise.txt`, 4 Zitate.
- Ledger: `research/schmale-treppe-261026-ledger.json` · Verifizierer: `research/verify_schmale_treppe_261026.py` (**53/53 PASS**, inkl. Einheiten-Arithmetik 800 mm=80 cm u. a.).
- Fetch-Skripte: research/fetch_schmale_261026.py, research/fetch_schmale_manu_261026.py (Hersteller primär).

## Grafik
`assets/images/treppenlift-schmale-treppe-messplan.svg` (980×680): Draufsicht Treppe (Wand links/Handlauf rechts) mit 3 Messwerten (lichte Weite, Klappmaß 31–34 cm, Restlaufbreite), engste-Stelle-Marker am Treppenauge, 3 Karten (messen → Klappmaß/Restbreite → Aufmaß terminieren) + Warnbox (Hersteller-/Fachportalangaben, Aufmaß entscheidet). Umlaut-freie Texte (Projektkonvention). **Sichtkontrolle:** getBBox-Overflow-Check 0 Elemente außerhalb der viewBox (`research/svg_shot_schmale_261026.mjs`), Vision-Sichtprobe "keine Auffälligkeiten". Evidence: `research/evidence/schmale-treppe-261026/svg-vollansicht.png`, `mobile-artikel.png`.

## Gates (alle in diesem Lauf, LAUNCH-Build)
- npm test (beide Build-Modi + test_site + test_articles + measurement + Playwright + test:partner): **Playwright 20 passed, test:partner ALL PASS (A2 ≥ 22)**; test_site nach LAUNCH-Rebuild PASS (**46 HTML-Seiten**), test_articles PASS (**22 Artikel**, Anker/Bilder/JSON-LD/SVG-XML).
- verify_checklists_build.py ALL PASS (RSS **22 Items**, Sitemap enthält Artikel, llms deckt alle ab).
- Content-Support-Gate `research/verify_schmale_treppe_content_261026.py`: jeder Key des Artikel-JSON (Intro, Abschnitte, Bullets, FAQs) im gebauten HTML; [1]–[5] auflösen, alle 5 Quellen zitiert; Related-Links 3× treppenlift-Cluster; Early-CTA compare_top → "Anbieter für Aufmaß vergleichen" → treppenlift-firmen-vergleich; Checklisten-Anker #abschnitt-8 existiert. **88 Checks ALL PASS.** (Neue Lektion: Zitations-sup-Anker unterbrechen den Fließtext — Vergleiche laufen jetzt tags- und citation-normalisiert, siehe Skript.)
- Mobile 390 px (Playwright-Chromium, `research/browser_check_schmale_261026.mjs`): 0 px Overflow, 5 Quellen/Grafik(346 px)/6 FAQs, Checklisten-Anker erreicht, related 3× lift. Chrome headless segfaultet im Cron (bekannt) → Chromium.
- Renderer: specialMap-Eintrag treppenlift-schmale-treppe → treppenlift-firmen-vergleich; llms-txt.py SUMMARIES + SECTION_MAP erweitert.
- Testzähler angehoben (gleicher Commit wie die Artikel, die sie zählen): test_articles 21→**22**; verify_checklists_build RSS 21→**22**; test_partner_links A2 ≥ 21→**22**.

## Wartungs-Trigger
- Hersteller-Mindestbreiten ändern sich: Beim nächsten Content-Refresh die 61/70/80/100-cm-Werte gegen die Herstellerseiten (Access BDD, TK, Lehner, Acorn, Lifta, HIRO) prüfen; Erhebungsdatum des Fachportals war 07.10.2026.
- Wenn der KfW-455-B-Stopp endet oder die Pflegekassenbeträge sich ändern: nur im Zuschuss-Ratgeber (dort verifiziert), dieser Artikel verweist nur.

## Notizen für künftige Läufe
- Terminal-Ausgaben in diesem Cron sanitizen offenbar bestimmte String-Kombinationen zu `***` (Schema-@context erschien kaputt, war per json.loads aber valide). Bei Verdacht auf korrupte Strings: mit Python json.loads/repr gegen die Datei prüfen, nicht auf grep-Ausgabe vertrauen.
