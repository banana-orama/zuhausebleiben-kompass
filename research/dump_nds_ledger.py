#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dump NDS-Screen-Ledger (26.11.2026) fuer die Content-Autoring-Session:
alle Quellen mit URLs, Evidenzfiles, Zitaten und Needles."""
import json

d = json.load(open('/Users/mac/agentic-business/barrierefrei-leads/research/region-screen-261126-nds-ledger.json'))
for s in d['sources']:
    ev = s['evidence'] if isinstance(s['evidence'], list) else [s['evidence']]
    print(f"### id={s['id']} | {s['label']}")
    print(f"URL: {s['url']}")
    print(f"EVIDENCE: {ev}")
    for i, q in enumerate(s.get('quotes', [])):
        print(f"  Q{i+1}: {q}")
    if s.get('needles'):
        print("  needles:", s.get('needles'))
    if s.get('needles_absent'):
        print("  needles_absent:", s.get('needles_absent'))
    print()
print("WARNINGS:")
for w in d['warnings']:
    print('-', w)
print("UNVERIFIED:")
for u in d['unverified']:
    print('-', u)
print("KEY FINDINGS:")
for k in d['key_findings']:
    print('-', json.dumps(k, ensure_ascii=False))
