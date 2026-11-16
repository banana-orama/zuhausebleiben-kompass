#!/usr/bin/env python3
"""Mobile-Check 390 px fuer region/bayern.html (LAUNCH-dist):
0 px horizontales Overflow, Tabelle scrollt im Container, FAQ toggelt.
Muster: verify_wohnumfeld_mobile_021126.py."""
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIST = ROOT / 'dist'
PAGE = DIST / 'region' / 'bayern.html'
SHOT = ROOT / 'research' / 'evidence' / 'region-bayern-161126' / 'mobile-390-bayern.png'

fails = []
with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={'width': 390, 'height': 844})
    page.goto(PAGE.as_uri())
    page.wait_for_timeout(400)
    overflow = page.evaluate(
        "() => Math.max(document.documentElement.scrollWidth, document.body.scrollWidth) - document.documentElement.clientWidth")
    print('horizontales Overflow:', overflow, 'px')
    if overflow > 0:
        fails.append(f'overflow {overflow}px')
    # Überblick-Tabelle im scroll-Container?
    tbl = page.evaluate(
        """() => { const w = document.querySelector('.table-scroll');
             if (!w) return null; return {ow: w.scrollWidth, cw: w.clientWidth, scrollable: w.scrollWidth >= w.clientWidth}; }""")
    print('Tabelle scroll-Container:', tbl)
    if not tbl or not tbl['scrollable']:
        fails.append('overview table not scrollable')
    # FAQ toggelt
    page.locator('details summary').first.click()
    page.wait_for_timeout(200)
    open_now = page.evaluate("() => document.querySelector('details').open")
    print('FAQ toggelt:', open_now)
    if not open_now:
        fails.append('faq does not toggle')
    page.screenshot(path=str(SHOT), full_page=False)
    print('Screenshot:', SHOT)
if fails:
    print('FAILS:', fails)
    raise SystemExit(1)
print('MOBILE 390px ALL PASS')
