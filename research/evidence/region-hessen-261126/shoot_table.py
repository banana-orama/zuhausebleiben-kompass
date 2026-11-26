import pathlib
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path.cwd()
PAGE = ROOT / 'dist/region/hessen.html'
with sync_playwright() as p:
    b = p.chromium.launch()
    d = b.new_page(viewport={'width': 900, 'height': 1100})
    d.goto(PAGE.as_uri())
    d.wait_for_load_state('load')
    d.wait_for_timeout(300)
    tbl = d.locator('.table-scroll').nth(1)
    tbl.screenshot(path=str(ROOT / 'research/evidence/region-hessen-261126/desktop-hoechstbetraege-tabelle2.png'))
    b.close()
print("shot ok")
