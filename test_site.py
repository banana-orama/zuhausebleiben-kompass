from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import xml.etree.ElementTree as ET
root=Path(__file__).parent/'dist'
base='/zuhausebleiben-kompass'
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
    assert p.noindex,(f,'preview indexing')
    for href in p.links:
        u=urlsplit(href)
        if u.netloc=='banana-orama.github.io' and u.path.startswith(base):
            rel=unquote(u.path[len(base):]).lstrip('/') or 'index.html'
            target=root/rel
            if target.is_dir():target=target/'index.html'
            assert target.exists(),(f,href)
for name in ('sitemap.xml','rss.xml'):ET.parse(root/name)
print(f'PASS: {len(files)} HTML pages, internal links, single H1, no forms, preview noindex and XML.')
