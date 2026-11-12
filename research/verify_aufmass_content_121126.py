#!/usr/bin/env python3
"""Content-Support-Prüfung für treppenlift-aufmass-termin (Briefing 25):
jeder content-ready-Key muss im gebauten HTML erscheinen; [1]-[8] lösen auf;
Related-Links exakt die 3 Whitelist-Ziele (angebote-vergleichen, unserioese,
schmale-treppe); Early-CTA → treppenlift-firmen-vergleich (specialMap,
„Anbieter für Aufmaß vergleichen“); SVG-Referenz; kein Partner-Marker,
keine Förderbeträge/KfW/Euro-Beträge im HTML. Läuft gegen den LAUNCH-dist."""
from html import unescape
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
slug = 'treppenlift-aufmass-termin'
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


# 1. Metadaten + intro (Array -> je eigene Lead-Absätze)
check('robots index,follow (LAUNCH)', 'index,follow' in html_raw.replace(', ', ','))
check('title', a['title'] in html_raw or a['title'].replace('&', '&amp;') in html_raw)
check('description', norm(a['description'])[:80] in html_raw)
check('h1', a['h1'] in html)
check('intro-0', plain(a['intro'][0])[:80] in html)
check('intro-1', plain(a['intro'][1])[:80] in html)
check('intro als 2 Lead-Absätze (kein Komma-Splice)', html.count('<p class="lead">') == 2 and '.,' not in html_raw.split('<p class="lead">')[1][:400])

# 2. Alle Abschnitte: paragraphs, bullets, table
for i, s in enumerate(a['sections']):
    check(f'sec{i} heading', norm(s['heading']) in html)
    for p in s.get('paragraphs', []):
        check(f'sec{i} paragraph', plain(p)[:90] in html)
    for b in s.get('bullets', []):
        check(f'sec{i} bullet', plain(b)[:90] in html)
    t = s.get('table')
    if t:
        for h in t['headers']:
            check(f'sec{i} table header "{h[:30]}"', norm(h) in html)
        for r in t['rows']:
            for c in r:
                check(f'sec{i} table cell "{plain(c)[:40]}"', plain(c)[:60] in html)

# 3. FAQs + Quellen
for f in a['faqs']:
    check(f'faq "{f["question"][:40]}"', norm(f['question']) in html)
    check(f'faq-answer "{f["question"][:30]}"', plain(f['answer'])[:90] in html)
for i, src in enumerate(a['sources'], 1):
    check(f'source {i} url', src['url'].replace('&', '&amp;') in html or src['url'] in html)
    check(f'source {i} checked_at', src['checked_at'] in html)

# 4. Kernzahlen/Wortlaute im gebauten HTML
for needle in ['Festpreis inklusive Montage', 'Bedenkzeit', '14-tägiges Widerrufsrecht',
               '12 Monate und 14 Tage', 'gleichem Leistungsumfang',
               'Kostenvoranschlag für die Pflegekasse', 'auf den Treppenstufen',
               'zwei bis drei Stunden', 'maximal fünf Stunden', 'innerhalb von 24 Stunden',
               'Unterschreiben Sie nicht vorschnell', '46 von 123']:
    check(f'Kernzahl im HTML: {needle[:40]}', needle in html)

# 5. Related-Links: exakt die 3 Whitelist-Ziele, Reihenfolge config-konform
rel_block = html[html.find('Passend dazu'):html.find('</section>', html.find('Passend dazu'))]
rel_links = re.findall(r'href="([^"]+)"', rel_block)
check('related count 3', len(rel_links) == 3, str(rel_links))
check('related 1 = angebote-vergleichen', 'treppenlift-angebote-vergleichen' in rel_links[0], str(rel_links))
check('related 2 = unserioese-anbieter', 'treppenlift-unserioese-anbieter' in rel_links[1], str(rel_links))
check('related 3 = schmale-treppe', 'treppenlift-schmale-treppe' in rel_links[2], str(rel_links))
check('related not self', all(slug not in u for u in rel_links), str(rel_links))

# 6. Early-CTA: firmen-vergleich (specialMap) + Checklisten-Anker (Abschnitt 8)
check('early CTA firmen-vergleich', '/treppenlift-firmen-vergleich.html' in html and 'Anbieter für Aufmaß vergleichen' in html)
check('checklist anchor -> abschnitt-8', 'href="#abschnitt-8"' in html)
check('data-content-id', f'data-content-id="{slug}"' in html)

# 7. SVG + Bildmetadaten
check('svg referenced', 'treppenlift-aufmass-termin-ablauf.svg' in html)
check('KI-Label im figcaption', 'KI-Illustration' in html)
check('alt-text gesetzt', 'alt="Fünf-Stufen-Flowchart' in html or 'alt="' in html)

# 8. Absenzen im gebauten HTML
for needle, n in [('4.180', 0), ('16.720', 0), ('KfW', 0), ('awin', 0),
                  ('rel="sponsored"', 0), ('data-partner-placement', 0), ('€', 0)]:
    c = html.count(needle)
    check(f'Absenz: 0x "{needle}"', c == n, str(c))

print(f"\n{len(FAIL)} FAILS")
if FAIL:
    for f in FAIL:
        print(' -', f)
    raise SystemExit(1)
print('ALL PASS')
