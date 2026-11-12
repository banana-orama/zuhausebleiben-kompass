#!/usr/bin/env python3
"""Mobile-Check 390 px für treppenlift-aufmass-termin (Briefing 25): 0 px Overflow, SVG passt."""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / "dist" / "treppenlift-aufmass-termin.html"

from playwright.sync_api import sync_playwright

FAIL = []
N = 0


def check(label, cond, detail=""):
    global N
    N += 1
    print(("PASS " if cond else "FAIL ") + label + ("" if cond else f"  {detail}"))
    if not cond:
        FAIL.append(label)


with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 390, "height": 844})
    pg.goto(PAGE.as_uri())
    pg.wait_for_load_state("load")

    m = pg.evaluate(
        """() => ({
        docW: document.documentElement.scrollWidth,
        bodyW: document.body.scrollWidth,
        imgW: (document.querySelector('figure img') || {}).width || null,
        h1Size: getComputedStyle(document.querySelector('h1')).fontSize
    })"""
    )
    check("0 px Overflow (390 px)", m["docW"] <= 390 and m["bodyW"] <= 390, str(m))
    check("SVG-Image skaliert auf Viewport", m["imgW"] is not None and m["imgW"] <= 390, str(m["imgW"]))
    b.close()

print(f"\n{N - len(FAIL)}/{N} Pässe")
if FAIL:
    for f in FAIL:
        print(" -", f)
    sys.exit(1)
print("ALL PASS")
