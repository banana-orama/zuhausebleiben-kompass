from pathlib import Path
import json, re
root = Path('/Users/mac/agentic-business/barrierefrei-leads')
a = json.loads((root / 'content-ready/badumbau-angebote-vergleichen.json').read_text())
h = (root / 'dist/badumbau-angebote-vergleichen.html').read_text()

def cit(s):
    s = re.sub(r'<sup class="cite">.*?</sup>', '', s, flags=re.S)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = re.sub(r'\[\d+\]', '', s)
    return re.sub(r'\s+', ' ', s)

plain = cit(h)
fails = []
def check(label, needle):
    np = re.sub(r'\[\d+\]', '', needle)
    np = re.sub(r'\s+', ' ', np).strip()
    if not np:
        return
    ok = np in plain
    if not ok:
        fails.append((label, np[:90]))
        print('FAIL', label, '|', np[:90])

check('intro', a['intro'])
for i, s in enumerate(a['sections']):
    check(f'section-{i+1}-heading', s['heading'])
    for p in (s.get('paragraphs') or []):
        check('p', p)
    for b in (s.get('bullets') or []):
        check('bullet', b)
    if 'table' in s:
        for hdr in s['table']['headers']:
            check('th', hdr)
        for row in s['table']['rows']:
            for c in row:
                check('td', c)
    for p in (s.get('paragraphs_after') or []):
        check('p_after', p)
for f in a['faqs']:
    check('faq-q', f['question'])
    check('faq-a', f['answer'])
for needle in ['4 180', '15 bis 20 Prozent', 'W1-I', 'W2-I', 'Oktober 2025', 'zwei bis drei Angebote', 'Aufstellung', 'unter Vorbehalt']:
    present = needle in plain
    if not present:
        fails.append(('figure', needle))
    print(('OK  ' if present else 'FAIL'), 'figure', needle)
n_cites = len(re.findall(r'\[\d+\]', h))
print('cite links in html:', n_cites)
print('FAILS:', len(fails))
if fails:
    raise SystemExit(1)
print('KEY-CONTENT OK — alle Absätze, Bullets, Tabellenzellen, FAQs, Anker-Nachbarschaft und Kennzahlen im HTML')
