#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Live-Readback Region Hessen (26.11.2026) auf der ÖFFENTLICHEN URL.
Poll bis Deploy angekommen (GitHub-Pages-Lag), dann: robots/Canonical,
Kernwordlaute, Quellenstand, Hub 5 Regionen, Sitemap exakt 5 Region-URLs,
RSS 41, Homepage, llms, Absenzen live 0×. Exit != 0 bei FAIL."""
import html as html_mod
import re
import sys
import time
import urllib.request

BASE = "https://zuhausebleiben-kompass.de"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
PASSED = 0
FAILED = 0
FAILS = []


def get(url, timeout=60):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def text(url):
    raw = get(url)
    try:
        s = raw.decode("utf-8")
    except UnicodeDecodeError:
        s = raw.decode("latin-1")
    return s


def clean(s):
    s = html_mod.unescape(s)
    s = re.sub(r"<script[\s\S]*?</script>", " ", s, flags=re.I)
    s = re.sub(r"<style[\s\S]*?</style>", " ", s, flags=re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = s.replace("\u00ad", "").replace("\u00a0", " ").replace("\u202f", " ")
    return re.sub(r"\s+", " ", s)


def check(label, cond, detail=""):
    global PASSED, FAILED
    if cond:
        PASSED += 1
        print("PASS", label)
    else:
        FAILED += 1
        FAILS.append("%s %s" % (label, str(detail)[:140]))
        print("FAIL", label, str(detail)[:140])


# --- 1) Poll: neue Region-URL bis 200 ---
url = BASE + "/region/hessen.html"
raw_page = None
for i in range(1, 31):
    try:
        raw_page = text(url)
        print("poll %d: 200" % i)
        break
    except Exception as e:
        print("poll %d: %s" % (i, e))
        time.sleep(20)
if raw_page is None:
    print("FAIL deploy poll: URL blieb unerreichbar")
    sys.exit(1)

page = clean(raw_page)
pn = page.lower()

# --- 2) Struktur live ---
check("robots index,follow", '<meta name="robots" content="index,follow"' in raw_page)
check("canonical", 'href="%s/region/hessen.html"' % BASE in raw_page)
check("title", "<title>Umbau-Förderung in Hessen — ZuhauseBleiben Kompass</title>" in raw_page)
check("h1", "<h1>Umbau und Förderung in Hessen</h1>" in raw_page)

# --- 3) Kernwordlaute live ---
LIVE_NEEDLES = [
    "als nicht rückzahlbarer Zuschuss in Höhe von bis zu 50 Prozent der zuwendungsfähigen Ausgaben",
    "einem Zuschuss in Höhe von maximal 15.000 Euro je Wohneinheit",
    "bis zu 30.000 Euro je Wohneinheit",
    "Lift-/Aufzugseinbau",
    "6.500 Euro (Produktseite)",
    "Um-/Einbau 5.500 Euro (Produktseite)",
    "Einbau von geeigneten Aufzügen (z.B. Treppenschrägaufzug)",
    "Ein Rechtsanspruch auf Gewährung der Förderung besteht nicht.",
    "eine Auswahl nach sozialer Dringlichkeit vorzunehmen",
    "Als Vorhabenbeginn ist grundsätzlich der Abschluss eines der Ausführung zuzurechnenden Lieferungs- und Leistungsvertrages zu werten",
    "werden auf die zuwendungsfähigen Ausgaben angerechnet",
    "Innerhalb von fünf Jahren",
    "eine Einstufung in den Pflegegrad 2 oder höher aufweist",
    "Keine Einkommensgrenze",
    "Für Leistungen nach Abschluss der Schulausbildung ist der Landeswohlfahrtverband Hessen zuständig.",
    "Dies kann z. B. ein behindertengerechter Bad- und/oder Küchenumbau oder der Einbau eines Treppenlifts sein.",
    "Es fallen keine Kosten an.",
    "Dazu gehören zum Beispiel das Einbauen eines Treppenlifts, verbreiterte Türen und Schwellen statt Stufen.",
    "Diesen Zuschuss können Sie nicht mehr beantragen.",
    "Treppenlifte, Senkrecht-, Hebe- oder Plattformlifte installieren",
    "mit dem Kredit der KfW gefördert werden.",
    "In Hessen gibt es 26 Pflegestützpunkte - in jedem Landkreis und in jeder kreisfreien Stadt einen.",
    "nicht zugemutet werden kann",
    "Treppenlift oder Aufzug: bis zu 6.500 Euro",
    "Das Wort Treppenlift kommt auf der Produktseite und in der Richtlinie nicht vor",
    "Quellenstand: 2026-11-26",
    "26 Organisationseinheiten (21 Landkreise und 5 kreisfreie Städte",
]
for n in LIVE_NEEDLES:
    check("live: " + n[:52], n.lower() in pn)
check("geprueft 19x live", page.count("geprüft 2026-11-26") == 19, str(page.count("geprüft 2026-11-26")))

# --- 4) Absenzen live ---
for bad in ["4.180", "16.720", "4 180", "awin1.com", 'rel="sponsored"', ">Anzeige<", "L-Bank", "Friedrichshafen", "\u00ad"]:
    check("live-absenz: " + repr(bad[:16]), bad not in raw_page)

# --- 5) Quellen live (Spot-URLs) ---
for u in ["https://www.wibank.de/wibank/behindertengerechter-umbau-von-wohneigentum",
          "https://www.lwv-hessen.de/leben-wohnen/wohnen/leistungen-fuer-wohnraum.html",
          "https://www.gesetze-im-internet.de/sgb_11/__40.html",
          "https://www.bad-homburg.de/de/stadt/aktuelles/land-hessen-foerdert-den-behindertengerechten-umbau-von-wohneigentum-ov8e4kbakn"]:
    check("live-src: " + u[:60], u in raw_page)

# --- 6) Hub live ---
hub = text(BASE + "/regional.html")
check("hub noindex", 'content="noindex,follow"' in hub)
check("hub prose hessen", "Baden-Württemberg und Hessen sind als erste Regionen vollständig recherchiert" in clean(hub))
check("hub card hessen", "/region/hessen.html" in hub)
check("hub alte-prosa 0x", "Nordrhein-Westfalen, Bayern, Sachsen und Baden-Württemberg sind als erste Regionen" not in clean(hub))

# --- 7) Sitemap live ---
sm = text(BASE + "/sitemap.xml")
locs = re.findall(r"<loc>([^<]+)</loc>", sm)
regions = [u for u in locs if "/region/" in u]
check("sitemap 5 regionen live", len(regions) == 5, str(regions))
check("sitemap hessen live", any(u.endswith("/region/hessen.html") for u in locs))
check("sitemap ohne hub live", not any("/regional.html" in u for u in locs))
check("sitemap ohne platzhalter live", not any(h in u for u in regions for h in ["niedersachsen", "brandenburg", "thueringen", "berlin", "hamburg", "saarland", "rheinland-pfalz", "schleswig-holstein", "bremen", "mecklenburg"]))

# --- 8) RSS / Homepage / llms / robots ---
rss = text(BASE + "/rss.xml")
check("rss 41 items live", rss.count("<item>") == 41, str(rss.count("<item>")))
hp = text(BASE + "/")
check("homepage index,follow", '<meta name="robots" content="index,follow"' in hp)
check("llms 200", "Ratgeber für ältere Menschen" in text(BASE + "/llms.txt"))
check("robots.txt sitemap", "sitemap" in text(BASE + "/robots.txt").lower())

print("\n== LIVE READBACK HESSEN: %d PASS, %d FAIL ==" % (PASSED, FAILED))
if FAILS:
    print("Fails:")
    for f in FAILS:
        print(" -", f)
sys.exit(1 if FAILED else 0)
