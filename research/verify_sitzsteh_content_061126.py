#!/usr/bin/env python3
"""Content-Support-Prüfung für treppenlift-sitzlift-oder-stehlift:
jeder content-ready-Key muss im gebauten HTML erscheinen; [1]-[8] lösen auf;
Related-Links im Lift-Cluster; Early-CTA-Ziel = firmen-vergleich; SVG + Kernzahlen.
Läuft gegen den LAUNCH-dist (erst npm run build:launch, dann dieses Skript)."""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
slug = 'treppenlift-sitzlift-oder-stehlift'
a = json.loads((ROOT / 'content-ready' / f'{slug}.json').read_text(encoding='utf-8'))
html_raw = (ROOT / 'dist' / f'{slug}.html').read_text(encoding='utf-8')
html = re.sub(r'<sup class="cite">.*?</sup>', '', html_raw)

FAIL = []


def norm(t):
    return re.sub(r'\s+', ' ', t).strip()


def plain(t):
    return re.sub(r'\s+', ' ', re.sub(r'\[\d\]', '', t)).strip()


def check(label, cond, detail=''):
    print(('PASS ' if cond else 'FAIL ') + label + ('' if cond else f'  {detail}'))
    if not cond:
        FAIL.append(label)


# 1. Metadaten + intro
check('robots index,follow (LAUNCH)', 'name="robots" content="index, follow"' in html_raw or 'index,follow' in html_raw.replace(', ', ','), html_raw[html_raw.find('robots'):html_raw.find('robots') + 60] if 'robots' in html_raw else 'no robots meta')
check('title', a['title'] in html_raw)
check('description', norm(a['description'])[:80] in html_raw)
check('h1', a['h1'] in html)
check('intro', plain(a['intro'][0])[:80] in html)

# 2. Alle Abschnitte: paragraphs, bullets, table, paragraphs_after
for i, s in enumerate(a['sections']):
    check(f'sec{i} heading', norm(s['heading']) in html)
    for p in s.get('paragraphs', []):
        check(f'sec{i} paragraph', plain(p)[:90] in html)
    for b in s.get('bullets', []):
        check(f'sec{i} bullet', plain(b)[:90] in html)
    if 'table' in s:
        for h in s['table']['headers']:
            check(f'sec{i} table header', plain(h) in html)
        for row in s['table']['rows']:
            for c in row:
                check(f'sec{i} table cell', plain(c)[:70] in html)
    for p in s.get('paragraphs_after', []):
        check(f'sec{i} paragraphs_after', plain(p)[:90] in html)

# 3. FAQs + Quellen
for f in a['faqs']:
    check(f'faq "{f["question"][:40]}"', norm(f['question']) in html)
    check(f'faq-answer "{f["question"][:30]}"', plain(f['answer'])[:90] in html)
for i, src in enumerate(a['sources'], 1):
    check(f'source {i} url', src['url'].replace('&', '&amp;') in html or src['url'] in html)
    check(f'source {i} checked_at', src['checked_at'] in html)

# 4. Related-Links im Lift-Cluster (exakt 3, alle treppenlift*)
rel_block = html[html.find('Passend dazu'):html.find('</section>', html.find('Passend dazu'))]
rel_links = re.findall(r'href="([^"]+)"', rel_block)
check('related count 3', len(rel_links) == 3, str(rel_links))
check('related all lift cluster', all('/treppenlift-' in u for u in rel_links), str(rel_links))

# 5. Early-CTA auf firmen-vergleich (specialMap) + kein Partner-Marker
check('early CTA firmen-vergleich', 'href="https://zuhausebleiben-kompass.de/treppenlift-firmen-vergleich.html" data-cta-id="compare_top"' in html_raw)
check('CTA-Label Sitz- und Stehlifte', 'Anbieter für Sitz- und Stehlifte vergleichen' in html_raw)
check('kein Partner-Marker', 'data-partner-placement' not in html_raw)

# 6. SVG eingebettet + Datei existiert
check('svg img tag', 'assets/images/treppenlift-sitzsteh-entscheidung.svg' in html_raw)
svg = (ROOT / 'assets' / 'images' / 'treppenlift-sitzsteh-entscheidung.svg').read_text(encoding='utf-8')
check('svg xml valid', svg.lstrip().startswith('<svg') and svg.rstrip().endswith('</svg>'))
check('svg KI-Kennzeichnung in caption', 'KI-unterstützt' in html)

# 7. Kernzahlen/Wortlaute im BUILT HTML (Prosa-Schreibweise)
for needle in ['Mindestbreite von 80 cm', 'Mindestens 55 cm', 'etwa 4.000 Euro',
               '12 Monate und 14 Tage', 'gängigste Art', 'ohne Gewähr',
               'skriptgeprüfte Absenz', 'kein unabhängiger Produkttest']:
    check(f'built enthält "{needle}"', needle in html)

# 8. Absatz-Integrität: alle 8 [n]-Zitate lösen auf Quellen-Anker
for n in range(1, 9):
    check(f'Anker source-{n}', f'id="source-{n}"' in html_raw)

# 9. Keine Vor-Launch-Prosa, keine Editorial-Flip-Phrasen
for bad in ['Entwurf zur ersten Orientierung', 'als Vorschau verfügbar', 'Vorschau', 'Preview']:
    check(f'kein "{bad}"', bad not in html_raw)

print(f"\n{'ALL PASS' if not FAIL else 'FAILS: ' + str(FAIL)} ({len(FAIL)} fails)")
import sys
sys.exit(1 if FAIL else 0)
