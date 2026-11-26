#!/usr/bin/env python3
"""Mobile-Check Region Hessen 26.11.2026: 390px Overflow = 0, Tabellen im
Scroll-Container, CTA-/FAQ-/Quellen-/Related-Zähler, Screenshots (LAUNCH-dist)."""
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / 'dist/region/hessen.html'
OUT = ROOT / 'research/evidence/region-hessen-261126'
OUT.mkdir(parents=True, exist_ok=True)

fails = []
with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={'width': 390, 'height': 844})
    page.goto(PAGE.as_uri())
    page.wait_for_load_state('load')
    page.wait_for_timeout(400)
    m = page.evaluate("""() => {
      const d = document.documentElement;
      const overflow = Math.max(d.scrollWidth, document.body.scrollWidth) - d.clientWidth;
      const tables = [...document.querySelectorAll('.table-scroll')];
      const ctas = [...document.querySelectorAll('.next-step a.button')].map(a => a.getAttribute('href'));
      const faqs = [...document.querySelectorAll('details')].length;
      const sources = [...document.querySelectorAll('.sources li')].length;
      const related = [...document.querySelectorAll('.related li a')].map(a => a.getAttribute('href'));
      const summaryVisible = [...document.querySelectorAll('details summary')].every(s => s.getBoundingClientRect().width > 0);
      return {overflow, tables: tables.length,
              tableW: tables.map(t => t.getBoundingClientRect().width),
              ctas, faqs, sources, related, summaryVisible,
              h1: document.querySelector('h1')?.textContent};
    }""")
    if m['overflow'] != 0:
        fails.append(('overflow-390', m['overflow']))
    if m['tables'] != 2:
        fails.append(('tables', m['tables']))
    for w in m['tableW']:
        if w > 390 + 1:
            fails.append(('table-width-390', w))
    for href in ['https://zuhausebleiben-kompass.de/treppenlift-zuschuss.html',
                 'https://zuhausebleiben-kompass.de/wohnumfeldverbesserung-beantragen.html',
                 'https://zuhausebleiben-kompass.de/treppenlift-foerderung-ohne-pflegegrad.html']:
        if href not in m['ctas']:
            fails.append(('cta-missing', href))
    if m['faqs'] != 6:
        fails.append(('faqs', m['faqs']))
    if m['sources'] != 19:
        fails.append(('sources', m['sources']))
    for href in ['https://zuhausebleiben-kompass.de/treppenlift-mietwohnung.html',
                 'https://zuhausebleiben-kompass.de/treppenlift-kosten.html']:
        if href not in m['related']:
            fails.append(('related-missing', href))
    if not m['summaryVisible']:
        fails.append(('faq-summary-invisible',))
    # Screenshots: oben (Hero/Lede) + Höchstbeträge-Tabelle (Desktop-Breite für Lesbarkeit)
    page.screenshot(path=str(OUT / 'mobile-390-top.png'))
    d = b.new_page(viewport={'width': 900, 'height': 1100})
    d.goto(PAGE.as_uri())
    d.wait_for_load_state('load')
    d.wait_for_timeout(300)
    sec = d.locator('#abschnitt-3')
    sec.screenshot(path=str(OUT / 'desktop-hoechstbetraege-tabelle.png'))
    b.close()

print('measured:', m)
if fails:
    print('FAILS:', fails)
    raise SystemExit(1)
print('ALL PASS (overflow 0 @390px, 2 Tabellen im Scroll-Muster, 3 CTAs, 6 FAQs, 19 Quellen, Related vollständig)')
