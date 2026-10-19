import html, re

raw = open('foerder-191026-kfw-159.html', 'rb').read().decode('utf-8', errors='replace')

print("=== KfW-159 FAQ (JSON-LD Questions, heute) ===")
for m in re.finditer(r'"@type":"Question","acceptedAnswer":\{"@type":"Answer","text":"(.*?)"\}', raw):
    q = m.group(1)
    q = html.unescape(re.sub(r'<[^>]+>', ' ', q))
    q = re.sub(r'\s+', ' ', q).strip()
    print('-', q[:420])
    print()

print("=== 'So funktioniert's' Schritte ===")
idx = raw.find('So funktioniert')
seg = raw[idx:idx+3000]
seg = html.unescape(re.sub(r'<[^>]+>', ' ', seg))
seg = re.sub(r'\s+', ' ', seg)
print(seg[:900])

# §20 WEG
raw20 = open('foerder-191026-weg-20.html', 'rb').read().decode('iso-8859-1')
t20 = html.unescape(re.sub(r'<[^>]+>', ' ', raw20))
t20 = re.sub(r'\s+', ' ', t20)
open('foerder-191026-weg-20.txt', 'w').write(t20)
print()
print("=== §20 WEG (heute) ===")
i = t20.find('(2)')
print(t20[i:i+420] if i >= 0 else 'Absatz 2 nicht gefunden')
