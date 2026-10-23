#!/usr/bin/env python3
"""Badumbau-Scan: HTML -> Text-Extrakte (.txt) + Kategorie-Grep auf aroundhome-home."""
import re, html, pathlib

ev = pathlib.Path(__file__).resolve().parent / 'evidence' / 'partner-scan-badumbau-231026'

FILES = [
    'badumbauheld-partner.html',
    'seniovo-partner.html',
    'aroundhome-triplea.html',
    'aroundhome-triplea-start.html',
    'awin-aroundhome-68536.html',
    'hienergy-aroundhome-awin.html',
    'aroundhome-home.html',
    'aroundhome-badezimmer.html',
    'ewerle-leadportale.html',
]

def to_text(h):
    h = re.sub(r'<script[\s\S]*?</script>|<style[\s\S]*?</style>|<!--[\s\S]*?-->', ' ', h)
    t = html.unescape(re.sub(r'<[^>]+>', ' ', h))
    return re.sub(r'[ \t\r\f\v]+', ' ', t)

for f in FILES:
    p = ev / f
    if not p.exists():
        print('SKIP', f)
        continue
    t = to_text(p.read_text(errors='ignore'))
    out = ev / (f[:-5] + '.txt')
    out.write_text(t, encoding='utf-8')
    print(f'{f} -> {out.name}: {len(t)} chars')

# Kategorie-Check auf der Aroundhome-Startseite
home = (ev / 'aroundhome-home.txt').read_text(errors='ignore')
print('\n===== Kategorie-Grep aroundhome.de Startseite =====')
for kw in ['Bad', 'bad', 'Sanierung', 'Dusche', 'barrierefrei', 'Badsanierung', 'bad-sanierung']:
    hits = list(re.finditer(r'\b' + kw, home))
    if hits:
        m = hits[0]
        s = max(0, m.start() - 100)
        print(f'[{kw}] x{len(hits)} …{re.sub(chr(92)+"s+", " ", home[s:m.end()+150])}…')
# Links auf Bad-Kategorien in RAW HTML
raw = (ev / 'aroundhome-home.html').read_text(errors='ignore')
print('\n===== Links mit bad/sanierung =====')
for m in list(re.finditer(r'href="([^"]*(?:bad|sanier)[^"]*)"', raw, re.I))[:12]:
    print(' ', m.group(1))
