import json, glob, sys

bad = []
files = sorted(glob.glob('content-ready/*.json'))
for f in files:
    try:
        json.load(open(f))
    except Exception as e:
        bad.append((f, str(e)))
if bad:
    for f, e in bad:
        print('JSON-FEHLER:', f, e)
    sys.exit(1)
print(f'ALLE {len(files)} JSON VALIDE')
