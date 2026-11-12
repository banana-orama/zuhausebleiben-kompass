#!/usr/bin/env python3
"""Live-Readback für Briefing 24 auf der öffentlichen URL (nach CI 424d925 success).
Pollt erst auf HTTP 200 (Pages-Deploy-Lag), dann: robots, Metadaten, Kernzahlen,
Absenzen, 2 Lead-Absätze, CTA/Anker, Related-Reihenfolge, SVG 200, Sitemap 46 locs,
RSS 35, Homepage, llms. Jede Assertion 4x geprüft (2 curl-Runden je 2x)."""
import re
import subprocess
import sys
import time

BASE = "https://zuhausebleiben-kompass.de"
SLUG = "wohnung-anpassen-nach-krankenhausentlassung"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124.0"

FAIL = []
N = 0


def check(label, cond, detail=""):
    global N
    N += 1
    print(("PASS " if cond else "FAIL ") + label + ("" if cond else f"  {detail}"))
    if not cond:
        FAIL.append(label)


def fetch(url):
    r = subprocess.run(["curl", "-sL", "--max-time", "45", "-A", UA, url], capture_output=True, text=True)
    return r.stdout


# Deploy-Lag abwarten: neuer Pfad kann 404 liefern, während alte Seiten 200 liefern
for attempt in range(20):
    page = fetch(f"{BASE}/{SLUG}.html")
    if page and "<h1" in page and "Entlassung" in page:
        break
    print(f"Warte auf Deploy ({attempt + 1}/20)...")
    time.sleep(15)

# Kern-Assertions 2 Runden x 2 Abrufe
for round_no in (1, 2):
    h1 = fetch(f"{BASE}/{SLUG}.html")
    h2 = fetch(f"{BASE}/{SLUG}.html")
    check(f"R{round_no} HTTP 200 + H1", "Wohnung nach der Krankenhausentlassung anpassen" in h1)
    check(f"R{round_no} robots index,follow", 'name="robots" content="index,follow"' in h1 or 'content="index,follow"' in h1)
    check(f"R{round_no} title", "Krankenhausentlassung: Wohnung anpassen" in h1)
    for needle in ["spätestens am fünften Arbeitstag", "25 Arbeitstage", "etwa fünf Kalenderwochen",
                   "Pflegegrade 2 bis 5", "acht Wochen pro Kalenderjahr", "zehnten Arbeitstag",
                   "bis zu 7 Tage", "Entlassmanagement"]:
        check(f"R{round_no} Kernzahl: {needle[:36]}", needle in h1 and needle in h2)
    for needle in ["4.180", "16.720", "KfW", "awin", 'rel="sponsored"', "data-partner-placement"]:
        check(f"R{round_no} Absenz 0x {needle}", h1.count(needle) == 0, str(h1.count(needle)))
    check(f"R{round_no} 2 Lead-Absätze", h1.count('<p class="lead">') == 2)
    check(f"R{round_no} kein Komma-Splice", ".,Dieser" not in h1)
    check(f"R{round_no} CTA wohnumfeld", "/wohnumfeldverbesserung-beantragen.html" in h1)
    check(f"R{round_no} data-content-id", f'data-content-id="{SLUG}"' in h1)
    check(f"R{round_no} Quellenstand 2026-11-12", "2026-11-12" in h1)
    rel = h1[h1.find("Passend dazu"):h1.find("</section>", h1.find("Passend dazu"))]
    order = re.findall(r'href="([^"]+)"', rel)
    check(f"R{round_no} related 3", len(order) == 3, str(order))
    if len(order) == 3:
        check(f"R{round_no} related Reihenfolge", all(k in order[i] for i, k in
              enumerate(["treppenlift-foerderung-ohne-pflegegrad", "hausnotruf-kosten-anbieter-vergleich", "treppenlift-mieten"])), str(order))

svg = fetch(f"{BASE}/assets/images/krankenhaus-entlassung-wegweiser.svg")
check("SVG 200 + viewBox", "viewBox=\"0 0 780 620\"" in svg and "drei Zeithorizonte" in svg)
sm = fetch(f"{BASE}/sitemap.xml")
check("Sitemap enthält neuen Artikel", SLUG in sm)
check("Sitemap 46 locs", sm.count("<loc>") == 46, str(sm.count("<loc>")))
rss = fetch(f"{BASE}/rss.xml")
check("RSS 35 items", rss.count("<item>") == 35, str(rss.count("<item>")))
home = fetch(f"{BASE}/")
check("Homepage 200 + Artikel verlinkt", "ZuhauseBleiben" in home and SLUG in home)
llms = fetch(f"{BASE}/llms.txt")
check("llms.txt enthält Artikel", SLUG in llms)

print(f"\n{N - len(FAIL)}/{N} Pässe")
if FAIL:
    print(f"FAILS ({len(FAIL)}):")
    for f in FAIL:
        print(" -", f)
    sys.exit(1)
print("LIVE READBACK ALL PASS")
