#!/usr/bin/env python3
"""Mobiler-Hausnotruf-Artikel 04.11.2026: prüft jede Ledger-Quote wörtlich gegen die
gespeicherte Evidence-Datei (whitespace-normalisiert) und die Kern-Arithmetik.
Exit 1 bei fehlender Assertion. Muster: verify_wohnumfeld_021126.py."""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
EV = ROOT / 'research' / 'evidence'
LEDGER = ROOT / 'research' / 'hausnotruf-mobil-041126-ledger.json'

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
print('== Arithmetik/Konsistenz')
checks = [
    ('Kap-Logik Zuzahlung: 10 % ab 250 € = 25 € (§ 40 Abs. 3-Höchstwert)', 250 * 0.10, 25),
    ('beWo 50 Std. ≈ 2,1 Tage -> innerhalb panorama "1 bis 7 Tage"', round(50 / 24, 1), 2.1),
    ('Malteser 72 Std. = 3 Tage Stromausfall-Brücke (Herstellerangabe)', 72 / 24, 3),
    ('kompass intern: Basis 27 + Aufpreis 10 = 37 -> >= Untergrenze Gesamtkosten 35', 27 + 10 >= 35, True),
    ('kompass intern: Basis 27 + Aufpreis 25 = 52 -> <= Obergrenze Gesamtkosten 70', 27 + 25 <= 70, True),
    ('Überlappung Gesamt-Spannen panorama 30–50 / kompass 35–70: 35..50', (35 <= 50 and 35 <= 70), True),
    ('Wochenfristen § 40 Abs. 7: 3 Wochen ≈ 21 Tage', 3 * 7, 21),
    ('Wochenfristen § 40 Abs. 7: 5 Wochen ≈ 35 Tage', 5 * 7, 35),
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
