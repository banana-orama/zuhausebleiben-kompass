import json, html, re
from pathlib import Path
ledger = json.loads(Path('/Users/mac/agentic-business/barrierefrei-leads/research/badumbau-angebote-ledger.json').read_text())
plain = Path('/Users/mac/.hermes/profiles/milo/cache/scratch/badumbau-batch')
pdf = (plain / 'einhornmerkblatt.txt').read_text()

def norm(s):
    s = html.unescape(s).replace('\xa0', ' ').replace('ä', 'ä').replace('ö', 'ö').replace('ü', 'ü').replace('ß', 'ß')
    s = re.sub(r'\s+', ' ', s)
    return s.strip().lower()

files = {}
for f in plain.glob('plain/*.txt'):
    files[f.stem] = norm(f.read_text())
files['einhornmerkblatt'] = norm(pdf)

url_file = {
    'verbraucherzentrale': 'vzs-handwerker',
    'gesetze-im-internet.de/bgb/__632a': 'bgb632a',
    'gesetze-im-internet.de/bgb/__650b': 'bgb650b',
    'gesetze-im-internet.de/bgb/__650k': 'bgb650k',
    'gesetze-im-internet.de/bgb/__634a': 'bgb634a',
    'din.de': 'din18534-din',
    'schluter.com': 'schluter18534',
    'einhornwerke.de': 'einhornmerkblatt',
    'sgb_11/__40': 'sgb40',
}

total, ok = 0, 0
for src in ledger['sources']:
    key = next(v for k, v in url_file.items() if k in src['url'])
    body = files[key]
    for q in src['quotes']:
        total += 1
        hit = norm(q['text']) in body
        ok += hit
        if not hit:
            print('FAIL', src['id'], '|', q['text'][:90])
print(f'{ok}/{total} quotes verified verbatim')
if ok != total:
    raise SystemExit(1)
print('LEDGER OK')
