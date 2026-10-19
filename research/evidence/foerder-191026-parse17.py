import html, re

def clean_iso(path):
    raw = open(path, 'rb').read().decode('iso-8859-1', errors='replace')
    txt = re.sub(r'<script.*?</script>', ' ', raw, flags=re.S)
    txt = re.sub(r'<[^>]+>', ' ', txt)
    txt = html.unescape(txt)
    txt = re.sub(r'\s+', ' ', txt)
    return txt

print("=== §14 SGB XI: Pflegebeduerftigkeitsbegriff ===")
t14 = clean_iso('foerder-191026-sgb11-14.html')
for pat in ['Pflegebedürftigkeit', 'Selbständigkeit', 'Kompensation']:
    print(f"[{pat}]", 'GEFUNDEN' if pat in t14 else 'NICHT GEFUNDEN')
i = t14.find('(1)')
print('   ...', t14[i:i+340] if i >= 0 else '')

def clean_utf(path):
    raw = open(path, 'rb').read().decode('utf-8', errors='replace')
    txt = re.sub(r'<script.*?</script>', ' ', raw, flags=re.S)
    txt = re.sub(r'<style.*?</style>', ' ', txt, flags=re.S)
    txt = re.sub(r'<[^>]+>', ' ', txt)
    txt = html.unescape(txt)
    txt = re.sub(r'\s+', ' ', txt)
    return txt

print()
print("=== BMG Tagespflege/Nachtpflege (heute) ===")
tp = clean_utf('foerder-191026-bmg-tagespflege.html')
for pat in ['Tagespflege', 'Nachtpflege', 'Pflegegrad 2', 'halbtägig']:
    print(f"[{pat}]", 'GEFUNDEN' if pat in tp else 'NICHT GEFUNDEN')
