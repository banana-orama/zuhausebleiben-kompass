#!/usr/bin/env python3
"""Fetch round 2: SGB IX §18 (KH-Begutachtung?), Konsumentenquellen (AOK/TK Entlassmanagement),
Konkurrenz-Artikel pflege-panorama Schlaganfall, Kurzzeitpflege-Verbraucherseite."""
import re, html, subprocess, pathlib

EVID = pathlib.Path('research/evidence/krankenhaus-121126')
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'

URLS = {
    'sgb9-18.html': 'https://www.gesetze-im-internet.de/sgb_9_2018/__18.html',
    'sgb11-39.html': 'https://www.gesetze-im-internet.de/sgb_11/__39.html',
    'aok-entlass.html': 'https://www.aok.de/pk/magazin/kit/hospital-entlassung/nach-dem-krankenhausaufenthalt/',
    'tk-entlass.html': 'https://www.tk.de/techniker-krankke/entlassmanagement-2005412',
    'panorama-schlaganfall.html': 'https://www.pflege-panorama.de/ratgeber/schlaganfall-wohnung-anpassen-2/',
}


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


for name, url in URLS.items():
    raw = EVID / ('raw-' + name)
    code = curl(url, raw)
    if code == '200':
        txt = strip_to_text(raw, EVID / name)
    else:
        txt = 'HTTP ' + code
        (EVID / name).write_text(txt, encoding='utf-8')
    print(f'{name}: {code} -> {len(txt)} chars')
