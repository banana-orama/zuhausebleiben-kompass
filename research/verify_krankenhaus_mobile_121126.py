#!/usr/bin/env python3
"""Mobile-Check 390 px: kein horizontaler Overflow auf dem neuen Artikel (LAUNCH-dist)."""
import subprocess
JS = r'''
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
  await page.goto('file:///Users/mac/agentic-business/barrierefrei-leads/dist/wohnung-anpassen-nach-krankenhausentlassung.html');
  await page.waitForTimeout(400);
  const res = await page.evaluate(() => {
    const doc = document.documentElement;
    const overflow = Math.max(doc.scrollWidth - window.innerWidth, 0);
    const h2s = [...document.querySelectorAll('h2')].map(h => h.textContent.trim());
    const svg = !!document.querySelector('figure img[src*="krankenhaus-entlassung-wegweiser"]');
    const imgW = svg ? document.querySelector('figure img[src*="krankenhaus"]').getBoundingClientRect().width : 0;
    return { overflow, articleH2: h2s.length, svgLoaded: svg, imgW: Math.round(imgW) };
  });
  console.log(JSON.stringify(res));
  await browser.close();
})();
'''
out = subprocess.run(['node', '-e', JS], capture_output=True, text=True, cwd='/Users/mac/agentic-business/barrierefrei-leads')
print(out.stdout.strip())
if out.stderr:
    print('STDERR:', out.stderr[:300])
import json, sys
r = json.loads(out.stdout)
ok = r['overflow'] == 0 and r['svgLoaded'] and r['imgW'] > 0
print('RESULT:', 'PASS' if ok else 'FAIL', f"(overflow {r['overflow']} px, H2 {r['articleH2']}, SVG width {r['imgW']} px)")
sys.exit(0 if ok else 1)
