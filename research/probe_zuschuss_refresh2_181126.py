#!/usr/bin/env python3
# Probe 2 (18.11.2026): Soft-Hyphen-Normalisierung für KfW/NRW.BANK/StMB-Needles.
import re, html
from pathlib import Path

D = Path(__file__).resolve().parent / 'evidence/zuschuss-refresh-181126'

def clean_utf(p):
    raw = p.read_text(encoding='utf-8', errors='replace')
    txt = re.sub(r'<script.*?</script>', ' ', raw, flags=re.S)
    txt = re.sub(r'<style.*?</style>', ' ', txt, flags=re.S)
    txt = re.sub(r'<[^>]+>', ' ', txt)
    txt = html.unescape(txt)
    txt = txt.replace('\u00ad', '')  # Soft-Hyphen entfernen (KfW nutzt U+00AD in Worten)
    return re.sub(r'\s+', ' ', txt)

k159 = clean_utf(D / 'kfw-159.html')
for n in ['Fachunternehmen', 'Haushaltsmittel', 'vor Abschluss', 'Rechtsanspruch',
          'Finanzierungspartner', 'Eigenleistungen', '50.000 Euro', 'Nachfinanzierung']:
    print('kfw159', repr(n), k159.count(n))
j = k159.find('Haushaltsmittel')
print('kfw159 haushalt ctx:', k159[max(0, j - 120):j + 160] if j >= 0 else 'n/a')
j = k159.find('Fachunternehmen')
print('kfw159 fach ctx:', k159[max(0, j - 100):j + 180] if j >= 0 else 'n/a')

nrw = clean_utf(D / 'nrwbank-barrierefrei.html')
for n in ['220.000', 'Modernisierung', 'Einkommensgrenzen', 'Barrierefrei umbauen']:
    print('nrwbank', repr(n), nrw.count(n))
j = nrw.find('220.000')
print('nrwbank 220 ctx:', nrw[max(0, j - 160):j + 200] if j >= 0 else 'n/a')

stmb = clean_utf(D / 'stmb-bayern-barrierefrei.html')
for n in ['10.000 Euro', 'Baudarlehen bis', 'leistungsfrei']:
    print('stmb', repr(n), stmb.count(n))
