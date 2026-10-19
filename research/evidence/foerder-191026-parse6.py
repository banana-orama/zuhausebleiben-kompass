import re
t40 = open('foerder-191026-sgb11-40.txt').read()
print("=== §40 SGB XI: 3-/5-Wochen-Kontext (heute) ===")
for pat in ['drei Wochen', 'fünf Wochen', 'als genehmigt']:
    for m in re.finditer(re.escape(pat), t40):
        seg = t40[max(0, m.start()-260):m.start()+300]
        print(f"[{pat}] ...{seg}...")
        print()
        break
