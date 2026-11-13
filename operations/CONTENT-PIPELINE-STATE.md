# Content-Pipeline-State — ZuhauseBleiben Kompass

Letzte Aktualisierung: 2026-11-13 (Nachmittag: Batch 23 — Region NRW als erste Region ausgebaut und live; vormittags Briefing 26 Hausnotruf-Alarm-Ablauf — 37. Ratgeber). Diese Datei ist das Produktionslog der Content-Pipeline. Sie ersetzt keine Freigabe; Launch-Modus ist aktiv (index), Formular bleibt deaktiviert.

### Batch 23 (2026-11-13, Cron-Lauf Nachmittag) — Region NRW (kein neuer Ratgeber; erste echte Region)

1. **Neu live:** region/nordrhein-westfalen.html (index,follow, Sitemap-Slot 49) — vier Förderwege: Pflegekasse (nur Verweise, 0 Beträge), NRW.BANK Eigentumsförderung – Modernisierung (Darlehen bis 220.000 € / 100 % / 30 J. fest / Tilgungsnachlass bis 50 %; § 13-WFNG-Grenzen-Tabelle; „anrechenfreie Beträge“ verbatim), Eingliederungshilfe LVR/LWL Leistungen für Wohnraum (Treppenlifter-Liste + § 64e verbatim; 2-Wochen-Zuständigkeitsprüfung; Kreis-RE-Pflegekasse-zuerst als markiertes Praxis-Beispiel), KfW-Stand 13.11. live (455-B gestoppt-Wortlaut, Kredit 159, Neustart 08.04.2026; NRW.BANK-Spiegel ohne Stopphinweis → Stale-Warnung auf der Seite). Plus Wohnberatung NRW, Mieter-Section (bundesweit abgegrenzt), 4 FAQs, Reihenfolgen-Checkliste, 10 Quellen geprüft 13.11.2026.
2. **Renderer:** generate.mjs Region-Loop datengetrieben (`data/region-<slug>.json` load-if-exists): Region mit Daten → Default-Robots (LAUNCH index, PREVIEW auto-noindex) + Sitemap via strukturellen Filter; ohne Daten → Platzhalter noindex,follow. Hub-Karte: echter NRW-Teaser, Hub bleibt noindex. test_site: NRW-MUSS-indexable-Assert + „genau eine Region in der Sitemap“ (Hub/Platzhalter draußen) — Fix-#5-Regel für die übrigen 11 Regionen unverändert.
3. **Gates/Tests:** Ledger 53/53 verbatim (research/region-nrw-131126-ledger.json + verify_region_nrw_131126.py; Evidenz research/evidence/region-nrw-131126/, Roh-HTML uncommitted); Content-Gate 71 Checks ALL PASS (verify_region_nrw_content_131126.py: Needles/Absenzen inkl. 0× 4.180/0× awin/0× sponsored, Related-Cluster, Quellen, Anker); npm test EXIT 0 (62 Seiten, 49 locs, Playwright, Partner A–F); Mobile 390 px 0 px Overflow (Tabellen im Scroll-Container), Desktop-Sichtkontrolle sauber; Deploy fe7f225, CI 43436255111 success, Live-Readback 38/38 ALL PASS (verify_region_nrw_live_131126.py), IndexNow 200.
4. **Muster etabliert:** nächste Region erst nach demselben Gate-Stapel (10+ offizielle Quellen verbatim, expand-or-noindex, Content-Gate, Live-Readback). Kein Regionen-Serien-Template (doorway-Regel).
5. **Refresh-Kandidat NEU:** (a) KfW-455-B: Wiederaufnahme für 2027 nur conditional — beim Bundeshaushalt-2027-Abschluss/KfW-News erneut prüfen (Evidenz kfw-455-live.txt + 2 News). (b) WFNG-§13-Einkommensgrenzen (Tabelle auf der NRW-Seite): jährliche Anpassung prüfen (.checked_at 13.11.2026). Bestehende Offenen unverändert (ADCELL-GO, Liftstar-Follow-up, Awin-Login-Status, GSC-Sitzung).

### Batch 22 (2026-11-13, Cron-Lauf) — Briefing 26: Hausnotruf-Alarm-Ablauf

1. **Neu veröffentlicht:** hausnotruf-alarm-ablauf.json (37. Ratgeber) — Care-Journey nach Batch-21-Vorgabe, Cluster mit zugelassenem Partner (Malteser, beratungstermin-Placement jetzt auf 3 Artikeln). Inhalt: Alarmkette Knopf→Zentrale→Sprechkontakt→Verzweigung (medizinischer Notfall → Rettungsdienst sofort vs. Alarmplan), stiller Alarm (Herstellerangabe „in jedem Fall Bereitschafts- oder Rettungsdienst", DRK „kommt immer jemand"), Maßnahmenplan inkl. Grenze („ersetzt nicht die individuelle Einschätzung") + freiwillige Krankheitsangaben, Fehlalarm/Probealarm (80 %, „Lieber einmal zu oft als einmal zu wenig", Absenz von Fehlalarm-Gebühren dokumentiert), Zentrale-Zeiten als Zentrumsangabe (30 s Ziel/94 % DRK Sachsen) + Verbandskontext (11.000 Rufe/3.600 Einsätze/Tag, 1,2 Mio Nutzer), BGH III ZR 92/16 (Leitsatz, Entlastungsbeweis § 280 Abs. 1 Satz 2 BGB, 16-Stunden-Erste-Hilfe-Ausbildung als Vertragsdetail) als Qualitätsfrage, 10-Punkte-Checkliste, 6 FAQs. 9 Quellen, 54/54 Zitate verbatim (`research/alarm-ablauf-131126-ledger.json`), Protokoll `research/hausnotruf-alarm-ablauf-batch.md`, Evidence `research/evidence/alarm-131126/`.
2. Renderer: specialMap +1 (Early-CTA → hausnotruf-kosten-anbieter-vergleich). llms-txt.py: Summary + Section +1. Zähler: test_articles 37, verify_checklists_build RSS 37 (Sitemap dynamisch 48 locs).
3. Gates: npm test EXIT 0 (62 Seiten/37 Artikel, Playwright 21, Partner A–F), verify_checklists_build ALL PASS, SVG-Gate 33/33 + Vision, Artikel-Akzeptanz 90/90 (Content-Support/Needles/Quellen/Placement/CTA/Related), Mobile 390px 0px Overflow.

## Bestand

### Batch 21 (2026-11-12, Cron-Lauf Nachmittag) — Briefing 25: Treppenlift-Aufmaß-Termin
1. **Neu veröffentlicht:** treppenlift-aufmass-termin.json (36. Ratgeber) — die letzte unbesetzte Journey-Stufe des Lift-Clusters (Auswahl ✓ → **Aufmaß ✗** → Angebot/Vertrag ✓ → Finanzierung ✓). 8 Abschnitte: Kurz beantwortet (Aufmaß = kostenloses Vermessen → schriftliches Festpreis-Angebot; unverbindlich mit Bedenkzeit); Warum erst nach Aufmaß (Schiene individuell vermessen, „Aufmaß vor Ort statt Preis nach Foto oder Telefonat bei kurvigen Treppen“, VZ-Festpreis-Empfehlung); Ablauf + Dauern (Vorab-Angebot „innerhalb von 24 Stunden“ → Vermessung → Festpreis; Montage 2–3 h gerade / max. 5 h kurvig [Lifta], „halber Tag“ [FAQ], „meist an einem Tag“ [Händler]; Schiene auf Stufen, nicht Wand; digitales Aufmaß — „Der Vor-Ort-Termin wird nicht ersetzt“); Vorbereitung (Pflegegrad-Bescheid/Antragsstand, Vermieter/WEA-Zustimmung VOR Termin, Steckdosen, Linienführung „Lassen sich Türen öffnen, bleibt genug Platz zum Gehen für den Rollator“ aus der VZ-Umfrage, Fragenliste + Vorbereitungs-Tabelle); 125-Bögen-Erfahrung (⅓ sofort unterschrieben [43+81+1=125], ⅓ ohne Widerrufs-/AGB-Info [83+37+5=125], 46/123 ohne Planungsunterlagen, „Rabatte, die nur am selben Abend gelten“ als dokumentiertes Druckmuster); Widerruf + Festpreis (§ 312g Abs. 1 verbatim, Werkvertrag/BGH, 12M+14T ohne Belehrung, Abs.-2-Nr.-1-Maßanfertigungs-Ausnahme für die Maßschiene EHRlich, +20-%-Kostenvoranschlagshinweis VZ, Zahlung erst bei Prüfbescheinigung + mängelfreier Funktion); Angebotsprüfung Position für Position (Festpreis inkl. Montage, Modell/Hersteller, Lieferzeit+Einbaudauer, Gewährleistung/Wartung, Elektroarbeiten, „nur mit gleichem Leistungsumfang vergleichen“, „Das Angebot eignet sich als Kostenvoranschlag für die Pflegekasse“ als Händlerangabe); 10-Punkte-Checkliste (Anker abschnitt-8). **Bewusst 0×:** Förderbeträge (4.180/16.720), KfW, €-Beträge, Partner-Marker.
2. **SERP-Gates (GSC im Cron weiter ohne Google-Sitzung):** 0/10 dedizierte Verbraucher-Guides zum Aufmaß-Termin; 5/10 Händler-/Hersteller-Seiten mit Interessenkonflikt (ts-treppenlifte, baethe, sonilift, siemer, lifta), 1 VZ-Journey-Artikel (Planung gesamt, KEIN Aufmaß-Protokoll — grep: 0 „Aufmaß“-Treffer), 1 CHIP-Unternehmensportrait. **Verworfen mit Beleg:** Plattformlift/Rollstuhllift (bereits im Bestand: treppenlift-plattformlift-rollstuhllift.json, 26 Rollstuhl-Mentions + SERP 10/10 dicht), Treppenlift verkaufen (pflege-panorama dedizierter 2026-Guide + 4 Teil-Sektionen + Ankauf-Händler-Dominanz, kein Payable-Event), Demenz-Wohnanpassung (gesund.bund.de + VZ 24.04.2026 + AOK + pflege.de + Wohnberatung dicht institutionell). Kanibalisierungs-Gate: „Aufmaß“ im Bestand nur Nebenrolle (schmale-treppe 13× Selbstmessung, firmen-vergleich 3× Firmenwahl). Details research/treppenlift-aufmass-termin-batch.md.
3. **Ledger 68/68 Pässe** (research/aufmass-121126-ledger.json + verify_aufmass_121126.py): 33 Verbatim-Zitate über 8 Quellen (VZ Planung Stand 20.01.2026, VZ-Umfrage-PDF 10.12.2020 [125 Bögen, dieselbe Primärquelle wie unserioese — heute frisch gegen die PDF-Extraktion verbatim], § 312g BGB gesetze-im-internet, ts-treppenlifte Stand November 2026, Lifta Hauptseite + FAQ, Bäthe, CHIP/Brandenburg-Liftsysteme) + 3 Arithmetik + 4 Absenzen. Händler-/Herstellerangaben im Artikel als solche gekennzeichnet. Evidenz research/evidence/aufmass-121126/ (12 Extrakte + SVG-Screenshot; Roh-HTML/PDF uncommitted).
4. **Renderer/Config:** specialMap +1 (Early-CTA „Anbieter für Aufmaß vergleichen“ → treppenlift-firmen-vergleich — identisches Label wie schmale-treppe, bewusst konsistent); cross-links.json links+rationale (angebote-vergleichen, unserioese, schmale-treppe — lift-intern); llms SUMMARIES + SECTION_MAP +1. Lift-Cluster via Slug-Präfix automatisch. Testzähler: test_articles 35→36, RSS 35→36, Partner A3 ≥34→≥35.
5. **Teststand:** npm test EXIT 0 (PREVIEW+LAUNCH 56 Seiten, test_articles 36, cross_links 36, titles, Playwright 21 passed, Partner A–F ALL PASS), danach build:launch; Content-Gate 0 FAILS (LAUNCH-dist; alle JSON-Keys inkl. table-cells, 2 Lead-Absätze, Related-Reihenfolge, CTA+Anker abschnitt-8, 7 Absenz-Needles inkl. 0× „€“); SVG 20/20 (getBBox 17 Texte, pairwise Text-Text 0, Text-Chip 0, Vision-Sichtkontrolle sauber — Screenshot in Evidenz); Mobile 390 px 0 px. Deploy: CI-Run 43231174256 success auf b07a856, **Live-Readback 30/30 ALL PASS** (robots index,follow, 10 Kernwortlaute live, Related-Reihenfolge, Early-CTA, SVG 200, Sitemap exakt 47 locs, RSS 36, Homepage, llms, 0 Partner-Marker/€/Förderbeträge live), IndexNow 200.
6. **Journey-Status:** Lift-Cluster damit komplett (Kosten, Firmen, Aufmaß, Angebote, Widerruf/Druck, Finanzierung, Steuer, Gebraucht, Miete, Förderung mit/ohne Pflegegrad, Außen, Schmal, Sitz/Steh, Plattform, unseriös). Nächste Content-Einheiten bevorzugt Care-/Wohn-Journey; dokumentierter Kandidat: Region-Ausbau mit verifizierten Landesprogrammen (doorway-Regel, eine Region vollständig).

### Batch 20 (2026-11-12, Cron-Lauf) — Briefing 24: Wohnung nach Krankenhausentlassung anpassen
1. **Neu veröffentlicht:** wohnung-anpassen-nach-krankenhausentlassung.json (35. Ratgeber) — Krankenhaus-Übergangs-Journey in drei Zeithorizonten: Im Krankenhaus Entlassmanagement (§ 39 Abs. 1a SGB V; Anspruch ggü. Krankenhaus vs. „nur" Unterstützung durch Kasse, Rahmenvertrag i. d. F. der 14. ÄndVb 19.11.2025; Einwilligung schriftlich/elektronisch; Übergangs-Verordnungen bis zu 7 Tage), Pflegebegutachtung im Krankenhaus (§ 18a Abs. 5: binnen 5 Arbeitstagen bei Weiterversorgungs-Hinweis; Auftrag 3 AT; verkürzt = min. PG 2 + Nachholung; 10-AT-Klausel bei Kurzzeitpflege-Anschluss), Bescheidfrist § 18c 25 AT ≈ 5 Wochen (Arithmetik 25/5=5); Erste Tage: Verordnungen einlösen, Kurzzeitpflege § 42 (nur PG 2–5, Übergangszeit, 8 Wochen/Jahr), Hausnotruf als baulose Absicherung (nur Verweis); Wochen-Monate: Wohnumfeld-Route § 40 Abs. 4 (subsidiär/Ermessen) + Abs. 7 Entscheidungsfrist 3/5 Wochen, Antrag VOR Umbau; Sozialdienst (AOK-Verbatim inkl. Selbst-ansprechen-Fall) + Pflegeberatung § 7a + EUTB § 32 SGB IX; 10-Punkte-Reihenfolge-Checkliste; 2 Fehlannahmen („KH organisiert alles" — VdK 100+ Berichte + Bentele-Verbatim; „EM zahlt den Umbau" — nein, separate Trägerrouten); Hilfsmittel-Grenze § 47 SGB IX („getragen oder mitgeführt oder bei einem Wohnungswechsel mitgenommen") schließt festen Lift aus — Refresh-Validierung von Briefing 23 gegen den Live-Text. Förderbeträge bewusst 0× im HTML (4.180/16.720), KfW 0×, Treppenlift-Preise 0×; kein Partner-Placement (CTA „Wohnumfeld-Zuschuss beantragen" → wohnumfeldverbesserung-beantragen via specialMap). 8 Abschnitte, 6 FAQs, 16 Quellen.
2. **SERP-Gates (GSC im Cron weiter ohne Google-Sitzung):** Bestand-Lücke grep-geprüft („Entlass" 1 Marginahinweis, § 18a/§ 18c/39a 0×); SERP-Feld organisch nur generische Barrierefrei-Portale + 1 Schlaganfall-Artikel; **Konkurrenz-Gap skriptgeprüft: pflege-panorama-Schlaganfall 0× „Entlassmanagement"** (Ledger-Absenz x5); Institutionenseiten dicht, aber journey-los. Details research/wohnung-anpassen-nach-krankenhausentlassung-batch.md.
3. **Ledger 84/84 Pässe** (research/krankenhaus-121126-ledger.json + verify_krankenhaus_121126.py): 24 Verbatim-Zitate über 16 Quellen (gesetze-im-internet SGB V § 39, SGB XI §§ 18/18a/18c/7a/40/42, SGB IX §§ 32/47 — § 47 heute frisch geholt, „tragbar/mitnehmbar"-Erinnerung als exaktes „getragen oder mitgeführt oder … mitgenommen" verifiziert; BMG; Rahmenvertrag-PDF 14. ÄndVb mit Dehyphenation; gesund.bund.de; VZ; AOK; VdK; pflege-panorama als Gap-Beleg) + Arithmetik + 5 Absenzen. Evidenz research/evidence/krankenhaus-121126/ (Roh-HTML/PDF uncommitted).
4. **Renderer-Fix vorab (eigener Commit 94556ac):** LIVE-Fehler — Array-Intros wurden komma-splizt in EINEN Lead-Absatz ohne Leerzeichen („…nutzen kann.,Dieser Ratgeber…", 6 Artikel live betroffen). Fix: Array-Intros als eigene `<p class="lead">`-Absätze + `.lead+.lead`-Margin; npm test EXIT 0 vor dem Push; Junction-Check 6/6 sauber.
5. **Renderer/Config:** isCare-Regex + „wohnung-anpassen" in BEIDEN Stellen (article-renderer.mjs + test_cross_links.py — Zwei-Stellen-Regel beachtet); specialMap +1; cross-links.json links+rationale (Whitelist 2× Lift-Cross: foerderung-ohne-pflegegrad + mieten, care-pool: hausnotruf-kosten); llms SUMMARIES + SECTION_MAP +1. Testzähler: test_articles 34→35, RSS 34→35, Partner A3 ≥33→≥34.
6. **Teststand:** npm test EXIT 0 (PREVIEW+LAUNCH 60 Seiten/46 locs, test_articles 35, cross_links 35, titles 0 Verletzungen, Playwright 21 passed, Partner A–F ALL PASS), danach build:launch; Content-Gate 135/135 (alle JSON-Keys inkl. table-cells, 2 Lead-Absätze, Related-Reihenfolge, CTA+Anker, SVG/alt/KI-Label, 7 Absenz-Needles); SVG getBBox 51 Elemente 0 Overflows + Pairwise 0 + Vision sauber; Mobile 390 px 0 px. Deploy: CI success auf 424d925, **Live-Readback 54/54 ALL PASS** (robots index,follow, 8 Kernzahlen 2 Runden × 2 Abrufe, 6 Absenzen live 0×, 2 Lead-Absätze, Related-Reihenfolge, SVG 200, Sitemap exakt 46 locs, RSS 35, Homepage-Link, llms), IndexNow 200. HINWEIS: Push trug den parallelen Docs-Commit a38e2cc (Partner-Enquiries 12.11, 3 txt) mit — legitim, docs-only.
7. **Refresh-Kandidat NEU:** Rahmenvertrag Entlassmanagement — 14. ÄndVb (19.11.2025) ist aktueller Lesefassungs-Stand; bei 15. Änderung den Absatz „Anspruch ggü. Krankenhaus vs. Kasse" re-prüfen. Bestehende Offenen (ADCELL-GO, Liftstar-Follow-up, Awin-Login-Status) unverändert.

### Batch 19 (2026-11-11, Cron-Lauf) — Briefing 23: Treppenlift-Förderung ohne Pflegegrad
1. **Neu veröffentlicht:** treppenlift-foerderung-ohne-pflegegrad.json (34. Ratgeber) — die drei realen Wege mit gesetzlicher Grundlage: Eingliederungshilfe/Soziale Teilhabe (§§ 113/77 SGB IX „Leistungen für Wohnraum" inkl. Umbau; § 99 wesentliche Behinderung + Abs.-3-Kann-Leistung; § 2 Behinderungsbegriff 6 Monate/Barrieren-Wechselwirkung; Schwerbehindertenausweis im Wortlaut NICHT Voraussetzung), Unfallversicherung (§ 26 SGB VII Soziale Teilhabe + „Hilfen … zur Führung eines möglichst selbständigen Lebens"; DGUV benennt Wohnen/Mobilität; § 66 SGB XIV analog), Sozialamt (§ 64e SGB XII mit § 61a-Pflegebedürftigkeitsbegriff inkl. wörtlichem „Treppensteigen"-Kriterium + § 2 Nachrang). Detailtiefe, die keine Konkurrenz-Seite dokumentiert: Beitragseinkommen = Vorvorjahr (§ 135), 85/75/60-%-Schwellen je Einkunftsart (§ 136), 150-%-Barvermögensschutz (§ 139), Darlehen statt Zuschuss möglich (§ 140), Gesamtplanverfahren mit Pflegekassen-Beteiligung (§ 117 Abs. 3), ICF-Bedarfsermittlung Mobilität/häusliches Leben (§ 118), Persönliches Budget mit 6-Monats-Bindung (§ 29), EUTB vor dem Antrag (§ 32). Zwei Fehlannahmen-Kapitel: DRV listet in § 9 SGB VI KEINE Soziale Teilhabe + Wohnungshilfen nur „vor der Haus- bzw. vor der Wohnungstür" (DRV-Verbatim); Hilfsmittel-Definition § 47 (tragbar/mitnehmbar) schließt festen Lift aus → ohne Pflegegrad keine Kassen-Route. Reform sauber getrennt: Drs. 21/8869 (02.11.2026, NICHT beschlossen) § 15-Schwelle „15 bis unter 30 Gesamtpunkten" + § 142b Bestandsschutz + BMG „Reha vor Pflege"; 2026er Anträge laufen nach alter Systematik. 10 Abschnitte, 6 FAQs, 28 Quellen; Pflegekassen-Beträge bewusst 0× im HTML (Verweis auf zuschuss-Ratgeber); kein Partner-Placement (CTA „Pflegekasse & KfW prüfen" → treppenlift-zuschuss).
2. **SERP-Gates (GSC im Cron weiter ohne Google-Sitzung):** Bestand-Lücke grep-geprüft (zuschuss-Artikel 0× Sozialamt/RV/SGB IX); SERP-Feld „ohne Pflegegrad" 10/10 Anbieter-/Broker-Seiten, mehrere mit falschen/stale KfW-Claims (455-B als lebend beschrieben, falscher 159-Programmname). Verworfen mit Beleg: Badumbau-Mietwohnung (§ 554/§ 20-WEG-Maschinerie liegt bei treppenlift-mietwohnung, bad-umbau hat eigenen Mietwohnungs-Abschnitt → Kannibalisierung), Umzug mit Lift (post-purchase, kein payable event). Details research/treppenlift-foerderung-ohne-pflegegrad-batch.md.
3. **Ledger 108/108 Pässe** (research/ohne-pflegegrad-111126-ledger.json + verify_ohne_pflegegrad_111126.py): 51 Verbatim-Zitate über 28 Quellen (15× gesetze-im-internet inkl. SGB IX 2018-Shortcode-Fund `sgb_9_2018` + SGB VI/VII/XII/XIV, DRV-berufliche-Reha, DGUV-Teilhabe, § 66 SGB XIV, § 61/61a/64e/2 SGB XII, Drs. 21/8869-PDF als dehyphenierte Evidenz + BMG-PM) + Kernzahlen + 5 Absenzen (0× 4.180/16.720, 0× „12,5"-NBA-Punktwert, 0× awin/sponsored). Evidenz research/evidence/ohne-pflegegrad-111126/ (37 txt + Screenshot; Roh-HTML/PDF uncommitted).
4. **Renderer:** article-renderer.mjs specialMap +1. data/cross-links.json links+rationale +1 (zuschuss, finanzierung, gebraucht-oder-neu — lift-intern). research/llms-txt.py SUMMARIES + SECTION_MAP (Treppenlift-Sektion) +1. isLift-Regex deckt den Slug via treppenlift-Präfix automatisch ab.
5. **Testzähler:** test_articles.py 33→34; verify_checklists_build.py RSS 33→34; test_partner_links.py A3 ≥32→≥33. Neu: research/verify_ohne_pflegegrad_{111126,content_111126,svg_mobile_111126,live_111126}.py + wait_ci_ohne_pflegegrad_111126.py + indexnow_submit_ohne_pflegegrad_111126.py + 8 fetch/check/inspect-Skripte. 1 Gate-Loop: description 166>160 → 154 (test_titles_meta grün).
6. **Teststand:** npm test EXIT 0 (test_site 59 Seiten/45 locs, test_articles 34, Playwright 21 passed, Partner A–F ALL PASS), Content-Gate 0 FAILS (LAUNCH-dist), SVG getBBox+Pairwise+Chip 0 Issues, Vision-Sichtkontrolle ohne Defekte, Mobile 390 px 0 px. Deploy: CI-Run 42992901718 success, **Live-Readback 40/40 ALL PASS** auf der öffentlichen URL (robots index,follow, 15 Kernzahl-Wortlaute, CTA, SVG 200, Sitemap exakt 45 locs, RSS 34, Homepage, llms), IndexNow 200.
7. **Refresh-Kandidat NEU (zwei Trigger):** (a) PNOG-Verabschiedung → Status-Absatz + die 4 pflegebezogenen Bestandsartikel (zuschuss, wohnumfeldverbesserung-beantragen, pflegegrad-antrag-ablauf-fristen, verhinderungspflege-tagespflege-ueberblick) gegen neues Recht re-prüfen (Bestandsschutz + „Reha vor Pflege" beachten). (b) BMG „Reha vor Pflege"-Konkretisierung könnte Kassen-Reha-Route für Umbauten stärken — beim Inkrafttreten erneut lesen. Bestehende Offenen (ADCELL-GO, Liftstar-Follow-up, Awin-Login-Status) unverändert.

### Batch 18 (2026-11-10, Cron-Lauf) — Briefing 22: Unseriöse Treppenlift-Anbieter erkennen
1. **Neu veröffentlicht:** treppenlift-unserioese-anbieter.json — Verkaufstaktiken + Rechte + Fall: 3 Kernwarnsignale (Zeitdruck/„nur kurzfristig drin"-Anfahrt-Behauptung, unterschobener Widerrufs-Verzicht inkl. Kundenstimme „An keiner Stelle war erkennbar…", Anzahlung ohne Besichtigung/Voranschlag „höchste Vorsicht geboten"), VZ-Betroffenen-Umfrage (125 Bögen/16 Länder, 12/2020: ⅓ sofort unterschrieben, ⅓ ohne ausreichende Widerrufs-/AGB-Info, 46/123 ohne Planungsunterlagen, „rund ein Viertel" gebrochene Werbeversprechen, „Abzocke"-Benennung für Wartungsverträge, Fünf-Marken-Fazit „PractiComfort (jetzt: mobilae)") MIT Methodik-Caveat (nur gemeldete Problemfälle), Taktik→Gesetz-Mapping (§ 4a UWG Aggressivität + Alter/Beeinträchtigung-Satz, § 7 UWG Telefonanruf ohne ausdrückliche Einwilligung „stets anzunehmen", § 5a UWG Unterlassen + kommerzieller Zweck kenntlich, § 312g BGB mit Abs.-2-Nr.-1-Grenze → Verweis finanzierung), Verbandsklage-Fall (VZ-BW vs. Mobilae GmbH Neuss, OLG Hamm, 8.10.2026, AZ I-13 UKl 17/26, 18 Klauseln programmatisch gezählt: Gewährleistungsausschluss, 65 %/25 %-Bruttoauftragssummen-Pauschalen, Datenweitergabe-Klausel, „Wir verarbeiten die Daten nach EUDGV.") MIT Unschuldsvermutung („Erst der weitere Verlauf des Verfahrens…"), Rechte-kompakt (Werkvertrag/BGH, 12M+14T, Zahlungsregel „erst wenn eingebaut und funktionstüchtig", Mängel 2 Jahre, Festpreis + 20-%-Hinweis-Schwelle) + 10-Punkte-Checkliste. 10 Abschnitte, 6 FAQs, 9 Quellen; Förderbeträge bewusst NICHT wiederholt (HTML-Gate 0 × „4.180").
2. **SERP-Gates (GSC im Cron weiter ohne Google-Sitzung):** exakte Intent (Kaltakquise/Fangprämie/Verkaufsdruck) hat 0 dedizierte Konkurrenz-Ratgeber — organisch nur test.de-Unterseite (sichtbar), 2–3 Anbieter-Magazine mit Interessenkonflikt, 1 Forum, davor 4 Ads; frischer Klausel-Fall (5 Tage alt) nur bei Anbieter-News/Forum; Bestand: Taktik-Winkel 0 Abschnitte (Klausel-Winkel liegt bei treppenlift-mieten — abgegrenzt). Verworfen: Pflegebett Kostenübernahme (SERP 8/10 institutionell dicht, Bestand deckt Route). Details research/treppenlift-unserioese-anbieter-batch.md.
3. **Ledger 105/105 Pässe** (research/unserioese-101126-ledger.json + verify_unserioese_101126.py): 62 Verbatim-Zitate über 9 Quellen (VZ 10711, VZ-Umfrage-PDF, test.de-Unterseite, VZ-Verbandsklage-Seite, vsforum, §§ 4a/5a/7 UWG + § 312g BGB) + 4 Umfrage-Chart-Arithmetik-Zeilen (83+37+5 / 43+81+1 / 29+93+3 / 77+46+2 = je 125) + Klausel-Count 18 + Integrität + 24 Kernzahlen + 9 Absenzen (keine Firma wird als unseriös etikettiert, keine Förderbeträge, keine Empfehlungen). Evidenz research/evidence/unserioese-101126/ (10 txt + Screenshot; Roh-HTML/PDF uncommitted).
4. **Bewusst kein Partner-Placement** — Lift-Cluster hat keine aktiven Placements (HIRO 9440 wartet auf ADCELL-GO); CTA-Route über specialMap auf treppenlift-angebote-vergleichen („Angebote sauber vergleichen"). Content-Gate assertet 0 Partner-Marker + 0 awin + 0 rel=sponsored.
5. **Renderer:** article-renderer.mjs specialMap +1. data/cross-links.json links+rationale +1 (angebote-vergleichen, mieten, kosten — lift-intern). research/llms-txt.py SUMMARIES + SECTION_MAP (Treppenlift-Sektion) +1. isLift trifft via treppenlift-Präfix.
6. **Testzähler:** test_articles.py 32→33; verify_checklists_build.py RSS 32→33; test_partner_links.py A3 ≥31→≥32. Neu: research/verify_unserioese_{101126,content_101126,svg_mobile_101126}.py + fetch/strip/restrip/gen/overlap-Skripte. Grafik assets/images/treppenlift-unserioese-anbieter-warntafel.svg (6 Kacheln + Footer, getBBox+Pairwise+Chip 0 Issues, Vision sauber, Mobile 390 px 0 px). Protokoll research/treppenlift-unserioese-anbieter-batch.md.
7. **Teststand:** npm test EXIT 0 (test_site 58 Seiten/44 locs, test_articles 33, Playwright 21 passed, Partner A–F ALL PASS), Content-Gate 0 FAILS (LAUNCH-dist; Lektion: `from html import unescape` statt `html.unescape` am geschatteten String + `&`-Escape in Bullet-Vergleichen). Deploy/Live-Readback/IndexNow: siehe launch-state 10.11.
8. **Refresh-Kandidat:** Verbandsklage I-13 UKl 17/26 ist ein laufendes Verfahren — nach erstem Urteil/Beschluss Re-Prüfung des Fall-Abschnitts (Ledger-Notiz). Bestehende Offenen (ADCELL-GO, Liftstar-Follow-up, Awin-Login-Status) unverändert.

### Batch 17 (2026-11-10, Cron-Lauf) — Briefing 21: Hausnotruf für Angehörige einrichten
1. **Neu veröffentlicht:** hausnotruf-angehoerige-einrichten.json — Angehörigen-Journey (Erkennen → Gespräch → Rollen/Vollmacht → Pflegekassen-Route → Anbieter/Beratung → Einrichtung/Test → Ferne-Begleitung), SERP-basiert gewählt (GSC im Cron weiter ohne Google-Sitzung): 5/8 SERP-Treffer = Ads, organisch nur 2 dedizierte Seiten (HSP ×2-Domain + BeWo), beide Anbieter-Magazine mit Interessenkonflikt; Bestand deckte den Intent mit 0 Abschnitten (grep-geprüft über alle 31 Artikel). Kernbefunde 117/117 Ledger-Pässe = 84 Verbatim-Zitate über 7 Quellen + 8 Artikel-Absenz-Checks + Integrität + Kernzahlen (research/angehoerige-101126-ledger.json + verify_angehoerige_101126.py, Evidenz research/evidence/angehoerige-101126/, Roh-HTML uncommitted): **4 Divergenzen dokumentiert** — D1 Vollmacht (HSP vage „kann eine Vollmacht erforderlich sein“ vs. notfallknopf spezifisch: Vorsorgevollmacht Vermögenssorge/Vertragsangelegenheiten, „Eine reine Gesundheitsvollmacht reicht dafür nicht aus“, Betreuer-Aufgabenkreis vs. BeWo „Vertrag als Angehörige anstoßen“), D2 Einrichtungsweg (Malteser Installation + persönliche Einweisung vs. BeWo funktionsfertig per SIM vs. VZ Leistungsanforderung „aufgestellt und eingerichtet“), D3 VZ-Zusatzleistungen intra-page „30 bis 50 Euro (oder auch mehr)“ vs. FAQ „30 bis 80 Euro“, D4 Kosten-Realismus (sanivia „0 € im Monat“ vs. VZ „bis zu 27 Euro“ + Voraussetzungen + MD-Prüfung vs. Malteser „27,00 € ab Pflegegrad 1“ mit eigener Einschränkung). Fristen: 3/5 Wochen Pflegekasse + „innerhalb einer Woche betriebsbereit“ (Kassenvertrag laut Portal), Versorgungsvertrag § 78 SGB XI + Vorleistungs-Frage, Zentrale-Daten (Adresse/Zugang, Gesundheitszustand/Medikamente, Kontaktdaten) + DSGVO, Demenz-Grenze (VZ) mit Mobil-GPS-Verweis, 10-Punkte-Checkliste. Zero-Arithmetik (alle Zahlen wörtliche Quellenangaben). 11 Abschnitte, 6 FAQs, 7 Quellen; Malteser nur Herstellerangabe.
2. **Bewusst kein Partner-Placement auf dem Artikel** — Placements leben exklusiv auf hausnotruf-kosten-anbieter-vergleich (Malteser aktiv, HIRO/Pflegehase warten auf ADCELL-GO); Early-CTA „Kosten & Anbieter vergleichen“ → hausnotruf-kosten-anbieter-vergleich (specialMap +1). Content-Gate assertet 0 Partner-Marker + 0 awin-Tracker + 0 Lift-CTA.
3. **Renderer:** article-renderer.mjs specialMap +1. data/cross-links.json links+rationale +1 (kosten-vergleich, schluesselhinterlegung, mobil-gps — care-intern). research/llms-txt.py SUMMARIES + SECTION_MAP (Hausnotruf-Sektion) +1. isCare-Regex trifft via hausnotruf-Präfix (keine Regex-Änderung).
4. **Testzähler:** test_articles.py 31→32; verify_checklists_build.py RSS 31→32; test_partner_links.py A3 ≥30→≥31. Neu: research/verify_angehoerige_{101126,content_101126,svg_mobile_101126}.py + strip/check-Skripte + Evidenz-Txt (7 Quellen). Grafik assets/images/hausnotruf-angehoerige-wegweiser.svg (5 nummerierte Schritte + Zeitfenster-Band, getBBox+Pairwise+Chip 0 Issues nach Fix — 1. Sichtkontrolle fand Schritt-3-Zeile hinter dem Chip, gekürzt; 2. Inspektion sauber, Mobile 390 px 0 px). Protokoll research/hausnotruf-angehoerige-einrichten-batch.md.
5. **Teststand:** npm test komplett grün EXIT 0 (test_site 57 Seiten, test_articles 32, cross_links, titles_meta nach Title-Kürzung 81→62/Desc 166→150, Playwright, Partner A–F ALL PASS). Content-Gate 117 PASS (LAUNCH-dist). Deploy/Live-Readback: siehe launch-state 10.11.
6. **Refresh-Kandidat:** keiner neu; bestehende Offenen (ADCELL-GO, Liftstar-Follow-up, Awin-Login-Status) unverändert. VZ-Fristen-/27-€-Angaben im Artikel mit checked_at 10.11.2026 datiert.

### Batch 16 (2026-11-09, Cron-Lauf) — Briefing 20: Treppenlift-Finanzierung
1. **Neu veröffentlicht:** treppenlift-finanzierung.json — Raten, Rechte und die Reform ab 20.11.2026, SERP-basiert gewählt (GSC im Cron weiter ohne Google-Sitzung): 8/10 Konkurrenz = Hersteller-/Händler-Selbstauskunft mit unverifizierbaren Konditionen, 1 Du-Form-Ratgeber mit Richtwerte-Disclaimer; Bestand deckte Ratenzahlung mit 1 Satz. Verworfen mit Beleg: Pflegegrad-Höherstufung (10/10 dicht, 4+ 2026-frisch, Kannibalisierungsrisiko mit pflegegrad-antrag), Duschsitz-Kassenübernahme (Small-Ticket, kein Payable-Event). Kernbefunden 70/70 Ledger-Pässe = 60 verbatim Zitate über 20 Quellen + 5 Lifta-Absenz-Patterns + 3 Arithmetik + BGBl-Titel + evz-Stand (research/verify_finanzierung_091126.py, Evidenz research/evidence/finanzierung-091126/, Roh-HTML uncommitted): **D5-Divergenzen** — Laufzeiten (TK 50/50 zinsfrei in 12 Monaten vs. HIRO easyCredit 2–60 [TeamBank AG] vs. Liftteam 12–60 vs. Lifta „individuell“), Betragsgrenze nur Liftteam („bis max. 10.000€“, auch nach Pflegekassenzuschuss-Abzug), Zinsausweis (TK/der-tl „0 %“, gebrauchtl „ohne Zinsen“, Lifta ohne Angabe), **der-tl Intra-Seiten-Widerspruch** („12 bis 60 Monate“ neben „Anzahlung von mind. 50 % ... auf 11 Teilzahlungen“), **Kredit-Reform ab 20.11.2026** (BGBl 2026 I Nr. 139, evz 30.10.2026: zinsfreie/Kleinst-/≤3-Monats-Kredite erfasst + Bonitätsprüfung + Datenschutz; Bundestag-Wortlaut; keine Konkurrenzseite kennt sie — Refresh-Trigger notiert), TK-KfW-Zins-Echo „ab 2,35 %“ (stale vs. gerenderte 3,19 %, bewusst nur Warnung), Snippet-Stale-Falle gebrauchtl („4000,- €“ Snippet vs. live 4.180 €). Rechte im Gesetzestext: § 491 (entgeltlich, <200-€-Ausnahme, ≤3 Monate), § 492 (Schriftform, Abschrift, Tilgungsplan), § 495 (Widerruf), § 356b (Fristbeginn erst mit Vertragsurkunde; 1 Monat bei Nachholung), § 500 Abs. 2 (Sondertilgung jederzeit), § 502 (Vorfälligkeit nur bei gebundenem Sollzins, max. 1 %/0,5 %), § 312g (Haustür-Widerruf; Abs. 2 Nr. 1 maßgefertigte Schiene ausgenommen) + 0-%-Nuance (VZ 14 T./≥200 €; vzhh § 356d 1J+14T.; vzbv „unentgeltlich/eingeschränkt“). Rechenbeispiel fiktiv deklariert (8.000 → 4.180 → 3.820 → 159,17 €/24 Mon.; 166,67 €/48 Mon., arithmetik-geprüft); SGB XI § 40-Grenze wörtlich („4 180 Euro je Maßnahme“); Förderbeträge bewusst nur als Verweis auf treppenlift-zuschuss. 10 Abschnitte, 6 FAQs, 20 Quellen.
2. **Bewusst kein Partner-Placement** — Lift-Cluster hat aktuell keine aktiven Placements (Lifta 40988 offen, HIRO 9440 wartet auf ADCELL-GO); Content-Gate assertet 0 Partner-Marker + 0 awin-Tracker. Early-CTA „Förderung zuerst prüfen“ → treppenlift-zuschuss (specialMap +1). Die Checkliste verlangt Betrags-/Laufzeit-/Zinsausweis-Grenzen aus dem konkreten Angebot statt Portal-Zahlen.
3. **Renderer:** article-renderer.mjs specialMap +1. research/llms-txt.py SUMMARIES + SECTION_MAP (Lift-Sektion) +1. isLift-Regex deckt den Slug automatisch ab. Kein cross-links-Eintrag nötig (Lift-Pool automatisch).
4. **Testzähler:** test_articles.py 30→31; verify_checklists_build.py RSS 30→31; test_partner_links.py A3 ≥29→≥30. Neu: research/verify_finanzierung_{091126,content_091126,svg_mobile_091126,live_091126}.py + fetch_finanzierung_091126.sh + strip_finanzierung_091126.py + indexnow_submit_finanzierung_091126.py + wait_ci_finanzierung_091126.py. Content-Gate-Lektion: citation-Strip auf `\[\d+\]` erweitert (Quellen >9 brachen den `\[\d\]`-Strip); Ledger-norm entfernt Strip-Artefakt-Leerzeichen vor Satzzeichen (Wortlaut unverändert). Grafik assets/images/treppenlift-finanzierung-wegweiser.svg (5 nummerierte Schritte + Legende, getBBox 0 Overflows + Pairwise 0 + Vision sauber, Mobile 390 px 0 px Overflow). Protokoll research/treppenlift-finanzierung-batch.md.
5. **Teststand:** npm test komplett grün (test_site 51 Seiten, test_articles 31, test_cross_links, test_titles_meta ALL PASS nach Desc-Kürzung 164→141, Playwright 21 passed, Partner A–F ALL PASS). Deploy: Commit 80501f7, CI 42629563205 success, Live-Readback 30/30 ALL PASS (Sitemap exakt 42 locs = LAUNCH-Referenz; erstes Readback-Fail war ein PREVIEW-dist-Zählartefakt, nicht die Live-Site), IndexNow 200.
6. **Refresh-Kandidat:** NEU — nach dem 20.11.2026 Reform-Abschnitt + §-491-Wortlaut gegen das neue Recht re-prüfen (VZ-Übergangsfragen dann gegen die neue Rechtslage). Bestehende Offenen (ADCELL-GO, Liftstar-Follow-up, Awin-Login-Status) unverändert.

### Batch 15 (2026-11-06, Cron-Lauf) — Briefing 19: Hausnotruf-Schlüsselhinterlegung
1. **Neu veröffentlicht:** hausnotruf-schluesselhinterlegung.json — die Schlüsselfrage vor Vertragsabschluss, SERP-basiert gewählt (GSC im Cron weiter ohne Google-Sitzung): organische Konkurrenz nur ~5–6 Seiten, davon 3 Anbieter-Magazine mit Interessenkonflikt; Bestand deckte den Intent mit 1 Satz. Verworfene Kandidaten mit Beleg: Kurzzeitpflege (7 dedizierte Ratgeber), Entlastungsbetrag (10+ Seiten + abgedeckte Sub-Winkel), Pflegezeit/Familienpflegezeit (6+ 2026-frische Ratgeber). Kernbefunde 99/99 Ledger-Pässe = 78 Zitate verbatim + 6 Absenz + 15 Artikel-Checks (research/schluessel-061126-ledger.json + verify_schluessel_061126.py): **Kosten-Divergenz dokumentiert** (Tresor einmalig 30 € [pflege-helfer24] vs. 35–100 € [easierLife]; Zentrale ~15 €/Monat vs. VZ „Zusatzleistungen … 30 bis 80 Euro"; Absenz-Checks: VZ 0× „15 Euro", 0× „Tresor"), **Pflegekasse ehrlich** (2 Portalangaben wiedergegeben; Gerät-vs.-Dienstleistungs-Abgrenzung ohne Beleg bewusst nicht behauptet), **Notfall-Strecke ohne Schlüssel** (Feuerwehr-Faustregel + Kommune-Divergenz + VG Gießen 2 K 2103/23.GI [test.de]; AG Hildburghausen 21 C 133/23 mit dem Vermieter-Argument „hätte die Tür mit einem hinterlegten Schlüssel öffnen können" + 2.957,21 € [Haufe]; AG Berlin-Mitte; VZ „fast 800 Euro"-Fall + Tageszeit-Divergenz), Erreichbarkeits-Grenzen + Kombi-Empfehlung, Einrichtungsgespräch-Checkliste, Datenschutz (kleiner Code-Kreis). 10 Abschnitte, 6 FAQs, 8 Quellen.
2. **Bewusst kein Partner-Placement auf dem Artikel** — Malteser nur als Herstellerangabe („auf Wunsch auch der Wohnungsschlüssel", Bereitschaft 365/24); Absenz skriptgeprüft: Malteser-Seite 0× Tresor / 0× Schlüsseldienst / 0× Hinterlegung → Tresor wird NICHT als Malteser-Option dargestellt. Placements leben exklusiv auf hausnotruf-kosten-anbieter-vergleich; CTA-Route über specialMap dorthin. Content-Gate assertet 0 Partner-Marker + 0 awin-Tracker.
3. **Renderer:** article-renderer.mjs specialMap +1 („Kosten & Anbieter vergleichen" → hausnotruf-kosten-anbieter-vergleich). data/cross-links.json links+rationale +1 (kosten-vergleich, sturzerkennung — care-intern). research/llms-txt.py SUMMARIES + SECTION_MAP +1. isCare trifft via hausnotruf-Präfix (keine Regex-Änderung).
4. **Testzähler:** test_articles 29→30 (Assert + RSS-Check); verify_checklists_build RSS 29→30; test_partner_links A3 ≥28→≥29. Neu: research/verify_schluessel_{061126,content_061126,svg_mobile_061126,live_061126}.py + evidence/schluessel-061126/ (7 Strip-/Extrakt-Skripte + 7 Evidenz-Txt; Roh-HTML uncommitted). Grafik assets/images/hausnotruf-schluessel-entscheidung.svg (4 Weg-Bänder + Kosten-Chips, getBBox 0 Overflows + Pairwise 0 + Chip-Kontext 0 + Vision sauber, Mobile 390 px 0 px). Protokoll research/hausnotruf-schluesselhinterlegung-batch.md.
5. **Teststand:** npm test EXIT 0 (Partner-Gates A–F ALL PASS; 1 bekannter Flaky-Consent-Keyboard-Fall solo re-geprüft PASS). Deploy: Commit d6e95a3, CI 42190782682 success, **Pages-Deploy-Lag ~2 min** (404→200 nach Poll), Live-Readback 41/41 ALL PASS auf der öffentlichen URL, IndexNow 200.
6. **Refresh-Kandidat notiert:** keiner neu; bestehende Offenen (ADCELL-GO, Liftstar-Follow-up, Awin-Login-Status) unverändert.

### Batch 14 (2026-11-06, Cron-Lauf) — Briefing 18: Sitzlift oder Stehlift
1. **Neu veröffentlicht:** treppenlift-sitzlift-oder-stehlift.json — Bauform-Wahl nach der PERSON (Treppe = Schiene, Person = Sitz/Stehplatz), SERP-basiert gewählt (GSC im Cron weiter ohne Google-Sitzung): organische Konkurrenz dünn (nur 2 Fachportale, davor Broker-Ads), intent-distinct (schmale-treppe behandelt die Treppenbreite, Bestand deckte Sitz-vs.-Steh nur mit 1 Satz). Kernbefunde 40 Zitate verbatim + 8 Absenz-Checks, 67/67 Ledger-Pässe (research/sitzsteh-061126-ledger.json + verify_sitzsteh_061126.py): Lifta-Stehlift-Wortlaut (Plattform/Stehplatte, Anlehn- vs. Sattelsitzlift-Mischform, „Gelenke nicht gänzlich beugen“, rutschfestes Fußbrett/sicherer Stand, Parkposition klappbar), Sitzlift als „gängigste Art“ mit Grenze „eigenständig aufsitzen/aufstehen“, Rollstuhl-Grenze beider Bauarten → Rollstuhl-/Plattformlift, **Absenz-Checks skriptgeprüft: HIRO (Produktseite+Preise) und TKE (Startseite+Modellübersicht) listen 0 × Stehlift** (Stehlift ist kein Standardartikel jedes Herstellers), Breiten-Divergenz dokumentiert statt Einzahl (Lifta 80 cm ≤2 WE vs. Fachportal „Mindestens 55 cm“ mit Stand-10/2025-„ohne Gewähr“-Hinweis; maßgeblich Aufmaß, Cross-Link Messanleitung schmale-treppe), Preis-Ehrlichkeit („kein pauschaler Preisvorteil seriös bezifferbar“ TLW + HIRO-Preistreiber Treppenform/Etagen/Einbauort ab ~4.000 € Herstellerangabe + „verbindlich ist das Angebot nach dem Aufmaß“), Angebots-Checkliste (Anchor „Zur Checkliste“) mit Ausführung/Bedienung/Probe/Umfang/Widerruf (VZ 14 T./Werkvertrag/12M+14T.)/Förderung-zuerst (nur Verweis, keine Beträge-Wiederholung). 8 Abschnitte, 6 FAQs, 8 Quellen; keine Arithmetik (alle Zahlen wörtliche Hersteller-/Portalangaben, im Ledger dokumentiert). Bewusst NICHT übernommen: HIRO-Förder-Claim („bezuschusst … bis 4.180 €“ — Hersteller vereinfacht Ermessensleistung; Zahlen bleiben im zuschuss-Ratgeber), RTL-Zahlen außer 55-cm-Divergenz-Zeile, TLW-Medizin-Diagnose-Framing.
2. **Renderer:** article-renderer.mjs specialMap +1 (Early-CTA „Anbieter für Sitz- und Stehlifte vergleichen“ → treppenlift-firmen-vergleich). research/llms-txt.py SUMMARIES + SECTION_MAP +1. isLift-Regex deckt den Slug automatisch ab (keine Regex-Änderung).
3. **Testzähler:** test_articles.py 28→29; verify_checklists_build.py RSS 28→29; test_partner_links.py A3 ≥27→≥28. Neu: research/verify_sitzsteh_{061126,content_061126,svg_mobile_061126,live_061126}.py + strip/pull-Scripts + inspect/show-Schema-Helper. Grafik assets/images/treppenlift-sitzsteh-entscheidung.svg (3 Fragen + 3 Ergebnis-Bänder, getBBox 0 Overflows + Pairwise-Overlap 0 + Vision inkl. Ecken-Zoom sauber, Mobile 390 px 0 px Overflow). Protokoll research/treppenlift-sitzlift-oder-stehlift-batch.md.
4. **Teststand:** npm test komplett grün (Exit 0; Playwright 21 passed; Partner A–F ALL PASS; LAUNCH 49 Seiten/8 Checklisten-URLs), Content-Gate ALL PASS, verify_checklists_build ALL PASS. Deploy+Live-Readback: siehe launch-state 06.11.
5. **Refresh-Kandidat notiert:** keiner neu; bestehende Offenen (ADCELL-GO, Liftstar-Follow-up, Awin-Login-Status) unverändert.

### Batch 13 (2026-11-04, Cron-Lauf) — Briefing 16: Mobiler Hausnotruf mit GPS
1. **Neu veröffentlicht:** hausnotruf-mobil-gps-unterwegs.json — mobiler Notruf für unterwegs und
   „ohne Festnetz" (auch stationär via Mobilfunk/SIM): Funktionsweise + Ortung nur im Notfall,
   Stationär-vs.-Mobil-Vergleichstabelle mit Reichweiten-Divergenz (30–50 m / 50–100 m / bis 150 m
   — dokumentiert statt Einzahl), drei Nutzerprofile (zuhause/unterwegs/Demenz) mit Uhr/Handy-
   Grenzen, Kosten-Bausteine mit Spannen-Dokumentation (GPS-Aufpreis 10–25 € kompass vs. 30–80 €
   VZ; Gesamt 30–50 vs. 35–70 €/Monat; Sturzerkennung ~5–10 €; Einrichtung ~49,90 € als einzelne
   Fachportalangabe), Pflegekasse als Drei-Ebenen-Auflösung des PORTAL-WIDERSPRUCHS (panorama/
   kompass „privat/Eigenanteil" vs. sanivia/hnrkosten „0 €/Monat": VZ-Basistarif bis 27 €/Monat
   seit 01.04.2026 + Vertragspartner-Bedingung + MD-Prüfung; Hilfsmittel-Weg mit Rehadat-GKV
   Position 52.40.01 inkl. ausdrücklich MOBILER Geräte NEO GSM/TA74 4G/derButler; § 40 Abs. 1/3/7
   Leihe + 10 %/max. 25 € + Mehrkosten-Satz + 3/5-Wochen-Fiktion), Ortung/Demenz (Zustimmungs-
   pflicht, Persönlichkeitsrecht, Vorsorgevollmacht, Geofencing-Frage, keine Pauschalempfehlung),
   Lade-Routine (Akku-Divergenz 1–7 Tage / 50 Std / täglich-bis-wöchentlich), 10-Fragen-Checkliste.
   11 Abschnitte, 6 FAQs, 12 Quellen, 85/85 Ledger-Pässe inkl. 8 Arithmetik-Checks
   (research/hausnotruf-mobil-041126-ledger.json + verify_hausnotruf_mobil_041126.py), Grafik
   assets/images/hausnotruf-mobil-entscheidung.svg (Marker/Band-Layout, getBBox 0 Overflows +
   Vision sauber), Protokoll research/hausnotruf-mobil-gps-unterwegs-batch.md. 27. Ratgeber;
   Topic SERP-basiert (GSC im Cron weiter ohne Google-Sitzung), intent-distinct (Bestand deckte
   den Mobil-Intent nur mit einem Zusatzkosten-Satz im Kosten-Artikel).
2. **Bewusst KEIN Malteser-Placement auf diesem Artikel:** Malteser hat (Produktseite+FAQ
   04.11.) nur das stationäre System — ein mobiler CTA wäre ein falsches Versprechen. Malteser
   nur als gekennzeichnete Herstellerangabe (Quellen 10/11: Mobilfunk ohne Telefonanschluss,
   72-h-Akku, GSM-Testruf); CTA-Route über Early-CTA auf hausnotruf-kosten-anbieter-vergleich
   (dort leben die aktiven Placements). Content-Gate assertet 0 Partner-Marker auf dem Artikel.
3. **Renderer:** article-renderer.mjs specialMap +1 (Early-CTA „Kosten & Anbieter vergleichen" →
   hausnotruf-kosten-anbieter-vergleich). data/cross-links.json +1 (3 Cluster-interne Cross-Ziele:
   sturzerkennung, kosten-vergleich, hilfsmittel-pflegekasse + rationale). llms-txt.py SUMMARIES +
   SECTION_MAP erweitert. isCare-Regex trifft über hausnotruf-Präfix (keine Regex-Änderung nötig).
4. **Testzähler:** test_articles 26→27; verify_checklists_build RSS 26→27 Items; test_partner_links
   A3 ≥ 27. Neu: research/verify_hausnotruf_mobil_{041126,svg,content,mobile}_041126.py +
   fetch_hausnotruf_mobil_041126.sh + strip_hausnotruf_mobil_041126.py.
5. **Teststand:** npm test komplett grün (beide Builds, test_site, test_articles 27, cross_links,
   titles_meta, measurement, Playwright-Consent, Partner-Gates A–F ALL PASS), Content-Support-Gate
   ALL PASS, Mobile 390 px 0 px Overflow. Live-Readback: siehe launch-state 04.11.
6. **Refresh-Kandidat notiert:** VZ hat Zusatzkosten-Spanne auf „30 bis 80 Euro" aktualisiert
   (heute gelesen); hausnotruf-kosten-anbieter-vergleich sagt noch „rund 30 bis 50 Euro oder mehr"
   (VZ-Stand 29.07.) — Zahl+checked_at in einer eigenen Kernartikel-Unit heben.

### Batch 12 (2026-11-02, Cron-Lauf) — Briefing 15: Wohnumfeld-Zuschuss beantragen
1. **Neu veröffentlicht:** wohnumfeldverbesserung-beantragen.json — Pflegekassen-Antragsstrecke nach
   § 40 Abs. 4 SGB XI: Ermessensleistung („können subsidiär“) mit Zweckformel, 4.180 € je Maßnahme /
   16.720 € WG-Deckel, Pflegegrade 1–5 (BMG), Antrag VOR dem Umbau (AOK/DAK/mkk/pflege.de wörtlich),
   gesetzliche 3/5-Wochen-Frist mit Genehmigungsfiktion laut Abs. 7 — ausdrücklich auch für
   wohnumfeldverbessernde Maßnahmen (Hauptdifferenzierung; Wettbewerber schreiben die Fiktion meist
   nur Hilfsmitteln zu) —, Unterlagen-Checkliste, Mietwohnung (Vermieter, Umzug-Sonderfall),
   Ablehnungsgründe + Widerspruch 1 Monat, fiktives Rechenbeispiel (9.400 → 4.180 → 5.220) +
   WG-Durchrechnung (8 × 2.090 €), Abgrenzung Hilfsmittel 33.40.05 (Aufsatz) vs. kompletter Umbau.
   10 Abschnitte, 6 FAQs, 10 Quellen, 46/46 Ledger-Pässe (research/wohnumfeld-021126-ledger.json),
   Grafik assets/images/wohnumfeld-antrag-wegweiser.svg (getBBox 0 Overflows + Badge-im-Rect +
   Vision sauber), Protokoll research/wohnumfeldverbesserung-beantragen-batch.md. 26. Ratgeber;
   Topic SERP-basiert (GSC blockiert), intent-distinct gegen zuschuss/hilfsmittel/pflegegrad
   (grep-Befund: 0 Antragsstrecken-Content im Bestand).
2. **Renderer:** article-renderer.mjs isCare-Regex + „wohnumfeld“, specialMap +1 (Early-CTA
   „Förderlandschaft im Überblick“ → treppenlift-zuschuss). test_cross_links.py Regex synchron.
   llms-txt.py SUMMARIES + SECTION_MAP erweitert.
3. **Testzähler:** test_articles 25→26; verify_checklists_build RSS 25→26 Items;
   test_partner_links A2 ≥ 26. data/cross-links.json: wohnumfeld → [hilfsmittel-pflegekasse,
   pflegegrad-antrag] (care-intern). Neu: verify_wohnumfeld_{021126,content,svg,mobile}_021126.py
   + fetch_wohnumfeld_021126.sh (Content-Gate-Lesson: sup.cite-<a>-Markup strippen, &-escapete
   URLs doppelt prüfen).
4. **Teststand:** npm test komplett grün (test_site 50 Seiten/37 locs, test_articles 26,
   cross_links 26/7, titles 0 Verletzungen, measurement, Playwright 20/20 nach Flaky-Re-Run,
   Partner ALL PASS), Content-Gate ALL PASS, Mobile 390 px 0 px Overflow. Deploy+Readback:
   launch-state 02.11.

### Index-Hygiene-Unit (2026-10-30, Abend, Cron-Lauf) — Audit-Fix #5: Region-Platzhalter noindex
1. **Live-Re-Derivation:** 13/49 Sitemap-URLs (Hub + 12 Bundesländer) waren „in Vorbereitung“-Stubs
   mit robots index,follow; Hub hatte 0 interne Inlinks. 27 % der Sitemap = Placeholder → Thin-Content-
   und Doorway-Risiko in der frühen Indexierungsphase.
2. **Umsetzung (keine Content-Löschung, nur Sichtbarkeit):** `robotsOverride:'noindex,follow'` auf
   regional.html + alle region/*.html in generate.mjs; Sitemap-Filter jetzt strukturell
   (`robotsOverride!=='noindex,follow'` — noindex kommt nie in die Sitemap, beide Erzeugungspfade).
   Stub-Copy unverändert ehrlich gelassen („Wir versprechen deshalb keine verfügbaren Fachbetriebe.“).
3. **Gates:** test_site.py — Region-Seiten MÜSSEN noindex sein (LAUNCH), 0 Region-URLs in der Sitemap,
   datenschutz bleibt indexierbar, alles andere indexierbar. Damit ist expand-or-noindex (#5) als
   Dauer-Gate geschlossen; Re-Indexierung pro Seite = robotsOverride entfernen, Gates erzwingen
   Sitemap-Konsistenz automatisch.
4. **Teststand:** npm test Exit 0 (test_site 49 Seiten/36 locs, test_articles 25, test_cross_links 25,
   test_titles_meta ALL PASS, Playwright 20, Partner-Gates ALL PASS). Deploy+Live-Readback: siehe
   launch-state 30.10. (Abend).
5. **Nicht Teil dieser Unit:** Region-Ausbau mit Landesförderprogrammen je Bundesland (recherchierter
   Batch mit Primärquellen, kein Massen-Template) — erst nach #6b/#9/#10 dran.

### Copy-Unit (2026-10-30, Cron-Lauf) — SEO-Audit Fix #7: Titel ≤65 / Meta-Descs ≤160
1. **Re-Derivation vor Umsetzung:** Befund X3/X4 (Snapshot 19.10., 18 Artikel) gegen die LIVE-Site
   neu erhoben (30.10., 31 URLs): 24 Ratgeber-Titel >65 (Renderer-Suffix „ — ZuhauseBleiben
   Kompass" = 25 Zeichen auf jedem `<title>`), 12 Descriptions >160 inkl. Checklisten-Hub (185)
   und pflegegrad-beantragen (242, Disclaimer-als-Snippet). Kein Snapshot-Recycling.
2. **Umsetzung (reine Copy-Edits, H1/Inhalte/Quellen unangetastet):**
   `research/apply_titles_meta_301026.py` kürzt 24 JSON-`title` auf Keyword-Kopf ≤40 (Live-Tag ≤65)
   und 10 `description` auf ≤155, chirurgisch per Top-Level-Zeilen-Regex. Lektion: der erste
   Versuch mit `json.dumps`-Roundtrip formatierte die kompakt geschriebenen Arrays der Batches
   6–14 um (428 Diff-Zeilen); Rollback + Zeilen-Regex → 34/34 Zeilen.
3. **Renderer:** generate.mjs Editorial-Loop respektiert jetzt `e.desc`-Override — X4 gelöst:
   pflegegrad-beantragen bekommt benefit-first desc (128), Disclaimer bleibt im Seitenkörper.
   build-checklists.mjs: neue optionale `pageTitle`/`pageDesc` je Checkliste (H1 = checklistTitle
   bleibt lang), Hub-Titel 82→51, Hub-Desc 185→140.
4. **Neues Gate:** `test_titles_meta.py` in npm test (nach test_cross_links, gegen LAUNCH-Dist):
   jede gebaute HTML-Seite ≤65 Title/≤160 Desc (Entity-unescaped), sitewide keine doppelten
   Titles, keine doppelten Descs (region/* bewusst ausgenommen — deren expand-or-noindex ist
   Fix #5), og:title spiegelt `<title>`. Testzähler unverändert (kein Seitenzuwachs).
5. **Teststand:** npm test komplett grün (inkl. test_titles_meta 49 Seiten 0 Verletzungen,
   Playwright-Consent, Partner-Gates A2 ≥ 25). RSS/llms.txt ziehen die kurzen Titel automatisch
   (llms-txt.py nutzt JSON-title, LEGACY_PAGES-Titel unangetastet). Deploy+Live-Readback: siehe
   launch-state 30.10.

### Renderer-Iteration (2026-10-28, Abend, Cron-Lauf) — Related-Cross-Links aus der Magnet-Analyse
1. **Umgesetzt:** die 6 offenen internen Link-Empfehlungen aus `research/GROWTH-BACKLOG.md`
   (Link-Magnet-Analyse, Deliverable 5) als `data/cross-links.json` + Renderer-Pfad in
   article-renderer.mjs: pflegegrad-antrag→verhinderungspflege-ueberblick+tuerbreiten-schnellcheck,
   treppenlift-mietwohnung→tuerbreiten (Cross-Cluster-Whitelist), hausnotruf×2→treppenlift-zuschuss
   (Cross-Cluster-Whitelist), beleuchtung→hilfsmittel-pflegekasse-uebernahme,
   wanne-zur-dusche→badumbau-angebote-vergleichen. Rollator→Hilfsmittel war bereits über die
   specialMap (Early-CTA „Kostenübernahme prüfen") erfüllt und ist nicht doppelt geführt.
2. **Mechanik:** Cross-Ziele stehen VOR der alphabetischen Cluster-Pool-Auswahl; Related-Liste bleibt
   exakt 3 Einträge (bestehende Per-Artikel-Gates mit len==3 bleiben grün). Unbekannte/self-Ziele im
   Config brechen den Build.
3. **Neues Gate:** `test_cross_links.py` (25 Artikel: je genau 3 Related-Links, Cross-Ziele vorne in
   Reihenfolge, kein nicht-whitelisted Cluster-Verstoß, Config-Integrität) in `npm test` eingehängt
   (Position: nach test_articles, gegen den LAUNCH-Dist). Lektion beim Gate-Bau: Cluster-Regel exakt
   replizieren (Bad-Pool schließt treppenlift-zuschuss bewusst ein) und das Related-Segment bis
   `</section>` begrenzen — ein Zeichen-Fenster griff sonst in den Footer und zählte falsche Links.
4. **Teststand:** npm test komplett grün (test_site 49 Seiten beide Modi, test_articles 25,
   test_cross_links 25/25, test_partner_links ALL PASS, Playwright consent+measurement+checklists,
   measurement-policy). Deploy+Live-Readback: siehe launch-state 28.10. (Abend).

### Batch 11 (2026-10-28, Cron-Lauf) — Briefing 14: Plattformlift/Rollstuhllift
1. **Neu veröffentlicht:** treppenlift-plattformlift-rollstuhllift.json — Plattformlift für
   Rollstuhlfahrer: Vier-Bauarten-Trennung vor Preisvergleich (Hublift / gerade / kurvig /
   Homelift; lehner belegt Begriffsvermischung), Portal-Spannen-Tabelle mit Stand-Spalte
   (Unter-Grenzen gerade innen 7.000/7.500/8.000/9.000/10.000 €) neben Herstellertabelle
   (HIRO-Preisseite 11.000–38.000 € inkl. Etagenstaffel, kurvig außen „Auf Anfrage“; Lifta
   ab 11.000 gerade / ab 19.000 kurvig, beide live 28.10.2026), Tragkraft-Widersprüche
   dokumentiert (225–300 vs. 250 vs. 300–320 vs. 200-kg-Grenze vs. 250–400 „inkl.
   Begleitperson“; HIRO 350 = 300 kg, 320 K = 250 kg live), Begleitperson-Widerspruch
   (treppenlifto vs. kostenwelt) und Tempo-Divergenz (0,1 vs. 0,15 m/s) als
   Angebots-Klärpunkte, Treppenbreiten-Widerspruch (Lifta 90–110 cm vs. „1 m“),
   Gebraucht-Divergenz (40 % vs. „unter 6.000“), Miete kaum üblich. 11 Abschnitte, 6 FAQs,
   11 Quellen, 185/185 Ledger-Pässe (research/plattformlift-281026-ledger.json +
   research/verify_plattformlift_281026.py: 103 verbatim + 20 Tabellen-Kontext + 12
   Arithmetik/Divergenz), Grafik assets/images/treppenlift-plattformlift-rollstuhllift-weg.svg
   (Zeilen-Layout, getBBox + Box-Kontext 0 Verstöße + Vision sauber), Protokoll
   research/treppenlift-plattformlift-rollstuhllift-batch.md. 25. Ratgeber; Förderbeträge
   bewusst nur als Verweis auf treppenlift-zuschuss; KfW-Stale-Echo (kostenwelt) im Ledger notiert.
2. **Renderer:** article-renderer.mjs specialMap +1 (Early-CTA „Anbieter für Rollstuhllifte
   vergleichen“ → treppenlift-firmen-vergleich). llms-txt.py SUMMARIES + SECTION_MAP erweitert.
3. **Testzähler:** test_articles 24→25; verify_checklists_build RSS 24→25 Items;
   test_partner_links A2 ≥ 25. Neu: research/verify_plattformlift_content_281026.py
   (Content-Support-Gate inkl. 22 Kernzahlen, robots-Normalisierung),
   research/verify_plattformlift_svg_281026.py (getBBox + Box-Kontext-Check + Screenshot),
   research/verify_plattformlift_mobile_281026.py (390 px),
   research/fetch_plattformlift_281026.py / fetch_plattformlift_mfr_281026.py.
4. **Topic-Gates dokumentiert:** Haltegriff-Bad verworfen (100–800-€-Produkt ohne bestätigten
   Partner, große Distanz zur Monetarisierung), Treppensteiger kein eigener Artikel (dünner
   Seitenklang); plattformlift intent-distinct (nur Alternativen-Erwähnungen in 6 Artikeln).

### Batch 10 (2026-10-27, Cron-Lauf) — Briefing 13: Außentreppe/Außenlift
1. **Neu veröffentlicht:** treppenlift-aussentreppen-aussenlift.json — Treppenlift für die
   Außentreppe: Wetterschutz-Bausteine (verzinkte/Alu-Schiene, abgedichtete Elektronik,
   Abdeckhaube als Pflicht-Zubehör), Preisdivergenz dokumentiert (4 Fachportale: 3.500–6.500 /
   4.000–10.000 / 5.000–10.000 / ab ca. 6.000 €; Lifta-Hersteller 6.500–8.500 € inkl. Einbau,
   vollständig innerhalb der eigenen Innen-Spanne 5.500–9.900 € — Pauschal-Aufschlag widerlegbar),
   IP-Divergenz (Fachportale 54/65/67 bzw. „65+“ vs. 0 IP-Angaben auf geprüften
   Herstellerseiten HIRO/Lifta → Schutzart + Temperaturbereich aus dem Datenblatt fordern),
   HIRO 160 AIR + Lifta Allwetter GTL 320 als gekennzeichnete Herstellerangaben,
   Zusatzposten draußen (Fundament als eigene Zeile, 230-V-Außensteckdose mit FI,
   EN 81-40 im Angebot), Winter-Praxis (−10/−15 °C, Akku −⅓, kein Streusalz),
   Genehmigung/MFH-Verweis, Miete außen (~50 €/Monat gerade), Gebraucht-Divergenz
   (40-%-Abschlag vs. Privatkauf-Warnung). 12 Abschnitte, 6 FAQs, 8 Quellen,
   88/88 Ledger-Pässe (research/aussenlift-271026-ledger.json +
   research/verify_aussenlift_271026.py: 78 verbatim + 3 IP-Absenz + 7 Arithmetik),
   Grafik assets/images/treppenlift-aussentreppen-aussenlift-wetterschutz.svg
   (Marker-/Legenden-Layout nach 1. Vision-Revision; getBBox 0 Overflows + Vision sauber),
   Protokoll research/treppenlift-aussentreppen-aussenlift-batch.md. 24. Ratgeber;
   Förderbeträge bewusst nur als Verweis auf treppenlift-zuschuss.
2. **Renderer:** article-renderer.mjs specialMap +1 (Early-CTA „Anbieter für Außenlift
   vergleichen“ → treppenlift-firmen-vergleich). llms-txt.py SUMMARIES + SECTION_MAP erweitert.
3. **Testzähler:** test_articles 23→24; verify_checklists_build RSS 23→24 Items;
   test_partner_links A2 ≥ 24. Neu: research/verify_aussen_content_271026.py
   (Content-Support-Gate inkl. 8 Kernzahlen), research/verify_aussen_svg_271026.py,
   research/verify_aussen_mobile_271026.py, research/fetch_aussenlift_271026.py.
4. **Topic-Gates dokumentiert:** außenlift intent-distinct (0 Bestandsüberschneidung),
   vorkaufsnah; Verbesserungslücke = Preisstreuung + IP-Nachweispflicht aus dem Datenblatt.

### Batch 9 (2026-10-27, Cron-Lauf) — Briefing 12: Maximalgewicht/Tragkraft
1. **Neu veröffentlicht:** treppenlift-maximalgewicht.json — Treppenlift-Tragkraft: Grenze gilt für
   Person plus Zuladung (Überlastschutz startet die Fahrt nicht), belegte Herstellerwerte als
   Tabelle (HIRO 135/150/175 gerade+kurvig; Lifta Esprit 4500 Kurvenlift „bis ca. 125 kg"
   Datenblatt 01/2020; Lifta Klassik gerade 160/kurvig 135 laut Fachportal aus Datenblättern
   05/23+06/2018 bei Modellseiten-Werbung „bis 160 kg"; Handicare 115–137/160/200),
   XXL-Technik (zweirohrige Schiene, Motor, Sitzbreite 55–60 cm+), Plattformlift 250–300 kg als
   Alternative, 8-Punkte-Aufmaß-Checkliste, Preis nur als Fachportal-Schätzung 15–25 % +
   HIRO-Plattformlift-Herstellerangabe. 10 Abschnitte, 6 FAQs, 9 Quellen, 40/40 Zitate verbatim
   (research/nutzlast-271026-ledger.json), Grafik assets/images/treppenlift-maximalgewicht-
   tragkraft.svg (getBBox-Check 0 Overflows + Vision-Probe, 3 Layoutfehler gefunden und
   behoben), Protokoll research/treppenlift-maximalgewicht-batch.md. 23. Ratgeber;
   Topic SERP-basiert (GSC blockiert), Pauschalangaben-Divergenz (120 vs 125–160 kg) als
   Verbesserungslücke; keine Kannibalisierung (grep: 0 Tragkraft-Inhalte im Bestand).
2. **Renderer:** article-renderer.mjs specialMap +1 (Early-CTA „Angebote vergleichen" →
   treppenlift-angebote-vergleichen). llms-txt.py SUMMARIES + SECTION_MAP erweitert.
3. **Testzähler:** test_articles 22→23; verify_checklists_build RSS 22→23 Items;
   test_partner_links A2 ≥ 23. Neu: research/verify_nutzlast_271026.py (Ledger/Arithmetik
   40/40), research/verify_nutzlast_content_271026.py (Content-Support-Gate, 128 Checks,
   Includes Tabelle/Bullets/Kernzahlen), research/verify_nutzlast_svg_271026.py
   (getBBox-Overflow + Screenshot), research/verify_nutzlast_mobile_271026.py (390 px),
   research/verify_live_readback_nutzlast_271026.py (Live-Readback).
4. **Topic-Gates dokumentiert:** Akku/Stromausfall verworfen (commodity, kaum originär
   Belegbares); Kurventreppe verworfen (Kannibalisierungsrisiko mit treppenlift-kosten).

### Batch 8 (2026-10-26, Cron-Lauf, Abend) — Briefing 11: Schmale Treppe
1. **Neu veröffentlicht:** treppenlift-schmale-treppe.json — Treppenlift auf schmaler Treppe:
   Zwei-Fragen-Trennung (Gerätemindestbreite 61–77 cm laut Fachportal-Erhebung 07.10.2026 vs.
   verbleibende Laufbreite), Herstellerdiskrepanz dokumentiert (HIRO 70 cm vs. Lifta/TK 80 cm,
   ≤ 2 Wohneinheiten; alle 100 cm MFH), Restbreite 60 cm als MVV-TB-Musterangabe mit
   Landesfassung-Vorbehalt, DIN 18065 (800/1.000 mm) als Fachportalangabe, Messregeln +
   Aufmaß-Checkliste, Alternativen (Stehlift, Plattformlift 90–110 cm, Treppensteiger,
   Deckenlift, Hauslift), Preisdifferenzierung nach Treppenform statt Breite. 10 Abschnitte,
   6 FAQs, 5 Quellen (VZ, 2 Fachportale mit Methodik, Lifta + HIRO als Herstellerangaben),
   53/53 Zitate verbatim (research/schmale-treppe-261026-ledger.json), Grafik
   assets/images/treppenlift-schmale-treppe-messplan.svg (Sichtkontrolle: 0 viewBox-Overflows,
   Vision-Probe sauber), Protokoll research/treppenlift-schmale-treppe-batch.md. 22. Ratgeber;
   Förderbeträge bewusst nur als Verweis auf treppenlift-zuschuss.
2. **Renderer:** article-renderer.mjs specialMap +1 (Early-CTA „Anbieter für Aufmaß vergleichen“
   → treppenlift-firmen-vergleich). llms-txt.py SUMMARIES + SECTION_MAP erweitert.
3. **Testzähler:** test_articles 21→22; verify_checklists_build RSS 21→22 Items;
   test_partner_links A2 ≥ 22. Neu: research/verify_schmale_treppe_content_261026.py
   (Content-Support-Gate, 88 Checks, tags/citation-normalisierte Fließtextvergleiche —
   sup-Anker brechen naive Vergleiche) + research/verify_schmale_treppe_261026.py
   (Ledger/Arithmetik 53/53).
4. **Topic-Gates dokumentiert:** Wartung (post-purchase, 10+ Konkurrenten), Einbau-Ablauf
   (dicht besetzt), Pflegegrad-Widerspruch (VZ-Dominanz) verworfen; schmale Treppe gewählt
   (kaufnah, intent-distinct, SERP-Widersprüche als Verbesserungslücke).

### Batch 7 (2026-10-26, Cron-Lauf) — Briefing 10: Steuer-Route
1. **Neu veröffentlicht:** treppenlift-steuerlich-absetzen.json — § 35a EStG (20 % der Arbeitskosten,
   max. 1.200 €, nur Arbeitskosten, Rechnung + Konto-Zahlung, Förder-Ausnahme Abs. 3 Satz 2)
   und § 33 EStG (zumutbare Belastung, Nachweise), Referentenentwurf 2027 (15 %/900 €, nicht
   beschlossen) strikt getrennt. 10 Abschnitte, 6 FAQs, 4 Quellen, 41/41 Zitate verbatim
   (research/steuer-261026-ledger.json), Grafik assets/images/treppenlift-steuer-weg.svg
   (Sichtkontrolle mit 2 gefundenen und behobenen Layoutfehlern), Protokoll
   research/treppenlift-steuerlich-absetzen-batch.md. 21. Ratgeber; Topic-Wahl SERP-basiert,
   da GSC im Cron nicht abrufbar (keine Google-Sitzung, kein Vault-Login).
2. **Renderer:** article-renderer.mjs specialMap +1 (Early-CTA „Förderung prüfen" →
   treppenlift-zuschuss). llms-txt.py SUMMARIES + SECTION_MAP erweitert.
3. **Testzähler:** test_articles 20→21; verify_checklists_build RSS 20→21 Items;
   test_partner_links A2 ≥ 21. Neu: research/verify_steuer_content_261026.py (Content-Support-Gate
   für den Artikel) + research/verify_steuer_261026.py (Ledger/Arithmetik).
4. **Pflicht-Refresh:** nach Verabschiedung ESt-Reformgesetz 2027 § 35a-Zahlen neu prüfen (Ledger-Notiz).

### Batch 6 (2026-10-23, Cron-Lauf) — Briefing 1 promoviert
1. **Neu veröffentlicht:** treppenlift-angebote-vergleichen.json — Promotion des vollständig gegateten
   Drafts vom 14.10. nach heutiger Re-Verifikation aller Quellen (§ 40 SGB XI 4 180/16 720, 3/5 Wochen;
   VZ Treppenlifte 13 Claims; VZ BGH I ZR 96/20; Details + Gate-Ergebnisse:
   research/treppenlift-angebote-vergleichen-batch.md). 20. Ratgeber; Phase 1 damit vollständig live.
2. **Renderer:** generate.mjs — Draft-Block + DRAFT_PAGES entfernt (URL jetzt in beiden Modi als
   Artikel); article-renderer.mjs specialMap-Eintrag → treppenlift-zuschuss „Förderung prüfen".
3. **Testzähler:** test_articles 19→20; test_site-Draft-Sonderfall entfernt; verify_checklists_build
   (RSS 20 Items, Sitemap enthält Artikel, llms deckt ab); test_partner_links A2 ≥ 20; llms-txt.py
   SUMMARIES + SECTION_MAP ergänzt.

### Batch 5 (2026-10-19, Cron-Lauf, Abend) — Briefing 7
1. **Neu veröffentlicht:** badumbau-angebote-vergleichen.json — Vergleichsmechanik für Badumbau-Angebote (Vergleichsbasis: dieselbe Beschreibung für jeden Betrieb; Positionstabelle Rückbau→Logistik; Abdichtung nach DIN 18534 Neufassung 2025-10 mit W1-I/W2-I und fugenlos=Vereinbarungspflicht; Preisbindung KV vs. Festpreis mit 15–20-%-Hinweisschwelle; Zusatzarbeiten § 650b/650k BGB; Abschläge § 632a BGB; Verjährung § 634a BGB 2/5 Jahre ab Abnahme; 8-Punkte-Fragenliste pro Betrieb). 8 Abschnitte, 6 FAQs, 9 Quellen mit Verbatim-Evidenz (research/badumbau-angebote-ledger.json, 25/25 maschinell verifiziert), Grafik assets/images/badumbau-angebote-vergleich.svg (Chromium-Sichtkontrolle), Protokoll research/badumbau-angebote-vergleichen-batch.md. Keine Marktpreise erfunden; DIN-Angaben als Hersteller-/Fachdarstellung gekennzeichnet; Rechtszahlen nur mit BGB-Quellenbeleg.
2. **Renderer:** article-renderer.mjs specialMap-Eintrag +1 (Early-CTA „Badumbau planen“ → /bad-umbau-barrierefrei.html statt Bad-Cluster-Default „Förderung prüfen“ → Treppenlift-Zuschuss).
3. **Testzähler:** test_articles.py 17→18 Artikel.
4. **Abgrenzung:** wanne-zur-dusche (Produktentscheidung/Bauablauf) und bad-umbau-barrierefrei (Gesamtplanung) unangetastet; neuer Artikel deckt die dedizierte Angebotsvergleichs-Mechanik (KV/Festpreis, Abschläge, §§ 650b/650k/634a, DIN-18534-Nachfragen) — intent-distinct, Related-Links im Bad-Cluster.

### Batch 4 (2026-10-19, Cron-Lauf) — Briefing 6
1. **Neu veröffentlicht:** bodengleiche-dusche-altbau.json — Machbarkeits-Fahrplan Altbau (vier Prüfentscheidungen: Aufbauhöhe, Weg zum Fallrohr, Decke/Konstruktion, Norm als Zielgröße), flache Alternative mit Restschwelle als ehrliche Option, 10-Punkte-Fragenliste für den Vor-Ort-Termin, Förderlogik § 40 Abs. 4 SGB XI (4.180/16.720 €, Ermessen), KfW 455-B Antragstopp (19.10. verifiziert) + 159 inkl. wörtlichem Kombinationsverbot/Ausnahme, § 554 BGB-Verweis mit Link auf Mietwohnung-Ratgeber. 8 Abschnitte, 6 FAQs, ~2.390 Wörter, 10 Quellen mit Verbatim-Evidenz (research/altbau-dusche-ledger.json, 29/29 Zitate maschinell verifiziert), Grafik assets/images/bodengleiche-dusche-altbau-pruefpunkte.svg (Chromium-Sichtkontrolle), Protokoll research/bodengleiche-dusche-altbau-batch.md + Acceptance research/evidence/bodengleiche-dusche-altbau-acceptance.md.
2. **Renderer-Fix:** article-renderer.mjs isBad-Cluster erkennt jetzt auch „dusche“ im Slug (bodengleiche-dusche-altbau landete sonst im lift-Cluster mit falschen „Passend dazu“-Links). Early-CTA-Ziel für den neuen Artikel: treppenlift-mietwohnung („Mietwohnung: Zustimmungen klären“).
3. **Testzähler:** test_articles.py 16→17 Artikel.

### Live-Kern (vor Batch 1/2, status editorial-reviewed-preview)
- treppenlift-kosten
- treppenlift-zuschuss
- bad-umbau-barrierefrei
- wanne-zur-dusche
- treppenlift-mieten
- treppenlift-firmen-vergleich
- treppenlift-gebraucht-oder-neu

### Batch 3 (2026-10-16, Cron-Lauf)
1. **Neu veröffentlicht:** treppenlift-mietwohnung.json (Briefing 4 laut SEO-STRATEGIE.md) — Zustimmungs-Fahrplan Miete/Eigentum/gemeinsames Treppenhaus (§ 554 BGB, § 20 WEG, § 40 SGB XI wörtlich belegt), Brandschutz als häufigster Ablehnungsgrund, Antrags-/Rückbau-/Sicherheitsleistung-Einordnung, 6-Schritte-Checkliste, 6 FAQs, 7 Quellen mit Verbatim-Evidenz (research/mietwohnung-ledger.json), Grafik assets/images/treppenlift-mietwohnung-zustimmung.svg (visuell geprüft), Protokoll research/treppenlift-mietwohnung-batch.md + Acceptance research/evidence/treppenlift-mietwohnung-acceptance.md. Status editorial-reviewed-preview → im Launch-Index wie die übrigen Ratgeber.
2. **Renderer-Fix:** article-renderer.mjs rendert jetzt `paragraphs_after` (Feld wurde bisher gedroppt). Betraf live den Artikel treppenlift-mieten: Schlussabsatz der Beispielrechnung (Break-even 23,6 Monate) fehlte seit Deploy 15.10. Nur dieser Artikel nutzt das Feld.
3. **Testzähler:** test_articles.py 11→12 Artikel.

### Batch 1 (2026-10-14, vorherige Session; Scratch: treppenlift-batch/, bad-batch/)
- Keine neuen content-ready-Dateien in Batch 1; bestehende 7 Artikel waren Gegenstand von Verifikation/Ledgern. Protokolle: research/treppenlift-batch.md, research/bad-foerderung-batch.md.

### Batch 2 (2026-10-15, diese Session) — Cluster „Hausnotruf" + „Wohnraum-Anpassung klein"
Neue content-ready-Dateien (alle status review-required):
1. hausnotruf-kosten-anbieter-vergleich.json — Kostenrahmen, Basistarifbausteine, Pflegekasse (27 €/Monat, Voraussetzungen), Vertrags-/Kündigungsgrundlagen, Vergleichscheckliste. 8 Abschnitte, 6 FAQ, 4 Quellen, ~1.516 Wörter.
2. hausnotruf-sturzerkennung-oder-knopf.json — Funktionsprinzip, Grenzen (langsame Stürze), Fehlalarme + Vorlauf/Abbruch, Entscheidungsmatrix, Kosten des Aufpreises, Notrufdaten/DSGVO, Beratungcheckliste. 9 Abschnitte, 6 FAQ, 3 Quellen, ~1.516 Wörter.
3. tuerbreiten-schwellen-schnellcheck.json — Messanleitung + Messbogen, Normorientierung (DIN 18040-2 als Fachportaldarstellung), Rampen-Stufenlogik, Kostenfaktoren Türverbreiterung, § 554 BGB, Pflegekasse vor Bau, Schnell-Check. 8 Abschnitte, 6 FAQ, 5 Quellen, ~1.659 Wörter.
4. beleuchtung-orientierung-im-alter.json — Sehveränderung, multiple Lichtquellen, Blendung/Kontraste, Raum-Kategorientabelle, Nachtlicht, Bewegungsmelder mit Vorbehalten, Lichtfarbe/Dimmen, Energie/Kostenstruktur, Einkaufscheckliste. 9 Abschnitte, 6 FAQ, 5 Quellen, ~1.612 Wörter.

Neue Bilder (assets/images/, alle „KI-Illustration · schematisch"):
- hausnotruf-ablauf.svg
- hausnotruf-sturz-entscheidung.svg
- tuer-schwelle-messcheck.svg
- licht-orientierung-tagesverlauf.svg

Recherche-Dokumente:
- research/hausnotruf-wohnen-klein-batch.md (Batch-Dokument Cluster A+B: Clusterwahl, SERP-Check, Quellenkette, Grenzen)
- research/evidence/batch2-hausnotruf-evidence.md (wörtliche Belege Cluster A)
- research/evidence/batch2-wohnen-klein-evidence.md (wörtliche Belege Cluster B)
- Rohabrufe/Scratch (temporär): /Users/mac/.hermes/profiles/milo/cache/scratch/batch2-clusters/

## Zustand und Gates

- **Aktualisiert 2026-10-16 (Lauf 2):** Die 4 Batch-2-Artikel wurden am 16.10. nach Quellen-Verifikation veröffentlicht (Commit 5f38a01, Parallel-Lauf) und sind live/indexierbar; die beiden folgenden historischen Batch-2-Zeilen beschreiben den Stand zum Batch-Zeitpunkt. Renderer/Generate wurden im Lauf 2 gezielt geändert (Cluster-Related + CTA-Ziele + Footer), mit Tests in beiden Build-Modi.
- Alle 4 Batch-2-Artikel: status „review-required“. Kein Build, kein Deploy, keine Sitemap-Änderung, noindex-Status unangetastet.
- Renderer/Generate/Design/CTA/Tests: nicht angefasst (Sperrliste beachtet).
- Offene Integrationsfragen für das Gate: **Frage 1 und 2 am 2026-10-16 (Lauf 2) gelöst** — article-renderer.mjs hat jetzt Cluster-Logik (bad/care/lift per Slug-Präfix) für „Passend dazu" und kontextpassende Early-CTA-Ziele (specialMap + Cluster-Defaults); Pflege-Cluster-Artikel verlinken sich gegenseitig statt in den Treppenlift-Trichter. Verbleibend:
  1. Vor Veröffentlichung: Pflegekassen-27-Euro-Stand (VZ, Stand 29.07.2026) erneut gegen aktuelle Quelle prüfen; KfW-Status unverändert lassen (455-B geschlossen, 159 offen — Stand 2026-10-14, betrifft bestehende Artikel).
  2. Bildpfade existieren; visuelle Layoutprüfung bleibt Gate.
- Cluster-Historie für spätere Auswertung: Hausnotruf laut HORIZONTALE-EXPANSION.md organischer angrenzender Cluster (Malteser als Referenz, Awin 112616 öffentlich bewerbbar); Wohnraum-klein stärkt Upsell-Pfad zu Treppenlift/Bad.

## Qualitätsgate-Regeln, die in Batch 2 angewandt wurden (für künftige Batches)

- Keine Preis-/Marktmittelwerte ohne verifizierbare Primärquelle; Redaktions-/Anbieterangaben stets als solche kennzeichnen.
- Fördernennungen immer mit Höchstbetrag-Logik (4.180 € je Maßnahme, Ermessen, keine Zusage).
- Medizinische Themen (Sturz, Demenz) nur als allgemeine Orientierung + explizite Grenzen; keine Diagnosen, keine individuellen Empfehlungen.
- Normangaben nur als gekennzeichnete Fachportaldarstellungen, nie als Normbestätigung für konkrete Objekte.
- Keine Gesundheitsdatenabfragen, keine Formulare, keine Partnerzusage im Text.
- Bilder: eigene schematische SVGs mit KI-Label, title/desc, Grenztext, viewBox für Renderer-Dimensionserkennung.

## Batch: hilfsmittel-dusch-wc-uebernahme (Briefing 9, 2026-10-21)

- Artikel live/indexierbar (Commit siehe git log): Dusch-WC — Krankenkassen-Route über gelistete
  Toilettenaufsätze mit Wascheinrichtung (PG 33.40.05, enge Arm-/Hand-Indikation), Pflegekassen-
  Wohnumfeldroute als Einzelfall, Selbstkauf-Kriterien, Antrags-Checkliste. 8 Quellen, 20/20 Zitate
  verbatim (`research/dusch-wc-ledger.json`), Beweisdateien `research/evidence/dusch-wc-*`.
- Renderer: specialMap-Eintrag (Early-CTA → hilfsmittel-pflegekasse-uebernahme); Care-Cluster trifft
  via Slug-Präfix. test_articles-Zähler 18→19 im selben Commit.
- Nicht Teil des Batches: In-Flight-Arbeiten anderer Läufe (RSS-Feed, Checklisten-Build, llms.txt,
  Growth-Dokumente) bleiben unangetastet/uncommittet.
