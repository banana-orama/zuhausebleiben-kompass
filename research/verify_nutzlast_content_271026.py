#!/usr/bin/env python3
"""Content-Support-Pruefung fuer treppenlift-maximalgewicht:
jeder content-ready-Key muss im gebauten HTML erscheinen; [1]-[9] muessen aufloesen;
Related-Links im Lift-Cluster; Early-CTA-Ziel = Angebote vergleichen (angebote-vergleichen).
Muster: verify_schmale_treppe_content_261026.py."""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
slug = 'treppenlift-maximalgewicht'
a = json.loads((ROOT / 'content-ready' / f'{slug}.json').read_text(encoding='utf-8'))
html = (ROOT / 'dist' / f'{slug}.html').read_text(encoding='utf-8')

FAIL = []


def norm(t):
    return re.sub(r'\s+', ' ', t).strip()


def plain(t):
    """Renderer verwandelt [n] in Quellen-Anker-Links — fuer den Textvergleich rausfiltern."""
    return re.sub(r'\s+', ' ', re.sub(r'\[\d\]', '', t)).strip()


htxt = norm(re.sub(r'\[\d\]', '', re.sub(r'<[^>]+>', ' ', html)))


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
    head = re.split(r'\[\d\]', f['answer'])[0]
    check('faq a', plain(head)[:70] in htxt)

# 3. Quellen 1-9 gerendert + Zitationen [1]-[9] aufloesen
for i, s in enumerate(a['sources'], 1):
    check(f'source-{i} anchor', f'id="source-{i}"' in html)
    check(f'source-{i} url', s['url'] in html)
used = set(int(n) for n in re.findall(r'\[(\d)\]', json.dumps(a['sections']) + json.dumps(a['faqs'])))
check('citations used <= sources', used <= set(range(1, len(a['sources']) + 1)), str(sorted(used)))
check('all 9 sources cited', used == set(range(1, 10)), str(sorted(used)))

# 4. CTA-Ziele: Early-CTA compare_top -> angebote-vergleichen ("Angebote vergleichen")
cta = re.search(r'data-cta-id="compare_top"[^>]*>([^<]+)<', html)
check('early CTA compare_top -> Angebote vergleichen', bool(cta) and 'Angebote vergleichen' in cta.group(1), cta.group(1) if cta else 'missing')
cta_pos = html.index('data-cta-id="compare_top"')
check('early CTA target = treppenlift-angebote-vergleichen', 'treppenlift-angebote-vergleichen.html' in html[cta_pos - 300:cta_pos + 80])
check('checklist section exists', 'Checkliste: die Tragkraft im Beratungsgespräch klären' in html)
check('checklist anchor target exists', re.search(r'id="abschnitt-\d+"', html) is not None)
# Related-Links: alle im Lift-Cluster, genau 3 (nur das <ul> der Related-Sektion)
seg_start = html.index('class="related">')
seg = html[seg_start:html.index('</ul>', seg_start)]
rel_slugs = re.findall(r'href="(?:https://zuhausebleiben-kompass\.de/)?([a-z0-9-]+)\.html"', seg)
check('related all lift-cluster', all(s.startswith('treppenlift') for s in rel_slugs), str(rel_slugs))
check('related non-empty', len(rel_slugs) == 3, str(rel_slugs))

# 5. Grafik eingebunden + Label + alt gesetzt
check('image src', 'assets/images/treppenlift-maximalgewicht-tragkraft.svg' in html)
check('KI caption', 'KI-unterstützt erstellte Schema-Grafik' in html)
check('image has alt', 'alt="Schema-Grafik zur Tragkraft' in html)

# 6. Kernzahlen im HTML (die Belege der Tabelle)
for num in ['125 kg', '135 kg', '150 kg', '160 kg', '175 kg', '200 kg', '250', '300 kg']:
    check(f'kernzahl {num} present', num in htxt)

# 7. Keine Verkaufs-/Diagnose-/Garantieversprechen-Claims
for bad in ['garantiert', 'immer möglich', 'ohne Aufmaß', 'PREISGARANTIE', 'Testsieger', '100 % sicher', 'Lieferung sofort möglich', 'Bewilligung wird zugesagt']:
    check(f'no claim "{bad}"', bad not in html)

print()
if FAIL:
    print(f'ERGEBNIS: {len(FAIL)} FAIL')
    sys.exit(1)
print('ERGEBNIS: ALL PASS')
