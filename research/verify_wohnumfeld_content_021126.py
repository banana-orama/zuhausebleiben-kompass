#!/usr/bin/env python3
"""Content-Support-Gate fuer wohnumfeldverbesserung-beantragen (02.11.2026):
assertet, dass JEDEGER Unterstuetzte JSON-Key (Abschnitte, Paragraphen, Bullets,
Tabellenzellen, paragraphs_after, FAQs, Quellen) wirklich im gebauten HTML landet —
tags- und citations-normalisiert (sup.cite-[n]-Reste brechen naive Vergleiche).
Plus: robots, CTAs/Anker, Related-Links (Cross-Ziele zuerst, care-Cluster),
SVG-Referenz + Datei, Kernzahlen, JSON-LD, keine Partner-Marker, Home/RSS/Sitemap/llms.
Muster: verify_schmale_treppe_content_261026.py."""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIST = pathlib.Path(__file__).resolve().parent.parent / 'dist'
SLUG = 'wohnumfeldverbesserung-beantragen'
a = json.loads((ROOT / 'content-ready' / f'{SLUG}.json').read_text(encoding='utf-8'))
html = (DIST / f'{SLUG}.html').read_text(encoding='utf-8')

FAIL = []


def check(name, ok, ctx=''):
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  [{ctx}]" if ctx else ''))
    if not ok:
        FAIL.append(name)


def norm(t):
    t = re.sub(r'\s+', ' ', t.replace('\u00ad', '').replace('\xa0', ' '))
    return t.strip().lower()


def plain(h):
    t = re.sub(r'<script[^>]*>.*?</script>', ' ', h, flags=re.S)
    t = re.sub(r'<style[^>]*>.*?</style>', ' ', t, flags=re.S)
    t = re.sub(r'<sup class="cite">.*?</sup>', '', t, flags=re.S)
    t = re.sub(r'<[^>]+>', ' ', t)
    import html as H
    t = H.unescape(t)
    return norm(t)


hay = plain(html)

# 1) robots + Basis
check('robots index,follow', 'name="robots" content="index,follow"' in html or "content=\"index,follow\"" in html)
check('title head', html.count('<title>Wohnumfeld-Zuschuss beantragen — ZuhauseBleiben Kompass</title>') == 1)
check('H1', '<h1>Zuschuss für wohnumfeldverbessernde Maßnahmen beantragen</h1>' in html)
check('kein noindex', 'noindex' not in html)

# 2) Intro + alle Abschnitts-Headings + Paragraphen + Bullets + Tabellen + paragraphs_after
check('intro gerendert', norm(re.sub(r'\[\d+\]', '', a['intro']))[:90] in hay)
for i, s in enumerate(a['sections'], 1):
    check(f'abschnitt-{i} heading', norm(s['heading']) in hay, s['heading'][:40])
    for p in s.get('paragraphs', []):
        check(f'abschnitt-{i} p', norm(re.sub(r'\[\d+\]', '', p))[:80] in hay, p[:40])
    for p in s.get('bullets', []):
        check(f'abschnitt-{i} li', norm(re.sub(r'\[\d+\]', '', p))[:80] in hay, p[:40])
    for p in s.get('paragraphs_after', []):
        check(f'abschnitt-{i} p_after', norm(re.sub(r'\[\d+\]', '', p))[:80] in hay, p[:40])
    tbl = s.get('table')
    if tbl:
        for hcell in tbl['headers']:
            check(f'abschnitt-{i} th', norm(hcell) in hay, hcell[:30])
        for row in tbl['rows']:
            for c in row:
                check(f'abschnitt-{i} td', norm(re.sub(r'\[\d+\]', '', c)) in hay, c[:30])

# 3) FAQs + Quellen
for f in a['faqs']:
    check('faq q', norm(re.sub(r'\[\d+\]', '', f['question'])) in hay, f['question'][:40])
    check('faq a', norm(re.sub(r'\[\d+\]', '', f['answer']))[:80] in hay, f['answer'][:40])
for i, s in enumerate(a['sources'], 1):
    url_esc = s['url'].replace('&', '&amp;')
    check(f'source-{i} url', s['url'] in html or url_esc in html, s['url'][:50])
    check(f'source-{i} checked', f'geprüft {s["checked_at"]}' in html)

# 4) CTAs, Anker, Related
check('checklist_top Anker #abschnitt-6', 'href="#abschnitt-6"' in html)
check('checklist_top Label', 'Zur Checkliste' in html)
check('compare_top Ziel', 'href="https://zuhausebleiben-kompass.de/treppenlift-zuschuss.html"' in html)
check('compare_top Label', 'Förderlandschaft im Überblick' in html)
check('print_bottom', 'data-cta-id="print_bottom"' in html)
check('editorial_contact', 'data-cta-id="editorial_contact"' in html)
rel = re.search(r'Passend dazu</h2><ul>(.*?)</ul>', html, re.S).group(1)
rel_slugs = re.findall(r'/([a-z0-9-]+)\.html', rel)
check('related genau 3', len(rel_slugs) == 3, str(rel_slugs))
check('related cross zuerst', rel_slugs[:2] == ['hilfsmittel-pflegekasse-uebernahme', 'pflegegrad-antrag-ablauf-fristen'], str(rel_slugs))
check('related kein self', SLUG not in rel_slugs)

# 5) SVG
svg_name = a['image']['src'].split('/')[-1]
check('img referenziert', html.count(svg_name) >= 2, svg_name)
check('img alt', a['image']['alt'][:60] in html)
check('SVG-Datei existiert', (DIST / a['image']['src']).exists())
check('figcaption KI-Kennzeichnung', 'KI-unterstützt' in html)

# 6) Kernzahlen im HTML (Prosa-Schreibweise, case-normalisiert)
for needle in ['4.180 euro', '16.720 euro', 'drei wochen', 'fünf wochen', 'pflegegrade 1 bis 5',
               '33.40.05.0', '2.090 euro', '5.220 euro', 'september 2021', 'vor dem umbau',
               'als genehmigt', 'innerhalb eines monats']:
    check(f'kernzahl "{needle}"', needle in hay)

# 7) JSON-LD valide + FAQPage
m = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
check('JSON-LD vorhanden', bool(m))
try:
    schema = json.loads(m.group(1))
    types = [n.get('@type') for n in schema.get('@graph', [])]
    check('JSON-LD Article', 'Article' in types, str(types))
    check('JSON-LD FAQPage', 'FAQPage' in types)
    check('keine ***-Korruption', '***' not in m.group(1))
except Exception as e:
    check('JSON-LD parse', False, str(e))

# 8) Keine Partner-Marker (Inaktiv-Build)
check('kein partner-cta', 'data-partner-placement' not in html)
check('kein rel=sponsored', 'rel="sponsored' not in html)

# 9) Home/RSS/Sitemap/llms
home = (DIST / 'index.html').read_text(encoding='utf-8')
check('home listet Artikel', SLUG in home)
rss = (DIST / 'rss.xml').read_text(encoding='utf-8')
check('rss enthält Artikel', SLUG in rss)
sm = (DIST / 'sitemap.xml').read_text(encoding='utf-8')
check('sitemap enthält Artikel', f'{SLUG}.html' in sm)
llms = (DIST / 'llms.txt').read_text(encoding='utf-8')
check('llms enthält Artikel', SLUG in llms)

print()
if FAIL:
    print(f"ERGEBNIS: {len(FAIL)} FAIL: {FAIL[:8]}")
    sys.exit(1)
print("ERGEBNIS: ALL PASS")
