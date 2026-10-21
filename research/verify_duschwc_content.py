#!/usr/bin/env python3
"""Key-content gate for hilfsmittel-dusch-wc-uebernahme: every supported content key must appear in built HTML."""
from pathlib import Path
import json, re

root = Path('/Users/mac/agentic-business/barrierefrei-leads')
a = json.loads((root / 'content-ready/hilfsmittel-dusch-wc-uebernahme.json').read_text())
h = (root / 'dist/hilfsmittel-dusch-wc-uebernahme.html').read_text()

def cit(s):
    s = re.sub(r'<sup class="cite">.*?</sup>', '', s, flags=re.S)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = re.sub(r'\[\d+\]', '', s)
    return re.sub(r'\s+', ' ', s)

plain = cit(h)
fails = []

def check(label, needle):
    np = re.sub(r'\[\d+\]', '', needle)
    np = re.sub(r'\s+', ' ', np).strip()
    if not np:
        return
    if np not in plain:
        fails.append((label, np[:90]))
        print('FAIL', label, '|', np[:90])

check('intro', a['intro'])
for i, s in enumerate(a['sections']):
    check(f'section-{i+1}-heading', s['heading'])
    for p in (s.get('paragraphs') or []):
        check('p', p)
    for b in (s.get('bullets') or []):
        check('bullet', b)
    if 'table' in s:
        for hdr in s['table']['headers']:
            check('th', hdr)
        for row in s['table']['rows']:
            for c in row:
                check('td', c)
    for p in (s.get('paragraphs_after') or []):
        check('p_after', p)
for f in a['faqs']:
    check('faq-q', f['question'])
    check('faq-a', f['answer'])

# load-bearing figures and distinctions must appear as text (not only in the image)
for needle in ['4.180', '16.720', '33.40.05', '10 Prozent', 'mindestens 5', 'höchstens 10 Euro',
               'Ohnhändigkeit', 'Gebrauchsgegenstände', 'binnen eines Monats', '28.09.2026', 'subsidiär']:
    present = needle in plain
    if not present:
        fails.append(('figure', needle))
    print(('OK  ' if present else 'FAIL'), 'figure', needle)

# related links + CTA must share the care cluster (no off-topic funnel)
rel_match = re.search(r'<section class="related">(.*?)</section>', h, re.S)
assert rel_match, 'related section missing'
rel_targets = re.findall(r'href="([^"]+)"', rel_match.group(1))
for t in rel_targets:
    slug = t.rsplit('/', 1)[-1].replace('.html', '')
    ok = re.match(r'^(hausnotruf|pflegegrad|hilfsmittel|rollator|verhinderungspflege|tuerbreiten|beleuchtung|treppenlift-(zuschuss|kosten))', slug)
    print('related:', slug, 'OK' if ok else 'OFF-CLUSTER')
    if not ok:
        fails.append(('related', slug))
cta = re.search(r'href="([^"]+)"[^>]*data-cta-id="compare_top"', h)
assert cta, 'early CTA missing'
cta_target = cta.group(1)
print('early CTA target:', cta_target)
assert 'hilfsmittel-pflegekasse-uebernahme' in cta_target, 'early CTA not the Hilfsmittel guide'

n_cites = len(re.findall(r'\[\d+\]', h))
print('cite links in html:', n_cites)
print('FAILS:', len(fails))
if fails:
    raise SystemExit(1)
print('KEY-CONTENT OK — alle Absätze, Bullets, Tabellenzellen, FAQs, Kennzahlen und Cluster-Ziele im HTML')
