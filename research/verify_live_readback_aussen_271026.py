#!/usr/bin/env python3
"""Live-Readback Briefing 13 (treppenlift-aussentreppen-aussenlift) auf der oeffentlichen URL.
Muster: verify_live_readback_nutzlast_271026.py."""
import re
import sys
import urllib.request

BASE = 'https://zuhausebleiben-kompass.de'
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36'}
FAIL = []


def fetch(path, binary=False):
    req = urllib.request.Request(BASE + path, headers=UA)
    with urllib.request.urlopen(req, timeout=45) as r:
        data = r.read()
    return (data if binary else data.decode('utf-8', errors='replace')), r.status


def check(label, cond, detail=''):
    print(('PASS ' if cond else 'FAIL ') + label + ('' if cond else f'  {detail}'))
    if not cond:
        FAIL.append(label)


art, st = fetch('/treppenlift-aussentreppen-aussenlift.html')
check('article HTTP 200', st == 200, str(st))
check('robots index,follow', 'name="robots" content="index,follow"' in art)
check('no ENTWURF badge', 'ENTWURF' not in art)
check('Quellenstand 2026-10-27', '2026-10-27' in art)
check('h1 correct', 'Treppenlift für die Außentreppe' in art)
check('8 sources rendered', len(re.findall(r'id="source-\d+"', art)) == 8)
check('price divergence table live', '3.500–6.500 €' in art and '6.500–8.500 €' in art)
check('lifta price incl einbau', 'inklusive Einbau und Inbetriebnahme' in art)
check('IP-absenz claim live', 'keiner der beiden hersteller nennt' in art.lower())
check('winter temp live', '−10 bis −15 °C' in art)
check('early CTA label', 'Anbieter für Außenlift vergleichen' in art)
cta_pos = art.find('data-cta-id="compare_top"')
check('early CTA target firmen-vergleich', cta_pos > 0 and 'treppenlift-firmen-vergleich.html' in art[cta_pos - 300:cta_pos + 80])
check('svg asset referenced', 'assets/images/treppenlift-aussentreppen-aussenlift-wetterschutz.svg' in art)
check('KI caption live', 'KI-unterstützt erstellte Schema-Grafik' in art)

svg, sst = fetch('/assets/images/treppenlift-aussentreppen-aussenlift-wetterschutz.svg', binary=True)
check('svg HTTP 200', sst == 200, str(sst))
check('svg has legend 6', b'230-V-Au' in svg and b'\xc3\x9fensteckdose' in svg)

home, hst = fetch('/')
check('home HTTP 200', hst == 200, str(hst))
check('home robots index,follow', 'name="robots" content="index,follow"' in home)
check('home lists new article', 'treppenlift-aussentreppen-aussenlift.html' in home)

sm, sst2 = fetch('/sitemap.xml')
locs = sm.count('<loc>')
check('sitemap 47 locs', locs == 47, str(locs))
check('article in sitemap', 'treppenlift-aussentreppen-aussenlift.html' in sm)

rss, rst = fetch('/rss.xml')
items = rss.count('<item>')
check('rss 24 items', items == 24, str(items))

llms, lst = fetch('/llms.txt')
check('llms.txt has article', 'aussentreppen-aussenlift' in llms)

firmen, fst = fetch('/treppenlift-firmen-vergleich.html')
check('CTA target page 200', fst == 200, str(fst))

print()
if FAIL:
    print(f'ERGEBNIS: {len(FAIL)} FAIL')
    sys.exit(1)
print('ERGEBNIS: ALL PASS')
