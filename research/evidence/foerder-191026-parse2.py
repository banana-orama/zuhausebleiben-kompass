import html, re

def clean(path):
    raw = open(path, 'rb').read()
    s = None
    for enc in ('utf-8', 'iso-8859-1', 'cp1252'):
        try:
            s = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    if s is None:
        s = raw.decode('utf-8', errors='replace')
    txt = re.sub(r'<script.*?</script>', ' ', s, flags=re.S)
    txt = re.sub(r'<style.*?</style>', ' ', txt, flags=re.S)
    txt = re.sub(r'<[^>]+>', ' ', txt)
    txt = html.unescape(txt)
    txt = re.sub(r'\s+', ' ', txt)
    return txt, s

t554, raw554 = clean('foerder-191026-bgb-554.html')
open('foerder-191026-bgb-554.txt', 'w').write(t554)
print("=== §554 BGB Text (erste 1200 Zeichen des Bodys) ===")
i = t554.find('554')
print(t554[i:i+1200])
print()
print("Suche 'Erlaubnis':", 'Erlaubnis' in t554, "| 'behinder':", 'behinder' in t554.lower())

t455, raw455 = clean('foerder-191026-kfw-455b.html')
open('foerder-191026-kfw-455b.txt', 'w').write(t455)
print()
print("=== KfW 455-B (Abruf 19.10.2026) ===")
for pat in ['ausgeschöpft', 'keine neuen Anträge', '2027', 'laufende Anträge', 'Zusage', '4.180', '455']:
    idx = t455.lower().find(pat.lower())
    if idx >= 0:
        print(f"[{pat}] ...{t455[max(0,idx-150):idx+250]}...")
    else:
        print(f"[{pat}] NICHT GEFUNDEN")
    print()

t159, raw159 = clean('foerder-191026-kfw-159.html')
open('foerder-191026-kfw-159.txt', 'w').write(t159)
print("=== KfW 159 (Abruf 19.10.2026) ===")
for pat in ['50.000', 'Finanzierungspartner', 'Rechtsanspruch', 'Haushaltsmittel', 'Fachunternehmen', 'Treppenlift', 'Badumbau', 'Nicht förderfähig', 'Eigenleistung']:
    idx = t159.lower().find(pat.lower())
    if idx >= 0:
        print(f"[{pat}] ...{t159[max(0,idx-120):idx+220]}...")
    else:
        print(f"[{pat}] NICHT GEFUNDEN")
    print()
