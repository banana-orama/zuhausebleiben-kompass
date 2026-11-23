#!/usr/bin/env python3
"""Live-Readback 23.11.2026 (Commit 585eded): 3 geänderte Artikel auf der öffentlichen URL.
Pollt bis zum Pages-Deploy-Lag (200 + neuer Content), dann Kern-Assertions."""
import re
import sys
import time
import urllib.request

BASE = "https://zuhausebleiben-kompass.de"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) LiveReadback/231126"}

PAGES = [
    ("hilfsmittel-dusch-wc-uebernahme.html", ["7,50", "15 Euro", "1. Januar 2027", "BGBl. 2026 I Nr. 228", "7,50 €/15 €"]),
    ("hilfsmittel-pflegekasse-uebernahme.html", ["7,50", "15 Euro", "1. Januar 2027", "Neufassung des § 61 SGB V", "Quellenstand: 2026-11-23"]),
    ("rollator-auswahl-passform-kosten.html", ["7,50", "15 Euro", "1. Januar 2027"]),
]

def get(url, timeout=30):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode("utf-8", errors="replace")

fails = []
# 1) Deploy-Lag: poll erster Artikel bis needle live
deadline = time.time() + 8 * 60
deployed = False
while time.time() < deadline:
    try:
        st, h = get(f"{BASE}/hilfsmittel-dusch-wc-uebernahme.html")
        if st == 200 and "7,50" in h:
            deployed = True
            print(f"Deploy-Poll: live nach {int(8*60 - (deadline - time.time()))}s")
            break
    except Exception as e:
        print("poll:", str(e)[:80])
    time.sleep(20)
if not deployed:
    print("FAIL: Deploy-Lag > 8 min, neuer Inhalt nicht sichtbar")
    fails.append(("deploy-lag",))
else:
    # 2) Artikel-Assertions
    for path, needles in PAGES:
        st, h = get(f"{BASE}/{path}")
        plain = re.sub(r"<[^>]+>", " ", h)
        robots = re.search(r'name="robots" content="([^"]+)"', h)
        ok_robots = robots and robots.group(1).replace(" ", "") == "index,follow"
        missing = [n for n in needles if n not in h and n not in plain]
        canon = re.search(r'rel="canonical" href="([^"]+)"', h)
        print(f"{path}: {st} robots={robots.group(1) if robots else '?'} canon={'ok' if canon else '?'} needles={'ALL' if not missing else missing}")
        if st != 200 or missing or not ok_robots:
            fails.append((path, st, missing))
    # 3) Sitemap + RSS + Homepage + llms
    st, sm = get(f"{BASE}/sitemap.xml")
    locs = sm.count("<loc>")
    print(f"sitemap: {st} locs={locs}")
    if st != 200 or locs != 53:
        fails.append(("sitemap", st, locs))
    st, rss = get(f"{BASE}/rss.xml")
    items = rss.count("<item>")
    print(f"rss: {st} items={items}")
    if st != 200 or items != 40:
        fails.append(("rss", st, items))
    st, home = get(f"{BASE}/")
    robots = re.search(r'name="robots" content="([^"]+)"', home)
    print(f"homepage: {st} robots={robots.group(1) if robots else '?'}")
    if st != 200 or (robots and "index" not in robots.group(1)):
        fails.append(("homepage", st))
    st, llms = get(f"{BASE}/llms.txt")
    print(f"llms.txt: {st} bytes={len(llms)}")
    if st != 200:
        fails.append(("llms", st))
    # 4) Alte-Fehlerklasse: pflegekasse Quellenstand frisch, duschwc Tabellenzelle korrekt
    st, h = get(f"{BASE}/hilfsmittel-dusch-wc-uebernahme.html")
    if 'source-9' not in h:
        fails.append(("duschwc-source-9 fehlt",))

print("FAILS:", len(fails))
sys.exit(1 if fails else 0)
