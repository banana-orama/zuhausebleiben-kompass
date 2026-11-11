#!/usr/bin/env python3
"""Fetch round 6: § 104 SGB IX, § 61a SGB XII, DGUV Teilhabe-Seite, EUTB-Portal, SGB XIV Index."""
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

def fetch(url, name, show=2000):
    r = subprocess.run(['curl', '-sL', '--max-time', '45', '-A', UA, url], capture_output=True)
    t = to_text(r.stdout)
    (EVID / name).write_text(t, encoding='utf-8')
    print(f'===== {name} ({len(t)} chars) =====')
    print(t[:show])
    print()
    return t

fetch('https://www.gesetze-im-internet.de/sgb_9_2018/__104.html', 'sgb9-104.txt', 1600)
fetch('https://www.gesetze-im-internet.de/sgb_12/__61a.html', 'sgb12-61a.txt', 1600)
fetch('https://www.dguv.de/de/reha-und-teilhabe/reha_leistung/teilhabe/index.jsp', 'dguv-teilhabe.txt', 2400)
fetch('https://www.teilhabeberatung.de/', 'eutb-portal.txt', 1600)

# SGB XIV index: find Teilhabe sections
r = subprocess.run(['curl', '-sL', '--max-time', '30', '-A', UA, 'https://www.gesetze-im-internet.de/sgb_14/index.html'],
                   capture_output=True)
t = to_text(r.stdout)
(EVID / 'sgb14-index.txt').write_text(t, encoding='utf-8')
print('--- SGB XIV index: Teilhabe/Heilbehandlung ---')
for line in t.split('\n'):
    if re.search(r'Teilhabe|Heilbehandlung', line):
        print('  ', line.strip()[:160])
