# Briefing 22 — Unseriöse Treppenlift-Anbieter erkennen (Batch 18, 10.11.2026)

## SERP-Auswahl (GSC im Cron weiter ohne Google-Sitzung)

Kandidaten this run: (A) unseriöse Anbieter/Kaltakquise, (B) Pflegebett Kostenübernahme.
Verworfen (B): SERP 8/10 institutionell dicht (gesund.bund.de, BMG, VZ ×3, Kassen-Seiten),
Bestand deckt die Hilfsmittel-Route in hilfsmittel-pflegekasse-uebernahme (grep-Hit "Pflegebett").

Gewählt (A), exakte Intent-Felder:
- Query-Feld „Treppenlift Kaltakquise/Fangprämie/unseriös": organisch ~4 Seiten — test.de
  Unterseite „windige Anbieter" (sichtbar, kein Paywall auf der Unterseite), 2–3 Anbieter-Magazine
  (prolift, treppenlifto, regional-treppenlift = Interessenkonflikt), 1 Forum; 4 Bing-Ads davor.
  Kein dedizierter Konkurrenz-Ratgeber zu Verkaufstaktiken. Der „Fangprämie"-SERP besteht
  fast nur aus Ads/Broker-Seiten — das SERP selbst zeigt das Phänomen.
- frischer Fall: VZ-BW-Verbandsklage gegen Mobilae (8.10.2026, OLG Hamm, 18 Klauseln),
  5 Tage nach Ereignis nur von Anbieter-News + Forum aufgegriffen, von keinem Ratgeber konsolidiert.
- Bestand: „Kaltakquise/Fangprämie" 0 Abschnitte (grep über 32 Artikel); Vertragsklausel-Winkel
  liegt bei treppenlift-mieten (Mobilae dort als Vertragsprüf-Kontext) — Abgrenzung: dieser
  Artikel = Verkaufstaktiken + Rechte + Fall, nicht Klauselprüfung je Position.
- Improvements: Taktiken→Gesetz-Mapping (§§ 4a/5a/7 UWG, § 312g BGB) hat kein Konkurrent,
  Betroffenen-Umfrage mit Methodik-Caveat, Klausel-Fall mit Klausel-Zitaten + Unschuldsvermutung.
- Verworfene Kandidaten der Vormäufe unverändert (Wartung, Haltegriffe-Bad, Schwellenrampe,
  Kurzzeitpflege, Entlastungsbetrag, Pflegezeit, Pflegegrad-Höherstufung, Duschsitz-Kasse,
  Kurventreppe, Akku, Treppensteiger).

## Quellen (9, alle 10.11.2026 live abgerufen, Evidenz research/evidence/unserioese-101126/)

1. VZ-Ratgeber Treppenlifte (10711) — neutraler Kern (Barrieren, Verkaufsgespräch-Warnungen,
   Werkvertrag/BGH, Widerruf 12M+14T, Portale-Warnung, Hausbesuch, Festpreis+20 %).
2. VZ-Umfrage-Auswertung PDF (10.12.2020) — 125 Betroffenen-Bögen/16 Länder: ⅓ sofort
   unterschrieben, ⅓ nicht über Widerruf/AGB informiert, 46/123 ohne Planungsunterlagen,
   29/125 gebrochene Werbeversprechen („rund ein Viertel"), 93/104 Mängel, 4/5 Gewährleistungs-
   /Garantieprobleme, „Abzocke"-Benennung für Wartungsverträge, Fünf-Marken-Fazit,
   „PractiComfort (jetzt: mobilae)". Methodik-Caveat im Artikel: nur gemeldete Problemfälle.
3. test.de Unterseite „So erkennen Sie windige Anbieter" — Taktik-Details sichtbar:
   Verzicht-Trick + Kundenstimme („An keiner Stelle war erkennbar…"), Storno-Fall,
   Anzahlung-Warnung, Dauer-Akquise, Auslands-Firmensitz, Pauschalpreis, gratis-Voranschlag-Meinung.
4. VZ-Verbandsklage-Seite — Unterlassungsklage, AZ I-13 UKl 17/26, Einreichung 08.10.2026,
   18 Klauseln (programmatisch gezählt), Klausel-Zitate: Gewährleistungsausschluss,
   65 %/25 %-Pauschalen, „Der Kunde stimmt der Weitergabe seiner Daten zu.",
   „Wir verarbeiten die Daten nach EUDGV."
5. verbraucherschutzforum.berlin (11.10.2026) — OLG Hamm + Neuss + „18 Vertragsklauseln"
   + Verlauf-Caveat („Erst der weitere Verlauf des Verfahrens…").
6–9. Gesetzestexte (BMJ gesetze-im-internet, Kürzel uwg_2004): § 4a UWG (Aggressivität +
   Alter/Beeinträchtigung-Satz), § 7 UWG (Belästigung, Telefonanruf ohne ausdrückliche
   Einwilligung „stets anzunehmen"), § 5a UWG (Unterlassen, kommerzieller Zweck kenntlich),
   § 312g BGB (Widerruf außerhalb von Geschäftsräumen; Abs. 2 Nr. 1 maßgefertigte Ware
   als ehrliche Grenze, Verweis auf finanzierungs-Ratgeber).

Ledger: research/unserioese-101126-ledger.json — 105/105 Pässe
(research/verify_unserioese_101126.py): 62 Verbatim-Zitate + 4 Umfrage-Chart-Arithmetik-Zeilen
(83+37+5 / 43+81+1 / 29+93+3 / 77+46+2 = je 125) + Klausel-Count 18 + Integrität
(alle [n] auf 1..9, jede Quelle ≥1×) + 24 Kernzahlen + 9 Absenz-Gates.

## Dokumentierte Nuancen statt Glättung

- N1 Umfrage misst nur gemeldete Problemfälle (Selection) und datiert 12/2020 — im Artikel.
- N2 Maßanfertigte Schiene kann durch § 312g Abs. 2 Nr. 1 (Ausnahme) durchschlagen —
  Grenze benannt, Verweis auf treppenlift-finanzierung (dort § 312g-Detail).
- N3 Klage ≠ Urteil (Unschuldsvermutung + Verlauf-Zitat); keine Firma wird als unseriös
  etikettiert — Absenz-Gate „unseriöser Anbieter Mobilae" = 0.
- N4 test.de gratis-Voranschlag ist Meinungsposition, als solche gekennzeichnet.
- N5 Förderbeträge bewusst NICHT wiederholt (0 × „4.180"/„16.720" im HTML, Gate), nur
  Verweis auf treppenlift-zuschuss.

## Grafik

assets/images/treppenlift-unserioese-anbieter-warntafel.svg — 6 nummerierte Kacheln
(Warnsignal + Kurzregel) + Quellen-Footer, Chip-Grid ohne Callouts. Gates: getBBox-Overflow +
Pairwise + Chip-Kontext 0 Issues (research/verify_unserioese_svg_mobile_101126.py, Chromium),
Mobile 390 px 0 px Overflow, Vision-Inspektion sauber (Screenshot evidence/unserioese-101126/
svg-screenshot.png). KI-unterstützt gekennzeichnet.

## Renderer/Infra

- article-renderer.mjs specialMap +1 (Early-CTA „Angebote sauber vergleichen" →
  treppenlift-angebote-vergleichen; Lift-Cluster hat keine aktiven Placements, bewusst
  0 Partner-Marker auf dem Artikel).
- data/cross-links.json links+rationale +1 (angebote-vergleichen, mieten, kosten — lift-intern).
- research/llms-txt.py SUMMARIES + SECTION_MAP (Treppenlift-Sektion) +1.
- isLift-Regex deckt den Slug via treppenlift-Präfix automatisch ab (keine Regex-Änderung).
- Testzähler: test_articles 32→33; verify_checklists_build RSS 32→33; test_partner_links A3 ≥31→≥32.

## Gates

- research/verify_unserioese_101126.py: 105/105 PASS (inkl. Arithmetik + Klausel-Count)
- research/verify_unserioese_content_101126.py: 0 FAILS (LAUNCH-dist; jeder JSON-Key im HTML,
  Related 3× Lift-Cluster in Cross-Reihenfolge, CTA + Label, 0 Partner-Marker/awin/sponsored,
  SVG kopiert, Anker 1..9, 0 Förderbeträge im HTML). Lektion: `from html import unescape`
  statt `html.unescape` am String (Variable schattet Modul) + `& Co.`-Escape in Bullets.
- research/verify_unserioese_svg_mobile_101126.py: ALL PASS (0 Geometrie-Issues, 0 px Mobile)
- npm test: EXIT 0 (test_site 58 Seiten, test_articles 33, cross_links, titles_meta,
  Playwright 21 passed, Partner A–F ALL PASS)
- verify_checklists_build.py: ALL PASS (LAUNCH-dist, RSS 33)
- Deploy/Live-Readback/IndexNow: siehe launch-state 10.11.
