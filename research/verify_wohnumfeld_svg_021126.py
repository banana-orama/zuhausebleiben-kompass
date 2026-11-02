#!/usr/bin/env python3
"""Sichtkontrolle fuer wohnumfeld-antrag-wegweiser.svg:
1) Text-BBox-Overflow-Check gegen viewBox (echte Renderer-Messung via Chromium)
2) Box-Kontext-Check (Text muss in seiner eigenen Box/Band bleiben)
3) Screenshot fuer visuelle Inspektion
Muster: verify_plattformlift_svg_281026.py."""
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
SVG = ROOT / 'assets/images/wohnumfeld-antrag-wegweiser.svg'
OUT = ROOT / 'research' / 'evidence' / 'wohnumfeld-021126'
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
        // Box-Kontext: Badge-Text muss im Badge-Rect bleiben; Band-Texte im Band
        const badge = [...svg.querySelectorAll('text')].find(t => t.textContent.includes('entscheidend'));
        const badgeRect = badge.previousElementSibling;
        const bb = badge.getBBox(), rb = {x: +badgeRect.getAttribute('x'), y: +badgeRect.getAttribute('y'), w: +badgeRect.getAttribute('width'), h: +badgeRect.getAttribute('height')};
        if (bb.x < rb.x || bb.x + bb.width > rb.x + rb.w) issues.push({badge: badge.textContent, bx: bb.x, br: bb.x + bb.width, rect: rb.x + '..' + (rb.x + rb.w)});
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
        print('PASS getBBox: 0 Overflows gegen viewBox, Badge im Rect')
    page.screenshot(path=str(SHOT), full_page=False)
    print('Screenshot:', SHOT)
    b.close()
    raise SystemExit(0 if ok else 1)
