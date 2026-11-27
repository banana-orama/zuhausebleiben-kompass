#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Live-Readback Region Niedersachsen (27.11.2026) auf der ÖFFENTLICHEN URL.
Poll bis Deploy angekommen (GitHub-Pages-Lag), dann: robots/Canonical,
Kernwordlaute, Quellenstand, Hub 6 Regionen, Sitemap exakt 6 Region-URLs,
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
url = BASE + "/region/niedersachsen.html"
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
check("canonical", 'href="%s/region/niedersachsen.html"' % BASE in raw_page)
check("title", "<title>Umbau-Förderung in Niedersachsen — ZuhauseBleiben Kompass</title>" in raw_page)
check("h1", "<h1>Umbau und Förderung in Niedersachsen</h1>" in raw_page)

# --- 3) Kernwordlaute live ---
LIVE_NEEDLES = [
    "Barrierereduzierende Modernisierung von selbstgenutztem Wohneigentum",
    "als ein anfänglich zinsloses, rückzahlbares Darlehen und als ein nicht rückzahlbarer Zuschuss in Form einer Anteilsfinanzierung zur Projektförderung gewährt",
    "Barrierereduzierende Modernisierung eines bestehenden Gebäudes mit Gesamtkosten von bis zu 15.000 Euro",
    "Einkommensgruppe A: bis zu 40 % der Gesamtkosten, max. 6.000 Euro",
    "Einkommensgruppen B+C: bis zu 30 % der Gesamtkosten, max. 4.500 Euro",
    "ist die Gewährung des Zuschusses an die Inanspruchnahme des Darlehens gebunden",
    "für die Dauer von 15 Jahren zu einem Zinssatz von 0 %",
    "bis zu 35 Prozent vor (maximal 17.500 Euro)",
    "Den Antrag auf barrierereduzierende und/oder klimagerechte Modernisierung selbstgenutzten Wohneigentums stellen Sie bitte bei der für Ihren Bauort zuständigen Wohnraumförderstelle (Landkreis, Stadt, Gemeinde).",
    "Ein Anspruch auf Gewährung einer Zuwendung besteht nicht, vielmehr entscheidet die Bewilligungsbehörde aufgrund ihres pflichtgemäßen Ermessens im Rahmen der verfügbaren Haushaltsmittel",
    "Derzeit verzeichnen wir ein besonders hohes Antragsaufkommen. Dadurch kann sich die Bearbeitung Ihres Antrags leider etwas verzögern.",
    "Bei Maßnahmen mit im Antrag zugrunde gelegten zuwendungsfähigen Ausgaben von weniger als 100 000 EUR ist der Vorhabenbeginn ab Antragstellung zugelassen.",
    "Durch die baulichen Maßnahmen muss eine Verringerung bestehender Barrieren erreicht werden",
    "Freibetrag von 4.000 Euro",
    "21.250 Euro für einen Einpersonenhaushalt und 28.750 Euro für zwei Personen",
    "Die Eigenmittel müssen 10 %, bei Haushalten mit 2 oder mehr Kindern sowie mit Menschen mit Behinderungen 7,5 %, der Gesamtkosten (z. B. Bargeld, Guthaben, Sach- und Arbeitsleistungen) betragen.",
    "in Höhe von 5.000 Euro für jede barrierefrei nutzbare Wohnung gemäß DIN 18040-2",
    "Das Wort Treppenlift kommt weder auf der NBank-Produktseite",
    "auch der Badumbau und Treppenlift, aber nicht der alleinige Treppenlift",
    "FORUM Gemeinschaftliches Wohnen e.V. und BAG Wohnungsanpassung e.V.",
    "Zuständig für die Leistungen der Eingliederungshilfe sind in Niedersachsen die Kommunen, das heißt die Landkreise, die kreisfreien Städte, die Region Hannover, die Städte Hannover, Göttingen, Hildesheim, Lingen (Ems) und Lüneburg.",
    "erst beginnend mit dem Monat der Antragstellung",
    "Bei den Leistungen der Eingliederungshilfe müssen Sie grundsätzlich einen Beitrag aus Ihrem Einkommen sowie aus Ihrem Vermögen, sofern es eine festgesetzte Grenze überschreitet, zahlen.",
    "Die Leistungen umfassen Leistungen für die Beschaffung, den Umbau, die Ausstattung und die Erhaltung von Wohnraum",
    "Diesen Zuschuss können Sie nicht mehr beantragen.",
    "Sollten im Jahr 2027 erneut Bundesmittel für barrierereduzierende Maßnahmen",
    "Treppenlifte, Senkrecht-, Hebe- oder Plattformlifte installieren",
    "Daher fördert das Land die Einrichtung und den Betrieb eines Senioren- und Pflegestützpunktes Niedersachsen oder eines Seniorenstützpunktes Niedersachsen in jedem Landkreis und jeder kreisfreien Stadt sowie in der Region Hannover, der Landeshauptstadt Hannover und der Stadt Göttingen.",
    "nicht zugemutet werden kann",
    "Mit den wohnumfeldverbessernden Maßnahmen gewährt Ihnen die Pflegekasse einen Zuschuss zu baulichen Maßnahmen wie z.B. Türverbreiterungen, Badumbau oder fest installierte Rampen und Treppenlifte.",
    "Quellenstand: 2026-11-27",
    "je 0 Treffer, geprüft am 27.11.2026",
    "für die Bewilligung nicht bindend",
]
for n in LIVE_NEEDLES:
    check("live: " + n[:52], n.lower() in pn)
check("geprueft 21x live", page.count("geprüft 2026-11-27") == 21, str(page.count("geprüft 2026-11-27")))

# --- 4) Absenzen live ---
for bad in ["4.180", "16.720", "4 180", "awin1.com", 'rel="sponsored"', ">Anzeige<", "L-Bank", "Friedrichshafen", "WIBank", "\u00ad"]:
    check("live-absenz: " + repr(bad[:16]), bad not in raw_page)

# --- 5) Quellen live (Spot-URLs) ---
for u in ["https://www.nbank.de/F%C3%B6rderprogramme/Aktuelle-F%C3%B6rderprogramme/Eigentumsf%C3%B6rderung-(Selbst-genutztes-Wohneigentum).html",
          "https://www.nbank.de/medien/nb-media/Downloads/Rechtliche-Grundlagen/Richtlinien/Richtlinie-F%C3%B6rderung-von-selbst-genutztem-Wohneigentum-(RL-Wohneigentum-2026).pdf",
          "https://soziales.niedersachsen.de/startseite/menschen_mit_behinderungen/eingliederungshilfe/wie_erhalte_ich_leistungen/-200447.html",
          "https://service.niedersachsen.de/detail?pstId=8664328",
          "https://neues-wohnen-nds.de/wohnberatung/fachinformationen/foerdermoeglichkeiten/",
          "https://www.gesetze-im-internet.de/bgb/__554.html"]:
    check("live-src: " + u[:60], u in raw_page)

# --- 6) Hub live ---
hub = text(BASE + "/regional.html")
check("hub noindex", 'content="noindex,follow"' in hub)
check("hub prose nds", "Hessen und Niedersachsen sind als erste Regionen vollständig recherchiert" in clean(hub))
check("hub card nds", "/region/niedersachsen.html" in hub)
check("hub teaser nds", "Sechste ausführlich recherchierte Region" in clean(hub))
check("hub alte-prosa 0x", "Baden-Württemberg und Hessen sind als erste Regionen" not in clean(hub))

# --- 7) Sitemap live ---
sm = text(BASE + "/sitemap.xml")
locs = re.findall(r"<loc>([^<]+)</loc>", sm)
regions = [u for u in locs if "/region/" in u]
check("sitemap 6 regionen live", len(regions) == 6, str(regions))
check("sitemap nds live", any(u.endswith("/region/niedersachsen.html") for u in locs))
check("sitemap ohne hub live", not any("/regional.html" in u for u in locs))
check("sitemap ohne platzhalter live", not any(h in u for u in regions for h in ["berlin", "brandenburg", "thueringen", "rheinland-pfalz", "saarland", "schleswig-holstein", "hamburg", "bremen", "mecklenburg"]))

# --- 8) RSS / Homepage / llms / robots ---
rss = text(BASE + "/rss.xml")
check("rss 41 items live", rss.count("<item>") == 41, str(rss.count("<item>")))
hp = text(BASE + "/")
check("homepage index,follow", '<meta name="robots" content="index,follow"' in hp)
check("llms 200", "Ratgeber für ältere Menschen" in text(BASE + "/llms.txt"))
check("robots.txt sitemap", "sitemap" in text(BASE + "/robots.txt").lower())

print("\n== LIVE READBACK NDS: %d PASS, %d FAIL ==" % (PASSED, FAILED))
if FAILS:
    print("Fails:")
    for f in FAILS:
        print(" -", f)
sys.exit(1 if FAILED else 0)
