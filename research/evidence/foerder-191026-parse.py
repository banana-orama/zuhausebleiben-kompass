import html, re

def clean(path):
    raw = open(path, 'rb').read().decode('iso-8859-1')
    txt = re.sub(r'<[^>]+>', ' ', raw)
    txt = html.unescape(txt)
    txt = re.sub(r'\s+', ' ', txt)
    return txt

t40 = clean('foerder-191026-sgb11-40.html')
t554 = clean('foerder-191026-bgb-554.html')
open('foerder-191026-sgb11-40.txt', 'w').write(t40)
open('foerder-191026-bgb-554.txt', 'w').write(t554)

print("=== §40 SGB XI (Abruf 19.10.2026) ===")
for pat in [r'4\s*180', r'16\s*720', r'Zuschuss', r'Investitionskosten']:
    m = re.findall(r'.{100}' + pat + r'.{180}', t40)
    for x in m[:2]:
        print(f"[{pat}] ...{x}...")
    if not m:
        print(f"[{pat}] NICHT GEFUNDEN")
    print()

print("=== Absaetze mit 4180/16720 (Absatzkontext) ===")
raw = open('foerder-191026-sgb11-40.html', 'rb').read().decode('iso-8859-1')
plain = html.unescape(re.sub(r'<[^>]+>', '', raw))
paras = re.split(r'(?=\(\d+\)\s)', plain)
paras = [re.sub(r'\s+', ' ', p).strip() for p in paras if p.strip()]
for p in paras:
    if re.search(r'4\s*180', p) or re.search(r'16\s*720', p):
        print(p[:600])
        print('---')

print("=== §554 BGB Kernpassagen ===")
for pat in [r'Erlaubnis', r'behinderte', r'unzumutbar']:
    m = re.findall(r'.{80}' + pat + r'.{140}', t554, re.I)
    for x in m[:1]:
        print(f"[{pat}] ...{x}...")
    if not m:
        print(f"[{pat}] NICHT GEFUNDEN")
    print()
