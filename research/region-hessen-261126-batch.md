# Batch 30 (2026-11-26): Region Hessen — fünfte Region (Screen Hessen/NDS, Parent-Live-Verify, Build)

Cron-Lauf 09:23. Kein neuer Artikel (41 unverändert); Content-Einheit = fünfte Region
nach dem NRW/Bayern/Sachsen/BW-Muster (launch-state 25.11.: „Fünfte Region
(Hessen/Niedersachsen-Screen) oder Kernartikel-Refresh nach GSC-Daten", GSC weiter
sitzungs-blockiert).

## Screen (2 parallele Subagenten, Belege-only)

- **Hessen: belegbar** — Weg 2 = „Behindertengerechter Umbau von Wohneigentum“
  (Richtlinie HMWEVW 14.12.2021/01.09.2023, Bewilligung WIBank): **Zuschuss, kein
  Darlehen**, bis 50 %, förderfähig bis 30.000 €/WE → max 15.000 €/WE;
  maßnahmenspezifische Höchstbeträge (Bad 5.500/Küche 5.500/**Lift-/Aufzugseinbau
  6.500**/sonstige je 3.000 €, Produktseite); Mindestausgaben 1.500 €; Bearbeitungsentgelt
  1 %/min 25 €; Auszahlung nach Schlussabrechnung; GdB ≥ 50 ODER Pflegegrad ≥ 2;
  **keine Einkommensgrenze** („Einkommen“ 0× in RL, Absenz maschinell geprüft);
  Anrechnung anderer Stellen (Pflegekasse!) statt Addition; Vorhabensbeginn = Abschluss
  Liefer-/Leistungsvertrag; Dringlichkeitsauswahl + Jahreskontingente, Volumen 2025
  4,0 Mio €; **Treppenlift 0× auf Produktseite UND RL** (benannt: Treppenschrägaufzug,
  Plattformlift). Weg 3: **LWV Hessen** (nach Schulausbildung), 21+5=26
  Organisationseinheiten, **Wohnraum-Leistungsseite nennt Treppenlift explizit (1×)**,
  Subsidiarität inkl. WIBank. Bericht `research/region-screen-261126-hessen.md`,
  Ledger 20 Quellen, Verbatim-Check 155/155.
- **NDS: belegbar mit engerer Kennzeichnung** — NBank „Barrierereduzierende
  Modernisierung“ (RL 2026): „Treppenlift“ 0× in ALLEN offiziellen Dokumenten, Eignung
  nur über nicht-amtliche Auslegung (FWG e.V.); Mieter leer aus. Bericht
  `research/region-screen-261126-nds.md`, Ledger 20 Quellen, Check 108/108.
- **Entscheidung: Hessen** — einziges Bundesland des Screens mit amtlich benannter
  Lift-Position (Höchstbetrag-Zeile) + EGH-Seite mit expliziter Treppenlift-Nennung;
  keine Einkommensgrenze (schlanker korrekt darstellbar); NDS nur mit
  Interessenkennzeichnung belegbar → für die fünfte Region zurückgestellt.

## Parent-Verifikation (26.11., frische Abrufe, `research/evidence/region-hessen-261126/`)

- `parent_verify_live.py` — **55/55 PASS** (jede Kernbehauptung frisch gegen
  Live-Originale: WIBank-Produktseite, RL-PDF in 3 pdftotext-Modi inkl. **-raw für die
  Spalten-Interleave-Heilung**, LWV, VP-EGH/-Pflegekasse, soziales.hessen.de
  (5 kreisfreie Städte verbatim), pflege-in-hessen, HMWEVW, wohnen-im-alter,
  Bad-Homburg, KfW 455-B/159, § 113/§ 77 SGB IX (`sgb_9_2018`-Shortcode), § 40 SGB XI
  („4 180“/„16 720“ geschützt)).
- `verify_quotes.py` — **28/28 PASS**: jedes im JSON verwendete Verbatim-Fragment
  einzeln. **Fund dabei:** Produktseite schreibt „Lift-/**Aufzugseinbau**“ (mit s) — der
  Screen-Bericht hatte „Aufzugeinbau“ leicht falsch transkribiert; JSON nutzt die
  verifizierte Schreibweise. De-Hyphenation mit Stopword-Heuristik („lieferungs- und“
  bleibt, „ab- schluss“ → „abschluss“).
- § 554 BGB heute frisch: Neufassung-Wortlaut „nicht **zugemutet werden kann**“ —
  die BW-Region-Seite paraphrasiert („nicht zumutbar ist“, ohne Anführungszeichen,
  sachlich korrekt); die Hessen-Seite zitiert exakt. Kein BW-Fix nötig, Refresh-Notiz.

## Content

`data/region-hessen.json` (Renderer-datengetrieben; generate.mjs Region-Liste +1,
Hub-Prosa/Desc auf 5 Regionen): 4 Wege, Höchstbeträge-Tabelle (10 Zeilen + Note),
5 Bullets (Rechtsanspruch/Kontingente, Vorhabensbeginn, 5-Jahres-Deckel, Anrechnung,
keine Einkommensgrenze), Antragstellen-Sektion (Magistrat/Kreisausschuss), EGH mit
Bad-Homburg als gekennzeichnetem kommunalem Vermittlungs-Einzelfall, KfW-Stand,
26 Pflegestützpunkte, Mieter-Sektion mit §-554-Wortlaut, Reihenfolgen-Bullets, 6 FAQs,
19 Quellen (checked_at 2026-11-26), Förderbeträge der Pflegekasse bewusst 0×,
0 Partner-Marker.

## Gates

- Content-Gate **111/111 PASS** (`research/verify_region_hessen_build_261126.py`,
  LAUNCH-dist: Struktur, 51 Kernwordlaute inkl. Wortlaut-Ehrlichkeits-Hinweis
  „Das Wort Treppenlift kommt auf der Produktseite und in der Richtlinie nicht vor“,
  6 FAQs, 19 Quellen-URLs, Related/CTA absolut, 10 Absenzen inkl. 0× L-Bank/Friedrichshafen,
  Hub 5-Regionen-Prosa + alte Prosa 0×, Sitemap exakt 5 Region-URLs, RSS 41).
- npm test **EXIT 0** (Playwright 22, Partner A–F ALL PASS, titles_meta ALL PASS).
- verify_checklists_build ALL PASS (nach build:launch).
- Mobile 390 px **0 px Overflow** (`research/verify_region_hessen_mobile_261126.py`,
  2 Tabellen im Scroll-Muster 346 px, 3 CTAs, 6 FAQs, 19 Quellen) + **Vision 2×**
  (Mobil-Top sauber; Höchstbeträge-Tabelle alle 10 Zeilen vollständig lesbar).

## Deploy

Siehe launch-state 26.11. (Commit/CI/Live-Readback/IndexNow dort nachgetragen).

## Offene Punkte / Refresh-Trigger

1. Frankfurt-Modernisierungsprogramm (kommunaler Kandidat) Cloudflare-blockiert —
   in einer Browser-Sitzung nachholen, falls Frankfurt später als kommunales Beispiel
   gewünscht ist (URL im Hessen-Ledger).
2. WIBank-Antragsvordrucke roh gesichert, inhaltlich ungeprüft (Formular-Felder/Fristen).
3. Höchstbetrags-Kombination (Lift+Bad im selben Antrag) = Auslegungsfrage — bewusst
   keine kombinierte Beispielrechnung publiziert.
4. Refresh-Trigger: RL-/Produktseite-Konditionen (Jahreskontingent/Dringlichkeit),
   KfW-455-B-2027 (bestehender Trigger), § 40 SGB XI Reform (PNOG, bestehender Trigger).
5. NDS-Screen steht vollständig in `research/region-screen-261126-nds.md` — Basis für
   eine mögliche sechste Region (dort dann die FWG-e.V.-Interessenkennzeichnung nach
   dem Sachsen-Muster führen).
