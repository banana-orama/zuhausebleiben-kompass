#!/usr/bin/env python3
"""Screenshot des SVG (Playwright, device scale 1)."""
import subprocess
JS = r'''
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 820, height: 660 } });
  await page.goto('file:///Users/mac/agentic-business/barrierefrei-leads/assets/images/krankenhaus-entlassung-wegweiser.svg');
  await page.screenshot({ path: '/Users/mac/.hermes/profiles/milo/cache/scratch/kh-svg-121126.png', fullPage: false });
  await browser.close();
})();
'''
out = subprocess.run(['node', '-e', JS], capture_output=True, text=True, cwd='/Users/mac/agentic-business/barrierefrei-leads')
print('shot ok' if out.returncode == 0 else 'ERR ' + out.stderr[:300])
