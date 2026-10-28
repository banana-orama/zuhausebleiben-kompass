#!/usr/bin/env python3
"""Sichtkontrolle fuer treppenlift-plattformlift-rollstuhllift-weg.svg:
1) Text-BBox-Overflow-Check gegen viewBox (echte Renderer-Messung via Chromium)
2) Box-Kontext-Check (Text muss in seiner eigenen Box bleiben, nicht nur im viewBox)
3) Screenshot fuer visuelle Inspektion
Muster: verify_aussen_svg_271026.py."""
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
SVG = ROOT / 'assets/images/treppenlift-plattformlift-rollstuhllift-weg.svg'
OUT = ROOT / 'research' / 'evidence' / 'plattformlift-281026'
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
    ok = True
    if overflow['issues']:
        ok = False
        print('OVERFLOW ISSUES:')
        for i in overflow['issues']:
            print('  ', i)
    else:
        print('PASS getBBox: 0 Overflows gegen viewBox')

    # Box-Kontext: jeder Text muss in dem rect liegen, dessen y-Band ihn einschliesst (Zeilen-Cards + Preis-Boxen)
    ctx = page.evaluate(
        """() => {
        const svg = document.querySelector('svg');
        const rects = [...svg.querySelectorAll('rect')].map(r => ({x: r.x.baseVal.value, y: r.y.baseVal.value, w: r.width.baseVal.value, h: r.height.baseVal.value}));
        const issues = [];
        for (const t of svg.querySelectorAll('text')) {
          const b = t.getBBox();
          // finde die kleinsten rect, das den Textursprung (x) vertikal einschliesst und horizontal beginnt vor dem Text
          const cand = rects.filter(r => b.y >= r.y && b.y + b.height <= r.y + r.h && b.x >= r.x && r.w > 40);
          if (!cand.length) continue;
          const r = cand.sort((a, z) => a.w - z.w)[0];
          if (b.x + b.width > r.x + r.w - 2) {
            issues.push({text: t.textContent.slice(0, 50), right: Math.round(b.x + b.width), boxRight: r.x + r.w});
          }
        }
        return issues;
      }"""
    )
    if ctx:
        ok = False
        print('BOX-KONTEXT ISSUES (Text laeuft ueber die Box hinaus):')
        for i in ctx:
            print('  ', i)
    else:
        print('PASS Box-Kontext: alle Texte bleiben in ihren Boxen')

    page.screenshot(path=str(SHOT))
    print('Screenshot:', SHOT)
    b.close()
    if not ok:
        raise SystemExit(1)
    print('ALL PASS')
