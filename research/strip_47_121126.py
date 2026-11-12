#!/usr/bin/env python3
"""Strip § 47 SGB IX raw html -> text (ISO-8859-1)."""
import re, html, pathlib
EVID = pathlib.Path('research/evidence/krankenhaus-121126')
raw = (EVID / 'sgb9-47.html').read_bytes()
head = raw[:2000].decode('utf-8', 'replace')
enc = 'iso-8859-1' if ('charset=iso-8859-1' in head.lower() or 'charset=windows-1252' in head.lower()) else None
try:
    s = raw.decode(enc or 'utf-8')
except UnicodeDecodeError:
    s = raw.decode('iso-8859-1', 'replace')
s = re.sub(r'(?is)<(script|style|head|nav|footer)[^>]*>.*?</\1>', ' ', s)
s = re.sub(r'(?is)<br\s*/?>', '\n', s)
s = re.sub(r'(?is)</(p|li|h[1-6]|td|tr)>', '\n', s)
s = re.sub(r'(?s)<[^>]+>', ' ', s)
s = html.unescape(s)
s = re.sub(r'[ \t\xa0]+', ' ', s)
s = re.sub(r'\n\s*\n+', '\n\n', s)
(EVID / 'sgb9-47.txt').write_text(s.strip(), encoding='utf-8')
print(len(s.strip()), 'chars')
