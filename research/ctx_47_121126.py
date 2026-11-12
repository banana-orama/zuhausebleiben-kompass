#!/usr/bin/env python3
"""§ 47 SGB IX Volltext + Artikel-Passage zum Vergleich."""
import re, html, pathlib, json
EVID = pathlib.Path('research/evidence/krankenhaus-121126')
raw = (EVID / 'probe-__47.html').read_bytes()
s = raw.decode('iso-8859-1', 'replace')
s = re.sub(r'(?is)<(script|style|head)[^>]*>.*?</\1>', ' ', s)
s = re.sub(r'(?s)<[^>]+>', ' ', s)
s = html.unescape(s)
s = re.sub(r'\s+', ' ', s)
i = s.find('§ 47')
print(s[i:i + 900])
print('---ARTIKEL---')
art = json.loads(pathlib.Path('content-ready/treppenlift-foerderung-ohne-pflegegrad.json').read_text(encoding='utf-8'))
t = json.dumps(art, ensure_ascii=False)
j = t.find('47 SGB')
print(t[max(0, j - 350):j + 200])
