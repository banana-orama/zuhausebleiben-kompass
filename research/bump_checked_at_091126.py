#!/usr/bin/env python3
"""Förder-Prüflauf 09.11.2026 — zwei Operationen, beide nur für heute tatsächlich
neu verifizierte Quellen:

1. checked_at → 2026-11-09 für § 40 SGB XI, KfW 455-B, KfW 159, BMG Wohnungsanpassung
   (heute: 33 curl-Assertionen PASS + Browser-Check 11/11).
   Marker als Teilstrings, decken Umlaut- UND encodierte URL-Formen.
   Technik: zeilenbasierter Zustandsautomat statt json.dumps-Roundtrip.
2. Sichtbare KfW-Prüfdatumsangaben „2. November 2026" → „9. November 2026" in den
   4 KfW-Artikeln (7 Sätze; heute per curl UND Chromium-Browser belegt — der Satz in
   treppenlift-zuschuss behauptet explizit „direkt im Browser geprüft").
   NICHT ersetzt: Gesamtdisclaimer „Stand: 2. November 2026" in wohnumfeldverbesserung
   (breiteres Quellenset heute nur per Link-Status geprüft — kein Überclaiming).
"""
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEW_DATE = '2026-11-09'
TARGET_MARKERS = [
    'gesetze-im-internet.de/sgb_11/__40.html',
    'Altersgerecht-Umbauen-Investitionszuschuss-(455)',
    'Altersgerecht-Umbauen-%28455%29',
    'Altersgerecht-Umbauen-(159)',
    'Altersgerecht-Umbauen-%28159%29',
    'bundesgesundheitsministerium.de/pflege-zu-hause/zuschuesse-zur-wohnungsanpassung',
]
CHECKED_RE = re.compile(r'("checked_at":\s*")(\d{4}-\d{2}-\d{2})(")')
OLD = '2. November 2026'
NEW = '9. November 2026'
EXPECTED_DATE_BUMPS = {
    'bad-umbau-barrierefrei': 2,
    'bodengleiche-dusche-altbau': 2,
    'treppenlift-zuschuss': 2,
    'wanne-zur-dusche': 1,
}

fail = []

# ---- 1) checked_at ----
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
    print(f'{slug}: {len(edits)} Quelle(n) checked_at → {NEW_DATE} (vorher: {", ".join(d for _, d in edits)})')
print(f'GESAMT: {total} checked_at-Felder in {len(changed)} Artikeln aktualisiert')

# ---- 2) sichtbare KfW-Datumssätze ----
print()
bumped = {}
for slug, expected in EXPECTED_DATE_BUMPS.items():
    fp = os.path.join(ROOT, 'content-ready', slug + '.json')
    txt = open(fp, encoding='utf-8').read()
    n = txt.count(OLD)
    if n != expected:
        fail.append(f'{slug}: erwartet {expected}× "{OLD}", gefunden {n} — Abbruch ohne Änderung')
        continue
    open(fp, 'w', encoding='utf-8').write(txt.replace(OLD, NEW))
    bumped[slug] = n
    print(f'{slug}: {n} sichtbare KfW-Prüfdaten "{OLD}" → "{NEW}"')

# wohnumfeldverbesserung MUSS seinen Gesamtdisclaimer behalten
fp = os.path.join(ROOT, 'content-ready', 'wohnumfeldverbesserung-beantragen.json')
cnt = open(fp, encoding='utf-8').read().count(OLD)
print(f'wohnumfeldverbesserung-beantragen: Gesamtdisclaimer "{OLD}" erhalten = {cnt}× (erwartet 1)')
if cnt != 1:
    fail.append(f'wohnumfeldverbesserung: Gesamtdisclaimer count {cnt} ≠ 1')

# Restprüfung: keine "2. November 2026" mehr außer dem Disclaimer
rest = 0
for fp in glob.glob(os.path.join(ROOT, 'content-ready', '*.json')):
    rest += open(fp, encoding='utf-8').read().count(OLD)
if rest != 1:
    fail.append(f'Restprüfung: noch {rest}× "{OLD}" in content-ready (erwartet nur 1 = wohnumfeldverbesserung)')
else:
    print(f'Restprüfung OK: {rest}× "{OLD}" verbleibend (nur wohnumfeldverbesserung-Disclaimer)')

if fail:
    print('\nFEHLER:')
    for f in fail:
        print(f'  {f}')
    raise SystemExit(1)
print('\nBump abgeschlossen: alle Ersetzungen exakt wie erwartet.')
