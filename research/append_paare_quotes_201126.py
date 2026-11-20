#!/usr/bin/env python3
"""Append verbatim evidence quotes to the paare ledger (pre-checked against evidence files)."""
import json, re
from pathlib import Path

LED = Path('research/paare-191126-ledger.json')
EV = Path('research/evidence/paare-191126')
led = json.loads(LED.read_text())

def flat(p):
    t = Path(p).read_text(errors='replace')
    t = re.sub(r'<[^>]+>', ' ', t)
    return re.sub(r'\s+', ' ', t)

ADD = [
    # (url-key, evidence file, exact quote)
    ('verbraucherzentrale.de', 'vz-10566.txt',
     'Wenn die pflegebedürftige Person mit jemandem zusammenlebt, muss diese oft und länger abwesend sein, zum Beispiel, weil sie bei der Arbeit ist.'),
    ('gkv-90prozent.de', 'raw-gkv-90prozent.html',
     'Kraft getreten und haben eine Mindestlaufzeit von zwei Jahren.'),
    ('johanniter.de', 'johanniter.txt',
     'Zusätzlich zur klassischen Hausnotruf-Basisstation mit stoß- und wasserfestem Handsender, wird der Johanniter-Hausnotruf für zuhause und unterwegs mit einem Mobilgerät geliefert, das im Notfall über das Mobilfunknetz eine Verbindung zu den Johannitern herstellt'),
]
hay_cache = {}
for key, fn, quote in ADD:
    hay = hay_cache.setdefault(fn, flat(EV / fn))
    flat_q = re.sub(r'\s+', ' ', quote)
    assert flat_q in hay, f'QUOTE NOT VERBATIM in {fn}: {quote[:60]}'
    for src in led['sources']:
        if key in src['url']:
            texts = {q['text'] for q in src.get('quotes', [])}
            if flat_q not in texts:
                src.setdefault('quotes', []).append({'text': flat_q, 'added': '2026-11-20'})
                print(f'appended to [{src["id"]}] {key}: {flat_q[:60]}…')
            else:
                print(f'already present [{src["id"]}]')
            break
    else:
        print('NO LEDGER ENTRY FOR', key)

LED.write_text(json.dumps(led, ensure_ascii=False, indent=2) + '\n')
print('ledger saved,', sum(len(s.get("quotes", [])) for s in led["sources"]), 'quotes total')
