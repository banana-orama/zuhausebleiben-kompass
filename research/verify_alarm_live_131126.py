#!/usr/bin/env python3
"""Live-Readback Briefing 26: https://zuhausebleiben-kompass.de/hausnotruf-alarm-ablauf.html (+Site-Assets)."""
import json
import re
import sys
import urllib.request
from html import unescape

BASE = "https://zuhausebleiben-kompass.de"
fails = []
n = 0


def check(label, cond, detail=""):
    global n
    n += 1
    print(("PASS " if cond else "FAIL ") + label + (f"  {detail}" if (detail and not cond) else ""))
    if not cond:
        fails.append(label)


def get(path):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, r.read().decode("utf-8", "ignore")


code, art = get("/hausnotruf-alarm-ablauf.html")
check("artikel HTTP 200", code == 200, str(code))
check("robots index,follow live", 'content="index,follow"' in art)
check("canonical live", "https://zuhausebleiben-kompass.de/hausnotruf-alarm-ablauf.html" in art)
check("H1 live", "Hausnotruf-Alarm: was nach dem Knopfdruck passiert" in art)

body = re.sub(r"\s+", " ", unescape(art))
low = body.lower()
for needle in ["94 prozent", "80 prozent fehlalarm, probealarm",
               "iii zr 92/16", "bereitschafts- oder rettungsdienst", "maßnahmenplan",
               "lieber einmal zu oft als einmal zu wenig", "11.000 rufe", "23.000 teilnehmer"]:
    check(f"live-needle '{needle}'", needle in low)

check("svg live verlinkt", "hausnotruf-alarmkette.svg" in art)
check("partner placement live", 'data-placement-id="malteser_beratungstermin"' in art)
check("rel sponsored live", 'rel="sponsored noopener"' in art)
check("early-cta live", "/hausnotruf-kosten-anbieter-vergleich.html" in art and 'data-cta-id="compare_top"' in art)
check("quellen-live: bv-hausnotruf", "https://www.bv-hausnotruf.de/hausnotruf/ablauf-eines-notrufs" in art)
check("quellen-live: bgh nwb", "https://datenbank.nwb.de/Dokument/697288/" in art)
check("keine_vorschau-prosa", "Entwurf zur ersten Orientierung" not in art)

code2, svg = get("/assets/images/hausnotruf-alarmkette.svg")
check("svg HTTP 200", code2 == 200, str(code2))
check("svg viewBox 1200x800", 'viewBox="0 0 1200 800"' in svg)

code3, sm = get("/sitemap.xml")
locs = re.findall(r"<loc>([^<]+)</loc>", sm)
check("sitemap HTTP 200", code3 == 200)
check("sitemap 48 locs", len(locs) == 48, str(len(locs)))
check("artikel in sitemap", any("hausnotruf-alarm-ablauf" in u for u in locs))

code4, rss = get("/rss.xml")
import xml.etree.ElementTree as ET
try:
    items = ET.fromstring(rss.encode("utf-8")).findall(".//item")
    check("rss 37 items", len(items) == 37, str(len(items)))
    check("rss enthält artikel", any("hausnotruf-alarm-ablauf" in (i.find("link").text or "") for i in items))
except Exception as e:
    check("rss parse", False, str(e))

code5, llms = get("/llms.txt")
check("llms 200", code5 == 200)
check("llms nennt artikel", "/hausnotruf-alarm-ablauf.html" in llms)

code6, home = get("/")
check("homepage 200 + nav", code6 == 200 and "hausnotruf-alarm-ablauf" in home)

code7, dse = get("/datenschutz.html")
check("dse nennt malteser", "Malteser" in dse)

# Placement darf NICHT auf anderen Artikeln sein (Marker-Disziplin)
code8, other = get("/hausnotruf-mobil-gps-unterwegs.html")
check("kein placement auf mobil-gps", "data-placement-id" not in other)

print(f"\n{n - len(fails)}/{n} checks PASS")
sys.exit(1 if fails else 0)
