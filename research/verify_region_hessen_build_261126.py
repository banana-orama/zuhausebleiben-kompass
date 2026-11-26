#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Content-Gate Region Hessen (26.11.2026) — gegen LAUNCH-dist.
Prüft: robots/Canonical/Title, alle Kernwordlaute im gebauten HTML (getaggt,
entities-unescape'd, Whitespace normalisiert, case-normalisiert), alle FAQ-Fragen,
alle 19 Quellen-URLs, Related-/CTA-Ziele absolut, Quellenstand, Absenzen
(Pflegekassen-Beträge 0×, Partner-Marker 0×, U+00AD 0×, alte Hub-Prosa 0×),
Hub 5 Regionen + noindex, Sitemap exakt 5 Region-URLs ohne Hub/Platzhalter.
Exit != 0 bei FAIL."""
import html as html_mod
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")
BASE = "https://zuhausebleiben-kompass.de"

PASSED = 0
FAILED = 0


def ok(label, cond, detail=""):
    global PASSED, FAILED
    if cond:
        PASSED += 1
        print("PASS", label)
    else:
        FAILED += 1
        print("FAIL", label, str(detail)[:120])


def read(path):
    with open(os.path.join(DIST, path), encoding="utf-8") as f:
        return f.read()


def clean(s):
    s = html_mod.unescape(s)
    s = re.sub(r"<script[\s\S]*?</script>", " ", s, flags=re.I)
    s = re.sub(r"<style[\s\S]*?</style>", " ", s, flags=re.I)
    s = re.sub(r"<sup[^>]*>.*?</sup>", " ", s, flags=re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = s.replace("\u00ad", "").replace("\u00a0", " ").replace("\u202f", " ")
    s = re.sub(r"\s+", " ", s)
    return s


page_raw = read("region/hessen.html")
page = clean(page_raw)
pn = page.lower()
d = json.load(open(os.path.join(ROOT, "data", "region-hessen.json"), encoding="utf-8"))

# --- Struktur ---
ok("robots index,follow", '<meta name="robots" content="index,follow"' in page_raw)
ok("canonical", 'href="%s/region/hessen.html"' % BASE in page_raw.replace("&amp;", "&"))
ok("title", "<title>%s — ZuhauseBleiben Kompass</title>" % d["title"] in page_raw)
ok("h1", "<h1>%s</h1>" % d["h1"] in page_raw)
ok("desc meta", 'name="description" content="%s"' % d["description"] in page_raw)
ok("quellenstand", "Quellenstand: 2026-11-26" in page)
ok("geprueft 19x", page.count("geprüft 2026-11-26") == 19, str(page.count("geprüft 2026-11-26")))

# --- Kernwordlaute (Prosa-Schreibweise) ---
NEEDLES = [
    "als nicht rückzahlbarer Zuschuss in Höhe von bis zu 50 Prozent der zuwendungsfähigen Ausgaben",
    "bis zu 30.000 Euro je Wohneinheit",
    "einem Zuschuss in Höhe von maximal 15.000 Euro je Wohneinheit",
    "Lift-/Aufzugseinbau",
    "6.500 Euro (Produktseite)",
    "Um-/Einbau 5.500 Euro (Produktseite)",
    "je 3.000 Euro (Produktseite)",
    "Maßnahmen unter 1.500 Euro werden nicht gefördert (Richtlinie)",
    "1 % des bewilligten Zuschusses, mindestens jedoch 25 Euro",
    "Einbau von geeigneten Aufzügen (z.B. Treppenschrägaufzug)",
    "Plattformlift",
    "Austausch der Badewanne gegen eine Dusche",
    "DIN 18040 Teil 2",
    "bei der Wohnungsbauförderstelle des Kreises oder der kreisfreien Stadt",
    "Ein Rechtsanspruch auf Gewährung der Förderung besteht nicht.",
    "eine Auswahl nach sozialer Dringlichkeit vorzunehmen",
    "4,0 Mio. Euro für den behindertengerechten Umbau",
    "Als Vorhabenbeginn ist grundsätzlich der Abschluss eines der Ausführung zuzurechnenden Lieferungs- und Leistungsvertrages zu werten",
    "werden auf die zuwendungsfähigen Ausgaben angerechnet",
    "Innerhalb von fünf Jahren",
    "pro Wohnung bzw. Antragstellerin oder Antragsteller",
    "eine Einstufung in den Pflegegrad 2 oder höher aufweist",
    "Grad der Behinderung von 50 Prozent oder mehr",
    "Schwerbehindertenausweis",
    "Pflegegradnachweis",
    "Zuschuss bis max. 15.000 Euro für selbstgenutzten Wohnraum",
    "Für Leistungen nach Abschluss der Schulausbildung ist der Landeswohlfahrtverband Hessen zuständig.",
    "26 Organisationseinheiten (21 Landkreise und 5 kreisfreie Städte",
    "Dies kann z. B. ein behindertengerechter Bad- und/oder Küchenumbau oder der Einbau eines Treppenlifts sein.",
    "Bevor Leistungen der Eingliederungshilfe bewilligt werden können, ist vorrangig zu klären",
    "Es fallen keine Kosten an.",
    "ggf. finanziell beteiligen",
    "innerhalb von 3 Wochen nach Antragseingang",
    "mit Gutachten innerhalb von 2 Wochen",
    "Dazu gehören zum Beispiel das Einbauen eines Treppenlifts, verbreiterte Türen und Schwellen statt Stufen.",
    "Diesen Zuschuss können Sie nicht mehr beantragen.",
    "Sollten im Jahr 2027 erneut Bundesmittel für barrierereduzierende Maßnahmen",
    "Treppenlifte, Senkrecht-, Hebe- oder Plattformlifte installieren",
    "mit dem Kredit der KfW gefördert werden.",
    "bis zu 50.000 Euro je Wohneinheit",
    "In Hessen gibt es 26 Pflegestützpunkte - in jedem Landkreis und in jeder kreisfreien Stadt einen.",
    "Barrierereduzierung, E-Mobilität, Einbruchsschutz und Steckersolargeräte",
    "nicht zugemutet werden kann",
    "die dem Gebrauch durch Menschen mit Behinderungen",
    "Die Leistungen umfassen Leistungen für die Beschaffung, den Umbau, die Ausstattung und die Erhaltung von Wohnraum",
    "Treppenlift oder Aufzug: bis zu 6.500 Euro",
    "Keine Einkommensgrenze",
    "Magistrat der kreisfreien Stadt",
    "Kreisausschuss des Landkreises",
    "Zuwendungsbescheid",
    "in einer Summe nach Abschluss der Maßnahmen",
]
for n in NEEDLES:
    ok("needle: " + n[:52], n.lower() in pn)

# --- Treppenlift-Nennungslogik (Wortlaut-Ehrlichkeit): das Wort "Treppenlift"
# erscheint als Eigentitel des Portals und in CTA-/Ratgeber-Kontexten, aber NICHT
# als angebliches Landesprogramm-Zitat — explizite Kennzeichnung muss vorhanden sein.
ok("wortlaut-hinweis treppenlift-0x", "Das Wort Treppenlift kommt auf der Produktseite und in der Richtlinie nicht vor" in page)

# --- FAQs ---
for f in d["faqs"]:
    ok("faq: " + f["q"][:48], f["q"].lower() in pn)

# --- Quellen-URLs ---
for s in d["sources"]:
    ok("src: " + s["url"][:56], s["url"] in page_raw)

# --- Related + CTA absolut ---
for r in d["related"]:
    ok("related: " + r["slug"], 'href="%s/%s.html"' % (BASE, r["slug"]) in page_raw)
ok("ctaEarly", 'href="%s/%s.html"' % (BASE, d["ctaEarly"]["slug"]) in page_raw)
ok("cta wohnumfeld", 'href="%s/wohnumfeldverbesserung-beantragen.html"' % BASE in page_raw)
ok("cta ohne-pflegegrad", 'href="%s/treppenlift-foerderung-ohne-pflegegrad.html"' % BASE in page_raw)

# --- Absenzen ---
for bad in ["4.180", "16.720", "4 180", "16 720", "awin1.com", 'rel="sponsored"', ">Anzeige<", "\u00ad", "L-Bank", "Friedrichshafen"]:
    ok("absenz: " + repr(bad[:20]), bad not in page_raw)

# --- Hub ---
hub_raw = read("regional.html")
hub = clean(hub_raw)
ok("hub noindex", 'content="noindex,follow"' in hub_raw)
ok("hub prose hessen", "Baden-Württemberg und Hessen sind als erste Regionen vollständig recherchiert" in hub)
ok("hub card hessen", "/region/hessen.html" in hub_raw)
ok("hub teaser hessen", "Landes-Zuschuss über die WIBank" in hub)
ok("hub desc 5 regionen", "Nordrhein-Westfalen, Bayern, Sachsen, Baden-Württemberg und Hessen sind ausgebaut, weitere Regionen folgen." in hub_raw)
ok("hub alte 4-regionen-prosa 0x", "Nordrhein-Westfalen, Bayern, Sachsen und Baden-Württemberg sind als erste Regionen" not in hub)

# --- Sitemap ---
sm = read("sitemap.xml")
locs = re.findall(r"<loc>([^<]+)</loc>", sm)
regions = [u for u in locs if "/region/" in u]
ok("sitemap 5 regionen", len(regions) == 5, str(regions))
ok("sitemap hessen drin", any(u.endswith("/region/hessen.html") for u in locs))
ok("sitemap ohne hub", not any("/regional.html" in u for u in locs))
ok("sitemap ohne platzhalter", not any(h in u for u in regions for h in ["niedersachsen", "brandenburg", "thueringen", "rheinland-pfalz", "saarland", "schleswig-holstein", "hamburg", "bremen", "mecklenburg", "berlin"]))

# --- RSS unverändert (keine Artikel-Änderung) ---
rss = read("rss.xml")
ok("rss item count 41", rss.count("<item>") == 41, str(rss.count("<item>")))

print("\n=== %d PASS, %d FAIL ===" % (PASSED, FAILED))
sys.exit(1 if FAILED else 0)
