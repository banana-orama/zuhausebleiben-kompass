#!/usr/bin/env python3
"""Live readback: poll until the FRESH paare deploy is public (new Johanniter sentence present),
then verify sitemap/RSS/llms/homepage/cross-links. Distinguishes fresh deploy from stale page."""
import re, sys, time, urllib.request

BASE = 'https://zuhausebleiben-kompass.de'
NEW_MARKER = 'Johanniter-Angebotsseite'   # only in the adopted source build
PATHS = {
    'paare': '/hausnotruf-fuer-paare.html',
    'sitemap': '/sitemap.xml',
    'rss': '/rss.xml',
    'llms': '/llms.txt',
    'home': '/index.html',
    'kosten': '/hausnotruf-kosten-anbieter-vergleich.html',
    'alarm': '/hausnotruf-alarm-ablauf.html',
    'angeh': '/hausnotruf-angehoerige-einrichten.html',
}
cache = {}

def get(p):
    for attempt in range(3):
        try:
            with urllib.request.urlopen(BASE + p, timeout=30) as r:
                return r.read().decode('utf-8', 'replace')
        except Exception as e:
            if attempt == 2: return ''
            time.sleep(5)
    return ''

deadline = time.time() + 420
fresh = False
while time.time() < deadline and not fresh:
    paare = get(PATHS['paare'])
    fresh = NEW_MARKER in paare
    if not fresh:
        print(time.strftime('%H:%M:%S'), 'still stale/missing, waiting…', flush=True)
        time.sleep(25)

cache['paare'] = get(PATHS['paare'])
for k in ('sitemap', 'rss', 'llms', 'home', 'kosten', 'alarm', 'angeh'):
    cache[k] = get(PATHS[k])

ok = True
def check(name, cond, detail=''):
    global ok
    print(('PASS' if cond else 'FAIL'), '|', name, ('| ' + str(detail)[:90] if detail else ''))
    if not cond: ok = False

check('fresh deploy live (Johanniter [7] sentence)', NEW_MARKER in cache['paare'])
check('robots index,follow', 'name="robots" content="index,follow"' in cache['paare'])
check('in sitemap', 'hausnotruf-fuer-paare.html' in cache['sitemap'])
check('in RSS', 'hausnotruf-fuer-paare.html' in cache['rss'])
check('llms.txt summary', 'hausnotruf-fuer-paare' in cache['llms'])
check('homepage lists it', 'hausnotruf-fuer-paare.html' in cache['home'])
check('paare related section links all 3 cluster targets', len(re.findall(r'hausnotruf-(kosten-anbieter-vergleich|alarm-ablauf|angehoerige-einrichten)\.html', cache['paare'])) >= 3)
check('at least one in-cluster page links back (pool cap-3 design)', 'hausnotruf-fuer-paare.html' in cache['alarm'])
check('key number 27,00 EUR live', '27,00 EUR' in cache['paare'])
check('54-Euro-Kontrast live', '54 Euro' in cache['paare'])
check('sources 8 live', len(re.findall(r'<li id="source-\d"', cache['paare'])) == 8)
check('svg live', 'hausnotruf-paare-konstellationen' in cache['paare'])
check('canonical absolute live', 'rel="canonical" href="https://zuhausebleiben-kompass.de/hausnotruf-fuer-paare.html"' in cache['paare'])

print('\nRESULT:', 'ALL PASS' if ok else 'FAILURES PRESENT')
sys.exit(0 if ok else 1)
