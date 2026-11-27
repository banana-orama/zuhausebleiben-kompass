#!/usr/bin/env python3
"""Screenshot der Tabellen-Elemente (MV, LAUNCH-dist) für die Vision-Kontrolle."""
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / 'dist/region/mecklenburg-vorpommern.html'
OUT = ROOT / 'research/evidence/region-mv-271126'

with sync_playwright() as p:
    b = p.chromium.launch()
    d = b.new_page(viewport={'width': 900, 'height': 1100})
    d.goto(PAGE.as_uri())
    d.wait_for_load_state('load')
    d.wait_for_timeout(300)
    tabs = d.locator('.table-scroll')
    tabs.nth(0).screenshot(path=str(OUT / 'desktop-wege-tabelle.png'))
    tabs.nth(1).screenshot(path=str(OUT / 'desktop-konditionen-tabelle.png'))
    b.close()
print('saved:', OUT / 'desktop-wege-tabelle.png', 'und', OUT / 'desktop-konditionen-tabelle.png')
