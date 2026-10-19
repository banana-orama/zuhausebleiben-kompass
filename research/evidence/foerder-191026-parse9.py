import re
raw = open('foerder-191026-kfw-159.html', 'rb').read().decode('utf-8', errors='replace')
print("=== KfW-159: Antragsreihenfolge-Phrasen ===")
for pat in ['Lieferungs', 'Verträge schließen', 'vor Beginn', 'Beginn der Maß', 'vorhandene Verträge', 'vorzeitige Antragstellung', 'Antrag stellen']:
    n = raw.count(pat)
    print(f"[{pat}] {n}x")
    if n:
        i = raw.find(pat)
        seg = re.sub(r'<[^>]+>', ' ', raw[max(0, i-220):i+260])
        seg = re.sub(r'\s+', ' ', seg).replace('&shy;', '').replace('&#160;', ' ')
        print('   ...', seg[:300])
