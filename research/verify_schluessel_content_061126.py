#!/usr/bin/env python3
"""Content-Support-Prüfung für hausnotruf-schluesselhinterlegung (Briefing 19):
jeder content-ready-Key muss im gebauten HTML erscheinen; [1]-[8] lösen auf;
Related-Links im Care-Cluster; Early-CTA-Ziel = hausnotruf-kosten-anbieter-vergleich;
SVG + Kernzahlen. Läuft gegen den LAUNCH-dist (erst npm run build:launch, dann Skript)."""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
slug = 'hausnotruf-schluesselhinterlegung'
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

# 2. Alle Abschnitte: paragraphs, bullets, table
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

# 4. Related-Links im Care-Cluster (exakt 3, alle care-Präfixe — absolute URLs im LAUNCH-Build)
CARE_PARTS = ('/hausnotruf-', '/pflegegrad', '/hilfsmittel', '/rollator', '/verhinderungspflege', '/tuerbreiten', '/beleuchtung', '/wohnumfeld')
rel_block = html[html.find('Passend dazu'):html.find('</section>', html.find('Passend dazu'))]
rel_links = re.findall(r'href="([^"]+)"', rel_block)
check('related count 3', len(rel_links) == 3, str(rel_links))
check('related all care cluster', all(any(cp in u for cp in CARE_PARTS) for u in rel_links), str(rel_links))
check('related Cross-Ziel 1 = kosten-vergleich', 'hausnotruf-kosten-anbieter-vergleich.html' in rel_links[0] if rel_links else False, str(rel_links))
check('related Cross-Ziel 2 = sturzerkennung', 'hausnotruf-sturzerkennung-oder-knopf.html' in rel_links[1] if len(rel_links) > 1 else False, str(rel_links))

# 5. Early-CTA auf hausnotruf-kosten-anbieter-vergleich (specialMap) + kein Partner-Marker
check('early CTA kosten-vergleich', 'href="https://zuhausebleiben-kompass.de/hausnotruf-kosten-anbieter-vergleich.html" data-cta-id="compare_top"' in html_raw)
check('CTA-Label', 'Kosten &amp; Anbieter vergleichen' in html_raw or 'Kosten & Anbieter vergleichen' in html_raw)
check('kein Partner-Marker', 'data-partner-placement' not in html_raw)
check('kein awin Tracker', 'awin1.com' not in html_raw)

# 6. SVG eingebettet + Datei existiert
check('svg img tag', 'assets/images/hausnotruf-schluessel-entscheidung.svg' in html_raw)
svg = (ROOT / 'assets' / 'images' / 'hausnotruf-schluessel-entscheidung.svg').read_text(encoding='utf-8')
check('svg xml valid', svg.lstrip().startswith('<svg') and svg.rstrip().endswith('</svg>'))
check('svg KI-Kennzeichnung in caption', 'KI-unterstützt' in html)

# 7. Kernzahlen/Wortlaute im BUILT HTML
for needle in ['2.957,21', 'fast 800 Euro', 'etwa 15 Euro', '30 bis 80 Euro',
               '35 bis 100 Euro', '27 und 40 Euro', '§ 536a BGB', 'kein Generalschlüssel',
               'AG Hildburghausen', 'AG Berlin-Mitte', '2 K 2103/23.GI',
               'nicht von der Pflegekasse bezuschusst', 'kostenpflichtig und müssen privat finanziert werden',
               'in demselben Gespräch', 'schneller am Einsatzort', '06.11.2026']:
    check(f'built enthält "{needle}"', needle in html)

# 8. Quellen-Anker 1..8
for n in range(1, 9):
    check(f'Anker source-{n}', f'id="source-{n}"' in html_raw)

# 9. Keine Vor-Launch-Prosa / Flip-Phrasen
for bad in ['Entwurf zur ersten Orientierung', 'als Vorschau verfügbar', 'Vorschau', 'Preview']:
    check(f'kein "{bad}"', bad not in html_raw)

print(f"\n{'ALL PASS' if not FAIL else 'FAILS: ' + str(FAIL)} ({len(FAIL)} fails)")
import sys
sys.exit(1 if FAIL else 0)
