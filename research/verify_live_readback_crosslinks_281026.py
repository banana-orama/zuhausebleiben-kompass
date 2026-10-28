#!/usr/bin/env python3
"""Live-Readback 28.10. (Abend): Cross-Related-Links auf der öffentlichen URL verifizieren."""
import json, pathlib, re, sys, urllib.request

BASE = "https://zuhausebleiben-kompass.de/"
CL = json.loads(pathlib.Path("data/cross-links.json").read_text(encoding="utf-8"))
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}

results = []


def fetch(path):
    req = urllib.request.Request(BASE + path, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, r.read().decode("utf-8", errors="replace")


def check(name, ok, detail=""):
    results.append((name, ok, detail))


# 1) Homepage + robots
code, html = fetch("")
check("homepage 200", code == 200, f"HTTP {code}")
check("homepage index,follow", 'name="robots" content="index,follow"' in html or "index,follow" in html)
code, robots = fetch("robots.txt")
check("robots.txt 200 + Sitemap-Direktive", code == 200 and "Sitemap:" in robots, f"HTTP {code}")

# 2) Alle betroffenen Artikel: HTTP 200 + Cross-Ziel an Position 1 + genau 3 Related-Links
for src, targets in CL["links"].items():
    try:
        code, html = fetch(f"{src}.html")
    except Exception as e:
        check(f"{src} fetch", False, str(e))
        continue
    check(f"{src} 200", code == 200, f"HTTP {code}")
    if 'class="related"' not in html:
        check(f"{src} related section", False, "fehlt")
        continue
    i = html.index('class="related">')
    j = html.index("</section>", i)
    rel = re.findall(r'href="(?:https://zuhausebleiben-kompass\.de/)?([a-z0-9-]+)\.html"', html[i:j])
    check(f"{src} exactly 3 related", len(rel) == 3, str(rel))
    check(f"{src} cross-target first = {targets[0]}", bool(rel) and rel[0] == targets[0], str(rel))
    if len(targets) > 1:
        check(f"{src} second cross-target = {targets[1]}", len(rel) > 1 and rel[1] == targets[1], str(rel))

# 3) Ein unveränderter Lift-Artikel als Regressionsprobe
code, html = fetch("treppenlift-schmale-treppe.html")
i = html.index('class="related">')
j = html.index("</section>", i)
rel = re.findall(r'href="(?:https://zuhausebleiben-kompass\.de/)?([a-z0-9-]+)\.html"', html[i:j])
check("schmale-treppe unchanged (3 lift-related)", len(rel) == 3 and all(s.startswith("treppenlift") for s in rel), str(rel))

# 4) Kein Partner-CTA-Marker durch diese Änderung (Inaktivität bleibt)
code, html = fetch("hausnotruf-kosten-anbieter-vergleich.html")
check("kein Partner-Marker (data-partner-placement)", "data-partner-placement" not in html)

fails = [r for r in results if not r[1]]
print(f"Live-Readback: {len(results) - len(fails)}/{len(results)} PASS")
for name, ok, detail in results:
    if not ok:
        print("FAIL:", name, detail)
if fails:
    sys.exit(1)
print("ALL PASS auf öffentlicher URL")
