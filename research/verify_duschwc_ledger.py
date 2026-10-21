#!/usr/bin/env python3
"""Verify every quote in dusch-wc-ledger.json appears verbatim in its evidence file."""
import json, html, re, sys
from pathlib import Path

repo = Path('/Users/mac/agentic-business/barrierefrei-leads')
ledger = json.loads((repo / 'research/dusch-wc-ledger.json').read_text())

def norm(s):
    s = html.unescape(s)
    s = s.replace('\xa0', ' ').replace('\u00ad', '')
    s = re.sub(r'\s+', ' ', s)
    return s.strip().lower()

total, ok = 0, 0
for src in ledger['sources']:
    body = norm((repo / 'research/evidence' / src['evidence']).read_text(encoding='utf-8'))
    for q in src['quotes']:
        total += 1
        hit = norm(q['text']) in body
        ok += hit
        if not hit:
            print('FAIL', src['id'], '|', q['text'][:100])
print(f'{ok}/{total} quotes verified verbatim')
if ok != total:
    sys.exit(1)
print('LEDGER OK')
