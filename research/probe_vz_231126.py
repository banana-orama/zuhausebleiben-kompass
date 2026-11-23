#!/usr/bin/env python3
"""Extrahiert den [7]-Zitat-Kontext aus hausnotruf-angehoerige-einrichten.json
und listet alle VZ-Kandidaten-URLs mit Status.
"""
import json
import re
import subprocess
import urllib.parse

a = json.load(open('content-ready/hausnotruf-angehoerige-einrichten.json'))
blob = json.dumps(a, ensure_ascii=False)
print('=== [7]-Verweise im Fließtext ===')
for m in re.finditer(r'\[7\]', blob):
    print('…', blob[max(0, m.start() - 400):m.start() + 30].replace('\\n', ' '), '\n')
s7 = a['sources'][6]
print('SRC[7]:', json.dumps(s7, ensure_ascii=False)[:400])

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
print('\n=== Kandidaten ===')
CAND = [
    'https://www.verbraucherzentrale.de/selbstbestimmt-die-onlinevorsorgedokumente-der-verbraucherzentralen-76270',
    'https://www.verbraucherzentrale.de/wissen/geld-versicherungen/altersvorsorge/ Vorsorgevollmacht',
]
for u in CAND[:1]:
    p = urllib.parse.urlsplit(u)
    enc = urllib.parse.urlunsplit(p[:5])
    r = subprocess.run(['curl', '-sS', '-A', UA, '-o', '/dev/null', '-w', '%{http_code}',
                        '--max-time', '20', '-L', enc], capture_output=True, text=True)
    print(r.stdout.strip(), u)
