#!/usr/bin/env python3
# Probe 4 (18.11.2026): StMB-Sätze für die Verbatim-Fixierung.
import re, html
from pathlib import Path

D = Path(__file__).resolve().parent / 'evidence/zuschuss-refresh-181126'
raw = (D / 'stmb-bayern-barrierefrei.html').read_text(encoding='utf-8', errors='replace')
txt = re.sub(r'<script.*?</script>', ' ', raw, flags=re.S)
txt = re.sub(r'<style.*?</style>', ' ', txt, flags=re.S)
txt = re.sub(r'<[^>]+>', ' ', txt)
txt = html.unescape(txt).replace('\u00ad', '')
txt = re.sub(r'\s+', ' ', txt)
for m in re.finditer(r'10\.000|leistungsfrei', txt):
    print('…', txt[max(0, m.start() - 200):m.start() + 200].strip(), '…')
    print('===')
