#!/usr/bin/env python3
"""Screenshot der L-Bank-Konditionen-Tabelle (Abschnitt 3) für die Sichtkontrolle."""
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / 'dist/region/baden-wuerttemberg.html'
OUT = ROOT / 'research/evidence/region-bw-251126'

with sync_playwright() as p:
    b = p.chromium.launch()
    d = b.new_page(viewport={'width': 900, 'height': 1200})
    d.goto(PAGE.as_uri())
    d.wait_for_load_state('load')
    d.wait_for_timeout(300)
    h2 = d.locator('#abschnitt-3')
    # Tabelle = nächstes .table-scroll nach dem H2 innerhalb derselben Section-Struktur
    h2.screenshot(path=str(OUT / 'sec3-h2b.png'))
    tbl = d.locator('.table-scroll').nth(1)
    tbl.screenshot(path=str(OUT / 'sec3-tabelle.png'))
    # Übersichtstabelle (Abschnitt 1) ebenfalls
    d.locator('.table-scroll').first.scroll_into_view_if_needed()
    b.close()
print('saved sec3-tabelle.png')
