#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Content-Gate Region Baden-Württemberg (25.11.2026) — gegen LAUNCH-dist.
Prüft: robots/Canonical/Title, alle Kernwordlaute im gebauten HTML (getaggt,
entities-unescape'd, Whitespace normalisiert, case-normalisiert), alle FAQ-Fragen,
alle 16 Quellen-URLs, Related-/CTA-Ziele absolut, Quellenstand, Absenzen
(Weg-1-Beträge 0×, Partner-Marker 0×, U+00AD 0×), Hub 4 Regionen + noindex,
Sitemap exakt 4 Region-URLs ohne Hub/Platzhalter. Exit != 0 bei FAIL."""
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
        print("FAIL", label, detail[:120])


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


def norm(s):
    return clean(s).lower()


page_raw = read("region/baden-wuerttemberg.html")
page = clean(page_raw)
pn = page.lower()
d = json.load(open(os.path.join(ROOT, "data", "region-baden-wuerttemberg.json"), encoding="utf-8"))

# --- Struktur ---
ok("robots index,follow", '<meta name="robots" content="index,follow"' in page_raw)
ok("canonical", 'href="%s/region/baden-wuerttemberg.html"' % BASE in page_raw.replace("&amp;", "&") or 'href="%s/region/baden-wuerttemberg.html"' % BASE in page_raw)
ok("title", "<title>%s — ZuhauseBleiben Kompass</title>" % d["title"] in page_raw)
ok("h1", "<h1>%s</h1>" % d["h1"] in page_raw)
ok("desc meta", 'name="description" content="%s"' % d["description"] in page_raw)
ok("quellenstand", "Quellenstand: 2026-11-25" in page)
ok("geprueft 16x", page.count("geprüft 2026-11-25") == 16, str(page.count("geprüft 2026-11-25")))

# --- Kernwordlaute (Prosa-Schreibweise) ---
NEEDLES = [
    "bis zu 50.000 €",
    "Sollzinssatz: 1,00 %",
    "Sollzinsverbilligung und -bindung: 10 Jahre",
    "Tilgung: 3,00 %",
    "mit 2 tilgungsfreien Anlaufjahren",
    "Bereitstellungsfreie Zeit: 12 Monate",
    "maximal 1.500 €",
    "vollständige Umsetzung der DIN 18040-2",
    "müssen Zugang, Wohn- und Schlafzimmer, Küche und Bad barrierereduziert sein",
    "Überwindung von Treppen und Stufen",
    "Maßnahmen an Sanitärräumen",
    "Einzelmaßnahmen zur Barriere-Reduzierung nach DIN 18040-2",
    "Anpassungsförderung",
    "wenigstens 50 erforderlich",
    "müssen von der Schwerbehinderung herrühren",
    "in Landkreisen: die Wohnraumförderungsstelle im Landratsamt",
    "in Stadtkreisen: die Wohnraumförderungsstelle im Bürgermeisteramt des Bauortes",
    "Förderportal der L-Bank",
    "Die Eigenleistung beträgt mindestens 25 Prozent",
    "mindestens 15 Prozent der Gesamtkosten",
    "71.000 €",
    "§ 10 Abs. 3 LWoFG",
    "mindestens einem Jahr bis zur Bewilligung",
    "Ein vorzeitiger Vorhabenbeginn führt zur Ablehnung der Förderung",
    "grundsätzlich keine Antragsfrist",
    "Diesen Zuschuss können Sie nicht mehr beantragen",
    "wird eine Antragstellung wieder möglich sein",
    "Treppenlifte, Senkrecht-, Hebe- oder Plattformlifte installieren",
    "mit dem Kredit der KfW gefördert werden",
    "44 Stadt- und Landkreise",
    "Aufzug / Treppenlift – Maximale Förderung 2.500 Euro",
    "freiwillige Sozialleistung, auf die kein Rechtsanspruch besteht",
    "Pflegestützpunkte",
    "unabhängig, neutral und kostenlos",
    "Barrierereduzierung, E-Mobilität, Einbruchsschutz und Steckersolargeräte",
    "selbst genutzten Wohnraum",
    "Maßnahmen zur Überwindung von Treppen und Stufen durch Rampen oder Aufzüge/Treppenlifte",
    "Alle Stadt- und Landkreise in Baden-Württemberg haben Pflegestützpunkte",
    "Die Leistungen umfassen Leistungen für die Beschaffung, den Umbau, die Ausstattung und die Erhaltung von Wohnraum",
    "deren Zusage nicht länger als 10 Jahre zurückliegt",
]
for n in NEEDLES:
    ok("needle: " + n[:52], n.lower() in pn)

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
for bad in ["4.180", "16.720", "4 180", "16 720", "awin1.com", 'rel="sponsored"', ">Anzeige<", "\u00ad"]:
    ok("absenz: " + repr(bad[:20]), bad not in page_raw)

# --- Hub ---
hub_raw = read("regional.html")
hub = clean(hub_raw)
ok("hub noindex", 'content="noindex,follow"' in hub_raw)
ok("hub prose bw", "Baden-Württemberg sind als erste Regionen vollständig recherchiert" in hub)
ok("hub card bw", "/region/baden-wuerttemberg.html" in hub_raw)
ok("hub teaser bw", "L-Bank-Darlehen bis 50.000 € mit Tilgungszuschuss bis 1.500 €" in hub)
ok("hub desc", 'Förderlandschaft regional: Nordrhein-Westfalen, Bayern, Sachsen und Baden-Württemberg sind ausgebaut, weitere Regionen folgen.' in hub_raw)

# --- Sitemap ---
sm = read("sitemap.xml")
locs = re.findall(r"<loc>([^<]+)</loc>", sm)
regions = [u for u in locs if "/region/" in u]
ok("sitemap 4 regionen", len(regions) == 4 and all(("/region/%s.html" % s) in u for s in ["nordrhein-westfalen", "bayern", "sachsen", "baden-wuerttemberg"] for u in [next((x for x in regions if s in x), "")] if u), str(regions))
ok("sitemap ohne hub", not any("/regional.html" in u for u in locs))
ok("sitemap ohne platzhalter", not any(h in u for u in regions for h in ["hessen", "niedersachsen", "brandenburg", "thueringen", "rheinland-pfalz", "saarland", "schleswig-holstein", "hamburg", "bremen", "mecklenburg", "berlin"]))
ok("sitemap bw indexierbar", any(u.endswith("/region/baden-wuerttemberg.html") for u in locs))

print("\n=== %d PASS, %d FAIL ===" % (PASSED, FAILED))
sys.exit(1 if FAILED else 0)
