#!/usr/bin/env python3
"""Extract exact evidence sentences for the three flagged claims."""
import re
from pathlib import Path
EV = Path('research/evidence/paare-191126')

def flat(p):
    t = Path(p).read_text(errors='replace')
    t = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', t, flags=re.S)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = t.replace('&nbsp;', ' ').replace('&auml;', 'ä').replace('&ouml;', 'ö').replace('&uuml;', 'ü').replace('&szlig;', 'ß')
    t = t.replace('\u00ad', '')
    return re.sub(r'\s+', ' ', t)

def show(label, hay, needle, width=220, n=3):
    print(f'--- {label} (needle={needle!r}) ---')
    i = 0; hits = 0
    low = hay.lower(); nl = needle.lower()
    while hits < n:
        i = low.find(nl, i)
        if i < 0: break
        print('  …' + hay[max(0, i - 60):i + width] + '…')
        i += len(nl); hits += 1
    if hits == 0: print('  NO MATCH')

vz = flat(EV / 'vz-10566.txt')
show('VZ abwesend', vz, 'abwesend')
show('VZ allein', vz, 'allein ist', 200, 2)
show('VZ 27 und 40', vz, '27 und 40', 160, 2)

gkv = flat(EV / 'gkv-hn-vertrag.txt')
show('GKV-Vertrag Laufzeit', gkv, 'laufzeit', 260, 6)
show('GKV-Vertrag zwei', gkv, 'zwei jahre', 200, 4)

p90 = flat(EV / 'raw-gkv-90prozent.html')
show('90prozent laufzeit', p90, 'laufzeit', 260, 3)
show('90prozent jahre', p90, 'jahr', 160, 4)
show('90prozent vertrag', p90, 'vertrag', 160, 3)

joh = flat(EV / 'johanniter.txt')
show('Johanniter Mobilgerät', joh, 'mobilgerät geliefert', 300, 2)
show('Johanniter Basisstation', joh, 'Basisstation mit stoß', 300, 2)
