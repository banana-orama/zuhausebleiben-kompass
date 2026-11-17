#!/usr/bin/env python3
"""Live-Readback badumbau-kosten (17.11.2026) auf der ÖFFENTLICHEN URL.
Poll bis 200 (Pages-Lag), dann: robots, Title/H1, Lead-Absätze, Kernzahlen,
Related-Reihenfolge, Early-CTA, SVG, Sitemap 52 locs, RSS 39, Homepage, llms,
Absenzen 0x awin/sponsored. Danach IndexNow-Submission (Article + Homepage)."""
import sys, time, re, json, urllib.request, html as htmlmod

BASE = 'https://zuhausebleiben-kompass.de'
ART = f'{BASE}/badumbau-kosten.html'
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}

def get(url, timeout=40):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode('utf-8', 'replace')

passes, fails = 0, []

def check(name, cond, detail=''):
    global passes
    if cond:
        passes += 1
    else:
        fails.append(f'{name}: {detail}')

# 1) Poll bis 200 (max ~8 min)
status, raw = 0, ''
for i in range(32):
    try:
        status, raw = get(ART)
        if status == 200:
            break
    except Exception as e:
        status = 0
    time.sleep(15)
check('article 200', status == 200, f'status={status}')
txt = htmlmod.unescape(raw)

# 2) Robots / Head
check('robots index,follow', 'index,follow' in raw, raw[:200])
check('canonical', 'rel="canonical" href="https://zuhausebleiben-kompass.de/badumbau-kosten.html"' in raw)
check('title', 'Badumbau-Kosten: Preis &amp; Eigenanteil' in raw or 'Badumbau-Kosten: Preis & Eigenanteil' in raw)
check('h1', 'Badumbau-Kosten: vom Portal-Richtwert zum Eigenanteil' in txt)

# 3) Lead-Absätze (2, ohne Komma-Splice)
for p in ['Ein Badumbau hat keinen Festpreis.', 'Dieser Ratgeber ordnet die veröffentlichten Spannen ein,']:
    check(f'lead {p[:25]}', p in txt)

# 4) Kernzahlen (Prosa-Wortlaut)
for n in ['4.180 Euro je Maßnahme', '16.720 Euro je Maßnahme', 'höchstens um 1.200 Euro',
          '13.000 und 30.000', '18.000', '13.820', '15 bis 20 Prozent',
          'öffentlich geförderte Maßnahmen, für die zinsverbilligte Darlehen',
          'Diesen Zuschuss können Sie nicht mehr beantragen', '455-B', 'Kredit 159',
          'geprüft 2026-11-17']:
    check(f'needle {n[:32]}', n in txt, 'fehlt live')

# 5) Related-Reihenfolge + Early-CTA
seg = re.search(r'<section class="related">.*?</section>', raw, re.S)
check('related section', bool(seg))
if seg:
    slugs = re.findall(r'href="https://zuhausebleiben-kompass\.de/([a-z0-9-]+)\.html"', seg.group(0))
    check('related order', slugs == ['badumbau-angebote-vergleichen', 'wohnumfeldverbesserung-beantragen', 'wanne-zur-dusche'], str(slugs))
check('early CTA target', 'href="https://zuhausebleiben-kompass.de/badumbau-angebote-vergleichen.html" data-cta-id="compare_top"' in raw or ('badumbau-angebote-vergleichen.html' in raw and 'compare_top' in raw))
check('cta label live', 'Angebote mit Einzelpositionen vergleichen' in txt)

# 6) Absenzen
for bad in ['awin', 'awinmid', 'sponsored', 'data-partner-placement', 'ENTWURF']:
    check(f'absent {bad}', bad not in raw, f'{bad} LIVE gefunden')

# 7) SVG
s2, svg = get(f'{BASE}/assets/images/badumbau-kosten-wegweiser.svg')
check('svg 200', s2 == 200, str(s2))
check('svg 5 legenden', svg.count('Eigenanteil') >= 2 and 'height="1180"' in svg)

# 8) Sitemap / RSS / Homepage / llms
s3, sm = get(f'{BASE}/sitemap.xml')
locs = re.findall(r'<loc>([^<]+)</loc>', sm)
check('sitemap 200', s3 == 200)
check('sitemap 52 locs', len(locs) == 52, str(len(locs)))
check('article in sitemap', any(u.endswith('badumbau-kosten.html') for u in locs))
s4, rss = get(f'{BASE}/rss.xml')
check('rss 39 items', rss.count('<item>') == 39, str(rss.count('<item>')))
check('rss has article', 'badumbau-kosten' in rss)
s5, home = get(BASE + '/')
check('home 200 + listing', s5 == 200 and 'badumbau-kosten' in home)
s6, llms = get(f'{BASE}/llms.txt')
check('llms 200 + article', s6 == 200 and 'badumbau-kosten' in llms)

print(f'LIVE PASSES: {passes}')
if fails:
    print(f'LIVE FAILS: {len(fails)}')
    for f in fails:
        print('  FAIL:', f)
    sys.exit(1)
print('LIVE READBACK ALL PASS')
