#!/usr/bin/env python3
"""Content-Support-Prüfung für treppenlift-foerderung-ohne-pflegegrad (Briefing 23):
jeder content-ready-Key muss im gebauten HTML erscheinen; [1]-[28] lösen auf;
Related-Links im Lift-Cluster (Cross-Ziele vorne: zuschuss, finanzierung, gebraucht-oder-neu);
Early-CTA-Ziel = treppenlift-zuschuss (specialMap); SVG; Reform-Status-Wortlaute;
kein Partner-Marker, keine Pflegekassen-Beträge im HTML. Läuft gegen den LAUNCH-dist."""
from html import unescape
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
slug = 'treppenlift-foerderung-ohne-pflegegrad'
a = json.loads((ROOT / 'content-ready' / f'{slug}.json').read_text(encoding='utf-8'))
html_raw = (ROOT / 'dist' / f'{slug}.html').read_text(encoding='utf-8')
html = unescape(re.sub(r'<sup class="cite">.*?</sup>', '', html_raw))

FAIL = []


def norm(t):
    return re.sub(r'\s+', ' ', t).strip()


def plain(t):
    return re.sub(r'\s+', ' ', re.sub(r'\[\d+\]', '', t)).strip()


def check(label, cond, detail=''):
    print(('PASS ' if cond else 'FAIL ') + label + ('' if cond else f'  {detail}'))
    if not cond:
        FAIL.append(label)


# 1. Metadaten + intro
check('robots index,follow (LAUNCH)', 'index,follow' in html_raw.replace(', ', ','))
check('title', a['title'] in html_raw or a['title'].replace('&', '&amp;') in html_raw)
check('description', norm(a['description'])[:80] in html_raw)
check('h1', a['h1'] in html)
check('intro-0', plain(a['intro'][0])[:80] in html)
check('intro-1', plain(a['intro'][1])[:80] in html)

# 2. Alle Abschnitte: paragraphs, bullets
for i, s in enumerate(a['sections']):
    check(f'sec{i} heading', norm(s['heading']) in html)
    for p in s.get('paragraphs', []):
        check(f'sec{i} paragraph', plain(p)[:90] in html)
    for b in s.get('bullets', []):
        check(f'sec{i} bullet', plain(b)[:90] in html)

# 3. FAQs + Quellen
for f in a['faqs']:
    check(f'faq "{f["question"][:40]}"', norm(f['question']) in html)
    check(f'faq-answer "{f["question"][:30]}"', plain(f['answer'])[:90] in html)
for i, src in enumerate(a['sources'], 1):
    check(f'source {i} url', src['url'].replace('&', '&amp;') in html or src['url'] in html)
    check(f'source {i} checked_at', src['checked_at'] in html)

# 4. Related-Links im Lift-Cluster (exakt 3, Cross-Ziele vorne)
rel_block = html[html.find('Passend dazu'):html.find('</section>', html.find('Passend dazu'))]
rel_links = re.findall(r'href="([^"]+)"', rel_block)
check('related count 3', len(rel_links) == 3, str(rel_links))
check('related order: zuschuss zuerst', rel_links and 'treppenlift-zuschuss' in rel_links[0], str(rel_links))
check('related contains finanzierung', any('treppenlift-finanzierung' in u for u in rel_links), str(rel_links))
check('related contains gebraucht-oder-neu', any('treppenlift-gebraucht-oder-neu' in u for u in rel_links), str(rel_links))
check('related all lift cluster', all('treppenlift' in u for u in rel_links), str(rel_links))
check('related not self', all(slug not in u for u in rel_links), str(rel_links))

# 5. Early-CTA: Pflegekasse & KfW prüfen → treppenlift-zuschuss (specialMap) + kein Partner-Marker
check('early CTA zuschuss',
      'href="https://zuhausebleiben-kompass.de/treppenlift-zuschuss.html" data-cta-id="compare_top"' in html_raw)
check('CTA-Label "Pflegekasse & KfW prüfen"', 'Pflegekasse &amp; KfW prüfen' in html_raw or 'Pflegekasse & KfW prüfen' in html_raw)
check('kein Partner-Marker', 'data-partner-placement' not in html_raw)
check('kein awin Tracker', 'awin1.com' not in html_raw)
check('kein rel=sponsored', 'rel="sponsored' not in html_raw)

# 6. SVG eingebettet + Datei existiert
check('svg img tag', 'assets/images/treppenlift-foerderung-ohne-pflegegrad-wegweiser.svg' in html_raw)
svg = (ROOT / 'assets' / 'images' / 'treppenlift-foerderung-ohne-pflegegrad-wegweiser.svg').read_text(encoding='utf-8')
check('svg xml valid', svg.lstrip().startswith('<svg') and svg.rstrip().endswith('</svg>'))
check('svg im dist kopiert', (ROOT / 'dist' / 'assets' / 'images' / 'treppenlift-foerderung-ohne-pflegegrad-wegweiser.svg').exists())
check('svg KI-Kennzeichnung im caption', 'KI-Illustration' in html)

# 7. Kernzahlen/Wortlaute im BUILT HTML (citation-normalisiert)
for needle in ['Leistungen für Wohnraum', '85 Prozent der jährlichen Bezugsgröße',
               '60 Prozent', '150 Prozent der jährlichen Bezugsgröße',
               'Vorvorjahres', 'innerhalb von zwei Wochen',
               'Dauer von sechs Monaten', '15 bis unter 30 Gesamtpunkten',
               'Drucksache 21/8869', 'Bestandsschutz', 'nicht beschlossen',
               'Treppensteigen', 'vor der Haus- bzw. vor der Wohnungstür',
               'Gesamtplanverfahren', 'Persönliches Budget', 'Internationalen Klassifikation',
               '11.11.2026', 'KI-unterstützt', 'Tobias Batke']:
    check(f'built enthält "{needle[:44]}"', needle in html)

# 8. Quellen-Anker 1..28
for n in range(1, 29):
    check(f'Anker source-{n}', f'id="source-{n}"' in html_raw)

# 9. Keine Vor-Launch-Prosa / Flip-Phrasen
for bad in ['Entwurf zur ersten Orientierung', 'als Vorschau verfügbar', 'Preview']:
    check(f'kein "{bad}"', bad not in html_raw)

# 10. Keine Pflegekassen-Beträge im HTML (bewusst nur Verweis auf zuschuss-Ratgeber)
check('HTML 0 × "4.180"', '4.180' not in html_raw, str(html_raw.count('4.180')))
check('HTML 0 × "16.720"', '16.720' not in html_raw)

print(f"\n{len(FAIL)} FAILS")
import sys
sys.exit(1 if FAIL else 0)
