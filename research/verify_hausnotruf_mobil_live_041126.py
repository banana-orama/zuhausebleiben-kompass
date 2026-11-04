#!/usr/bin/env python3
"""Live-Readback fuer hausnotruf-mobil-gps-unterwegs auf der oeffentlichen URL (04.11.2026).
Muster: verify_wohnumfeld_live_021126.py."""
import re
import sys
import urllib.request

BASE = 'https://zuhausebleiben-kompass.de'
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
FAIL = []


def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.status, r.read().decode('utf-8', errors='replace')


def check(name, ok, ctx=''):
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  [{ctx}]" if ctx else ''))
    if not ok:
        FAIL.append(name)


code, html = fetch(f'{BASE}/hausnotruf-mobil-gps-unterwegs.html')
check('Artikel-URL HTTP 200', code == 200, str(code))
check('robots index,follow', 'name="robots" content="index,follow"' in html)
check('Title', '<title>Mobiler Hausnotruf: GPS, Akku, Kosten — ZuhauseBleiben Kompass</title>' in html)
check('H1', 'Mobiler Hausnotruf mit GPS: auch unterwegs Hilfe auf Knopfdruck' in html)
check('kein noindex/ENTWURF', 'noindex' not in html and 'ENTWURF' not in html)

plain = re.sub(r'<script[^>]*>.*?</script>', ' ', html, flags=re.S)
plain = re.sub(r'<sup class="cite">.*?</sup>', '', plain, flags=re.S)
plain = re.sub(r'<[^>]+>', ' ', plain)
import html as H
plain = H.unescape(plain)
plain = re.sub(r'\s+', ' ', plain).lower()
for needle in ['30 bis 50 meter', '50 bis 100 meter', 'rund 150 meter', '27 euro', '10 bis 25',
               '30 bis 80 euro', '35 bis 70', '52.40.01', 'zehn prozent, höchstens 25 euro',
               'seit dem 1. april 2026', 'vertragspartner der pflegekasse', 'bis zu 72 stunden',
               'rund 1 bis 7 tage', 'drei bzw. fünf wochen']:
    check(f'Kernzahl "{needle}"', needle in plain)

check('Checklisten-Anker #abschnitt-11', 'href="#abschnitt-11"' in html)
check('CTA Kosten & Anbieter', ('Kosten &amp; Anbieter vergleichen' in html or 'Kosten & Anbieter vergleichen' in html)
      and 'data-cta-id="compare_top"' in html)
check('print_bottom', 'data-cta-id="print_bottom"' in html)
check('editorial_contact', 'data-cta-id="editorial_contact"' in html)
check('Quellenstand 2026-11-04', 'geprüft 2026-11-04' in html)
src_urls = [
    'https://www.pflege-panorama.de/ratgeber/mobiler-hausnotruf/',
    'https://pflegekompass.de/magazin/ratgeber/hausnotruf-mobil-gps',
    'https://www.verbraucherzentrale.de/wissen/gesundheit-pflege/pflege-zu-hause/hausnotrufsysteme-erklaert-so-helfen-sie-im-notfall-funktionen-vorteile-kosten-10566',
    'https://www.gesetze-im-internet.de/sgb_11/__40.html',
    'https://www.rehadat-gkv.de/produkt/index.html?prod=notruf&s3f=s3f&reloaded',
    'https://sanivia.de/ratgeber/notrufsysteme-fuer-senioren/',
    'https://www.hausnotruf-kosten.de/hausnotruf-ohne-festnetz/',
    'https://www.hausnotruf-kosten.de/mobiler-hausnotruf/',
    'https://www.bewo-telehealthcare.com/ratgeber/hausnotruf-basis-vs-mobiler-notruf',
    'https://www.malteser.de/hausnotruf.html',
    'https://www.malteser.de/hausnotruf/faq.html',
    'https://www.pflege-durch-angehoerige.de/hilfsmittel-beratung/notrufsysteme/mobiler-notruf/gps-tracker/',
]
check('Alle 12 Quellen-URLs', all(u in html or u.replace('&', '&amp;') in html for u in src_urls))
check('Related 3 Ziele', html.count('Passend dazu') == 1
      and all(s in html.split('Passend dazu')[1][:900] for s in
              ['hausnotruf-sturzerkennung-oder-knopf', 'hausnotruf-kosten-anbieter-vergleich', 'hilfsmittel-pflegekasse-uebernahme']))
check('kein Partner-Marker', 'data-partner-placement' not in html and 'rel="sponsored' not in html)

code_svg, _ = fetch(f'{BASE}/assets/images/hausnotruf-mobil-entscheidung.svg')
check('SVG-Asset 200', code_svg == 200, str(code_svg))
for target in ['hausnotruf-sturzerkennung-oder-knopf', 'hausnotruf-kosten-anbieter-vergleich', 'hilfsmittel-pflegekasse-uebernahme']:
    c, _ = fetch(f'{BASE}/{target}.html')
    check(f'Related/CTA-Ziel {target} 200', c == 200, str(c))

code_h, home = fetch(BASE + '/')
check('Homepage 200 + listet Artikel', code_h == 200 and 'hausnotruf-mobil-gps-unterwegs' in home)

code_s, sm = fetch(BASE + '/sitemap.xml')
locs = re.findall(r'<loc>([^<]+)</loc>', sm)
check('Sitemap 200, 37 locs', code_s == 200 and len(locs) == 37, str(len(locs)))
check('Sitemap enthält Artikel', any('hausnotruf-mobil-gps-unterwegs' in u for u in locs))
check('Sitemap ohne Region', not any('/region/' in u for u in locs))

code_r, rss = fetch(BASE + '/rss.xml')
items = rss.count('<item>')
check('RSS 200, 27 Items', code_r == 200 and items == 27, str(items))
check('RSS enthält Artikel', 'hausnotruf-mobil-gps-unterwegs' in rss)

code_l, llms = fetch(BASE + '/llms.txt')
check('llms.txt 200 + enthält Artikel', code_l == 200 and 'hausnotruf-mobil-gps-unterwegs' in llms)

print()
if FAIL:
    print(f"ERGEBNIS: {len(FAIL)} FAIL: {FAIL[:8]}")
    sys.exit(1)
print("ERGEBNIS: ALL PASS")
