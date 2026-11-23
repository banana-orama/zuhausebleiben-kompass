#!/usr/bin/env python3
"""Primary verification for secondary-cited rulings: V ZR 140/22, VIII ZR 234/23, § 46 WEG.
Fetch via BGH Entscheidungssuche / bundesgerichtshof.de + gesetze-im-internet, extract needles."""
import html, json, re, subprocess, sys, urllib.parse

OUT = 'research/evidence/weg-231126/raw'
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'

def curl(url, out=None):
    cmd = ['curl', '-sL', '--max-time', '60', '-A', UA, '-w', '\n%{http_code} %{content_type}']
    if out:
        cmd += ['-o', out]
    cmd.append(url)
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.stdout

# 1) § 46 WEG (Anfechtungsfrist)
print('=== § 46 WEG ===')
raw = curl('https://www.gesetze-im-internet.de/woeigg/__46.html', f'{OUT}/woeigg__46.html')
code = raw.strip().split('\n')[-1]
print('status:', code)
b = open(f'{OUT}/woeigg__46.html', 'rb').read().decode('iso-8859-1', errors='replace')
t = ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', b.replace('\u00a0', ' '))).split())
m = re.search(r'\(1\)\s*Ein Beschluss kann[^.]*\.', t)
print('§46 Abs1:', (m.group(0) if m else 'NOT FOUND')[:300])
m2 = re.search(r'Frist (?:beträgt|ist)[^.]*\.', t)
if m2:
    print('Frist-Satz:', m2.group(0)[:300])

# 2) BGH Entscheidungssuche: V ZR 140/22 und VIII ZR 234/23
for az, fname in [('V ZR 140/22', 'vzr-140-22'), ('VIII ZR 234/23', 'viiizr-234-23')]:
    print(f'=== {az} ===')
    q = urllib.parse.quote(az)
    search_html = curl(f'https://www.bundesgerichtshof.de/SiteGlobals/Forms/Suche/EntscheidungssucheBGH_Formular.html?templateQueryString={q}', f'/tmp/bgh_search_{fname}.html')
    links = re.findall(r'href="(https://www\.bundesgerichtshof\.de/SharedDocs/Entscheidungen/DE/[^"]+?%s[^"]*)"' % re.escape(az.replace(' ', '_')), search_html)
    if not links:
        links = re.findall(r'href="(https://www\.bundesgerichtshof\.de/SharedDocs/Entscheidungen/DE/[^"]+)"', search_html)
    links = [l for l in links if 'publicationFile' in l or l.endswith('.pdf')]
    print('pdf links:', links[:3])
    if links:
        pdf_url = html.unescape(links[0])
        r = subprocess.run(['curl', '-sL', '--max-time', '90', '-A', UA, '-o', f'{OUT}/{fname}.pdf', '-w', '%{http_code} %{content_type}', pdf_url], capture_output=True, text=True)
        print('pdf fetch:', r.stdout)
        if r.stdout.startswith('200'):
            subprocess.run(['pdftotext', '-layout', f'{OUT}/{fname}.pdf', f'{OUT}/{fname}.txt'], check=True)
            txt = ' '.join(open(f'{OUT}/{fname}.txt', encoding='utf-8', errors='replace').read().split())
            open(f'{OUT}/{fname}.flat.txt', 'w').write(txt)
            print('--- first 700 chars ---')
            print(txt[:700])
