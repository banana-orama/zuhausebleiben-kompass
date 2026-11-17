# Exakte Wortlaut-Zeilen: §35a EStG, §40 SGB XI, VZ, KfW-159
import os
D = '/Users/mac/agentic-business/barrierefrei-leads/research/evidence/badumbau-kosten-171126'

def show(name, pats, ctx=0):
    txt = open(f'{D}/{name}.txt', encoding='utf-8').read()
    lines = txt.split('\n')
    print(f'\n===== {name} =====')
    printed = set()
    for pat in pats:
        for i, ln in enumerate(lines):
            if pat.lower() in ln.lower():
                lo, hi = max(0, i-ctx), min(len(lines), i+ctx+1)
                for j in range(lo, hi):
                    if j not in printed:
                        printed.add(j)
                        print(f'  {j:4d}| {lines[j][:340]}')
                print('  ---')

# §35a Abs. 3: Handwerkerleistungen + Förder-Ausnahme (kompletter Absatz)
show('estg-35a', ['Handwerkerleistungen', 'öffentliche Mittel', 'Renovierungs'], ctx=4)
# §40: Abs. 4 (subsidiär + 4.180/16.720) + Abs. 7 (Fristen)
show('sgb11-40', ['subsidiär', '4 180', 'wohnumfeldverbessernden', 'drei Wochen'], ctx=2)
# VZ: 20-%-Schwelle + Festpreis + Angebot vs. Kostenvoranschlag
show('vz-handwerker', ['20 Prozent', '20 %', 'Festpreis', 'verbindlich'], ctx=1)
# KfW 159: Produktkern
show('kfw-159', ['zinswerte', 'Darlehen', 'Altersgerecht', 'Maßnahmen', '100.000'], ctx=1)
