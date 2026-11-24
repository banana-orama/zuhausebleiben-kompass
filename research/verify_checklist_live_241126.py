#!/usr/bin/env python3
"""Live-Readback Checklist-8-Deploy auf der öffentlichen URL (Commit 8b8d06d)."""
import re, sys, time, urllib.request, xml.etree.ElementTree as ET
BASE="https://zuhausebleiben-kompass.de"; fails=[]
def get(p, timeout=30):
    req=urllib.request.Request(BASE+p, headers={"User-Agent":"Mozilla/5.0 (readback)"})
    with urllib.request.urlopen(req, timeout=timeout) as r: return r.status, r.read().decode("utf-8","replace")
def check(name, cond, detail=""):
    print(("PASS" if cond else "FAIL"), name, detail)
    if not cond: fails.append(name)
html=None
for i in range(30):
    try:
        st,html=get("/checklisten/badumbau-kosten.html")
        if st==200 and "Badumbau-Budget" in html: print(f"deploy live ab poll {i+1}"); break
    except Exception as e: pass
    time.sleep(10)
st,cl=get("/checklisten/badumbau-kosten.html")
check("checklist 200", st==200, str(st))
m=re.search(r'<meta name="robots" content="([^"]+)"',cl); check("robots index,follow", m and m.group(1)=="index,follow", m and m.group(1))
check("canonical", 'href="https://zuhausebleiben-kompass.de/checklisten/badumbau-kosten.html"' in cl)
check("title pin", "Checkliste: Badumbau-Budget" in cl)
check("h1 pin", "Badumbau-Budget planen" in cl)
check("10-Schritte-OL", cl.count("<ol>")>=1 and "In dieser Reihenfolge: das Budget schützen" in cl)
for needle in ["Pflegegrad prüfen oder beantragen","Auftrag erst nach der Förderzusage","Kostenbausteine: was in einem Angebot ausgewiesen sein muss","Eigenanteil rechnen: Beispielwerte durch eigene Zahlen ersetzen","3.000 bis 7.000","18.000"]:
    check("needle: "+needle[:30], needle in cl)
check("source-back link", 'href="https://zuhausebleiben-kompass.de/badumbau-kosten.html"' in cl)
check("consent default", "window.gtag('consent', 'default'" in cl)
check("no external scripts", not re.search(r'<(?:script|iframe)[^>]+src=["\']https?:', cl))
check("no partner markers", ("awin1.com" not in cl) and ('rel="sponsored"' not in cl))
check("checked_at Stand 2026-11-23", "Stand 2026-11-23" in cl, cl.count("Stand 2026-11-23"))
st,hub=get("/checklisten/index.html")
check("hub 200", st==200)
check("hub Acht-Arbeitsblaetter", "Acht Arbeitsblätter" in hub)
check("hub desc Acht", "Acht kostenlose druckbare Checklisten" in hub)
check("hub 8 Karten", hub.count('class="check-card"')==8, str(hub.count('class="check-card"')))
check("hub card new", '/checklisten/badumbau-kosten.html' in hub)
ld=re.search(r'<script type="application/ld\+json">(.*?)</script>',hub,re.S).group(1)
import json as J; g=J.loads(ld)["@graph"]; check("jsonld 8 items", len(g[1]["itemListElement"])==8, str(len(g[1]["itemListElement"])))
st,sm=get("/sitemap.xml"); ET.fromstring(sm)
locs=re.findall(r"<loc>([^<]+)</loc>",sm)
cl_urls=[u for u in locs if "/checklisten/" in u]
check("sitemap 55 locs", len(locs)==55, str(len(locs)))
check("sitemap 9 checklist urls", len(cl_urls)==9, str(len(cl_urls)))
check("new in sitemap", any(u.endswith("/checklisten/badumbau-kosten.html") for u in locs))
st,rss=get("/rss.xml"); items=rss.count("<item>")
check("rss 41 items", items==41, str(items))
st,home=get("/"); rm=re.search(r'<meta name="robots" content="([^"]+)"',home); check("home index,follow", rm and rm.group(1)=="index,follow")
st,llms=get("/llms.txt"); check("llms 200", st==200)
print(); print("RESULT:", "ALL PASS" if not fails else f"{len(fails)} FAILS: {fails}")
sys.exit(1 if fails else 0)
