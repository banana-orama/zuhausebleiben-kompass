#!/usr/bin/env python3
"""Wohnumfeld-Artikel 02.11.2026: prüft jede Ledger-Quote wörtlich gegen die gespeicherte
Evidence-Datei (whitespace-normalisiert, Soft-Hyphens entfernt) und die Kern-Arithmetik.

Exit 1 bei fehlender Assertion. Muster: verify_steuer_261026.py."""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
EV = ROOT / 'research' / 'evidence'
LEDGER = ROOT / 'research' / 'wohnumfeld-021126-ledger.json'

FAIL = []


def norm(t):
    return re.sub(r'\s+', ' ', t.replace('\u00ad', '').replace('\xa0', ' '))


def read_text_any(p):
    raw = p.read_bytes()
    text = None
    for enc in ('utf-8', 'iso-8859-1'):
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    if text is None:
        text = raw.decode('utf-8', errors='replace')
    if p.suffix == '.html':
        text = re.sub(r'<script[^>]*>.*?</script>', ' ', text, flags=re.S | re.I)
        text = re.sub(r'<style[^>]*>.*?</style>', ' ', text, flags=re.S | re.I)
        text = re.sub(r'<!--.*?-->', ' ', text, flags=re.S)
        text = re.sub(r'<[^>]+>', ' ', text)
        import html as _html
        text = _html.unescape(text)
    return text


ledger = json.loads(LEDGER.read_text(encoding='utf-8'))
total = 0
for src in ledger['sources']:
    text = norm(read_text_any(EV / src['evidence']))
    print(f"== Quelle [{src['id']}] {src['title'][:70]}  (evidence: {src['evidence']})")
    for q in src['quotes']:
        total += 1
        qtext = q['text'] if isinstance(q, dict) else q
        if norm(qtext) in text:
            print(f"   PASS ({len(qtext)} Zeichen) {qtext[:76]}…")
        else:
            FAIL.append((src['id'], qtext))
            print(f"   FAIL  NICHT GEFUNDEN: {qtext[:100]}…")

print()
print('== Arithmetik')
checks = [
    ('9.400 − 4.180 = 5.220 Eigenanteil (fiktives Beispiel)', 9400 - 4180, 5220),
    ('4 × 4.180 = 16.720 (WG-Deckel)', 4 * 4180, 16720),
    ('16.720 / 8 = 2.090 je Person (BMG-Wohngruppen-Beispiel)', 16720 / 8, 2090),
    ('16.720 / 5 = 3.344 je Person bei fünf Berechtigten', 16720 / 5, 3344),
    ('3 Wochen ≈ 21 Tage Konsistenz', 3 * 7, 21),
    ('5 Wochen ≈ 35 Tage Konsistenz', 5 * 7, 35),
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
