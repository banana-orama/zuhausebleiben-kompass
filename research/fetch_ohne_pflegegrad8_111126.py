#!/usr/bin/env python3
"""Fetch round 8: § 2 SGB IX, BMG-PNOG-PM, Drucksache-21/8869 PDF probe."""
import re, html, subprocess, pathlib

EVID = pathlib.Path('research/evidence/ohne-pflegegrad-111126')
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'

def to_text(raw_bytes):
    head = raw_bytes[:4000].decode('utf-8', 'replace').lower()
    if 'charset=utf-8' in head:
        s = raw_bytes.decode('utf-8', 'replace')
    else:
        try:
            s = raw_bytes.decode('utf-8')
            if 'Ã' in s[:3000] or 'â' in s[:3000]:
                s = raw_bytes.decode('iso-8859-1', 'replace')
        except UnicodeDecodeError:
            s = raw_bytes.decode('iso-8859-1', 'replace')
    s = re.sub(r'(?is)<(script|style|head|nav|footer)[^>]*>.*?</\1>', ' ', s)
    s = re.sub(r'(?is)</(p|li|h[1-6]|td|tr)>', '\n', s)
    s = re.sub(r'(?s)<[^>]+>', ' ', s)
    s = html.unescape(s)
    s = re.sub(r'[ \t\xa0]+', ' ', s)
    s = re.sub(r'\n\s*\n+', '\n\n', s)
    return s.strip()

def fetch(url, name, needle=None, show=900):
    r = subprocess.run(['curl', '-sL', '--max-time', '60', '-A', UA, url], capture_output=True)
    raw = r.stdout
    if name.endswith('.pdf'):
        out = EVID / name
        out.write_bytes(raw)
        print(f'{name}: {len(raw)} bytes saved ({out})')
        return None
    t = to_text(raw)
    (EVID / name).write_text(t, encoding='utf-8')
    print(f'===== {name} ({len(t)} chars) =====')
    if needle:
        low = t.lower()
        i = low.find(needle.lower())
        print('HIT:' if i >= 0 else 'MISS:', (t[max(0, i - 250):i + 900] if i >= 0 else t[:500]).replace(chr(10), ' ¶ '))
    else:
        print(t[:show])
    print()

fetch('https://www.gesetze-im-internet.de/sgb_9_2018/__2.html', 'sgb9-2.txt')
fetch('https://www.bundesgesundheitsministerium.de/presse/pressemitteilungen/kabinett-beschliesst-pflegeneuordnungsgesetz',
      'bmg-pnog-pm.txt', needle='Begutachtungssystematik')
fetch('https://dserver.bundestag.de/btd/21/088/2108869.pdf', 'drucksache-21-8869.pdf')
