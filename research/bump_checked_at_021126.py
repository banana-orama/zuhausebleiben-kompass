#!/usr/bin/env python3
"""Förder-Prüflauf 02.11.2026: stellt checked_at → 2026-11-02 NUR für die heute
tatsächlich inhaltlich neu verifizierten Quellen (§ 40 SGB XI, KfW 455-B, KfW 159,
BMG Wohnungsanpassung) in allen zitierenden Artikeln.

Läuft VOR der URL-Normalisierung (Marker decken die aktuell im Content
stehenden URL-Formen). Technik: zeilenbasierter Zustandsautomat statt
json.dumps-Roundtrip (der würde kompakte Arrays expandieren).
"""
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEW_DATE = '2026-11-02'
TARGET_MARKERS = [
    'gesetze-im-internet.de/sgb_11/__40.html',
    'kfw.de/inlandsfoerderung/Privatpersonen/Bestandsimmobilie/F%C3%B6rderprodukte/Altersgerecht-Umbauen-Investitionszuschuss-(455)/',
    'kfw.de/inlandsfoerderung/Privatpersonen/Bestehende-Immobilie/Förderprodukte/Altersgerecht-Umbauen-(159)',
    'kfw.de/inlandsfoerderung/Privatpersonen/Bestehende-Immobilie/F%C3%B6rderprodukte/Altersgerecht-Umbauen-(159)',
    'bundesgesundheitsministerium.de/pflege-zu-hause/zuschuesse-zur-wohnungsanpassung',
]
CHECKED_RE = re.compile(r'("checked_at":\s*")(\d{4}-\d{2}-\d{2})(")')

changed = {}
for fp in sorted(glob.glob(os.path.join(ROOT, 'content-ready', '*.json'))):
    slug = os.path.basename(fp)[:-5]
    lines = open(fp, encoding='utf-8').read().splitlines(keepends=True)
    pending = False
    edits = []
    for i, line in enumerate(lines):
        if any(m in line for m in TARGET_MARKERS):
            pending = True
            continue
        if pending and '"checked_at"' in line:
            m = CHECKED_RE.search(line)
            if m and m.group(2) != NEW_DATE:
                edits.append((i + 1, m.group(2)))
                lines[i] = CHECKED_RE.sub(r'\g<1>' + NEW_DATE + r'\g<3>', line)
            pending = False
    if edits:
        open(fp, 'w', encoding='utf-8').write(''.join(lines))
        changed[slug] = edits

total = 0
for slug, edits in sorted(changed.items()):
    total += len(edits)
    print(f'{slug}: {len(edits)} Quelle(n) → {NEW_DATE} (vorher: {", ".join(d for _, d in edits)})')
print(f'\nGESAMT: {total} checked_at-Felder in {len(changed)} Artikeln aktualisiert')
