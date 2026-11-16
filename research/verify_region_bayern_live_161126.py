#!/usr/bin/env python3
"""Live-Readback fuer die Bayern-Region-Seite auf der oeffentlichen URL.
Erwartet: 200, index,follow, Kernfakten im Body, 17 Quellen checked 16.11.,
Sitemap exakt 51 locs mit nrw+bayern, Hub-Spiegel, 0x Partner-/Betrags-Marker."""
import re, sys, time
from html import unescape
from urllib.request import urlopen, Request

BASE = 'https://zuhausebleiben-kompass.de'
UA = {'User-Agent': 'Mozilla/5.0 (readback check)'}

def get(path, tries=3):
    for i in range(tries):
        try:
            with urlopen(Request(BASE + path, headers=UA), timeout=30) as r:
                return r.status, r.read().decode('utf-8', errors='replace')
        except Exception as e:
            if i == tries - 1:
                raise
            time.sleep(4)

fails = []
def check(name, cond, detail=''):
    print(('PASS' if cond else 'FAIL'), name, detail)
    if not cond:
        fails.append(name)

def body_of(html):
    t = re.sub(r'<sup[^>]*>.*?</sup>', ' ', html, flags=re.S)
    t = re.sub(r'<[^>]+>', ' ', t)
    return re.sub(r'\s+', ' ', unescape(t))

# Pages-Deploy-Lag abwarten: der neue Pfad muss 200 liefern
for attempt in range(8):
    st, bayern = get('/region/bayern.html')
    if st == 200:
        break
    print('poll', st, 'attempt', attempt + 1)
    time.sleep(20)
check('bayern.html 200', st == 200, f'status={st}')
check('robots index,follow', '<meta name="robots" content="index,follow"' in bayern)
check('canonical', 'href="https://zuhausebleiben-kompass.de/region/bayern.html"' in bayern)
b = body_of(bayern)
for needle in ['Umbau und Förderung in Bayern', '10.000', '28.300', '43.200',
               '10.700', '3.200', 'sozialen Dringlichkeit', 'formlos',
               'Diesen Zuschuss können Sie nicht mehr beantragen',
               'wird eine Antragstellung wieder möglich sein',
               'Treppenlifte, Senkrecht-, Hebe- oder Plattformlifte installieren',
               'mit dem Kredit der KfW gefördert werden',
               'Pflegestützpunkt', '40.000', 'nicht namentlich']:
    check(f'live fact "{needle[:44]}"', needle in b)
for absent in ['4.180', '16.720', 'awin', 'sponsored', '>Anzeige<', 'NRW.BANK', 'LVR', 'LWL']:
    check(f'live absence "{absent}"', absent not in b)
check('17 Quellen checked 16.11.', bayern.count('geprüft 2026-11-16') >= 17, f"n={bayern.count('geprüft 2026-11-16')}")
check('CTA treppenlift-zuschuss', 'treppenlift-zuschuss.html' in bayern)

st2, sm = get('/sitemap.xml')
locs = [u.split('<loc>')[1].split('</loc>')[0] for u in sm.split('<url>')[1:]]
region_urls = sorted(u for u in locs if '/region/' in u)
check('sitemap 51 locs', len(locs) == 51, f'n={len(locs)}')
check('sitemap regions nrw+bayern', region_urls == [
    'https://zuhausebleiben-kompass.de/region/bayern.html',
    'https://zuhausebleiben-kompass.de/region/nordrhein-westfalen.html'], str(region_urls))

st3, hub = get('/regional.html')
hb = body_of(hub)
check('hub 200 + 2-Regionen-Prosa', st3 == 200 and 'Nordrhein-Westfalen und Bayern sind als erste Regionen' in hb)
check('hub bayern teaser', 'leistungsfreies Landesdarlehen bis 10.000' in hb)

st4, home = get('/')
check('home 200', st4 == 200)

print(f"\n{'ALL PASS' if not fails else 'FAILS: ' + ', '.join(fails)}")
sys.exit(1 if fails else 0)
