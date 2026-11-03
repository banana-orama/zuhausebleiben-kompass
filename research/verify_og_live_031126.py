#!/usr/bin/env python3
"""Live-Readback Audit #6b/#10 auf der öffentlichen URL (nach CI + GH-Pages-Deploy)."""
import hashlib, json, struct, sys, time, urllib.request

BASE = 'https://zuhausebleiben-kompass.de'
OG = BASE + '/assets/images/og-zuhausebleiben-kompass.png'
results = []

def fetch(url, binary=False):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (readback)'})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
        return (r.status, dict(r.headers), data if binary else data.decode('utf-8', 'replace'))

def check(name, ok, detail=''):
    results.append((name, ok, detail))
    print(('PASS' if ok else 'FAIL') + f' {name} {detail}')

# 1) og:image PNG live: 200, PNG-Magic, gleiche Bytes wie lokal
st, hdr, body = fetch(OG, binary=True)
check('og.png HTTP 200', st == 200, f'status={st} type={hdr.get("Content-Type")} bytes={len(body)}')
local = open('assets/images/og-zuhausebleiben-kompass.png', 'rb').read()
check('og.png bytes identisch zum Repo', hashlib.sha256(body).hexdigest() == hashlib.sha256(local).hexdigest(),
      f'sha={hashlib.sha256(body).hexdigest()[:12]}')
check('og.png ist PNG >=1200x630', body[:8] == b'\x89PNG\r\n\x1a\n' and struct.unpack('>II', body[16:24])[0] >= 1200)

# 2) Home: Meta-Satz + robots + Consent-Deferral-Code live
st, hdr, home = fetch(BASE + '/')
check('home 200', st == 200)
check('home robots index,follow', 'name="robots" content="index,follow"' in home)
check('home og:image absolut', f'property="og:image" content="{OG}"' in home)
check('home og:image:width/height', 'property="og:image:width" content="1200"' in home and 'property="og:image:height" content="630"' in home)
check('home twitter:card', '<meta name="twitter:card" content="summary_large_image">' in home)
check('home referrer policy', '<meta name="referrer" content="strict-origin-when-cross-origin">' in home)
check('home og:url = canonical', 'rel="canonical" href="https://zuhausebleiben-kompass.de/"' in home and 'property="og:url" content="https://zuhausebleiben-kompass.de/"' in home)

# 3) consent.mjs live enthaelt die Deferral-Logik (Deploy-Beweis)
st, hdr, cm = fetch(BASE + '/assets/consent.mjs')
check('consent.mjs 200', st == 200)
check('consent.mjs enthaelt requestIdleCallback-Deferral', 'requestIdleCallback' in cm and 'earlyClicks' in cm)
check('consent.mjs bootstrap-Reihenfolge unveraendert (revision 2)', 'revision: 2' in cm)

# 4) Artikel: Article-JSON-LD image[0]=PNG + Metas
st, hdr, art = fetch(BASE + '/treppenlift-kosten.html')
check('artikel 200', st == 200)
check('artikel og:image', f'property="og:image" content="{OG}"' in art)
check('artikel Article.image[0] = PNG', '"image":["https://zuhausebleiben-kompass.de/assets/images/og-zuhausebleiben-kompass.png"' in art.replace(' ', ''))
check('artikel referrer+twitter', '<meta name="referrer" content="strict-origin-when-cross-origin">' in art and 'summary_large_image' in art)

# 5) Checklisten-Seite (zweiter Generator) traegt denselben Meta-Satz
st, hdr, cl = fetch(BASE + '/checklisten/index.html')
check('checklisten og:image+referrer', f'property="og:image" content="{OG}"' in cl and 'strict-origin-when-cross-origin' in cl)

# 6) Regression: Sitemap 36 locs, datenschutz weiter drin
st, hdr, sm = fetch(BASE + '/sitemap.xml')
locs = sm.count('<loc>')
check('sitemap 36 locs', locs == 36, f'locs={locs}')
check('datenschutz in sitemap', 'datenschutz.html' in sm)

fails = [r for r in results if not r[1]]
print(f"\n{len(results) - len(fails)}/{len(results)} PASS" + (' — ALL PASS' if not fails else f' — {len(fails)} FAIL'))
sys.exit(1 if fails else 0)
