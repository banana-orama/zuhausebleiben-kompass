import html, re

def clean_iso(path):
    raw = open(path, 'rb').read().decode('iso-8859-1', errors='replace')
    txt = re.sub(r'<script.*?</script>', ' ', raw, flags=re.S)
    txt = re.sub(r'<[^>]+>', ' ', txt)
    txt = html.unescape(txt)
    txt = re.sub(r'\s+', ' ', txt)
    return txt

print("=== Wo steht 'Haelfte' der Weiterzahlung? ===")
for name, path in [('§37', 'foerder-191026-sgb11-37.html'), ('§39', 'foerder-191026-sgb11-39.html')]:
    t = clean_iso(path)
    hits = [m.start() for m in re.finditer('Hälfte', t)]
    print(f"[{name}] 'Hälfte' {len(hits)}x")
    for h in hits[:2]:
        print('   ...', t[max(0, h-220):h+160])
