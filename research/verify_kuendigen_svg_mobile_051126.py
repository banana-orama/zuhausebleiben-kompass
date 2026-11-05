#!/usr/bin/env python3
"""Sichtkontrolle hausnotruf-kuendigen-wege.svg + Mobile-Check der Artikel-Seite:
1) Text-BBox-Overflow-Check gegen viewBox (echte Chromium-Messung)
2) Element-auf-Element-Überlappung der Textzeilen (Sichtkontrolle-Ersatz via Geometrie + Screenshot)
3) Screenshot SVG + Mobile-390px-Overflow der built Seite
Muster: verify_wohnumfeld_svg_021126.py; Achtung: getBBox sieht KEIN Text-über-Text —
deshalb zusätzlich Pairwise-Overlap der Text-Rects und visuelle Screenshot-Inspektion."""
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
SVG = ROOT / 'assets/images/hausnotruf-kuendigen-wege.svg'
PAGE = ROOT / 'dist/hausnotruf-kuendigen.html'
OUT = ROOT / 'research/evidence/hausnotruf-kuendigen-051126'
OUT.mkdir(parents=True, exist_ok=True)

fails = []
with sync_playwright() as p:
    b = p.chromium.launch()
    # 1+2: SVG-Geometrie
    page = b.new_page(viewport={'width': 980, 'height': 760})
    page.goto(SVG.as_uri())
    page.wait_for_timeout(400)
    issues = page.evaluate(
        """() => {
        const svg = document.querySelector('svg');
        const vb = svg.viewBox.baseVal;
        const issues = [];
        const boxes = [];
        for (const t of svg.querySelectorAll('text')) {
          const bb = t.getBBox();
          boxes.push({el: t.textContent.slice(0, 50), x: bb.x, y: bb.y, r: bb.x + bb.width, bot: bb.y + bb.height});
          if (bb.x < 0 || bb.y < 0 || bb.x + bb.width > vb.width || bb.y + bb.height > vb.height) {
            issues.push({type: 'out-of-canvas', el: t.textContent.slice(0, 50), r: bb.x + bb.width, bot: bb.y + bb.height});
          }
        }
        // Pairwise-Text-Überlappung (echtes Sichtproblem, das getBBox-vs-viewBox verpasst)
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

    # 3: Mobile 390px — horizontaler Overflow der Artikel-Seite (LAUNCH-dist!)
    mp = b.new_page(viewport={'width': 390, 'height': 844})
    mp.goto(PAGE.as_uri())
    mp.wait_for_timeout(600)
    overflow = mp.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
    if overflow > 0:
        fails.append(f"Mobile 390px horizontaler Overflow: {overflow}px")
    else:
        print(f"Mobile 390px: kein horizontales Overflow ({overflow}px)")
    mp.screenshot(path=str(OUT / 'mobile-390-kuendigen.png'), full_page=False)
    mp.close()
    b.close()

for f in fails:
    print("FAIL", f)
print(f"RESULT: {'ALL PASS' if not fails else f'{len(fails)} FAILS'} — Screenshots: {OUT}/svg-screenshot.png, mobile-390-kuendigen.png")
raise SystemExit(1 if fails else 0)
