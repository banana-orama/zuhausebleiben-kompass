#!/usr/bin/env python3
"""Content-Support-Prüfung für hausnotruf-kuendigen:
jeder content-ready-Key muss im gebauten HTML erscheinen; [1]-[9] müssen auflösen;
Related-Links im Care-Cluster; Early-CTA-Ziel = Vergleichsseite; Kernzahlen im HTML.
Läuft gegen den LAUNCH-dist (erst build:launch, dann dieses Skript)."""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
slug = 'hausnotruf-kuendigen'
a = json.loads((ROOT / 'content-ready' / f'{slug}.json').read_text(encoding='utf-8'))
html_raw = (ROOT / 'dist' / f'{slug}.html').read_text(encoding='utf-8')
# Citation-Remnants als GANZES Element strippen (Renderer: <sup class="cite"><a href="#source-n">[n]</a></sup>)
html = re.sub(r'<sup class="cite">.*?</sup>', '', html_raw)

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
check('h1 present', a['h1'] in html)
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

# 3. Quellen 1-9 gerendert + alle Zitationen auflösen
for i, s in enumerate(a['sources'], 1):
    check(f'source-{i} anchor', f'id="source-{i}"' in html)
    check(f'source-{i} url', s['url'] in html)
used = set(int(n) for n in re.findall(r'\[(\d)\]', json.dumps(a['sections']) + json.dumps(a['faqs']) + a['intro']))
check('citations within sources', used <= set(range(1, len(a['sources']) + 1)), str(used))
check('all sources cited', used == set(range(1, len(a['sources']) + 1)), f'uncited: {set(range(1, 10)) - used}')

# 4. Kernzahlen im HTML (prose-Schreibweise, case-normalisiert)
hay = re.sub(r'\s+', ' ', html)
for needle in ['14 Tage', '27 Euro', 'zwei Jahre', 'einem Monat zum Monatsende', 'zwölf Monate und 14 Tage',
               'Verträge hier kündigen', 'jetzt kündigen', 'Vertragspartner der Pflegekasse']:
    check(f'needle: {needle}', needle.lower() in hay.lower())

# 5. Bild: eingebunden, Dimensionen, Alt, Caption
img = a['image']
check('image src rendered', img['src'] in html)
check('image alt rendered', img['alt'][:60] in html)
check('image caption rendered', 'KI-unterstützt' in html)
svg_text = (ROOT / img['src']).read_text(encoding='utf-8')
m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg_text)
check('svg viewBox', m is not None, img['src'])

# 6. Related-Links im Care-Cluster + CTA-Kontexte (Attribut-unabhängig prüfen)
start = html.index('class="related">')
seg = html[start:html.index('</section>', start)]
rel = re.findall(r'href="(?:https://zuhausebleiben-kompass\.de/)?([a-z0-9-]+)\.html"', seg)
check('related count 3', len(rel) == 3, str(rel))
care = re.compile(r'^(hausnotruf|pflegegrad|hilfsmittel|rollator|verhinderungspflege|tuerbreiten|beleuchtung|wohnumfeld)')
check('related all care-cluster', all(care.match(r) for r in rel), str(rel))
check('related first = vergleich', rel and rel[0] == 'hausnotruf-kosten-anbieter-vergleich', str(rel))
cta_ids = re.findall(r'data-cta-id="([a-z_]+)"', html)
check('cta ids within policy', set(cta_ids) <= {'checklist_top', 'compare_top', 'print_bottom', 'editorial_contact'}, str(cta_ids))
m_cta = re.search(r'<a[^>]*data-cta-id="compare_top"[^>]*>', html)
check('early CTA exists', m_cta is not None)
check('early CTA -> vergleich', m_cta is not None and 'hausnotruf-kosten-anbieter-vergleich.html' in m_cta.group(0))
check('early CTA content-id', m_cta is not None and 'data-content-id="hausnotruf-kuendigen"' in m_cta.group(0))
m_chk = re.search(r'<a[^>]*data-cta-id="checklist_top"[^>]*>', html)
href_m = re.search(r'href="#abschnitt-(\d+)"', m_chk.group(0)) if m_chk else None
sec_idx = next((i for i, s in enumerate(a['sections']) if 'Checkliste' in s['heading']), None)
check('checklist_top -> checklist anchor', href_m is not None and sec_idx is not None and int(href_m.group(1)) == sec_idx + 1, str(href_m and href_m.group(1)))

# 7. Legal/robots (LAUNCH-Modus: indexierbar)
check('robots index,follow', 'name="robots" content="index,follow"' in html)
check('in sitemap', slug + '.html' in (ROOT / 'dist' / 'sitemap.xml').read_text(encoding='utf-8'))

print()
print(f"RESULT: {'ALL PASS' if not FAIL else f'{len(FAIL)} FAILS: {FAIL}'}")
raise SystemExit(1 if FAIL else 0)
