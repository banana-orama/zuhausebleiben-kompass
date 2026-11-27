#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Live-Readback Region Mecklenburg-Vorpommern (27.11.2026) auf der ÖFFENTLICHEN URL.
Poll bis Deploy angekommen, dann: robots/Canonical, Kernwordlaute, 13x geprüft,
Hub 7 Regionen, Sitemap exakt 7 Region-URLs, RSS 41, Homepage, llms, Absenzen 0×.
Exit != 0 bei FAIL."""
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


# --- 1) Poll: Region-URL mit MV-typischem Content bis 200 ---
url = BASE + "/region/mecklenburg-vorpommern.html"
raw_page = None
for i in range(1, 31):
    try:
        raw_page = text(url)
        if "Personenaufzüge und Lifte" in html_mod.unescape(re.sub(r"<[^>]+>", " ", raw_page)):
            print("poll %d: 200 + MV-Content live" % i)
            break
        print("poll %d: 200 aber alter Content" % i)
        raw_page = None
    except Exception as e:
        print("poll %d: %s" % (i, e))
    time.sleep(20)
if raw_page is None:
    print("FAIL deploy poll: URL blieb unerreichbar oder ohne MV-Content")
    sys.exit(1)

page = clean(raw_page)
pn = page.lower()

# --- 2) Struktur live ---
check("robots index,follow", '<meta name="robots" content="index,follow"' in raw_page)
check("canonical", 'href="%s/region/mecklenburg-vorpommern.html"' % BASE in raw_page)
check("title", "<title>Förderung in Mecklenburg-Vorpommern — ZuhauseBleiben Kompass</title>" in raw_page)
check("h1", "<h1>Umbau und Förderung in Mecklenburg-Vorpommern</h1>" in raw_page)

# --- 3) Kernwordlaute live ---
LIVE_NEEDLES = [
    "Landesprogramm zur Reduzierung von Barrieren im Wohnungsbestand",
    "Personenaufzüge und Lifte, barrierearmes Wohnen",
    "tritt mit Wirkung vom 01. Januar 2026 in Kraft und am 31. Dezember 2026 außer Kraft",
    "Bewilligungsstelle ist das Landesförderinstitut Mecklenburg-Vorpommern, Geschäftsbereich der NORD/LB Girozentrale",
    "Die Zuwendungen werden im Rahmen der Projektförderung als nichtrückzahlbare Zuschüsse gewährt.",
    "Schriftliche Anträge sind formgebunden vor Vorhabenbeginn, d. h. vor Abschluss jeglicher Lieferungs- und Leistungsverträge im Landesförderinstitut M-V einzureichen.",
    "Planungsleistungen gelten nicht als Beginn.",
    "Ein Rechtsanspruch des Antragstellers auf Gewährung der Zuwendung besteht nicht",
    "müssen mindestens 2 000 Euro je Wohnung betragen",
    "Nachrüstung von Personenaufzügen, Treppenliften oder anderen mechanischen vertikalen Personenfördersystemen",
    "bis zu 4.500 Euro Förderung für Treppenlifte",
    "Antragsberechtigt sind Eigentümer von selbst genutztem Wohnraum und Mieter mit Zustimmung des Vermieters.",
    "B - Mieter, im Einverständnis mit dem Eigentümer/Vermieter für die selbstgenutzte Mietwohnung",
    "Für Maßnahmen, bei denen der Mieter Zuwendungsempfänger ist, gilt Nummer 5.2.2 entsprechend.",
    "Erklärung Eigentümer bei Antragstellung durch Mieter",
    "Zuständig sind die Landkreise und kreisfreien Städte in Mecklenburg-Vorpommern als Sozialhilfeträger",
    "Das Programm zum Abbau von Barrieren im Wohnungsbestand wurde jetzt um 2 Millionen Euro aufgestockt.",
    "um einen Antragsannahmestopp zu vermeiden",
    "Diesen Zuschuss können Sie nicht mehr beantragen.",
    "Sollten im Jahr 2027 erneut Bundesmittel für barrierereduzierende Maßnahmen",
    "Treppenlifte, Senkrecht-, Hebe- oder Plattformlifte installieren",
    "Mit 19 Pflegestützpunkten in Mecklenburg-Vorpommern",
    "kostenfreie und trägerunabhängige Beratung",
    "Barrierereduzierung, E-Mobilität, Einbruchsschutz und Steckersolargeräte",
    "Eine zum Nachteil des Mieters abweichende Vereinbarung ist unwirksam.",
    "198.000 €",
    "33.000 €",
    "Quellenstand: 2026-11-27",
    "geprüft am 27.11.2026",
    "Internet-Archive-Snapshots vom 08./09.11.2026",
]
for n in LIVE_NEEDLES:
    check("live: " + n[:52], n.lower() in pn)
check("geprueft 13x live", page.count("geprüft 2026-11-27") == 13, str(page.count("geprüft 2026-11-27")))
check("faqs 6 live", raw_page.count("<details>") == 6, str(raw_page.count("<details>")))
check("sources 13 live", raw_page.count('class="fine"> — geprüft') == 13, str(raw_page.count('class="fine"> — geprüft')))

# --- 4) Absenzen live ---
for bad in ["4.180", "16.720", "17.500", "12.500", "Niedersachsenbüro", "WIBank", "L-Bank", "Friedrichshafen",
            "awin1.com", 'rel="sponsored"', ">Anzeige<", "\u00ad", "data-partner-placement"]:
    check("live-absenz: " + repr(bad[:16]), bad not in raw_page)

# --- 5) Quellen live (Spot-URLs) ---
for u in ["https://www.lfi-mv.de/foerderfinder/personenaufzuege-und-lifte-barrierearmes-wohnen",
          "https://www.presseportal.de/blaulicht/pm/108531/6257916",
          "https://www.presseportal.de/blaulicht/pm/108531/6331780",
          "https://land-mv.de/sites/default/files/2026-10/2026_Landesplan%20Pflege%20Mecklenburg-Vorpommern_AGP_dip-1.pdf",
          "https://www.pflegestuetzpunktemv.de/",
          "https://www.gesetze-im-internet.de/bgb/__554.html",
          "https://www.kfw.de/159"]:
    check("live-src: " + u[:60], u in raw_page)

# --- 6) Hub live ---
hub = text(BASE + "/regional.html")
hubb = clean(hub)
check("hub noindex", 'content="noindex,follow"' in hub)
check("hub prose 7 regionen", "Niedersachsen und Mecklenburg-Vorpommern sind als erste Regionen vollständig recherchiert" in hubb)
check("hub card mv", "/region/mecklenburg-vorpommern.html" in hub)
check("hub teaser mv", "Siebte ausführlich recherchierte Region" in hubb)
check("hub alte-prosa 0x", "Hessen und Niedersachsen sind als erste Regionen" not in hubb)

# --- 7) Sitemap live ---
sm = text(BASE + "/sitemap.xml")
locs = re.findall(r"<loc>([^<]+)</loc>", sm)
regions = [u for u in locs if "/region/" in u]
check("sitemap 7 regionen live", len(regions) == 7, str(regions))
check("sitemap mv live", any(u.endswith("/region/mecklenburg-vorpommern.html") for u in locs))
check("sitemap ohne hub live", not any("/regional.html" in u for u in locs))
check("sitemap ohne platzhalter live", not any(h in u for u in regions for h in ["berlin", "hamburg", "rheinland-pfalz", "schleswig-holstein", "thueringen", "brandenburg", "bremen", "saarland"]))

# --- 8) RSS / Homepage / llms / robots ---
rss = text(BASE + "/rss.xml")
check("rss 41 items live", rss.count("<item>") == 41, str(rss.count("<item>")))
hp = text(BASE + "/")
check("homepage index,follow", '<meta name="robots" content="index,follow"' in hp)
check("llms 200", "Ratgeber für ältere Menschen" in text(BASE + "/llms.txt"))
check("robots.txt sitemap", "sitemap" in text(BASE + "/robots.txt").lower())

print("\n== LIVE READBACK MV: %d PASS, %d FAIL ==" % (PASSED, FAILED))
if FAILS:
    print("Fails:")
    for f in FAILS:
        print(" -", f)
sys.exit(1 if FAILED else 0)
