#!/usr/bin/env python3
"""Mobile-Check 390px für hausnotruf-alarm-ablauf (Briefing 26)."""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / "dist" / "hausnotruf-alarm-ablauf.html"
SHOT = ROOT / "research" / "evidence" / "alarm-131126" / "mobile-390-artikel.png"

from playwright.sync_api import sync_playwright

fails = []
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 390, "height": 844})
    pg.goto(PAGE.as_uri())
    pg.wait_for_load_state("load")
    sw = pg.evaluate("() => Math.max(document.documentElement.scrollWidth, document.body.scrollWidth)")
    print(f"scrollWidth @390px: {sw}px -> {'PASS' if sw <= 392 else 'FAIL'}")
    if sw > 392:
        fails.append("overflow")
    pg.screenshot(path=str(SHOT), full_page=False)
    print(f"Screenshot: {SHOT}")
sys.exit(1 if fails else 0)
