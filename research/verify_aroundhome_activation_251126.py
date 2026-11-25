#!/usr/bin/env python3
"""Aroundhome-Aktivierungs-Gates gegen den REALen LAUNCH-dist (25.11.2026).

Playbook operations/aroundhome-activation-prep.md, Acceptance-Schritt 3:
  A  Beide Placements auf genau den 5 adressierten Bad-Cluster-Artikeln
     (data-partner-placement, rel="sponsored noopener", escapete Tracker-URL,
     Anzeige-Kennzeichnung, CTA-/Label-/Subline-Text, target=_blank).
  B  0 Aroundhome-Marker auf allen anderen dist-HTML-Seiten.
  C  Malteser-Placements unverändert (awinmid=112616, beide placement_ids).
  D  datenschutz.html spiegelt Aroundhome (Name, Bereich, Cookie 30 Tage,
     Profil geprüft am 25.11., verifizierte DSE-URL, Fallback-Text 0x,
     Abschnitte 1-9 stabil, Abschnitt-5-Variante mit Empfehlungslinks).
  E  JSON-LD auf den 5 adressierten Seiten parse-valide.
  F  Sitemap-Umfang identisch zum LIVE-Stand vor der Aktivierung + die 5
     Artikel + datenschutz bleiben drin; robots index,follow (LAUNCH-Modus).
"""
import glob
import html as html_mod
import json
import pathlib
import re
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIST = ROOT / 'dist'
TRACKER_RAW = 'awinmid=68536&awinaffid=3124891'
TRACKER_ESC = 'awinmid=68536&amp;awinaffid=3124891'
ADDRESSED = {
    'badumbau-angebote-vergleichen': 'aroundhome_badumbau_angebote',
    'bad-umbau-barrierefrei': 'aroundhome_badumbau_angebote',
    'badumbau-kosten': 'aroundhome_badumbau_planung',
    'wanne-zur-dusche': 'aroundhome_badumbau_planung',
    'bodengleiche-dusche-altbau': 'aroundhome_badumbau_planung',
}
CTA_TEXTS = {
    'aroundhome_badumbau_angebote': ('Passende Fachbetriebe vergleichen',
                                     'Fachbetriebe für den barrierefreien Badumbau finden'),
    'aroundhome_badumbau_planung': ('Angebote für Ihren Badumbau einholen',
                                    'Badumbau: Angebote von regionalen Fachbetrieben einholen'),
}
FAILS = []
PASSES = 0


def check(name, cond, detail=''):
    global PASSES
    if cond:
        PASSES += 1
        print('PASS ' + name + ((' — ' + detail) if detail else ''))
    else:
        FAILS.append((name, detail))
        print('FAIL ' + name + ((' — ' + detail) if detail else ''))


def page_text(p):
    raw = p.read_text(encoding='utf-8')
    return raw, html_mod.unescape(raw)


# A: adressierte Seiten
for slug, pid in ADDRESSED.items():
    p = DIST / (slug + '.html')
    if not p.exists():
        check('exists:' + slug, False, 'Datei fehlt')
        continue
    raw, txt = page_text(p)
    check('marker:' + slug, 'data-partner-placement="' + pid + '"' in raw, pid)
    check('rel:' + slug, 'rel="sponsored noopener"' in raw)
    check('tracker-esc:' + slug, TRACKER_ESC in raw)
    check('tracker-raw-after-unescape:' + slug, TRACKER_RAW in txt)
    check('target:' + slug, 'target="_blank"' in raw)
    i = raw.find('data-partner-placement="' + pid + '"')
    check('cta-section:' + slug, i >= 0, 'Marker-Position')
    if i >= 0:
        block = html_mod.unescape(raw[max(0, i - 1200):i + 2600])
        cta, label = CTA_TEXTS[pid]
        check('anzeige:' + slug, 'Anzeige' in block)
        check('cta-text:' + slug, cta in block)
        check('label:' + slug, label in block)
        check('verguetungshinweis:' + slug, ('Vergütung' in block or 'unverbindlich' in block))
    # E: JSON-LD valide
    lds = re.findall(r'<script type="application/ld\+json">(.*?)</script>', raw, re.S)
    ok = True
    for ld in lds:
        try:
            json.loads(ld)
        except Exception as e:
            ok = False
            check('jsonld:' + slug, False, str(e)[:80])
    if ok:
        check('jsonld:' + slug, True, str(len(lds)) + ' Blocks')

# B: keine Aroundhome-Marker sonstwo
others = [f for f in glob.glob(str(DIST / '*.html')) + glob.glob(str(DIST / '*' / '*.html'))
          if pathlib.Path(f).stem not in ADDRESSED and 'datenschutz' not in f]
leaks = []
for f in others:
    raw = pathlib.Path(f).read_text(encoding='utf-8')
    if 'awinmid=68536' in raw or 'aroundhome_badumbau' in raw:
        leaks.append(f)
check('no-leak-on-other-pages', len(leaks) == 0, str(leaks[:4]) + ' (' + str(len(others)) + ' Seiten geprüft)')

# C: Malteser unverändert
p = DIST / 'hausnotruf-kosten-anbieter-vergleich.html'
raw, _ = page_text(p)
check('malteser-intact:tracker', raw.count('awinmid=112616') >= 2, str(raw.count('awinmid=112616')))
check('malteser-intact:pid1', 'malteser_beratungstermin' in raw)
check('malteser-intact:pid2', 'malteser_info_material' in raw)

# D: Datenschutz
p = DIST / 'datenschutz.html'
raw, txt = page_text(p)
check('dse:name', 'Aroundhome DE' in txt)
check('dse:desc', 'Badumbau-Vermittlung' in txt)
check('dse:cookie', 'Cookie-Laufzeit laut Programmprofil 30 Tage' in txt)
check('dse:checked', 'Profil geprüft am 25. November 2026' in txt)
check('dse:url', 'https://www.aroundhome.de/datenschutzerklaerung/' in txt)
check('dse:awin-netzwerk', 'Awin (Awin AG)' in txt)
check('dse:malteser-still-there', 'Aktuell beworbener Anbieter über Awin: Malteser' in txt)
check('dse:fallback-gone', 'Derzeit sind keine gekennzeichneten Empfehlungslinks' not in txt)
check('dse:sec5-variante', 'ausgehende Empfehlungslinks' in txt)
for n in range(1, 10):
    check('dse:sec-' + str(n), ('<h2>' + str(n) + '.' in raw))

# F: Sitemap + robots
p = DIST / 'sitemap.xml'
raw = p.read_text(encoding='utf-8')
locs = raw.count('<loc>')
live_locs = None
try:
    with urllib.request.urlopen('https://zuhausebleiben-kompass.de/sitemap.xml', timeout=30) as r:
        live_locs = r.read().decode('utf-8').count('<loc>')
except Exception as e:
    check('sitemap-live-fetch', False, str(e)[:80])
check('sitemap:size-unchanged', live_locs == locs, 'dist=' + str(locs) + ' live-vor-aktivierung=' + str(live_locs))
for slug in ADDRESSED:
    check('sitemap:keep:' + slug, ('/' + slug + '.html') in raw)
check('sitemap:keep:datenschutz', '/datenschutz.html' in raw)
p = DIST / 'badumbau-kosten.html'
raw, _ = page_text(p)
check('robots:launch-mode', 'name="robots" content="index, follow"' in raw or 'name="robots" content="index,follow"' in raw)

print('')
print('ERGEBNIS: ' + str(PASSES) + ' PASS, ' + str(len(FAILS)) + ' FAIL')
sys.exit(1 if FAILS else 0)
