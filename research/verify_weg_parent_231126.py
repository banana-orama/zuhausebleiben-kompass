#!/usr/bin/env python3
"""Parent verification: re-check delegated WEG quotes against raw originals + live law pages.
Needles are the article's headline claims — each must appear verbatim in the cleaned raw text,
and the live law pages must still return 200 with the needle content today."""
import json, subprocess, sys, unicodedata

BASE = 'research/evidence/weg-231126'
fails, checks = [], 0

def clean(s):
    # collapse whitespace the same way the ledger builder did
    return ' '.join(s.split())

def norm_live(b):
    # live pages: ISO-8859-1 handled by curl+iconv below; normalize nbsp/soft-hyphen/whitespace
    b = b.replace('\u00ad', '').replace('\u00a0', ' ').replace('\u202f', ' ')
    import html as h
    b = h.unescape(b)
    return clean(b)

# 1) ledger-legal.json quotes verbatim in raw cleaned files
led = json.load(open(f'{BASE}/ledger-legal.json'))
print(f'ledger entries: {len(led)}')
raw_map = {
    '__20': f'{BASE}/raw/wegg__20.txt',
    '__21': f'{BASE}/raw/wegg__21.txt',
    '__44': f'{BASE}/raw/wegg__44.txt',
    'full': f'{BASE}/raw/wegg-full.txt',
    'vzr244': f'{BASE}/raw/vzr-244-22.flat.txt',
    'vzr33': f'{BASE}/raw/vzr-33-23.flat.txt',
    'pm': f'{BASE}/raw/pm-026-2024.txt',
}
raw_cache = {k: clean(open(p, encoding='utf-8').read()) for k, p in raw_map.items()}
url_to_raw = [
    ('woeigg/__20', '__20'), ('woeigg/__21', '__21'), ('woeigg/__44', '__44'),
    ('woeigg/BJNR', 'full'), ('V_ZR_244-22', 'vzr244'), ('V_ZR__33-23', 'vzr33'),
    ('2024026', 'pm'),
]
for e in led:
    checks += 1
    q = clean(e['quote'])
    tag = next((k for pat, k in url_to_raw if pat in e['url']), None)
    if not tag or q not in raw_cache[tag]:
        fails.append(f"ledger quote NOT in raw [{tag}]: {e['source_id']} :: {q[:80]}")
print(f'ledger->raw verbatim: {checks} checks, {len(fails)} fails')

# 2) live re-fetch of the three law pages + PM — needles TODAY
live_needles = {
    'https://www.gesetze-im-internet.de/woeigg/__20.html': [
        'dem Gebrauch durch Menschen mit Behinderungen',
        'grundlegend umgestalten oder einen Wohnungseigentümer ohne sein Einverständnis gegenüber anderen unbillig benachteiligen',
        'Stromerzeugung durch Steckersolargeräte',
    ],
    'https://www.gesetze-im-internet.de/woeigg/__21.html': [
        'hat dieser Wohnungseigentümer zu tragen',
        'Nur ihm gebühren die Nutzungen',
    ],
    'https://www.gesetze-im-internet.de/woeigg/__44.html': [
        'Beschlussersetzungsklage',
    ],
    'https://www.bundesgerichtshof.de/SharedDocs/Pressemitteilungen/DE/2024/2024026.html': [
        'jedenfalls Zweifel hieran hegen',
        'einfacher Stimmenmehrheit',
        'grundsätzlich ohne Bedeutung',
    ],
}
for url, needles in live_needles.items():
    r = subprocess.run(['curl', '-sL', '--max-time', '45', url], capture_output=True)
    body = r.stdout
    if r.returncode != 0 or not body:
        fails.append(f'LIVE fetch failed: {url} rc={r.returncode}')
        continue
    enc = 'iso-8859-1' if 'gesetze-im-internet' in url else 'utf-8'
    text = norm_live(body.decode(enc, errors='replace'))
    txt_only = __import__('re').sub(r'<[^>]+>', ' ', text)
    for n in needles:
        checks += 1
        nn = clean(__import__('re').sub(r'<[^>]+>', ' ', norm_live(n)))
        if nn not in txt_only:
            fails.append(f'LIVE needle MISSING at {url}: {n[:90]}')
print(f'total checks: {checks}, total fails: {len(fails)}')
for f in fails:
    print('FAIL:', f)
sys.exit(1 if fails else 0)
