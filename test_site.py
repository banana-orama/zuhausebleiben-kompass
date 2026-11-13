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
        # 13.11.2026: Nordrhein-Westfalen ist als erste Region ausgebaut
        # (data/region-nrw.json, 10 Quellen mit checked_at) und MUSS im Launch-Build
        # indexierbar sein; Hub und alle übrigen Regionen bleiben Platzhalter (noindex).
        if f.name == 'nordrhein-westfalen.html':
            assert not p.noindex,(f,'expanded NRW region must be indexable at launch')
        else:
            assert p.noindex,(f,'region placeholder must stay noindex until expanded')
    elif f.name == 'pflegegrad-beantragen.html':
        # Audit #9 (2026-11-03): dünner Legacy-Stub in den Antrag-Ratgeber gefaltet —
        # die Weiterleitungsseite bleibt dauerhaft noindex und außerhalb der Sitemap.
        assert p.noindex,(f,'redirect stub must stay noindex (audit #9 fold)')
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
_region_locs=[u for u in locs if '/region/' in u or u.endswith('/regional.html')]
assert _region_locs==[u for u in _region_locs if u.endswith('/region/nordrhein-westfalen.html')] and len(_region_locs)==1,('exactly the expanded NRW region belongs in the sitemap — no hub, no placeholders (fix #5 + 13.11. expansion)',_region_locs)
assert not any(u.endswith('/pflegegrad-beantragen.html') for u in locs),('redirect stub must stay out of the sitemap (audit #9)',)
assert len(locs)==len(set(locs)),('duplicate sitemap URLs',)
# Audit #9: Weiterleitungsseite muss auf den Antrag-Ratgeber zeigen (Meta-Refresh + Canonical),
# und die vor-Launch-Prosa „Entwurf zur ersten Orientierung" darf nirgends mehr im Launch-Build stehen.
stub=(root/'pflegegrad-beantragen.html').read_text()
guide_url=json.loads((root.parent/'data/content.json').read_text())['brand']['base_url'].rstrip('/')+'/pflegegrad-antrag-ablauf-fristen.html'
assert 'http-equiv="refresh"' in stub and 'pflegegrad-antrag-ablauf-fristen.html' in stub,('stub must meta-refresh to the guide',)
assert ('rel="canonical" href="'+guide_url+'"') in stub,('stub canonical must point to the guide',guide_url)
assert not any('Entwurf zur ersten Orientierung' in f.read_text() for f in files),('pre-launch draft prose must be gone from the launch build (audit #9)',)
# Audit #6b/#10 (2026-11-03): og:image >=1200px (PNG, nicht nur SVG), twitter card und
# explizite Referrer-Policy auf JEDER Seite; og:image-Maße/alt gesetzt; og:url = canonical.
import struct
OG_PNG=root/'assets'/'images'/'og-zuhausebleiben-kompass.png'
assert OG_PNG.exists(),('og PNG missing from build',)
_b=OG_PNG.read_bytes()
assert _b[:8]==b'\x89PNG\r\n\x1a\n',('og asset is not a PNG',)
_w,_h=struct.unpack('>II',_b[16:24]);assert _w>=1200 and _h>=630,('og PNG too small',_w,_h)
_base=json.loads((root.parent/'data/content.json').read_text())['brand']['base_url'].rstrip('/')
OG_URL=_base+'/assets/images/og-zuhausebleiben-kompass.png'
for f in files:
    h=f.read_text()
    assert ('property="og:image" content="'+OG_URL+'"') in h,(f,'og:image missing/wrong')
    assert 'property="og:image:width" content="1200"' in h,(f,'og:image:width missing')
    assert 'property="og:image:height" content="630"' in h,(f,'og:image:height missing')
    assert 'property="og:image:alt" content="' in h and 'content="ZuhauseBleiben Kompass — Ratgeber' in h,(f,'og:image:alt missing')
    assert '<meta name="twitter:card" content="summary_large_image">' in h,(f,'twitter card missing')
    assert '<meta name="referrer" content="strict-origin-when-cross-origin">' in h,(f,'referrer policy missing')
    _can=(h.split('rel="canonical" href="')[1].split('"')[0]) if 'rel="canonical" href="' in h else ''
    assert _can and ('property="og:url" content="'+_can+'"') in h,(f,'og:url must mirror canonical')
mode='PREVIEW (noindex)' if not __import__('os').environ.get('INDEX') else 'LAUNCH (index)'
print(f'PASS: {len(files)} HTML pages, internal links, single H1, no forms, datenschutz in sitemap ({len(locs)} locs), {mode}, XML valid.')
