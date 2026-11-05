# Batch 8 / Briefing 17: Hausnotruf kündigen — Research-Protokoll

Prüfdatum: 05.11.2026 (CET). Artikel: `content-ready/hausnotruf-kuendigen.json` (status: editorial-reviewed-preview).
Cluster: Care/Hausnotruf (Slug-Regex `^(hausnotruf|...)` deckt den Slug in article-renderer.mjs UND test_cross_links.py bereits ab — geprüft, keine Renderer-OP nötig).

## 1. Themenwahl und Abgrenzung (kein Kanibalisieren)

Bestand vor dem Lauf (Cluster Hausnotruf):
- hausnotruf-kosten-anbieter-vergleich (Kosten, Anbieter, Pflegekasse 27 €, Vertrag/Laufzeit als EINE Sektion, Vergleichscheckliste)
- hausnotruf-sturzerkennung-oder-knopf (Funktionsprinzip/Eignung)
- hausnotruf-mobil-gps-unterwegs (mobil/GPS/ohne Festnetz)

Gewählte Suchintention: **„Hausnotruf kündigen"** (Post-Kauf-Intention: Frist, Widerruf, Button, Todesfall, Umzug, Wechsel).
Abgrenzung nach innen: Der Vergleichsartikel behandelt Laufzeit/Widerruf in einer Sektion; die neue Seite bedient die eigene Intention (aktiver Vertrag beenden) und FUNNELT in die Vergleichsseite (Placement-Träger, Malteser 10-€-CPL-Beratungstermin live). Nach außen: Wettbewerber (seniorenhaushalt24, pflegeweide, vertrag-kuendigen.com, alarmbands, kuendigungmuster) sind dünn, meist ohne Gesetzestext-Basis, ohne Pflegekassen-Wechsel-Warnung.

Eigene Verbesserung (Konkurrenz hat keiner):
1. Gesetzestext-Basis: § 309 Nr. 9 BGB (24-Monats-Kappe, Verlängerungsgrenzen, 1-Monat-Frist), § 312k BGB (Kündigungsbutton + Abs. 6: fehlender Button → jederzeit ohne Frist kündbar), § 355/§ 356 BGB (Widerruf), § 1922 BGB (Todesfall/Gesamtrechtsnachfolge).
2. Wechsel-Falle: Pflegekasse zahlt nur bei Anbietern, die Vertragspartner der Pflegekasse sind (VZ verbatim) — vor Kündigung prüfen, nicht danach.
3. Geräte-Rückgabe und Doppelvertrag-Timing als praktischer Abschlussblock.

Bewusst NICHT übernommen: Die pflegemittelbox-Aussage „Die Verbraucherzentrale empfiehlt Hausnotrufe ohne feste Laufzeit … Kündigungsfrist von höchstens zwei Wochen … fristlose Kündigung im Todesfall" — die zitierte VZ-Seite (Stand 29.07.2026, direkt abgerufen) enthält diese Aussage NICHT (geprüft, grep „kündi/widerruf/laufzeit/frist" = 0 Treffer im Artikelkörper). Phantom-Zitat vermieden. Ebenso nicht übernommen: Anbietertabelle mit Preisen aus BILD/Sekundärquellen (keine Primärverifizierung), pflege.net/hausnotruf-vertrag (403 Bot-Wall beim Abruf, daher ohne Verifizierung nicht zitiert).

## 2. SERP-Check (05.11.2026, Websuche, keine Rangfolge/Volumendaten)

Queries: „Hausnotruf kündigen Frist Vorlage Anbieter wechseln", „Hausnotruf Vertrag Laufzeit Mindestvertragsdauer 24 Monate kündigen".
Treffer (Auswahl): seniorenhaushalt24 („Fristen von 14 Anbietern und ein Musterschreiben" — undatiert, keine Gesetzestexte), pflegeweide („Frist, Todesfall, Umzug ins Pflegeheim" — nennt § 309 Nr. 9-ähnliche Regeln ohne Normverifizierung), pflege-helfer24 (Betreuungsvollmacht-Winkel), alarmbands + kuendigungmuster (Generatoren/Thin), bundesverbraucherhilfe (Kündigungsbutton-Allgemeinwissen), VdK Hamburg (funktionaler Artikel ohne Vertragsfocus).
Intention: konkret-praktisch (Frist + Weg + Schreiben). Kein dominanter redaktioneller Standardartikel mit Normbelegen → Vermittler-/Ratgeber-Positionierung erklärbar.

## 3. Primärquellen (direkt abgerufen 05.11.2026, Evidenz: research/evidence/hausnotruf-kuendigen-051126/)

| # | Quelle | Abruf | Kernaussagen (verbatim im Ledger) |
|---|---|---|---|
| 1 | Verbraucherzentrale: Hausnotrufsysteme erklärt (Stand 29.07.2026) | 200 | „Der Hausnotrufanbieter muss Vertragspartner der Pflegekasse sein." · „Mit Pflegegrad übernimmt die Pflegekasse bis zu 27 Euro monatlich." · Basistarif = Gerät, Funksender, Installation/Einweisung, 24h-Zentrale · Antrag formlos |
| 2 | § 309 BGB (gesetze-im-internet, ISO-8859-1-Pipeline) | 200 | Nr. 9 lit. a: länger als zwei Jahre bindende Laufzeit unwirksam · lit. b: stillschweigende Verlängerung nur unbestimmte Zeit + jederzeit kündbar mit höchstens einem Monat · lit. c: Kündigungsfrist max. ein Monat vor Ablauf |
| 3 | § 312k BGB | 200 | Abs. 2: Schaltfläche „Verträge hier kündigen" + Bestätigungsseite „jetzt kündigen" · Abs. 4: sofortige Bestätigung Datum/Uhrzeit in Textform · Abs. 5: kein Zeitpunkt → frühestmöglicher Termin · Abs. 6: fehlen Schaltfläche/Seite → jederzeit ohne Einhaltung einer Kündigungsfrist kündbar |
| 4 | § 355 BGB | 200 | Abs. 1: Widerruf durch Erklärung, keine Begründung, rechtzeitige Absendung genügt · Abs. 2: „Die Widerrufsfrist beträgt 14 Tage." |
| 5 | § 356 BGB | 200 | Abs. 4: ohne Belehrung Erlöschen spätestens zwölf Monate und 14 Tage · Abs. 5 Nr. 2: Erlöschen bei Dienstleistungen mit vollständiger Erbringung bei Zustimmung vor Beginn |
| 6 | § 1922 BGB | 200 | Abs. 1: Vermögen geht als Ganzes auf die Erben über |
| 7 | VZ: Verträge wirksam widerrufen (Stand 28.07.2026) | 200 | Widerrufsfrist 14 Tage · ohne Belehrung 12 Monate und 14 Tage · Textform (E-Mail, SMS, Fax, Webformular) · Beweise aufheben + Bestätigung fordern |
| 8 | Malteser: Hausnotruf (gelisteter Partner) | 200 | „Sie haben jederzeit die Möglichkeit, den Hausnotruf mit einer Frist von einem Monat zum Monatsende zu kündigen." (Anbieterangabe) |
| 9 | Malteser: FAQ (gelisteter Partner) | 200 | „Der Vertrag kann jederzeit in Textform, also per Brief, E-Mail, Fax oder über das Online-Formular, mit einer Frist von 1 Monat zum Monatsende gekündigt werden." (Anbieterangabe) |

Nicht-fundierte Normen bewusst gemieden: § 309a BGB existiert nicht mehr (404 beim Abruf — 2022 in § 309 integriert), Art. 246 EGBGB ebenfalls abgeschafft (404) — dadurch keine veralteten Normzitate. § 620 BGB (Dienstvertrag-Spezialfall) bewusst nicht als Kündigungsgrundlage verwendet, da § 309 Nr. 9 + § 312k die tragenden Normen sind.

## 4. Grenzen der Aussagen

- „In Allgemeinen Geschäftsbedingungen" als Qualifizierer beibehalten (§ 309 gilt für AGB; individuell vereinbarte Laufzeiten sind nicht Nr. 9 unterworfen) — im Artikel sichtbar gemacht.
- Todesfall-Nachweispflichten (Todesanzeige/Erbschein) als übliche Anbieterpraxis formuliert, ohne konkrete Frist-/Unterlagenbehauptung.
- Keine Vorlage mit vollständiger Rechtswirkung („Muster") — stattdessen sieben Bausteine des Schreibens; kein Rechtsrat.
- Preiserhöhungs-Kündigungsrecht bewusst NICHT behandelt (kein verifizierbarer Norm-/Anbieterbeleg im Abruf).

## 5. Produktion

- Eigene Schema-Grafik `assets/images/hausnotruf-kuendigen-wege.svg` (drei Wege + Prüfband, Haus-Stil wie Mobil-Grafik, nummerierte Marker, Umlaut-frei, Stand im desc; Screenshot-Sichtkontrolle + Geometrie-Check nach Build).
- In-Artikel-Checkliste (Sektion 8, bullets) als Entscheidungshilfe; eigenständige druckbare Checklisten-Seite bewusst auf den nächsten Lauf verschoben (build-checklists-CHECKLISTS-Entry + Sitemap/JSON-LD-Zähler dann gemeinsam).
- specialMap-CTA: hausnotruf-kuendigen → /hausnotruf-kosten-anbieter-vergleich.html („Kosten & Anbieter vergleichen") — Themenkonsistenz: Wechselnde vergleichen Anbieter.
- Cross-Whitelist (data/cross-links.json): hausnotruf-kuendigen → [hausnotruf-kosten-anbieter-vergleich, hilfsmittel-pflegekasse-uebernahme].
- Counter-Bumps: test_articles.py 27→28; verify_checklists_build.py „rss has 27"→28.
- Neues Content-Support-Gate: research/verify_kuendigen_content_051126.py (alle JSON-Keys gegen built HTML, Zitate lösen auf, Related im Care-Cluster, CTA-Ziel Vergleichsseite); Live-Gate: research/verify_kuendigen_live_051126.py.

## 6. Fortsetzungspfad (nächster Lauf)

1. Druckbare Checklisten-Seite „Hausnotruf kündigen & wechseln" (build-checklists.mjs Entry, Sitemap-Zähler 7→8, JSON-LD 6→7 gemeinsam bumpen).
2. GSC-Queries, sobald Google-Sitzung verfügbar (Zugangslücke dokumentiert in operations/ACCESS-STATE.md).
3. Liftstar-Follow-up (Keychain-Blocker) unverändert offen.
