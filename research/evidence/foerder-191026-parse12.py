import html, re
raw = open('foerder-191026-sgb5-61.html', 'rb').read().decode('iso-8859-1', errors='replace')
txt = re.sub(r'<script.*?</script>', ' ', raw, flags=re.S)
txt = re.sub(r'<[^>]+>', ' ', txt)
txt = html.unescape(txt)
txt = re.sub(r'\s+', ' ', txt)
print("=== §61 SGB V: Volltext (Kern) ===")
i = txt.find('Versicherte, die das 18.')
print(txt[i:i+900] if i >= 0 else txt[:900])
