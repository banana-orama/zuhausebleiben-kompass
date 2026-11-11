#!/usr/bin/env python3
"""Fetch round 5: remaining anchors + carrier-system pages."""
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

def fetch(url, name, show=1900):
    r = subprocess.run(['curl', '-sL', '--max-time', '45', '-A', UA, url], capture_output=True)
    t = to_text(r.stdout)
    (EVID / name).write_text(t, encoding='utf-8')
    start = t.find('§ ')
    body = t[start:start + show] if start >= 0 else t[:show]
    print(f'===== {name} ({len(t)} chars) =====\n{body}\n')

fetch('https://www.gesetze-im-internet.de/sgb_12/__61.html', 'sgb12-61.txt', 1400)
fetch('https://www.gesetze-im-internet.de/sgb_12/__2.html', 'sgb12-2.txt', 1200)
fetch('https://www.gesetze-im-internet.de/indhvo/__2.html', 'indhvo-2.txt', 1400)
fetch('https://www.gesetze-im-internet.de/sgb_9_2018/__117.html', 'sgb9-117.txt', 1600)
fetch('https://www.gesetze-im-internet.de/sgb_9_2018/__32.html', 'sgb9-32.txt', 1200)
fetch('https://www.gesetze-im-internet.de/sgb_14/__6.html', 'sgb14-6.txt', 1600)
fetch('https://www.gesetze-im-internet.de/sgb_9_2018/__135.html', 'sgb9-135.txt', 900)

# status probes
for url in ('https://www.teilhabeberatung.de/',
            'https://www.dguv.de/de/service/faq/reha/index.jsp'):
    r = subprocess.run(['curl', '-sL', '-o', '/dev/null', '-w', '%{http_code}', '--max-time', '30', '-A', UA, url],
                       capture_output=True, text=True)
    print('probe', url, '->', r.stdout.strip())

# find DGUV Reha page via their search? use homepage nav
raw = subprocess.run(['curl', '-sL', '--max-time', '30', '-A', UA, 'https://www.dguv.de/'], capture_output=True).stdout
hits = set(re.findall(rb'href="([^"]*(?:reha|teilhabe)[^"]*)"', raw, re.I))
print('DGUV nav reha-links:', [h.decode('utf-8', 'replace')[:90] for h in list(hits)[:8]])
