#!/usr/bin/env python3
"""Förder-Prüflauf 01.11.2026: mappt je Artikel die offiziellen Quellen
(kfw.de / gesetze-im-internet.de / bundesgesundheitsministerium.de) mit checked_at,
damit nur heute tatsächlich neu verifizierte Quellen auf 2026-11-01 gestellt werden."""
import json
import glob
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOM = ('kfw.de', 'gesetze-im-internet.de', 'bundesgesundheitsministerium.de')

rows = []
for fp in sorted(glob.glob(os.path.join(ROOT, 'content-ready', '*.json'))):
    d = json.load(open(fp, encoding='utf-8'))
    slug = d.get('slug') or os.path.basename(fp)[:-5]
    for s in d.get('sources', []):
        u = s.get('url', '')
        if any(dom in u for dom in DOM):
            rows.append((slug, s.get('checked_at', '?'), s.get('title', '')[:58], u))

cur = None
for slug, checked, title, u in sorted(rows):
    if slug != cur:
        print(f'\n== {slug}')
        cur = slug
    print(f'   [{checked}] {title}\n       {u}')

print(f'\nGESAMT: {len(rows)} offizielle Quellenreferenzen in {len(set(r[0] for r in rows))} Artikeln')
