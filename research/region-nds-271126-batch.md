# Batch-Protokoll: Region Niedersachsen (sechste Region) — 27.11.2026, Cron 09:23

## Einheit
`data/region-niedersachsen.json` — sechste ausführlich recherchierte Region nach dem NRW/Bayern/Sachsen/BW/Hessen-Muster, gebaut auf dem vollständig dokumentierten Screen vom 26.11. (`research/region-screen-261126-nds.md`, Ledger 108/108 verbatim, 20 Quellen). Batch 30 (Hessen) hatte NDS als 6.-Region-Basis eingeplant; GSC/Awin/Agency-Einheiten blieben Betreiber-blockiert.

## Inhalt (Kernbefunde, alle heute frisch gegen Live-Originale verifiziert)
- **Weg 2 (Kern):** NBank „Barrierereduzierende Modernisierung von selbstgenutztem Wohneigentum" (RL Wohneigentum 2026, RdErl. MW 25.06.2026, Nds. MBl. 2026 Nr. 317). Reiner Zuschuss bei Gesamtkosten bis 15.000 €: EG A bis 40 %/max. 6.000 €, EG B+C bis 30 %/max. 4.500 €; ab 15.001 € Darlehen (15 J., 0 %, Tilgung 2 %) + gebundener Zuschuss (EG A ≤50k: bis 35 %/17.500 €; B+C: 25 %/12.500 €). Eigenmittel 10 %/7,5 %; Zuwendungszeitraum 15 J. (5 J. bei ≤15.000 €); Auszahlung 30/60/10; Bearbeitungsentgelt 1 %/0,75 %; Verwaltungskostenbetrag 0,5 %.
- **Treppenlift-Ehrlichkeit (Differenzierung zum Sachsen-Fund):** „Treppenlift" 0× in RL, Produktinfo, Produktseite, VV NWoFG, Ministeriumsseite (je frisch gezählt); „Rollstuhl" 0× in der RL. Förderfähigkeit nur über die Barrieren-Funktionsdefinition (RL 7.3 verbatim). Praxis-Auslegung des **Nichtamtlichen** Niedersachsenbüros Neues Wohnen (Träger FWG e.V. + BAG Wohnungsanpassung e.V., Impressum belegt) mit Interessenkennzeichnung: „auch der Badumbau und Treppenlift, aber nicht der alleinige Treppenlift" — als nicht bindend markiert + Sachsen-Vergleich.
- **Strukturelle Grenze:** Programm nur für selbst genutztes Wohneigentum — Mieter leer aus (schwächer als Sachsen); NBank-Mietwohnungs-Produkt als Investorenprogramm eingeordnet („5.000 Euro für jede barrierefrei nutzbare Wohnung gemäß DIN 18040-2" — Zahl an Vermieter, nicht an Mieter).
- **Vorhabensbeginn-Ausnahme:** <100.000 € Ausgaben → Beginn ab Antragstellung zugelassen (Treppenlift-Maßnahmen fallen darunter) — plus ehrlicher Hinweis auf das Ablehnungsrisiko.
- **Status:** offen, aber Wartezeit-Wortlaut der Produktseite („besonders hohes Antragsaufkommen …"), datiert 27.11.2026, kein Stopp.
- **Einkommen:** EG A 21.250/28.750/+3.750 € (GVBl. 2025 Nr. 7, ab 01.03.2025); B +40 %, C +60 % (bestimmte Gebiete); Freibetrag 4.000 € je Person GdB ≥ 50/PG 2-5 (DVO § 3 — „wenigstens 50"-Wortlaut); Tragbarkeit 675/600/475 €.
- **Weg 3:** EGH über die Kommunen (Träger-Satz verbatim: Landkreise, kreisfreie Städte, Region Hannover, Städte Hannover/Göttingen/Hildesheim/Lingen (Ems)/Lüneburg — bewusst KEINE Zahlformel, 36-gegen-37-Frage offen gelassen); Antrag fristlos, Leistungsbeginn ab Antragstellungs-Monat; Vorrangprüfung + Eigenbeteiligung (Serviceportal, SPA heute im Browser gerendert).
- **Weg 1:** Pflegekasse bundesweit 0 Beträge; MS-Broschüre-Satz als ministerialer Ratgeber-Kontext gekennzeichnet. **Weg 4:** KfW 455-B-Stopp-Wortlaut + 2027-Bedingung, Kredit 159 mit Treppenlifte-Katalog und Kombi-Ausnahme (Stand 27.11.).
- **Kommunale Zusatzprogramme:** als amtlich nicht dokumentiert markiert (LHH-Programm = Neubau-Mietwohnraum, Treppenlift 0×; Siemer-Vendor-Claim unverifiziert) — nur Prüfhinweis „bei der Wohnraumförderstelle nachfragen".
- **Bewusst 0×:** Pflegekassen-Beträge (4.180/16.720), Partner-Marker, U+00AD, Zahlen aus ALT-Quellen (MW-Seite 15-%-Eigenkapital, MS-Broschüre 3.000 €, NBank-2017-Produktinfo).

## Verifikation (Parent, 27.11., frische Abrufe)
- `research/evidence/region-nds-271126/parent_verify_live.py` **92/92 PASS**: NBank-Produktseite + Produktinfo-PDF + RL-PDF + GVBl-Änderungsgesetz + DVO + VV (je 3 pdftotext-Modi mit De-Hyphenation), Beratungsstellen, Investoren-PDF, MW (ALT-Marker „15 Prozent" live bestätigt = dokumentierte Nicht-Zahlenquelle), soziales.niedersachsen.de EGH + SPN, Niedersachsenbüro Fördermöglichkeiten + Impressum, MS-Broschüre, KfW 455-B/159, §§ 113/77 SGB IX + 40 SGB XI (4 180/16 720 geschützt) + 554 BGB. **Skript-Lektion:** die Träger-Namen des Niedersachsenbüros stehen in IMG-alt-Attributen → Roh-HTML-Check statt Tag-Strip.
- **Serviceportal-SPA** (pstId=8664328, JS+ALTCHA) heute im Browser gerendert: 3 Kernfragmente live verifiziert, Extrakt `serviceportal-nds-egh-8664328-rendered-271126.txt` (der Screen vom 26.11. hatte den SPA-Render als Evidence; heute frisch wiederholt).
- `verify_quotes.py` **39/39 PASS**: jedes Content-Verbatim einzeln gegen Live-Original/SPA-Extrakt.
- **Zitat-Treue-Fund vor Build:** Lead/Weg-2-Zitat stand im Dativ („Barrierereduzierenden …") statt exakter Nominativ-Quellform → JSON korrigiert (Wortlaut-Zitate immer nominativ exakt).

## Gates
- Content-Gate `research/verify_region_nds_build_271126.py` **127/127 PASS** (LAUNCH-dist): Struktur/robots/Canonical, 61 Kernwordlaute, Wortlaut-Ehrlichkeits-Needles (Absenz-Dokumentation, je-0-Treffer-Zeile, Nichtamtlich-Kennzeichnung, Nicht-Bindend-Hinweis), 6 FAQs, 21 Quellen-URLs, Related/CTA absolut, 11 Absenzen (inkl. WIBank/L-Bank/Friedrichshafen-Kreuz-Regionen), Hub 6-Regionen + alte Prosa 0×, Sitemap exakt 6 Region-URLs, RSS 41.
- `npm test` **EXIT 0** (titles_meta 0 Verletzungen nach Desc-Kürzung 167→146, Playwright consent **22 passed**, Partner A–F), `verify_checklists_build` ALL PASS. Danach `build:launch` (npm-test-dist ist PREVIEW) und Gates erneut auf LAUNCH-dist.
- Mobile `verify_region_nds_mobile_271126.py`: 390 px **0 px Overflow**, 2 Tabellen im Scroll-Muster (346 px), 3 CTAs, 6 FAQs, 21 Quellen, Related vollständig; Screenshots + Vision: Mobile sauber, Konditionen-Tabelle 9/9 Zeilen vollständig.
- Tabellenbreiten-Messung (`check_nds_table_widths.py`): NDS-Wege-Tabelle inner 773 px vs. Container 740 px (scrollable) — **identisches site-weites Muster wie Hessen (777 px)**, kein Defekt, im Scroll-Container gelöst.

## Deploy
Commit + CI + Live-Readback + IndexNow: siehe launch-state 27.11.

## Refresh-Trigger NEU
- **NBank-Produktseite-Wartezeit-Banner** (datiert 27.11.2026 im Gate „je 0 Treffer, geprüft am 27.11.2026" + Wartezeit-Wortlaut): bei jedem Re-Check Datum pflegen; Förderstopp-Formulierung (analog KfW 455-B) würde eine Content-Änderung auslösen.
- **RL Wohneigentum 2026 / NWoFG-Einkommensgrenzen**: jährliche Anpassungs-Prüfung (GVBl.-Beobachtung); DVO-Freibeträge.
- **Nichtamtliche Auslegung (Niedersachsenbüro)**: falls das Land den Treppenlift künftig amtlich benennt (RL-Änderung), Ehrlichkeits-Abschnitt + FAQ aktualisieren.
- **Offene Fragen (Screen §6 unverändert):** Serviceportal-EGH-Akkordeons (formloser Antrag/Gesamtplan/Fristen — nicht zitiert), kommunale Ergänzungsprogramme Region Hannover (unbelegt), NBank-Bewilligungsstand nicht publiziert.
