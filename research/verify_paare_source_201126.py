#!/usr/bin/env python3
"""Acceptance v2: full ledger quote check (incl. raw-HTML evidence) + fixed needles + [7] cited."""
import json, re, sys, unicodedata
from pathlib import Path

ROOT = Path('.')
ok = True
def check(name, cond, detail=''):
    global ok
    print(('PASS' if cond else 'FAIL'), '|', name, ('| ' + str(detail)[:120] if detail else ''))
    if not cond: ok = False

def norm(s):
    s = unicodedata.normalize('NFKC', s)
    s = s.replace('\u00ad', '')
    s = s.replace('„', '"').replace('“', '"').replace('”', '"').replace('‚', "'").replace('‘', "'").replace('’', "'")
    s = re.sub(r'\s+', ' ', s)
    return s.lower()

def flat(p):
    t = Path(p).read_text(errors='replace')
    t = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', t, flags=re.S)
    t = re.sub(r'<[^>]+>', ' ', t)
    for a, b in (('&nbsp;', ' '), ('&auml;', 'ä'), ('&ouml;', 'ö'), ('&uuml;', 'ü'), ('&szlig;', 'ß'),
                 ('&quot;', '"'), ('&#8222;', '"'), ('&#8220;', '"'), ('&#8221;', '"')):
        t = t.replace(a, b)
    return t

EV = Path('research/evidence/paare-191126')
EVFILES = {
    'malteser.de/hausnotruf.html': EV / 'malteser.txt',
    'verbraucherzentrale.de': EV / 'vz-10566.txt',
    'gkv-spitzenverband.de/media/dokumente': EV / 'gkv-hn-vertrag.txt',
    'gkv-spitzenverband.de/pflegeversicherung/pflegehilfsmittelvertraege': EV / 'raw-gkv-phmv.html',
    'gkv-90prozent.de': EV / 'raw-gkv-90prozent.html',
    'drk.de': EV / 'drk-bv.txt',
    'johanniter.de': EV / 'johanniter.txt',
    'pflege-panorama.de': EV / 'pflege-panorama.txt',
}
led = json.loads(Path('research/paare-191126-ledger.json').read_text())
qtotal = qok = 0
for src in led['sources']:
    u = src['url']; qs = src.get('quotes', [])
    if not qs:
        print('  · no quotes:', u[:70]); continue
    f = None
    for pat, path in EVFILES.items():
        if pat in u: f = path; break
    if f is None or not f.exists():
        check(f"evidence for ledger[{src['id']}] {u[:50]}", False, str(f)); continue
    hay = norm(flat(f))
    for q in qs:
        qtotal += 1
        hit = norm(q['text']) in hay
        qok += 1 if hit else 0
        if not hit:
            check(f"quote[ledger {src['id']}] in {f.name}", False, q['text'][:100])
check('ALL ledger quotes verbatim (8/8 sources)', qok == qtotal and qtotal > 0, f'{qok}/{qtotal}')

art = json.loads(Path('content-ready/hausnotruf-fuer-paare.json').read_text())
alltxt = json.dumps(art, ensure_ascii=False)
cited = sorted(set(int(m) for m in re.findall(r'\[(\d)\]', alltxt)))
check('citation ids 1-8 all used', cited == list(range(1, 9)), str(cited))

gkv = norm(flat(EV / 'gkv-hn-vertrag.txt'))
vz = norm(flat(EV / 'vz-10566.txt'))
p90 = norm(flat(EV / 'raw-gkv-90prozent.html'))
drk = norm(flat(EV / 'drk-bv.txt'))
pp = norm(flat(EV / 'pflege-panorama.txt'))
joh = norm(flat(EV / 'johanniter.txt'))
check('Vertrag: 27,00 EUR netto', '27,00 eur' in gkv)
check('Vertrag: Produktgruppe 52', 'produktgruppe 52' in gkv)
check('Vertrag: Mehrkosten/Aufzahlung §33+§40', re.search(r'33 absatz 1 satz 9 sgb v.{0,80}40 absatz 1 satz 3 sgb xi.{0,120}mehrkosten', gkv) is not None)
check('VZ: oft und länger abwesend', 'oft und länger abwesend' in vz)
check('VZ: fast den ganzen Tag allein', 'fast den ganzen tag allein' in vz)
check('VZ: Basistarif 27 und 40 Euro', ('27 und 40 euro' in vz))
check('VZ: Pflegekasse bis zu 27 Euro', 'bis zu 27 euro' in vz)
check('90prozent: Mindestlaufzeit zwei Jahren', 'mindestlaufzeit von zwei jahren' in p90)
check('90prozent: 1. April 2026 in Kraft', re.search(r'1\. april 2026\s*kraft getreten', p90) is not None)
check('DRK: ein Handsender, ein Basisgerät', 'ein handsender' in drk and 'ein basisger' in drk)
check('pflege-panorama: 54 Euro', '54 euro' in pp)
check('Johanniter: Basisstation+Handsender+Mobilgerät', 'basisstation mit stoß- und wasserfestem handsender' in joh and 'mobilgerät geliefert' in joh)
check('Demenz-Grenze bei VZ', 'demenz' in vz)
check('checked_at 2026-11-19 on all 8 sources', all(s.get('checked_at') == '2026-11-19' for s in art['sources']))
for slug in ('hausnotruf-kosten-anbieter-vergleich', 'hausnotruf-alarm-ablauf', 'hausnotruf-angehoerige-einrichten'):
    check(f'related slug exists: {slug}', (ROOT / 'content-ready' / f'{slug}.json').exists())
src_svg = ROOT / 'assets/images/hausnotruf-paare-konstellationen.svg'
check('src svg exists + equals committed dist copy', src_svg.exists() and (ROOT / 'dist/assets/images/hausnotruf-paare-konstellationen.svg').read_bytes() == src_svg.read_bytes())

print('\nRESULT:', 'ALL PASS' if ok else 'FAILURES PRESENT')
sys.exit(0 if ok else 1)
