#!/usr/bin/env python3
"""Link-Status aller im Live-Content zitierten offiziellen URLs (23.11.2026).

Sammelt: (a) alle sources[].url aus content-ready/*.json, (b) alle URLs bekannter
offizieller Domains aus dem Roh-JSON. Neu gegenüber 16.11.: nrwbank.de und
stmb.bayern.de (Money-Page-Quellen [6]/[7]).
Prüft per curl (follow redirects). Ein Retry bei 000/4xx/5xx (gesetze-im-internet
Rate-Limit ist transient — Lesson aus 26.10.-Lauf).
"""
import glob
import json
import re
import subprocess
import sys
import time
import urllib.parse

ROOT = '/Users/mac/agentic-business/barrierefrei-leads'
OFFICIAL = ('gesetze-im-internet', 'bundesgesundheitsministerium', 'kfw.de',
            'gkv-spitzenverband', 'nrwbank.de', 'stmb.bayern.de')

urls = set()
for f in glob.glob(f'{ROOT}/content-ready/*.json'):
    raw = open(f, encoding='utf-8').read()
    for m in re.findall(r'https://[^"\\\s]*(?:' + '|'.join(re.escape(d) for d in OFFICIAL) + r')[^"\\\s]*', raw):
        urls.add(m.rstrip('",').rstrip(','))
    try:
        art = json.loads(raw)
        for s in art.get('sources', []):
            u = s.get('url', '')
            if u.startswith('http'):
                urls.add(u.rstrip(','))
    except Exception as e:
        print(f'WARN  {f}: {e}')

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
fails = []
for u in sorted(urls):
    p = urllib.parse.urlsplit(u)
    enc = urllib.parse.urlunsplit((p.scheme, p.netloc, urllib.parse.quote(p.path, safe="/@()%,;~$!&+=:'"), p.query, p.fragment))
    code = ''
    for attempt in (1, 2):
        r = subprocess.run(['curl', '-sS', '-A', UA, '-o', '/dev/null', '-w', '%{http_code}',
                            '--max-time', '25', '-L', enc], capture_output=True, text=True)
        code = r.stdout.strip()
        if code == '200':
            break
        time.sleep(2)
    mark = 'OK ' if code == '200' else 'FAIL'
    if code != '200':
        fails.append(u)
    print(f'{mark} {code}  {u}')

print(f'\nGeprüft: {len(urls)} URLs (distinct), FAIL: {len(fails)}')
if fails:
    for u in fails:
        print(f'  FAIL: {u}')
    sys.exit(1)
print('Alle zitierten offiziellen URLs HTTP 200.')
