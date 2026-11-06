#!/usr/bin/env python3
"""Strip fetched HTML pages to readable text + print Schlüssel-relevant passages."""
import re, html, sys, os

D = os.path.dirname(os.path.abspath(__file__))
for name in ['easierlife', 'pflegehelfer24', 'pflegeeinstieg', 'malteser', 'vz-hausnotruf']:
    p = os.path.join(D, f'{name}.html')
    if not os.path.exists(p):
        print(f'== {name}: MISSING'); continue
    raw = open(p, encoding='utf-8', errors='replace').read()
    raw = re.sub(r'<(script|style|noscript)[^>]*>.*?</\1>', ' ', raw, flags=re.S | re.I)
    txt = re.sub(r'<[^>]+>', '\n', raw)
    txt = html.unescape(txt)
    txt = re.sub(r'[ \t\xa0]+', ' ', txt)
    txt = re.sub(r'\n\s*\n+', '\n', txt)
    out = os.path.join(D, f'{name}.txt')
    open(out, 'w', encoding='utf-8').write(txt)
    lines = [l.strip() for l in txt.split('\n') if l.strip()]
    print(f'== {name}: {len(lines)} lines -> {name}.txt')
    hits = [l for l in lines if re.search(r'[Ss]chlüssel|Notöffnung|Türöffnung|[Tt]resor', l)]
    for h in hits[:14]:
        print('   •', h[:230])
    print()
