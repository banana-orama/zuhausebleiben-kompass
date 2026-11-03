#!/usr/bin/env python3
"""Live-Readback Audit #9 (Stub-Fold), 2026-11-03 — gegen die ÖFFENTLICHE URL."""
import re, sys, urllib.request

BASE = "https://zuhausebleiben-kompass.de"
fails = []
def check(name, ok, info=""):
    print(("PASS " if ok else "FAIL ") + name + (f"  [{info}]" if info and not ok else ""))
    if not ok: fails.append(name)

def get(path):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "Mozilla/5.0 (zbk-readback)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, r.read().decode("utf-8", errors="replace")

# 1. Weiterleitungsseite
st, stub = get("/pflegegrad-beantragen.html")
check("stub HTTP 200", st == 200, str(st))
rb = re.search(r'name="robots" content="([^"]+)"', stub)
check("stub robots noindex,follow", rb and rb.group(1) == "noindex,follow", rb.group(1) if rb else "none")
rf = re.search(r'http-equiv="refresh" content="0; url=([^"]+)"', stub)
check("stub meta-refresh -> guide", rf and rf.group(1) == BASE + "/pflegegrad-antrag-ablauf-fristen.html", rf.group(1) if rf else "none")
cn = re.search(r'rel="canonical" href="([^"]+)"', stub)
check("stub canonical -> guide", cn and cn.group(1) == BASE + "/pflegegrad-antrag-ablauf-fristen.html", cn.group(1) if cn else "none")
check("stub Flip-Prosa entfernt", "Entwurf zur ersten Orientierung" not in stub)
check("stub Handoff-Link sichtbar", "pflegegrad-antrag-ablauf-fristen.html" in stub and "Diese Seite ist umgezogen" in stub)

# 2. Ziel-Guide unverändert indexierbar
st, guide = get("/pflegegrad-antrag-ablauf-fristen.html")
check("guide HTTP 200", st == 200, str(st))
gb = re.search(r'name="robots" content="([^"]+)"', guide)
check("guide bleibt index,follow", gb and gb.group(1) == "index,follow", gb.group(1) if gb else "none")
check("guide Titel intakt", "Pflegegrad beantragen" in re.search(r"<title>(.*?)</title>", guide, re.S).group(1))

# 3. Sitemap
st, sm = get("/sitemap.xml")
locs = re.findall(r"<loc>([^<]+)</loc>", sm)
check("sitemap 36 locs", len(locs) == 36, str(len(locs)))
check("stub raus aus Sitemap", not any(u.endswith("/pflegegrad-beantragen.html") for u in locs))
check("guide bleibt in Sitemap", any(u.endswith("/pflegegrad-antrag-ablauf-fristen.html") for u in locs))

# 4. llms.txt
st, llms = get("/llms.txt")
check("llms ohne Stub", "/pflegegrad-beantragen.html" not in llms)
check("llms deckt weiter 26 Ratgeber ab", llms.count(".html):") >= 26, str(llms.count(".html):")))

# 5. Regressionen
st, home = get("/")
hb = re.search(r'name="robots" content="([^"]+)"', home)
check("Homepage 200 index,follow", st == 200 and hb.group(1) == "index,follow", hb.group(1) if hb else "none")
st, rss = get("/rss.xml")
check("RSS 26 Items", rss.count("<item>") == 26, str(rss.count("<item>")))
st, dse = get("/datenschutz.html")
check("datenschutz unverändert indexierbar", st == 200 and 'name="robots" content="index,follow"' in dse)

print(f"\n{'ALL PASS' if not fails else 'FAILS: ' + ', '.join(fails)}")
sys.exit(1 if fails else 0)
