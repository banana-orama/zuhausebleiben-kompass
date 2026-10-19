# Recherche- und Freigabeprotokoll: Bodengleiche Dusche im Altbau (Briefing 6, Phase 1)

Datum: 2026-10-19 · Lauf: Cron (milo) · Status: **veröffentlicht** (Launch-Index, Formular weiter deaktiviert)

## 1. Briefing und Suchintention

Briefing 6 laut SEO-STRATEGIE.md: „Bodengleiche Dusche im Altbau: technische Grenzen ohne
Fern-Diagnose." Zielgruppe: ältere Menschen und Angehörige, die vor der Beauftragung wissen
wollen, ob der Umbau im eigenen Altbau überhaupt geht — und was stattdessen geht.

Nutzerfrage: „Ist eine bodengleiche Dusche in MEINEM Altbau möglich, was wird geprüft, was
kostet es, wer zahlt?"

## 2. SERP-Check (2 Queries, 2026-10-19)

Q1 „bodengleiche Dusche im Altbau möglich Aufbauhöhe Abfluss", Q2 „bodengleiche Dusche Altbau
Probleme Leitung Abfluss hängende Decke". Befund:

- 4 direkte Konkurrenten zum Thema (noa-haustechnik, fliesenwerker, haustechnik-krause,
  fliesen-barretta): drei Handwerker-/Vermittlungsseiten mit Callback-/Angebots-Funnel und
  400–3.500 Wörtern, plus ein Fachportal-Beitrag (haustec 2019) für Profis (Fallstudie
  „Abwasser bergauf", Produktperspektive).
- Rest Q2: Rohrreinigungs-Dienstleister (verstopfter Abfluss — andere Intention).
- Kein Wettbewerber bietet Betroffenen einen vollständigen Fahrplan: alle vier Prüfentscheidungen
  (Aufbauhöhe, Fallrohr, Decke/Konstruktion, Norm-Zielgröße) + Warnsignale + Reihenfolge
  Förderung + Mietwohnung/Eigentum-Verzweigung + druckbare 10-Punkte-Fragenliste.
-Verbesserung: normnahe Einordnung mit Fachportal-Kennzeichnung (keine Normgarantie),
  Anbieter-/Studienzahlen sauber getrennt, konkrete Gesprächsfragen, KfW-Lage zum Abrufdatum.

## 3. Quellenkette

Ledger mit Verbatim-Evidenz (29 Zitate, maschinell gegen abgerufene Volltexte verifiziert):
`research/altbau-dusche-ledger.json`. Roh-Abrufe: Scratch `altbau-batch/` (curl, 2026-10-19).

1. § 40 SGB XI (gesetze-im-internet.de) — Ermessensformel, 4 180 €/16 720 € (geschützte
   Leerzeichen; entities dekodiert) ✓
2. BMG Zuschüsse zur Wohnungsanpassung — PG 1–5, bis zu 4.180 € ✓
3. KfW 455-B — Antragstopp wegen ausgeschöpfter Mittel; laufende Anträge/Zusagen reserviert ✓
4. KfW 159 — bis 50.000 €/Wohneinheit, Haushaltsmittelvorbehalt, Fachunternehmen;
   FAQ: „Kombination der Förderungen für die gleiche Maßnahme ist nicht möglich" +
   Ausnahme verschiedene Maßnahmen (Badumbau ≠ Treppenlift) ✓
5. nullbarriere.de DIN 18040-2 Bad/WC (Fachportaldarstellung) — niveaugleicher Übergang,
   max. 2 cm mit Abschrägung, Gefälle 0,5–1,5 % (2 % nicht wesentlich überschreiten),
   abgehängte Decke im Bestand, Membran-Duschwasserpumpe ✓
6. barrierefreies-bad.de (Fachportaldarstellung, 24.08.2026) — 120×120/150×150,
   „Altersgerecht" kein Normbegriff, Restschwelle 7–15 cm ✓
7. ZVSHK Machbarkeitsstudie Pflegebad (PDF) — Schlauchbad < 5 qm als Altbau-Mustergrundriss,
   schwellenlos zugängliche Dusche als Mindestanforderung, Kostenordnung 25 Tsd./15 Tsd. € ✓
8. haustec.de (Fachportal, 24.06.2019) — Wanne ca. 20 cm über Boden, Ablauf min. 5 cm darunter,
   ca. 25 cm Hub im Beispiel, Förderhöhe 1,3 m, ca. 30 l/min (Produktangaben gekennzeichnet) ✓
9. § 554 BGB — Anspruch auf Erlaubnis, Zumutbarkeitsgrenze ✓
10. Fliesenwerker (Fachbetriebs-FAQ, Anbieterangabe gekennzeichnet) — extraflache Systeme
    ab ca. 6,5 cm, Holzbalkendecke konstruktive Maßnahmen, flache Alternative ✓

Zahlenlogik mit python3 geprüft: 20+5=25 (haustec-Beispiel), 4×4.180=16.720 (SGB XI),
2×120=240<300 (Bewegungsfläche vs. 150er-Logik konsistent dargestellt).

## 4. Grenzen, die der Artikel zieht

- Keine Fern-Diagnose: Machbarkeit ausschließlich durch Vor-Ort-Messung.
- DIN-18040-Werte nur als Fachportaldarstellung und Planungsziel, keine Bestandspflicht.
- Anbieter-/Produktzahlen (6,5 cm; 1,3 m; 30 l/min) ausdrücklich als solche gekennzeichnet.
- Keine Marktmittelwerte; Studien-Kostenordnung (ZVSHK) als Einordnung, nicht als Preisangabe.
- Keine Förderzusage; KfW-455-B-Stand mit Abrufdatum; Kombinationsverbot mit KfW-Wortlaut.
- Mietrecht nur als Verweis auf § 554 BGB + Verlinkung des Mietwohnung-Ratgebers; keine
  Rechtsberatung im Einzelfall.
- Keine Gesundheitsdaten, keine Formulare, keine Partnerzusage, keine Test-/Erfahrungserfindung.

## 5. Bild

`assets/images/bodengleiche-dusche-altbau-pruefpunkte.svg` (1000×780, eigene SVG nach
Hausstil, KI-Illustration gekennzeichnet, title/desc, Quellenstand im Bild). Sichtkontrolle:
Chromium-Render 1000×780, alle 4 Karten vollständig, keine Überlappung/Ränder (Screenshot
geprüft). Manifest-Eintrag mit Provenance/Limitations ergänzt.

## 6. Freigabeprüfung (Gate)

- [x] SERP dokumentiert, Verbesserung benannt (Abschnitt 2)
- [x] Primär-/Fachquellen verbatim belegt (Ledger, 29/29 OK)
- [x] Keine erfundene Expertise; KI-Unterstützung im Renderer-Fuß sichtbar
- [x] Direkte Antwort am Anfang, Sie-Ansprache, keine Angstwerbung
- [x] Bild: eigenes Schema, geprüft, Manifest, Alt-Text
- [x] Title/Description/H1/Struktur; ein H1 (test_site)
- [x] Build+Tests: test_site PASS (beide Modi), test_articles 17/17, consent 13/13,
      measurement PASS, Key-Content-Assertion 0 FAILS (alle Absätze/Zellen/FAQs/Anker im HTML)
- [x] Mobile 390 px: Layout/Typo/CTA geprüft; H1-Darstellung identisch zur Live-Baseline
      (treppenlift-mietwohnung); Bild-Blank im lokalen Screenshot ist Abruf-Artefakt der
      noch nicht deployten Produktions-URL — Beweis über Live-Readback nach Deploy
- [x] Keine Abweichung von Betriebsregeln (keine Partnerlinks/Formulare, kein KI-Freispruch)

Ergebnis: **PASS** → Status editorial-reviewed-preview, Launch-Build enthält den Artikel.
