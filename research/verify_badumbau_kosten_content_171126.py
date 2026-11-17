# Content-Gate badumbau-kosten (17.11.2026) gegen LAUNCH-dist
# Alle JSON-Keys, Kernzahlen, Related-Links, CTA, Anker, Absenzen.
from html import unescape
import json, re, sys, os

BASE = '/Users/mac/agentic-business/barrierefrei-leads'
DIST = f'{BASE}/dist'
SLUG = 'badumbau-kosten'

art = json.load(open(f'{BASE}/content-ready/{SLUG}.json', encoding='utf-8'))
raw = open(f'{DIST}/{SLUG}.html', encoding='utf-8').read()
html = unescape(raw)

def strip_citations(s):
    s = re.sub(r'<sup[^>]*>.*?</sup>', '', s, flags=re.S)
    s = re.sub(r'\[\d+\]', '', s)
    return re.sub(r'\s+', ' ', s).strip()

def norm(s):
    s = strip_citations(s)
    return re.sub(r'\s+', ' ', s).strip()

passes, fails = 0, []

def check(name, cond, detail=''):
    global passes
    if cond:
        passes += 1
    else:
        fails.append(f'{name}: {detail}')

# 1) Headline-Elemente
check('title', art['title'] in html, art['title'])
check('h1', art['h1'] in html, art['h1'])
check('description in meta', art['description'] in raw)
check('robots index,follow', 'name="robots" content="index,follow"' in raw or 'content="index,follow"' in raw)

# 2) Intro-Absätze (Array = 2 Lead-Absätze, kein Komma-Splice)
if isinstance(art['intro'], list):
    check('intro count == 2', len(art['intro']) == 2, str(len(art['intro'])))
    for i, p in enumerate(art['intro']):
        check(f'intro[{i}]', norm(p) in norm(html), p[:60])

# 3) Sections: heading, paragraphs, bullets, tables, paragraphs_after
for si, sec in enumerate(art['sections'], 1):
    check(f's{si} heading', norm(sec['heading']) in norm(html), sec['heading'][:50])
    check(f's{si} anchor', f'abschnitt-{si}' in raw, f'abschnitt-{si}')
    for pi, p in enumerate(sec.get('paragraphs', [])):
        check(f's{si} p{pi}', norm(p) in norm(html), p[:60])
    for bi, b in enumerate(sec.get('bullets', [])):
        check(f's{si} bullet{bi}', norm(b) in norm(html), b[:60])
    t = sec.get('table')
    if t:
        for h in t['headers']:
            check(f's{si} th {h[:20]}', strip_citations(h) in html, h)
        for ri, row in enumerate(t['rows']):
            for ci, cell in enumerate(row):
                check(f's{si} r{ri}c{ci}', strip_citations(cell) in html, cell[:40])
    for pi, p in enumerate(sec.get('paragraphs_after', [])):
        check(f's{si} after{pi}', norm(p) in norm(html), p[:60])

# 4) FAQs
for fi, faq in enumerate(art.get('faqs', [])):
    check(f'faq{fi} q', norm(faq['question']) in norm(html), faq['question'][:50])
    check(f'faq{fi} a', norm(faq['answer']) in norm(html), faq['answer'][:50])

# 5) Quellen: alle URLs im HTML (Escape-Varianten), Anker-Referenzen
for si, src in enumerate(art['sources'], 1):
    url = src['url'].replace('&', '&amp;')
    check(f'src{si} url', url in raw or src['url'] in raw, src['url'][:50])

# 6) Kernzahlen (Prosa-Wortlaut!)
NEEDLES = ['4.180 Euro je Maßnahme', '16.720 Euro je Maßnahme', '20 Prozent der Aufwendungen',
           'höchstens um 1.200 Euro', 'nur für Arbeitskosten', '13.000 und 30.000',
           '8.000 Euro', '40.000 Euro', '15.000 bis 25.000', '13.000 bis 28.000',
           '18.000', '13.820', '6.000', '15 bis 20 Prozent', 'drei Wochen', 'fünf Wochen',
           'öffentlich geförderte Maßnahmen', 'zinsverbilligte Darlehen', '455-B', 'Kredit 159']
for n in NEEDLES:
    check(f'needle {n[:30]}', n in html, 'fehlt')

# 7) Absenzen (Live-HTML)
for bad in ['awin', 'awinmid', 'sponsored', 'rel="nofollow sponsored"', 'data-partner-placement', 'ENTWURF', '4 180']:
    check(f'absent {bad}', bad not in raw, f'{bad} gefunden')

# 8) Related-Links: genau 3, Reihenfolge cross-links.json, absolute URLs
links_json = json.load(open(f'{BASE}/data/cross-links.json', encoding='utf-8'))
expected = links_json['links'][SLUG]
rel_section = re.search(r'<section class="related">.*?</section>', raw, re.S)
check('related section exists', bool(rel_section))
if rel_section:
    seg = rel_section.group(0)
    hrefs = re.findall(r'href="(https://[^"]*/([a-z0-9-]+)\.html)"', seg)
    got_slugs = [s for _, s in hrefs]
    check('related order', got_slugs == expected, f'{got_slugs} != {expected}')
    check('related exactly 3', len(got_slugs) == 3, str(len(got_slugs)))

# 9) Early-CTA (specialMap)
cta = 'data-cta-id="compare_top"'
check('early CTA marker', cta in raw, 'compare_top fehlt')
check('early CTA target', 'href="https://zuhausebleiben-kompass.de/badumbau-angebote-vergleichen.html"' in raw or '/badumbau-angebote-vergleichen.html' in raw)
check('cta label', 'Angebote mit Einzelpositionen vergleichen' in html)

# 10) SVG-Bild
img = art['image']
check('svg src', img['src'] in raw)
check('svg file exists', os.path.exists(f'{BASE}/assets/images/{os.path.basename(img["src"])}'))
check('alt set', img['alt'] in raw)
check('KI caption', 'KI-Illustration' in raw)

# 11) Checkbox: article json cite markers resolve (max source number)
maxn = len(art['sources'])
used = set(int(x) for x in re.findall(r'\[(\d+)\]', json.dumps(art)))
check('citations within range', all(1 <= n <= maxn for n in used), str(sorted(used)))
check('all sources cited', len(used) >= maxn, f'{len(used)} von {maxn}')

print(f'PASSES: {passes}')
if fails:
    print(f'FAILS: {len(fails)}')
    for f in fails:
        print('  FAIL:', f)
    sys.exit(1)
print('ALL PASS')
