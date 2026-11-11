#!/usr/bin/env python3
"""Dump article JSON schema of briefing 22 + check renderer/test registration points."""
import json, re, pathlib

art = json.load(open('content-ready/treppenlift-unserioese-anbieter.json'))
print('TOP KEYS:', list(art.keys()))
for k, v in art.items():
    if isinstance(v, str):
        print(f'  {k}: str({len(v)}) = {v[:80]!r}')
    elif isinstance(v, list):
        print(f'  {k}: list[{len(v)}]')
        if v and isinstance(v[0], dict):
            print(f'    item keys: {list(v[0].keys())}')
            print(f'    item0: {json.dumps(v[0], ensure_ascii=False)[:300]}')
    elif isinstance(v, dict):
        print(f'  {k}: dict keys={list(v.keys())}')

print()
print('--- section key variants across article ---')
seen = set()
for s in art.get('sections', []):
    seen.update(s.keys())
print(sorted(seen))

print()
print('--- renderer/test registration points ---')
for f in ('scripts/article-renderer.mjs', 'scripts/llms-txt.py', 'tests/test_articles.py',
          'tests/verify_checklists_build.py', 'tests/test_partner_links.py', 'data/cross-links.json'):
    p = pathlib.Path(f)
    if not p.exists():
        # try alternate locations
        for alt in pathlib.Path('.').glob(f'**/{p.name}'):
            if 'node_modules' not in str(alt) and 'dist' not in str(alt):
                p = alt
                break
    print(f'== {p}')
    txt = p.read_text(encoding='utf-8', errors='replace')
    for pat in ('unserioese', 'angehoerige', '33', '≥32', '>= 32', 'specialMap'):
        hits = [m.start() for m in re.finditer(re.escape(pat), txt)]
        if hits and pat in ('unserioese', 'angehoerige'):
            i = hits[-1]
            print(f'  [{pat}] x{len(hits)} last@{i}: …{txt[max(0,i-120):i+160]}…'.replace(chr(10), ' '))
        elif hits:
            print(f'  [{pat}] x{len(hits)}')
