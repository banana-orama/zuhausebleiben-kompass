#!/usr/bin/env python3
"""Förder-Prüflauf 23.11.2026: Fetch aller Kernquellen nach research/evidence/.

Prüffläche (Stand heute):
 - gesetze-im-internet.de/sgb_11/__40.html            (ISO-8859-1, Entities)
 - kfw.de 455-B  (kanonikal: Bestandsimmobilie + Umlaut-ö + trailing slash)
 - kfw.de 159    (kanonikal: Bestehende-Immobilie + Umlaut + trailing slash)
 - bundesgesundheitsministerium.de zuschuesse-zur-wohnungsanpassung
 - nrwbank.de barrierefrei-umbauen            (Money-Page-Claim 220.000 €)
 - stmb.bayern.de barrierefreieswohnen        (Money-Page-Claim 10.000 € leistungsfrei)
 - gesetze-im-internet.de/estg/__35a.html     (badumbau-kosten: 20 % / 1.200 €)

Druckt je Quelle: HTTP-Status (final nach Redirects), canonical, Titel.
Bytes-sicher: gesetze-im-internet liefert ISO-8859-1 (kein text=True-Dekode).
"""
import re
import subprocess
import sys
import urllib.parse

EV = '/Users/mac/agentic-business/barrierefrei-leads/research/evidence'
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'

TARGETS = [
    ('foerder-231126-sgb11-40.html',
     'https://www.gesetze-im-internet.de/sgb_11/__40.html'),
    ('foerder-231126-kfw-455b.html',
     'https://www.kfw.de/inlandsfoerderung/Privatpersonen/Bestandsimmobilie/Förderprodukte/Altersgerecht-Umbauen-Investitionszuschuss-(455)/'),
    ('foerder-231126-kfw-159.html',
     'https://www.kfw.de/inlandsfoerderung/Privatpersonen/Bestehende-Immobilie/Förderprodukte/Altersgerecht-Umbauen-(159)/'),
    ('foerder-231126-bmg-wohnanp.html',
     'https://www.bundesgesundheitsministerium.de/pflege-zu-hause/zuschuesse-zur-wohnungsanpassung'),
    ('foerder-231126-nrwbank.html',
     'https://www.nrwbank.de/de/privatpersonen/wohneigentum-gestalten/barrierefrei-umbauen'),
    ('foerder-231126-stmb.html',
     'https://www.stmb.bayern.de/wohnen/wohnraum_nutzen/barrierefreieswohnen/'),
    ('foerder-231126-estg-35a.html',
     'https://www.gesetze-im-internet.de/estg/__35a.html'),
]

fails = []
for fname, url in TARGETS:
    enc = urllib.parse.urlsplit(url)
    enc_url = urllib.parse.urlunsplit((enc.scheme, enc.netloc,
                                       urllib.parse.quote(enc.path, safe='/@()%,;~$!&+=:'),
                                       enc.query, ''))
    r = subprocess.run(['curl', '-sS', '-L', '--compressed', '-A', UA,
                        '-w', '\n__STATUS__%{http_code} %{url_effective}',
                        '--max-time', '40', enc_url],
                       capture_output=True)
    out = r.stdout
    m = re.search(rb'\n__STATUS__(\d{3}) (https?://\S+)$', out)
    if m:
        code = m.group(1).decode()
        final_url = m.group(2).decode('utf-8', 'replace')
        raw = out[:m.start()]
    else:
        code, final_url, raw = 'ERR', r.stderr.decode('utf-8', 'replace')[:120], out
    if code != '200':
        fails.append((fname, code, url))
    size = len(raw)
    raw_init = True
    open(f'{EV}/{fname}', 'wb').write(raw)
    head = raw[:8000].decode('utf-8', 'replace')
    canon = re.search(r'<link[^>]+rel="canonical"[^>]+href="([^"]+)"', head)
    title = re.search(r'<title>([^<]{0,150})', head)
    print(f'{code}  {fname}  {size}B')
    print(f'     final: {final_url}')
    if canon:
        print(f'     canonical: {canon.group(1)}')
    if title:
        print(f'     title: {title.group(1).strip()[:110]}')

print()
if fails:
    print(f'FETCH-FAILS: {len(fails)}: {fails}')
    sys.exit(1)
print('Alle 7 Quellen HTTP 200 gezogen (Evidence in research/evidence/).')
