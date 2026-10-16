# Recherche- und Freigabeprotokoll: Treppenlift in der Mietwohnung (Briefing 4, Phase 1)

Erstellt: 2026-10-16 (Cron-Lauf, Betreiber-Modell). Umfang: ein Artikel (`content-ready/treppenlift-mietwohnung.json`), eine Grafik, Renderer-Fix für `paragraphs_after`, Testzähler 11→12, dieses Protokoll, Ledger, Evidenzdateien. Keine Formulare, keine Partnerlinks, keine Werbeausgaben.

## SERP-Check (2026-10-16, web_search, 2 Queries)

Query 1: „Treppenlift Mietwohnung Vermieter Zustimmung § 554 BGB Einbau" → 10/10 Treffer: Vermittlungs-/Lead-Portale (checkfox, treppenliftwissen, pflege.net, regional-treppenlift, siemer), Kanzlei-Forenbeiträge (strunz-alter, mietrechtsiegen), SEO-Mietrechtsseiten (tenant-rights). Query 2: „verbraucherzentrale Treppenlift Vermieter" → VZ-Ratgeber, VZ-Entscheidungshilfe-PDF (2024-09), Vergleichsportale.

Lücke: Alle Konkurrenten vermitteln Anfragen oder werben für Anbieter; die Gesetzestexte werden paraphrasiert statt zitiert; keines der Portale trennt sauber zwischen Miete (§ 554 BGB), Eigentumswohnung (§ 20 WEG) und gemeinsamem Treppenhaus, und keines zeigt die Reihenfolge Zustimmung → Brandschutz → Antrag → Aufmaß/Förderung als Fahrplan. Suchvolumina nicht behauptet.

## Suchintention und Abgrenzung

- Zielgruppe: Mieter, Eigentümer von Eigentumswohnungen und Angehörige, die vor der Anfrage beim Vermieter/einer Verwaltung stehen.
- Keine Kannibalisierung: `treppenlift-mieten` behandelt den Mietvertrag als Produkt, `treppenlift-kosten` die Kaufkosten, `tuerbreiten-schwellen-schnellcheck` das Messen. Diese Seite behandelt ausschließlich die Zustimmungs-/Rechtslage und den Antragsfahrplan. Interne Verlinkung über Renderer-Related-Logik (treppenlift-Cluster).
- Monetarisierung: unverändert gesperrt (keine Formulare, keine Partnerlinks vor Liftstar-Kanalfreigabe).

## Quellenkette (Ledger: research/mietwohnung-ledger.json, alle 7 Quellen mit Verbatim-Evidenz)

Artikel-Nummerierung = Ledger-IDs 1–7. Abrufe 2026-10-16 via curl (HTTP 200):

1. § 554 BGB, gesetze-im-internet.de/bgb/__554.html — Anspruchsgrundlage, Zumutbarkeitsvorbehalt, Sicherheitsleistung (Abs. 1 S. 3), Unwirksamkeit abweichender Vereinbarungen (Abs. 2). Evidenz: research/evidence/bgb554-mietwohnung.{html,txt}.
2. § 20 WEG, gesetze-im-internet.de/woeigg/__20.html — Beschluss (Abs. 1), Anspruchsvariante für Menschen mit Behinderungen (Abs. 2), Zustimmungserfordernis Betroffener (Abs. 3), Grenze (Abs. 4). Evidenz: weg20-mietwohnung.{html,txt}. (URL-Kürzel `woeigg`, nicht `weg`.)
3. § 40 SGB XI, gesetze-im-internet.de/sgb_11/__40.html — Abs. 4 (subsidiär, Ermessen, 4.180 € je Maßnahme), Abs. 7 (3/5 Wochen-Fristen, Genehmigungsfiktion bei fehlender Begründung). Evidenz: sgb11-40-mietwohnung.{html,txt}.
4. Verbraucherzentrale-Ratgeber Treppenlifte (Festpreis/20-%-Regel, Mehrparteienhaus-Zustimmung, Baugenehmigung je Bundesland, Planungsfragen, Problemfelder-Liste). Evidenz: vz-treppenlifte-mietwohnung.txt.
5. Verbraucherzentrale-Entscheidungshilfe PDF (2024-09): „Wohnen Sie zur Miete, so müssen Sie die Erlaubnis des Eigentümers einholen. In einem gemeinschaftlichen Treppenhaus müssen die Miteigentümer oder andere Mieter vor Einbau ebenfalls zustimmen." Evidenz: vz-entscheidungshilfe-mietwohnung.txt.
6. pflege.net Treppenlift in der Mietwohnung (Vergleichsportal, enthält Anfrage-Funnel — als solche gekennzeichnet): Anspruchseinordnung, Brandschutz als häufigster Ablehnungsgrund, konkreter Antrag (Liftmodell/Fachfirma/Stromversorgung), Rückbaupflicht. Evidenz: pflegenet-mietwohnung.txt.
7. treppenliftwissen.de (Fachportal): Sicherheitsleistung getrennt von Kaution, AG Pankow/Weißensee (11.10.2012) — als Portalangabe ohne eigene Volltextprüfung wiedergegeben, Erlaubnis vor Förderantrag. Evidenz: treppenliftwissen-mietwohnung.txt.

Citation-Gate: `sources.py verify` am Ledger mit `--evidence` ausgeführt (Fehler bei erstem Quote-Login-Bug und einem paraphrasierten Quote — beide korrigiert, alle Zitate verbatim verifiziert gegen die gespeicherten Abrufe).

## Rechtliche Einordnung im Artikel (bewusste Grenzen)

- Gesetzestexte wörtlich, mit Quellenlink; Interpretationen als eigene Einordnung mit `*` markiert.
- AG-Pankow-Urteil nur als Fachportal-Angabe mit ausdrücklichem Hinweis, dass der Volltext nicht geprüft wurde.
- Keine Rechtsberatung, keine Erfolgszusage beim Vermieter, keine Zustimmungs- oder Rückbauformulierungen als Muster.
- Keine Gesundheitsdatenabfrage, keine Formulare.

## Bild

`assets/images/treppenlift-mietwohnung-zustimmung.svg` (1000×780, viewBox identisch, XML validiert): Vier-Schritte-Fahrplan (Wohnsituation → Brandschutz → Schriftlicher Antrag → Aufmaß/Förderung) plus Hinweisleiste „Zustimmung ist Voraussetzung — auch für die Förderung". Rechtsstand-Zeile mit geprüften Normen und Datum. Visuelle Prüfung: Render via Chromium-Headless (1000×780) + Sichtkontrolle — keine Überlappungen, keine abgeschnittenen Texte, Pfeile korrekt. Alternativrender via qlmanage war 1000×1000 gequetscht (Thumbnail-Limit des Tools) — Chromium-Render ist maßgeblich. KI-Kennzeichnung im sichtbaren Caption + in title/desc. Manifest-Eintrag in research/image-manifest.json.

## Renderer-Fix (getrennt dokumentiert, im selben Commit)

`article-renderer.mjs` ignorierte das Feld `paragraphs_after` — der Schlussabsatz der Beispielrechnung des Artikels `treppenlift-mieten` (Break-even 23,6 Monate, Zuschuss-Hinweis) fehlte auf der Live-Seite seit Deploy 2026-10-15 (nur im Bild-Alt-Text vorhanden). Fix: Renderer rendert `paragraphs_after` nach der Tabelle. Verifiziert im Build-Output (`genauer: 23,6` jetzt im HTML). Betroffene Live-Seiten: nur `treppenlift-mieten` (einziger Artikel mit `paragraphs_after`).

## Gates

- `npm run build:launch` (32 Seiten), `INDEX=1 python3 test_site.py` PASS, `python3 test_articles.py` PASS (Zähler 12), `npm run test:measurement` PASS, `npm run test:consent` 13/13 PASS.
- Artefakt-Checks auf dist/treppenlift-mietwohnung.html: robots index,follow; 1 H1; kein Formular; IMG mit Dimensionen; 7 Quellen; 6 FAQs; TOC 8 Einträge; Article-Schema; KI-Caption; ~2.500 Wörter (roh inkl. Navigation).
- Mobil: Layout über Responsive-Design des Renderers; visuelle Kontrolle des SVG bei 1000×780. Keine separaten Mobil-Screenshots in diesem Lauf — Renderer/Design unverändert gegenüber dem letzten Mobil-Check.
