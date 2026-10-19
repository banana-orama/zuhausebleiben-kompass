import html, re

def clean_utf(path):
    raw = open(path, 'rb').read().decode('utf-8', errors='replace')
    txt = re.sub(r'<script.*?</script>', ' ', raw, flags=re.S)
    txt = re.sub(r'<style.*?</style>', ' ', txt, flags=re.S)
    txt = re.sub(r'<[^>]+>', ' ', txt)
    txt = html.unescape(txt)
    txt = re.sub(r'\s+', ' ', txt)
    return txt

tpg = clean_utf('foerder-191026-bmg-pflegegrade.html')
print("=== BMG Pflegegrade: alternative Suchbegriffe ===")
for pat in ['Pflegegrad', 'Grad 1', 'NWB', 'Selbständigkeit']:
    idx = tpg.find(pat)
    print(f"[{pat}]", 'GEFUNDEN' if idx >= 0 else 'NICHT GEFUNDEN')
i = tpg.find('Pflegegrad')
if i >= 0:
    print('   ...', tpg[max(0, i-100):i+300])
