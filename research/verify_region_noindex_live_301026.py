#!/usr/bin/env python3
"""Live-Readback 30.10. Abend: Fix #5 (Region noindex + Sitemap-Ausschluss) auf der oeffentlichen URL.
Prueft: Region-Seiten noindex,follow + HTTP 200; Artikel/Datenschutz weiterhin index,follow;
Sitemap 36 locs, 0 Region-URLs, datenschutz enthalten; RSS/llms unverändert frisch."""
import re, sys, urllib.request

BASE = "https://zuhausebleiben-kompass.de/"
UA = {"User-Agent": "Mozilla/5.0 (compatible; zbk-ops-readback/1.0)"}
fails = []

def get(path: str) -> str:
    req = urllib.request.Request(BASE + path, headers=UA)
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")

def robots_of(html: str):
    m = re.search(r'<meta name="robots" content="([^"]*)"', html)
    return m.group(1) if m else None

# 1) Region-Seiten: noindex,follow + 200
for p in ["region/bayern.html", "region/nordrhein-westfalen.html", "region/thueringen.html", "regional.html"]:
    try:
        html = get(p)
        r = robots_of(html)
        ok = r == "noindex,follow"
        print(("PASS" if ok else "FAIL"), p, "-> robots:", r)
        if not ok:
            fails.append(p)
    except Exception as e:  # noqa: BLE001
        print("FAIL", p, "->", e)
        fails.append(p)

# 2) Artikel + Datenschutz: weiterhin index,follow
for p in ["treppenlift-kosten.html", "datenschutz.html"]:
    html = get(p)
    r = robots_of(html)
    ok = r == "index,follow"
    print(("PASS" if ok else "FAIL"), p, "-> robots:", r)
    if not ok:
        fails.append(p)

# 3) Sitemap: 36 locs, 0 Region, datenschutz + Beispielartikel drin
sm = get("sitemap.xml")
locs = re.findall(r"<loc>([^<]+)</loc>", sm)
region_hits = [u for u in locs if "/region/" in u or u.endswith("regional.html")]
checks = [
    (len(locs) == 36, f"sitemap locs = {len(locs)} (erwartet 36)"),
    (len(region_hits) == 0, f"region URLs in Sitemap = {len(region_hits)}"),
    (any(u.endswith("datenschutz.html") for u in locs), "datenschutz.html in Sitemap"),
    (any(u.endswith("treppenlift-kosten.html") for u in locs), "treppenlift-kosten.html in Sitemap"),
    (len(set(locs)) == len(locs), "keine Duplikate"),
]
for ok, label in checks:
    print(("PASS" if ok else "FAIL"), label)
    if not ok:
        fails.append(label)

# 4) RSS/llms unverändert frisch
rss = get("rss.xml")
items = len(re.findall(r"<item>", rss))
llms = get("llms.txt")
print(("PASS" if items == 25 else "FAIL"), f"RSS items = {items}")
print(("PASS" if "treppenlift" in llms else "FAIL"), "llms.txt erreichbar mit Inhalt")
if items != 25 or "treppenlift" not in llms:
    fails.append("rss/llms")

print("---")
print("ALL PASS" if not fails else f"FAILURES: {fails}")
sys.exit(0 if not fails else 1)
