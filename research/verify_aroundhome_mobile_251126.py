#!/usr/bin/env python3
"""Mobile-Check der 5 Aroundhome-platzierten Artikel (390px, LAUNCH-dist).

Overflow = 0 px je Seite; der Partner-CTA ist sichtbar (Box-Breite > 0),
Link rel="sponsored noopener" + data-partner-placement gesetzt; Screenshot
des CTA-Blocks auf badumbau-kosten (Vision-Prüfung folgt separat).
"""
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / 'research/evidence/aroundhome-251126'
OUT.mkdir(parents=True, exist_ok=True)
SLUGS = ['badumbau-angebote-vergleichen', 'bad-umbau-barrierefrei', 'badumbau-kosten',
         'wanne-zur-dusche', 'bodengleiche-dusche-altbau']
fails = []
with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={'width': 390, 'height': 844})
    for slug in SLUGS:
        pg = ROOT / ('dist/' + slug + '.html')
        page.goto(pg.as_uri())
        page.wait_for_load_state('load')
        page.wait_for_timeout(350)
        m = page.evaluate("""() => {
          const d = document.documentElement;
          const overflow = Math.max(d.scrollWidth, document.body.scrollWidth) - d.clientWidth;
          const wrap = document.querySelector('aside[data-partner-placement]');
          let ctaInfo = null;
          if (wrap) {
            const cta = wrap.querySelector('a');
            const r = cta.getBoundingClientRect();
            ctaInfo = {rel: cta.getAttribute('rel'), target: cta.getAttribute('target'),
                       pid: wrap.getAttribute('data-partner-placement'),
                       href: cta.href, w: Math.round(r.width), visible: r.width > 0 && r.height > 0};
          }
          return {overflow, cta: ctaInfo};
        }""")
        if m['overflow'] != 0:
            fails.append(('overflow-390:' + slug, m['overflow']))
        if not m['cta']:
            fails.append(('cta-missing:' + slug,))
        else:
            c = m['cta']
            if c['rel'] != 'sponsored noopener':
                fails.append(('cta-rel:' + slug, c['rel']))
            if c['target'] != '_blank':
                fails.append(('cta-target:' + slug, c['target']))
            if not c['visible']:
                fails.append(('cta-invisible:' + slug,))
            if 'awinmid=68536' not in c['href']:
                fails.append(('cta-href:' + slug, c['href']))
        print(slug, '→ overflow', m['overflow'], '| cta', (m['cta'] or {}).get('pid'), (m['cta'] or {}).get('w'))
        if slug == 'badumbau-kosten':
            el = page.query_selector('aside[data-partner-placement]')
            if el:
                el.screenshot(path=str(OUT / 'cta-mobile-badumbau-kosten-390.png'))
    b.close()
print('')
print('ERGEBNIS: ' + str(len(fails)) + ' FAILS')
for f in fails:
    print('FAIL', f)
raise SystemExit(1 if fails else 0)
