#!/usr/bin/env python3
"""Verify ledger-market.json: parse, count, and verbatim-check quotes against raw extracts."""
import json
import re
import sys

BASE = '/Users/mac/agentic-business/barrierefrei-leads/research/evidence/weg-231126'
RAW = BASE + '/raw/market'
REPO_EVID = '/Users/mac/agentic-business/barrierefrei-leads/research/evidence'

TXT_MAP = {
    'checkfox': RAW + '/checkfox.txt',
    'nullbarriere': RAW + '/nullbarriere.txt',
    'wegwissen': RAW + '/wegwissen.txt',
    'herfurtner': RAW + '/herfurtner.txt',
    'lifta': RAW + '/lifta-weg.txt',
    'hiro': RAW + '/hiro-ge.txt',
    'tke-mf': RAW + '/tke-mf.txt',
    'tke-vor': RAW + '/tke-vor.txt',
    'siemer': RAW + '/siemer-weg.txt',
    'tlgurus': RAW + '/tlgurus.txt',
    'vz': REPO_EVID + '/vz-treppenlifte-mietwohnung.txt',
}

SRC_MAP = {
    'checkfox-weg': 'checkfox', 'nullbarriere-weg': 'nullbarriere',
    'wegwissen-bf': 'wegwissen', 'herfurtner-weg': 'herfurtner',
    'lifta-weg': 'lifta', 'hiro-ge': 'hiro', 'tke-mf': 'tke-mf',
    'tke-vor': 'tke-vor', 'siemer-weg': 'siemer', 'vz-treppenlift': 'vz',
}


def norm(s: str) -> str:
    # Whitespace-insensitive verbatim check: collapse all whitespace.
    return re.sub(r'\s+', ' ', s).strip()


def main() -> int:
    data = json.load(open(BASE + '/ledger-market.json', encoding='utf-8'))
    quotes = data['quotes']
    print(f"quotes: {len(quotes)} (target 15-25)")
    ok = True
    if not (15 <= len(quotes) <= 25):
        ok = False
        print('FAIL: quote count out of range')

    # Load all source texts normalized.
    texts = {k: norm(open(v, encoding='utf-8').read()) for k, v in TXT_MAP.items()}

    failures = []
    seen_sources = set()
    for q in quotes:
        seen_sources.add(q['source_id'].rsplit('-', 1)[0])
        frag = q['quote']
        # Each fragment between ellipses must appear verbatim (whitespace-normalized).
        parts = [p for p in norm(frag).split('[...]') if p.strip()]
        src_key = SRC_MAP[q['source_id'].rsplit('-', 1)[0]]
        hay = texts[src_key]
        for part in parts:
            if part.strip() not in hay:
                failures.append((q['source_id'], part[:80]))
    for sid, frag in failures:
        ok = False
        print(f"MISMATCH {sid}: {frag!r}")

    # Schema check.
    required = {'source_id', 'url', 'title', 'quote', 'context_note'}
    for q in quotes:
        missing = required - set(q.keys())
        if missing:
            ok = False
            print(f"SCHEMA FAIL {q.get('source_id')}: missing {missing}")

    print(f"sources covered: {len(seen_sources)} -> {sorted(seen_sources)}")
    print(f"per-source counts: ", end='')
    from collections import Counter
    print(dict(Counter(q['source_id'].rsplit('-', 1)[0] for q in quotes)))
    print('RESULT:', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
