#!/usr/bin/env python3
"""Prüflauf 16.11.2026: checked_at-Bump nur für heute real neu verifizierte Quellen
(§40 SGB XI, KfW 455-B, KfW 159, BMG Zuschüsse Wohnungsanpassung)
+ sichtbare KfW-Prüfdatumsangaben 9.→16. November 2026 in den 4 KfW-Artikeln
(durch heutigen curl-Volltext + Browser-Check belegt).

Zeilen-Zustandsautomat (kein JSON-Roundtrip): URL-Zeile merken, checked_at-Zeile
nur ersetzen, wenn die gemerkte URL heute im Prüfscope lag. Danach Diff-Sanity:
jede geänderte Zeile muss Datum-/Checked_at-Kontext haben.
"""
import glob
import re
import subprocess
import sys

ROOT = '/Users/mac/agentic-business/barrierefrei-leads'
OLD, NEW = '2026-11-09', '2026-11-16'
SCOPE = (
    'gesetze-im-internet.de/sgb_11/__40.html',
    'Altersgerecht-Umbauen-Investitionszuschuss-(455)',
    'Altersgerecht-Umbauen-(159)',
    'bundesgesundheitsministerium.de/pflege-zu-hause/zuschuesse-zur-wohnungsanpassung',
)
VISIBLE_FILES = {
    'bad-umbau-barrierefrei': 2,
    'bodengleiche-dusche-altbau': 2,
    'treppenlift-zuschuss': 2,
    'wanne-zur-dusche': 1,
}

changed_files, changed_ca, changed_vis = [], 0, 0
for f in sorted(glob.glob(f'{ROOT}/content-ready/*.json')):
    lines = open(f, encoding='utf-8').read().splitlines(keepends=True)
    cur_url = ''
    n_ca, n_vis = 0, 0
    for i, line in enumerate(lines):
        m = re.search(r'"url":\s*"([^"]+)"', line)
        if m:
            cur_url = m.group(1)
            continue
        if '"checked_at"' in line and cur_url and any(s in cur_url for s in SCOPE):
            new = line.replace(OLD, NEW)
            if new != line:
                lines[i] = new
                n_ca += 1
                continue  # URL bleibt gemerkt für nächste checked_at-Zeile? (nur 1 pro Source-Objekt)
    slug = f.rsplit('/', 1)[-1][:-5]
    if slug in VISIBLE_FILES:
        for i, line in enumerate(lines):
            new = line.replace('9. November 2026', '16. November 2026')
            if new != line:
                lines[i] = new
                n_vis += line.count('9. November 2026')
    if n_ca or n_vis:
        open(f, 'w', encoding='utf-8').write(''.join(lines))
        changed_files.append((slug, n_ca, n_vis))
        changed_ca += n_ca
        changed_vis += n_vis

print('Geänderte Dateien (slug, checked_at-Bumps, sichtbare-Datums-Bumps):')
for slug, a, b in changed_files:
    print(f'  {slug}: checked_at={a}, sichtbar={b}')
print(f'SUMME: {changed_ca} checked_at, {changed_vis} sichtbare Datumsangaben')
if changed_vis != sum(VISIBLE_FILES.values()):
    print(f'WARNUNG: sichtbare Bumps {changed_vis} != erwartet {sum(VISIBLE_FILES.values())}')
    sys.exit(1)

# ---- Diff-Sanity: nur Datumszeilen ----
r = subprocess.run(['git', '-C', ROOT, 'diff', '--', 'content-ready/'], capture_output=True, text=True)
bad = []
for line in r.stdout.splitlines():
    if line.startswith(('+', '-')) and not line.startswith(('+++', '---')):
        if not re.search(r'(checked_at|\d\. November 2026|2026-11-\d\d)', line):
            bad.append(line)
print(f'Diff-Sanity: {len(bad)} Fremd-Zeilen')
for b in bad:
    print('  !', b[:160])
sys.exit(1 if bad else 0)
