#!/usr/bin/env python3
"""Mobile-Check zuschuss-refresh 18.11.2026: 390px Overflow = 0, Status-Tabelle im
Scroll-Container, Screenshot der neuen Sektion für die Sichtkontrolle (LAUNCH-dist)."""
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / 'dist/treppenlift-zuschuss.html'
OUT = ROOT / 'research/evidence/zuschuss-refresh-181126'
OUT.mkdir(parents=True, exist_ok=True)

fails = []
with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={'width': 390, 'height': 844})
    page.goto(PAGE.as_uri())
    page.wait_for_load_state('load')
    page.wait_for_timeout(400)
    m = page.evaluate("""() => {
      const d = document.documentElement;
      const overflow = Math.max(d.scrollWidth, document.body.scrollWidth) - d.clientWidth;
      const sec = document.getElementById('abschnitt-2');
      const scroll = sec ? sec.querySelector('.table-scroll') : null;
      const links = [...document.querySelectorAll('a[href*="/region/"]')].map(a => a.getAttribute('href'));
      const rect = scroll ? scroll.getBoundingClientRect() : null;
      return {
        overflow,
        hasSec: !!sec,
        hasScroll: !!scroll,
        scrollW: rect ? rect.width : 0,
        links,
        heading: sec ? sec.querySelector('h2')?.textContent : null
      };
    }""")
    if m['overflow'] != 0:
        fails.append(('overflow-390', m['overflow']))
    if not m['hasSec'] or not m['hasScroll']:
        fails.append(('status-section-missing', m['hasSec'], m['hasScroll']))
    if m['scrollW'] and m['scrollW'] > 390 + 1:
        fails.append(('scroll-width', m['scrollW']))
    for href in ['https://zuhausebleiben-kompass.de/region/nordrhein-westfalen.html',
                 'https://zuhausebleiben-kompass.de/region/bayern.html']:
        if href not in m['links']:
            fails.append(('link-missing-mobile', href))
    # Screenshot der Status-Sektion (Desktop-Breite für die Lesbarkeit)
    d = b.new_page(viewport={'width': 900, 'height': 900})
    d.goto(PAGE.as_uri())
    d.wait_for_load_state('load')
    d.wait_for_timeout(300)
    d.locator('#abschnitt-2').screenshot(path=str(OUT / 'status-table-screenshot.png'))
    b.close()

print('MOBILE:', 'PASS' if not fails else f'FAIL {fails}')
print('heading:', m['heading'])
print('links:', len(m['links']))
exit(1 if fails else 0)
