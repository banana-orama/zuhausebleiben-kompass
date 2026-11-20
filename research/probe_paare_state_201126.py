#!/usr/bin/env python3
"""Probe: state of the stranded paare article (source vs live built page)."""
import json, re, html as htmllib

# 1) live page robots + key content vs local JSON
raw = open('/tmp/live-paare.html', encoding='utf-8', errors='replace').read()
m = re.search(r'<title>(.*?)</title>', raw, re.S)
print('LIVE title:', (m.group(1).strip() if m else 'NONE')[:100])
m = re.search(r'name="robots"\s+content="([^"]+)"', raw) or re.search(r'content="([^"]+)"\s+name="robots"', raw)
print('LIVE robots:', m.group(1) if m else 'NO-ROBOTS-META')
print('LIVE svg ref:', 'hausnotruf-paare-konstellationen' in raw)
m = re.search(r'geprüft[^<]{0,40}|\d{2}\.\d{2}\.\d{4}', raw)
print('LIVE first date-ish:', m.group(0) if m else None)
print('LIVE partner markers:', raw.count('data-partner-placement'), '| sponsored rel:', raw.count('rel="sponsored"'))

# 2) source JSON: full section inventory + status meaning
d = json.load(open('content-ready/hausnotruf-fuere-paare.json')) if False else json.load(open('content-ready/hausnotruf-fuer-paare.json'))
print('\nSRC status:', d['status'], '| slug:', d['slug'], '| faqs:', len(d.get('faqs', [])))
print('SRC intro keys:', sorted(d.get('intro', {}).keys()) if isinstance(d.get('intro'), dict) else type(d.get('intro')))
secs = d.get('sections', [])
print('SRC sections:', len(secs))
for s in secs:
    keys = [k for k in s.keys() if k not in ('heading',)]
    print('  *', str(s.get('heading', ''))[:60], '->', keys)
# every content key inventory (for the keys-in-HTML gate)
def walk(o, path=''):
    if isinstance(o, dict):
        for k, v in o.items():
            walk(v, f'{path}.{k}')
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, f'{path}[{i}]')
    elif isinstance(o, str) and len(o) > 25:
        print(f'  STR {path} = {o[:60]!r}')
print('\nSRC source count:', len(d['sources']))
for s in d['sources']:
    print('  -', s.get('url', '')[:80])

# 3) how does generate.mjs treat status?
gen = open('generate.mjs', encoding='utf-8').read()
for m in re.finditer(r'.*status.*', gen):
    line = m.group(0).strip()
    if any(w in line for w in ('reviewed', 'preview', 'noindex', 'release', 'robots')):
        print('GEN status-line:', line[:160])
print('\nGEN launch/index flags:', [l.strip()[:150] for l in gen.splitlines() if '--index' in l or 'indexable' in l.lower()][:6])
