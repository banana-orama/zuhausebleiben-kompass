#!/usr/bin/env python3
"""Dump plain text of Awin merchant profile + Triple-A start page for the badumbau scan."""
import re, html, pathlib

ev = pathlib.Path(__file__).resolve().parent / 'evidence' / 'partner-scan-badumbau-231026'

def txt(name):
    h = (ev / name).read_text(errors='ignore')
    h = re.sub(r'<script[\s\S]*?</script>|<style[\s\S]*?</style>', ' ', h)
    t = html.unescape(re.sub(r'<[^>]+>', ' ', h))
    return re.sub(r'\s+', ' ', t)

t = txt('awin-aroundhome-68536.html')
print('===== AWIN 68536 (%d chars) =====' % len(t))
print(t[:2600])
print()
kws = ['Vergütung', 'Provision', 'Lead', 'Cookie', 'commission', 'Bewerbung', 'nicht beworben', 'beworben', 'Autobestätigung']
for kw in kws:
    for m in list(re.finditer(kw, t, re.I))[:2]:
        s = max(0, m.start() - 120)
        print(f'[{kw}] …{t[s:m.end() + 180]}…')
print()
t2 = txt('aroundhome-triplea-start.html')
print('===== TRIPLE-A START (%d chars) =====' % len(t2))
for kw in ['Affiliate', 'registrieren', 'Programm', 'Vergüt', 'Provision', 'Bedingung']:
    for m in list(re.finditer(kw, t2, re.I))[:2]:
        s = max(0, m.start() - 130)
        print(f'[{kw}] …{t2[s:m.end() + 200]}…')
