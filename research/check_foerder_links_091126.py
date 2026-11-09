#!/usr/bin/env python3
"""Link-Status aller im Live-Content zitierten offiziellen URLs (09.11.2026).
Sammelt kfw.de / gesetze-im-internet / bundesgesundheitsministerium / gkv-spitzenverband
URLs aus content-ready/*.json, kodiert Umlaut-Pfade, prüft per curl (follow redirects).
"""
import glob
import re
import subprocess
import sys
import urllib.parse

ROOT = '/Users/mac/agentic-business/barrierefrei-leads'
pat = re.compile(r'https://[^"]*(?:gesetze-im-internet|bundesgesundheitsministerium|kfw\.de|gkv-spitzenverband)[^"]*')
urls = set()
for f in glob.glob(f'{ROOT}/content-ready/*.json'):
    raw = open(f, encoding='utf-8').read()
    for m in pat.findall(raw):
        urls.add(m.rstrip('",').rstrip(','))

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
fails = []
for u in sorted(urls):
    p = urllib.parse.urlsplit(u)
    enc = urllib.parse.urlunsplit((p.scheme, p.netloc, urllib.parse.quote(p.path, safe="/@()%,;~$!&+=:'"), p.query, p.fragment))
    r = subprocess.run(['curl', '-sS', '-A', UA, '-o', '/dev/null', '-w', '%{http_code}', '--max-time', '25', '-L', enc],
                       capture_output=True, text=True)
    code = r.stdout.strip()
    mark = 'OK ' if code == '200' else 'FAIL'
    if code != '200':
        fails.append(u)
    print(f'{mark} {code}  {u}')

print(f'\nGeprüft: {len(urls)} URLs, FAIL: {len(fails)}')
if fails:
    sys.exit(1)
