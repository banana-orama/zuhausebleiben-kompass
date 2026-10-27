#!/usr/bin/env python3
"""Live-Readback Briefing 12 (27.10.2026): oeffentliche URL, robots, Struktur, Sitemap, RSS, llms, Homepage."""
import re
import subprocess
import sys

BASE = "https://zuhausebleiben-kompass.de"
SLUG = "treppenlift-maximalgewicht"
FAIL = []


def get(url):
    r = subprocess.run(["curl", "-sL", "--max-time", "40", "-w", "\n%{http_code}", url],
                       capture_output=True, text=True)
    body, _, code = r.stdout.rpartition("\n")
    return code.strip(), body


def check(label, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + label + ("" if cond else f"  {detail}"))
    if not cond:
        FAIL.append(label)


# 1. Artikel-URL
code, html = get(f"{BASE}/{SLUG}.html")
check("artikel HTTP 200", code == "200", code)
robots = re.search(r'<meta name="robots" content="([^"]+)"', html or "")
check("robots index,follow", bool(robots) and robots.group(1) == "index,follow", robots.group(1) if robots else "missing")
check("Quellenstand 2026-10-27", "geprüft 2026-10-27" in html)
check("H1 korrekt", "Treppenlift Maximalgewicht: welche Tragkraft trägt Sie sicher?" in html)
# CTA am Element-Attribut, nicht an CSS-Klassen (Renderer inlined CSS in jede Seite)
check("Early-CTA Attribut + Ziel", re.search(r'data-cta-id="compare_top"[^>]*href="[^"]*treppenlift-angebote-vergleichen\.html"', html) is not None
      or re.search(r'href="[^"]*treppenlift-angebote-vergleichen\.html"[^>]*data-cta-id="compare_top"', html) is not None)
check("Checklisten-CTA Attribut", 'data-cta-id="checklist_top"' in html)
check("Checklisten-Anker existiert", re.search(r'id="abschnitt-\d+"', html) is not None)
check("9 Quellen gerendert", html.count('id="source-') == 9, str(html.count('id="source-')))
check("SVG eingebunden", "assets/images/treppenlift-maximalgewicht-tragkraft.svg" in html)
segm = re.search(r'class="related">.*?</section>', html, re.S)
seg = segm.group(0) if segm else ""
check("related 3x treppenlift", len(re.findall(r'href="[^"]*treppenlift[a-z-]*\.html"', seg)) == 3)

# Kernzahlen im Live-HTML
for n in ["125 kg", "135 kg", "175 kg", "200 kg"]:
    check(f"Kernzahl {n} live", n in html)

# 2. SVG-Asset live
code2, _ = get(f"{BASE}/assets/images/treppenlift-maximalgewicht-tragkraft.svg")
check("SVG-Asset HTTP 200", code2 == "200", code2)

# 3. Sitemap
code3, sm = get(f"{BASE}/sitemap.xml")
locs = re.findall(r"<loc>([^<]+)</loc>", sm or "")
check("sitemap HTTP 200", code3 == "200", code3)
check("sitemap enthaelt Artikel", any(SLUG in u for u in locs), str(len(locs)))
check("sitemap <loc> >= 46 (45 nach Batch 8 + 1 Artikel)", len(locs) >= 46, str(len(locs)))

# 4. RSS
code4, rss = get(f"{BASE}/rss.xml")
items = re.findall(r"<item>", rss or "")
check("rss HTTP 200", code4 == "200", code4)
check("rss 23 Items", len(items) == 23, str(len(items)))
check("rss enthaelt Artikel", SLUG in (rss or ""))

# 5. llms.txt
code5, llms = get(f"{BASE}/llms.txt")
check("llms HTTP 200", code5 == "200", code5)
check("llms enthaelt Artikel", SLUG in (llms or ""))

# 6. Homepage listet neuen Ratgeber
code6, home = get(BASE + "/")
check("homepage HTTP 200", code6 == "200", code6)
check("homepage robots index,follow", 'content="index,follow"' in (home or ""))
check("homepage listet Ratgeber", SLUG in (home or ""))

print()
if FAIL:
    print(f"ERGEBNIS: {len(FAIL)} FAIL: {FAIL}")
    sys.exit(1)
print("ERGEBNIS: ALL PASS")
