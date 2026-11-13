#!/usr/bin/env python3
"""Mobile-Check + Sichtkontrolle der NRW-Region-Seite (LAUNCH-dist):
1) Mobile 390px: kein horizontaler Overflow
2) Tabelle: table-scroll vorhanden (min-width Tabelle scrollt, bricht nicht das Layout)
3) Interaktive Elemente: details/summary, print-button, consent-controls vorhanden
4) Screenshots: Desktop 1280 + Mobile 390 (Evidenz)
Muster: verify_unserioese_svg_mobile_101126.py."""
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / 'dist/region/nordrhein-westfalen.html'
OUT = ROOT / 'research/evidence/region-nrw-131126'
OUT.mkdir(parents=True, exist_ok=True)

fails = []
with sync_playwright() as p:
    b = p.chromium.launch()

    # Mobile 390px
    page = b.new_page(viewport={'width': 390, 'height': 844})
    page.goto(PAGE.as_uri())
    page.wait_for_timeout(500)
    overflow = page.evaluate(
        "() => ({doc: document.documentElement.scrollWidth, vw: window.innerWidth,"
        " body: document.body.scrollWidth})")
    if overflow['doc'] > overflow['vw'] + 1 or overflow['body'] > overflow['vw'] + 1:
        fails.append(f"Mobile 390px Overflow: {overflow}")
    else:
        print(f"Mobile 390px: kein Overflow (doc={overflow['doc']}, vw={overflow['vw']})")
    # Tabelle scrollt in eigenem Container
    ts = page.evaluate(
        "() => {const t=document.querySelector('.table-scroll');"
        " return t? {ok:true, scrollW:t.scrollWidth, clientW:t.clientWidth} : {ok:false}}")
    if not ts.get('ok'):
        fails.append('table-scroll fehlt auf Mobile')
    elif ts['scrollW'] > ts['clientW']:
        print(f"Tabelle im Scroll-Container: scrollW={ts['scrollW']} clientW={ts['clientW']} (scrollt)")
    # Interaktives
    for sel in ['.table-scroll', 'details summary', '.next-step a.button',
                '.related a', '.sources li a', '.print-button',
                '[data-consent-settings]', 'meta[name="robots"][content="index,follow"]']:
        n = page.locator(sel).count()
        if n == 0:
            fails.append(f"Element fehlt: {sel}")
        else:
            print(f"OK {sel}: {n}")
    page.screenshot(path=str(OUT / 'nrw-mobile-390.png'), full_page=False)

    # Desktop 1280
    d = b.new_page(viewport={'width': 1280, 'height': 900})
    d.goto(PAGE.as_uri())
    d.wait_for_timeout(400)
    ov_d = d.evaluate("() => ({doc: document.documentElement.scrollWidth, vw: window.innerWidth})")
    if ov_d['doc'] > ov_d['vw'] + 1:
        fails.append(f"Desktop Overflow: {ov_d}")
    else:
        print(f"Desktop 1280: kein Overflow (doc={ov_d['doc']})")
    # FAQ aufmachen und prüfen
    d.locator('details summary').first.click()
    d.wait_for_timeout(150)
    vis = d.locator('details[open]').count()
    if vis < 1:
        fails.append('FAQ details lässt sich nicht öffnen')
    else:
        print(f"FAQ open: {vis}")
    # Consent-Banner erscheint (idle-deferral)
    d.wait_for_timeout(1600)
    consent = d.locator('.cc-banner, [aria-label*="Einwilligung"], #cm').count()
    print(f"Consent-DOM sichtbar: {consent > 0}")
    d.screenshot(path=str(OUT / 'nrw-desktop-1280.png'), full_page=False)
    b.close()

if fails:
    print("FAIL:", *fails, sep="\n  ")
    raise SystemExit(1)
print("verify_region_nrw_mobile_131126: ALL PASS")
