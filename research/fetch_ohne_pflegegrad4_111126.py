#!/usr/bin/env python3
"""Fetch round 4: § 77/§ 99/§ 115/§ 29 SGB IX, § 64e SGB XII, DGUV page."""
import re, html, subprocess, pathlib

EVID = pathlib.Path('research/evidence/ohne-pflegegrad-111126')
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'

def to_text(raw_bytes):
    try:
        s = raw_bytes.decode('iso-8859-1')
    except UnicodeDecodeError:
        s = raw_bytes.decode('utf-8', 'replace')
    s = re.sub(r'(?is)<(script|style|head|nav|footer)[^>]*>.*?</\1>', ' ', s)
    s = re.sub(r'(?is)</(p|li|h[1-6]|td|tr)>', '\n', s)
    s = re.sub(r'(?s)<[^>]+>', ' ', s)
    s = html.unescape(s)
    s = re.sub(r'[ \t\xa0]+', ' ', s)
    s = re.sub(r'\n\s*\n+', '\n\n', s)
    return s.strip()

def fetch(url, name):
    r = subprocess.run(['curl', '-sL', '--max-time', '45', '-A', UA, url], capture_output=True)
    t = to_text(r.stdout)
    (EVID / name).write_text(t, encoding='utf-8')
    start = t.find('§ ')
    body = t[start:start + 2200] if start >= 0 else t[:2200]
    print(f'===== {name} ({len(t)} chars) =====\n{body}\n')
    return t

for n in (77, 99, 115, 29):
    fetch(f'https://www.gesetze-im-internet.de/sgb_9_2018/__{n}.html', f'sgb9-{n}.txt')

t64e = fetch('https://www.gesetze-im-internet.de/sgb_12/__64e.html', 'sgb12-64e.txt')

# DGUV: probe likely pages for wohnumfeldverbessernde Hilfen
for url in ('https://www.dguv.de/de/reha-und-teilhabe/index.jsp',
            'https://www.dguv.de/faq/reha/index.jsp'):
    r = subprocess.run(['curl', '-sL', '-o', '/dev/null', '-w', '%{http_code}', '--max-time', '30', '-A', UA, url],
                       capture_output=True, text=True)
    print('DGUV probe', url, '->', r.stdout.strip())

# EAP raw title check
raw = subprocess.run(['curl', '-sL', '--max-time', '40', '-A', UA,
                      'https://www.einheitlicher-ansprechpartner.de/EAP/DE/Home/home_node.html'],
                     capture_output=True).stdout
head = raw[:1200].decode('utf-8', 'replace')
m = re.search(r'<title>([^<]+)</title>', head)
print('EAP title:', m.group(1) if m else head[:200])
