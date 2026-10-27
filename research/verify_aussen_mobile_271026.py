#!/usr/bin/env python3
"""Mobile-Check 390 px fuer den neuen Artikel treppenlift-aussentreppen-aussenlift:
kein horizontaler Overflow, Checklisten-Anchor erreichbar, SVG sichtbar.
Muster: verify_nutzlast_mobile_271026.py."""
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
URL = (ROOT / 'dist' / 'treppenlift-aussentreppen-aussenlift.html').as_uri()

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={'width': 390, 'height': 844})
    page.goto(URL)
    page.wait_for_timeout(500)
    overflow = page.evaluate(
        "() => ({doc: document.documentElement.scrollWidth, win: window.innerWidth,"
        " body: document.body.scrollWidth})")
    print('scrollWidth 390px viewport:', overflow)
    ok = overflow['doc'] <= 390 and overflow['body'] <= 390
    print('0 px horizontaler Overflow' if ok else 'OVERFLOW GEFUNDEN')
    # Checklisten-Anchor
    page.goto(URL + '#abschnitt-10')
    page.wait_for_timeout(300)
    anchor = page.evaluate("() => {const el = document.getElementById('abschnitt-10'); return el ? el.querySelector('h2').textContent : null}")
    print('anchor abschnitt-10:', anchor)
    # SVG im Fluss
    img = page.evaluate("() => {const i = document.querySelector('figure img'); return i ? {src: i.getAttribute('src').split('/').pop(), w: i.clientWidth} : null}")
    print('figure img:', img)
    # Early CTA
    cta = page.evaluate("() => {const a = document.querySelector('[data-cta-id=compare_top]'); return a ? {text: a.textContent.trim(), href: a.getAttribute('href')} : null}")
    print('early CTA:', cta)
    b.close()
print('OK' if ok else 'FAIL')
