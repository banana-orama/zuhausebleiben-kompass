#!/usr/bin/env python3
"""Live-Readback zuschuss-refresh 18.11.2026: oeffentliche URL nach dem Deploy pruefen.
Pollt die URL bis der neue Content live ist (Pages-Deploy-Lag), dann alle Assertions."""
import re, subprocess, sys, time

URL = "https://zuhausebleiben-kompass.de/treppenlift-zuschuss.html"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126.0 Safari/537.36"
fails, passes = [], []

def get(url):
    r = subprocess.run(["curl", "-sSL", "--fail", "-A", UA, url], capture_output=True, text=True, timeout=60)
    return r.returncode == 0, r.stdout

# 1. Auf neue Sektion pollen (Deploy-Lag: alter Stand 200, neuer Inhalt folgt spaeter)
h = None
for attempt in range(10):
    ok, h = get(URL)
    if ok and "Förderstatus heute" in h:
        print(f"Neuer Content live nach Poll {attempt + 1}")
        break
    time.sleep(30)
if not h or "Förderstatus heute" not in h:
    print("FAIL: neue Sektion nach 5 min nicht live")
    sys.exit(2)

def need(name, needle, min_count=1):
    n = h.count(needle)
    (passes if n >= min_count else fails).append((name, needle[:80], n))

def absent(name, needle):
    (passes if needle not in h else fails).append((name, needle[:80], h.count(needle)))

need("robots", '<meta name="robots" content="index,follow"')
need("status-heading", "Förderstatus heute: Was ist beantragbar?")
need("status-datum-intro", "am 18. November 2026", 2)
need("tbl-status-header", "Status am 18.11.2026")
need("cell-455b", "Gestoppt — keine neuen Anträge")
need("kfw-verbatim", "Diesen Zuschuss können Sie nicht mehr beantragen")
need("cell-nrw", "zinsgünstige Darlehen bis 220.000 Euro")
need("cell-bayern", "leistungsfreies Baudarlehen bis 10.000 Euro")
need("link-nrw-live", '<a href="https://zuhausebleiben-kompass.de/region/nordrhein-westfalen.html">NRW-Ratgeber ansehen</a>')
need("link-bayern-live", '<a href="https://zuhausebleiben-kompass.de/region/bayern.html">Bayern-Ratgeber ansehen</a>')
need("src-6", 'id="source-6"')
need("src-7", 'id="source-7"')
need("quellenstand", "Quellenstand: 2026-11-18")
need("455-prosa-neu", "wurde am 18. November 2026 direkt abgerufen und geprüft")
absent("stale-datum", "16. November 2026")
absent("partner-placement", "data-partner-placement")
absent("sponsored", 'rel="sponsored"')
absent("awin", "awin1.com")
absent("gesetz-schreibweise", "4 180")

ok_s, sitemap = get("https://zuhausebleiben-kompass.de/sitemap.xml")
locs = sitemap.count("<loc>")
(passes if ok_s and locs == 52 else fails).append(("sitemap-52", locs, ok_s))
ok_z, zuschuss_sitemap = get("https://zuhausebleiben-kompass.de/sitemap.xml")
(passes if "treppenlift-zuschuss.html" in zuschuss_sitemap else fails).append(("zuschuss-in-sitemap", 1, ok_z))
ok_r, rss = get("https://zuhausebleiben-kompass.de/rss.xml")
(passes if ok_r and rss.count("<item>") == 39 else fails).append(("rss-39", rss.count("<item>"), ok_r))
for name, url in [("svg", "https://zuhausebleiben-kompass.de/assets/images/foerderablauf.svg"),
                  ("region-nrw", "https://zuhausebleiben-kompass.de/region/nordrhein-westfalen.html"),
                  ("region-bayern", "https://zuhausebleiben-kompass.de/region/bayern.html")]:
    okx, _ = get(url)
    (passes if okx else fails).append((name + "-200", url, okx))

print(f"LIVE-READBACK: {len(passes)} PASS / {len(fails)} FAIL")
for name, needle, n in fails:
    print(f"FAIL {name}: {needle!r} count={n}")
sys.exit(1 if fails else 0)
