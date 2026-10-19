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

print("=== §18 SGB XI Abs. 3: 20 Arbeitstage/Gutachterliste ===")
t18 = clean_iso('foerder-191026-sgb11-18.html')
i = t18.find('20 Arbeitstagen')
print('GEFUNDEN' if i >= 0 else 'NICHT GEFUNDEN')
if i >= 0:
    print('...', t18[max(0,i-200):i+330])
print()

print("=== BMG Pflegegrade: 25 Arbeitstage ===")
tpg = clean_utf('foerder-191026-bmg-pflegegrade.html')
for pat in ['25 Arbeitstage', 'Arbeitstage']:
    i = tpg.find(pat)
    print(f"[{pat}]", 'GEFUNDEN' if i >= 0 else 'NICHT GEFUNDEN')
    if i >= 0:
        print('   ...', tpg[max(0,i-160):i+220])
        break
print()

print("=== BMG Tagespflege: Unterkunft/Verpflegung/Investition ===")
tp = clean_utf('foerder-191026-bmg-tagespflege.html')
for pat in ['Unterkunft', 'Investitionskosten', 'Verpflegung']:
    i = tp.find(pat)
    print(f"[{pat}]", 'GEFUNDEN' if i >= 0 else 'NICHT GEFUNDEN')
    if i >= 0:
        print('   ...', tp[max(0,i-140):i+200])
