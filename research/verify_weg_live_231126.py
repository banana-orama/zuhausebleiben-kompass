#!/usr/bin/env python3
"""Live-Readback WEG-Artikel 23.11.2026 — gegen die ÖFFENTLICHE URL (nicht origin-only).
Checkt: 200, robots index,follow, Canonical, H1/Title, Kernwortlaute, Related+CTA,
SVG 200, Sitemap 54 locs inkl. Artikel, RSS 41, llms.txt, Homepage-Verlinkung,
Partner-Marker 0, Impressum-USt-IdNr. (Separatcheck), keine Em-dash-Artefakte."""
import re, subprocess, sys, time, html as H

BASE = 'https://zuhausebleiben-kompass.de'
SLUG = 'treppenlift-eigentumswohnung-weg'
fails, checks = [], 0

def check(name, cond, detail=''):
    global checks
    checks += 1
    if not cond:
        fails.append(f'{name} :: {detail}')

def fetch(url):
    r = subprocess.run(['curl', '-sL', '--max-time', '60', url, '-w', '\n__HTTP__%{http_code}'],
                       capture_output=True, text=True)
    body, _, code = r.stdout.rpartition('__HTTP__')
    return body, code.strip()

def norm(s):
    s = H.unescape(s)
    s = re.sub(r'<sup[^>]*>.*?</sup>', ' ', s, flags=re.S)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = re.sub(r'\[\d+\]', ' ', s)
    return ' '.join(s.split())

# Deploy-Lag abwarten (Pages kann minutenlang 404 auf NEUE Pfade liefern)
body = ''
for attempt in range(1, 13):
    body, code = fetch(f'{BASE}/{SLUG}.html')
    if code == '200':
        print(f'Poll {attempt}: 200')
        break
    print(f'Poll {attempt}: {code} — warte 20s')
    time.sleep(20)
check('Artikel-URL 200', code == '200', code)

n = norm(body)
check('robots index,follow', 'index,follow' in body)
check('canonical', f'{BASE}/{SLUG}.html' in body)
check('title', '<title>Treppenlift in der Eigentumswohnung — ZuhauseBleiben Kompass</title>' in body)
check('h1', 'Der Weg zum Beschluss nach § 20 WEG' in n)
check('Quellenstand 2026-11-23', '2026-11-23' in body)

for needle in [
    'können beschlossen oder einem Wohnungseigentümer durch Beschluss gestattet werden',
    'Dafür ist es „ohne Belang“',
    'jeweils mit einfacher Stimmenmehrheit',
    'jedenfalls Zweifel hieran hegen',
    'Nur ihm gebühren die Nutzungen',
    '150 bis 300 Euro',
    '65 Zentimeter erhöhten Terrasse',
    'V ZR 244/22',
    'V ZR 33/23',
    'Beschlussantrag-Checkliste',
    'auf eigene Kosten einen Treppenlift im Treppenhaus',
]:
    check(f'live needle: {needle[:44]}', norm(needle) in n)

for gone in ['V ZR 140', 'VIII ZR', '4.180', '6.250', 'data-partner-placement', 'awin1.com', 'Entwurf zur ersten Orientierung']:
    check(f'live absent: {gone}', gone not in n)

mrel = re.search(r'<section class="related"><h2>Passend dazu</h2><ul>(.*?)</ul>', body, re.S)
rels = re.findall(r'href="https://zuhausebleiben-kompass\.de/([a-z\-]+)\.html"', mrel.group(1)) if mrel else []
check('live related order', rels == ['treppenlift-mietwohnung', 'wohnumfeldverbesserung-beantragen', 'treppenlift-kosten'], str(rels))
mh = re.search(r'href="([^"]+)" data-cta-id="compare_top"', body) or re.search(r'<a class="text-link" href="([^"]+)"[^>]*data-cta-id="compare_top"', body)
check('live CTA -> firmen-vergleich', bool(mh) and mh.group(1).endswith('/treppenlift-firmen-vergleich.html'), str(mh))

svg, scode = fetch(f'{BASE}/assets/images/treppenlift-weg-entscheidung.svg')
check('SVG 200 + Inhalt', scode == '200' and 'WEG-Beschluss nach § 20' in svg, scode)

sm, _ = fetch(f'{BASE}/sitemap.xml')
check('Sitemap 54 locs', sm.count('<loc>') == 54, str(sm.count('<loc>')))
check('Sitemap enthält Artikel', f'{SLUG}.html' in sm)
rss, _ = fetch(f'{BASE}/rss.xml')
check('RSS 41 Items', rss.count('<item>') == 41, str(rss.count('<item>')))
check('RSS enthält Artikel', SLUG in rss)
llms, lc = fetch(f'{BASE}/llms.txt')
check('llms 200 + Eintrag', lc == '200' and SLUG in llms, lc)
home, _ = fetch(f'{BASE}/')
check('Homepage verlinkt Artikel', SLUG in home)
imp, _ = fetch(f'{BASE}/impressum.html')
check('Impressum USt-IdNr. live', 'DE305157036' in imp)

print(f'checks: {checks}, fails: {len(fails)}')
for f in fails:
    print('FAIL:', f)
sys.exit(1 if fails else 0)
