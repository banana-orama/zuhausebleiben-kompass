#!/usr/bin/env python3
"""Live-Readback Briefing 15 (02.11.2026) gegen die OEFFENTLICHE URL:
Artikel-Seite, robots, Kernzahlen, CTAs, SVG-Asset, Related-Ziele, Home, Sitemap 37 locs,
RSS 26 Items, llms.txt. Muster: verify_live_readback_plattformlift_281026.py."""
import re
import sys
import urllib.request

BASE = 'https://zuhausebleiben-kompass.de'
URL = f'{BASE}/wohnumfeldverbesserung-beantragen.html'
FAIL = []


def fetch(url, binary=False):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (readback-check)'})
    with urllib.request.urlopen(req, timeout=45) as r:
        data = r.read()
        return (r.status, data if binary else data.decode('utf-8', errors='replace'))


def check(name, ok, ctx=''):
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  [{ctx}]" if ctx else ''))
    if not ok:
        FAIL.append(name)


code, html = fetch(URL)
check('Artikel-URL HTTP 200', code == 200, str(code))
check('robots index,follow', 'name="robots" content="index,follow"' in html)
check('Title', '<title>Wohnumfeld-Zuschuss beantragen — ZuhauseBleiben Kompass</title>' in html)
check('H1', 'Zuschuss für wohnumfeldverbessernde Maßnahmen beantragen' in html)
check('kein ENTWURF/noindex', 'noindex' not in html and 'ENTWURF' not in html)

plain = re.sub(r'<sup class="cite">.*?</sup>', '', html, flags=re.S)
plain = re.sub(r'<[^>]+>', ' ', plain)
plain = re.sub(r'\s+', ' ', plain).lower()
for needle in ['4.180 euro je maßnahme', '16.720 euro', 'drei wochen', 'fünf wochen',
               'pflegegrade 1 bis 5', 'als genehmigt', 'vor dem umbau', '5.220 euro', '2.090 euro']:
    check(f'Kernzahl "{needle}"', needle in plain)

check('Checklisten-Anker', 'href="#abschnitt-6"' in html)
check('CTA Förderlandschaft', 'Förderlandschaft im Überblick' in html and 'data-cta-id="compare_top"' in html)
check('print_bottom', 'data-cta-id="print_bottom"' in html)
check('editorial_contact', 'data-cta-id="editorial_contact"' in html)
check('Quellenstand 2026-11-02', 'geprüft 2026-11-02' in html)
check('Alle 10 Quellen-URLs', all(u in html.replace('&amp;', '&') or u.replace('&', '&amp;') in html
                                 for u in ['gesetze-im-internet.de/sgb_11/__40.html',
                                           'bundesgesundheitsministerium.de/pflege-zu-hause/zuschuesse-zur-wohnungsanpassung',
                                           'verbraucherzentrale.de/sites/default/files/2021-09/wohnumfeldverbessernde_massnahmen_bevollmaechtigter.pdf',
                                           'meine-pflegekasse.de/fileadmin/Dokumente/Formulare/Pflege/antrag-pflege-wohnumfeldmassnahme-mkk.pdf',
                                           'gkv-spitzenverband.de/media/dokumente/krankenversicherung_1/hilfsmittel/fortschreibungen_aktuell/12_2025/2025_12_11_Produktgruppe_33_Toilettenhilfen.pdf',
                                           'rehadat-gkv.de/produkt/index.html',
                                           'pflege.de/pflegekasse-pflegefinanzierung/pflegeleistungen/wohnraumanpassung/',
                                           'dak.de/dak/ihr-anliegen/pflege/wohnraumanpassung/',
                                           'aok.de/pk/pflegeleistungen/wohnraumanpassungen-und-barrierefreiheit/',
                                           'verwaltung.bund.de/leistungsverzeichnis/de/leistung/99106013080001']))
check('Related 3 Ziele', html.count('Passend dazu') == 1 and
      all(s in html for s in ['hilfsmittel-pflegekasse-uebernahme.html', 'pflegegrad-antrag-ablauf-fristen.html',
                              'beleuchtung-orientierung-im-alter.html']))
check('kein Partner-Marker', 'data-partner-placement' not in html and 'rel="sponsored' not in html)

code_svg, _ = fetch(f'{BASE}/assets/images/wohnumfeld-antrag-wegweiser.svg', binary=True)
check('SVG-Asset 200', code_svg == 200, str(code_svg))

for target in ['/treppenlift-zuschuss.html', '/hilfsmittel-pflegekasse-uebernahme.html',
               '/pflegegrad-antrag-ablauf-fristen.html', '/beleuchtung-orientierung-im-alter.html']:
    c, _ = fetch(BASE + target)
    check(f'Related/CTA-Ziel {target} 200', c == 200, str(c))

code_h, home = fetch(BASE + '/')
check('Homepage 200 + listet Artikel', code_h == 200 and 'wohnumfeldverbesserung-beantragen' in home)

code_s, sm = fetch(BASE + '/sitemap.xml')
locs = re.findall(r'<loc>([^<]+)</loc>', sm)
check('Sitemap 200, 37 locs', code_s == 200 and len(locs) == 37, str(len(locs)))
check('Sitemap enthält Artikel', any('wohnumfeldverbesserung-beantragen' in u for u in locs))
check('Sitemap ohne Region', not any('/region/' in u for u in locs))

code_r, rss = fetch(BASE + '/rss.xml')
items = rss.count('<item>')
check('RSS 200, 26 Items', code_r == 200 and items == 26, str(items))
check('RSS enthält Artikel', 'wohnumfeldverbesserung-beantragen' in rss)

code_l, llms = fetch(BASE + '/llms.txt')
check('llms.txt 200 + Artikel', code_l == 200 and 'wohnumfeldverbesserung-beantragen' in llms)

print()
if FAIL:
    print(f"ERGEBNIS: {len(FAIL)} FAIL: {FAIL}")
    sys.exit(1)
print("ERGEBNIS: ALL PASS")
