#!/usr/bin/env python3
"""Content-Support-Prüfung für treppenlift-unserioese-anbieter (Briefing 22):
jeder content-ready-Key muss im gebauten HTML erscheinen; [1]-[9] lösen auf;
Related-Links im Lift-Cluster (Cross-Ziele vorne: angebote-vergleichen, mieten, kosten);
Early-CTA-Ziel = treppenlift-angebote-vergleichen (specialMap); SVG + Kernzahlen;
kein Partner-Marker, keine Förderbeträge im HTML. Läuft gegen den LAUNCH-dist."""
from html import unescape
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
slug = 'treppenlift-unserioese-anbieter'
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
check('related order: angebote-vergleichen zuerst',
      rel_links and 'treppenlift-angebote-vergleichen' in rel_links[0], str(rel_links))
check('related contains mieten', any('treppenlift-mieten' in u for u in rel_links), str(rel_links))
check('related contains kosten', any('treppenlift-kosten' in u for u in rel_links), str(rel_links))
check('related all lift cluster', all('treppenlift' in u for u in rel_links), str(rel_links))
check('related not self', all(slug not in u for u in rel_links), str(rel_links))

# 5. Early-CTA: Angebote sauber vergleichen → treppenlift-angebote-vergleichen (specialMap) + kein Partner-Marker
check('early CTA angebote-vergleichen',
      'href="https://zuhausebleiben-kompass.de/treppenlift-angebote-vergleichen.html" data-cta-id="compare_top"' in html_raw)
check('CTA-Label "Angebote sauber vergleichen"', 'Angebote sauber vergleichen' in html_raw)
check('kein Partner-Marker', 'data-partner-placement' not in html_raw)
check('kein awin Tracker', 'awin1.com' not in html_raw)
check('kein rel=sponsored', 'rel="sponsored' not in html_raw)

# 6. SVG eingebettet + Datei existiert
check('svg img tag', 'assets/images/treppenlift-unserioese-anbieter-warntafel.svg' in html_raw)
svg = (ROOT / 'assets' / 'images' / 'treppenlift-unserioese-anbieter-warntafel.svg').read_text(encoding='utf-8')
check('svg xml valid', svg.lstrip().startswith('<svg') and svg.rstrip().endswith('</svg>'))
check('svg im dist kopiert', (ROOT / 'dist' / 'assets' / 'images' / 'treppenlift-unserioese-anbieter-warntafel.svg').exists())
check('svg KI-Kennzeichnung in caption', 'KI-unterstützt' in html)

# 7. Kernzahlen/Wortlaute im BUILT HTML (Prosa-Schreibweise, citation-normalisiert)
for needle in ['125 ausgefüllte Umfragebögen', '12 Monate und 14 Tage', 'I-13 UKl 17/26',
               '8. Oktober 2026', '18 Vertragsklauseln', 'in Höhe von 65 % der Bruttoauftragssumme',
               'in Höhe von 25 % der Bruttoauftragssumme', 'Maßanfertigung und Lieferung sofort',
               'Keinesfalls sollten Sie sich zu einem Vertragsabschluss drängen lassen',
               'geistige und körperliche Beeinträchtigungen, das Alter',
               'ohne dessen vorherige ausdrückliche Einwilligung', 'höchste Vorsicht geboten',
               'zahlen Sie erst, wenn der Lift eingebaut und funktionstüchtig ist',
               'An keiner Stelle war erkennbar', 'PractiComfort', 'zwei Jahre lang',
               '10. Dezember 2020', 'Verbandsklageregister', 'Oberlandesgericht Hamm',
               '10.11.2026', 'KI-unterstützt']:
    check(f'built enthält "{needle}"', needle in html)

# 8. Quellen-Anker 1..9
for n in range(1, 10):
    check(f'Anker source-{n}', f'id="source-{n}"' in html_raw)

# 9. Keine Vor-Launch-Prosa / Flip-Phrasen
for bad in ['Entwurf zur ersten Orientierung', 'als Vorschau verfügbar', 'Preview']:
    check(f'kein "{bad}"', bad not in html_raw)

# 10. Keine Förderbeträge im HTML (bewusst nur Verweis auf zuschuss-Ratgeber)
check('HTML 0 × "4.180"', '4.180' not in html_raw, str(html_raw.count('4.180')))
check('HTML 0 × "16.720"', '16.720' not in html_raw)

print(f"\n{len(FAIL)} FAILS")
import sys
sys.exit(1 if FAIL else 0)
