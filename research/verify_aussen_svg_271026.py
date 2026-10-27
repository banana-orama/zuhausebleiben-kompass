#!/usr/bin/env python3
"""Sichtkontrolle fuer treppenlift-aussentreppen-aussenlift-wetterschutz.svg:
1) Text-BBox-Overflow-Check gegen viewBox (echte Renderer-Messung via Chromium)
2) Screenshot fuer visuelle Inspektion
Muster: verify_nutzlast_svg_271026.py."""
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
SVG = ROOT / 'assets/images/treppenlift-aussentreppen-aussenlift-wetterschutz.svg'
OUT = ROOT / 'research' / 'evidence' / 'aussenlift-271026'
OUT.mkdir(parents=True, exist_ok=True)
SHOT = OUT / 'svg-screenshot.png'

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={'width': 980, 'height': 680})
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
        // rect-Elemente ebenfalls pruefen
        for (const t of svg.querySelectorAll('rect[x]')) {
          const b = t.getBBox();
          if (b.x + b.width > vb.width || b.y + b.height > vb.height) {
            issues.push({rect: b.x + ',' + b.y, r: b.x + b.width, bot: b.y + b.height});
          }
        }
        return {issues, vb: vb.width + 'x' + vb.height};
      }"""
    )
    print('viewBox:', overflow['vb'])
    if overflow['issues']:
        print('OVERFLOW ISSUES:')
        for i in overflow['issues']:
            print('  ', i)
    else:
        print('0 viewBox-Overflows')
    page.screenshot(path=str(SHOT), full_page=False)
    b.close()
print('screenshot:', SHOT)
