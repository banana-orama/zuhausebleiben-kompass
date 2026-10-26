#!/usr/bin/env python3
"""Live-Readback Briefing 11 (26.10.2026): oeffentliche URL, robots, Struktur, Sitemap, RSS, llms, Homepage."""
import re
import subprocess
import sys

BASE = "https://zuhausebleiben-kompass.de"
SLUG = "treppenlift-schmale-treppe"
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
check("kein ENTWURF-Badge", "ENTWURF" not in html)
check("Quellenstand 2026-10-26", "geprüft 2026-10-26" in html)
check("H1 korrekt", "Treppenlift für schmale Treppen: welche Breite reicht?" in html)
# CTA am Element-Attribut, nicht an CSS-Klassen (Renderer inlined CSS in jede Seite)
check("Early-CTA Attribut + Ziel", re.search(r'data-cta-id="compare_top"[^>]*href="[^"]*treppenlift-firmen-vergleich\.html"', html) is not None
      or re.search(r'href="[^"]*treppenlift-firmen-vergleich\.html"[^>]*data-cta-id="compare_top"', html) is not None)
check("Checklisten-CTA Attribut", 'data-cta-id="checklist_top"' in html)
check("Checklisten-Anker existiert", re.search(r'id="abschnitt-\d+"', html) is not None)
check("5 Quellen gerendert", html.count('id="source-') == 5, str(html.count('id="source-')))
check("SVG eingebunden", f"assets/images/{SLUG}-messplan.svg" in html)
check("related 3x treppenlift", len(re.findall(r'class="related">.*?</section>', html, re.S)) == 1
      and (lambda seg: len(re.findall(r'href="[^"]*treppenlift[a-z-]*\.html"', seg)) == 3)(re.search(r'class="related">.*?</section>', html, re.S).group(0) if re.search(r'class="related">.*?</section>', html, re.S) else ""))

# 2. SVG-Asset live
code2, _ = get(f"{BASE}/assets/images/{SLUG}-messplan.svg")
check("SVG-Asset HTTP 200", code2 == "200", code2)

# 3. Sitemap
code3, sm = get(f"{BASE}/sitemap.xml")
locs = re.findall(r"<loc>([^<]+)</loc>", sm or "")
check("sitemap HTTP 200", code3 == "200", code3)
check("sitemap enthaelt Artikel", any(SLUG in u for u in locs), str(len(locs)))
check("sitemap <loc> >= 45 (44 nach Batch 7 + 1 Artikel)", len(locs) >= 45, str(len(locs)))

# 4. RSS
code4, rss = get(f"{BASE}/rss.xml")
items = re.findall(r"<item>", rss or "")
check("rss HTTP 200", code4 == "200", code4)
check("rss 22 Items", len(items) == 22, str(len(items)))
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
