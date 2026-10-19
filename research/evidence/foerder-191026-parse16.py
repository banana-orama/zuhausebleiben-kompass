import html, re

def clean_iso(path):
    raw = open(path, 'rb').read().decode('iso-8859-1', errors='replace')
    txt = re.sub(r'<script.*?</script>', ' ', raw, flags=re.S)
    txt = re.sub(r'<[^>]+>', ' ', txt)
    txt = html.unescape(txt)
    txt = re.sub(r'\s+', ' ', txt)
    return txt

print("=== §15 SGB XI: Pflegegrad-Schwellen ===")
t15 = clean_iso('foerder-191026-sgb11-15.html')
for pat in [r'12,5', r'\b27\b', r'90\b', r'100\b']:
    hits = re.findall(r'.{60}' + pat + r'.{100}', t15)
    print(f"[{pat}]", 'GEFUNDEN' if hits else 'NICHT GEFUNDEN')
    for h in hits[:1]:
        print('   ...', h.strip()[:220])
print()

print("=== §39 SGB XI: Verhinderungspflege / Ersatz-? ===")
t39 = clean_iso('foerder-191026-sgb11-39.html')
i = t39.find('(1)')
print(t39[i:i+380] if i >= 0 else t39[:350])
print()

print("=== §41 SGB XI: Leistungen je Pflegegrad ===")
t41 = clean_iso('foerder-191026-sgb11-41.html')
for pat in ['721', '1 031', '1 494', '1 797', '2 085']:
    print(f"[{pat}]", 'GEFUNDEN' if pat in t41 else 'NICHT GEFUNDEN')
print()

print("=== §42a SGB XI: Entlastungsbetrag ===")
t42a = clean_iso('foerder-191026-sgb11-42a.html')
for pat in ['131', '3 539']:
    print(f"[{pat}]", 'GEFUNDEN' if pat in t42a else 'NICHT GEFUNDEN')
i = t42a.find('3 539')
if i >= 0:
    print('   ...', t42a[max(0,i-160):i+200])
