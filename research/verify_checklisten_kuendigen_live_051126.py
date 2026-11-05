#!/usr/bin/env python3
"""Live-Readback: 7. Checkliste hausnotruf-kuendigen auf der oeffentlichen URL (Cron-Lauf 05.11.)."""
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET

BASE = "https://zuhausebleiben-kompass.de"
fails = []


def check(name, cond, detail=""):
    print(("PASS" if cond else "FAIL"), name, detail)
    if not cond:
        fails.append(name)


def get(path):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "Mozilla/5.0 (readback)"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except Exception as e:
        return 0, str(e)


st, pg = get("/checklisten/hausnotruf-kuendigen.html")
check("new checklist 200", st == 200, str(st))
check("robots index,follow", 'name="robots" content="index,follow"' in pg)
check("canonical", 'rel="canonical" href="' + BASE + '/checklisten/hausnotruf-kuendigen.html"' in pg)
check("title", "Checkliste: Hausnotruf kündigen" in pg)
check("source-back link", 'href="' + BASE + '/hausnotruf-kuendigen.html"' in pg)
check("print button", "Checkliste drucken" in pg)
check("3 check-blocks", pg.count('class="check-block"') == 3, str(pg.count('class="check-block"')))
check("KI disclosure", "KI-Unterstützung" in pg)
check("no tracking loader", not re.search(r"googletagmanager\.com|google-analytics\.com|stape\.io", pg))
check("stand 05.11.", "Stand 2026-11-05" in pg)

st, hub = get("/checklisten/index.html")
check("hub 200", st == 200, str(st))
check("hub sieben Arbeitsblaetter", "Sieben Arbeitsblätter" in hub)
check("hub 7 cards", hub.count('class="check-card"') == 7, str(hub.count('class="check-card"')))
m = re.search(r'<script type="application/ld\+json">(.*?)</script>', hub, re.S)
try:
    ld = json.loads(m.group(1))
    check("hub JSON-LD parses", True)
    check("hub ItemList 7 items", len(ld["@graph"][1]["itemListElement"]) == 7)
    urls = [i["url"] for i in ld["@graph"][1]["itemListElement"]]
    check("ItemList has new slug", BASE + "/checklisten/hausnotruf-kuendigen.html" in urls)
except Exception as e:
    check("hub JSON-LD parses", False, str(e))

st, sm = get("/sitemap.xml")
locs = re.findall(r"<loc>([^<]+)</loc>", sm)
cl = [u for u in locs if "/checklisten/" in u]
check("sitemap 8 checklist URLs", len(cl) == 8, str(len(cl)))
check("sitemap includes new slug", any(u.endswith("/checklisten/hausnotruf-kuendigen.html") for u in cl))

st, rss = get("/rss.xml")
check("rss 28 items unchanged", rss.count("<item>") == 28, str(rss.count("<item>")))
st, home = get("/")
check("home 200", st == 200)
check("home nav checklisten", 'href="' + BASE + '/checklisten/index.html"' in home)

print()
print("RESULT:", "ALL PASS" if not fails else f"{len(fails)} FAILS: {fails}")
sys.exit(1 if fails else 0)
