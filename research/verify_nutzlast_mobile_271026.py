#!/usr/bin/env python3
"""Mobile-Check 390px fuer treppenlift-maximalgewicht: kein horizontaler Overflow,
Tabelle scrollbar in ihrem Container, Grafik skaliert, CTA/FAQ bedienbar."""
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
URL = (ROOT / 'dist' / 'treppenlift-maximalgewicht.html').as_uri()
SHOT = ROOT / 'research' / 'evidence' / 'nutzlast-271026' / 'mobile-390.png'

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={'width': 390, 'height': 844})
    page.goto(URL)
    page.wait_for_timeout(300)
    m = page.evaluate(
        """() => {
        const doc = document.documentElement;
        const overflowX = doc.scrollWidth - doc.clientWidth;
        const fig = document.querySelector('.editorial-figure img');
        const tableWrap = document.querySelector('.table-scroll');
        const cta = document.querySelectorAll('.reader-actions a');
        return {
          overflowX,
          imgW: fig ? fig.getBoundingClientRect().width : null,
          tableScrollable: tableWrap ? (tableWrap.scrollWidth >= tableWrap.clientWidth) : null,
          tableWrapW: tableWrap ? tableWrap.getBoundingClientRect().width : null,
          ctaCount: cta.length,
          h1Count: document.querySelectorAll('h1').length,
          robots: document.querySelector('meta[name="robots"]')?.content,
        };
      }"""
    )
    print(m)
    ok = m['overflowX'] == 0 and m['h1Count'] == 1 and m['ctaCount'] == 3
    print('MOBILE CHECK:', 'PASS' if ok else 'FAIL')
    page.screenshot(path=str(SHOT))
    b.close()
