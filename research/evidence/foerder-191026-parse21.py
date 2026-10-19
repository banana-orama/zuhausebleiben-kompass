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

print("=== §37 SGB XI: Pflegegeld-Betraege ===")
t37 = clean_iso('foerder-191026-sgb11-37.html')
t37n = re.sub(r'(\d) (\d\d)', r'\1\2', t37)
for pat in ['131', '161', '565', '685', '990']:
    print(f"[{pat}]", 'GEFUNDEN' if pat in t37n else 'NICHT GEFUNDEN')

print()
print("=== BMG Entlastungsbetrag: 131 Euro ===")
te = clean_utf('foerder-191026-bmg-entlastung.html')
for pat in ['131 Euro', 'Entlastungsbetrag']:
    i = te.find(pat)
    print(f"[{pat}]", 'GEFUNDEN' if i >= 0 else 'NICHT GEFUNDEN')
    if i >= 0 and pat == '131 Euro':
        print('   ...', te[max(0,i-150):i+220])
