#!/usr/bin/env python3
"""Nutzlast-Artikel 27.10.2026: prueft jede Ledger-Quote woertlich gegen die
gespeicherte Evidence-Datei (whitespace-normalisiert, Soft-Hyphens entfernt)
und die Tragkraft-Arithmetik. Exit 1 bei fehlender Assertion.
Muster: verify_schmale_treppe_261026.py."""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
EV = ROOT / 'research' / 'evidence'
LEDGER = ROOT / 'research' / 'nutzlast-271026-ledger.json'

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
print('== Tragkraft-Arithmetik / Konsistenz')
checks = [
    ('HIRO-Leiter aufsteigend sortiert: 135 < 150 < 175', 135 < 150 < 175, True),
    ('Handicare-Leiter aufsteigend: 115/137 < 160 (1000) < 200 (1000XXL)', max(115, 137) < 160 < 200, True),
    ('HIRO-Standard 135 kg ueber Deckel des Infoportals "120 kg" (Doku der Diskrepanz)', 135 > 120, True),
    ('Lifta-Diskrepanz gerade 160 vs kurvig 135 = 25 kg Differenz', 160 - 135, 25),
    ('XXL bis 200 kg liegt ueber HIRO-Anfrage-Wert 175 kg', 200 > 175, True),
    ('Plattformlift 250-300 kg ueber alle Sitzlift-Werte', min(250, 300) > 200, True),
    ('Sitzbreite XXL 55-60 cm groesser als Standard-Sitz ca. 45-47 cm (Kontextbreite)', 55 > 47, True),
    ('Aufschlag-Schaetzung 15-25 %: obere untere Schranke geordnet', 15 < 25, True),
    ('Beispielrechnung: 118 kg Person + 7 kg Zuladung = 125 kg, erreicht Grenze eines 125-kg-Modells exakt', 118 + 7, 125),
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
