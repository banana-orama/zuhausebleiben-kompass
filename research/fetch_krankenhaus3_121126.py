#!/usr/bin/env python3
"""Fetch round 3: Konsumentenquellen (gesund.bund.de, VZ, AOK, VdK) + Rahmenvertrag 14. ÄndVb
(19.11.2025, aktueller als die am Vortag gegriffene 13. ÄndVb) + Strip § 18c SGB XI."""
import re, html, subprocess, pathlib

EVID = pathlib.Path('research/evidence/krankenhaus-121126')
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'

URLS = {
    'gesundbund-entlassung.html': 'https://gesund.bund.de/entlassung-aus-dem-krankenhaus',
    'vz-entlassmanagement.html': 'https://verbraucherzentrale.de/wissen/gesundheit-pflege/aerztinnen-und-kliniken/krankenhaus-was-kommt-danach-entlassmanagement-unterstuetzt-101021',
    'aok-entlassung.html': 'https://www.aok.de/pk/leistungen/medizinische-behandlung/entlassung-krankenhaus',
    'vdk-entlassmanagement.html': 'https://vdk.de/aktuelles/tipp/entlassmanagement-hilflos-nach-der-operation',
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

# § 18c nachstrippen (roh lag schon vor)
strip_to_text(EVID / 'raw-sgb11-18c.html', EVID / 'sgb11-18c.html')
print('sgb11-18c.html gestrippt:', (EVID / 'sgb11-18c.html').stat().st_size, 'bytes')

# Rahmenvertrag 14. ÄndVb (19.11.2025)
code = curl('https://gkv-spitzenverband.de/media/dokumente/krankenversicherung_1/amb_stat_vers/entlassmanagement/14._AendVb_Rahmenvertrag_Entlassmanagement_19.11.2025_Lesefassung_ohne_Anlagen.pdf',
            EVID / 'rahmenvertrag-14aendvb.pdf')
print('rahmenvertrag-14aendvb pdf:', code, (EVID / 'rahmenvertrag-14aendvb.pdf').stat().st_size if code == '200' else 0)
