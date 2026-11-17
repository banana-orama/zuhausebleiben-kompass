# Text-Extraktion der Badumbau-Kosten-Evidenz (17.11.2026)
# Strip Tags, decode Entities, collapse whitespace -> .txt pro Quelle
from html import unescape
import re, os

D = os.path.dirname(os.path.abspath(__file__))
SOURCES = ['badumbau-ratgeber', 'pflegekompass', 'kostenwelt', 'pflege-panorama',
           'konstruktionsfuhrer', 'vz-handwerker', 'sgb11-40', 'estg-35a',
           'kfw-159', 'kfw-455b', 'bauguru', 'badklar']

def extract(name):
    raw = open(f'{D}/{name}.html', encoding='utf-8', errors='replace').read()
    # drop script/style/noscript/svg blocks
    raw = re.sub(r'(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>', ' ', raw)
    raw = re.sub(r'(?s)<!--.*?-->', ' ', raw)
    txt = re.sub(r'(?i)<br\s*/?>|</p>|</li>|</h[1-6]>|</tr>|</div>', '\n', raw)
    txt = re.sub(r'<[^>]+>', ' ', txt)
    txt = unescape(txt)
    txt = txt.replace('\xa0', ' ')
    lines = [re.sub(r'[ \t]+', ' ', ln).strip() for ln in txt.split('\n')]
    lines = [ln for ln in lines if ln]
    out = '\n'.join(lines)
    open(f'{D}/{name}.txt', 'w', encoding='utf-8').write(out)
    return len(out)

for s in SOURCES:
    n = extract(s)
    print(f'{s}.txt {n} chars')
