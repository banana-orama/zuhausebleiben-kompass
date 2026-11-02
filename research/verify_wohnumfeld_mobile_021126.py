#!/usr/bin/env python3
"""Mobile-Check 390 px fuer wohnumfeldverbesserung-beantragen.html:
0 px horizontales Overflow, CTAs sichtbar/klickbar, SVG in die Breite skaliert.
Muster: verify_plattformlift_mobile_281026.py."""
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIST = ROOT / 'dist'
PAGE = DIST / 'wohnumfeldverbesserung-beantragen.html'
SHOT = ROOT / 'research' / 'evidence' / 'wohnumfeld-021126' / 'mobile-390.png'

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
    # SVG skaliert? (lazy-Image: erst hinrollen, dann laden lassen)
    page.locator('figure img').first.scroll_into_view_if_needed()
    page.wait_for_timeout(700)
    img = page.evaluate(
        """() => { const i = document.querySelector('figure img'); const r = i.getBoundingClientRect();
             return {w: r.width, cw: document.documentElement.clientWidth, natural: i.naturalWidth, complete: i.complete}; }""")
    print('SVG-Breite mobil:', img)
    if not (0 < img['w'] <= img['cw']):
        fails.append('SVG-Breite unpassend')
    svg_file = DIST / 'assets' / 'images' / 'wohnumfeld-antrag-wegweiser.svg'
    if img['natural'] < 300 and not svg_file.exists():
        fails.append('SVG weder geladen noch als Datei vorhanden')
    # CTAs vorhanden + klickbar (nth visible)
    for sel, label in [('a[data-cta-id="checklist_top"]', 'checklist_top'),
                       ('a[data-cta-id="compare_top"]', 'compare_top'),
                       ('button[data-cta-id="print_bottom"]', 'print_bottom'),
                       ('a[data-cta-id="editorial_contact"]', 'editorial_contact')]:
        vis = page.locator(sel).first.is_visible()
        print(f'CTA {label} sichtbar:', vis)
        if not vis:
            fails.append(f'CTA {label} nicht sichtbar')
    # Tabelle scrollbar (table-scroll region)
    ts = page.locator('.table-scroll').first.is_visible()
    print('Tabelle in table-scroll:', ts)
    if not ts:
        fails.append('table-scroll fehlt')
    # Checklisten-Anker springt
    page.locator('#abschnitt-6').scroll_into_view_if_needed()
    y = page.evaluate("() => window.scrollY")
    print('Scroll zu #abschnitt-6:', y > 0)
    if y <= 0:
        fails.append('Anker #abschnitt-6 nicht erreichbar')
    page.screenshot(path=str(SHOT))
    b.close()

print('Screenshot:', SHOT)
if fails:
    print('FAILS:', fails)
    raise SystemExit(1)
print('MOBILE 390: ALL PASS')
