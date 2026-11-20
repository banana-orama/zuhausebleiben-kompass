# Batch: hausnotruf-fuer-paare (Adoption des gestrandeten 19.11.-Batches, 2026-11-20)

## Ausgangslage

Der 19.11.-Lauf hatte den Artikel (content-ready JSON, SVG, Cross-Links, Gate-Bumps, Ledger,
Evidence) **lokal fertig gebaut**, aber nur die generierte `dist/hausnotruf-fuer-paare.html`
im Impressum-Commit `1a1a712` versehentlich mit-committet — die QUELLE fehlte im Repo. Folge:
die Seite war live erreichbar (stale Build überlebt den CI-Build, weil `generate.mjs` dist
nicht leert), aber **Orphan**: nicht in Sitemap, RSS, Homepage, llms.txt, ohne Cross-Links.
Dieser Lauf adoptiert den Batch mit eigener Abnahme und setzt die Quelle ab.

## Eigene Abnahme (201126)

1. **Zitate/Quellen:** 35/35 Ledger-Zitate verbatim gegen Beweisdateien geprüft, jetzt für
   ALLE 8 Artikelquellen inkl. der bislang ungeprüften (GKV-PHMV-Übersicht, 90prozent-
   E-Magazin, gegen raw-*.html). `research/verify_paare_source_201126.py` ALL PASS.
2. **Fund [7]-Lücke:** Quelle 7 (Johanniter) war im Fließtext nie zitiert. Fix: Johanniter-
   Paket-Satz (Basisstation + Handsender + Mobilgerät für unterwegs) im Kapitel „Der zweite
   Knopf" ergänzt, verbatim-Verankerung im Ledger (Id 7) nachgetragen. Artikel zitiert jetzt
   [1]–[8] vollständig.
3. **Kernzahlen verbatim gegen Beweise:** 27,00 EUR netto + Produktgruppe 52 + Mehrkosten-
   Regelung (§ 33 Abs. 1 S. 9 SGB V / § 40 Abs. 1 S. 3 SGB XI) im Vertragstext;
   „oft und länger abwesend" + „fast den ganzen Tag allein" + „27 und 40 Euro" bei VZ;
   „Mindestlaufzeit von zwei Jahren" im 90prozent-HTML (erste Greps scheiterten an
   Zeilenumbrüchen/Tags — Flat-Extraction löste alle drei Verdachtsstellen als GESTÜTZT auf).
4. **SVG:** Geometrie-Gate (kein Element außerhalb viewBox 1000x800, Playwright getBBox) +
   Sichtprüfung im echten Seitenkontext (Screenshot nach Build, alle 4 Kacheln vollständig,
   keine Überlappungen; qlmanage-Crop war Artefakt). KI-Kennzeichnung im Caption + alt.
5. **Gates:** npm test komplett (Kette erreicht test:partner ALL PASS; A3 >= 38),
   test_articles erwartet 40, RSS-Check 40 (verify_checklists_build ALL PASS), neues
   Content-Support-Gate `research/verify_article_keys_paare_201126.py` (alle JSON-Keys im
   Built-HTML, 0 Misses; robots index,follow; canonical absolut; keine Partner-Marker).
   Mobil 390 px: 0 px Overflow.

## Beweisdateien

`research/evidence/paare-191126/` (GKV-Vertrag PDF/TXT, VZ, DRK, Malteser, Johanniter,
pflege-panorama, 90prozent, PHMV, SVG-Screenshots `svg-in-page-201126.png`,
`mobile-artikel-201126.png`), Ledger `research/paare-191126-ledger.json`.

## Fix für die Zukunft (aus diesem Fund)

CI/deploy löscht dist NICHT vor dem Build — ein versehentlich committetes dist/HTML kann
also als stale Datei überleben und live gehen, obwohl die Quelle fehlt. Dist-Commits sind
deshalb weiter verboten; beim nächsten Renderer-Einarbeiten prüfen, ob `generate.mjs`
besser mit leerem dist-Verzeichnis baut (renderer-entscheidung, separater Lauf).

## Live-Readback (nach 2fafb93, CI 44704309239 success)

13/13 PASS: frischer Deploy bewiesen über neuen [7]-Satz; robots index,follow; in
Sitemap, RSS, llms.txt, Homepage; Related-Links auf paare zu allen 3 Cluster-Zielen;
27,00 EUR + 54-Euro-Kontrast live; 8 Quellen; SVG + absoluter Canonical. IndexNow
HTTP 200 mit 5 URLs (`research/indexnow_submit_paare_201126.py`).

Erkenntnis Related-Pool: `article-renderer.mjs` cappt „Passend dazu" auf 3 Links
(crossSlugs zuerst, dann Cluster-Pool in Glob-Reihenfolge) — neue Artikel bekommen
KEINE Rücklinks von den Hub-Seiten, außer der Zufall trifft es (alarm-ablauf). Ist
bestehendes Designverhalten je Batch, kein Defekt; gewünschte Rückverlinkung wäre
als crossSlugs-Eintrag DES Zielartikels zu modellieren, nicht als Pool-Änderung.
