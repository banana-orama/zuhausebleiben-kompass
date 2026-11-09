#!/usr/bin/env python3
"""Live-Readback des Förder-Prüflaufs 09.11.2026 gegen die öffentliche URL
(GitHub Pages Deploy lag CI success um Minuten — pollt bis zum Sichtbarwerden).
Asserts je Seite; Exit 1 bei Verfehlen. Ausgabe in research/live_readback_091126.log."""
import subprocess
import sys
import time

BASE = 'https://zuhausebleiben-kompass.de'
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'

CHECKS = [
    ('/treppenlift-zuschuss.html', {
        'count>=2': '9. November 2026',
        'count==0': '2. November 2026',
        'contains': 'geprüft 2026-11-09',
        'robots': 'index,follow',
    }),
    ('/bad-umbau-barrierefrei.html', {
        'count>=2': '9. November 2026',
        'count==0': '2. November 2026',
        'robots': 'index,follow',
    }),
    ('/bodengleiche-dusche-altbau.html', {
        'count>=2': '9. November 2026',
        'count==0': '2. November 2026',
        'robots': 'index,follow',
    }),
    ('/wanne-zur-dusche.html', {
        'count>=1': '9. November 2026',
        'count==0': '2. November 2026',
        'robots': 'index,follow',
    }),
    ('/wohnumfeldverbesserung-beantragen.html', {
        'count==1': '2. November 2026',
        'count==0': '9. November 2026',
        'robots': 'index,follow',
    }),
    ('/hilfsmittel-dusch-wc-uebernahme.html', {
        'count>=1': 'ab 2,19 Prozent (Stand: 10. Juli 2025)',
        'robots': 'index,follow',
    }),
    ('/', {
        'robots': 'index,follow',
    }),
]


def fetch(path):
    r = subprocess.run(['curl', '-sS', '-A', UA, '--max-time', '30', BASE + path],
                       capture_output=True, text=True)
    return r.stdout


deadline = time.time() + 420
fails = []
pages = {}
while time.time() < deadline:
    pages = {}
    ready = True
    for path, _ in CHECKS:
        html = fetch(path)
        pages[path] = html
        if path == '/treppenlift-zuschuss.html' and '9. November 2026' not in html:
            ready = False  # Deploy-Lag: neuer Inhalt noch nicht da
    if ready:
        break
    print(f'… deploy lag: treppenlift-zuschuss zeigt neuen Inhalt noch nicht ({int(deadline - time.time())}s Rest), warte 25s')
    time.sleep(25)

for path, spec in CHECKS:
    html = pages[path]
    if not html:
        fails.append(f'{path}: LEERE Antwort (curl fehlgeschlagen)')
        print(f'FAIL {path}: keine Antwort')
        continue
    ok = True
    for kind, needle in spec.items():
        if kind == 'contains':
            present = needle in html
            status = 'PASS' if present else 'FAIL'
            if not present:
                fails.append(f'{path}: "{needle}" fehlt (contains)')
                ok = False
            print(f'{status} {path} contains "{needle}"')
        elif kind == 'robots':
            present = f'<meta name="robots" content="{needle}">' in html
            status = 'PASS' if present else 'FAIL'
            if not present:
                fails.append(f'{path}: robots != {needle}')
                ok = False
            print(f'{status} {path} robots={needle}')
        elif kind.startswith('count=='):
            want = int(kind.split('==')[1])
            got = html.count(needle)
            status = 'PASS' if got == want else 'FAIL'
            if got != want:
                fails.append(f'{path}: count "{needle}" = {got}, erwartet {want}')
                ok = False
            print(f'{status} {path} count "{needle}" = {got} (erwartet {want})')
        elif kind.startswith('count>='):
            want = int(kind.split('>=')[1])
            got = html.count(needle)
            status = 'PASS' if got >= want else 'FAIL'
            if got < want:
                fails.append(f'{path}: count "{needle}" = {got}, erwartet >= {want}')
                ok = False
            print(f'{status} {path} count "{needle}" = {got} (erwartet >= {want})')
    if ok:
        print(f'OK   {path} HTTP 200, alle lokalen Asserts PASS')

print('=' * 80)
if fails:
    print(f'ERGEBNIS: {len(fails)} FAIL(s):')
    for f in fails:
        print(f'  {f}')
    sys.exit(1)
print(f'ERGEBNIS: LIVE-READBACK ALL PASS ({len(CHECKS)} Seiten, öffentliche URL {BASE})')
