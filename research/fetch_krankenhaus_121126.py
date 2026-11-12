#!/usr/bin/env python3
"""Fetch round 1: Entlassmanagement-Journey Quellen (Briefing 24).
Gesetzesseiten (SGB V §39 / SGB XI §§18,7a,40,42,47 / SGB IX §32), BMG-Begriffsseite,
GKV-Rahmenvertrag-Entlassmanagement-PDF. ISO-8859-1-Pipeline wie Batch 19.
"""
import re, html, subprocess, pathlib

EVID = pathlib.Path('research/evidence/krankenhaus-121126')
EVID.mkdir(parents=True, exist_ok=True)

URLS = {
    'sgb5-39.html': 'https://www.gesetze-im-internet.de/sgb_5/__39.html',
    'sgb11-18.html': 'https://www.gesetze-im-internet.de/sgb_11/__18.html',
    'sgb11-7a.html': 'https://www.gesetze-im-internet.de/sgb_11/__7a.html',
    'sgb11-40.html': 'https://www.gesetze-im-internet.de/sgb_11/__40.html',
    'sgb11-42.html': 'https://www.gesetze-im-internet.de/sgb_11/__42.html',
    'sgb11-47.html': 'https://www.gesetze-im-internet.de/sgb_11/__47.html',
    'sgb9-32.html': 'https://www.gesetze-im-internet.de/sgb_9_2018/__32.html',
    'bmg-entlassmanagement.html': 'https://www.bundesgesundheitsministerium.de/service/begriffe-von-a-z/e/entlassmanagement',
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


for name, url in URLS.items():
    raw = EVID / ('raw-' + name)
    code = curl(url, raw)
    txt = strip_to_text(raw, EVID / name) if code == '200' else 'HTTP ' + code
    (EVID / name).write_text(txt, encoding='utf-8')
    print(f'{name}: {code} -> {len(txt)} chars')

# GKV-Rahmenvertrag PDF
pdf_raw = EVID / 'rahmenvertrag-entlassmanagement.pdf'
code = curl('https://www.gkv-spitzenverband.de/media/dokumente/krankenversicherung_1/amb_stat_vers/entlassmanagement/13._AendVb_Rahmenvertrag_Entlassmanagement_23.05.2025_Lesefassung_ohne_Anlagen.pdf', pdf_raw)
print('rahmenvertrag pdf:', code, pdf_raw.stat().st_size if code == '200' else 0, 'bytes')
