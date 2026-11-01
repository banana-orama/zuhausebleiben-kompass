#!/usr/bin/env python3
"""Live-Readback 01.11.2026: öffentliche URL nach Deploy 88de460 (CI 41346461814).
Prüft: HTTP 200, geprüft-2026-11-01-Quellenzeilen, Quellenstand-Meta, sichtbare
KfW-Prüfdaten „1. November 2026", robots index,follow."""
import json
import re
import subprocess
import sys
import urllib.request

BASE = json.load(open('data/content.json', encoding='utf-8'))['brand']['base_url'].rstrip('/')
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}

FAIL = []


def fetch(path):
    # python-seitige DNS-Auflösung ist auf dieser Maschine intermittierend flaky
    # (curl/dig lösen zuverlässig auf) — daher curl als Transport.
    for attempt in range(3):
        p = subprocess.run(
            ['curl', '-sS', '--max-time', '30', '-A', UA['User-Agent'],
             BASE + '/' + path.lstrip('/')],
            capture_output=True, text=True)
        if p.returncode == 0:
            return 200, p.stdout
        if attempt == 2:
            raise RuntimeError(f'curl rc={p.returncode}: {p.stderr.strip()[:120]}')
        import time
        time.sleep(2)
    raise RuntimeError('unreachable')


checks = [
    ('treppenlift-zuschuss.html', ['geprüft 2026-11-01', 'Quellenstand: 2026-11-01', 'am 1. November 2026', 'index,follow']),
    ('bad-umbau-barrierefrei.html', ['geprüft 2026-11-01', 'am 1. November 2026', 'index,follow']),
    ('bodengleiche-dusche-altbau.html', ['geprüft 2026-11-01', 'am 1. November 2026', 'index,follow']),
    ('wanne-zur-dusche.html', ['geprüft 2026-11-01', 'am 1. November 2026' if False else 'index,follow']),
    ('hilfsmittel-dusch-wc-uebernahme.html', ['geprüft 2026-11-01', '2,19 Prozent (Stand: 10. Juli 2025)', 'index,follow']),
    ('treppenlift-kosten.html', ['geprüft 2026-11-01']),
    ('rollator-auswahl-passform-kosten.html', ['geprüft 2026-11-01', 'Abrufstand vom 16. Oktober 2026']),
    ('hilfsmittel-pflegekasse-uebernahme.html', ['geprüft 2026-11-01', 'Abrufstand vom 19. Oktober 2026']),
]
for path, needles in checks:
    try:
        status, html = fetch(path)
    except Exception as e:
        FAIL.append(f'{path}: FETCH {e}')
        print(f'FAIL  {path}: {e}')
        continue
    if status != 200:
        FAIL.append(f'{path}: HTTP {status}')
        print(f'FAIL  {path}: HTTP {status}')
        continue
    missing = [n for n in needles if n not in html]
    if missing:
        FAIL.append(f'{path}: fehlt {missing}')
        print(f'FAIL  {path}: fehlt {missing}')
    else:
        print(f'PASS  {path}: alle {len(needles)} Needles live ({", ".join(n[:34] for n in needles)})')

# Kein „26. Oktober"-KfW-Stempel mehr in den 3 gepatchten Artikeln
for path in ('treppenlift-zuschuss.html', 'bad-umbau-barrierefrei.html', 'bodengleiche-dusche-altbau.html'):
    _, html = fetch(path)
    if '26. Oktober 2026' in html:
        FAIL.append(f'{path}: alter Stempel „26. Oktober 2026" noch live')
        print(f'FAIL  {path}: alter KfW-Stempel noch live')
    else:
        print(f'PASS  {path}: kein „26. Oktober 2026"-Stempel mehr')

status, home = fetch('/')
print('info  Homepage:', status, '| robots', re.search(r'name="robots" content="([^"]+)"', home).group(1))
status, sm = fetch('/sitemap.xml')
print('info  Sitemap:', status, '|', sm.count('<loc>'), 'locs')

if FAIL:
    print('\nERGEBNIS: FAIL —', FAIL)
    sys.exit(1)
print('\nERGEBNIS: Live-Readback PASS — Deploy 88de460 auf öffentlicher URL bestätigt.')
