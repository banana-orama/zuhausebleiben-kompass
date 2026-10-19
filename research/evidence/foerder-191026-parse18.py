import html, re

def clean_iso(path):
    raw = open(path, 'rb').read().decode('iso-8859-1', errors='replace')
    txt = re.sub(r'<script.*?</script>', ' ', raw, flags=re.S)
    txt = re.sub(r'<[^>]+>', ' ', txt)
    txt = html.unescape(txt)
    txt = re.sub(r'\s+', ' ', txt)
    return txt

def clean_utf(path):
    raw = open(path, 'rb').read().decode('utf-8', errors='replace')
    txt = re.sub(r'<script.*?</script>', ' ', raw, flags=re.S)
    txt = re.sub(r'<style.*?</style>', ' ', txt, flags=re.S)
    txt = re.sub(r'<[^>]+>', ' ', txt)
    txt = html.unescape(txt)
    txt = re.sub(r'\s+', ' ', txt)
    return txt

print("=== §41 SGB XI: alle Betraege (geschuetzte Leerzeichen normalisieren) ===")
t41 = clean_iso('foerder-191026-sgb11-41.html')
t41n = re.sub(r'(\d) (\d\d\d)', r'\1\2', t41)  # 1 031 -> 1031
for pat in ['721', '1031', '1494', '1797', '2085']:
    print(f"[{pat}]", 'GEFUNDEN' if pat in t41n else 'NICHT GEFUNDEN')
print()

print("=== §18 SGB XI: Begutachtung Fristen ===")
t18 = clean_iso('foerder-191026-sgb11-18.html')
for pat in ['fünf Arbeitstagen', 'drei Wochen', 'Terminsicherung']:
    print(f"[{pat}]", 'GEFUNDEN' if pat in t18 else 'NICHT GEFUNDEN')
i = t18.find('fünf Arbeitstagen')
if i >= 0:
    print('   ...', t18[max(0,i-160):i+200])
print()

print("=== §87 SGG: Klagefrist ===")
t87 = clean_iso('foerder-191026-sgg-87.html')
i = t87.find('Monat')
print('   ...', t87[max(0,i-200):i+200] if i >= 0 else t87[:350])
print()

print("=== GKV p_himi (42-Euro-Seite) ===")
tgkv = clean_utf('foerder-191026-gkv-phimi.html')
for pat in ['42 Euro', 'Verbrauch', 'Kostenerstattung', '1. Januar 2025']:
    print(f"[{pat}]", 'GEFUNDEN' if pat in tgkv else 'NICHT GEFUNDEN')
i = tgkv.find('42 Euro')
if i >= 0:
    print('   ...', tgkv[max(0,i-180):i+220])
