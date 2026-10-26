#!/usr/bin/env python3
"""Content-Support-Prüfung für treppenlift-steuerlich-absetzen:
jeder content-ready-Key muss im gebauten HTML erscheinen; [1]-[4] müssen auflösen;
Related-Links im Lift-Cluster; Early-CTA-Ziel = Förderung prüfen."""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
slug = 'treppenlift-steuerlich-absetzen'
a = json.loads((ROOT / 'content-ready' / f'{slug}.json').read_text(encoding='utf-8'))
html = (ROOT / 'dist' / f'{slug}.html').read_text(encoding='utf-8')

FAIL = []


def norm(t):
    return re.sub(r'\s+', ' ', t).strip()


def plain(t):
    """Renderer verwandelt [n] in Quellen-Anker-Links — für den Textvergleich rausfiltern."""
    return re.sub(r'\s+', ' ', re.sub(r'\[\d\]', '', t)).strip()


def check(label, cond, detail=''):
    print(('PASS ' if cond else 'FAIL ') + label + ('' if cond else f'  {detail}'))
    if not cond:
        FAIL.append(label)


# 1. intro + alle Abschnitte: paragraphs, bullets, table, paragraphs_after
check('intro present', plain(a['intro'])[:80] in html)
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
        check(f'sec{i} paragraph_after', plain(p)[:90] in html)

# 2. FAQs vollständig
for f in a['faqs']:
    check('faq q', norm(f['question']) in html)
    head = re.split(r'\[\d\]', f['answer'])[0]
    check('faq a', plain(head)[:70] in html)

# 3. Quellen 1-4 gerendert + Zitationen [1]-[4] auflösen
for i, s in enumerate(a['sources'], 1):
    check(f'source-{i} anchor', f'id="source-{i}"' in html)
    check(f'source-{i} url', s['url'] in html)
used = set(int(n) for n in re.findall(r'\[(\d)\]', json.dumps(a['sections']) + json.dumps(a['faqs'])))
check('citations used ⊆ sources', used <= set(range(1, len(a['sources']) + 1)), str(sorted(used)))
check('all 4 sources cited', used == set(range(1, 5)), str(sorted(used)))

# 4. CTA-Ziele: Early-CTA compare_top → treppenlift-zuschuss ("Förderung prüfen")
cta = re.search(r'data-cta-id="compare_top"[^>]*>([^<]+)<', html)
check('early CTA compare_top → Förderung prüfen', bool(cta) and 'Förderung prüfen' in cta.group(1), cta.group(1) if cta else 'missing')
check('early CTA target = treppenlift-zuschuss', 'treppenlift-zuschuss.html' in html[html.index('data-cta-id="compare_top"') - 200:html.index('data-cta-id="compare_top"') + 80])
# Related-Links: alle im Lift-/Förder-Cluster, keine Care-/Bad-Funnel
seg = html[html.index('class="related">'):html.index('class="related">') + 1200]
rel_slugs = re.findall(r'href="(?:https://zuhausebleiben-kompass\.de/)?([a-z0-9-]+)\.html"', seg)
check('related all lift-cluster', all(s.startswith('treppenlift') for s in rel_slugs), str(rel_slugs))
check('related non-empty', len(rel_slugs) == 3, str(rel_slugs))

# 5. Grafik eingebunden + Label
check('image src', 'assets/images/treppenlift-steuer-weg.svg' in html)
check('KI caption', 'KI-unterstützt erstellte Schema-Grafik' in html)

# 6. Kein Steuerversprechen / keine Beratungsclaims
for bad in ['Garantie', 'garantiert', 'Steuerberatung im Einzelfall', 'sicher absetzbar', 'Steuerspar-Tipp']:
    check(f'no claim "{bad}"', bad not in html)

print()
if FAIL:
    print(f'ERGEBNIS: {len(FAIL)} FAIL')
    sys.exit(1)
print('ERGEBNIS: ALL PASS')
