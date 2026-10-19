import html, re

def clean_iso(path):
    raw = open(path, 'rb').read().decode('iso-8859-1', errors='replace')
    txt = re.sub(r'<script.*?</script>', ' ', raw, flags=re.S)
    txt = re.sub(r'<[^>]+>', ' ', txt)
    txt = html.unescape(txt)
    txt = re.sub(r'\s+', ' ', txt)
    return txt

print("=== §41 SGB XI: Betragsabsatz roh ===")
t41 = clean_iso('foerder-191026-sgb11-41.html')
i = t41.find('(1)')
print(t41[i:i+1100])
print()

print("=== §18 SGB XI: Kernzitate ===")
t18 = clean_iso('foerder-191026-sgb11-18.html')
for pat in ['Arbeitstagen', 'Wochen', 'Begutachtung']:
    idx = t18.find(pat)
    print(f"[{pat}]", 'GEFUNDEN' if idx >= 0 else 'NICHT GEFUNDEN')
i = t18.find('(1)')
print(t18[i:i+600])
