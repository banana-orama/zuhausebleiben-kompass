import re

t40 = open('foerder-191026-sgb11-40.txt').read()
print("=== §40 SGB XI heute: Abs.2/3-Betraege ===")
for pat in [r'42\s*Euro', r'25\s*Euro', r'vom Hundert', r'10\s*Prozent', r'zehn vom Hundert']:
    hits = re.findall(r'.{90}' + pat + r'.{110}', t40)
    print(f"[{pat}]", 'GEFUNDEN:' if hits else 'NICHT GEFUNDEN')
    for h in hits[:1]:
        print('   ...', h.strip()[:260])
print()

t159 = open('foerder-191026-kfw-159.txt').read()
print("=== KfW 159 heute: Kontexte ===")
for pat in ['Vorbehalt', 'Nachfinanzierung', 'Anspruch', 'zurückzahlen', 'Beginn']:
    idx = t159.find(pat)
    if idx >= 0:
        print(f"[{pat}] ...{t159[max(0,idx-200):idx+260]}...")
    else:
        print(f"[{pat}] nicht im gerenderten Text")
    print()

raw159 = open('foerder-191026-kfw-159.html', 'rb').read().decode('utf-8', errors='replace')
print("=== Roh-HTML: Fachunternehmen/Nachfinanzierung-Kontext ===")
for pat in ['Fachunternehmen', 'Nachfinanzierung']:
    for m in re.finditer(pat, raw159):
        seg = raw159[max(0, m.start()-250):m.start()+300]
        seg = re.sub(r'<[^>]+>', ' ', seg)
        seg = re.sub(r'\s+', ' ', seg).replace('&shy;', '').replace('&#160;', ' ')
        print(f"[{pat}] ...{seg[:280]}...")
        print()
        break
