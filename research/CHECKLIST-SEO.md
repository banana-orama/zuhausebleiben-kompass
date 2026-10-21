# CHECKLIST-SEO — Print-Checklisten als Link-Magneten

Stand: 2026-10-19 · Workstream: Growth Lever 2 (linkable assets) · Build: `node scripts/build-checklists.mjs` → `dist/checklisten/` (7 Seiten: Übersicht + 6 Checklisten)

## Warum Checklisten als Link-Magnete funktionieren

1. **Sie lösen das eigentliche Problem der Zielgruppe: Druckbare Handlungssicherheit.** Ältere Menschen und Angehörige stehen vor Behörden- und Anbietergesprächen (Pflegekasse, Gutachter, Treppenlift-Vertreter, Handwerker). Ein Blatt zum Abhaken wird physisch mitgenommen, ausgedruckt, an den Kühlschrank gehängt — und genau dieses Objekt teilen Pflegedienste, Beratungsstellen, Ergotherapeuten und Angehörigengruppen. Ratgeber-Absätze werden verlinkt, Checklisten werden **verschenkt**.
2. **Natürliche Anker-URLs statt Content-Syndication.** „Schick ihnen die Checkliste" erzeugt Links mit exaktem, merkbarem Pfad (`/checklisten/…`), nicht nur Zitate. Redaktionelle Verlinkungen von Pflegeblogs und Angehörigen-Portalen zeigen in der Praxis genau dieses Verhaltensmuster (verweis auf druckbare Arbeitsblätter statt auf Fließtext).
3. **SERP-Passung zu einem eigenen Query-Typ.** Checklisten-Queries („… checkliste pdf", „… fragen zum ausdrucken") haben einen erkennbaren Intent: Nutzer wollen das Objekt, nicht die Erklärung. Wer nur den Ratgeber ausliefert, gewinnt diesen Intent nicht — ein dediziertes, druckoptimiertes Blatt schon.
4. **PDF-artiger Mehrwert ohne PDF-Nachteil.** Die Seiten sind echtes HTML (indexierbar, canonical, intern verlinkt) mit `@media print`-CSS: Sie ranken wie Seiten UND drucken wie PDFs. Ein reines PDF würde weder interne Verlinkung noch SEO-Wirkung entfalten; die Kombination ist der eigentliche Hebel.
5. **Null-Infrastruktur-Lead-Magnet.** Kein Formular, kein Gated Content, keine PII — konform mit der aktuellen Portal-Phase (keine Lead-Collection, Consent-Standard „denied"). Der „Conversion"-Pfad ist die Internal-Link-Rückführung in den Ratgeber (und von dort in die späteren CTAs).

## Warum ausgerechnet diese 6 (Quelle: vorhandene Entscheidungshilfen in den Artikeln)

| Checkliste | Herkunft im Artikel | Value-Hypothesis (1 Zeile) |
|---|---|---|
| Pflegegrad-Antrag (Ablauf + Fristen) | 10-Punkte-Checkliste + Fristen-Tabelle | Familien im Antragstress bekommen jeden Fristenschritt zum Abhaken — das am häufigsten weitergegebene Blatt der Pflege-Enter-Gruppe. |
| Hilfsmittel-Kostenübernahme (Antragsgespräch) | Checkliste für das Antragsgespräch (10 Punkte) | Für das Gespräch mit der Pflegekasse: nichts vergessen, Eigenanteil-Deckel parat — klassisches Weitergabe-Blatt für Pflegedienste und Beratungsstellen. |
| Hausnotruf-Vergleich | Vergleichscheckliste zum Ausdrucken (11 Punkte) | Senioren-Telefone bieten heute 20 Anbieter — die Vergleichsmatrix verhindert Fehlbuchungen und wird von Angehörigen vor Vertragsabschluss gesucht. |
| Treppenlift-Entscheidungsmatrix + 8 Fragen | Entscheidungsmatrix (10 Prüfpunkte × 3 Betriebe) + Acht-Fragen-Block | Drei Anbieter-Visiten auf einem Blatt: Der einzige Vergleichsbogen, der für Hausbesuche gebaut ist — Linkziel Nr. 1 für Enter-Unternehmens-Blogs. |
| Tür-/Schwellen-Messbogen | Messbogen (Abschnitt 1) + Schnell-Check | Der einzige „Werkzeug"-Charakter der sechs: Gemessene Werte werden eingetragen und direkt im Pflegekassen-Antrag verwendet → hohe Speicher- und Weitergabe-Quote. |
| Badumbau-Angebotsvergleich | Positionstabelle (7 Positionen) + Angebotscheck (8 Fragen) | Schützt vor den teuersten Fehlern (pauschales Angebot, fehlende Abdichtungs-Position) — typisches Blatt, das Angehörige vor Vertragsunterschrift durchgehen. |

## Ziel-Keywords (primär → sekundär)

Jede Checklisten-Seite canonical auf sich selbst; der Artikel bleibt die „Erklär"-URL, die Checkliste die „Objekt"-URL. Keine Cannibalization, weil die Intent-Typen differieren.

| Seite | Primär | Sekundär / Long-Tail |
|---|---|---|
| pflegegrad-antrag-ablauf-fristen (Checkliste) | `pflegegrad antrag checkliste pdf` | `pflegegrad checkliste zum ausdrucken`, `pflegegrad fristen tabelle`, `pflegegrad begutachtung vorbereiten checkliste` |
| hilfsmittel-pflegekasse-uebernahme (Checkliste) | `hilfsmittel pflegekasse checkliste` | `hilfsmittel antrag pflegekasse muster`, `hilfsmittel zuzahlung pflegekasse 25 euro`, `hilfsmittel antragsgespräch fragen` |
| hausnotruf-kosten-anbieter-vergleich (Checkliste) | `hausnotruf vergleich checkliste` | `hausnotruf anbieter vergleich pdf`, `hausnotruffragen zum ausdrucken`, `hausnotruf test stiftung warentest` (indirekt) |
| treppenlift-firmen-vergleich (Checkliste) | `treppenlift fragen checkliste` | `treppenlift anbieter vergleich vorlage`, `treppenlift entscheidungsmatrix`, `treppenlift hausbesuch fragen pdf` |
| tuerbreiten-schwellen-schnellcheck (Checkliste) | `türbreite messen rollator` | `schwellen im altbau messen`, `messbogen türbreiten schwellen pdf`, `pflegekasse antrag türen vorlage` |
| badumbau-angebote-vergleichen (Index) | `badumbau angebote vergleichen checkliste` | `badumbau angebot checkliste pdf`, `dusche anbieter vergleich fragen`, `bad umbau kostenpositionen` |
| index (Checklisten-Hub) | `checklisten pflege ausdrucken` | `pflege checklisten kostenlos`, `checklisten senioren wohnen pdf`, `umbau seniorengerecht checkliste pdf |

Siehe SEO-STRATEGIE.md im Repo-Root: Der Hub ist der Anchor für Cluster-übergreifende Queries („checklisten", „ausdrucken"), die einzelnen Seiten für die Objekt-Queries.

## Google-konforme Aufmachung (keine Doorway/Gateway-Problematik)

- Jede Checkliste hat **Eigenwert**: Der volle Inhalt des Arbeitsblatts ist auf der Seite sichtbar (nicht hinter Download/Print versteckt) — Google sieht denselben Mehrwert wie der Nutzer.
- Keine Close-Variationen desselben Inhalts: 6 verschiedene Entscheidungsprobleme, kein Template-Spam mit eingetauschten Suchworten.
- Canonical auf die eigene URL, `index,follow` (Launch-Entscheidung: Checklisten sind wertvolle Indexierungs-Ziele; die noindex-Option bleibt bewusst offen — ein `<meta name="robots">`-Flip ist eine Zeile im Builder).
- Interne Verkettung beidseitig: Artikel ↔ Checkliste (keine Sackgasse), Hub verlinkt alle 6 + alle Artikel.

## Promotion-Plan (Reihenfolge = Priorität)

### Phase 1 — 0 bis 2 Wochen nach Freigabe („niedrige Reibung, hohe Relevanz")
- **Pflegedienste & Tagespflegen regional (Nümbrecht/Oberberg, dann NRW):** kurze, persönliche E-Mail (Betreff: „Kostenlose Checklisten für Ihre Angehörigenarbeit") — nicht um Links bitten, sondern das Objekt anbieten; Verlinkung folgt, wenn das Blatt in Abläufen landet. 20 Kontakte/Woche, template + personalisierte Zeile.
- **Pflegeberatungsstellen (Pflegestützpunkte), Verbraucherzentrale-Beratungsstellen, Sozialverbände (VdK/SoVD-Kreisstellen):** gleicher Ansatz; diese verlinken bereits heute auf „Merkblätter" — hier gibt es echte Lücke im Angebot.
- **Ergotherapeuten, Hausarztpraxen, Sanitätshäuser** (Oberberg + Köln/Bonn als nächste Metropolregion): Aushang-Objekt anbieten (der Messbogen und die Hausnotruf-Checkliste sind die besten „Aushang"-Kandidaten).

### Phase 2 — 2 bis 6 Wochen (Communities & UGC-Plattformen)
- **Reddit:** r/Pflege (deutsch), r/Finanzen (Pflegegrad-Threads), r/Eltern (bei Hilfsmittel-Fällen) — als Antwort in bestehenden Threads („ich habe dazu eine druckbare Checkliste gebaut, Link") — **nie als selbst-promotenden Post**, nur in laufenden Fragen.
- **Fragen-Portale:** gutefrage.net, forum.gofeminin.de (Pflege-Subforen), med1.de (Foren zu Pflegegrad) — profilbasiert, erst nach Beteiligung.
- **Facebook-Gruppen:** „Pflege im Heim", „Angehörige Pflege" & regionaler Gruppen (Suche über Facebook-Gruppensuche „Pflege Oberberg"), Beiträge als „Ich habe das mal zusammengefasst, gerne ausdrucken" — Regel: erst 4 Wochen Beteiligung, dann eigenes Objekt.
 FB-Regel: nur in Gruppen, deren Regeln Link-Teilungen erlauben; Admin vorher anschreiben.

### Phase 3 — 4 bis 10 Wochen (Redaktionelle Platzierungen / Der Link-Build)
- **Pflege-/Angehörigenportale mit Link-Listen:** pflege.de-Redaktion, wegweiser-pflege.de (Verbraucherzentrale NRW), pflegelotse, care-evidence-Portale — Ansprache als „Ressource-Tipp" mit konkretem Nutzen für deren Leser.
- **Lokale Medien (Oberbergischer Kreis):** Bergische Blatt, Gummersbacher Zeitung/Wochenblatt — Lokaljournalisten greifen „kostenlose Checklisten aus Nümbrecht" gern auf (PI = pressemeldung mit Objekt, nicht Firmen-PI).
- **Podcasts/Newsletter im Pflege-Themenfeld:** z. B. „Pflege daheim"-Newsletter, PflegeZeit-Newsletter — Newsletter-Empfehlung mit Link (Checklisten sind Newsletter-freundlich: objektbezogen, kein Funnel).
- **Gastbeiträge** (nur mit echtem Mehrwert-Objekt als Anker): „Die 8 Fragen vor dem Treppenlift-Vertrag" — der Artikel existiert bereits, die Checkliste ist das verlinkbare Objekt.

### Phase 4 — laufend
- **Eigene Newsletter-Liste** (später): Checklisten als „Download der Woche" — leads to downstream conversions, no PII at signup (double-opt-in, rechtssicher aufbauen, wenn Listenaufbau beschlossen ist).
- **Print-QR-Codes** für Kooperationspartner (Sanitätshaus, Beratungsstellen): QR auf Aushang → Checklisten-URL.

###Messung
- GA4 (nur bei erteilter Einwilligung): `cta_click` auf die Hub-Verlinkung, später Outbound-Klick-Messung mit `link_attribution`-Erweiterung — keine Auswertung vor Launch.
- Such Console: Queries mit „checkliste", „pdf", „ausdrucken" separat bewerten; Rankings der 7 URLs gegen Artikel-URLs differenzieren (Cannibalization-Kontrolle).

## Nicht tun

- **Kein Gated Content, kein E-Mail-Zwang:** würde den Link-Magnet-Mechanismus brechen und die Portal-Phase (keine Lead-Collection) verletzen.
- **Noindex/Deindex:** Checklisten sind ein Indexierungs-Ziel; der Builder setzt bewusst `index,follow`. Ein Flip auf noindex bliebe einer späteren Launch-Entscheidung vorbehalten (eine Zeile im Builder).
- **Keine Drafts-Verlinkung:** Nur geprüfte Artikel (`editorial-reviewed-preview`) werden verlinkt; Drafts (`treppenlift-angebote-vergleichen`) bleiben unverlinkt.
- **Keine Testurteile/Testsieger-Signale** auf Checklisten-Seiten (keine Experten-Claim ohne Beleg) — Passung zur Portal-Transparenz-Regel (KI-Unterstützung wird deklariert).
- **Keine automatische PDF-Datei** in Phase 1: Der Browser-Druck (A4-Print-CSS) ersetzt eine PDF-Datei in den SERP-Ausspielungen; eine echte PDF-Variante wäre nur bei nachgewiesenem Query-Bedarf („…pdf" Queries mit schwacher HTML-URL) ein Phase-4-Test mit eigener Kampagne. (SERP-„pdf"-Queries werden von HTML-Seiten mit sauberem Print-CSS ausreichend bedient; der OCR-/Objekt-Charakter bleibt erhalten.)

## Wire-in für den Parent

1. Builder existiert separat: `node scripts/build-checklists.mjs` (documented, nicht in generate.mjs verdrahtet — ausdrückliche Parent-Entscheidung ausstehend).
2. Empfohlene Verkettung, wenn verdrahtet wird: `"build": "node generate.mjs && node scripts/build-checklists.mjs"` in package.json; `build:launch` analog.
3. **Wichtig:** Die Consent- und Link-Tests der Site laufen über `dist/` rekursiv — die neuen Seiten in `dist/checklisten/` müssen denselben CMP-Vertrag erfüllen, was der Builder garantiert (gleicher Head-Vertrag wie generate.mjs). Bis zur Verdrahtung baut `npm run build` die Checklisten **nicht** — `node scripts/build-checklists.mjs` manuell laufen lassen.
4. Sitemap/Hub-Verlinkung vom Homepage/Artikel-Layout: bewusst **nicht** „still" eingebaut — Homepage-/Artikel-Verlinkung des Hubs (z. B. im `.guides`-Grid oder Footer) ist eine Parent-Entscheidung (Sichtbarkeit vs. preview-phase minimalism), keine Agent-Entscheid homepage-Architektur.
5. Die 6 Artikel-JSONs wurden nicht verändert; die Extraktion liest nur. Wenn eine Artikel-Sektion umstrukturiert wird, bricht der Builder mit benanntem Fehler („missing section/bullets/table"), statt leere Blätter zu erzeugen — Failsafe gegen stille Inhaltsverluste.
