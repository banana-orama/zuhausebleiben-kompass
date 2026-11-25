#!/usr/bin/env python3
"""Öffentlicher Live-Readback der Aroundhome-Aktivierung (25.11.2026).

Poll auf den Deploy (Pages-Lag), dann gegen die ÖFFENTLICHE URL:
  5 Artikel mit placement (marker/rel/tracker/Anzeige), datenschutz-Spiegel,
  Malteser intakt, keine Leaks auf Fremdseiten, Sitemap 57, robots index,follow.
"""
import html as html_mod
import sys
import time
import urllib.request

BASE = 'https://zuhausebleiben-kompass.de/'
ADDRESSED = {
    'badumbau-angebote-vergleichen.html': 'aroundhome_badumbau_angebote',
    'bad-umbau-barrierefrei.html': 'aroundhome_badumbau_angebote',
    'badumbau-kosten.html': 'aroundhome_badumbau_planung',
    'wanne-zur-dusche.html': 'aroundhome_badumbau_planung',
    'bodengleiche-dusche-altbau.html': 'aroundhome_badumbau_planung',
}
NO_LEAK = ['treppenlift-kosten.html', 'index.html', 'hausnotruf-kosten-anbieter-vergleich.html',
           'treppenlift-zuschuss.html', 'region/baden-wuerttemberg.html']
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


def get(path, timeout=30):
    req = urllib.request.Request(BASE + path, headers={'User-Agent': 'Mozilla/5.0 (readback-verify)'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode('utf-8', 'replace')


# Poll auf Deploy: badumbau-kosten muss den aroundhome-Marker tragen
deployed = False
for attempt in range(20):
    try:
        st, raw = get('badumbau-kosten.html')
        if st == 200 and 'awinmid=68536' in raw:
            deployed = True
            print('Deploy sichtbar nach Poll ' + str(attempt + 1))
            break
    except Exception:
        pass
    time.sleep(15)
check('deploy-visible', deployed)

for slug, pid in ADDRESSED.items():
    try:
        st, raw = get(slug)
    except Exception as e:
        check('fetch:' + slug, False, str(e)[:60])
        continue
    txt = html_mod.unescape(raw)
    check('status:' + slug, st == 200, str(st))
    check('marker:' + slug, 'data-partner-placement="' + pid + '"' in raw, pid)
    check('rel:' + slug, 'rel="sponsored noopener"' in raw)
    check('tracker:' + slug, 'awinmid=68536&awinaffid=3124891' in txt)
    i = raw.find('data-partner-placement="' + pid + '"')
    if i >= 0:
        block = html_mod.unescape(raw[max(0, i - 1200):i + 2600])
        check('anzeige:' + slug, 'ANZEIGE' in block.upper())
    check('robots:' + slug, ('noindex' not in raw.lower()[:1200]))

st, raw = get('datenschutz.html')
txt = html_mod.unescape(raw)
check('dse:status', st == 200)
check('dse:name', 'Aroundhome DE' in txt)
check('dse:desc', 'Badumbau-Vermittlung' in txt)
check('dse:checked', 'Profil geprüft am 25. November 2026' in txt)
check('dse:url', 'https://www.aroundhome.de/datenschutzerklaerung/' in txt)
check('dse:malteser', 'Aktuell beworbener Anbieter über Awin: Malteser' in txt)
check('dse:fallback-gone', 'Derzeit sind keine gekennzeichneten Empfehlungslinks' not in txt)

st, raw = get('hausnotruf-kosten-anbieter-vergleich.html')
check('malteser-live:intact', raw.count('awinmid=112616') >= 2, str(raw.count('awinmid=112616')))
check('malteser-live:no-aroundhome', 'awinmid=68536' not in raw)

leaks = []
for slug in NO_LEAK:
    try:
        st, raw = get(slug)
        if 'awinmid=68536' in raw or 'aroundhome_badumbau' in raw:
            leaks.append(slug)
    except Exception:
        leaks.append(slug + ' (fetch)')
check('no-leak-live', len(leaks) == 0, str(leaks))

st, raw = get('sitemap.xml')
check('sitemap:57-locs', raw.count('<loc>') == 57, str(raw.count('<loc>')))

print('')
print('ERGEBNIS: ' + str(PASSES) + ' PASS, ' + str(len(FAILS)) + ' FAIL')
sys.exit(1 if FAILS else 0)
