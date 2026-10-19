import html, re

def clean(path):
    raw = open(path, 'rb').read()
    s = raw.decode('iso-8859-1', errors='replace')
    txt = re.sub(r'<script.*?</script>', ' ', s, flags=re.S)
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

t33 = clean('foerder-191026-sgb11-33.html')
print("=== §33 SGB XI: Vorversicherungszeit ===")
for pat in ['zwei Jahre', 'zehn Jahren', 'auf Antrag']:
    print(f"[{pat}]", 'GEFUNDEN' if pat in t33 else 'NICHT GEFUNDEN')
i = t33.find('zwei Jahre')
print('   ...', t33[max(0,i-150):i+220] if i>=0 else '')
print()

t30 = clean('foerder-191026-sgb11-30.html')
print("=== §30 SGB XI: Dynamisierung ===")
for pat in ['yearly', 'jährlich', 'zum 1. Januar', 'Verordnung']:
    print(f"[{pat}]", 'GEFUNDEN' if pat in t30 else 'NICHT GEFUNDEN')
i = t30.find('(1)')
print('   ...', t30[i:i+320] if i>=0 else '')
print()

t61 = clean('foerder-191026-sgb5-61.html')
print("=== §61 SGB V: Zuzahlung/Belastungsgrenze ===")
for pat in ['2 vom Hundert', 'Belastungsgrenze', 'jährlich']:
    print(f"[{pat}]", 'GEFUNDEN' if pat in t61 else 'NICHT GEFUNDEN')
print()

tbmg = clean_utf('foerder-191026-bmg-pflegehilfsmittel.html')
print("=== BMG Pflegehilfsmittel ===")
for pat in ['Notrufsystem', 'leihweise', '25 Euro', 'Verbrauch', 'Produktgruppen']:
    print(f"[{pat}]", 'GEFUNDEN' if pat in tbmg else 'NICHT GEFUNDEN')
i = tbmg.find('Notrufsystem')
print('   ...', tbmg[max(0,i-150):i+250] if i>=0 else '')
