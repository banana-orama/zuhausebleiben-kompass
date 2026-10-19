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

print("=== §84 SGG: Widerspruchsfrist ===")
t84 = clean_iso('foerder-191026-sgg-84.html')
i = t84.find('(1)')
print(t84[i:i+420] if i >= 0 else t84[:400])
print()

print("=== VZ Pflegehilfsmittel (heute) ===")
tvz = clean_utf('foerder-191026-vz-pflegehilfsmittel.html')
for pat in ['42 Euro', '40 Euro', '25 Euro', '10 Prozent', 'Belastung', '4.180', 'fest mit']:
    print(f"[{pat}]", 'GEFUNDEN' if pat in tvz else 'NICHT GEFUNDEN')
i = tvz.find('42 Euro')
if i >= 0:
    print('   ...', tvz[max(0,i-180):i+240])
print()

print("=== GKV-Spitzenverband Hilfsmittelverzeichnis ===")
tgkv = clean_utf('foerder-191026-gkv-hilfsmittelverzeichnis.html')
for pat in ['Produktgruppe', 'Hilfsmittelverzeichnis']:
    print(f"[{pat}]", 'GEFUNDEN' if pat in tgkv else 'NICHT GEFUNDEN')
print()

print("=== BMG Pflegegrade (heute) ===")
tpg = clean_utf('foerder-191026-bmg-pflegegrade.html')
for pat in ['12,5', '27 Punkte', 'Punkte', 'sechs Pflegegrade']:
    print(f"[{pat}]", 'GEFUNDEN' if pat in tpg else 'NICHT GEFUNDEN')
