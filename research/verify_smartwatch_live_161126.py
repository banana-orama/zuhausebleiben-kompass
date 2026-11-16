#!/usr/bin/env python3
"""Live-Readback für hausnotruf-smartwatch-als-ersatz auf der öffentlichen URL.

Asserts (nach CI + Pages-Deploy; 404 zuerst als Deploy-Lag lesen, dann poll):
robots index,follow · Title/Desc · Kernwortlaute (27 und 40 Euro, 30 bis 80, rund 30 bis 50,
ab bereits 50 Euro, Pflegegrad 1, seit 1. April 2026, 25,50 Euro, 20 bis 25 Euro,
einfacher in der Bedienung, weniger geeignet, ungeeignet) · 2 Lead-Absätze ·
Related-Reihenfolge · Early-CTA (compare_top → kosten-vergleich) · Checklisten-Anker ·
SVG absolut 200 · Sitemap exakt 50 locs inkl. Artikel · RSS 38 Items · Homepage-Link ·
llms.txt-Eintrag · Absenzen live (0× awin1.com/4.180/16.720/data-partner-placement/
rel="sponsored") · Quellen checked_at 2026-11-16.
"""
import sys
import urllib.request

BASE = 'https://zuhausebleiben-kompass.de'
SLUG = 'hausnotruf-smartwatch-als-ersatz'
UA = {'User-Agent': 'Mozilla/5.0 (compatible; live-readback/1.0)'}

FAIL = []
N = 0


def check(label, cond, detail=""):
    global N
    N += 1
    print(("PASS " if cond else "FAIL ") + label + ("" if cond else f"  {detail}"))
    if not cond:
        FAIL.append(label)


def fetch(path):
    req = urllib.request.Request(BASE + path, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, r.read().decode('utf-8', 'replace')


code, html = fetch(f'/{SLUG}.html')
check('Artikel 200', code == 200, str(code))
check('robots index,follow', '<meta name="robots" content="index,follow">' in html)
check('Title korrekt', '<title>Smartwatch oder Handy statt Hausnotruf? — ZuhauseBleiben Kompass</title>' in html)
check('H1 live', 'Smartwatch oder Handy statt Hausnotruf? Was die Quellen sagen' in html)
leads = html.count('<p class="lead">')
check('2 Lead-Absätze', leads == 2, str(leads))

for needle in ['27 und 40 Euro', '30 bis 80 Euro', 'rund 30 bis 50 Euro (oder auch mehr)',
               'ab bereits 50 Euro', 'mehreren hundert Euro', 'Pflegegrad 1',
               'seit 1. April 2026', '25,50 Euro', '20 bis 25 Euro',
               'einfacher in der Bedienung als ein Telefon oder Handy',
               'nicht gezielt auslösen', 'Ungeeignet sind solche Hausnotrufgeräte',
               'Manche Produkte können die Freiheit einschränken',
               'wer nimmt im Notfall ab', 'geprüft 2026-11-16']:
    check(f"live: '{needle[:48]}'", needle in html, 'fehlt')

seg_start = html.find('<section class="related">')
seg_end = html.find('</section>', seg_start)
seg = html[seg_start:seg_end] if seg_start >= 0 else ''
order = ['hausnotruf-kosten-anbieter-vergleich', 'hausnotruf-sturzerkennung-oder-knopf', 'hausnotruf-mobil-gps-unterwegs']
pos = [seg.find(f'/{s}.html') for s in order]
check('Related exakt 3 Ziele', all(p >= 0 for p in pos), str(pos))
check('Related-Reihenfolge', pos == sorted(pos), str(pos))

check('Early-CTA compare_top', 'data-cta-id="compare_top"' in html and '/hausnotruf-kosten-anbieter-vergleich.html' in html)
check('Checklisten-Anker', 'href="#abschnitt-9"' in html and 'Zur Checkliste' in html)
check('Druck-CTA', 'data-cta-id="print_bottom"' in html)

for needle in ['awin1.com', '4.180', '16.720', 'data-partner-placement', 'rel="sponsored"']:
    check(f"live Absenz 0 × '{needle}'", html.count(needle) == 0, str(html.count(needle)))

svg_code, _ = fetch('/assets/images/hausnotruf-smartwatch-entscheidung.svg')
check('SVG 200', svg_code == 200, str(svg_code))
check('SVG absolut referenziert', f'{BASE}/assets/images/hausnotruf-smartwatch-entscheidung.svg' in html)

code_sm, sm = fetch('/sitemap.xml')
locs = sm.count('<loc>')
check(f'Sitemap exakt 50 locs (ist {locs})', code_sm == 200 and locs == 50, str(locs))
check('Artikel in Sitemap', f'{BASE}/{SLUG}.html' in sm)

code_rss, rss = fetch('/rss.xml')
check('RSS 200', code_rss == 200, str(code_rss))
check('RSS 38 Items', rss.count('<item>') == 38, str(rss.count('<item>')))

code_home, home = fetch('/')
check('Homepage 200 + Artikel verlinkt', code_home == 200 and f'/{SLUG}.html' in home, str(code_home))

code_llms, llms = fetch('/llms.txt')
check('llms.txt 200 + Eintrag', code_llms == 200 and SLUG in llms, str(code_llms))

print()
print(f"{N - len(FAIL)}/{N} PASS" + ("  — ALL PASS" if not FAIL else f"  — {len(FAIL)} FAILS"))
sys.exit(1 if FAIL else 0)
