#!/usr/bin/env python3
"""Diagnose der 6 FAILs: Vergleich 19.10-Evidence vs. 26.10-Evidence."""
import html as htmllib
import re

EV = '/Users/mac/agentic-business/barrierefrei-leads/research/evidence'


def load_text(fname, charset, strip_scripts=True):
    raw = open(f'{EV}/{fname}', 'rb').read()
    txt = raw.decode(charset, errors='replace')
    txt = htmllib.unescape(txt)
    if strip_scripts:
        txt = re.sub(r'<script[^>]*>.*?</script>', ' ', txt, flags=re.S | re.I)
    txt = re.sub(r'<style[^>]*>.*?</style>', ' ', txt, flags=re.S | re.I)
    txt = re.sub(r'<[^>]+>', ' ', txt)
    txt = txt.replace('\xa0', ' ').replace('\u202f', ' ').replace('\u00ad', '')
    txt = re.sub(r'\s+', ' ', txt)
    return txt


def find_ctx(text, needle, before=150, after=150):
    p = text.find(needle)
    if p < 0:
        return None
    return text[max(0, p - before):p + len(needle) + after]


print('### 1) § 40: "subsid" in 19.10- und 26.10-Fetch')
for f in ('foerder-191026-sgb40.html', 'foerder-261026-sgb40.html'):
    try:
        t = load_text(f, 'iso-8859-1')
        idx = [m.start() for m in re.finditer(r'subsid', t)]
        print(f'{f}: hits={len(idx)}')
        for i in idx[:3]:
            print('   …', t[max(0, i - 120):i + 160], '…')
    except FileNotFoundError:
        print(f'{f}: nicht vorhanden')

print()
print('### 2) § 40 Abs. 4 Satz 1 vollständig (26.10)')
t26 = load_text('foerder-261026-sgb40.html', 'iso-8859-1')
ctx = find_ctx(t26, 'individuellen Wohnumfeldes', 200, 400)
print('   …', ctx, '…')

print()
print('### 3) KfW 159 mit Soft-Hyphen-Strip: Vorbehalt/Rechtsanspruch/Fachunternehmen')
for f in ('foerder-191026-kfw159.html', 'foerder-261026-kfw159.html'):
    try:
        t = load_text(f, 'utf-8')
        for n in ('Haushaltsmittel', 'Rechtsanspruch', 'Fachunternehmen', 'Kombination der Förderungen', 'gleiche Maßnahme'):
            c = find_ctx(t, n, 100, 200)
            print(f'{f} | {n}: {"GEFUNDEN" if c else "fehlt"}')
            if c:
                print('     …', c, '…')
    except FileNotFoundError:
        print(f'{f}: nicht vorhanden')

print()
print('### 4) KfW 159 RAW (ohne Script-Strip): Kombination-FAQ in JSON-LD?')
for f in ('foerder-261026-kfw159.html',):
    raw = open(f'{EV}/{f}', 'rb').read().decode('utf-8', errors='replace')
    raw = htmllib.unescape(raw).replace('\u00ad', '')
    for n in ('Kombination der Förderungen', 'gleiche Maßnahme'):
        p = raw.find(n)
        print(f'{f} | RAW {n}:', 'GEFUNDEN' if p >= 0 else 'fehlt')
        if p >= 0:
            print('     …', re.sub(r'\s+', ' ', raw[max(0, p - 200):p + 260]), '…')

print()
print('### 5) anteilig in § 40 (26.10)')
c = find_ctx(t26, 'anteilig', 150, 150)
print('   …', c, '…')
