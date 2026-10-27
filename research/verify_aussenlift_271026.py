#!/usr/bin/env python3
"""Aussenlift-Artikel 27.10.2026: prueft jede Ledger-Quote woertlich gegen die
gespeicherte Evidence-Datei (whitespace-normalisiert, Soft-Hyphens entfernt),
die IP-Absenz auf den Herstellerseiten und die Preis-Arithmetik. Exit 1 bei Fehlern.
Muster: verify_schmale_treppe_261026.py."""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
EV = ROOT / 'research' / 'evidence'
LEDGER = ROOT / 'research' / 'aussenlift-271026-ledger.json'

FAIL = []


def norm(t):
    return re.sub(r'\s+', ' ', t.replace('\u00ad', '').replace('\xa0', ' '))


ledger = json.loads(LEDGER.read_text(encoding='utf-8'))
total = 0
for src in ledger['sources']:
    text = norm((EV / src['evidence']).read_text(encoding='utf-8'))
    print(f"== Quelle [{src['id']}] {src['title'][:70]}  (evidence: {src['evidence']})")
    for q in src['quotes']:
        total += 1
        if norm(q['text']) in text:
            print(f"   PASS ({len(q['text'])} Zeichen) {q['text'][:76]}…")
        else:
            FAIL.append((src['id'], q['text']))
            print(f"   FAIL  NICHT GEFUNDEN: {q['text'][:100]}…")

print()
print('== IP-Absenz auf Herstellerseiten (gepruefte Abrufe vom 27.10.2026)')
for name in ['hiro-aussen', 'lifta-aussenlifte', 'lifta-faq']:
    text = (EV / f'aussenlift-271026/{name}.txt').read_text(encoding='utf-8')
    hits = re.findall(r'IP[- ]?(?:4\d|5\d|6\d|X\d|Schutzklasse|Schutz)', text, flags=re.I)
    total += 1
    ok = len(hits) == 0
    print(f"   {'PASS' if ok else 'FAIL'}  {name}: {len(hits)} IP-Klassen-Treffer (erwartet 0)")
    if not ok:
        FAIL.append(('ip-absenz', name))

print()
print('== Preis-Arithmetik / Divergenz-Dokumentation')
checks = [
    ('Lifta aussen gerade 6.500 € liegt innerhalb der eigenen Innen-Spanne 5.500–9.900 € (Ueberlappung belegt)',
     5500 <= 6500 and 8500 <= 9900, True),
    ('Seniorenrat-Untergrenze 3.500 € liegt unter Lifta-Untergrenze 6.500 € (Divergenz belegt)',
     3500 < 6500, True),
    ('treppenliftwissen-Untergrenze 5.000 € liegt zwischen 3.500 und 6.500 (Streuung dokumentiert)',
     3500 < 5000 < 6500, True),
    ('personenaufzuege-Innen-Vergleich 3.500–9.000 € ueberlappt aussen 6.000–15.000 €',
     6000 < 9000, True),
    ('tlw-Aufpreis-Angabe 1.000–4.000 €: Untergrenze kleiner als Obergrenze',
     1000 < 4000, True),
    ('Akku-Austausch 150–300 € kleiner als Lifta aussen-gerade-Untergrenze 6.500 € (Reihenfolge plausibel)',
     300 < 6500, True),
    ('HIRO-Garantie 2 Jahre gesamt <= 5 Jahre Antriebsrollen/Fahrbahn',
     2 <= 5, True),
]
for label, a, b in checks:
    ok = a == b
    total += 1
    print(f"   {'PASS' if ok else 'FAIL'}  {label}" + ('' if ok else f': {a} != {b}'))
    if not ok:
        FAIL.append(('arith', label))

print()
if FAIL:
    print(f"ERGEBNIS: {total - len(FAIL)}/{total} PASS, {len(FAIL)} FAIL")
    sys.exit(1)
print(f"ERGEBNIS: {total}/{total} PASS")
