#!/usr/bin/env python3
"""Full text of the Awin 68536 profile + status/SEM greps on raw HTML."""
import re, html, pathlib

ev = pathlib.Path(__file__).resolve().parent / 'evidence' / 'partner-scan-badumbau-231026'
raw = (ev / 'awin-aroundhome-68536.html').read_text(errors='ignore')

h = re.sub(r'<script[\s\S]*?</script>|<style[\s\S]*?</style>', ' ', raw)
t = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', h)))
i = t.find('Doch Achtung')
print('===== LEAD-KRITERIEN ab "Doch Achtung" =====')
print(t[i:i + 1400] if i >= 0 else '(Marker nicht gefunden — voller Text folgt)')
print()
print('===== RAW-HTML Greps =====')
for kw in ['beworben', 'Promotion', 'Bedingung', 'SEM', 'locked', 'closed', 'geschlossen', 'offline']:
    hits = re.findall('.{70}' + kw + '.{90}', raw, re.I)
    for x in hits[:2]:
        print(f'[{kw}] …{x}…')
