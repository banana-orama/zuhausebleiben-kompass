#!/usr/bin/env python3
"""Förder-Prüflauf 01.11.2026: Link-Status ALLER im Live-Content zitierten
offiziellen URLs (kfw.de / gesetze-im-internet.de / bundesgesundheitsministerium.de).
Exit 1, wenn eine URL nicht HTTP 200 liefert."""
import glob
import json
import os
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOM = ('kfw.de', 'gesetze-im-internet.de', 'bundesgesundheitsministerium.de')
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'

urls = {}
for fp in sorted(glob.glob(os.path.join(ROOT, 'content-ready', '*.json'))):
    d = json.load(open(fp, encoding='utf-8'))
    slug = d.get('slug') or os.path.basename(fp)[:-5]
    for s in d.get('sources', []):
        u = s.get('url', '')
        if any(dom in u for dom in DOM):
            urls.setdefault(u, []).append(slug)

from urllib.parse import quote
fails = []
print(f'Prüfe {len(urls)} distinct offizielle URLs (HTTP-Status, folgt Redirects)…\n')
for u, articles in sorted(urls.items()):
    # Umlaut-Pfade (z. B. …/Förderprodukte/…) prozentkodieren, sonst meckert urllib über ASCII
    req_url = quote(u, safe=':/%()=?&-._~')
    req = urllib.request.Request(req_url, headers={'User-Agent': UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            status = r.getcode()
    except Exception as e:
        status = f'ERR {e}'
    ok = status == 200
    if not ok:
        fails.append((u, status))
    print(f'{"PASS" if ok else "FAIL"}  {status:3}  {u}  [{len(articles)} Artikel]')

print(f'\nERGEBNIS: {len(urls) - len(fails)}/{len(urls)} HTTP 200')
if fails:
    print(f'FEHLGESCHLAGEN: {fails}')
    raise SystemExit(1)
