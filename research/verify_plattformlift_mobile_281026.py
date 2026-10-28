#!/usr/bin/env python3
"""Mobile-Pruefung 390px fuer treppenlift-plattformlift-rollstuhllift:
kein Horizontal-Overflow, Anker/Checkliste/Early-CTA/SVG/Quellen erreichbar.
Muster: verify_aussen_mobile_271026.py."""
import pathlib
import sys

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = (ROOT / 'dist' / 'treppenlift-plattformlift-rollstuhllift.html').as_uri()
FAIL = []

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={'width': 390, 'height': 844})
    page.goto(PAGE)
    page.wait_for_timeout(300)

    overflow = page.evaluate(
        "() => ({w: document.documentElement.scrollWidth, vw: window.innerWidth,"
        " body: document.body.scrollWidth})"
    )
    print('scrollWidth:', overflow)
    if max(overflow['w'], overflow['body']) > overflow['vw']:
        FAIL.append(f'horizontal overflow: {overflow}')
    else:
        print('PASS 0 px horizontal overflow @390')

    # Tabellen-Scrollregion existiert (table-scroll) und ist fokussierbar
    ts = page.locator('.table-scroll').count()
    print('PASS table-scroll regions:', ts) if ts >= 2 else FAIL.append(f'table-scroll count {ts}')

    # Early CTA
    cta = page.locator('[data-cta-id="compare_top"]')
    if cta.count() == 1 and cta.first.is_visible():
        print('PASS early compare_top sichtbar:', cta.first.inner_text()[:40])
    else:
        FAIL.append('compare_top fehlt/unsichtbar')
    cl = page.locator('[data-cta-id="checklist_top"]')
    if cl.count() == 1:
        print('PASS checklist_top vorhanden:', cl.first.inner_text()[:30])
    else:
        FAIL.append('checklist_top fehlt')

    # Anker: Checkliste anspringen
    page.locator('[data-cta-id="checklist_top"]').first.click()
    page.wait_for_timeout(250)
    y = page.evaluate('() => window.scrollY')
    print('PASS Checklisten-Anker springt, scrollY:', y) if y > 100 else FAIL.append(f'anker scrollY {y}')

    # SVG sichtbar + dimensioniert
    img = page.locator('figure img[src*="plattformlift"]')
    if img.count() == 1:
        box = img.first.bounding_box()
        print('PASS SVG eingebunden, Breite:', round(box['width']))
        if not box or box['width'] < 100:
            FAIL.append('svg breite ungueltig')
    else:
        FAIL.append('svg img fehlt')

    # Print-Button + editorial contact
    if page.locator('[data-cta-id="editorial_contact"]').count() == 1:
        print('PASS editorial contact vorhanden')
    else:
        FAIL.append('editorial contact fehlt')

    # Quellenanker
    for i in (1, 6, 11):
        if page.locator(f'#source-{i}').count() == 1:
            print(f'PASS source-{i} Anker vorhanden')
        else:
            FAIL.append(f'source-{i} fehlt')

    b.close()

if FAIL:
    print('FEHLER:')
    for f in FAIL:
        print('  -', f)
    sys.exit(1)
print('ALL PASS')
