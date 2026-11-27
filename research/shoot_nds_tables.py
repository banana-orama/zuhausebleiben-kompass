#!/usr/bin/env python3
"""Tabellen-Screenshots der NDS-Region-Seite (Desktop 900px, LAUNCH-dist)."""
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / 'dist/region/niedersachsen.html'
OUT = ROOT / 'research/evidence/region-nds-271126'
OUT.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    b = p.chromium.launch()
    d = b.new_page(viewport={'width': 900, 'height': 1200})
    d.goto(PAGE.as_uri())
    d.wait_for_load_state('load')
    d.wait_for_timeout(300)
    tabs = d.locator('.table-scroll')
    print('tables found:', tabs.count())
    tabs.nth(0).screenshot(path=str(OUT / 'desktop-wege-tabelle.png'))
    tabs.nth(1).screenshot(path=str(OUT / 'desktop-konditionen-tabelle.png'))
    b.close()
print('saved:', OUT / 'desktop-wege-tabelle.png', '+', OUT / 'desktop-konditionen-tabelle.png')
