#!/usr/bin/env python3
"""Mobile-Check 23.11.2026: 3 geänderte Artikel bei 390 px — Overflow 0 + der 2027-Satz im Viewport-Text."""
import pathlib
import re
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "research/evidence/hilfsmittel-zuzahl-231126"
OUT.mkdir(parents=True, exist_ok=True)
SLUGS = ["hilfsmittel-dusch-wc-uebernahme", "hilfsmittel-pflegekasse-uebernahme", "rollator-auswahl-passform-kosten"]

fails = []
with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 390, "height": 844})
    for slug in SLUGS:
        page.goto((ROOT / f"dist/{slug}.html").as_uri())
        page.wait_for_load_state("load")
        page.wait_for_timeout(300)
        m = page.evaluate("""() => {
          const d = document.documentElement;
          return { overflow: Math.max(d.scrollWidth, document.body.scrollWidth) - d.clientWidth };
        }""")
        body = page.evaluate("() => document.body.innerText")
        ok_2027 = ("1. Januar 2027" in body) and ("7,50" in body)
        shot = OUT / f"mobile-390-{slug}.png"
        page.screenshot(path=str(shot), full_page=False)
        print(slug, "overflow:", m["overflow"], "| 2027-Satz sichtbar:", ok_2027, "| shot:", shot.name)
        if m["overflow"] != 0:
            fails.append((slug, "overflow", m["overflow"]))
        if not ok_2027:
            fails.append((slug, "2027-satz"))
print("FAILS:", len(fails))
raise SystemExit(1 if fails else 0)
