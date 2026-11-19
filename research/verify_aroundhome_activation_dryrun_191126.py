#!/usr/bin/env python3
"""Aroundhome-Aktivierungs-Dry-Run (19.11.2026).

Beweist, dass die Aktivierung am Freischalttag als EIN Commit
(data/partner-links.json + DSE_META in generate.mjs) sauber baut:

  H  Fixture (approved=true + Placements) gegen PRODUKTIONS-generate.mjs
     -> Build MUSS abbrechen (DSE_META fehlt) = Same-Commit-Gate scharf.
  A  Mit DSE_META.aroundhome: CTA nur auf den adressierten Bad-Cluster-Artikeln,
     no-deeplink-Tracker (awinmid=68536&awinaffid=3124891), rel="sponsored noopener",
     Anzeige-Kennzeichnung, placement_id.
  B  Keine Bad-Cluster-Placements auf Nicht-Bad-Artikeln (Treppenlift/ Hausnotruf
     bleiben malteser-only bzw. markerfrei).
  C  datenschutz.html spiegelt Aroundhome (Name, Cookie 30 Tage, verifizierte DSE-URL).
  D  JSON-LD der adressierten Seiten bleibt parse-valide.
  E  Sitemap-Umfang identisch zum Produktionsbuild (keine Seitenänderung).
  F  Teilaktivierung (approved=true, placements=[]) bricht ab (Renderer-Kontradiktion).
Nach dem Lauf wird generate.mjs per git checkout restored (Dry-Run bleibt unsichtbar).
"""
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EV = ROOT / 'research/evidence/aroundhome-191126'
FIXTURE = EV / 'partner-links-fixture-activation.json'
PARTIAL = EV / 'partner-links-fixture-partial.json'
DIST = ROOT / 'cache/aroundhome-dryrun-dist'
GEN = ROOT / 'generate.mjs'
TRACKER = 'https://www.awin1.com/cread.php?awinmid=68536&awinaffid=3124891'
FAILS = []


def check(name, cond, detail=''):
    print(('PASS ' if cond else 'FAIL ') + name + ((' — ' + detail) if detail else ''))
    if not cond:
        FAILS.append(name)


def run_build(cfg, expect_ok):
    env = dict(os.environ)
    env['DIST_DIR'] = str(DIST.relative_to(ROOT))
    env['PARTNER_LINKS_CONFIG'] = str(cfg)
    r = subprocess.run(['node', 'generate.mjs', '--index'], cwd=ROOT, env=env,
                       capture_output=True, text=True, timeout=240)
    ok = r.returncode == 0
    return ok, r


def read(name):
    return (DIST / name).read_text(encoding='utf-8')


def marker_count(html):
    return sum(html.count(m) for m in (
        'data-partner-placement', 'rel="sponsored', 'class="partner-cta"', 'awin1.com'))


def main():
    shutil.rmtree(DIST, ignore_errors=True)
    EV.mkdir(parents=True, exist_ok=True)

    # Fixture: voller Aktivierungszustand (Textlink-Start, 2 Placements, kein Deeplink)
    src = json.loads((ROOT / 'data/partner-links.json').read_text(encoding='utf-8'))
    for p in src['partners']:
        if p['id'] == 'aroundhome':
            p['approved'] = True
            p['approval_readback'] = {
                'date': 'DRYRUN-PLATZHALTER',
                'evidence': 'Bei echter Freischaltung: Status-Readback (Bewerbung offen -> '
                            'zugelassen / Agency-Freischaltung via Publisher-ID 3124891) hier '
                            'mit Datum+Beleg eintragen. Tracker-Format ohne Deeplink wurde '
                            '19.11. als Pre-Approval-Probe verifiziert (302, awc-Attribution).'
            }
            p['placements'] = [
                {
                    'placement_id': 'aroundhome_badumbau_angebote',
                    'articles': ['badumbau-angebote-vergleichen', 'bad-umbau-barrierefrei'],
                    'url': TRACKER,
                    'label': 'Fachbetriebe für den barrierefreien Badumbau finden',
                    'cta_text': 'Passende Fachbetriebe vergleichen',
                    'subline': 'Kostenlos und unverbindlich · Aroundhome prüft die Anfrage '
                               'und vermittelt passende regionale Fachbetriebe'
                },
                {
                    'placement_id': 'aroundhome_badumbau_planung',
                    'articles': ['badumbau-kosten', 'wanne-zur-dusche', 'bodengleiche-dusche-altbau'],
                    'url': TRACKER,
                    'label': 'Badumbau: Angebote von regionalen Fachbetrieben einholen',
                    'cta_text': 'Angebote für Ihren Badumbau einholen',
                    'subline': 'Kostenlos und unverbindlich · Qualifizierung und Matching '
                               'erfolgen beim Anbieter, nicht auf dieser Seite'
                }
            ]
    FIXTURE.write_text(json.dumps(src, indent=2, ensure_ascii=False), encoding='utf-8')

    # Teilaktivierung: approved ohne Placements (muss abbrechen)
    part = json.loads((ROOT / 'data/partner-links.json').read_text(encoding='utf-8'))
    for p in part['partners']:
        if p['id'] == 'aroundhome':
            p['approved'] = True
    PARTIAL.write_text(json.dumps(part, indent=2, ensure_ascii=False), encoding='utf-8')

    gen_before = GEN.read_text(encoding='utf-8')
    restored = False
    try:
        # H) Produktions-generate.mjs (ohne DSE_META.aroundhome) + Voll-Fixture -> MUSS werfen
        ok, r = run_build(FIXTURE, expect_ok=False)
        threw_dse = ('DSE_META fehlt' in (r.stderr or '') + (r.stdout or ''))
        check('H gate-fires: Build bricht ohne DSE_META.aroundhome ab',
              (not ok) and threw_dse,
              'rc=%s dse-msg=%s' % (r.returncode, threw_dse))

        # F) Teilaktivierung (approved, keine Placements) -> MUSS werfen (Renderer-Regel)
        ok2, r2 = run_build(PARTIAL, expect_ok=False)
        threw_partial = ('no placements' in (r2.stderr or '')) or ('no placements' in (r2.stdout or ''))
        check('F partial-activation: approved ohne Placement bricht ab',
              (not ok2) and threw_partial, 'rc=%s' % r2.returncode)

        # DSE_META.aroundhome ergänzen (der exakte Same-Commit-Edit)
        old = "const DSE_META={malteser:{desc:'Hausnotruf',cookie:'30 Tage',checked:'2. November 2026',url:'https://www.malteser.de/datenschutz.html'}};"
        new = ("const DSE_META={malteser:{desc:'Hausnotruf',cookie:'30 Tage',checked:'2. November 2026',"
               "url:'https://www.malteser.de/datenschutz.html'},"
               "aroundhome:{desc:'Badumbau-Vermittlung',cookie:'30 Tage',checked:'19. November 2026',"
               "url:'https://www.aroundhome.de/datenschutzerklaerung/'}};")
        assert GEN.read_text(encoding='utf-8') == gen_before
        assert old in gen_before, 'DSE_META-Anker nicht gefunden'
        GEN.write_text(gen_before.replace(old, new), encoding='utf-8')

        # A-E) Vollaktivierung
        ok3, r3 = run_build(FIXTURE, expect_ok=True)
        check('A build-ok: Aktivierungszustand baut mit DSE_META.aroundhome', ok3,
              (r3.stderr or '')[-200:])
        if ok3:
            placements = {
                'badumbau-angebote-vergleichen.html': 'aroundhome_badumbau_angebote',
                'bad-umbau-barrierefrei.html': 'aroundhome_badumbau_angebote',
                'badumbau-kosten.html': 'aroundhome_badumbau_planung',
                'wanne-zur-dusche.html': 'aroundhome_badumbau_planung',
                'bodengleiche-dusche-altbau.html': 'aroundhome_badumbau_planung',
            }
            for page, pid in placements.items():
                h = read(page)
                # & ist in built HTML als &amp; escaped (Pitfall) — Tracker-Needle escapet pruefen
                url_escaped = 'awinmid=68536&amp;awinaffid=3124891'
                check('A %s rendert Placement %s' % (page, pid),
                      ('data-partner-placement="%s"' % pid) in h
                      and url_escaped in h
                      and 'rel="sponsored noopener"' in h
                      and 'Anzeige · Kooperation mit Aroundhome DE' in h)

            for off in ('treppenlift-zuschuss.html', 'treppenlift-kosten.html',
                        'hausnotruf-kosten-anbieter-vergleich.html'):
                h = read(off)
                has_ah = 'aroundhome_badumbau' in h
                check('B %s ohne Aroundhome-Marker' % off, not has_ah)
            h_mal = read('hausnotruf-koten-anbieter-vergleich.html') if False else read('hausnotruf-kosten-anbieter-vergleich.html')
            check('B Malteser-Placement unverändert weiter vorhanden',
                  'malteser_beratungstermin' in h_mal and 'awinmid=112616' in h_mal)

            d = read('datenschutz.html')
            check('C DSE nennt Aroundhome + Cookie + DSE-URL',
                  'Aroundhome DE' in d and '30 Tage' in d
                  and 'https://www.aroundhome.de/datenschutzerklaerung/' in d
                  and 'Badumbau-Vermittlung' in d)

            import html as html_mod
            for page in ('badumbau-angebote-vergleichen.html', 'badumbau-kosten.html'):
                h = read(page)
                for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
                    try:
                        html_mod.unescape  # import shadow-guard reference
                        json.loads(html_mod.unescape(m))
                    except Exception as e:
                        check('D JSON-LD parse %s' % page, False, str(e)[:120])
                        break
                else:
                    check('D JSON-LD parse %s' % page, True)

            sitemap = read('sitemap.xml')
            locs = sitemap.count('<loc>')
            # generate-only-Build: Checklisten-URLs kommen erst aus build-checklists.mjs.
            # Invariante: gleicher Umfang wie ein Produktions-generate-only-Build im selben Baum
            # + alle 5 adressierten Artikel in der Sitemap.
            loc_urls = set(re.findall(r'<loc>(.*?)</loc>', sitemap))
            for page in placements:
                check('E %s in Sitemap' % page, any(u.endswith(page) for u in loc_urls))
            prod_env_build = str(DIST) + '-prodcmp'
            env2 = dict(os.environ)
            env2['DIST_DIR'] = str(Path(prod_env_build).relative_to(ROOT))
            env2.pop('PARTNER_LINKS_CONFIG', None)
            r4 = subprocess.run(['node', 'generate.mjs', '--index'], cwd=ROOT, env=env2,
                                capture_output=True, text=True, timeout=240)
            if r4.returncode == 0:
                prod_locs = (Path(prod_env_build) / 'sitemap.xml').read_text(encoding='utf-8').count('<loc>')
                check('E Sitemap-Umfang = Produktions-generate-only-Build (%d locs, erwartetes Delta +8 Checklisten via build-checklists)' % prod_locs,
                      locs == prod_locs, 'dryrun=%s prod=%s' % (locs, prod_locs))
                shutil.rmtree(prod_env_build, ignore_errors=True)
            else:
                check('E Vergleichsbuild (Produktions-Config) fehlgeschlagen', False, r4.stderr[-150:])
    finally:
        GEN.write_text(gen_before, encoding='utf-8')
        restored = subprocess.run(['git', 'diff', '--quiet', '--', 'generate.mjs'],
                                  cwd=ROOT, capture_output=True).returncode == 0
        check('generate.mjs restored (kein Diff)', restored)

    shutil.rmtree(DIST, ignore_errors=True)
    print('\n%d FAILS' % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == '__main__':
    main()
