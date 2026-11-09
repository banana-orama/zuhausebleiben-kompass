#!/usr/bin/env python3
"""Live-Readback treppenlift-finanzierung auf der öffentlichen URL (nach CI success):
Deploy-Lag abwarten (404→200-Poll), dann Kern-Assertions gegen den Live-HTML-Stand."""
import re
import sys
import time
import urllib.request

BASE = "https://zuhausebleiben-kompass.de"
URL = f"{BASE}/treppenlift-finanzierung.html"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
fails = []


def get(url, timeout=30):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode("utf-8", errors="replace")


def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + ("" if cond else f"  {detail}"))
    if not cond:
        fails.append(name)


# Deploy-Lag: bis zu 5 min auf HTTP 200 pollen
status, html = 0, ""
deadline = time.time() + 300
while time.time() < deadline:
    try:
        status, html = get(URL)
        if status == 200:
            break
    except Exception as e:
        print(f"poll: {URL} -> {type(e).__name__}")
    time.sleep(15)
check("Artikel live HTTP 200", status == 200, str(status))

if status == 200:
    check("robots index,follow", 'name="robots" content="index,follow"' in html.replace(", ", ","))
    check("H1", "Treppenlift finanzieren: Ratenzahlung, Ihre Rechte und die Reform" in html)
    for needle in ["4 180 Euro je Maßnahme", "2 bis 60 Monaten", "max. 10.000",
                   "20. November 2026", "159,17", "356d BGB", "unentgeltlichen Darlehensvertrag",
                   "09.11.2026", "KI-unterstützt"]:
        check(f"live enthält '{needle}'", needle in html)
    check("CTA Förderung zuerst", "Förderung zuerst prüfen" in html)
    check("CTA-Ziel zuschuss", "href=\"https://zuhausebleiben-kompass.de/treppenlift-zuschuss.html\"" in html)
    check("kein awin-Tracker", "awin1.com" not in html)
    check("SVG-Pfad referenziert", "assets/images/treppenlift-finanzierung-wegweiser.svg" in html)
    check("Quellenstand sichtbar", "2026-11-09" in html)
    st_svg, svg = get(f"{BASE}/assets/images/treppenlift-finanzierung-wegweiser.svg")
    check("SVG live 200", st_svg == 200, str(st_svg))
    check("SVG viewBox", "viewBox=\"0 0 780 620\"" in svg)

st_home, home = get(BASE + "/")
check("Homepage 200", st_home == 200, str(st_home))
check("Homepage listet Ratgeber", "treppenlift-finanzierung.html" in home)
check("Homepage robots", 'index,follow' in home.replace(", ", ","))

st_sm, sitemap = get(BASE + "/sitemap.xml")
locs = sitemap.count("<loc>")
check("Sitemap 200", st_sm == 200, str(st_sm))
check("Sitemap inkl. Artikel", "treppenlift-finanzierung.html" in sitemap)
# Referenz: LAUNCH-dist-Build vom 09.11. (42 locs — Regionen/Redirects bewusst draußen)
check("Sitemap exakt 42 locs (LAUNCH-Referenz)", locs == 42, str(locs))

st_rss, rss = get(BASE + "/rss.xml")
items = rss.count("<item>")
check("RSS 200", st_rss == 200, str(st_rss))
check("RSS 31 Items", items == 31, str(items))
check("RSS listet Artikel", "treppenlift-finanzierung.html" in rss)

st_llms, llms = get(BASE + "/llms.txt")
check("llms.txt 200", st_llms == 200, str(st_llms))
check("llms listet Artikel", "treppenlift-finanzierung" in llms)

print(f"\nRESULT: {'ALL PASS' if not fails else str(len(fails)) + ' FAILS'}")
sys.exit(1 if fails else 0)
