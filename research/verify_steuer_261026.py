#!/usr/bin/env python3
"""Steuer-Artikel 26.10.2026: prüft jede Ledger-Quote wörtlich gegen die gespeicherte
Evidence-Datei (whitespace-normalisiert, Soft-Hyphens entfernt) und die Kern-Arithmetik.

Exit 1 bei fehlender Assertion. Muster: verify_foerder_2610.py (Lessons eingearbeitet)."""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
EV = ROOT / 'research' / 'evidence'
LEDGER = ROOT / 'research' / 'steuer-261026-ledger.json'

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
print('== Arithmetik')
checks = [
    ('6.000 € × 20 % = 1.200 € (Heute: Höchstbetrag)', 6000 * 0.20, 1200),
    ('2.800 € Lohnanteil × 20 % = 560 € (Beispielrechnung)', 2800 * 0.20, 560),
    ('2.800 + 3.700 = 6.500 € Beispielrechnung', 2800 + 3700, 6500),
    ('900 € / 15 % → 6.000 € (Entwurf 2027)', 900 / 0.15, 6000),
    ('1.200 € / 20 % → 6.000 € (Konsistenz)', 1200 / 0.20, 6000),
]
for label, a, b in checks:
    ok = a == b
    total += 1
    print(f"   {'PASS' if ok else 'FAIL'}  {label}: {a}" + ('' if ok else f' != {b}'))
    if not ok:
        FAIL.append(('arith', label))

print()
if FAIL:
    print(f"ERGEBNIS: {total - len(FAIL)}/{total} PASS, {len(FAIL)} FAIL")
    sys.exit(1)
print(f"ERGEBNIS: {total}/{total} PASS")
