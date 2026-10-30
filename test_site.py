from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import xml.etree.ElementTree as ET
import json
root=Path(__file__).parent/'dist'
site=urlsplit(json.loads((root.parent/'data/content.json').read_text())['brand']['base_url'])
base=site.path.rstrip('/')
class Page(HTMLParser):
    def __init__(self):
        super().__init__();self.links=[];self.forms=0;self.h1=0;self.noindex=False
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag=='a':self.links.append(d.get('href',''))
        if tag=='form':self.forms+=1
        if tag=='h1':self.h1+=1
        if tag=='meta' and d.get('name')=='robots':self.noindex='noindex' in d.get('content','')
files=list(root.rglob('*.html'))
for f in files:
    p=Page();p.feed(f.read_text())
    assert p.h1==1,(f,'heading count')
    assert p.forms==0,(f,'unsafe form')
    if f.name == 'datenschutz.html':
        assert not p.noindex,(f,'privacy policy is indexable at launch')
    elif f.parent.name == 'region' or f.name == 'regional.html':
        # Fix #5 (2026-10-30): Region-Platzhalter bleiben noindex, bis sie mit
        # verifiziertem Landesprogramm-Inhalt erweitert sind (expand-or-noindex-Gate).
        assert p.noindex,(f,'region placeholder must stay noindex until expanded')
    else:
        assert not p.noindex,(f,'launch build: indexable page without noindex')
    for href in p.links:
        u=urlsplit(href)
        if u.netloc==site.netloc and u.path.startswith(base):
            rel=unquote(u.path[len(base):]).lstrip('/') or 'index.html'
            target=root/rel
            if target.is_dir():target=target/'index.html'
            assert target.exists(),(f,href)
for name in ('sitemap.xml','rss.xml'):ET.parse(root/name)
sm=(root/'sitemap.xml').read_text()
locs=[u.split('<loc>')[1].split('</loc>')[0] for u in sm.split('<url>')[1:]]
assert any(u.endswith('/datenschutz.html') for u in locs),('datenschutz.html missing from sitemap',len(locs))
assert not any('/region/' in u or u.endswith('/regional.html') for u in locs),('region placeholders must stay out of the sitemap (fix #5)',)
assert len(locs)==len(set(locs)),('duplicate sitemap URLs',)
mode='PREVIEW (noindex)' if not __import__('os').environ.get('INDEX') else 'LAUNCH (index)'
print(f'PASS: {len(files)} HTML pages, internal links, single H1, no forms, datenschutz in sitemap ({len(locs)} locs), {mode}, XML valid.')
