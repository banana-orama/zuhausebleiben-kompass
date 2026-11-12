#!/usr/bin/env python3
"""SVG-Geometrie-Gate: getBBox-Overflow + Paarwise-Overlap (ohne Header/Footer) für
krankenhaus-entlassung-wegweiser.svg. Startet Chromium headless via Node (playwright)."""
import subprocess, json, sys

JS = r'''
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 900, height: 800 } });
  await page.goto('file:///Users/mac/agentic-business/barrierefrei-leads/assets/images/krankenhaus-entlassung-wegweiser.svg');
  const res = await page.evaluate(() => {
    const svg = document.querySelector('svg');
    const vb = svg.viewBox.baseVal;
    const items = [...svg.querySelectorAll('text,rect,circle')].filter(el => {
      const cls = el.getAttribute('class') || '';
      return !cls.includes('chip');
    });
    const boxes = items.map(el => {
      let b;
      try { b = el.getBBox(); } catch (e) { return null; }
      return { tag: el.tagName, x: b.x, y: b.y, w: b.width, h: b.height, txt: (el.textContent || '').trim().slice(0, 40) };
    }).filter(Boolean);
    const overflows = boxes.filter(b =>
      b.x < -0.5 || b.y < -0.5 || b.x + b.w > vb.width + 0.5 || b.y + b.h > vb.height + 0.5);
    // Pairwise overlap: nur Text-on-Text und Text-on-Hintergrundbänder ist kritisch;
    // Kreise + ihre Ziffern und Band-Header über dem Band-Rect sind gewollt.
    const texts = boxes.filter(b => b.tag === 'text');
    const overlaps = [];
    for (let i = 0; i < texts.length; i++) {
      for (let j = i + 1; j < texts.length; j++) {
        const a = texts[i], c = texts[j];
        const sep = a.x + a.w < c.x - 0.5 || c.x + c.w < a.x - 0.5 ||
                    a.y + a.h < c.y - 0.5 || c.y + c.h < a.y - 0.5;
        if (!sep) overlaps.push([a.txt, c.txt]);
      }
    }
    return { vb: { w: vb.width, h: vb.height }, n: boxes.length, overflows, overlaps };
  });
  console.log(JSON.stringify(res, null, 1));
  await browser.close();
})();
'''
out = subprocess.run(['node', '-e', JS], capture_output=True, text=True, cwd='/Users/mac/agentic-business/barrierefrei-leads')
print(out.stdout)
if out.stderr:
    print('STDERR:', out.stderr[:400])
res = json.loads(out.stdout)
bad = res['overflows'] or res['overlaps']
print('RESULT:', 'FAIL' if bad else 'PASS', f"({res['n']} Elemente, {len(res['overflows'])} Overflows, {len(res['overlaps'])} Overlaps)")
sys.exit(1 if bad else 0)
