#!/usr/bin/env python3
"""Sichtkontrolle fuer hausnotruf-mobil-entscheidung.svg:
1) Text-BBox-Overflow-Check gegen viewBox (echte Renderer-Messung via Chromium)
2) Rect-Kontext-Check (hervorgehobenes Band: Texte muessen im Rect bleiben)
3) Screenshot fuer visuelle Inspektion
Muster: verify_wohnumfeld_svg_021126.py."""
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
SVG = ROOT / 'assets/images/hausnotruf-mobil-entscheidung.svg'
OUT = ROOT / 'research' / 'evidence' / 'hausnotruf-mobil-041126'
OUT.mkdir(parents=True, exist_ok=True)
SHOT = OUT / 'svg-screenshot.png'

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={'width': 980, 'height': 760})
    page.goto(SVG.as_uri())
    page.wait_for_timeout(400)
    overflow = page.evaluate(
        """() => {
        const svg = document.querySelector('svg');
        const vb = svg.viewBox.baseVal;
        const issues = [];
        for (const t of svg.querySelectorAll('text')) {
          const b = t.getBBox();
          if (b.x < 0 || b.y < 0 || b.x + b.width > vb.width || b.y + b.height > vb.height) {
            issues.push({text: t.textContent.slice(0, 60), x: b.x, y: b.y, r: b.x + b.width, bot: b.y + b.height});
          }
        }
        for (const t of svg.querySelectorAll('rect[x]')) {
          const b = t.getBBox();
          if (b.x + b.width > vb.width || b.y + b.height > vb.height) {
            issues.push({rect: b.x + ',' + b.y, r: b.x + b.width, bot: b.y + b.height});
          }
        }
        // Box-Kontext: alle Texte, die im hervorgehobenen Band liegen (y 552..632), muessen im Band bleiben
        const band = [...svg.querySelectorAll('rect')].find(r => +r.getAttribute('y') === 552);
        const bx = +band.getAttribute('x'), by = 552, bw = +band.getAttribute('width'), bh = +band.getAttribute('height');
        for (const t of svg.querySelectorAll('text')) {
          const b = t.getBBox();
          const inBand = b.y >= by - 2 && b.y + b.height <= by + bh + 2;
          if (inBand && (b.x < bx || b.x + b.width > bx + bw)) {
            issues.push({bandText: t.textContent.slice(0, 50), r: b.x + b.width, limit: bx + bw});
          }
        }
        // Marker-Kreise muessen vertikal auseinanderliegen (min 78 px Abstand bei r=22)
        const ys = [...svg.querySelectorAll('circle')].map(c => +c.getAttribute('cy'));
        for (let i = 1; i < ys.length; i++) {
          if (ys[i] - ys[i - 1] < 78) issues.push({markerGap: ys[i - 1] + '->' + ys[i]});
        }
        return {issues, vb: vb.width + 'x' + vb.height};
      }"""
    )
    print('viewBox:', overflow['vb'])
    ok = True
    if overflow['issues']:
        ok = False
        print('OVERFLOW ISSUES:')
        for i in overflow['issues']:
            print('  ', i)
    else:
        print('PASS getBBox: 0 Overflows gegen viewBox, Band-Kontext + Marker-Abst\u00e4nde sauber')
    page.screenshot(path=str(SHOT), full_page=False)
    print('Screenshot:', SHOT)
    b.close()
    raise SystemExit(0 if ok else 1)
