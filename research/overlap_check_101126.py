#!/usr/bin/env python3
"""Overlap-Check: Wo deckt der Bestand das 'unseriöse Anbieter'-Topic schon ab?"""
import json, os

os.chdir('/Users/mac/agentic-business/barrierefrei-leads/content-ready')
FILES = [
    'treppenlift-angebote-vergleichen.json',
    'treppenlift-firmen-vergleich.json',
    'treppenlift-mieten.json',
    'treppenlift-finanzierung.json',
    'treppenlift-mietwohnung.json',
    'treppenlift-gebraucht-oder-neu.json',
]
KEYWORDS = ['unseri', 'Abzocke', 'windig', 'Warnsignal', 'Mobilae', 'Fangpr',
            'Kaltakquise', 'Akquise', 'Telefonverkauf', 'Untergeschoben',
            'Prämie', 'Vorauszahlung', 'Vertreter', 'Klingel', 'Druck mach',
            'nachsetzen', 'Notlage ausnutzen']

def walk(o, path=''):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, path + '.' + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, path + f'[{i}]')
    elif isinstance(o, str):
        yield path, o

for f in FILES:
    d = json.load(open(f))
    print('==', f)
    seen = set()
    for kw in KEYWORDS:
        for p, s in walk(d):
            if kw.lower() in s.lower() and (kw, p) not in seen:
                seen.add((kw, p))
                snippet = ' '.join(s.split())[:200]
                print(f'  {kw} @ {p}: {snippet}')
