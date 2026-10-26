#!/usr/bin/env python3
"""Schmale-Treppe-Artikel 26.10.2026: prueft jede Ledger-Quote woertlich gegen die
gespeicherte Evidence-Datei (whitespace-normalisiert, Soft-Hyphens entfernt)
und die Einheiten-Arithmetik. Exit 1 bei fehlender Assertion.
Muster: verify_steuer_261026.py."""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
EV = ROOT / 'research' / 'evidence'
LEDGER = ROOT / 'research' / 'schmale-treppe-261026-ledger.json'

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
print('== Einheiten-Arithmetik / Konsistenz')
checks = [
    ('DIN 18065: 800 mm = 80 cm (Fachportal-Angabe, ≤ 2 Wohnungen)', 800 / 10, 80),
    ('DIN 18065: 1.000 mm = 100 cm (Fachportal-Angabe, allgemein)', 1000 / 10, 100),
    ('Klappmass 31–34 cm ab Wand liegt unter 60 cm Restlaufbreite (MVV TB, Muster)', 34 < 60, True),
    ('Schmalster Herstellerwert 61 cm unterhalb der Range "die meisten 62–77 cm"', 61 < 62, True),
    ('HIRO gerade 4.000–10.000 € liegt unter kurvig 9.000–17.000 €', 4000 < 9000 and 10000 < 17000, True),
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
