#!/usr/bin/env python3
"""Live-Readback Briefing 23 (treppenlift-foerderung-ohne-pflegegrad) auf der öffentlichen URL.
Pollt den neuen Artikel bis 200 (Pages-Deploy-Lag), prüft robots/canonical/Kernzahlen/CTA/
Partner-Absenz/SVG/Sitemap/RSS/Homepage/llms. Muster: verify_unserioese_live_101126.py."""
import re
import subprocess
import sys
import time
from html import unescape

BASE = "https://zuhausebleiben-kompass.de"
SLUG = "treppenlift-foerderung-ohne-pflegegrad"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126.0 Safari/537.36"

FAIL = []
N = 0


def check(label, cond, detail=""):
    global N
    N += 1
    print(("PASS " if cond else "FAIL ") + label + ("" if cond else f"  {detail}"))
    if not cond:
        FAIL.append(label)


def fetch(url):
    r = subprocess.run(["curl", "-sL", "--max-time", "40", "-A", UA, "-w", "\n%{http_code}", url],
                       capture_output=True, text=True)
    body, _, code = r.stdout.rpartition("\n")
    return body, code.strip()


# 1. Artikel bis 200 (Deploy-Lag)
html, code = "", ""
for attempt in range(30):
    html, code = fetch(f"{BASE}/{SLUG}.html")
    if code == "200" and len(html) > 10000:
        break
    print(f"attempt {attempt + 1}: HTTP {code}, poll...")
    time.sleep(20)
check("Artikel HTTP 200", code == "200", code)
html = unescape(html)
check("robots index,follow", 'name="robots" content="index,follow"' in html)
check("canonical", "canonical" in html and f"{SLUG}.html" in html)
check("title", "Treppenlift-Förderung ohne Pflegegrad" in html)
check("H1", "Diese Wege bestehen wirklich" in html)
check("Quellenstand 2026-11-11", "11.11.2026" in html or "2026-11-11" in html)

# 2. Kernzahlen live
for needle in ["15 bis unter 30 Gesamtpunkten", "Drucksache 21/8869", "Treppensteigen",
               "85 Prozent der jährlichen Bezugsgröße", "60 Prozent",
               "150 Prozent der jährlichen Bezugsgröße", "Einkünfte des Vorvorjahres",
               "vor der Haus- bzw. vor der Wohnungstür", "Bestandsschutz",
               "Gesamtplanverfahren", "Persönliches Budget",
               "Internationalen Klassifikation", "nicht beschlossen",
               "KI-unterstützt", "Tobias Batke"]:
    check(f'live "{needle[:44]}"', needle in html)

# 3. CTA + Partner-Absenz
check("CTA compare_top → treppenlift-zuschuss",
      'href="https://zuhausebleiben-kompass.de/treppenlift-zuschuss.html" data-cta-id="compare_top"' in html)
check("CTA-Label", "Pflegekasse &amp; KfW prüfen" in html or "Pflegekasse & KfW prüfen" in html)
check("kein Partner-Marker", "data-partner-placement" not in html)
check("kein awin Tracker", "awin1.com" not in html)
check("kein rel=sponsored", 'rel="sponsored' not in html)
check("0 × 4.180", "4.180" not in html)
check("0 × 16.720", "16.720" not in html)

# 4. Related-Links
rel_i = html.find("Passend dazu")
rel_block = html[rel_i:html.find("</section>", rel_i)]
rel_links = re.findall(r'href="([^"]+)"', rel_block)
check("related 3 lift-intern", len(rel_links) == 3 and all("treppenlift" in u for u in rel_links), str(rel_links))
check("related zuschuss zuerst", rel_links and "treppenlift-zuschuss" in rel_links[0], str(rel_links))

# 5. SVG
svg_url = f"{BASE}/assets/images/treppenlift-foerderung-ohne-pflegegrad-wegweiser.svg"
_, svg_code = fetch(svg_url)
check("SVG HTTP 200", svg_code == "200", svg_code)
check("SVG referenziert", "treppenlift-foerderung-ohne-pflegegrad-wegweiser.svg" in html)
svg_body, _ = fetch(svg_url)
check("SVG Rechtsstand live", "11.11.2026" in svg_body and "KI-Illustration" in svg_body)

# 6. Sitemap / RSS / Homepage / llms
sm, _ = fetch(f"{BASE}/sitemap.xml")
locs = sm.count("<loc>")
check(f"Sitemap enthält Artikel", SLUG in sm)
check("Sitemap 45 locs", locs == 45, str(locs))
rss, _ = fetch(f"{BASE}/rss.xml")
items = rss.count("<item>")
check(f"RSS 34 items", items == 34, str(items))
check("RSS enthält Artikel", SLUG in rss)
home, home_code = fetch(f"{BASE}/")
check("Homepage 200 index,follow", home_code == "200" and 'index,follow' in home)
check("Homepage listet Artikel", SLUG in home)
llms, _ = fetch(f"{BASE}/llms.txt")
check("llms.txt enthält Artikel", SLUG in llms)

print(f"\n{N} checks, {len(FAIL)} FAILS")
sys.exit(1 if FAIL else 0)
