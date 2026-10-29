#!/usr/bin/env python3
"""Schema-Deploy-Gate fuer b120a2e (FAQPage + Org/WebSite + Article-Dates).
Prueft den FRISCHEN dist-Build: jedes ld+json-Block parst, FAQPage auf allen
Artikeln, Zitations-Superscripts [n] aus Schema-Texten gestrippt, keine
Sanitizer-Korruption ('***') im Kontext, datePublished/-Modified je Artikel."""
import json, re, sys, glob, os

DIST = os.environ.get('DIST_DIR') or os.path.join(os.path.dirname(__file__), '..', 'dist')
fails = []
ok = 0

def ldjson_blocks(html):
    return re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)

# 1) Alle ld+json-Bloecke im gesamten Dist parsen
pages = glob.glob(os.path.join(DIST, '*.html'))
for p in pages:
    html = open(p, encoding='utf-8').read()
    for i, blk in enumerate(ldjson_blocks(html)):
        try:
            data = json.loads(blk)
        except Exception as e:
            fails.append(f'{os.path.basename(p)} block{i}: JSON-PARSE {e}')
            continue
        blob = json.dumps(data, ensure_ascii=False)
        if '***' in blob:
            fails.append(f'{os.path.basename(p)} block{i}: SANITIZER-KORRUPTION')
        if data.get('@context') not in ('https://schema.org', 'https://schema.org/'):
            fails.append(f'{os.path.basename(p)} block{i}: context={data.get("@context")!r}')
        else:
            ok += 1

# 2) Artikel-Gates — Artikelliste aus content-ready/*.json (echte Ratgeber, keine Rechts-/Meta-Seiten)
cr = os.path.join(os.path.dirname(__file__), '..', 'content-ready')
slugs = sorted(os.path.splitext(f)[0] for f in os.listdir(cr) if f.endswith('.json'))
articles = [os.path.join(DIST, s + '.html') for s in slugs]
missing = [s for s in slugs if not os.path.exists(os.path.join(DIST, s + '.html'))]
if missing:
    fails.append(f'Artikel ohne Built-Seite: {missing}')
faq_count = 0
for p in articles:
    html = open(p, encoding='utf-8').read()
    blocks = ldjson_blocks(html)
    graphs = []
    for blk in blocks:
        d = json.loads(blk)
        if isinstance(d.get('@graph'), list):
            graphs = d['@graph']
    types = [n.get('@type') for n in graphs]
    slug = os.path.basename(p)[:-5]
    if 'Article' not in types:
        fails.append(f'{slug}: kein Article-Node')
    if 'BreadcrumbList' not in types:
        fails.append(f'{slug}: keine BreadcrumbList')
    art = next((n for n in graphs if n.get('@type') == 'Article'), {})
    for key in ('datePublished', 'dateModified', 'author', 'publisher'):
        if key not in art:
            fails.append(f'{slug}: Article.{key} fehlt')
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', str(art.get('datePublished', ''))):
        fails.append(f'{slug}: datePublished kein ISO-Datum: {art.get("datePublished")!r}')
    faq = next((n for n in graphs if n.get('@type') == 'FAQPage'), None)
    # Anzahl der <details> im sichtbaren FAQ-Abschnitt muss mit mainEntity uebereinstimmen
    m = re.search(r'<section class="faq">(.*?)</section>', html, re.S)
    if m:
        n_vis = len(re.findall(r'<details>', m.group(1)))
        if n_vis == 0:
            continue  # Artikel ohne FAQ-Abschnitt
        if faq is None:
            fails.append(f'{slug}: {n_vis} FAQs sichtbar, aber kein FAQPage-Node')
        else:
            faq_count += 1
            qs = [q.get('name', '') for q in faq.get('mainEntity', [])]
            if len(qs) != n_vis:
                fails.append(f'{slug}: mainEntity {len(qs)} != sichtbar {n_vis}')
            for q in qs:
                if re.search(r'\[\d+\]', q):
                    fails.append(f'{slug}: Zitationsmarker in Schema-Frage: {q[:60]!r}')
                    break
            for ans in faq.get('mainEntity', []):
                t = ans.get('acceptedAnswer', {}).get('text', '')
                if re.search(r'\[\d+\]', t):
                    fails.append(f'{slug}: Zitationsmarker in Schema-Antwort')
                    break
    else:
        if faq is not None:
            fails.append(f'{slug}: FAQPage-Node ohne sichtbaren FAQ-Abschnitt')

# 3) Home-Graph
home = open(os.path.join(DIST, 'index.html'), encoding='utf-8').read()
htypes = []
for blk in ldjson_blocks(home):
    d = json.loads(blk)
    htypes += [n.get('@type') for n in d.get('@graph', [])]
if 'Organization' not in htypes:
    fails.append('home: kein Organization-Node')
if 'WebSite' not in htypes:
    fails.append('home: kein WebSite-Node')

print(f'ld+json-Bloecke parse-valide: {ok}')
print(f'Artikel mit FAQPage-Schema: {faq_count}')
print(f'Home-Graph-Typen: {htypes}')
if fails:
    print(f'\nFAILS ({len(fails)}):')
    for f in fails:
        print(' FAIL', f)
    sys.exit(1)
print('ALL PASS')
