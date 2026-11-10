#!/usr/bin/env python3
"""Live-Readback für hausnotruf-angehoerige-einrichten (Briefing 21, Deploy d214dd0).
Prüft die ÖFFENTLICHE URL (nicht origin-only): HTTP 200, robots index,follow,
Kernzahlen im HTML, SVG 200, Sitemap/RSS/Homepage, Canonical, kein Partner-Marker.
Muster: verify_schluessel_live_061126.py."""
import pathlib
import subprocess
import sys
import time

BASE = "https://zuhausebleiben-kompass.de"
URL = f"{BASE}/hausnotruf-angehoerige-einrichten.html"
SVG = f"{BASE}/assets/images/hausnotruf-angehoerige-wegweiser.svg"

FAIL = []
N = 0


def check(label, cond, detail=""):
    global N
    N += 1
    print(("PASS " if cond else "FAIL ") + label + ("" if cond else f"  {detail}"))
    if not cond:
        FAIL.append(label)


def curl(url, extra=None):
    cmd = ["curl", "-sL", "--max-time", "30", "-w", "\n%{http_code}", url]
    if extra:
        cmd = extra + cmd[1:] if False else cmd
    r = subprocess.run(cmd, capture_output=True, text=True)
    body, _, code = r.stdout.rpartition("\n")
    return code.strip(), body


# 1. Poll bis 200 (Pages-Deploy-Lag)
deadline = time.time() + 8 * 60
code, html = "000", ""
while time.time() < deadline:
    code, html = curl(URL)
    if code == "200":
        break
    print(f"poll: {URL} -> {code}, waiting...")
    time.sleep(20)
check("live 200", code == "200", code)

if code == "200":
    # 2. robots + canonical
    check("robots index,follow", "index,follow" in html.replace(", ", ","))
    check("canonical", 'rel="canonical" href="https://zuhausebleiben-kompass.de/hausnotruf-angehoerige-einrichten.html"' in html)
    # 3. Kernzahlen/Wortlaute (Prosa-Schreibweise)
    for needle in ["27 und 40 Euro", "bis zu 27 Euro", "drei Wochen", "fünf Wochen",
                   "innerhalb einer Woche", "bis zu 50 Metern", "30 bis 50 Euro",
                   "Vorsorgevollmacht für Vermögenssorge", "Versorgungsvertrag nach § 78 SGB XI",
                   "funktionsfertig", "reine Gesundheitsvollmacht", "Vertragspartner der Pflegekasse",
                   "10.11.2026", "KI-unterstützt"]:
        check(f"live enthält '{needle}'", needle in html)
    # 4. CTA + kein Partner
    check("early CTA kosten-vergleich", "hausnotruf-kosten-anbieter-vergleich.html" in html and "compare_top" in html)
    check("kein Partner-Marker", "data-partner-placement" not in html)
    check("kein awin Tracker", "awin1.com" not in html)
    # 5. SVG + Sitemap + RSS + Homepage
    sc, _ = curl(SVG)
    check("svg live 200", sc == "200", sc)
    sc, sm = curl(f"{BASE}/sitemap.xml")
    check("sitemap live 200", sc == "200", sc)
    check("sitemap enthält neuen Artikel", "hausnotruf-angehoerige-einrichten.html" in sm)
    import re
    locs = len(re.findall(r"<loc>", sm))
    check("sitemap loc count 43", locs == 43, str(locs))
    sc, rss = curl(f"{BASE}/rss.xml")
    check("rss live 200", sc == "200", sc)
    check("rss enthält neuen Artikel", "hausnotruf-angehoerige-einrichten" in rss)
    sc, home = curl(BASE + "/")
    check("homepage live 200", sc == "200", sc)
    check("homepage verlinkt neuen Artikel", "hausnotruf-angehoerige-einrichten" in home)
    # 6. llms.txt
    sc, ll = curl(f"{BASE}/llms.txt")
    check("llms.txt live 200", sc == "200", sc)
    check("llms.txt enthält neuen Artikel", "hausnotruf-angehoerige-einrichten" in ll)

print(f"\n{N - len(FAIL)}/{N} PASS")
sys.exit(1 if FAIL else 0)
