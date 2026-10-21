#!/usr/bin/env python3
"""Live-Readback der öffentlichen URL nach Deploy 370f848."""
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET

BASE = "https://zuhausebleiben-kompass.de"
fails = []


def get(path):
    req = urllib.request.Request(BASE + path, headers={"Cache-Control": "no-cache", "User-Agent": "zbk-live-readback/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, r.read().decode("utf-8", "replace")


def check(name, cond, detail=""):
    print(("PASS" if cond else "FAIL"), name, detail)
    if not cond:
        fails.append(name)


s, hub = get("/checklisten/index.html")
check("hub 200", s == 200, str(s))
check("hub robots index", '<meta name="robots" content="index,follow">' in hub)
check("hub canonical", 'rel="canonical" href="https://zuhausebleiben-kompass.de/checklisten/index.html"' in hub)
check("hub h1", "Checklisten zum Ausdrucken" in hub)
check("hub 6 cards", hub.count('class="check-card"') == 6, str(hub.count('class="check-card"')))
check("hub jsonld schema.org", '"@context":"https://schema.org"' in hub)
check("hub no tracking loader", not re.search(r"googletagmanager\.com|stape\.io", hub))

for slug in ["tuerbreiten-schwellen-schnellcheck", "pflegegrad-antrag-ablauf-fristen", "badumbau-angebote-vergleichen"]:
    s, pg = get(f"/checklisten/{slug}.html")
    check(f"{slug} 200+index", s == 200 and 'content="index,follow"' in pg, str(s))

s, home = get("/")
check("home 200", s == 200)
check("home nav checklisten", 'href="https://zuhausebleiben-kompass.de/checklisten/index.html"' in home)
check("home faq fix", "als Vorschau" not in home and "öffentlich verfügbar" in home)

s, sm = get("/sitemap.xml")
locs = re.findall(r"<loc>([^<]+)</loc>", sm)
check("sitemap 200+xml", s == 200 and sm.startswith("<?xml"))
check("sitemap 42 locs", len(locs) == 42, str(len(locs)))
check("sitemap 7 checklisten", len([u for u in locs if "/checklisten/" in u]) == 7)
check("sitemap no draft", not any("treppenlift-angebote-vergleichen" in u for u in locs))

s, rss = get("/rss.xml")
check("rss 200", s == 200)
check("rss new desc", "Unabhängiger Ratgeber" in rss and "Noch keine verifizierten" not in rss)
check("rss 19 items", rss.count("<item>") == 19, str(rss.count("<item>")))

s, llms = get("/llms.txt")
check("llms 200", s == 200)
check("llms articles", llms.count("](https://zuhausebleiben-kompass.de/") >= 21, str(llms.count("](https://zuhausebleiben-kompass.de/")))
check("llms no draft", "treppenlift-angebote-vergleichen" not in llms)

# Briefing-9-Artikel weiterhin live (Regression aus dem Batch-Push)
s, d = get("/hilfsmittel-dusch-wc-uebernahme.html")
check("briefing9 still live", s == 200 and 'content="index,follow"' in d)

print()
print("RESULT:", "ALL PASS" if not fails else f"{len(fails)} FAILS: {fails}")
sys.exit(1 if fails else 0)
