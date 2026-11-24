#!/usr/bin/env python3
"""Live-Readback Region Sachsen (24.11.2026) auf der öffentlichen URL.
Poll bis Deploy angekommen (GitHub Pages lag hinter CI), dann alle Checks.
Exit != 0 bei FAIL."""
import html as html_mod
import re
import sys
import time
import urllib.request

BASE = "https://zuhausebleiben-kompass.de"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124.0"}
FAILS = []


def get(url, timeout=60):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def clean(s):
    s = html_mod.unescape(s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = s.replace("\u00ad", "").replace("\u00a0", " ")
    return re.sub(r"\s+", " ", s)


def check(name, cond, detail=""):
    if not cond:
        FAILS.append("%s :: %s" % (name, detail))


# --- Poll bis die neue Region live ist (Deploy-Lag) ---
sachsen = None
for attempt in range(30):
    try:
        sachsen = get(BASE + "/region/sachsen.html")
        if "Umbau und Förderung in Sachsen" in sachsen:
            print("Deploy nach Poll %d angekommen" % (attempt + 1))
            break
    except Exception as e:
        print("poll %d: %s" % (attempt + 1, e))
    time.sleep(15)
else:
    print("FAIL: Seite nach 30 Polls nicht live")
    sys.exit(1)

sx = clean(sachsen)
needles = [
    "Umbau und Förderung in Sachsen",
    "Quellenstand: 2026-11-24",
    "grundsätzlich zu 80 Prozent, maximal mit einem Betrag von 4 000 Euro",
    "maximal mit einem Betrag von 10 000 Euro gefördert",
    "100 % der förderfähigen Ausgaben, max. 5.000 €",
    "max. 12.500 €",
    "mindestens 1 500 Euro",
    "Treppenlifte sind innerhalb der Mietwohnung bzw. eines Einfamilienhauses förderfähig",
    "Die Förderung ist nachrangig gegenüber Leistungen Dritter",
    "Summe der positiven Einkünfte des Haushalts eines Jahres gemäß § 2 Absatz 2 Einkommensteuergesetz",
    "40 000 Euro", "60 000 Euro", "40.000 €", "60.000 €",
    "Bewilligungsstelle ist die Sächsische Aufbaubank",
    "Förderportal Sachsen",
    "Auftragserteilung an eine Fachfirma",
    "4 bis max. 12 Wochen",
    "24.09.2026", "05.11.2026",
    "Antragsteller ist immer die mobilitätseingeschränkte Person selbst",
    "abschließbare Boxen",
    "von der Grundstücksgrenze bis zu einer Hauseingangstür",
    "grundsätzlich von den Landkreisen und den Kreisfreien Städten erbracht",
    "innerhalb von zwei Wochen aktiv eine Pflegeberatung",
    "bereits ausgeschöpft",
    "50.000 Euro je Wohneinheit",
    "die dem Gebrauch durch Menschen mit Behinderungen dienen",
    "Vermieterbestätigung",
    "Förderung ohne Pflegegrad: welche Wege real offen sind",
    "Treppenlift-Kosten: was wirklich zu zahlen ist",
]
for n in needles:
    check("LIVE-NEEDLE %r" % n[:60], n in sx)
check("robots index,follow", 'content="index,follow"' in sachsen, re.search(r'name="robots" content="[^"]+"', sachsen).group(0) if 'name="robots" content="' in sachsen else "missing")
check("canonical", "/region/sachsen.html" in (re.search(r'rel="canonical" href="([^"]+)"', sachsen).group(1) if re.search(r'rel="canonical" href="([^"]+)"', sachsen) else ""))
check("13 Quellen live", sachsen.count("— geprüft 2026-11-24") == 13, str(sachsen.count("— geprüft 2026-11-24")))
check("6 FAQs live", sachsen.count("<details>") == 6)
check("alte 8.000-Kondition 0×", "maximal 8 000 Euro" not in sx and "max. 8.000 €" not in sx)
check("alte 20.000-Kondition 0×", "maximal 20 000 Euro" not in sx and "max. 20.000 €" not in sx)
check("kein Partner-Marker", "rel=\"sponsored\"" not in sachsen and "awin1.com" not in sachsen)

# --- § 554 Fix live auf NRW/Bayern ---
old = "verlangen die Duldung bzw. Zustimmung des Vermieters nach § 554 BGB"
for path in ["/region/nordrhein-westfalen.html", "/region/bayern.html"]:
    t = clean(get(BASE + path))
    check("554-ALT 0× live %s" % path, old not in t)
    check("554-NEU live %s" % path, "die dem Gebrauch durch Menschen mit Behinderungen dienen" in t)

# --- Hub ---
hub = clean(get(BASE + "/regional.html"))
check("Hub 3-Regionen-Prosa", "Nordrhein-Westfalen, Bayern und Sachsen sind als erste Regionen vollständig recherchiert" in hub)
check("Hub-Teaser Sachsen", "Dritte ausführlich recherchierte Region" in hub)
check("Hub noindex", 'content="noindex,follow"' in get(BASE + "/regional.html"))

# --- Sitemap ---
sm = get(BASE + "/sitemap.xml")
locs = re.findall(r"<loc>([^<]+)</loc>", sm)
region_locs = [u for u in locs if "/region/" in u]
check("Sitemap genau 3 Regionen", len(region_locs) == 3, str(region_locs))
check("Sitemap sachsen", any(u.endswith("/region/sachsen.html") for u in locs))
check("Sitemap ohne Hub", not any(u.endswith("/regional.html") for u in locs))

# --- Homepage + robots.txt + RSS zählen ---
home = get(BASE + "/")
check("Homepage 200/index", 'content="index,follow"' in home)
llms = get(BASE + "/llms.txt")
check("llms.txt 200 mit Ratgebern", "treppenlift-zuschuss" in llms)
robots = get(BASE + "/robots.txt")
check("robots.txt Sitemap-Direktive", "sitemap.xml" in robots)
rss = get(BASE + "/rss.xml")
check("RSS 41 unverändert", rss.count("<item>") == 41, str(rss.count("<item>")))

print("LIVE-READBACK SACHSEN 241126 (öffentliche URL)")
for f in FAILS:
    print("FAIL", f)
print("RESULT: %d checks, %d FAIL" % (len(needles) + 17, len(FAILS)))
sys.exit(1 if FAILS else 0)
