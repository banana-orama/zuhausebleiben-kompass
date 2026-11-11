#!/usr/bin/env python3
"""Inspect existing coverage around candidate briefing-23 topics."""
import json, re

def load(slug):
    return json.load(open(f'content-ready/{slug}.json'))

z = load('treppenlift-zuschuss')
print('=== treppenlift-zuschuss ===')
print('title:', z.get('title'))
print('section heads:')
for s in z.get('sections', []):
    print('  -', s.get('heading'))
text = json.dumps(z, ensure_ascii=False).lower()
for kw in ['pflegekasse', 'kfw', 'sozialamt', 'jobcenter', 'rentenversicherung', 'eingliederungshilfe',
           'schwerbehinder', 'pflegegrad', 'sgb ix', 'sgb vi', 'unfall', 'agentur f', 'em-pension',
           'reha', 'bedürftig', 'einkommen']:
    n = text.count(kw)
    print(f'  {kw!r}: {n}')

print()
print('=== mietwohnung: umzug/554-context ===')
m = load('treppenlift-mietwohnung')
mt = json.dumps(m, ensure_ascii=False).lower()
for kw in ['umzug', '554', '20 weg', 'brandschutz', 'wohnumfeld']:
    print(f'  {kw!r}: {mt.count(kw)}')

print()
print('=== bad-umbau-barrierefrei: mietwohnung-context ===')
b = load('bad-umbau-barrierefrei')
bt = json.dumps(b, ensure_ascii=False).lower()
print('  mietwohnung:', bt.count('mietwohnung'), '| vermieter:', bt.count('vermieter'), '| 554:', bt.count('554'))
print('  heads:', [s.get('heading') for s in b.get('sections', [])][:12])

print()
print('=== badumbau-angebote-vergleichen miet/vermieter ===')
a = load('badumbau-angebote-vergleichen')
at = json.dumps(a, ensure_ascii=False).lower()
print('  mietwohnung:', at.count('mietwohnung'), '| vermieter:', at.count('vermieter'))
