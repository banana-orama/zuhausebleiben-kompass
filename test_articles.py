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
assert len(articles)==30, f'expected 30 articles, got {len(articles)}'
for f in articles:
    a=json.loads(f.read_text());p=Doc();p.feed((ROOT/'dist'/f'{a["slug"]}.html').read_text())
    assert all(x in p.ids for x in p.refs),(f,'broken anchor')
    assert len(p.images)==1,(f,'missing article illustration')
    for image in p.images:
        assert image['alt'] and image['width'] and image['height']
        assert (ROOT/'dist'/urlsplit(image['src']).path.lstrip('/')).exists()
    assert len(p.scripts)==1
    assert p.scripts[0]['@graph'][0]['@type']=='Article'
    art=schemas=[s for s in p.scripts if any(n.get('@type')=='Article' for n in s.get('@graph',[]))][0]['@graph'][0]
    imgs=art['image']
    assert isinstance(imgs,list) and len(imgs)==2,(f,'Article.image must list og PNG + SVG')
    assert imgs[0].startswith('https://') and imgs[0].endswith('/assets/images/og-zuhausebleiben-kompass.png'),(f,'Article.image[0] must be the >=1200px PNG')
    assert imgs[1].endswith('.svg'),(f,'Article.image[1] should keep the article SVG')
for f in (ROOT/'dist/assets/images').glob('*.svg'):ET.parse(f)
print(f'PASS: {len(articles)} article renders, image assets and dimensions, citation/TOC anchors, Article/Breadcrumb JSON-LD, SVG XML.')
