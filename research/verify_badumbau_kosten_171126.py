# Ledger-Verifikation badumbau-kosten (17.11.2026)
# Prueft: alle Zitate verbatim in den Evidenz-.txt (Soft-Hyphen/Entity-normalisiert),
# Absenz-Checks, Arithmetik. Exit 1 bei FAILS.
import json, os, sys, re

BASE = '/Users/mac/agentic-business/barrierefrei-leads'
LEDGER = f'{BASE}/research/badumbau-kosten-171126-ledger.json'

def norm(s):
    s = s.replace('\u00ad', '')           # soft hyphens raus
    s = s.replace('\xa0', ' ')            # nbsp
    s = re.sub(r'\s+', ' ', s)            # whitespace kollabieren
    return s

ledger = json.load(open(LEDGER, encoding='utf-8'))
passes, fails = 0, []

# 1) Verbatim-Zitate
qcount = 0
for src in ledger['sources']:
    ev = os.path.join(BASE, src['evidence'])
    txt = norm(open(ev, encoding='utf-8').read())
    for q in src['quotes']:
        qcount += 1
        if norm(q) in txt:
            passes += 1
        else:
            fails.append(f'QUOTE fehlt [{src["key"]}]: {q[:80]}...')

# 2) Absenzen
for a in ledger['absences']:
    ev = os.path.join(BASE, f'research/evidence/badumbau-kosten-171126/{a["source"]}.txt')
    txt = norm(open(ev, encoding='utf-8').read())
    c = txt.count(a['pattern'])
    if c == a['expected']:
        passes += 1
    else:
        fails.append(f'ABSENZ verletzt [{a["source"]}] "{a["pattern"]}": {c} Treffer (erwartet {a["expected"]})')

# 3) Arithmetik
for a in ledger['arithmetic']:
    got = eval(a['expr'])
    if got == a['expected']:
        passes += 1
    else:
        fails.append(f'ARITHMETIK [{a["expr"]}]: {got} != {a["expected"]}')

print(f'Zitate gesamt: {qcount}')
print(f'PASSES: {passes}')
if fails:
    print(f'FAILS: {len(fails)}')
    for f in fails:
        print('  FAIL:', f)
    sys.exit(1)
print('ALL PASS')
