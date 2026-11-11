#!/usr/bin/env python3
"""Fetch round 2: corrected law URLs + DRV carrier pages."""
import re, html, subprocess, pathlib

EVID = pathlib.Path('research/evidence/ohne-pflegegrad-111126')

URLS = {
    'sgb9-55.html': 'https://www.gesetze-im-internet.de/sgb_9_2018/__55.html',
    'sgb9-6.html': 'https://www.gesetze-im-internet.de/sgb_9_2018/__6.html',
    'sgb9-26.html': 'https://www.gesetze-im-internet.de/sgb_9_2018/__26.html',
    'sgb9-90.html': 'https://www.gesetze-im-internet.de/sgb_9_2018/__90.html',
    'sgb9-113.html': 'https://www.gesetze-im-internet.de/sgb_9_2018/__113.html',
    'sgb9-136.html': 'https://www.gesetze-im-internet.de/sgb_9_2018/__136.html',
    'sgb9-139.html': 'https://www.gesetze-im-internet.de/sgb_9_2018/__139.html',
    'sgb9-140.html': 'https://www.gesetze-im-internet.de/sgb_9_2018/__140.html',
    'sgb6-9.html': 'https://www.gesetze-im-internet.de/sgb_6/__9.html',
    'sgb6-13.html': 'https://www.gesetze-im-internet.de/sgb_6/__13.html',
    'sgb6-15.html': 'https://www.gesetze-im-internet.de/sgb_6/__15.html',
    'drv-berufliche-reha.html': 'https://deutsche-rentenversicherung.de/DRV/DE/Reha/Berufliche-Reha/berufliche-reha.html',
    'drv-medizinische-reha.html': 'https://deutsche-rentenversicherung.de/DRV/DE/Reha/Medizinische-Reha/medizinische-reha.html',
    'dguv-reha.html': 'https://www.dguv.de/de/reha-und-teilhabe/reha-leistungen/leistungen-zur-teilhabe-am-leben-in-der-gemeinschaft/index.jsp',
}

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'

def curl(url, out_raw):
    r = subprocess.run(['curl', '-sL', '--max-time', '45', '-A', UA, url, '-o', str(out_raw), '-w', '%{http_code}'],
                       capture_output=True, text=True)
    return r.stdout.strip()

def strip_to_text(raw_path, txt_path):
    raw = open(raw_path, 'rb').read()
    enc = None
    head = raw[:2000].decode('utf-8', 'replace')
    if 'charset=iso-8859-1' in head.lower() or 'charset=windows-1252' in head.lower():
        enc = 'iso-8859-1'
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
    open(txt_path, 'w', encoding='utf-8').write(s.strip())
    return s.strip()

def grep_ctx(s, needle, width=300, max_hits=5):
    hits, low, start = [], s.lower(), 0
    while len(hits) < max_hits:
        i = low.find(needle, start)
        if i < 0:
            break
        hits.append(s[max(0, i - width // 3):i + width].replace('\n', ' ¶ '))
        start = i + 1
    return hits

for fname, url in URLS.items():
    raw = EVID / f'raw-{fname}'
    code = curl(url, raw)
    if code != '200':
        print(f'### {fname}: HTTP {code}')
        continue
    s = strip_to_text(raw, EVID / fname.replace('.html', '.txt'))
    print(f'### {fname}: 200, {len(s)} chars')
    for needle in ('wohnumfeldverbessernd', 'behinderungsgerecht'):
        for h in grep_ctx(s, needle):
            print(f'   [{needle[:12]}] …', h[:420])
