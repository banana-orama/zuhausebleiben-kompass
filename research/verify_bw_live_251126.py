#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Live-Readback Region BW (25.11.2026) auf der ÖFFENTLICHEN URL.
Pollt bis Deploy sichtbar (Pages-Lag), prüft dann: BW-Region (200, robots,
Canonical, Kernwordlaute, 16 Quellen, FAQs, Related, CTA, Absenzen), Hub
(noindex + BW-Prosa + 4 Region-URLs), Sitemap (exakt 4 Region-URLs), Homepage,
Sachsen-§-554-Refresh live. Exit != 0 bei FAIL."""
import html as html_mod
import re
import sys
import time
import urllib.request

BASE = "https://zuhausebleiben-kompass.de"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"}
PASSED = 0
FAILED = 0


def fetch(path):
    req = urllib.request.Request(BASE + path, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.status, r.read().decode("utf-8", "ignore")


def clean(s):
    s = html_mod.unescape(s)
    s = re.sub(r"<script[\s\S]*?</script>", " ", s, flags=re.I)
    s = re.sub(r"<style[\s\S]*?</style>", " ", s, flags=re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = s.replace("\u00ad", "").replace("\u00a0", " ").replace("\u202f", " ")
    s = re.sub(r"\s+", " ", s)
    return s


def ok(label, cond, detail=""):
    global PASSED, FAILED
    if cond:
        PASSED += 1
        print("PASS", label)
    else:
        FAILED += 1
        print("FAIL", label, str(detail)[:120])


# Deploy-Lag abwarten: BW-URL muss 200 liefern (Pages baut nach CI nach)
status = None
for attempt in range(30):
    try:
        status, raw = fetch("/region/baden-wuerttemberg.html")
        print("poll %d: %d" % (attempt + 1, status))
        if status == 200 and "Umbau-Förderung in Baden-Württemberg" in raw:
            break
    except Exception as e:
        print("poll %d: %s" % (attempt + 1, str(e)[:80]))
    time.sleep(20)
else:
    print("FAIL deploy nicht sichtbar")
    sys.exit(1)

page_raw = raw
page = clean(page_raw)
pn = page.lower()
ok("robots index,follow", '<meta name="robots" content="index,follow"' in page_raw)
ok("canonical", 'href="%s/region/baden-wuerttemberg.html"' % BASE in page_raw)
ok("title", "<title>Umbau-Förderung in Baden-Württemberg — ZuhauseBleiben Kompass</title>" in page_raw)
ok("h1", "<h1>Umbau und Förderung in Baden-Württemberg</h1>" in page_raw)

NEEDLES = [
    "bis zu 50.000 €", "Sollzinssatz: 1,00 %", "mit 2 tilgungsfreien Anlaufjahren",
    "maximal 1.500 €", "vollständige Umsetzung der DIN 18040-2",
    "Überwindung von Treppen und Stufen", "Maßnahmen an Sanitärräumen",
    "Anpassungsförderung", "wenigstens 50 erforderlich",
    "in Landkreisen: die Wohnraumförderungsstelle im Landratsamt",
    "Förderportal der L-Bank", "mindestens 25 Prozent", "mindestens 15 Prozent",
    "71.000 €", "mindestens einem Jahr bis zur Bewilligung",
    "Ein vorzeitiger Vorhabenbeginn führt zur Ablehnung der Förderung",
    "Diesen Zuschuss können Sie nicht mehr beantragen",
    "Treppenlifte, Senkrecht-, Hebe- oder Plattformlifte installieren",
    "44 Stadt- und Landkreise", "Aufzug / Treppenlift – Maximale Förderung 2.500 Euro",
    "freiwillige Sozialleistung, auf die kein Rechtsanspruch besteht",
    "Pflegestützpunkte", "Barrierereduzierung, E-Mobilität, Einbruchsschutz und Steckersolargeräte",
    "selbst genutzten Wohnraum", "deren Zusage nicht länger als 10 Jahre zurückliegt",
    "Quellenstand: 2026-11-25",
]
for n in NEEDLES:
    ok("live: " + n[:52], n.lower() in pn)

ok("16 Quellen live", page.count("geprüft 2026-11-25") == 16, page.count("geprüft 2026-11-25"))
ok("6 FAQs live", page_raw.count("<details") >= 6, page_raw.count("<details"))
for u in ["l-bank.de/produkte/wohnimmobilien/eigentumsfinanzierung-bw-zusatzfinanzierung-barrierefreiheit",
          "service-bw.de/zufi/leistungen/553", "mlw.baden-wuerttemberg.de", "kfw.de/159"]:
    ok("live src: " + u[:44], u in page_raw)
for slug in ["treppenlift-mietwohnung", "wohnumfeldverbesserung-beantragen", "treppenlift-kosten", "treppenlift-zuschuss", "treppenlift-foerderung-ohne-pflegegrad"]:
    ok("live link: " + slug, 'href="%s/%s.html"' % (BASE, slug) in page_raw)
for bad in ["4.180", "16.720", "awin1.com", 'rel="sponsored"', "\u00ad"]:
    ok("live absenz: " + repr(bad[:14]), bad not in page_raw)

# Hub
st, hub_raw = fetch("/regional.html")
hub = clean(hub_raw)
ok("hub 200", st == 200)
ok("hub noindex", 'content="noindex,follow"' in hub_raw)
ok("hub BW-Prosa", "Baden-Württemberg sind als erste Regionen vollständig recherchiert" in hub)
ok("hub BW-Karte", "/region/baden-wuerttemberg.html" in hub_raw)

# Sitemap
st, sm = fetch("/sitemap.xml")
locs = re.findall(r"<loc>([^<]+)</loc>", sm)
regions = [u for u in locs if "/region/" in u]
ok("sitemap 4 regionen", len(regions) == 4, str(regions))
ok("sitemap enthält bw", any(u.endswith("/region/baden-wuerttemberg.html") for u in locs))
ok("sitemap ohne hub", not any("/regional.html" in u for u in locs))
ok("sitemap ohne platzhalter", not any(h in u for u in regions for h in ["hessen", "niedersachsen", "brandenburg", "berlin"]))

# Homepage + Sachsen-§-554-Refresh + llms
st, home = fetch("/")
ok("homepage 200 index,follow", st == 200 and '<meta name="robots" content="index,follow"' in home)
st, sach = fetch("/region/sachsen.html")
sach_c = clean(sach)
ok("sachsen 554-refresh live", "geprüft am 25.11.2026; die Norm nennt seit der Neufassung" in sach_c)
st, llms = fetch("/llms.txt")
ok("llms 200", st == 200 and len(llms) > 500)

print("\n=== %d PASS, %d FAIL ===" % (PASSED, FAILED))
sys.exit(1 if FAILED else 0)
