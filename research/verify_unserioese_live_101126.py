#!/usr/bin/env python3
"""Live-Readback Briefing 22 (treppenlift-unserioese-anbieter) auf der öffentlichen URL.
Pollt den neuen Artikel bis 200 (Pages-Deploy-Lag), prüft robots/canonical/Kernzahlen/CTA/
Partner-Abstienz/SVG/Sitemap/RSS/Homepage/llms. Muster: verify_angehoerige_live_101126.py."""
import re
import subprocess
import sys
import time
from html import unescape

BASE = "https://zuhausebleiben-kompass.de"
SLUG = "treppenlift-unserioese-anbieter"
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
check("canonical", f"canonical" in html and f"{SLUG}.html" in html)
check("title", "Unseriöse Treppenlift-Anbieter erkennen" in html)
check("H1", "Warnsignale und Ihre Rechte" in html)
check("Quellenstand 2026-11-10", "10.11.2026" in html or "2026-11-10" in html)

# 2. Kernzahlen live
for needle in ["125 ausgefüllte Umfragebögen", "12 Monate und 14 Tage", "I-13 UKl 17/26",
               "8. Oktober 2026", "18 Vertragsklauseln", "in Höhe von 65 % der Bruttoauftragssumme",
               "in Höhe von 25 % der Bruttoauftragssumme", "Maßanfertigung und Lieferung sofort",
               "geistige und körperliche Beeinträchtigungen, das Alter",
               "ohne dessen vorherige ausdrückliche Einwilligung", "höchste Vorsicht geboten",
               "zahlen Sie erst, wenn der Lift eingebaut und funktionstüchtig ist",
               "An keiner Stelle war erkennbar", "PractiComfort", "10. Dezember 2020",
               "Oberlandesgericht Hamm", "KI-unterstützt"]:
    check(f'live enthält "{needle}"', needle in html)

# 3. CTA + Related
check("CTA compare_top → angebote-vergleichen",
      f'{BASE}/treppenlift-angebote-vergleichen.html" data-cta-id="compare_top"' in html)
check("CTA-Label", "Angebote sauber vergleichen" in html)
rel = html[html.find("Passend dazu"):html.find("</section>", html.find("Passend dazu"))]
rel_links = re.findall(r'href="([^"]+)"', rel)
check("related count 3", len(rel_links) == 3, str(rel_links))
check("related alle lift-cluster", all("treppenlift" in u for u in rel_links), str(rel_links))

# 4. Partner-Abstinenz
check("0 Partner-Marker", "data-partner-placement" not in html)
check("0 awin", "awin1.com" not in html)
check("0 rel=sponsored", 'rel="sponsored' not in html)

# 5. SVG
svg_body, svg_code = fetch(f"{BASE}/assets/images/treppenlift-unserioese-anbieter-warntafel.svg")
check("SVG 200", svg_code == "200", svg_code)
check("SVG KI-Kennzeichnung", "KI-unterstuetzte" in svg_body or "KI-unterstützte" in svg_body)

# 6. Sitemap / RSS / Homepage / llms
sm, sm_code = fetch(f"{BASE}/sitemap.xml")
check("Sitemap 200", sm_code == "200", sm_code)
locs = sm.count("<loc>")
check("Sitemap 44 locs", locs == 44, str(locs))
check("Sitemap enthält Artikel", SLUG in sm)
rss, rss_code = fetch(f"{BASE}/rss.xml")
check("RSS 200", rss_code == "200", rss_code)
check("RSS 33 items", rss.count("<item>") == 33, str(rss.count("<item>")))
home, home_code = fetch(f"{BASE}/")
check("Homepage 200 index,follow", home_code == "200" and "index,follow" in home, home_code)
check("Homepage listet Artikel", SLUG in home)
llms, llms_code = fetch(f"{BASE}/llms.txt")
check("llms.txt 200 + Artikel", llms_code == "200" and SLUG in llms, llms_code)

print(f"\n{N - len(FAIL)}/{N} PASS")
sys.exit(1 if FAIL else 0)
