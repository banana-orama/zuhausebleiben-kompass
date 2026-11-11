#!/usr/bin/env python3
"""Fetch round 3: remaining SGB IX sections, SGB XII probe, EAP portal, full reads."""
import re, html, subprocess, pathlib, sys

EVID = pathlib.Path('research/evidence/ohne-pflegegrad-111126')
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'

def curl(url, out=None):
    args = ['curl', '-sL', '--max-time', '45', '-A', UA, url]
    if out:
        args += ['-o', str(out)]
    r = subprocess.run(args, capture_output=True)
    return r.stdout

def to_text(raw_bytes):
    try:
        s = raw_bytes.decode('iso-8859-1')
    except UnicodeDecodeError:
        s = raw_bytes.decode('utf-8', 'replace')
    s = re.sub(r'(?is)<(script|style|head|nav|footer)[^>]*>.*?</\1>', ' ', s)
    s = re.sub(r'(?is)<br\s*/?>', '\n', s)
    s = re.sub(r'(?is)</(p|li|h[1-6]|td|tr)>', '\n', s)
    s = re.sub(r'(?s)<[^>]+>', ' ', s)
    s = html.unescape(s)
    s = re.sub(r'[ \t\xa0]+', ' ', s)
    s = re.sub(r'\n\s*\n+', '\n\n', s)
    return s.strip()

# --- new law sections ---
for n in (8, 14, 42, 47, 49, 118):
    raw = curl(f'https://www.gesetze-im-internet.de/sgb_9_2018/__{n}.html')
    t = to_text(raw)
    (EVID / f'sgb9-{n}.txt').write_text(t, encoding='utf-8')
    m = re.search(r'§\s*' + str(n) + r'\s+[A-ZÄÖÜ][^•]{0,60}', t)
    print(f'sgb9 §{n}: {len(t)} chars | Titel: {m.group(0)[:70] if m else "?"}')
    for needle in ('wohnumfeldverbessernd', 'Wohnungshilfe', 'behinderungsgerecht', 'Wohnung'):
        i = t.find(needle)
        if i >= 0:
            print(f'   [{needle}] …{t[max(0,i-150):i+280]}'.replace(chr(10), ' ¶ '))

# --- SGB XII index probe: any Wohnumfeld/wohnbedarf sections? ---
raw = curl('https://www.gesetze-im-internet.de/sgb_12/index.html')
t = to_text(raw)
(EVID / 'sgb12-index.txt').write_text(t, encoding='utf-8')
print('--- SGB XII index hits ---')
for line in t.split('\n'):
    if re.search(r'Wohn|Hilfe zur Pflege|Leben in der Gemeinschaft|Behinder', line):
        print('  ', line.strip()[:150])

# --- EAP portal ---
raw = curl('https://www.einheitlicher-ansprechpartner.de/EAP/DE/Home/home_node.html')
code_probe = 'Einheitlicher Ansprechpartner' in raw.decode('utf-8', 'replace')
print(f'EAP portal: 200 + title found = {bool(code_probe)}')

# --- print key fetched sections fully ---
for f in ('sgb9-113', 'sgb9-90', 'sgb6-9', 'sgb6-13', 'sgb7-26'):
    p = EVID / f'{f}.txt'
    if p.exists():
        t = p.read_text(encoding='utf-8')
        start = t.find('§ ')
        body = t[start:start + 2600] if start >= 0 else t[:2600]
        print(f'\n===== {f} =====\n{body}')
