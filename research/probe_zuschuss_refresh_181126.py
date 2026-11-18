#!/usr/bin/env python3
# Probe-Skript 18.11.2026: Needles für die Verify-Festlegung (SGB XI ISO-8859-1-Pipeline + NRW.BANK-Varianten).
import re, html
from pathlib import Path

D = Path(__file__).resolve().parent / 'evidence/zuschuss-refresh-181126'

def clean_isox(p):
    raw = p.read_bytes().decode('iso-8859-1')
    txt = re.sub(r'<[^>]+>', ' ', raw)
    txt = html.unescape(txt)
    return re.sub(r'\s+', ' ', txt)

def clean_utf(p):
    raw = p.read_text(encoding='utf-8', errors='replace')
    txt = re.sub(r'<script.*?</script>', ' ', raw, flags=re.S)
    txt = re.sub(r'<style.*?</style>', ' ', txt, flags=re.S)
    txt = re.sub(r'<[^>]+>', ' ', txt)
    txt = html.unescape(txt)
    return re.sub(r'\s+', ' ', txt)

sgb = clean_isox(D / 'sgb11-40.html')
for n in ['4 180', '16 720', 'subsidiär', 'wohnumfeldverbessernden Maßnahmen', 'Absatz 4']:
    print('sgb11-40', repr(n), sgb.count(n))

nrw = clean_utf(D / 'nrwbank-barrierefrei.html')
for n in ['220.000', '220 000', '220.000 Euro', 'Tilgungsnachlass', 'Barrierefrei umbauen',
          'Darlehen bis', '100 %', 'bis zu 220', 'Förderdarlehen']:
    print('nrwbank', repr(n), nrw.count(n))
i = nrw.lower().find('darlehen')
print('nrwbank ctx:', nrw[max(0, i - 120):i + 160] if i >= 0 else 'n/a')

stmb = clean_utf(D / 'stmb-bayern-barrierefrei.html')
for n in ['10.000', 'Baudarlehen', 'Barrierefrei', 'leistungsfrei', 'soziale Dringlichkeit']:
    print('stmb', repr(n), stmb.count(n))

k455 = clean_utf(D / 'kfw-455b.html')
for n in ['nicht mehr beantragen', '2027', 'Fördermittel', 'ausgeschöpft']:
    print('kfw455', repr(n), k455.count(n))
j = k455.find('nicht mehr beantragen')
print('kfw455 ctx:', k455[max(0, j - 200):j + 120] if j >= 0 else 'n/a')

k159 = clean_utf(D / 'kfw-159.html')
for n in ['50.000', 'Fachunternehmen', 'Haushaltsmittel', 'vor Abschluss', 'Rechtsanspruch']:
    print('kfw159', repr(n), k159.count(n))
