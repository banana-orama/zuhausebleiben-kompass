# Förderstatus-Prüfung: Offizielle Quellen gegen Live-Content

# Prüflauf-Einträge: neuester oben, Marker "AKTUELL" wandert mit.

## Prüflauf 09.11.2026, 08:20–08:52 CET (cron, autonomous) — AKTUELL

**Ergebnis in einem Satz:** Alle förderrelevanten Zahlen und Rechtsaussagen des Live-Contents stimmen zum Quellenstand vom 09.11.2026 — **null Abweichungen** (33 curl-Volltext-Assertionen PASS, Browser-Check 11/11 PASS, 37/37 offizielle URLs HTTP 200). KfW-455-B-Antragstopp unverändert; KfW-159-Bedingungen unverändert; BMG-Werte inkl. Zinspassage unverändert.

**Neue Beobachtung (kein Korrekturanlass, ledger-notiert):** Die **KfW-159-Seite zeigt gerendert erstmals einen eigenen Zinssatz: „Zinssatz: ab 3,19 % effektivem Jahreszins"** (statischer HTML-Extrakt zeigt weiterhin den Platzhalter „ab -,-- %" — der Satz wird client-seitig gerendert; Browser-Check via Chromium 09.11. belegt die 3,19 %). Kein Content-Bezug: Kein Artikel behauptet etwas über den KfW-159-Zinssatz; der einzige konkrete Zins im Live-Content ist das korrekt dem **BMG** zugeschriebene Zitat „ab 2,19 Prozent (Stand: 10. Juli 2025)" (`hilfsmittel-dusch-wc-uebernahme`, Quelle [7]) — die BMG-Seite enthält die Aussage weiterhin (09.11. PASS), das Zitat bleibt exakt korrekt. „Zinsverbilligt"-Formulierungen in bodengleiche/steuerlich-absetzen bleiben wahr. Beim nächsten Lauf: prüfen, ob die 3,19 % auch im statischen Abruf erscheinen und ob sich ein 159-Zins-Hinweis für einen der KfW-Artikel anbietet (keine Pflicht — keine falsche Aussage im Content).

**Verifiziert am 09.11.2026 (Belege `research/evidence/foerder-091126-*.html`, Skript `research/verify_foerder_091126.py`, Log `verify_foerder_091126.log`):**
- **§ 40 SGB XI** (gesetze-im-internet, ISO-8859-1): 14/14 PASS — Abs. 2 „42 Euro" ✓, Abs. 3 „zehn vom Hundert, höchstens jedoch 25 Euro" ✓, Abs. 4 „subsidiär"/Zweckformel/„4 180 Euro je Maßnahme"/„16 720 Euro"/anteilig ✓, Abs. 7 „drei Wochen"/„fünf Wochen"/„als genehmigt" ✓, Fußnote „ab dem 1.1.2025" ✓ — unverändert zu 02.11.
- **KfW 455-B**: 6/6 PASS — Antragstopp („können Sie nicht mehr beantragen", „ausgeschöpft"), „Laufende Anträge nicht betroffen", Zusage „reserviert", 2027 nur bei neuen Bundesmitteln, „noch nicht mit Ihrem Vorhaben begonnen" — unverändert. Canonical = exakt die zitierte Form (Umlaut).
- **KfW 159**: 9/9 PASS auf der Kanonikalform (Umlaut+Slash) — 50.000 €/WE, Haushaltsmittelvorbehalt, kein Rechtsanspruch, Fachunternehmen, vor Vertragsabschluss, Treppenlifte (FB 3), Kombinationsausschluss, Nachfinanzierungs-Ausschluss — unverändert. Canonical = zitierte Form.
- **BMG Zuschüsse zur Wohnungsanpassung**: 4/4 PASS (4.180/16.720 €, PG 1–5, Zweitzuschuss) + 2.090 €/Person Wohngemeinschaft ✓ + Zinspassage „ab 2,19 Prozent (Stand: 10. Juli 2025)" unverändert ✓.

**Browser-Check (Chromium, `research/browser_check_foerder_091126.mjs`, Log `browser_check_foerder_091126.log`):** 455-B 6/6 sichtbar; 159 Kanonikalform 5/5 (2 sichtbar, 3 FAQ-Needles nur im DOM — bekanntes Akkordeon-Verhalten, textContent-Fallback greift).

**Link-Status:** 37/37 im Content zitierte offizielle URLs HTTP 200 (`research/check_foerder_links_091126.py`, Log `check_foerder_links_091126.log`) — inkl. der neuen Artikel (hausnotruf-mobil, wohnumfeldverbesserung, GKV-PDF).

**Geänderte Dateien:** 16 × `content-ready/*.json` — **31 `checked_at` → 2026-11-09** (nur heute re-verifizierte Quellen § 40/455-B/159/BMG; Skript `research/bump_checked_at_091126.py`, Zeilen-Zustandsautomat, Marker decken Umlaut- UND encodierte Formen) + **7 sichtbare KfW-Prüfdatumsangaben** „2. November" → „9. November 2026" (bad-umbau ×2, bodengleiche ×2, treppenlift-zuschuss ×2 — inkl. „direkt im Browser geprüft" —, wanne ×1; durch heutigen curl + Browser-Check 11/11 gedeckt). Bewusst **nicht** hochgesetzt: Gesamtdisclaimer „Stand: 2. November 2026" in wohnumfeldverbesserung (umfasst AOK/DAK/Kassenformular/pflege.de — heute nur per Link-Status geprüft, kein Überclaiming) und alle übrigen Quellenprüfdaten. `data/content.json` unangetastet (Altentwürfe, Renderer überschreibt).

**Build/Deploy:** build:launch (50 Seiten, Mode: LAUNCH index) + test_site.py + test_articles.py + test_partner_links.py PASS. Commit `1279a39` gepusht (28 Dateien: 16 content-ready + 12 research; Parallel-Run-Churn unberührt), CI-Run 42579543595 **success**.

**Live-Readback (09.11., öffentliche URL `research/live_readback_091126.py`, Log `live_readback_091126.log`):** 7/7 ALL PASS — treppenlift-zuschuss „9. November 2026" 3×/„2. November" 0× + „geprüft 2026-11-09"-Footer; bad-umbau 3×/0×; bodengleiche 3×/0×; wanne 1×/0×; wohnumfeldverbesserung Gesamtdisclaimer „2. November" unverändert 1× (korrekt); hilfsmittel-dusch-wc BMG-Zinspassage 1×; alle Seiten robots `index,follow`, HTTP 200; Homepage `index,follow`.

**Lessons:** (1) `gh run list --json status` liefert **lowercase** Werte (`"completed"`, `"in_progress"`) — Case-sensitiver Vergleich auf `'COMPLETED'` lässt den Wait-Loop endlos laufen (Beweis kam trotzdem aus dem Log; Skript künftighin case-insensitive). (2) Cron-Sicherheitsfilter blockt inline `python3 -c` als „dangerous script execution" — URL-Kodierung/Checks immer als Skriptdatei ablegen. (3) `git add` mit einer nicht existierenden pathspec bricht VOR dem Staging ab (atomar) — gestagte Menge danach kurz verifizieren.

---

## Prüflauf 02.11.2026, 08:12–08:45 CET (cron, autonomous)

**Ergebnis in einem Satz:** Alle förderrelevanten Zahlen und Rechtsaussagen des Live-Contents stimmen zum Quellenstand vom 02.11.2026 — **null Abweichungen** (42 Volltext-Assertionen PASS per curl). Der offene Beobachtungspunkt vom 01.11. ist **geschlossen und umgesetzt**: KfW kanonikalisiert 159 auf Umlaut + trailing slash; die zitierten KfW-URLs wurden darauf normalisiert (kosmetischer Zitier-Fix, kein Inhaltsfehler — beide Formen inhaltlich identisch). BMG nennt weiterhin „ab 2,19 Prozent (Stand: 10. Juli 2025)“ (Artikel-Attribution korrekt); KfW 159 zeigt weiter keinen eigenen Satz („ab -,-- %“).

**Kanonikalbefund (offener Punkt 01.11.):** KfW 159 antwortet auf **beide** bisher zitierten Formen (encodiert + Umlaut, ohne Slash) mit **301** → Umleitung über einen **http-Zwischenschritt** auf die trailing-slash-Form (2 Hops). `<link rel="canonical">` + `og:url` der Zielseite: `…/Bestehende-Immobilie/Förderprodukte/Altersgerecht-Umbauen-(159)/` (Umlaut + Slash). 455-B: die zitierte encodiert-Form antwortet direkt 200 (kein Redirect), canonical ist ebenfalls die Umlaut+Slash-Form. → **Fix:** 8 Zitier-URLs in 4 Artikeln auf die Kanonikalform normalisiert (455-B `%C3%B6`→`ö` 4×; 159 → Umlaut+Slash 4×, davon 1× encodiert). Identischer Assertionssatz 9/9 auf alter und neuer Form (`curl -L`); Leser sparen künftig die Redirect-Kette. Keine sonstigen Referenzen auf die Altformen in tests/data/scripts.

**Verifiziert am 02.11.2026 (Volltext-Assertionen, Belege `research/evidence/foerder-021126-*.html`, Skript `research/verify_foerder_021126.py`, Log `verify_foerder_021126.log`):**
- **§ 40 SGB XI** (gesetze-im-internet, ISO-8859-1): 14/14 PASS — Abs. 2 „42 Euro“ ✓, Abs. 3 „zehn vom Hundert, höchstens jedoch 25 Euro je Pflegehilfsmittel“ ✓, Abs. 4 „subsidiär“/Zweckformel/„4 180 Euro je Maßnahme“/„16 720 Euro“/anteilige Aufteilung ✓, Abs. 7 „drei Wochen“/„fünf Wochen“/„als genehmigt“ ✓, Fußnote „ab dem 1.1.2025“ ✓ — unverändert zu 01.11.
- **KfW 455-B**: 6/6 PASS — Antragstopp („können Sie nicht mehr beantragen“, „ausgeschöpft“), „Laufende Anträge nicht betroffen“, Zusage „reserviert“, 2027 nur bei neuen Bundesmitteln, „noch nicht mit Ihrem Vorhaben begonnen“ — unverändert.
- **KfW 159**: 9/9 PASS auf **beiden** URL-Varianten (vor der Normalisierung gezogen) — 50.000 €/WE, Haushaltsmittelvorbehalt, kein Rechtsanspruch, Fachunternehmen, vor Vertragsabschluss, Treppenlifte (FB 3), Kombinationsausschluss, Nachfinanzierungs-Ausschluss — unverändert.
- **BMG Zuschüsse zur Wohnungsanpassung**: 4/4 PASS (4.180/16.720 €, PG 1–5, Zweitzuschuss) + 2.090 €/Person Wohngemeinschaft ✓ + **Zinspassage unverändert**: „…zinsvergünstigte Kredite ab 2,19 Prozent (Stand: 10. Juli 2025) bis zu einer Höhe von 50.000 Euro…“ → Artikel `hilfsmittel-dusch-wc-uebernahme` zitiert das korrekt dem BMG zu; keine Änderung nötig.

**Browser-Check (Chromium, `research/browser_check_foerder_021126.mjs`, Log `browser_check_foerder_021126.log`):** 455-B **6/6 sichtbar**; 159 auf der **neuen Kanonikalform** 5/5 — davon 2 sichtbar, 3 FAQ-Needles **nur im DOM** (eingeklappte Akkordeons). **Lesson:** `document.body.innerText` enthält eingeklappte Akkordeon-Inhalte nicht — Browser-Checks für FAQ-/Förderbereich-Needles brauchen einen `textContent`-Fallback (Skript hat beides, Layer wird je Needle ausgegeben).

**Geänderte Dateien:** 14 × `content-ready/*.json` (28 `checked_at` → 2026-11-02, Skript `research/bump_checked_at_021126.py`) + 8 KfW-Zitier-URLs → Kanonikalform (4 Artikel) + **7 sichtbare KfW-Prüfdatumsangaben** „1. November“ → „2. November 2026“ (bad-umbau ×2, bodengleiche ×2, treppenlift-zuschuss ×2 — inkl. „direkt im Browser geprüft“ —, wanne ×1; gedeckt durch den heutigen Browser-Check 11/11). Diff-Sanity: 43/43 geänderte Zeilen ausschließlich `checked_at`/kfw.de/„November 2026“, 0 Fremdzeilen. Bewusst **nicht** hochgesetzt: Gesamtdisclaimer „Abrufstand 19.10./16.10.“ (hilfsmittel-pflegekasse, rollator, pflegegrad, verhinderungspflege — deren übrige Quellen heute nicht inhaltlich neu geprüft) und historische Datumsaussagen. `data/content.json` unangetastet (Altentwürfe, Renderer überschreibt).

**Build/Deploy:** build:launch (45 Seiten, Mode: LAUNCH index) + test_site.py + test_articles.py + test_partner_links.py PASS. Commit `c916862` gepusht (nur eigene Dateien, Parallel-Run-dist-Churn unberührt), CI-Run 41404999468 **success**. Hinweis: die Mode-Angabe in der Summary-Zeile von test_site.py hängt am `INDEX`-Env-Var-Default (druckt „PREVIEW“, auch wenn LAUNCH gebaut wurde) — die verbindlichen Robots-Assertions pro Datei sind es, die greifen.

**Live-Readback (02.11., öffentliche URL):** `treppenlift-zuschuss` zeigt „2. November 2026 direkt im Browser geprüft“ + beide KfW-Links in Kanonikalform (159 Umlaut+Slash als href, 455-B Umlaut), **0** verbleibende encodiert-Formen, robots `index,follow`; bad-umbau / bodengleiche / wanne je HTTP 200 mit 2.-November-Datum, Kanonikal-URLs und 0 encodiert-Resten; Homepage `index,follow`.

---

## Prüflauf 01.11.2026, 21:16–21:30 CET (cron, autonomous)

**Ergebnis in einem Satz:** Alle förderrelevanten Zahlen und Rechtsaussagen des Live-Contents stimmen zum Quellenstand vom 01.11.2026 — **null Abweichungen** (47 Content-Assertionen PASS). Der offene Beobachtungspunkt vom 26.10. ist **geschlossen**: BMG nennt weiterhin „ab 2,19 Prozent (Stand: 10. Juli 2025)" unverändert; das Artikelzitat bleibt exakt korrekt. KfW 159 zeigt weiter keinen eigenen Satz („ab -,-- %").

**Verifiziert am 01.11.2026 (Volltext-Assertionen, Belege `research/evidence/foerder-011126-*.html`, Skript `research/verify_foerder_011126.py`):**
- **§ 40 SGB XI** (gesetze-im-internet, ISO-8859-1): 14/14 PASS — Abs. 2 „42 Euro" ✓, Abs. 3 „zehn vom Hundert, höchstens jedoch 25 Euro je Pflegehilfsmittel" ✓, Abs. 4 „subsidiär"/Zweckformel/„4 180 Euro je Maßnahme"/„16 720 Euro"/anteilige Aufteilung ✓, Abs. 7 „drei Wochen"/„fünf Wochen"/„als genehmigt" ✓, Fußnote Betragsstand „ab dem 1.1.2025" ✓ — alles unverändert zu 26.10.
- **KfW 455-B**: 6/6 PASS — Antragstopp („können Sie nicht mehr beantragen", „ausgeschöpft"), „Laufende Anträge nicht betroffen", Zusage „reserviert", 2027 nur bei neuen Bundesmitteln, „noch nicht mit Ihrem Vorhaben begonnen" — unverändert.
- **KfW 159**: 9/9 PASS **auf beiden URL-Varianten** (encodiert + Umlaut) — „bis zu 50.000 Euro je Wohneinheit", Haushaltsmittelvorbehalt/kein Rechtsanspruch, „Fachunternehmen", „vor dem Abschluss", „Treppenlifte", FAQ „Kombination der Förderungen für die gleiche Maßnahme ist nicht möglich", „Nachfinanzierung" — unverändert. KfW zeigt weiter „ab -,-- %" (kein eigener Zinssatz publiziert).
- **BMG Zuschüsse zur Wohnungsanpassung**: 4/4 PASS („bis zu 4.180 Euro", „Pflegegrade 1 bis 5", „16.720 Euro", Zweitzuschuss „zweites Mal") + 2.090 €/Person Wohngemeinschaft ✓ + **Zinspassage unverändert**: „…zinsvergünstigte Kredite ab 2,19 Prozent (Stand: 10. Juli 2025) bis zu einer Höhe von 50.000 Euro…" → Artikel `hilfsmittel-dusch-wc-uebernahme` zitiert das korrekt dem BMG zu (Quelle [7]); keine Änderung nötig.

**Link-Status:** 29/30 distinct offizielle URLs HTTP 200 (`research/check_foerder_links_011126.py`). Der eine „FAIL" war ein Artefakt des Prüfskripts (urllib verweigert Umlaut-Pfade ohne Prozentkodierung; via curl bestätigt: beide 159-Varianten antworten nach Redirect-Kette mit identischem Inhalt — beide Varianten bestehen denselben 9er-Assertionssatz). Skript gepatcht (`urllib.parse.quote`).

**Neue Beobachtung (kein Korrekturanlass):** KfW-159 antwortet jetzt mit **301** auf die zitierten URLs (Ziel: trailing-slash-Variante `…Altersgerecht-Umbauen-(159)/`). Für Browser-Besucher folgen die zitierten Links korrekt auf; Belegdateien mit `curl -L` gezogen. Beim nächsten Lauf prüfen, ob KfW die trailing-slash-Form als Kanonikalusgabe macht (dann ggf. zitierte URLs auf die Endform stellen — rein kosmetisch, kein Inhaltsfehler).

**Geänderte Dateien:** 14 × `content-ready/*.json` (28 `checked_at` → 2026-11-01, Skript `research/bump_checked_at_011126.py`, Zeilen-Zustandsautomat statt JSON-Roundtrip; Diff-Sanity: nur Datumszeilen) + **7 sichtbare KfW-Prüfdatumsangaben** „26. Oktober" → „1. November 2026" (treppenlift-zuschuss: Fließtext „direkt im Browser geprüft" — zusätzlich durch heutigen Playwright-Browser-Check 6/6 PASS gegen die Live-KfW-Seite gedeckt — und FAQ; bad-umbau: Fließtext + FAQ; wanne-zur-dusche: Fließtext; bodengleiche: Fließtext + FAQ). Erster Grep fand nur 3 der 7 (length-anchored Regex `.{60}Oktober` versagte bei kürzeren Passagen) — zweiter unanchored Sweep fand die restlichen 4; Lesson: Datums-Sweeps immer unanchored. Bewusst **nicht** hochgesetzt: Gesamtdisclaimer „Abrufstand vom 19.10./16.10." (hilfsmittel-pflegekasse, rollator, pflegegrad, verhinderungspflege — deren Quellensets heute nur per Link-Status, nicht inhaltlich neu geprüft) und historische Datumsaussagen (TK-Preise 14.10., VZ-Verbandsklage 8.10., Editorial-Check-Angaben 23.10./26.10. in angebote-vergleichen/schmale-treppe/steuerlich-absetzen — deren Quellensets heute nicht neu geprüft wurden, die Sätze sind historisch wahr). `data/content.json` unangetastet (Altentwürfe, werden vom Renderer überschrieben).

---

## Prüflauf 26.10.2026, 08:01–08:35 CET (cron, autonomous)

**Ergebnis in einem Satz:** Alle förderrelevanten Zahlen und Rechtsaussagen des Live-Contents stimmen zum Quellenstand vom 26.10.2026 — **null Abweichungen**, keine sachlichen Korrekturen nötig. Aktualisiert wurden nur Prüfdaten (`checked_at` → 2026-10-26) für die heute tatsächlich neu verifizierten Quellen sowie 8 sichtbare KfW-Prüfdatumsangaben („19. Oktober"→„26. Oktober") in 4 Artikeln.

**Verifiziert am 26.10.2026 (Volltext-Assertionen, Belege `research/evidence/foerder-261026-*.html`):**
- **§ 40 SGB XI** (gesetze-im-internet, ISO-8859-1): Abs. 2 „42 Euro"/Kostenerstattung ✓, Abs. 3 „zehn vom Hundert, höchstens jedoch 25 Euro je Pflegehilfsmittel" ✓, Abs. 4 „subsidiär" + Zweckformel + „4 180 Euro je Maßnahme" + „16 720 Euro" + „anteilig auf die Versicherungsträger" ✓, Abs. 7 „drei Wochen"/„fünf Wochen"/„als genehmigt" ✓, Fußnote Betragsstand „ab dem 1.1.2025" ✓
- **KfW 455-B**: Antragstopp („können Sie nicht mehr beantragen", „ausgeschöpft") ✓, „Laufende Anträge nicht betroffen" ✓, Zusage = „reserviert" ✓, Wiederöffnung 2027 nur bei neuen Bundesmitteln ✓, „noch nicht mit Ihrem Vorhaben begonnen" ✓ — per curl **und** im echten Chromium (Playwright, gerenderter Text, `research/browser_check_foerder_2610.mjs`, alle 6 PASS)
- **KfW 159**: „bis zu 50.000 Euro je Wohneinheit" ✓, „Vorbehalt verfügbarer Haushaltsmittel" + „Rechtsanspruch … grundsätzlich nicht" ✓, „Fachunternehmen … Eigenleistungen sind nicht förderfähig" ✓, „vor dem Abschluss von Lieferungs- oder Leistungsverträgen" ✓, FAQ „Kombination der Förderungen für die gleiche Maßnahme ist nicht möglich" (sichtbar + JSON-LD) ✓, Ausschluss „Nachfinanzierungen bereits begonnener oder abgeschlossener Vorhaben" ✓, Förderbereich 3 „Treppenlifte …" ✓; beide zitierten URL-Varianten (%C3%B6 und Umlaut) antworten HTTP 200 mit identischem Inhalt
- **BMG Zuschüsse zur Wohnungsanpassung**: „bis zu 4.180 Euro", „Pflegegrade 1 bis 5", „viermal 4.180 … 16.720 Euro", Zweitzuschuss „zweites Mal", 2.090 €/Person Wohngemeinschaft ✓
- **Link-Status aller 28 im Content zitierten offiziellen URLs** (gesetze-im-internet ×19, BMG ×5, KfW ×2+1 Variante): ausnahmslos HTTP 200

**Beobachtung (kein Korrekturanlass):** Die KfW-159-Seite zeigt aktuell „Zinssatz: ab -,-- %" (kein konkreter Satz publiziert). Der Artikel `hilfsmittel-dusch-wc-uebernahme` zitiert „ab 2,19 Prozent (Stand: 10. Juli 2025)" korrekt **dem BMG** zu — BMG-Seite enthält die Aussage weiterhin (26.10. geprüft). Keine Änderung nötig; beim nächsten Lauf prüfen, ob BMG den Stand aktualisiert.

**Lessons (Matching-Technik):** gesetze-im-internet **und** kfw.de rendrieren Soft-Hyphens (U+00AD) in Wörtern („subsid­är", „Haushalts­mittel") — ohne Strippen melden exakte Stringsuchen fälschlich „nicht gefunden" (das Skript `research/verify_foerder_2610.py` stript jetzt U+00AD; erst danach 36/36 Assertionen PASS). Zusätzlich gelernt: Wortlaut-Needles müssen Einschübe wie „des Pflegebedürftigen" berücksichtigen.

**Geänderte Dateien:** 14 × `content-ready/*.json` (28 `checked_at`, 8 Fließtext-/FAQ-/Tabellendaten in bad-umbau-barrierefrei, bodengleiche-dusche-altbau, treppenlift-zuschuss, wanne-zur-dusche). Bewusst **nicht** auf 26.10. gesetzt: „Abrufstand 19.10."-Gesamtdisclaimer in hilfsmittel-pflegekasse, treppenlift-mietwohnung, pflegegrad-caption, verhinderungspflege-caption (deren Quellen sets heute nur per Link-Status, nicht inhaltlich neu geprüft wurden — kein Überclaiming). `data/content.json` unangetastet (Altentwürfe, werden vom Renderer überschrieben).

**Build/Deploy:** build:launch + test_site.py + test_articles.py + test_partner_links.py PASS → Commit gepusht → CI success → Live-Readback öffentliche URL bestätigt (siehe Cron-Report).

---

## Vorheriger Prüflauf

**Prüflauf:** 19.10.2026, 08:02–08:45 CEST (cron, autonomous)
**Umfang:** Alle förder-/rechtsrelevanten Aussagen der 16 Live-Ratgeber (`content-ready/*.json`) gegen heute abgerufene Originale.
**Betroffene Datei `data/content.json` ist bewusst NICHT bearbeitet:** Sie enthält Altentwürfe und wird im Renderer (`generate.mjs` + `article-renderer.mjs`) vollständig durch `content-ready/*.json` überschrieben — Änderungen nur dort wären nicht live.

## Ergebnis in einem Satz

**Keine einzige förderliche Zahl oder Rechtsaussage des Live-Contents weicht vom heutigen Quellenstand ab.** Korrekturgebende Betrags-/Textänderungen waren nicht nötig; aktualisiert wurden nur die sichtbaren Prüfdaten (`checked_at`, „am 14./16. Oktober geprüft"-Sätze) auf 2026-10-19, wo die jeweilige Quelle heute tatsächlich neu abgerufen und jede zitierte Aussage einzeln im Text nachgewiesen wurde.

## Methode

- Abruf per curl der Original-HTML in `research/evidence/foerder-191026-*.html` (Belegdateien, alle HTTP 200).
- gesetze-im-internet.de ist ISO-8859-1 mit HTML-Entities und rendert Tausendergruppen mit geschütztem Leerzeichen (`4 180`); die Auswertung dekodiert Entities, strippt Tags und normalisiert Whitespace, bevor Zahlen asserted werden (naiver `4.180`-Stringsearch meldet fälschlich „nicht gefunden").
- KfW-Seiten: gerenderte Seite (curl) **und** zusätzlich 455-B im echten Browser geprüft (gerenderter Seitentext, Screenshot) — curl und Browser zeigen identischen Status.
- Jede im Live-Content zitierte Kernzahl wurde einzeln im Quelltext lokalisiert (Kontextzitate unten); nicht nur Seite-erreichbar-geprüft.

## Belegte Aussagen je Quelle (Abruf 19.10.2026)

### § 40 SGB XI — gesetze-im-internet.de/sgb_11/__40.html
- **Abs. 2:** Verbrauchshilfsmittel — Aufwendungen der Pflegekassen „dürfen monatlich den Betrag von 42 Euro nicht übersteigen"; Kostenerstattung möglich. (hilfsmittel-Artikel)
- **Abs. 3:** Volljährige zahlen „zehn vom Hundert, höchstens jedoch 25 Euro je Pflegehilfsmittel an die abgebende Stelle"; Härtefall-Befreiung, Belastungsgrenze nach § 62 SGB V. (hilfsmittel, rollator)
- **Abs. 4:** „subsidär" Zuschüsse für individuelle Wohnumfeldverbesserung, Zweckkatalog (häusliche Pflege ermöglichen/erheblich erleichtern, selbständige Lebensführung wiederherstellen), „4 180 Euro je Maßnahme", Mehrpersonen: je 4 180 €, gesamt „16 720 Euro", >4 Berechtigte anteilige Aufteilung. (zuschuss, bad, wanne, mietwohnung, kosten, mieten, tuerbreiten, beleuchtung, hilfsmittel)
- **Abs. 7:** Entscheidung „spätestens bis zum Ablauf von drei Wochen", mit Pflegefachperson/MD „fünf Wochen"; ohne begründete Mitteilung „gilt die Leistung nach Ablauf der Frist als genehmigt". (mietwohnung, mieten)
- Fußnote im Text: Beträge gem. § 40 iVm § 30 Abs. 1 ab 1.1.2025 (Bek. v. 14.11.2024) — konsistent mit Dynamisierungshinweis.

### KfW 455-B — kfw.de …/Altersgerecht-Umbauen-Investitionszuschuss-(455) [curl + Browser]
- „Diesen Zuschuss können Sie nicht mehr beantragen." / „Wegen der hohen Nachfrage sind die Fördermittel für Maßnahmen zur Barrierereduzierung bereits ausgeschöpft. Ab sofort können Sie daher keine Anträge mehr im Produkt … (455-B) stellen."
- „Laufende Anträge nicht betroffen" — laufende werden bearbeitet; bei erfüllten Voraussetzungen Zusage, damit ist der Zuschuss „reserviert", Auszahlung nach Nachweis.
- „Sollten im Jahr 2027 erneut Bundesmittel … bereitgestellt werden, wird eine Antragstellung wieder möglich sein." (bedingt, nicht zugesichert)
- „Sie können einen Antrag nur stellen, wenn Sie noch nicht mit Ihrem Vorhaben begonnen haben."
- Verweis auf 159 als Alternative. — (zuschuss, bad, wanne)

### KfW 159 — kfw.de …/Altersgerecht-Umbauen-(159)
- „Kreditbetrag: bis zu 50.000 Euro je Wohneinheit"; Laufzeit bis 30 Jahre, bis 10 Jahre Zinsbindung.
- „Die Förderung steht unter dem Vorbehalt verfügbarer Haushaltsmittel. Ein Rechtsanspruch hierauf besteht grundsätzlich nicht."
- „Sprechen Sie vor dem Abschluss von Lieferungs- oder Leistungsverträgen oder dem Kaufvertrag mit einem Finanzierungspartner …"
- FAQ (JSON-LD, gerendert): Einbau/Nachrüstung „durch ein Fachunternehmen des Bauhandwerks" (Material über Bauherrn möglich, über dessen Rechnung förderfähig); „Kombination der Förderungen für die gleiche Maßnahme ist nicht möglich."
- Ausschlüsse (Roh-HTML): Umschuldungen, „Nachfinanzierungen bereits begonnener oder abgeschlossener Vorhaben", Unterhaltungselektronik. Maßnahmen aus Pflegeversicherung/Pflege-Pflichtversicherung ausgeschlossen; Ausnahme: verschiedene Maßnahmen (z. B. Badumbau Zuschuss, Treppenlift Kredit).
- Förderbereich 3 nennt „Treppenlifte, Senkrecht-, Hebe- oder Plattformlifte installieren". — (zuschuss, bad, wanne)

### BMG Zuschüsse zur Wohnungsanpassung — bundesgesundheitsministerium.de/pflege-zu-hause/zuschuesse-zur-wohnungsanpassung
- „für Pflegebedürftige der Pflegegrade 1 bis 5 auf Antrag bis zu 4.180 Euro"; Zweckformel wie § 40 Abs. 4.
- Beispiele: „Türverbreiterungen oder fest installierte Rampen und Treppenlifte, aber auch für den pflegegerechten Umbau des Badezimmers".
- Mehrpersonen: „bis zu viermal 4.180 Euro, also bis zu 16.720 Euro"; >4 Personen anteilig; Beispiel Wohngemeinschaft 2.090 €/Person.
- Zweitzuschuss: „kann auch ein zweites Mal gewährt werden, wenn die Pflegesituation sich so verändert hat, dass erneute Maßnahmen nötig werden." — (zuschuss, bad, tuerbreiten, wanne)

### § 554 BGB (gesetze-im-internet.de/bgb/__554.html) und § 20 WEG (woeigg/__20.html)
- § 554 Abs. 1: Anspruch auf Erlaubnis baulicher Veränderungen, die „dem Gebrauch durch Menschen mit Behinderungen … dienen"; entfällt bei Unzumutbarkeit für den Vermieter; Abs. 2: zum-Nachteil-Abweichung unwirksam. — (mietwohnung, bad, wanne, tuerbreiten)
- § 20 Abs. 2 WEG: jeder Wohnungseigentümer kann „angemessene bauliche Veränderungen verlangen", die dem Gebrauch durch Menschen mit Behinderungen dienen; Beschluss im Rahmen ordnungsmäßiger Verwaltung. — (mietwohnung)

### Pflegegrad-/Verfahrensquellen
- **§ 33 SGB XI:** Leistungen auf Antrag; Vorversicherungszeit „in den letzten zehn Jahren … mindestens zwei Jahre". (hilfsmittel, pflegegrad)
- **§ 14 SGB XI:** Pflegebedürftigkeitsbegriff (gesundheitlich bedingte Beeinträchtigungen der Selbständigkeit). (pflegegrad)
- **§ 15 SGB XI:** Schwellen 12,5–<27 (PG 1), … ab 70–<90 (PG 4), 90–100 (PG 5). (pflegegrad)
- **§ 18 SGB XI:** Auftrag an MD „innerhalb von drei Arbeitstagen ab Eingang des Antrags"; Abs. 3: Gutachterliste u. a. „wenn innerhalb von 20 Arbeitstagen ab Antragstellung keine Begutachtung erfolgt ist". (pflegegrad)
- **BMG Pflegegrade:** „Bearbeitungsfrist … beträgt 25 Arbeitstage"; verkürzte Frist „von einer Woche" in benannten Fällen. (pflegegrad)
- **§ 84 SGG / § 87 SGG:** Widerspruch/Klage „binnen eines Monats". (hilfsmittel, pflegegrad)

### Hilfsmittel-/Verbrauchsquellen
- **BMG Pflegehilfsmittel:** technische Pflegehilfsmittel „wie beispielsweise einem Pflegebett, Lagerungshilfen oder einem Notrufsystem" vs. Verbrauchsprodukte; leihweise Überlassung; 25-Euro-Deckel genannt. (hilfsmittel, hausnotruf×2, rollator)
- **GKV-Spitzenverband p_himi:** „Aufwendungen … ab dem 01.01.2025 monatlich … 42 Euro nicht übersteigen (§ 40 Abs. 2 SGB XI)", Kostenerstattung möglich, darüber hinaus selbst tragen. (hilfsmittel)
- **GKV Hilfsmittelverzeichnis:** Produktgruppen-Logik nachweisbar. (hilfsmittel, rollator)
- **VZ Pflegehilfsmittel:** „maximal 42 Euro im Monat" (Verbrauch), 25 €/10 % Zuzahlung, Befreiung; **keine** veraltete 40-€-Nennung mehr auf der Seite. (hilfsmittel)
- **VZ Hausnotruf:** „Kosten … im Basistarif meist zwischen 27 und 40 Euro monatlich"; „Seit dem 1. April 2026 … 27 Euro monatlich" Übernahme; „Der Medizinische Dienst prüft"; „Der Hausnotrufanbieter muss Vertragspartner der Pflegekasse sein"; Zusatzleistungen privat. (hausnotruf×2, hilfsmittel)

### Verhinderungspflege/Tagespflege-Quellen
- **§ 39 SGB XI:** Ersatzpflege „für längstens acht Wochen je Kalenderjahr". 
- **§ 41 SGB XI:** Tages-/Nachtpflege Gesamtwerte je Kalendermonat: PG2 „721 Euro", PG3 „1 357 Euro", PG4 „1 685 Euro", PG5 „2 085 Euro"; inkl. notwendiger Beförderung. Artikelwerte (721/1.357/1.685/2.085) deckungsgleich.
- **§ 37 SGB XI Abs. 2:** „Die Hälfte des bisher bezogenen Pflegegeldes wird während einer Kurzzeitpflege nach § 42 und während einer Verhinderungspflege nach § 39 …" weitergezahlt — Artikelzitat korrekt.
- **§ 42a SGB XI:** „Gesamtleistungsbetrages von insgesamt bis zu 3 539 Euro je Kalenderjahr (Gemeinsamer Jahresbetrag)".
- **BMG Entlastungsleistungen:** „Entlastungsbetrag in Höhe von bis zu 131 Euro monatlich (also insgesamt bis zu 1.572 Euro im Jahr)", auch für PG 1.
- **BMG Tagespflege:** „Kosten für Unterkunft und Verpflegung sowie gesondert berechenbare Investitionskosten müssen … grundsätzlich privat getragen werden."

## Aktualisierte Prüfdaten (eingespielt)

`checked_at` → `2026-10-19` nur für heute neu abgerufene Originale; Hersteller-/Portalseiten (Malteser, TK, pflege.net, treppenliftwissen, nullbarriere, din18040, licht.de, Desideria, sanitätshaus.net, pflege-einstieg.de, gesund.bund.de, VZ Widerruf/Mobilitätshilfen/Hilfsmittel-beantragen/Treppenlifte, Vergleichsportal, BeWo, Awin-eigene) bleiben auf ihrem letzten realen Prüfstand:

| Artikel | Aktualisierte Quellen | Fließtext-Datumskorrekturen |
|---|---|---|
| treppenlift-zuschuss | alle 5 (§40, 455-B, 159, BMG, §554) | „14.10.2026"→„19.10.2026" (Tabelle, Abschnitt, FAQ) |
| bad-umbau-barrierefrei | alle 5 | „Am 14. Oktober 2026"→„Am 19. Oktober 2026" (Abschnitt+FAQ) |
| wanne-zur-dusche | alle 5 | „Am 14. Oktober 2026"→„Am 19. Oktober 2026" |
| hilfsmittel-pflegekasse | alle 10 | „Abrufstand vom 16. Oktober 2026"→„19."; Bild-Caption 16.10.→19.10. |
| treppenlift-mietwohnung | §554, §20 WEG, §40 (3 von 7) | „Stand der Prüfung: 16.10.2026"→„19.10.2026" |
| pflegegrad-antrag | §33, §14, §15, §18, §84, §87, BMG (7 von 10) | Bild-Caption „Abruf 16.10.2026"→„19.10.2026" |
| verhinderungspflege-tagespflege | §39, §37, §41, §42a, §30, BMG×2 (7 von 8) | Caption „Stand 16.10.2026"→„19.10.2026" |
| treppenlift-kosten | §40 (1 von 3) | — (Herstellerpreise 14.10. bleiben) |
| treppenlift-mieten | §40 (1 von 6) | — |
| rollator | §40, BMG, §61, GKV (4 von 8) | — |
| hausnotruf-kosten | VZ Hausnotruf, BMG (2 von 4) | — |
| hausnotruf-sturz | VZ Hausnotruf (1 von 3) | — |
| tuerbreiten | BMG, §554, §40 (3 von 5) | — |
| beleuchtung | §40 (1 von 5) | — |

## Grenzen

- Diese Prüfung ist Quellen- und Sachstandsverifikation, **keine Bewilligungszusage** und keine individuelle Förderberatung. Alle Artikel formulieren dies bereits korrekt.
- KfW-455-B-Status ist volatil (Budget-abhängig); erneuter Check beim nächsten Förderlauf.
- KfW-159-Bedingungen (technische Mindestanforderungen im Detail) sind auf der Produktseite verlinkt, aber nicht als Volltext abgerufen; der Content behauptet nur das, was auf der Produktseite/FAQ sichtbar ist (Fachunternehmen, keine Eigenleistung/Nachfinanzierung, keine Kombination gleiche Maßnahme) — das ist belegt.
- Landesprogramme: im Live-Content bewusst nicht als geprüft dargestellt („individuell prüfen") — das bleibt korrekt, hier gab es nichts nachzuziehen.
