# Recherche- und Freigabeprotokoll: Badumbau-Angebote vergleichen (Briefing 7, Phase 1)

Datum: 2026-10-19 · Lauf: Cron (milo) · Status: **veröffentlicht** (Launch-Index, Formular weiter deaktiviert)

## 1. Briefing und Suchintention

Briefing 7 laut SEO-STRATEGIE.md: „Badumbau-Angebote vergleichen: Abdichtung, Rückbau und
Zusatzarbeiten." Zielgruppe: ältere Menschen und Angehörige, die mehrere Angebote vor sich
haben und entscheiden müssen, ohne die Technik selbst beurteilen zu können.

Nutzerfrage: „Wie mache ich zwei oder drei Badumbau-Angebote wirklich vergleichbar — und
welche Regeln (Preisbindung, Abschläge, Zusatzarbeiten, Gewährleistung) schützen mich?"

## 2. SERP-Check (2 Queries, 2026-10-19)

Q1 „Badumbau Angebote vergleichen Wanne Dusche umbauen Angebot Kosten Aufstellung",
Q2 „barrierefreier Badumbau Angebot Abdichtung DIN 18534 Rückbau Zusatzarbeiten Elektro
Zonen". Befund:

- Q1: 7 Treffer, ausschließlich Kosten-Leitfäden (3.000–8.000 € Spannen, „Angebot anfordern"-
  Funnels: auftragsglueck, badumbauheld, renovierung-ratgeber, pflege-panorama,
  barrierefrei-profis, altersgerecht-modernisieren, pflegeheimat24). Kein Wettbewerber
  liefert eine Vergleichsmechanik (Positionen, Preisbindungstypen, Abschlagsregeln).
- Q2: DIN-18534-Fachquellen (din.de Verbraucherrat, Schlüter, einhornwerke-Merkblatt mit
  Verweis auf die Neufassung 2025-10; meisterfliesen nennt Oktober-2025-Update), keine
  konsumentenorientierte Aufbereitung für den Angebotstisch.
- Suchresultat-Totals sind keine Direktkonkurrentenzählung; bewertet wurde die
  Intentionsabdeckung.

Verbesserung: Erster Ratgeber, der die Vergleichsmechanik komplett macht —
Vergleichsbasis → Positionstabelle → Abdichtungsfragen (DIN 18534, Klassen W1-I/W2-I,
fugenlos = Vereinbarungspflicht) → Preisbindung (KV unverbindlich + 15–20-%-Hinweisschwelle
vs. Festpreis) → Zusatzarbeiten (§ 650b/650k BGB) → Abschläge (§ 632a BGB) → Gewährleistung
(§ 634a BGB, 2/5 Jahre ab Abnahme) → druckbarer Fragenkatalog pro Betrieb.

## 3. Quellenkette

Ledger mit Verbatim-Evidenz (25 Zitate, maschinell gegen abgerufene Volltexte verifiziert):
`research/badumbau-angebote-ledger.json`, Verifikationsskript
`research/verify_badumbau_ledger.py` (25/25 OK). Roh-Abrufe: Scratch `badumbau-batch/`
(curl, 2026-10-19).

1. Verbraucherzentrale (Stand 10.12.2025) — 2–3 Angebote, KV unverbindlich +
   15–20-%-Hinweis + Kündigungsrecht, Festpreisbindung, Vor-/Nach-/Nebenarbeiten,
   Einzelpositionen auf Rechnung, Mängel sofort schriftlich ✓
2. § 632a BGB — Abschlag nur für erbrachte/geschuldete Leistungen, Aufstellungspflicht,
   Verweigerungsrecht, Beweislast bis Abnahme beim Unternehmer ✓
3. § 650b BGB — Unternehmer verpflichtet zu Mehr-/Mindervergütungs-Angebot ✓
4. § 650k BGB — Baubeschreibung wird Vertragsinhalt, Auslegung zu Lasten des
   Unternehmers, Fertigstellungszeit/Dauer verbindlich im Vertrag ✓
5. § 634a BGB — 2 Jahre Werk / 5 Jahre Bauwerk, Beginn mit Abnahme ✓
6. DIN e. V. Verbraucherrat — Neufassung Oktober 2025, Planung/Umsetzung/Wartung,
   Gewerke-Koordination ✓
7. Schlüter-Systems (Hersteller-Fachdarstellung) — Klassen je Fläche, W0-I bis W3-I,
   W2-I: nur feuchtigkeitsunempfindliche Untergründe ✓
8. Einhorn-Werke-Merkblatt (Stand 09/2026, Norm 2025-10) — Wand meist W1-I, Boden
   bodengleiche Dusche W2-I, Zuordnung durch Planer, fugenlos nicht geregelt =
   Vereinbarungspflicht, 2017er-Merkblätter überholt ✓
9. § 40 SGB XI — 4 180 € Grenze (Abs. 4); heute im Recheck-Lauf erneut live bestätigt
   (research/foerderstatus.md, Snapshot foerder-191026-sgb40) ✓

Keine Marktpreisdaten erhoben — bewusst keine Durchschnittspreise erfunden (Betriebsregel).

## 4. Grenzen, die der Artikel zieht

- Allgemeine Orientierung und Gesprächsvorbereitung; keine Rechtsberatung und keine
  juristische Bewertung konkreter Verträge (explizit in Abschnitt 5 und FAQ).
- Normangaben (DIN 18534, Klassen) nur als Fach-/Herstellerdarstellung mit
  Kennzeichnung; Zuordnung trifft der Planer.
- Keine Aufforderung, Angebote mit gesetzlichen Fristen zu „unterbieten"; Gewährleistung
  nur als Abgleich mit schriftlicher Betriebsangabe.
- Keine Förderzusage; § 40 Abs. 4 SGB XI nur als Betragsgrenze mit Ermessenshinweis.
- Keine Gesundheitsdaten, keine Formulare, keine Partnerzusage, keine Test-/Erfahrungserfindung.
- KI-Unterstützung im Renderer-Fuß sichtbar; keine eigenen Baustellen-/Produkttests.

## 5. Bild

`assets/images/badumbau-angebote-vergleich.svg` (1000×780, eigene SVG nach Hausstil,
KI-Illustration gekennzeichnet, title/desc, Quellenstand im Bild). Sichtkontrolle:
Chromium-Render 1000×780 — alle 4 Karten vollständig, Hinweisbox im Bild, keine
Überlappungen (Screenshot geprüft). Manifest-Eintrag mit Provenance/Limitations ergänzt.

## 6. Abgrenzung (No-Cannibalization-Gate)

- wanne-zur-dusche: Produktentscheidung (bodengleich/niedrig/umfassend) + Bauablauf;
  Angebotscheck dort nur ein Abschnitt ohne Quellenmechanik. Verlinkt hin.
- bad-umbau-barrierefrei: Gesamtplanung/Entscheidungsmatrix; Kostenvergleich nur als
  Checklistenskizze ohne Rechts-/Normbelege. Verlinkt hin.
- Dieser Artikel: die dedizierte Vergleichsmechanik (intentional-distinct, keiner der
  Bestandsartikel benennt KV-vs-Festpreis, Abschläge, § 650b/k, § 634a oder DIN-18534-
  Nachfragen im Angebot). Related-Links bleiben im Bad-Cluster.

## 7. Freigabeprüfung (Gate)

- [x] SERP dokumentiert, Verbesserung benannt (Abschnitt 2)
- [x] Primär-/Fachquellen verbatim belegt (Ledger, 25/25 OK, Skript-Ausgabe im Lauf)
- [x] Keine erfundene Expertise; KI-Unterstützung im Renderer-Fuß sichtbar
- [x] Direkte Antwort am Anfang, Sie-Ansprache, keine Angstwerbung
- [x] Bild: eigenes Schema, geprüft, Manifest, Alt-Text
- [x] Title/Description/H1/Struktur; ein H1 (test_site)
- [x] Build+Tests: test_site PASS (beide Modi), test_articles 18/18, consent 13/13,
      measurement PASS, Key-Content-Assertion 0 FAILS (alle Absätze/Zellen/FAQs im HTML)
- [x] Mobile 390 px: Layout/Typo/CTA/Tabelle geprüft (Screenshots); Bild-Blank im lokalen
      Screenshot ist Abruf-Artefakt der noch nicht deployten Produktions-URL — Beweis über
      Live-Readback nach Deploy
- [x] Renderer: specialMap-Eintrag (Early-CTA „Badumbau planen" → bad-umbau-barrierefrei);
      Related-Links ausschließlich Bad-Cluster (bad-umbau-barrierefrei,
      bodengleiche-dusche-altbau, treppenlift-zuschuss via Cluster-Regel)
- [x] Keine Abweichung von Betriebsregeln (keine Partnerlinks/Formulare, kein KI-Freispruch)

Ergebnis: **PASS** → Status editorial-reviewed-preview, Launch-Build enthält den Artikel.
