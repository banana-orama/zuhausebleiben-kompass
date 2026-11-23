# Batch-Protokoll: Hilfsmittel-Zuzahlung 2027 (§ 61 SGB V Neufassung) — 23.11.2026

## Anlass
Refresh-Kandidat aus Batch 25 (17.11.): „Hilfsmittel-Zuzahlungsänderung 01.01.2027 (GKV-BSSG lt.
pflegekompass 7,50–15 €) bewusst NICHT im Artikel behauptet (nicht selbst verifiziert) → verifizieren,
dann in hilfsmittel-Artikeln“. Diese Lauf hat die Verifizierung gegen Primärquellen nachgeholt und in
3 Artikel eingearbeitet. **Kein neuer Artikel** (vorab 4 SERP-Kandidaten geprüft und mit Beleg
verworfen, siehe unten).

## Verifizierung (23.11.2026, Evidenz research/evidence/hilfsmittel-zuzahl-231126/)
1. **§ 61 SGB V live** (gesetze-im-internet, ISO-8859-1 + Entities dekodiert, sgb5-61-231126.html):
   „betragen 10 vom Hundert des Abgabepreises, **mindestens jedoch 5 Euro und höchstens 10 Euro**;
   allerdings jeweils nicht mehr als die Kosten des Mittels“ — `7,50`: 0 Treffer, `15 Euro`: 0 Treffer.
   → Die Änderung ist noch NICHT in Kraft; die Live-Artikel waren korrekt.
2. **GKV-Beitragssatzstabilisierungsgesetz** (BGBl. 2026 I Nr. 228, vom 24.07.2026, verkündet
   29.07.2026; PDF via KVN-Mirror → pdftotext, bgbl-2026-i-228-gkv-bstabg.txt):
   - „**23. § 61 wird durch den folgenden § 61 ersetzt:**“ mit Wortlaut „betragen **10 Prozent** des
     Abgabepreises, **mindestens jedoch 7,50 Euro und höchstens 15 Euro**; allerdings jeweils nicht
     mehr als die Kosten des Mittels“; zudem stationäre Maßnahmen 10 → 15 €/Kalendertag, Heilmittel/
     HKP „sowie 15 Euro je Verordnung“.
   - **Inkrafttreten:** Art. 8 Abs. 2 listet „Nummer 20 bis 23“ explizit: „**treten am 1. Januar 2027
     in Kraft**“. Das Datum steht im Gesetz selbst — die BMG-Klärungsdebatte (pta-Magazin) betrifft
     Art.-1-Nr. 23 nicht.
3. **GKV-Spitzenverband-PM 2293952** (27.07.2026, Extrakt committed, Roh-HTML uncommitted):
   „mindestens 5 Euro (**ab 2027: 7,50 Euro**)“, „höchstens 10 Euro (**ab 2027: 15 Euro**)“, „Bei zum
   Verbrauch bestimmten Hilfsmitteln ist die Zuzahlung auf höchstens 10 Euro (ab 2027: 15 Euro) im
   Monat begrenzt“.
4. **§ 33 SGB XI live** (Quellenstand-Träger des pflegekasse-Artikels): „auf Antrag“,
   „mindestens zwei Jahre“, „vor der Antragstellung“ verbatim bestätigt → checked_at legitim gebumpt.

## Umsetzung (content-ready/, chirurgische Text-Edits, kein json-Roundtrip)
| Artikel | Änderung |
|---|---|
| hilfsmittel-dusch-wc-uebernahme | Weg-1-Absatz + Tabelle „Aufsätze“-Zelle + 2 FAQ-Antworten um 2027-Satz ergänzt; Quelle [9] BGBl; § 61 checked_at → 2026-11-23 |
| hilfsmittel-pflegekasse-uebernahme | Krankenkassen-Absatz („Drittens die Krankenkasse“) um 2027-Satz ergänzt; Quelle [11] BGBl; § 61 + § 33 SGB XI checked_at → 2026-11-23 (Quellenstand-Zeile frisch) |
| rollator-auswahl-passform-kosten | Kostenträger-Absatz + Eigenanteil-FAQ um 2027-Satz ergänzt; Quelle [11] BGBl; § 61 checked_at → 2026-11-23 |

Wording-Grundsatz: heutige Werte (5/10 €) bleiben stehen und gelten bis 31.12.2026; die Änderung ist
als datierte Vorlauf-Notiz mit Gesetz + BGBl-Zitat ergänzt, keine Zusage-/Beratungsformulierung.

## Verworfene Artikel-Kandidaten (SERP 23.11., GSC weiter ohne Google-Sitzung)
1. **Badewanne mit Tür / Einsteigewanne**: dediziertes Domain-Ökosystem (diewannentuer.de ×2),
   pflegekompass- + pflege.de-Guides + seniorenlotse — dicht, dünne Verbesserungslücke.
2. **WC-Erhöhung/Toilettensitzerhöhung**: 5+ dedizierte Anbieterseiten + DAK institutionell;
   Kannibalisierung mit hilfsmittel-dusch-wc (GKV-Route 33.40.05).
3. **Hausnotruf nach Glasfaser-Umstellung**: 0 dedizierte Ratgeber, aber Belege nur ISP-Hilfeseiten/
   Foren/Techblogs — keine Ratgeber-fähige Primärquelle; Fern-Diagnose-Risiko.
4. **Rollstuhlgerechtes Bad (DIN 18040-Maße)**: 7+ dedizierte Seiten inkl. offiziellem LVR-Planungs-PDF,
   nullbarriere.de, HEWI, pflege-panorama (2026) — dicht.

## Gates/Tests
- `npm test` EXIT 0 (Partner A–F ALL PASS inkl. Playwright).
- `npm run build:launch` (60 Seiten, Sitemap 8 Checklist-URLs), danach:
  - `verify_hilfsmittel_zuzahl_231126.py` **0 FAILS** (46 Checks: 11 verbatim über 3 Primärquellen,
    3× JSON-Struktur/Quellen/Zitier-Integrität, 3× Built-HTML Needles + source-Anker + robots).
  - bestehendes `verify_duschwc_content.py` 0 FAILS (alle Alt-Needles unverändert grün).
  - `verify_checklists_build.py` ALL PASS (RSS/Sitemap unverändert).
  - `verify_hilfsmittel_zuzahl_mobile_231126.py`: 3 Seiten 390 px **0 px Overflow** + 2027-Satz im
    gerenderten Text + Screenshots (Vision-Check 1/3 sauber).
- Checklisten-HTML: keine 7,50-Übernahme (Checklisten-Inhalt vom §-61-Satz nicht betroffen).

## Refresh-Trigger (NEU)
- **01.01.2027**: § 61 SGB V Neufassung in Kraft → dann müssen die 3 Artikel die 7,50/15-€-Werte als
  AKTUELLE Werte führen und die Vorlauf-Formulierung („Zum 1. Januar 2027 hebt … an“) auf
  Gegenwartsform umstellen + Quellenstand prüfen. Gate-Needles („1. Januar 2027“, „7,50“) bleiben
  als Beweisstruktur; der JSON-Satz muss dann umgeschrieben werden.
- § 61-Änderung umfasst auch stationäre Maßnahmen (10 → 15 €/Tag) und Heilmittel/HKP
  („15 Euro je Verordnung“) — für unsere Artikel ohne Content-Bezug, aber beim nächsten
  Zuzahlungs-Refresh mitlesen.
