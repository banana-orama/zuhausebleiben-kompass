# Batch: Hilfsmittel Dusch-WC (Briefing 9) — SERP, Quellen, Entscheidungen

Datum: 2026-10-21 · Slug: `hilfsmittel-dusch-wc-uebernahme` · Cluster: Pflege/Alltag (care)

## SERP-Befund (Websuche 21.10.2026)

Suchintention: „dusch-wc pflegekasse/krankenkasse/zuschuss“ — kaufnahes Entscheidungsstadium,
überwiegend Angehörige. Trefferbild stark durchsetzt mit kommerziellen Angeboten und sich
widersprechenden Aussagen:

- altersgerecht-modernisieren.de: „Aufsatz → Krankenkasse (§ 33 SGB V), Komplettanlage → Pflegekasse“ — halb richtig, aber ohne Indikations-/Einzelfall-Präzisierung.
- vitalpoint24.de (zwei Treffer): bewirbt „kostenlose Dusch-WCs über die Pflegekasse gemäß § 40 SGB XI“, „bis zu 4.180 €“, übernimmt Antragsprozess — vermischt Wohnumfeld-Einzelfall mit Produkterstattung.
- sozialrat.org (23.06.2026): „Dusch-WC ist weder in Produktgruppe 04 noch 33 gelistet“ — am Verzeichnisstand 28.09.2026 nachprüfbar falsch (33.40.05 existiert, siehe Ledger [5]).
- mewacare.com / as-dusch-wc.de: „mit anerkannter Hilfsmittelnummer … bei positivem Bescheid erstattet“ — Richtung richtig, ohne die enge Indikation zu nennen; AS verweist aufs Produkt „Jasmin Bidet“, das tatsächlich gelistet ist (33.40.05.0006).

Eigene Verbesserung: als erstes deutschsprachiges Ratgeberergebnis die Verzeichnisrealität
(Produktart 33.40.05.0 mit wörtlicher Indikation), die drei Trägerwege mit ihren Grenzen und eine
Antrags-Checkliste zusammenführen; alle Zahlen ans Primärmaterial (Gesetzestext, GKV-SV-Fortschreibung,
REHADAT) zurückbinden. Kein SERP-Konkurrent zeigt die Indikation wörtlich.

## Quellen (alle verbatim im Ledger `research/dusch-wc-ledger.json`, 20/20 geprüft)

1. § 40 SGB XI (Abs. 4 Wohnumfeld: „können subsidiär“, 4 180 / 16 720 €; Abs. 5 Konkurrenzprüfung)
2. § 33 SGB V (Hilfsmittelanspruch, Gebrauchsgegenstände-Ausschluss)
3. § 61 SGB V (Zuzahlung 10 %, min. 5 €, max. 10 €)
4. GKV-SV-Fortschreibung PG 33 „Toilettenhilfen“ vom 11.12.2025 (Produktart 33.40.05.0: Beschreibung,
   Indikation Arme/Hände, Leistungsrecht inkl. Montage, mehrkostenfreie Versorgung)
5. REHADAT-Produkt 33.40.05.0006 (Verzeichnisstand Bundesanzeiger 28.09.2026) + Gegenprobe „dusch-wc“
   (nur Dusch-Toilettenstühle/-rollstühle, keine kompletten Anlagen)
6. Verbraucherzentrale (Zuzahlungsregel Hilfsmittel)
7. BMG Zuschüsse zur Wohnungsanpassung (4.180 €, Pflegegrade 1–5; KfW-159-Kredit 2,19 %, 50.000 €)
8. § 84 SGG (Widerspruch binnen eines Monats)

Beweisdateien: `research/evidence/dusch-wc-*`. Bewusst NICHT behauptet: Pflegehilfsmittelverzeichnis-
Mitgliedschaft der 33.40.05-Positionen (ungeprüft), Gerichtsrechtsprechung zum WC-Ersatz, Marktpreise.

## Entscheidungen

- Slug mit Präfix `hilfsmittel-` → Care-Cluster im Renderer ohne Codeänderung; Related-Links und
  Early-CTA (hilfsmittel-pflegekasse-uebernahme) per specialMap-Eintrag kontextrichtig.
- Grafik: eigene 3-Wege-Entscheidungs-SVG (`assets/images/hilfsmittel-dusch-wc-wege.svg`), im Browser
  gerendert (oben/unten), KI-Label im Caption, Manifest-Eintrag mit Provenance/Limitierungen.
- Abgrenzung zu `hilfsmittel-pflegekasse-uebernahme`: jener erklärt die Pflegekassen-Systemik
  (§§ 33/40 SGB XI); dieser behandelt die Produktkategorie Dusch-WC inkl. Krankenkassen-Route —
  intent-distinct, kein Kannibalisierungsfall.
- „Kostenlos über die Pflegekasse“-Werbung im Text kritisch eingeordnet, ohne Einzelshops zu benennen.

## Gates (21.10.2026)

- Build beide Modi PASS; test_site.py PASS (44 Seiten, PREVIEW-Check); test_articles.py PASS (19, Zähler angehoben)
- Ledger 20/20 verbatim; Key-Content 0 FAILS (77 Zitat-Links, Kennzahlen, Cluster-Ziele)
- Consent 13/13 (exklusive fremdem In-Flight-Spec `tests/checklists.spec.mjs`, das separat rot — nicht Teil dieses Batches)
- Mobile 390 px: kein Overflow, Bild 346 px, Controls ≥ 44 px
- SVG: XML-Test in test_articles.py, Browser-Sichtkontrolle oben + unten
