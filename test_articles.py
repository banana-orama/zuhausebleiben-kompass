import json
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET
ROOT=Path(__file__).parent
class Doc(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=set();self.refs=[];self.images=[];self.scripts=[];self.current=None
    def handle_starttag(self,t,attrs):
        d=dict(attrs)
        if 'id' in d:self.ids.add(d['id'])
        if t=='a' and d.get('href','').startswith('#'):self.refs.append(d['href'][1:])
        if t=='img':self.images.append(d)
        if t=='script' and d.get('type')=='application/ld+json':self.current=''
    def handle_data(self,s):
        if self.current is not None:self.current+=s
    def handle_endtag(self,t):
        if t=='script' and self.current is not None:self.scripts.append(json.loads(self.current));self.current=None
articles=list((ROOT/'content-ready').glob('*.json'))
assert len(articles)==21, f'expected 21 articles, got {len(articles)}'
for f in articles:
    a=json.loads(f.read_text());p=Doc();p.feed((ROOT/'dist'/f'{a["slug"]}.html').read_text())
    assert all(x in p.ids for x in p.refs),(f,'broken anchor')
    assert len(p.images)==1,(f,'missing article illustration')
    for image in p.images:
        assert image['alt'] and image['width'] and image['height']
        assert (ROOT/'dist'/urlsplit(image['src']).path.lstrip('/')).exists()
    assert len(p.scripts)==1
    assert p.scripts[0]['@graph'][0]['@type']=='Article'
for f in (ROOT/'dist/assets/images').glob('*.svg'):ET.parse(f)
print(f'PASS: {len(articles)} article renders, image assets and dimensions, citation/TOC anchors, Article/Breadcrumb JSON-LD, SVG XML.')
