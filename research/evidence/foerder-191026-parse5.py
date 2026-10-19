import re
t40 = open('foerder-191026-sgb11-40.txt').read()
print("=== §40 SGB XI: Wochen-Fristen? ===")
for pat in ['drei Wochen', 'fünf Wochen', 'genehmigt', 'Medizinischer Dienst']:
    print(pat, '->', 'GEFUNDEN' if pat in t40 else 'NICHT IN §40')
print()
print("=== §40 Absaetze 5-7 (Ende des Paragrafen) ===")
idx = t40.find('(5)')
print(t40[idx:idx+900] if idx >= 0 else 'Absatz 5 nicht gefunden')
