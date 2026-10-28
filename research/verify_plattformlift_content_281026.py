#!/usr/bin/env python3
"""Content-Support-Pruefung fuer treppenlift-plattformlift-rollstuhllift:
jeder content-ready-Key muss im gebauten HTML erscheinen; [1]-[11] muessen aufloesen;
Related-Links im Lift-Cluster; Early-CTA-Ziel = Anbieter fuer Rollstuhllifte vergleichen
(firmen-vergleich); Kernzahlen im gebauten HTML (Prosa-Schreibweise).
Muster: verify_aussen_content_271026.py."""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
slug = 'treppenlift-plattformlift-rollstuhllift'
a = json.loads((ROOT / 'content-ready' / f'{slug}.json').read_text(encoding='utf-8'))
html = (ROOT / 'dist' / f'{slug}.html').read_text(encoding='utf-8')

FAIL = []


def norm(t):
    return re.sub(r'\s+', ' ', t).strip()


def plain(t):
    """Renderer verwandelt [n] in Quellen-Anker-Links — fuer den Textvergleich rausfiltern."""
    return re.sub(r'\s+', ' ', re.sub(r'\[\d+\]', '', t)).strip()


# tag- und citationsichere Volltextansicht (sup-Anker hinterlassen "[n]"-Resttext)
htxt = norm(re.sub(r'\[\d+\]', '', re.sub(r'<[^>]+>', ' ', html)))


def check(label, cond, detail=''):
    print(('PASS ' if cond else 'FAIL ') + label + ('' if cond else f'  {detail}'))
    if not cond:
        FAIL.append(label)


# 1. intro + alle Abschnitte: paragraphs, bullets, table, paragraphs_after
check('intro present', plain(a['intro'])[:80] in htxt)
for i, s in enumerate(a['sections']):
    check(f'sec{i} heading', norm(s['heading']) in html)
    for p in s.get('paragraphs', []):
        check(f'sec{i} paragraph', plain(p)[:90] in htxt)
    for b in s.get('bullets', []):
        check(f'sec{i} bullet', plain(b)[:90] in htxt)
    if 'table' in s:
        for h in s['table']['headers']:
            check(f'sec{i} table header', plain(h) in htxt)
        for row in s['table']['rows']:
            for c in row:
                check(f'sec{i} table cell', plain(c)[:70] in htxt)
    for p in s.get('paragraphs_after', []):
        check(f'sec{i} paragraph_after', plain(p)[:90] in htxt)

# 2. FAQs vollstaendig
for f in a['faqs']:
    check('faq q', norm(f['question']) in html)
    head = re.split(r'\[\d+\]', f['answer'])[0]
    check('faq a', plain(head)[:70] in htxt)

# 3. Quellen 1-11 gerendert + Zitationen aufloesen
for i, s in enumerate(a['sources'], 1):
    check(f'source-{i} anchor', f'id="source-{i}"' in html)
    check(f'source-{i} url', s['url'] in html)
used = set(int(n) for n in re.findall(r'\[(\d+)\]', json.dumps(a['sections']) + json.dumps(a['faqs'])))
check('citations used <= sources', used <= set(range(1, len(a['sources']) + 1)), str(sorted(used)))
check('all 11 sources cited', used == set(range(1, 12)), str(sorted(used)))

# 4. CTA-Ziele: Early-CTA compare_top -> firmen-vergleich ("Anbieter fuer Rollstuhllifte vergleichen")
cta = re.search(r'data-cta-id="compare_top"[^>]*>([^<]+)<', html)
check('early CTA compare_top -> Rollstuhllift-Anbieter', bool(cta) and 'Anbieter für Rollstuhllifte vergleichen' in cta.group(1), cta.group(1) if cta else 'missing')
cta_pos = html.index('data-cta-id="compare_top"')
check('early CTA target = treppenlift-firmen-vergleich', 'treppenlift-firmen-vergleich.html' in html[cta_pos - 300:cta_pos + 80])
check('checklist section exists', 'Checkliste: Plattformlift-Angebot prüfen' in html)
check('checklist anchor target exists', re.search(r'id="abschnitt-\d+"', html) is not None)
# Related-Links: alle im Lift-Cluster, genau 3
seg = html[html.index('class="related">'):html.index('class="related">') + 1200]
rel_slugs = re.findall(r'href="(?:https://zuhausebleiben-kompass\.de/)?([a-z0-9-]+)\.html"', seg)
check('related all lift-cluster', all(s.startswith('treppenlift') for s in rel_slugs), str(rel_slugs))
check('related non-empty', len(rel_slugs) == 3, str(rel_slugs))

# 5. Grafik eingebunden + Label + alt gesetzt
check('image src', 'assets/images/treppenlift-plattformlift-rollstuhllift-weg.svg' in html)
check('KI caption', 'KI-unterstützt erstellte Schema-Grafik' in html)
check('image has alt', 'alt="Entscheidungshilfe Rollstuhllift' in html)

# 6. Keine Verkaufs-/Diagnose-/Bewilligungs-Claims
for bad in ['PREISGARANTIE', 'Testsieger', '100 % sicher', 'Bewilligung garantiert', 'bewilligt wird', 'Lieferung sofort möglich', 'Förderzusage']:
    check(f'no claim "{bad}"', bad not in html)

# 7. Kernzahlen im gebauten HTML (Prosa-Schreibweise mit Punkt-Tausendertrenner)
keys = [
    '7.000 bis 10.000 Euro',
    '11.000 bis 38.000 Euro',
    'ab 11.000 Euro',
    'ab 19.000 Euro',
    '12.500 bis 16.000 Euro',
    '18.000–26.000',
    '30.000–38.000',
    '1,55 für die zweite',
    '2,05 für die dritte',
    '90 bis 110 cm',
    '120 bis 140 cm',
    '800×1000 mm',
    '620×750',
    '225 bis 300 kg',
    '300 kg',
    '250 kg',
    '0,1 m/s',
    '0,15 m/s',
    '50 bis 200 €',
    '99 bis 150 kg',
    '200 bis 450 Euro',
    '4.180 Euro pro Person',
]
for k in keys:
    check(f'key number "{k}"', k in htxt)

# 8. Noindex-Status im Launch-Build (index,follow erwartet) — hier Launch-Dist pruefen
robots = re.search(r'name="robots" content="([^"]+)"', html)
check('robots meta present', bool(robots), 'missing')
if robots:
    check('robots index,follow (launch)', robots.group(1).replace(' ', '') == 'index,follow', robots.group(1))

print()
if FAIL:
    print(f'{len(FAIL)} FAIL:')
    for f in FAIL:
        print('  -', f)
    sys.exit(1)
print('ALL PASS')
