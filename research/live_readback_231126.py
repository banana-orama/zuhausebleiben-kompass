#!/usr/bin/env python3
"""Live-Readback 23.11.2026: öffentliche URL prüfen (nicht nur dist/Build).
Erwartet wird der Deploy von Commit 39c084c (GitHub Pages laggt CI um Minuten —
bei 404/Altstand warten und erneut pollen).
"""
import subprocess
import sys
import time

BASE = 'https://zuhausebleiben-kompass.de'
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'

PAGES = [
    '/treppenlift-zuschuss.html',
    '/bad-umbau-barrierefrei.html',
    '/bodengleiche-dusche-altbau.html',
    '/wanne-zur-dusche.html',
    '/hausnotruf-angehoerige-einrichten.html',
    '/index.html',
]


def fetch(path):
    r = subprocess.run(['curl', '-sS', '-L', '--compressed', '-A', UA, '--max-time', '30',
                        f'{BASE}{path}'], capture_output=True)
    return r.stdout.decode('utf-8', 'replace')


def count(text, needle):
    return text.count(needle)


def robots(text):
    import re
    m = re.search(r'name="robots" content="([^"]+)"', text)
    return m.group(1) if m else 'KEIN-ROBOTS'


def wait_for_deploy(max_rounds=20):
    """Deploy-Lag: bis der Money-Page-Stempel '23. November' live erscheint pollen."""
    for i in range(max_rounds):
        t = fetch('/treppenlift-zuschuss.html')
        if count(t, '23. November 2026') >= 3:
            print(f'Deploy-Live nach {i + 1} Poll(s).')
            return
        print(f'Poll {i + 1}: noch Altstand ({count(t, "18. November 2026")}× 18-Nov / {count(t, "23. November 2026")}× 23-Nov) — 30 s warten')
        time.sleep(30)
    print('WARN: Deploy-Stand nicht erreicht — Readback bricht ab.')
    sys.exit(2)


wait_for_deploy()
fails = []

def check(label, cond):
    print(('PASS  ' if cond else 'FAIL  ') + label)
    if not cond:
        fails.append(label)

# --- money-page ---
t = fetch('/treppenlift-zuschuss.html')
check('money-page HTTP+robots index,follow', robots(t) == 'index,follow')
check('money-page 23. November 2026 x3+ (Intro/Sektion/FAQ)', count(t, '23. November 2026') >= 3)
check('money-page Status am 23.11.2026 x1', count(t, 'Status am 23.11.2026') == 1)
check('money-page 0x 18. November / Status am 18.11', count(t, '18. November 2026') == 0 and count(t, 'Status am 18.11') == 0)
check('money-page geprüft 2026-11-23 x6 (7 Quellen, §554 bleibt alt)', count(t, 'geprüft 2026-11-23') == 6)
check('money-page Ampel-Rows unverändert: 220.000 x1, 10.000 x1', count(t, '220.000') >= 1 and count(t, '10.000') >= 1)
check('money-page 455-B-Verbatim „Diesen Zuschuss können Sie nicht mehr beantragen" x1+ (Renderer dupliziert FAQ-Answers ins JSON-LD — exakte Prosa-Gleichheit gilt nicht)', count(t, 'Diesen Zuschuss können Sie nicht mehr beantragen') >= 1)
check('money-page §40-Zahlen: 4.180/16.720', count(t, '4.180') >= 1 and count(t, '16.720') >= 1)

# --- 3 KfW-Ratgeber ---
# Renderer spiegelt FAQ-Answers ins JSON-LD → jedes Prosa-Datum kann 2× im HTML
# stehen. Verbindliche Signale: neues Datum mind. n23×, altes Datum exakt 0×,
# geprüft-2026-11-23-Quellenfooter exakt 4×.
for path, n23 in [('/bad-umbau-barrierefrei.html', 2), ('/bodengleiche-dusche-altbau.html', 2), ('/wanne-zur-dusche.html', 1)]:
    t = fetch(path)
    check(f'{path}: robots index,follow', robots(t) == 'index,follow')
    check(f'{path}: 23. November 2026 >= {n23} (JSON-LD-Duplikate möglich)', count(t, '23. November 2026') >= n23)
    check(f'{path}: 0x 16. November', count(t, '16. November 2026') == 0)
    check(f'{path}: geprüft 2026-11-23 x4', count(t, 'geprüft 2026-11-23') == 4)

# --- VZ-Fix-Seite ---
t = fetch('/hausnotruf-angehoerige-einrichten.html')
check('angehoerige: robots index,follow', robots(t) == 'index,follow')
check('angehoerige: neue VZ-URL /vorsorgevollmacht im Quellenblock', count(t, 'https://www.verbraucherzentrale.de/vorsorgevollmacht') == 1)
check('angehoerige: 0x tote Veranstaltungs-URL', count(t, 'ernstfall-gewappnet') == 0)
check('angehoerige: Paraphrase „ausdrücklichen Vollmacht" ohne Anführungszeichen-Zitat', count(t, 'ausdrücklichen Vollmacht') >= 1 and count(t, 'In dieser Situation braucht es eine rechtliche Vertretung') == 0)
check('angehoerige: VZ-Quelle geprüft 2026-11-23 (Restquelle 11-10 bleibt)', count(t, 'geprüft 2026-11-23') >= 1)

# --- Homepage ---
t = fetch('/index.html')
check('Homepage robots index,follow', robots(t) == 'index,follow')

print('=' * 70)
print(f'ERGEBNIS: {len(fails)} FAIL von 24 Checks' if fails else 'ERGEBNIS: alle 24 Checks PASS — Deploy live verifiziert.')
if fails:
    for f in fails:
        print('  FAIL:', f)
    sys.exit(1)
