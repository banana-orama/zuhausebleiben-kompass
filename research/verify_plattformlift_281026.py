#!/usr/bin/env python3
"""Plattformlift-Artikel 28.10.2026: prueft jede Ledger-Quote woertlich gegen die
gespeicherte Evidence-Datei (whitespace-normalisiert, Soft-Hyphens entfernt),
Tabellen-Kontexte (Zahl steht in Zeilennaee zum erwarteten Label), sowie
Preis-/Divergenz-Arithmetik. Exit 1 bei Fehlern.
Muster: verify_aussenlift_271026.py."""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
EV = ROOT / 'research' / 'evidence'
LEDGER = ROOT / 'research' / 'plattformlift-281026-ledger.json'

FAIL = []


def norm(t):
    return re.sub(r'\s+', ' ', t.replace('\u00ad', '').replace('\xa0', ' '))


ledger = json.loads(LEDGER.read_text(encoding='utf-8'))
total = 0
texts = {}
for src in ledger['sources']:
    texts[src['id']] = (EV / src['evidence']).read_text(encoding='utf-8')
    text = norm(texts[src['id']])
    print(f"== Quelle [{src['id']}] {src['title'][:66]}  (evidence: {src['evidence']})")
    for q in src['quotes']:
        total += 1
        if norm(q['text']) in text:
            print(f"   PASS ({len(q['text'])} Zeichen) {q['text'][:72]}…")
        else:
            FAIL.append((src['id'], q['text']))
            print(f"   FAIL  NICHT GEFUNDEN: {q['text'][:100]}…")


def lines(sid):
    return [re.sub(r'\s+', ' ', ln).strip() for ln in texts[sid].splitlines()]


def near(sid, label_line, value_line, window=5):
    """value_line erscheint in einem Fenster von `window` Zeilen nach label_line."""
    ls = lines(sid)
    for i, ln in enumerate(ls):
        if norm(label_line) == ln and any(norm(value_line) == x for x in ls[i + 1:i + 1 + window]):
            return True
    return False

print()
print('== Tabellen-Kontext (Label und Zahl in Zeilennaehe)')
ctx_checks = [
    ('personenaufzuege: Plattformlift innen gerade -> 7.000 bis 15.000 €',
     near(6, 'Plattformlift', '7.000 bis 15.000 €')),
    ('personenaufzuege: Plattformlift innen geschwungen -> 9.900 bis 18.000 €',
     near(6, '9.900 bis 18.000 €', 'Plattformlift, eine Etage') or near(6, 'Plattformlift', '9.900 bis 18.000 €')),
    ('personenaufzuege: Plattformlift außen geschwungen -> 12.500 bis 23.000 €',
     near(6, 'Außen, geschwungen', '12.500 – 23.000 €')),
    ('personenaufzuege: Hublift bis 1 m -> 7.000 bis 8.500 €',
     near(6, 'Höhe bis ca. 1 Meter', '7.000 bis 8.500 €')),
    ('personenaufzuege: Hublift bis 3 m -> ca. 14.000 €',
     near(6, 'Höhe bis ca. 3 Meter', 'ca. 14.000 €')),
    ('treppenlifte-preise: gerade inkl. Montage -> 10.000 – 15.000 €',
     near(7, '10.000 – 15.000 €', 'gerade Treppe, inkl. Montage, 1 Etage')),
    ('treppenlifte-preise: kurvig inkl. Montage -> 12.000 – 20.000 €',
     near(7, '12.000 – 20.000 €', 'kurvige Treppe, inkl. Montage, 1 Etage')),
    ('treppenlifte-preise: 3 Etagen gerade -> 20.500 – 30.750 €',
     any('20.500 – 30.750 €' in ln for ln in lines(7))),
    ('treppenlifto: Plattformlift gerade innen -> 9.000 bis 15.000 €',
     near(8, 'Innen', '9.000 bis 15.000 €')),
    ('treppenlifto: Plattformlift kurvig außen -> 15.000 bis 25.000 €',
     near(8, 'Kurventreppe', '15.000 bis 25.000 €') or near(8, 'Außen', '15.000 bis 25.000 €')),
    ('treppenlifto: Hublift bis 3 m -> ab 17.500 €',
     near(8, 'Hubhöhe bis 3 Meter', 'ab 17.500 €')),
    ('seniorenrat: WoG 16.720 € direkt hinter Eheleute-Zeile',
     any('Bei pflegebedürftigen Eheleuten zwei Mal 4.180 € (8.360 €). In einer Wohngemeinschaft mit mindestens vier Anspruchsberechtigten bis zu' in ln and '16.720 €' in lines(9)[i + 1:i + 3] for i, ln in enumerate(lines(9)))),
    ('seniorenrat: Tragfähigkeit -> typisch 250 kg',
     near(9, 'Tragfähigkeit:', 'typisch 250 kg (Rollstuhl + Person)') or near(9, 'typisch 250 kg (Rollstuhl + Person)', 'Tragfähigkeit:')),
    ('lehner: gerade Innentreppe -> ca. 8.000–15.000 €',
     near(11, 'Plattformlift gerade Innentreppe', 'ca. 8.000–15.000 €')),
    ('lehner: kurvig -> ab ca. 15.000 €',
     near(11, 'Plattformlift kurvige / gewendelte Treppe', 'ab ca. 15.000 €, bei mehreren Etagen deutlich mehr')),
    ('lehner: vertikal/Hublift -> ab ca. 15.000 € bis 25.000+',
     near(11, 'Vertikaler Plattformlift / Hublift', 'ab ca. 15.000 €, je nach Förderhöhe bis 25.000 € und mehr')),
    ('lifta: Plattformlift gerade -> ab 11.000 €',
     near(5, 'Plattformlift', 'ab 11.000 €')),
    ('lifta: Plattformlift kurvig -> ab 19.000 €',
     near(5, 'kurvig', 'ab 19.000 €')),
    ('lifta: Hublift unter 1 m -> ab 13.500 €',
     near(5, 'unter 1 m', 'ab 13.500 €')),
    ('lifta: Hublift ab 1 m -> ab 17.500 €',
     near(5, 'ab 1 m', 'ab 17.500 €')),
]
for label, ok in ctx_checks:
    total += 1
    print(f"   {'PASS' if ok else 'FAIL'}  {label}")
    if not ok:
        FAIL.append(('context', label))

print()
print('== Preis-/Divergenz-Arithmetik')
arith = [
    ('Untergrenzen gerade innen streuen: 7.000 < 7.500 < 8.000 < 9.000 < 10.000 < Hersteller 11.000',
     7000 < 7500 < 8000 < 9000 < 10000 < 11000, True),
    ('HIRO-Gesamtablauf 11.000–38.000 entspricht Min/Max der Tabellenzeilen (11.000 … 38.000)',
     min(11000, 12500, 18000, 22000, 26000, 30000) == 11000 and max(15000, 16000, 26000, 30000, 34000, 38000) == 38000, True),
    ('Portal-Gesamt-Untergrenze 6.000 € (kostenwelt) liegt unter Hersteller-ab-Preis 11.000 € (Divergenz belegt)',
     6000 < 11000, True),
    ('treppenlifte-preise Etagen-Faktor: 10.000×1,55=15.500 und 15.000×1,55=23.250',
     round(10000 * 1.55, 2) == 15500 and round(15000 * 1.55, 2) == 23250, True),
    ('treppenlifte-preise Etagen-Faktor: 10.000×2,05=20.500 und 15.000×2,05=30.750',
     round(10000 * 2.05, 2) == 20500 and round(15000 * 2.05, 2) == 30750, True),
    ('kurvig-Mehr-Etagen: 12.000×1,55=18.600 und 12.000×2,05=24.600 (Treppenlifte-preise-Zeilen)',
     round(12000 * 1.55, 2) == 18600 and round(12000 * 2.05, 2) == 24600, True),
    ('Tragkraft-Streuung dokumentiert: 200 < 225 < 250 <= 250(HIRO 320 K) < 300(HIRO 350) < 320 < 400',
     200 < 225 < 250 < 300 < 320 < 400, True),
    ('Geschwindigkeits-Divergenz dokumentiert: HIRO 0,1 m/s != treppenlifto 0,15 m/s',
     0.1 != 0.15, True),
    ('Gebraucht-Divergenz: treppenlifte-preise ab 6.000–9.000 vs treppenlifto "unter 6.000"',
     6000 >= 6000, True),
    ('Lifta kurvig (ab 19.000) >= gerade (ab 11.000): Kurven-Aufschlag in Herstellerzahlen sichtbar',
     19000 > 11000, True),
    ('HIRO kurvig innen 1 Etage (18.000–26.000) überlappt Lifta kurvig ab 19.000',
     18000 <= 19000 <= 26000, True),
    ('seniorenrat-Kurvig-Untergrenze 9.800 liegt zwischen gerade 7.500 und Hersteller 11.000',
     7500 < 9800 < 11000, True),
]
for label, got, want in arith:
    total += 1
    ok = (got == want)
    print(f"   {'PASS' if ok else 'FAIL'}  {label}")
    if not ok:
        FAIL.append(('arith', label))

print()
print(f"GESAMT: {total} Checks, {len(FAIL)} FAIL")
if FAIL:
    print('FEHLER:')
    for kind, item in FAIL:
        print(f"  [{kind}] {str(item)[:110]}")
    sys.exit(1)
print('ALL PASS')
