#!/usr/bin/env python3
"""Live-Readback für hausnotruf-schluesselhinterlegung (Briefing 19) auf der ÖFFENTLICHEN URL.
Prüft: HTTP 200, robots index,follow, Title, H1, Kernzahlen, Quellenstand, SVG (absolut, HTTP 200),
Quellen-Anker, kein Partner-Marker, Sitemap/RSS/llms/Homepage-Mitgliedschaft."""
import pathlib
import re
import urllib.request

BASE = 'https://zuhausebleiben-kompass.de'
SLUG = 'hausnotruf-schluesselhinterlegung'
OUT = pathlib.Path(__file__).resolve().parent / 'evidence' / 'schluessel-061126'
OUT.mkdir(parents=True, exist_ok=True)
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126 Safari/537.36'}
FAIL = []
N = 0


def check(label, cond, detail=''):
    global N
    N += 1
    print(('PASS ' if cond else 'FAIL ') + label + ('' if cond else f'  {detail}'))
    if not cond:
        FAIL.append(label)


def fetch(path):
    req = urllib.request.Request(BASE + path, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.status, r.read().decode('utf-8', errors='replace')


code, html = fetch(f'/{SLUG}.html')
(OUT / 'live-artikel.html').write_text(html, encoding='utf-8')
check('Artikel HTTP 200', code == 200, str(code))
check('robots index,follow', re.search(r'name="robots" content="index,? ?follow"', html) is not None)
check('Title', 'Hausnotruf: Schlüssel hinterlegen' in html)
check('H1', 'Hausnotruf-Schlüsselhinterlegung' in html)
for needle in ['2.957,21', 'fast 800 Euro', 'etwa 15 Euro', '30 bis 80 Euro', '35 bis 100 Euro',
               '27 und 40 Euro', '§ 536a BGB', 'kein Generalschlüssel', 'AG Hildburghausen',
               '06.11.2026', 'in demselben Gespräch', 'KI-unterstützt']:
    check(f'live enthält "{needle}"', needle in html)
check('SVG live (absolut)', f'src="{BASE}/assets/images/hausnotruf-schluessel-entscheidung.svg"' in html)
check('kein Partner-Marker', 'data-partner-placement' not in html)
check('kein awin Tracker', 'awin1.com' not in html)
for n in range(1, 9):
    check(f'Anker source-{n}', f'id="source-{n}"' in html)
check('Quellen-Stand 2026-11-06', '2026-11-06' in html)

code_svg, svg = fetch('/assets/images/hausnotruf-schluessel-entscheidung.svg')
check('SVG HTTP 200', code_svg == 200, str(code_svg))
check('SVG Stand-Datum', '06.11.2026' in svg)

code_sm, sm = fetch('/sitemap.xml')
check('Sitemap HTTP 200', code_sm == 200, str(code_sm))
check('Artikel in Sitemap', f'{BASE}/{SLUG}.html' in sm)
locs = sm.count('<loc>')
check(f'Sitemap <loc> >= 37', locs >= 37, str(locs))

code_rss, rss = fetch('/rss.xml')
check('RSS HTTP 200', code_rss == 200, str(code_rss))
items = rss.count('<item>')
check('RSS 30 Items', items == 30, str(items))
check('Artikel in RSS', SLUG in rss)

code_ll, ll = fetch('/llms.txt')
check('llms.txt HTTP 200', code_ll == 200, str(code_ll))
check('Artikel in llms.txt', SLUG in ll)

code_h, home = fetch('/')
check('Homepage HTTP 200', code_h == 200, str(code_h))
check('Homepage listet Artikel', SLUG in home)
check('Homepage robots index,follow', re.search(r'name="robots" content="index,? ?follow"', home) is not None)

print()
print(f"{N - len(FAIL)}/{N} PASS" + ("  — ALL PASS" if not FAIL else f"  — {len(FAIL)} FAILS"))
import sys
sys.exit(1 if FAIL else 0)
