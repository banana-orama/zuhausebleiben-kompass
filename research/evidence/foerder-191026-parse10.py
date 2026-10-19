import html, re
raw = open('foerder-191026-vz-hausnotruf.html', 'rb').read().decode('utf-8', errors='replace')
txt = re.sub(r'<script.*?</script>', ' ', raw, flags=re.S)
txt = re.sub(r'<style.*?</style>', ' ', txt, flags=re.S)
txt = re.sub(r'<[^>]+>', ' ', txt)
txt = html.unescape(txt)
txt = re.sub(r'\s+', ' ', txt)
open('foerder-191026-vz-hausnotruf.txt', 'w').write(txt)
print("=== VZ Hausnotruf (Abruf 19.10.2026) ===")
for pat in ['27 Euro', '1. April 2026', 'Medizinische', 'Basistarif']:
    idx = txt.find(pat)
    if idx >= 0:
        print(f"[{pat}] ...{txt[max(0,idx-200):idx+300]}...")
    else:
        print(f"[{pat}] NICHT GEFUNDEN")
    print()
