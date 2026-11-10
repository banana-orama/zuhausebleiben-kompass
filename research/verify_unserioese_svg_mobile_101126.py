#!/usr/bin/env python3
"""Sichtkontrolle treppenlift-unserioese-anbieter-warntafel.svg + Mobile-Check der Artikel-Seite:
1) Text-BBox-Overflow-Check gegen viewBox (echte Chromium-Messung)
2) Element-auf-Element-Überlappung der Textzeilen (Pairwise-Overlap)
3) Chip-Kontext-Check: Textboxen dürfen Chip-Rechtecke nicht horizontal verlassen
4) Screenshot SVG + Mobile-390px-Overflow der built Seite (LAUNCH-dist)
Muster: verify_angehoerige_svg_mobile_101126.py."""
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
SVG = ROOT / 'assets/images/treppenlift-unserioese-anbieter-warntafel.svg'
PAGE = ROOT / 'dist/treppenlift-unserioese-anbieter.html'
OUT = ROOT / 'research/evidence/unserioese-101126'
OUT.mkdir(parents=True, exist_ok=True)

fails = []
with sync_playwright() as p:
    b = p.chromium.launch()
    # 1+2+3: SVG-Geometrie
    page = b.new_page(viewport={'width': 980, 'height': 880})
    page.goto(SVG.as_uri())
    page.wait_for_timeout(400)
    issues = page.evaluate(
        """() => {
        const svg = document.querySelector('svg');
        const vb = svg.viewBox.baseVal;
        const issues = [];
        const boxes = [];
        const rects = [];
        for (const r of svg.querySelectorAll('rect.chip')) {
          const bb = r.getBBox();
          rects.push({x: bb.x, y: bb.y, r: bb.x + bb.width, bot: bb.y + bb.height});
        }
        for (const t of svg.querySelectorAll('text')) {
          const bb = t.getBBox();
          boxes.push({el: t.textContent.slice(0, 50), x: bb.x, y: bb.y, r: bb.x + bb.width, bot: bb.y + bb.height});
          if (bb.x < 0 || bb.y < 0 || bb.x + bb.width > vb.width || bb.y + bb.height > vb.height) {
            issues.push({type: 'out-of-canvas', el: t.textContent.slice(0, 50), r: bb.x + bb.width, bot: bb.y + bb.height});
          }
          for (const rc of rects) {
            if (bb.y >= rc.y - 4 && bb.y + bb.height <= rc.bot + 4 && bb.x >= rc.x - 4 && bb.x < rc.x + rc.width) {
              if (bb.x + bb.width > rc.r + 6) {
                issues.push({type: 'chip-overflow', el: t.textContent.slice(0, 40), r: Math.round(bb.x + bb.width), chipR: Math.round(rc.r)});
              }
            }
          }
        }
        for (let i = 0; i < boxes.length; i++) {
          for (let j = i + 1; j < boxes.length; j++) {
            const a = boxes[i], c = boxes[j];
            const ox = Math.min(a.r, c.r) - Math.max(a.x, c.x);
            const oy = Math.min(a.bot, c.bot) - Math.max(a.y, c.y);
            if (ox > 2 && oy > 2) issues.push({type: 'text-overlap', a: a.el, b: c.el, ox, oy});
          }
        }
        return issues;
        }""")
    for i in issues:
        fails.append(f"SVG {i['type']}: {i}")
    print(f"SVG geometry issues: {len(issues)}")
    page.locator('svg').screenshot(path=str(OUT / 'svg-screenshot.png'), timeout=15000)
    page.close()

    # 4: Mobile 390px — horizontaler Overflow der Artikel-Seite (LAUNCH-dist!)
    mp = b.new_page(viewport={'width': 390, 'height': 844})
    mp.goto(PAGE.as_uri())
    mp.wait_for_timeout(600)
    overflow = mp.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
    print(f"mobile 390px overflow px: {overflow}")
    if overflow > 0:
        fails.append(f"mobile overflow {overflow}px")
    mp.close()
    b.close()

print("ALL PASS" if not fails else "FAILS: " + str(fails))
import sys
sys.exit(1 if fails else 0)
