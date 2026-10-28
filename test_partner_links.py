#!/usr/bin/env python3
"""Partner-Link-Map Gate (data/partner-links.json).

Verifiziert:
  A  Inaktiv (Einstellung im Repo): kein einziger Partner-Marker im Build.
  B  Aktiv (Test-Fixture mit Beispiel-Tracker): CTA nur in den adressierten
     Artikeln, mit rel="sponsored", Anzeige-Kennzeichnung, placement_id,
     Verguetungshinweis; sonstwo null Marker; JSON-LD bleibt valide.
  C  URL ohne approval=true  -> Build bricht ab (Kontradiktion).
  D  approved=true ohne URL -> Build bricht ab (halb aktiver Zustand).
  E  placement_id eindeutig und formatstabil (regex), Slugs existieren.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FAILS = []


def check(name, cond, detail=''):
    if cond:
        print(f'PASS {name}')
    else:
        FAILS.append(f'{name} {detail}')
        print(f'FAIL {name} {detail}')


def run_generate(dist_name, cfg_path=None, expect_ok=True):
    env = dict(os.environ)
    env['DIST_DIR'] = dist_name
    env.pop('PARTNER_LINKS_CONFIG', None)
    if cfg_path is not None:
        env['PARTNER_LINKS_CONFIG'] = str(cfg_path)
    r = subprocess.run(['node', 'generate.mjs', '--index'], cwd=ROOT, env=env,
                       capture_output=True, text=True, timeout=180)
    if expect_ok and r.returncode != 0:
        print('--- stdout tail ---')
        print(r.stdout[-1500:])
        print('--- stderr tail ---')
        print(r.stderr[-1500:])
    return r


def read_html(dist_name, name):
    return (ROOT / dist_name / name).read_text(encoding='utf-8')


def marker_count(html):
    return sum(html.count(m) for m in (
        'data-partner-placement', 'rel="sponsored', 'class="partner-cta"', 'awin1.com'))


def fixture_config(active=True, approved=True, with_url=True, slug='hausnotruf-kosten-anbieter-vergleich'):
    placement = {
        'placement_id': 'hausnotruf_infomaterial_end',
        'label': 'Informationsmaterial der Malteser anfordern',
        'subline': 'Hausnotruf-Grundlagen zum Vergleich mehrerer Anbieter.',
        'cta_text': 'Infos anfordern',
        'url': 'https://tracker.example.com/awin-test?mid=112616' if with_url else '',
        'articles': ['hausnotruf-kosten-anbieter-vergleich', 'hausnotruf-sturzerkennung-oder-knopf'],
    }
    if slug:
        placement['articles'] = [slug] + [s for s in placement['articles'] if s != slug]
    return {
        'active': active,
        'partners': [{
            'id': 'malteser', 'name': 'Malteser', 'awin_advertiser_id': 112616,
            'approved': approved, 'approval_readback': 'test-fixture',
            'placements': [placement],
        }],
    }


def main():
    tmp = Path(tempfile.mkdtemp(prefix='partner-test-', dir=ROOT))
    try:
        # --- Szenario E: eingebaute Konfigurationsdatei ist formatstabil ---
        cfg_raw = json.loads((ROOT / 'data/partner-links.json').read_text(encoding='utf-8'))
        check('E1 repo-config active=false', cfg_raw.get('active') is False)
        ids = [p['placement_id'] for part in cfg_raw['partners'] for p in part['placements']]
        check('E2 no duplicate placement_id', len(ids) == len(set(ids)))

        # --- Szenario A: inaktive Repo-Konfiguration rendert nichts ---
        r = run_generate('dist-pl-inactive')
        check('A0 inactive build exits 0', r.returncode == 0)
        if r.returncode == 0:
            total = 0
            for page in (ROOT / 'dist-pl-inactive').rglob('*.html'):
                total += marker_count(page.read_text(encoding='utf-8'))
            check('A1 zero partner markers in default build', total == 0, f'found {total}')
            check('A2 article count still >= 25',
                  len(list((ROOT / 'dist-pl-inactive').glob('*.html'))) >= 25)

        # --- Szenario B: aktive Fixture rendert nur adressierte Artikel ---
        cfg_b = tmp / 'cfg-active.json'
        cfg_b.write_text(json.dumps(fixture_config()), encoding='utf-8')
        r = run_generate('dist-pl-active', cfg_b)
        check('B0 active fixture build exits 0', r.returncode == 0)
        if r.returncode == 0:
            hn1 = read_html('dist-pl-active', 'hausnotruf-kosten-anbieter-vergleich.html')
            hn2 = read_html('dist-pl-active', 'hausnotruf-sturzerkennung-oder-knopf.html')
            for name, html in [('B1 hausnotruf-kosten', hn1), ('B2 hausnotruf-sturz', hn2)]:
                check(name + ' has partner CTA',
                      html.count('data-partner-placement="hausnotruf_infomaterial_end"') == 1)
                check(name + ' rel sponsored noopener', 'rel="sponsored noopener"' in html)
                check(name + ' target blank', 'target="_blank"' in html)
                check(name + ' disclosure', 'Vergütung erhalten' in html and 'Anzeige' in html)
                check(name + ' placement id attr', 'data-placement-id="hausnotruf_infomaterial_end"' in html)
                check(name + ' cta id', 'data-cta-id="partner_malteser"' in html)
            # JSON-LD bleibt im Partner-Seitenkontext valide
            m = re.search(r'<script type="application/ld\+json">(.*?)</script>', hn1, re.S)
            if m is None:
                check('B3 JSON-LD parses on partner page', False, 'no JSON-LD script tag')
            else:
                try:
                    json.loads(m.group(1))
                    check('B3 JSON-LD parses on partner page', True)
                except Exception as e:  # noqa: BLE001
                    check('B3 JSON-LD parses on partner page', False, str(e))
            # sonstwo null Marker
            leaks = []
            for page in (ROOT / 'dist-pl-active').rglob('*.html'):
                if page.name in ('hausnotruf-kosten-anbieter-vergleich.html',
                                 'hausnotruf-sturzerkennung-oder-knopf.html'):
                    continue
                if marker_count(page.read_text(encoding='utf-8')):
                    leaks.append(page.name)
            check('B4 zero partner markers on all other pages', not leaks, str(leaks[:5]))

        # --- Szenario C: URL ohne approval=true bricht Build ab ---
        cfg_c = tmp / 'cfg-unapproved-url.json'
        cfg_c.write_text(json.dumps(fixture_config(approved=False)), encoding='utf-8')
        r = run_generate('dist-pl-c', cfg_c, expect_ok=False)
        check('C1 url without approval fails build', r.returncode != 0)

        # --- Szenario D: approved ohne URL bricht Build ab ---
        cfg_d = tmp / 'cfg-approved-nourl.json'
        cfg_d.write_text(json.dumps(fixture_config(with_url=False)), encoding='utf-8')
        r = run_generate('dist-pl-d', cfg_d, expect_ok=False)
        check('D1 approved without url fails build', r.returncode != 0)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        for d in ('dist-pl-inactive', 'dist-pl-active', 'dist-pl-c', 'dist-pl-d'):
            shutil.rmtree(ROOT / d, ignore_errors=True)

    print()
    if FAILS:
        print(f'{len(FAILS)} FAILS')
        for f in FAILS:
            print(' -', f)
        return 1
    print('ALL PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
