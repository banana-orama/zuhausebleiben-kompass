import html, re

raw = open('foerder-191026-bmg-wohnumfeld.html', 'rb').read().decode('utf-8', errors='replace')
txt = re.sub(r'<script.*?</script>', ' ', raw, flags=re.S)
txt = re.sub(r'<style.*?</style>', ' ', txt, flags=re.S)
txt = re.sub(r'<[^>]+>', ' ', txt)
txt = html.unescape(txt)
txt = re.sub(r'\s+', ' ', txt)
open('foerder-191026-bmg-wohnumfeld.txt', 'w').write(txt)

print("=== BMG Zuschuesse Wohnungsanpassung (Abruf 19.10.2026) ===")
for pat in ['Pflegegrad 1', 'Pflegegrade 1 bis 5', 'Treppenlift', '4.180', 'erneut', '16.720']:
    idx = txt.find(pat)
    if idx >= 0:
        print(f"[{pat}] ...{txt[max(0,idx-160):idx+260]}...")
    else:
        print(f"[{pat}] NICHT GEFUNDEN")
    print()
