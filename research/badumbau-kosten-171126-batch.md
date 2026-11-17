# Batch 28 (2026-11-17, Cron-Lauf) — Briefing 28: badumbau-kosten (39. Ratgeber)

## Produktionseinheit
**Artikel:** `content-ready/badumbau-kosten.json` — Badumbau-Kosten-Architektur (Kosten-Journey des Bad-Clusters, Pendant zu treppenlift-kosten/hausnotruf-kosten).
**Status:** editorial-reviewed-preview (Live-Index-Modus, index,follow), 8 Abschnitte, 3 Tabellen, 10-Punkte-Checkliste (abschnitt-7), 6 FAQs, 12 Quellen, SVG-Erklärgrafik.

## Topic-Gate (GSC im Cron weiter ohne Google-Sitzung → SERP-basiert)
- **Ads-Lage:** Positionen 1–5 = ausschließlich bezahlte Anzeigen (pflege-helfer24, pflegehilfe.org, aroundhome.de [unser Pauschalpartner], seniovo, my-hammer) mit „4.180 € Zuschuss sichern“-Versprechen.
- **Organisch:** ~8–10 dedizierte Seiten, überwiegend Anbieter-/Vermittlungs-Portale; stark divergierende Komplett-Spannen: 15.000–30.000 (badumbau-ratgeber), 15.000–25.000 + Teilumbau 8.000–15.000 (konstruktionsfuhrer), 15.000–25.000 (kostenwelt), 13.000–28.000 (bauguru24), 12.000–25.000 Badsanierung-allgemein (badklar), Light 8.000/Komfort 18.000–25.000/Luxus 40.000+ (pflege-panorama). **Kein Portal dokumentiert die Streuung selbst.**
- **Bestand:** Stock-Grep 17.11.: kein dedizierter Kosten-Ratgeber im Bad-Cluster („kosten“ 2–19× nur verstreut, „budget“ 0×). Cluster: bad-umbau-barrierefrei, badumbau-angebote-vergleichen, bodengleiche-dusche-altbau, wanne-zur-dusche, hilfsmittel-dusch-wc-uebernahme.
- **Verworfen mit Beleg:** „Badewanne oder Dusche“ (bereits in launch-state-Verwerfen-Liste + wanne-zur-dusche behandelt Varianten), „Badumbau Förderung“ (wohnumfeldverbesserung-beantragen besitzt die Antragsstrecke; dieser Artikel erklärt den Förderstand nur als Eigenanteil-Kontext mit Verweis), „Badsanierung allgemein“ (badklar et al. decken es; kein Payable-Event-Mehrwert ohne Barrierefrei-Fokus).
- **Verbesserung (ehrlich abgegrenzt):** pflegekompass UND pflege-panorama dokumentieren die §35a-Förder-Ausnahme bereits (Skript-Check: pflegekompass 2× „öffentlich gefördert“; konstruktionsfuhrer 0× „zinsverbilligt“ trotz Steuerbonus-Angabe; badumbau-ratgeber/kostenwelt/bauguru/badklar 0× „35a“ komplett; VZ 0× „Badumbau“). Unsere Basis: 1) konsolidierte Divergenz-Tabelle mit Interessenkennzeichnung (kein Wettbewerber hat sie), 2) §35a-Ausnahme auf den Gesetzestext zurückgeführt statt Portal-Echo, 3) subsidiär-Ermessen-Ehrlichkeit gegen die Ads-Versprechen, 4) Kostenbausteine NUR mit zitierbaren Bandbreiten (keine erfundenen Positionssummen), 5) Reihenfolge-Strecke mit 3/5-Wochen-Frist + Genehmigungsfiktion + 455-B-Stopp-Wortlaut im selben Text.

## Ledger
`research/badumbau-kosten-171126-ledger.json` — **58/58 PASS** (`research/verify_badumbau_kosten_171126.py`): 47 Verbatim-Zitate über 12 Quellen (§40 SGB XI + §35a EStG gesetze-im-internet live 17.11. inkl. Abs.-4-Höchstbeträge 4 180/16 720 mit Gesetzesschreibweise, Abs.-7-Fristen+Fiktion, §35a Abs.-3-Sätze 1+2 mit Förder-Ausnahme + Abs.-5 „nur für Arbeitskosten“/„Rechnung … Zahlung auf das Konto des Erbringers“; KfW 455-B-Stopp-Wortlaut + 159-Fachunternehmen/Eigenleistungen; VZ 15–20-%-Hinweis + Angebot-Bindung; 6 Portal-Quellen mit Bandbreiten) + 7 Absenz-Checks + 4 Arithmetik-Checks (18.000−4.180=13.820; 6.000×0,20=1.200; 4.180×2=8.360; ×4=16.720).
Evidenz: `research/evidence/badumbau-kosten-171126/` (Extrakte + Scan-Skripte committed, Roh-HTML uncommitted).

## Renderer/Config
- specialMap +1: Early-CTA „Angebote mit Einzelpositionen vergleichen“ → /badumbau-angebote-vergleichen.html (Cluster-Journey; kein Partner-Placement — Bad-Cluster ohne aktive Placements).
- cross-links.json: badumbau-kosten → [badumbau-angebote-vergleichen, wohnumfeldverbesserung-beantragen (bewusster Care-Cross: Antrag-VOR-Baubeginn-Strecke), wanne-zur-dusche] + rationale.
- llms-txt.py: SUMMARIES + SECTION_MAP (Bad-Sektion) +1. Cluster via `"bad"`-Substring automatisch (beide Stellen konsistent).
- Testzähler: test_articles 38→**39**; verify_checklists_build RSS 38→**39**; test_partner_links A3 ≥36→≥**37**.

## Gates
- npm test EXIT 0 (PREVIEW+LAUNCH je 64 Seiten, test_articles **39**, cross_links 39/17 Whitelist, titles ALL PASS nach Title-Kürzung 76→61/Desc 184→151, Playwright **21 passed**, Partner A–F ALL PASS).
- verify_checklists_build ALL PASS gegen LAUNCH (RSS **39**, Sitemap **52 locs**, llms/Checklisten intakt).
- Content-Gate `verify_badumbau_kosten_content_171126.py`: **187/187 ALL PASS** (alle JSON-Keys inkl. table-cells + paragraphs_after, 20 Kernzahlen, Related-Reihenfolge, CTA+Label, 12 Quellen-URLs, Anker abschnitt-1..8, Zitationsbereich 1–12, Absenzen 0× awin/sponsored/ENTWURF/„4 180“-Gesetzesschreibweise, robots index,follow).
- SVG `verify_badumbau_svg_mobile_171126.py`: getBBox 0 Out-of-Canvas, Pairwise 0 Overlaps, Box-Overflow 0 + **Vision-Sichtkontrolle sauber** (2 Runden: Runde 1 fand überlange Footer-Zeile 1144>1000 + fehlende Legende 5 → behoben, Runde 2 bestätigt 5 Legenden, keine Überlappung).
- Mobile 390 px: **0 px Overflow**.

## Deploy / Live-Readback / IndexNow
(siehe launch-state-Eintrag — Commit, CI, öffentlicher Readback, IndexNow nach Deployment)

## Refresh-Trigger
- KfW 455-B: 2027-Wiederaufnahme nur conditional — beim Bundeshaushalt-2027-Abschluss/KfW-News re-prüfen (bestehender Trigger, gilt jetzt auch für diesen Artikel).
- §35a-Arbeitskosten-/Höchstbetrag-Regeln: nur bei ESt-Änderung (Referentenentwurf 2027: 15 %/900 € — nicht beschlossen; Trigger „PNOG-Verabschiedung/ESt-Reform“ greift).
- Portal-Spannen (Tabelle): bei nächstem Badumbau-Batch-Durchlauf Stichtage re-prüfen (badumbau-ratgeber ohne eigenes Stand-Datum).
- Hilfsmittel-Zuzahlungs-Änderung ab 01.01.2027 (GKV-Beitragssatzstabilisierungsgesetz, laut pflegekompass „mindestens 7,50 und höchstens 15 Euro“) — für hilfsmittel-Artikel relevant, hier bewusst NICHT behauptet (nicht im eigenen Ledger verifiziert).
