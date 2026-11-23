#!/usr/bin/env python3
"""Prüflauf 23.11.2026 — Content-Fixes + Prüfdaten-Bump.

1) Link-Rot-Fix hausnotruf-angehoerige-einrichten:
   Die zitierte VZ-Veranstaltungsseite (…/veranstaltungen/fuer-den-ernstfall-gewappnet-…-123149,
   checked 2026-11-10) ist nach Event-Ende 404 (Wayback-Snapshot 09.11.2026: 200 + Verbatim-Zitat
   belegt). Ersatz: durable VZ-Wissenseite /vorsorgevollmacht (Abruf heute 200, „Stand:
   21. September 2026"), die dieselbe Aussage trägt („Das aber geht nur mit einer
   ausdrücklichen Vollmacht."). Die beiden Verbatim-Flüsterzitate werden daher zu Paraphrasen
   ohne Anführungszeichen — nichts behauptet mehr wörtliche Unterstützung durch eine tote Seite.
2) checked_at-Bump NUR für heute real neu verifizierte Quellen (§40 SGB XI, EStG §35a,
   KfW 455-B, KfW 159, BMG Wohnungsanpassung, NRW.BANK, StMB) → 2026-11-23.
3) Sichtbare KfW-Abrufdaten 16./18. November → 23. November 2026 (durch heutigen
   curl-Volltext 47/47 + Browser-Check 11/11 belegt).

Zeilen-/String-Replace ohne JSON-Roundtrip. Exit 1 bei falschen Trefferzählern.
"""
import glob
import re
import subprocess
import sys

ROOT = '/Users/mac/agentic-business/barrierefrei-leads'
TODAY_ISO = '2026-11-23'

# ---------- 1) VZ-Link-Rot-Fix ----------
F = f'{ROOT}/content-ready/hausnotruf-angehoerige-einrichten.json'
raw = open(F, encoding='utf-8').read()

SWAPS = [
    # Fließtext: Verbatim-Zitat (tote Seite) → Paraphrase (live Seite)
    ('auch Sorge allein ist kein Vertretungsrecht: „In dieser Situation braucht es eine rechtliche Vertretung – weder Ehepartner noch Kinder können dies automatisch übernehmen.“[7]',
     'auch Sorge allein ist kein Vertretungsrecht: Ehepartner und Kinder vertreten nicht automatisch — rechtlich geht es nur mit einer ausdrücklichen Vollmacht.[7]'),
    # FAQ: Teil-Verbatim → Paraphrase
    ('dafür „braucht es eine rechtliche Vertretung“ wie eine Vorsorgevollmacht oder Betreuung.[7]',
     'dafür braucht es eine ausdrückliche Vollmacht, etwa eine Vorsorgevollmacht oder Betreuung.[7]'),
    # Quelle [7]: tote Veranstaltungseite → durable Wissenseite
    ('"title": "Verbraucherzentrale (Veranstaltungsseite): Für den Ernstfall gewappnet — Wissenswertes zur Vorsorgevollmacht"',
     '"title": "Verbraucherzentrale – Vorsorgevollmacht: Warum sie so wichtig ist"'),
    ('"url": "https://www.verbraucherzentrale.de/veranstaltungen/fuer-den-ernstfall-gewappnet-wissenswertes-zur-vorsorgevollmacht-123149"',
     '"url": "https://www.verbraucherzentrale.de/vorsorgevollmacht"'),
]
for old, new in SWAPS:
    n = raw.count(old)
    if n != 1:
        print(f'ABBRUCH: VZ-Swap Treffer {n} != 1 für: {old[:80]}…')
        sys.exit(1)
    raw = raw.replace(old, new)
# checked_at der getauschten Quelle (Zeilen-Zustandsmaschine: nur checked_at-Zeile
# NACH der /vorsorgevollmacht-url-Zeile — 2026-11-10 tragen heute 7 Quellen).
lines = raw.splitlines(keepends=True)
hit = 0
cur_vz = False
for i, line in enumerate(lines):
    if '"url": "https://www.verbraucherzentrale.de/vorsorgevollmacht"' in line:
        cur_vz = True
        continue
    if cur_vz and '"checked_at"' in line:
        new = re.sub(r'"checked_at":\s*"2026-\d\d-\d\d"', f'"checked_at": "{TODAY_ISO}"', line)
        if new == line:
            print('ABBRUCH: checked_at-Zeile nach VZ-URL trug kein 2026-Datum')
            sys.exit(1)
        lines[i] = new
        hit += 1
        cur_vz = False
if hit != 1:
    print(f'ABBRUCH: VZ checked_at-Ersatz {hit} != 1')
    sys.exit(1)
raw = ''.join(lines)
open(F, 'w', encoding='utf-8').write(raw)
print(f'VZ-Fix: {len(SWAPS)} String-Swaps + checked_at → {TODAY_ISO} OK')
subprocess.run(['python3', '-m', 'json.tool', F], capture_output=True, check=True)

# ---------- 2) checked_at-Bump (URL-Scope = heute verifiziert) ----------
SCOPE = (
    'gesetze-im-internet.de/sgb_11/__40.html',
    'Altersgerecht-Umbauen-Investitionszuschuss-(455)',
    'Altersgerecht-Umbauen-(159)',
    'bundesgesundheitsministerium.de/pflege-zu-hause/zuschuesse-zur-wohnungsanpassung',
    'nrwbank.de/de/privatpersonen/wohneigentum-gestalten/barrierefrei-umbauen',
    'stmb.bayern.de/wohnen/wohnraum_nutzen/barrierefreieswohnen/',
    'gesetze-im-internet.de/estg/__35a.html',
)
total_ca = 0
for f in sorted(glob.glob(f'{ROOT}/content-ready/*.json')):
    lines = open(f, encoding='utf-8').read().splitlines(keepends=True)
    cur_url = ''
    n_ca = 0
    for i, line in enumerate(lines):
        m = re.search(r'"url":\s*"([^"]+)"', line)
        if m:
            cur_url = m.group(1)
            continue
        if '"checked_at"' in line and cur_url and any(s in cur_url for s in SCOPE):
            new = re.sub(r'"checked_at":\s*"2026-\d\d-\d\d"', f'"checked_at": "{TODAY_ISO}"', line)
            if new != line:
                lines[i] = new
                n_ca += 1
    if n_ca:
        open(f, 'w', encoding='utf-8').write(''.join(lines))
        total_ca += n_ca
        print(f'checked_at {f.split("/")[-1]}: {n_ca}')
print(f'checked_at gesamt: {total_ca}')

# ---------- 3) sichtbare Abrufdaten ----------
VISIBLE = {
    'bad-umbau-barrierefrei.json': [('"16. November 2026"', '"23. November 2026"', 2)],
    'bodengleiche-dusche-altbau.json': [('"16. November 2026"', '"23. November 2026"', 2)],
    'wanne-zur-dusche.json': [('"16. November 2026"', '"23. November 2026"', 1)],
    'treppenlift-zuschuss.json': [
        ('"18. November 2026"', '"23. November 2026"', 3),
        ('"Status am 18.11.2026"', '"Status am 23.11.2026"', 1),
    ],
}
for fname, rules in VISIBLE.items():
    f = f'{ROOT}/content-ready/{fname}'
    raw = open(f, encoding='utf-8').read()
    for old, new, expect in rules:
        n = raw.count(old)
        if n != expect:
            print(f'ABBRUCH: {fname} Treffer {n} != {expect} für {old}')
            sys.exit(1)
        raw = raw.replace(old, new)
        print(f'sichtbar {fname}: {old} x{n} → {new}')
    open(f, 'w', encoding='utf-8').write(raw)
    subprocess.run(['python3', '-m', 'json.tool', f], capture_output=True, check=True)

print('FIX+BUMP abgeschlossen.')
