# Partner-Scan Bad-Cluster (23.10.2026, Cron-Lauf 3)

**Zweck:** Der Bad-Cluster (bad-umbau-barrierefrei, wanne-zu-dusche, bodengleiche-dusche-altbau, badumbau-angebote-vergleichen, dusch-wc-*, duschkopf, bad-wanne-hoehe + Checklisten Badumbau-Angebote) hatte bislang **keine untersuchte Monetarisierungsroute** — der Partner-Scan 231026 (morgens) deckte nur Treppenlift (Lifta/Acorn) und Hausnotruf (Malteser/Pflegehase/hausnotruf.de) ab. Der Morgenlauf hatte den Bad-Cluster nicht berührt (grep: 0 Treffer zu bad/dusche im Scan-Dokument).

## Ergebnis: Aroundhome DE (Awin 68536) — ein Kandidat, antragsfertig vorbereitet

**Was Aroundhome ist:** Vermittlungsplattform (ehem. MyHammer-Umfeld, Berlin), vermittelt Verbraucheranfragen an Fachpartner; nach eigener Startseite sind **Badezimmer** und **Treppenlift** aktive „Beliebte Services“ [3]. Die Badezimmer-Landingpage bewirbt genau unsere Leserschaft: barrierefreier Badezimmerumbau, „Experten finden und Angebot einholen“, ebenerdige Duschen [2].

**Konditionen laut Awin-Öffentlichem Profil 68536 (23.10.2026 gelesen, ohne Login):** [1]
- **Vergütung:** Umsatzbeteiligung, „im Regelfall 30 %“ des Umsatzes, den Aroundhome mit dem Lead erzielt — **kein Fix-CPL**.
- Cookie 30 Tage; Lead-Validierung im Schnitt 8 Tage; Echtzeit-Tracking.
- **Lead-Kriterien:** „echte Kontaktdaten, keine doppelten und nur exklusive Anfragen, keine Testanfragen, keine Auslandsanfragen“ — Annahmerisiko trägt der Lead, nicht wir.
- Für Leser: „Bis zu 3 individuelle Angebote von lokalen Firmen“, geprüfte Anbieter.
- Affiliate-Management: be around GmbH / Artefact (Torsten Leidloff, aroundhome-all-aff-de@artefact.com; Florian Steinfatt, affiliateprogramm@aroundhome.de).

**Wirtschaftlichkeit — ehrliche Einordnung (Hypothese, kein Forecast):**
- 30 % von Aroundhomes Lead-Ertrag. Was Aroundhome je Badumbau-Lead erlöst, ist nicht öffentlich; als Größenordnung dient nur eine Sekundärquelle: Handwerker zahlen je nach Portal/Gewerk 8–120 € je Kundenanfrage, Aroundhome mit Festpreis je qualifizierter Anfrage und max. 3 Fachpartnern je Anfrage [8, ausdrücklich Sekundärquelle]. Ein akzeptierter Lead könnte damit einstellig bis niedrig zweistellig € erbringen — **unbestätigt**. Falsche Lead-Qualität = 0 €.
- Gegenüber Lifta (50 €/Lead fix, Treppenlift) und Malteser (1 €/10 € CPL fix, Hausnotruf) ist das Modell variabler und schwerer vorhersagbar. Es schließt aber die einzige bisher unmonetarisierte Kerncluster-Lücke und nutzt das **bereits bestehende Awin-Publisher-Konto (3124891)** — keine neue Netzwerkregistrierung nötig.

**Verwerfungen (mit Beleg):**
- **Badumbauheld** — „Partner werden“ richtet sich an **Fachbetriebe**, die Anfragen *empfangen* und Provision zahlen [4]; wir sind kein Handwerksbetrieb. Keine Publisher-Route erkennbar.
- **Seniovo** — Partnernetzwerk für Fachpartner (Aroundhome-Bezug: „bereits über 500 vermittelte Kund:innen“ [5] belegt zugleich, dass Aroundhomes Badumbau-Vermittlung real aktiv ist). Kein Publisher-/Affiliate-Angebot auf der Seite.

**Nebenbefund:** Aroundhome betreibt parallel ein eigenes Affiliate-Tracking („Triple A“, Artefact/easy.affiliate) [7]. Wir bleiben beim Awin-Programm (ein Konto, ein Reporting); Triple-A nur falls Awin-Weg scheitert.

## Abhängigkeiten und offene Punkte (keine Zusage, kein Link vorher)

1. **Bewerbung nötig (Awin-Login blockiert):** Anwendung auf Programm 68536 über das bestehende Publisher-Konto — identischer Blocker wie Lifta/Malteser-Status-Readback (Browsersitzung tot, kein Vault-Eintrag). Der Status beider laufenden Bewerbungen ist seit 15./17.10. nicht ablesbar.
2. **SEM-/Traffic-Regeln:** Öffentliches Profil zeigt keine SEM-Klausel; Programmbedingungen liegen hinter dem Login. Beim Bewerbungsdialog (Promotion-Typ „Content“) und/oder per Erstmail klären — Gleiche-Justification wie bisher (redaktioneller Content, kein SEM, keine Gesundheitsdaten).
3. **Datenschutz:** Reine Affiliate-Weiterleitung (Leser verlässt die Site, Aroundhome wird Controller seines Formulars). Kennzeichnung + Datenschutzerklärungs-Ergänzung erst wenn ein Link live geht (gleiche Regel wie ADCELL).
4. **Lead-Datensparsamkeit:** Wir erzeugen selbst kein Formular und erfassen keine Gesundheitsdaten; der Leser übermittelt seine Daten direkt an Aroundhome. Keine Datenweitergabe durch uns.
5. **Vergütungshinweis in CTA:** Platzierung mit Umsatzbeteiligung muss anders formuliert werden als Fix-CPL („Beteiligung am Vermittlungsumsatz“ statt „X € pro Lead“) — erst bei Aktivierung.

## Vorbereitete Einträge (Rendering bleibt inaktiv)

`data/partner-links.json`: Dritter Partner-Eintrag `aroundhome` (awin_advertiser_id 68536, approved=false, placements=[]) — Renderer rendert weiterhin nichts (active=false); Gate `test_partner_links.py` schließt die neue Datei ein.

## Artefakte

- Ledger: `research/partner-scan-badumbau-231026-ledger.json` — **24/24 Zitate maschinell verbatim verifiziert** (`research/verify_partner_scan_badumbau_231026.py`)
- Extrakte: `research/evidence/partner-scan-badumbau-231026/` (9 HTML + 9 txt; Roh-HTML bewusst nicht committed — nur Skripte + Ledger + txt-Extrakte)
- Skripte: `research/extract_evidence_badumbau.py`, `research/check_quotes_badumbau.py`, `research/dump_badumbau_awin.py`, `research/dump_68536_full.py`, `research/extract_badumbau_scan.py`
