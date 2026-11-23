#!/usr/bin/env python3
"""Content-Gate: treppenlift-eigentumswohnung-weg (23.11.2026).
Läuft gegen LAUNCH-Dist (npm run build:launch vorher!). Checks:
- robots/canonical/title/H1, Quellenstand
- Kernwortlaute (tag-/citation-normalisiert, nach schmale-treppe-Lektion)
- Zitations-Marker [1]..[14], Quellen-Anker source-1..14, keine [15]+
- Related exakt 3 in konfigurierter Reihenfolge (absolute URLs)
- Early-CTA compare_top Ziel + Label
- Absenzen: V ZR 140/VIII ZR unverified-Urteile, Förderbeträge, Partner-Marker, Entwurf-Prosa, em-dash in Article-JSON
- Key-Coverage: alle Absätze/Bullets/Tabellenzellen/FAQs im Built-HTML
"""
import html, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIST = ROOT / 'dist'
SLUG = 'treppenlift-eigentumswohnung-weg'
fails, checks = [], 0

def check(name, cond, detail=''):
    global checks
    checks += 1
    if not cond:
        fails.append(f'{name} :: {detail}')

def norm(s):
    s = html.unescape(s)
    s = re.sub(r'<sup[^>]*>.*?</sup>', ' ', s, flags=re.S)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = re.sub(r'\[\d+\]', ' ', s)  # citation markers auf BEIDEN Seiten strippen
    s = s.replace('\u2014', ' ')
    return ' '.join(s.split())

raw = (DIST / f'{SLUG}.html').read_text(encoding='utf-8')
n = norm(raw)

check('robots index,follow', 'index,follow' in raw, raw[raw.find('name="robots"'):raw.find('name="robots"')+60])
check('canonical', f'{SLUG}.html' in re.search(r'rel="canonical" href="([^"]+)"', raw).group(1))
check('title', '<title>Treppenlift in der Eigentumswohnung — ZuhauseBleiben Kompass</title>' in raw)
check('h1', 'Treppenlift in der Eigentumswohnung: Der Weg zum Beschluss nach § 20 WEG' in n)
check('Quellenstand 2026-11-23', '2026-11-23' in raw)

NEEDLES = [
    'können beschlossen oder einem Wohnungseigentümer durch Beschluss gestattet werden',
    'Dafür ist es „ohne Belang“',
    'jeweils mit einfacher Stimmenmehrheit',
    'jedenfalls Zweifel hieran hegen',
    'Nur ihm gebühren die Nutzungen',
    '150 bis 300 Euro',
    'mit ärztlichen Attesten oder Gutachten',
    'ist ein WEG-Beschluss erforderlich',
    'ohne Beschluss darf nicht gebaut werden',
    '65 Zentimeter erhöhten Terrasse',
    'V ZR 244/22',
    'V ZR 33/23',
    'auf eigene Kosten einen Treppenlift im Treppenhaus',
    'nicht extrem entstellt',
    'Beschlussersetzungsklage',
    'grundlegend umgestalten oder einen Wohnungseigentümer ohne sein Einverständnis gegenüber anderen unbillig benachteiligen',
    'mehr als zwei Dritteln der abgegebenen Stimmen und der Hälfte aller Miteigentumsanteile',
    'Der Einbau erfolgt durch einen Fachbetrieb unter Beachtung der brandschutzrechtlichen Vorgaben',
]
for needle in NEEDLES:
    check(f'needle: {needle[:50]}', norm(needle) in n)

# Absenzen
for gone in ['V ZR 140', 'VIII ZR', '4.180', '16.720', '6.250', 'data-partner-placement', 'awin1.com',
             'Entwurf zur ersten Orientierung', 'vermitteln aktuell Angebote', 'sicher geld']:
    check(f'absent: {gone}', gone not in n, f'{n.count(gone)}x gefunden')

# Article-JSON em-dash-frei (Template-Chrome ausgenommen)
jtext = (ROOT / 'content-ready' / f'{SLUG}.json').read_text(encoding='utf-8')
check('Article-JSON em-dash-frei', '\u2014' not in jtext, f"{jtext.count(chr(8212))}x U+2014")

# Zitations-Marker: [1]..[14] benutzt, keine [15]+
used = set(int(m) for m in re.findall(r'\[(\d+)\]', jtext))
check('alle 14 Quellen zitiert', used == set(range(1, 15)), f'genutzt: {sorted(used)}')
built_markers = set(int(m) for m in re.findall(r'\[(\d+)\]</a>', raw))
check('built markers == used', built_markers == used, f'built: {sorted(built_markers)}')
for i in range(1, 15):
    check(f'anchor source-{i}', f'id="source-{i}"' in raw)

# Related: exakt 3, Reihenfolge mietwohnung -> wohnumfeld -> kosten
mrel = re.search(r'<section class="related"><h2>Passend dazu</h2><ul>(.*?)</ul>', raw, re.S)
check('related section present', bool(mrel))
if mrel:
    rels = re.findall(r'href="https://zuhausebleiben-kompass\.de/([a-z\-]+)\.html"', mrel.group(1))
    check('related count 3', len(rels) == 3, str(rels))
    check('related order', rels == ['treppenlift-mietwohnung', 'wohnumfeldverbesserung-beantragen', 'treppenlift-kosten'], str(rels))

# Early-CTA
mcta = re.search(r'data-cta-id="compare_top"[^>]*>([^<]+)', raw)
mhref = re.search(r'href="([^"]+)" data-cta-id="compare_top"', raw) or re.search(r'<a class="text-link" href="([^"]+)"[^>]*data-cta-id="compare_top"', raw)
check('compare_top href', bool(mhref) and mhref.group(1).endswith('/treppenlift-firmen-vergleich.html'), str(mhref.group(1) if mhref else None))
check('compare_top label', bool(mcta) and 'Anbieter für den Einbau vergleichen' in mcta.group(1), str(mcta.group(1) if mcta else None))
check('checklist CTA anchor', 'Zur Checkliste' in raw and 'abschnitt-6' in raw)

# Key-Coverage: alle Fließtexte aus dem JSON im Built-HTML
art = json.loads(jtext)
def flat_text(o):
    out = []
    if isinstance(o, str):
        out.append(o)
    elif isinstance(o, dict):
        for v in o.values():
            out.extend(flat_text(v))
    elif isinstance(o, list):
        for v in o:
            out.extend(flat_text(v))
    return out
for frag in flat_text([art['intro'], art['sections'], art['faqs']]):
    frag = frag.strip()
    if len(frag) < 12 or frag.endswith('*') is False and not any(c in frag for c in 'aeiouäöü'):
        pass
    f = norm(frag)
    if len(f) >= 12:
        check(f'coverage: {f[:48]}...', f in n)

# FAQPage-Schema: 6 Fragen
schema_texts = re.findall(r'<script type="application/ld\+json">(.*?)</script>', raw, re.S)
check('ein ld+json block', len(schema_texts) == 1, str(len(schema_texts)))
sch = json.loads(schema_texts[0])
faq = [x for x in sch['@graph'] if x.get('@type') == 'FAQPage']
check('FAQPage schema', len(faq) == 1)
if faq:
    qs = [q['name'] for q in faq[0]['mainEntity']]
    check('FAQ 6 Fragen', len(qs) == 6, str(len(qs)))
    for q in qs:
        check(f'FAQ-Frage im Body: {q[:40]}', norm(q) in n)

# Sitemap-Mitgliedschaft
sm = (DIST / 'sitemap.xml').read_text(encoding='utf-8')
check('in Sitemap', f'{SLUG}.html' in sm)

print(f'checks: {checks}, fails: {len(fails)}')
for f in fails:
    print('FAIL:', f)
sys.exit(1 if fails else 0)
