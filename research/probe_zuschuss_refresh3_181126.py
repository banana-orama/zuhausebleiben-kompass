#!/usr/bin/env python3
# Probe 3 (18.11.2026): KfW-159 Ablauf-Formulierung (article claim: "vor Abschluss von Lieferungs- oder Leistungsverträgen").
import re, html
from pathlib import Path

D = Path(__file__).resolve().parent / 'evidence/zuschuss-refresh-181126'
raw = (D / 'kfw-159.html').read_text(encoding='utf-8', errors='replace')
txt = re.sub(r'<script.*?</script>', ' ', raw, flags=re.S)
txt = re.sub(r'<style.*?</style>', ' ', txt, flags=re.S)
txt = re.sub(r'<[^>]+>', ' ', txt)
txt = html.unescape(txt).replace('\u00ad', '')
txt = re.sub(r'\s+', ' ', txt)

for m in re.finditer(r'Abschluss', txt):
    print('…', txt[max(0, m.start() - 150):m.start() + 120].strip(), '…')
    print('---')
