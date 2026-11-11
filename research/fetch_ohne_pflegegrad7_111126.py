#!/usr/bin/env python3
"""Fetch round 7: UTF-8-safe refetch of carrier pages + § 66 SGB XIV."""
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
            if 'Ã' in s[:3000] or 'â' in s[:3000]:  # mojibake marker -> actually ISO
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

def fetch(url, name, show=1200, needle=None):
    r = subprocess.run(['curl', '-sL', '--max-time', '45', '-A', UA, url], capture_output=True)
    t = to_text(r.stdout)
    (EVID / name).write_text(t, encoding='utf-8')
    print(f'===== {name} ({len(t)} chars) =====')
    if needle:
        low = t.lower()
        i = low.find(needle.lower())
        if i >= 0:
            print('HIT:', t[max(0, i - 200):i + 600].replace(chr(10), ' ¶ '))
        else:
            print('needle miss:', needle)
            print(t[:600])
    else:
        print(t[:show])
    print()

fetch('https://deutsche-rentenversicherung.de/DRV/DE/Reha/Berufliche-Reha/berufliche-reha.html',
      'drv-berufliche-reha.txt', needle='Wohnungshilfen')
fetch('https://deutsche-rentenversicherung.de/DRV/DE/Reha/Medizinische-Reha/medizinische-reha.html',
      'drv-medizinische-reha.txt', show=900)
fetch('https://www.teilhabeberatung.de/', 'eutb-portal.txt', show=700)
fetch('https://www.gesetze-im-internet.de/sgb_14/__66.html', 'sgb14-66.txt', show=1500)

fetch('https://www.dguv.de/de/reha_leistung/teilhabe/index.jsp', 'dguv-teilhabe.txt', needle='Sozialen Teilhabe')
