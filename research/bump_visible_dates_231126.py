#!/usr/bin/env python3
"""Prüflauf 23.11.2026 — sichtbare KfW-Abrufdaten (Teil 2 nach fix_vz_and_bump):
16./18. November → 23. November 2026, mit exakten Trefferzahl-Assertions.
"""
import subprocess
import sys

ROOT = '/Users/mac/agentic-business/barrierefrei-leads'
VISIBLE = {
    'bad-umbau-barrierefrei.json': [('16. November 2026', '23. November 2026', 2)],
    'bodengleiche-dusche-altbau.json': [('16. November 2026', '23. November 2026', 2)],
    'wanne-zur-dusche.json': [('16. November 2026', '23. November 2026', 1)],
    'treppenlift-zuschuss.json': [
        ('18. November 2026', '23. November 2026', 3),
        ('Status am 18.11.2026', 'Status am 23.11.2026', 1),
    ],
}
for fname, rules in VISIBLE.items():
    f = f'{ROOT}/content-ready/{fname}'
    raw = open(f, encoding='utf-8').read()
    for old, new, expect in rules:
        n = raw.count(old)
        if n != expect:
            print(f'ABBRUCH: {fname} Treffer {n} != {expect} für {old}')
            sys.exit(1)
        raw = raw.replace(old, new)
        print(f'sichtbar {fname}: {old} x{n} → {new}')
    open(f, 'w', encoding='utf-8').write(raw)
    subprocess.run(['python3', '-m', 'json.tool', f], capture_output=True, check=True)
print('Sichtbare Abrufdaten aktualisiert.')
