#!/usr/bin/env python3
"""Live-Readback treppenlift-sitzlift-oder-stehlift auf der öffentlichen URL.
Erst nach Push + CI + Deploy laufen lassen (public URL, kein origin-only Check)."""
import pathlib
import re
import sys
import urllib.request

BASE = "https://zuhausebleiben-kompass.de"
SLUG = "treppenlift-sitzlift-oder-stehlift"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124 Safari/537.36"}

FAIL = []
N = 0


def fetch(path: str) -> str:
    req = urllib.request.Request(BASE + path, headers=UA)
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.read().decode("utf-8", errors="replace")


def check(label, cond, detail=""):
    global N
    N += 1
    print(("PASS " if cond else "FAIL ") + label + ("" if cond else f"  {detail}"))
    if not cond:
        FAIL.append(label)


# Artikel live
html = fetch(f"/{SLUG}.html")
check("HTTP 200 + HTML", html.lstrip().startswith("<!DOCTYPE") or "<html" in html[:200])
check("robots index,follow", re.search(r'name="robots" content="index,?\s*follow"', html) is not None)
check("h1 live", "Sitzlift oder Stehlift" in html)
check("Canonical", f'href="{BASE}/{SLUG}.html"' in html)
for needle in ["Mindestbreite von 80 cm", "Mindestens 55 cm", "etwa 4.000 Euro",
               "12 Monate und 14 Tage", "gängigste Art", "skriptgeprüfte Absenz",
               "06.11.2026", "Angebots-Checkliste: die Fragen vor dem Aufmaß",
               "Anbieter für Sitz- und Stehlifte vergleichen"]:
    check(f"live enthält '{needle}'", needle in html)
check("SVG live", 'src="/assets/images/treppenlift-sitzsteh-entscheidung.svg"' in html)
check("Quellen-Lifta-Stehlift", "lifta.de/treppenlift/stehlift" in html)
check("Quellen-VZ", "verbraucherzentrale.de" in html)
check("kein Partner-Marker", "data-partner-placement" not in html)
check("Quellenstand-Zeile", "Quellenstand: 2026-11-06" in html)

# SVG selbst live
svg = fetch("/assets/images/treppenlift-sitzsteh-entscheidung.svg")
check("SVG 200 + Stand", "06.11.2026" in svg and svg.lstrip().startswith("<svg"))

# Sitemap: Artikel drin, RSS 29 Items
sm = fetch("/sitemap.xml")
check("Sitemap enthält Artikel", f"{SLUG}.html" in sm)
check("Sitemap keine Region-URLs", "/region/" not in sm)
rss = fetch("/rss.xml")
check("RSS 29 Items", rss.count("<item>") == 29, str(rss.count("<item>")))

# Homepage listet den neuen Ratgeber
home = fetch("/")
check("Homepage listet Artikel", f'href="{BASE}/{SLUG}.html"' in home or f"/{SLUG}.html" in home)

# llms.txt aktualisiert
llms = fetch("/llms.txt")
check("llms.txt listet Artikel", SLUG in llms)

print(f"\n{N - len(FAIL)}/{N} PASS")
sys.exit(1 if FAIL else 0)
