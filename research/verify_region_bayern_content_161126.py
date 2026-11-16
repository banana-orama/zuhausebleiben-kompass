#!/usr/bin/env python3
"""Content-Support-Gate für die Bayern-Region-Seite (LAUNCH-dist).
Läuft gegen dist/, wie die NRW-Variante. Prüft Kernzahlen, Absenzen,
Quellen, Anker, Verweise und Sitemap-Konsistenz. Exit 0 = ALL PASS."""
import json, re, sys
from pathlib import Path
from html import unescape

root = Path(__file__).resolve().parent.parent / 'dist'
page = root / 'region' / 'bayern.html'
hub = root / 'regional.html'
sm = root / 'sitemap.xml'
fails, passes = [], []

def check(name, cond, detail=''):
    (passes if cond else fails).append(f"{name} {detail}".strip())

def strip_html(html):
    t = re.sub(r'<sup[^>]*>.*?</sup>', ' ', html, flags=re.S)
    t = re.sub(r'<[^>]+>', ' ', t)
    return re.sub(r'\s+', ' ', unescape(t))

check('page exists', page.exists(), str(page))
h = page.read_text()
body = strip_html(h)
raw = h

# Robots + Basis
check('robots index,follow', '<meta name="robots" content="index,follow"' in h)
check('title in <title>', 'Umbau-Förderung in Bayern: vier Wege' in h and 'ZuhauseBleiben Kompass' in h)
check('H1', 'Umbau und Förderung in Bayern' in body)
check('KI-Kennzeichnung', 'KI-Unterstützung' in body)
check('Quellenstand 16.11.2026', '16.11.2026' in body)

# Kernzahlen (prose spelling, dotted)
for needle in ['10.000', '28.300', '43.200', '10.700', '3.200', '50.000',
               '40.000', '1 %', 'Oberbayern', 'Schwaben', 'BayernLabo',
               'BayWoFG', '§ 113 Abs. 2 Nr. 1', '§ 77 SGB IX', 'formlos',
               'ZBFS', 'Pflegestützpunkt', 'sozialen Dringlichkeit',
               'Belegungsbindung', 'Fehlbedarfsfinanzierung']:
    check(f'number/fact "{needle}"', needle in body)

# KfW-Wortlaute
check('455-B Stopp-Wortlaut', 'Diesen Zuschuss können Sie nicht mehr beantragen' in body)
check('2027-Bedingung', 'wird eine Antragstellung wieder möglich sein' in body)
check('159 Treppenlift-Maßnahme', 'Treppenlifte, Senkrecht-, Hebe- oder Plattformlifte installieren' in body)
check('Kombi-Kredit-Hinweis', 'mit dem Kredit der KfW gefördert werden' in body)

# Ehrlichkeit: Treppenlift nicht namentlich im Landesprogramm
check('Treppenlift-Absenz-Transparenz', 'nicht namentlich' in body)
check('Baustein-Beispiele Aufzug/Rampe', 'Aufzug' in body and 'Rampe' in body)

# NRW-Differenzierung FAQ (genau einmal) + "nicht gefunden"-Ehrlichkeit
check('anrechenfreie nur als NRW-Abgrenzung', body.count('anrechenfreien Beträgen') == 1 and 'nicht gefunden' in body)

# Absenzen: keine §40-Beträge, keine Partnermarker, keine NRW-Programmzahlen
for absent in ['4.180', '16.720', '8.360', '220.000', '23.540', 'awin',
               'sponsored', 'rel="noopener sponsored"', '>Anzeige<', 'NRW.BANK', 'LVR', 'LWL']:
    check(f'absence "{absent}"', absent not in body)

# Beschreibungs-Länge (Titel-Gate-Spiegel)
desc = json.loads((root.parent / 'data' / 'region-bayern.json').read_text())['description']
check('description <=160', len(desc) <= 160, f'len={len(desc)}')
check('title <=65 incl suffix', len('Umbau-Förderung in Bayern: vier Wege — ZuhauseBleiben Kompass') <= 65)

# Quellen
srcs = json.loads((root.parent / 'data' / 'region-bayern.json').read_text())['sources']
check('sources >= 12', len(srcs) >= 12, f'n={len(srcs)}')
check('sources all checked 16.11.', all(s['checked_at'] == '2026-11-16' for s in srcs))
check('sources rendered', h.count('<li><a href="https://') >= len(srcs))
for s in srcs[:6]:
    check(f"source url present {s['url'][:48]}", s['url'] in h)

# CTA/Related-Ziele existieren im dist
for target in ['treppenlift-zuschuss', 'wohnumfeldverbesserung-beantragen',
               'treppenlift-foerderung-ohne-pflegegrad', 'treppenlift-mietwohnung',
               'pflegegrad-antrag-ablauf-fristen', 'treppenlift-kosten']:
    check(f'target exists {target}', (root / f'{target}.html').exists())
check('ctaEarly wired', 'treppenlift-zuschuss.html' in h)
check('related section', 'Passend dazu' in h)

# FAQ-Struktur
check('6 FAQ details', h.count('<details>') == 6, f'n={h.count("<details>")}')

# Hub
hb = hub.read_text()
check('hub lead mentions both regions', 'Nordrhein-Westfalen und Bayern sind als erste Regionen' in hb)
check('hub card Bayern + teaser', 'bayern.html' in hb and 'leistungsfreies Landesdarlehen bis 10.000' in hb)
check('hub noindex', '<meta name="robots" content="noindex,follow"' in hb)

# Platzhalter-Prosa darf auf der Bayern-Seite nicht mehr stehen
check('placeholder prose gone', 'noch nicht recherchiert und angebunden' not in body)

# Sitemap: genau die zwei ausgebauten Regionen, keine Platzhalter
locs = [u.split('<loc>')[1].split('</loc>')[0] for u in sm.read_text().split('<url>')[1:]]
region_urls = sorted(u for u in locs if '/region/' in u)
check('sitemap regions == nrw+bayern', region_urls == [
    'https://zuhausebleiben-kompass.de/region/bayern.html',
    'https://zuhausebleiben-kompass.de/region/nordrhein-westfalen.html'], str(region_urls))
check('sitemap total 51 locs', len(locs) == 51, f'n={len(locs)}')
check('hub not in sitemap', not any(u.endswith('/regional.html') for u in locs))

# Keine Entwurfs-/Vorschau-Prosa
check('no draft prose', 'Entwurf zur ersten Orientierung' not in body)

print(f"PASS {len(passes)} / FAIL {len(fails)}")
for f_ in fails:
    print('FAIL:', f_)
sys.exit(1 if fails else 0)
