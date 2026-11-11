#!/usr/bin/env python3
"""Quick verbatim check of ohne-pflegegrad ledger (runs before article exists)."""
import json, re, sys

LEDGER = json.load(open('research/ohne-pflegegrad-111126-ledger.json'))

def norm(t):
    t = t.replace('\u00ad', '')
    t = re.sub(r'\s+', ' ', t)
    t = re.sub(r'\s+([.,;:!?])', r'\1', t)
    return t.strip()

fail = 0
for src in LEDGER['sources']:
    ev = norm(open(src['evidence'], encoding='utf-8').read())
    for q in src['quotes']:
        ok = norm(q) in ev
        if not ok:
            fail += 1
            print(f"FAIL [{src['n']}] {q[:90]}…")
print(f"{sum(len(s['quotes']) for s in LEDGER['sources'])} quotes checked, {fail} fails")
sys.exit(1 if fail else 0)
