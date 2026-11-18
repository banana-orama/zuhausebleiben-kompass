# Audit: all anchor texts linking to treppenlift-zuschuss.html across built pages + specialMap
import re, io, sys, json, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

dist = 'dist'
target = 'treppenlift-zuschuss.html'
anchor_stats = {}
for fn in sorted(os.listdir(dist)):
    if not fn.endswith('.html'):
        continue
    p = os.path.join(dist, fn)
    html = open(p, encoding='utf-8').read()
    # find <a ... href="...treppenlift-zuschuss.html"...>TEXT</a> (href may contain fragment)
    for m in re.finditer(r'<a\b([^>]*)href="([^"]*' + re.escape(target) + r'[^"]*)"([^>]*)>(.*?)</a>', html, re.S):
        text = re.sub(r'<[^>]+>', '', m.group(4)).strip()
        key = text[:80]
        anchor_stats.setdefault(key, []).append(fn)

print('=== Anchor texts -> pages (dist LAUNCH) ===')
for text, pages in sorted(anchor_stats.items()):
    print(f'[{len(pages)}x] "{text}"  e.g. {pages[0]}')

print()
print('=== specialMap in article-renderer.mjs (kosten/mieten/finanzierung/zuschuss rows) ===')
src = open('article-renderer.mjs', encoding='utf-8').read()
for m in re.finditer(r"'(treppenlift-(?:kosten|mieten|finanzierung|zuschuss|firmen-vergleich|angebote-vergleichen))'[^}]{0,300}", src):
    print(m.group(0)[:260].replace('\n', ' '))
    print('---')
