#!/usr/bin/env python3
"""Content-Support-Prüfung für treppenlift-finanzierung (Briefing 20):
jeder content-ready-Key muss im gebauten HTML erscheinen; [1]-[20] lösen auf;
Related-Links im Lift-Cluster; Early-CTA-Ziel = treppenlift-zuschuss (Förderung zuerst);
SVG + Kernzahlen; Reform-Datum; kein Partner-Marker. Läuft gegen den LAUNCH-dist
(erst npm run build:launch, dann Skript)."""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
slug = 'treppenlift-finanzierung'
a = json.loads((ROOT / 'content-ready' / f'{slug}.json').read_text(encoding='utf-8'))
html_raw = (ROOT / 'dist' / f'{slug}.html').read_text(encoding='utf-8')
html = re.sub(r'<sup class="cite">.*?</sup>', '', html_raw)

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

# 4. Related-Links im Lift-Cluster (exakt 3 — absolute URLs im LAUNCH-Build)
rel_block = html[html.find('Passend dazu'):html.find('</section>', html.find('Passend dazu'))]
rel_links = re.findall(r'href="([^"]+)"', rel_block)
check('related count 3', len(rel_links) == 3, str(rel_links))
check('related all lift cluster', all('/treppenlift-' in u for u in rel_links), str(rel_links))
check('related not self', all('treppenlift-finanzierung' not in u for u in rel_links), str(rel_links))

# 5. Early-CTA: Förderung zuerst prüfen → treppenlift-zuschuss (specialMap) + kein Partner-Marker
check('early CTA zuschuss', 'href="https://zuhausebleiben-kompass.de/treppenlift-zuschuss.html" data-cta-id="compare_top"' in html_raw)
check('CTA-Label Förderung zuerst', 'Förderung zuerst prüfen' in html_raw)
check('kein Partner-Marker', 'data-partner-placement' not in html_raw)
check('kein awin Tracker', 'awin1.com' not in html_raw)

# 6. SVG eingebettet + Datei existiert
check('svg img tag', 'assets/images/treppenlift-finanzierung-wegweiser.svg' in html_raw)
svg = (ROOT / 'assets' / 'images' / 'treppenlift-finanzierung-wegweiser.svg').read_text(encoding='utf-8')
check('svg xml valid', svg.lstrip().startswith('<svg') and svg.rstrip().endswith('</svg>'))
check('svg KI-Kennzeichnung in caption', 'KI-unterstützt' in html)

# 7. Kernzahlen/Wortlaute im BUILT HTML (Prosa-Schreibweise)
for needle in ['4 180 Euro je Maßnahme', '2 bis 60 Monaten', 'max. 10.000', '11 Teilzahlungen',
               '12 bis 60 Monate', 'individuelle Finanzierungsvereinbarung', 'Im selben Termin',
               '20. November 2026', '2,35 %', '159,17', '166,67', '0,5 Prozent',
               '356d BGB', 'unentgeltlichen Darlehensvertrag', 'innerhalb von 14 Tagen widerrufen',
               'vorzeitig erfüllen', 'millimetergenau', '09.11.2026', 'KI-unterstützt']:
    check(f'built enthält "{needle}"', needle in html)

# 8. Quellen-Anker 1..20
for n in range(1, 21):
    check(f'Anker source-{n}', f'id="source-{n}"' in html_raw)

# 9. Keine Vor-Launch-Prosa / Flip-Phrasen
for bad in ['Entwurf zur ersten Orientierung', 'als Vorschau verfügbar', 'Preview', 'Preview']:
    check(f'kein "{bad}"', bad not in html_raw)

# 10. Förderbeträge bewusst NICHT als eigene Claims (nur Herstelleraussage + Gesetzestext)
#     (keine KfW-Zins-Nennung als eigene Empfehlung)
check('kein eigenes KfW-Zins-Claim', 'KfW-Zinssatz' not in html)

print(f"\n{'ALL PASS' if not FAIL else 'FAILS: ' + str(FAIL)} ({len(FAIL)} fails)")
import sys
sys.exit(1 if FAIL else 0)
