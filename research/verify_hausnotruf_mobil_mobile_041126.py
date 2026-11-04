#!/usr/bin/env python3
"""Mobile-Check fuer hausnotruf-mobil-gps-unterwegs (04.11.2026): 390-px-Viewport,
kein horizontaler Overflow, SVG sichtbar skaliert, CTAs mit Touch-Groesse.
Muster: verify_wohnumfeld_mobile_021126.py."""
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
FILE = (ROOT / 'dist' / 'hausnotruf-mobil-gps-unterwegs.html').as_uri()
FAIL = []

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={'width': 390, 'height': 844})
    page.goto(FILE)
    page.wait_for_timeout(400)
    overflow = page.evaluate(
        "() => ({sw: document.documentElement.scrollWidth, iw: window.innerWidth,"
        " svgW: (document.querySelector('figure img, figure svg')||{}).getBoundingClientRect?document.querySelector('figure img, figure svg').getBoundingClientRect().width:null})")
    ok_overflow = overflow['sw'] <= overflow['iw'] + 1
    print(f"PASS overflow 390px: scrollWidth {overflow['sw']} <= innerWidth {overflow['iw']}" if ok_overflow
          else f"FAIL overflow 390px: scrollWidth {overflow['sw']} > innerWidth {overflow['iw']}")
    if not ok_overflow:
        FAIL.append('overflow')
    svg_w = overflow.get('svgW')
    svg_ok = svg_w is not None and 300 <= svg_w <= 391
    print(f"{'PASS' if svg_ok else 'FAIL'} SVG-Breite im Mobile-Layout: {svg_w}")
    if not svg_ok:
        FAIL.append('svg-width')
    buttons = page.evaluate(
        "() => [...document.querySelectorAll('.reader-actions a, .reader-actions button')]"
        ".map(el => {const r = el.getBoundingClientRect(); return {h: Math.round(r.height), t: el.textContent.trim().slice(0,30)};})")
    for btn in buttons:
        ok_b = btn['h'] >= 40
        print(f"{'PASS' if ok_b else 'FAIL'} CTA-Hoehe {btn['h']}px  «{btn['t']}»")
        if not ok_b:
            FAIL.append('cta-size')
    page.screenshot(path=str(ROOT / 'research/evidence/hausnotruf-mobil-041126/mobile-390.png'), full_page=False)
    b.close()

print()
if FAIL:
    print(f"ERGEBNIS: FAIL {FAIL}")
    raise SystemExit(1)
print("ERGEBNIS: ALL PASS")
