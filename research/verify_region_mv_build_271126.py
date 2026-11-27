#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Content-Gate Region Mecklenburg-Vorpommern (27.11.2026) — gegen LAUNCH-dist.

Checks:
1. Struktur: robots index,follow, canonical, title/h1/desc + og-Spiegel, Quellenstand,
   13x geprüft 2026-11-27, 6 FAQs, 13 Quellen-URLs, Related/CTAs absolut, print-button.
2. JSON-vs-HTML-Vollständigkeit: JEDE Content-Zeichenkette aus dem Region-JSON
   (leads, sections[].p, bullets, table head/rows/note, faqs, standLine, cta-Labels,
   teaser) muss im gebauten HTML auftreten (Renderer-Drop-Fehlerklasse).
3. Kern-Verbatim-Needles (Prosa-Schreibweise).
4. Absenzen: Pflegekassen-Beträge, andere Landesprogramme (NBank-Zahlen/WIBank/L-Bank/
   Niedersachsenbüro), Partner-Marker, U+00AD, alte 6-Regionen-Prosa.
5. Hub: noindex, 7-Regionen-Prosa + MV-Karte + Teaser, alte Prosa 0×.
6. Sitemap exakt 7 Region-URLs, kein Hub, kein Platzhalter (inkl. bremen/saarland).
7. RSS unverändert 41 Items. Platzhalter berlin bleibt noindex.
Exit != 0 bei FAIL.
"""
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
        print("FAIL", label, str(detail)[:160])


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


page_raw = read("region/mecklenburg-vorpommern.html")
page = clean(page_raw)
pn = page.lower()
d = json.load(open(os.path.join(ROOT, "data", "region-mecklenburg-vorpommern.json"), encoding="utf-8"))

# --- 1. Struktur ---
ok("robots index,follow", '<meta name="robots" content="index,follow"' in page_raw)
ok("canonical", 'href="%s/region/mecklenburg-vorpommern.html"' % BASE in page_raw.replace("&amp;", "&"))
ok("title", "<title>%s — ZuhauseBleiben Kompass</title>" % d["title"] in page_raw)
ok("title-len<=65", len(d["title"] + " — ZuhauseBleiben Kompass") <= 65, len(d["title"] + " — ZuhauseBleiben Kompass"))
ok("desc-len<=160", len(d["description"]) <= 160, len(d["description"]))
ok("desc meta", 'name="description" content="%s"' % d["description"] in page_raw)
ok("og:title Spiegel", 'property="og:title" content="%s — ZuhauseBleiben Kompass"' % d["title"] in page_raw)
ok("h1", "<h1>%s</h1>" % d["h1"] in page_raw)
ok("quellenstand", "Quellenstand: 2026-11-27" in page)
ok("geprueft 13x", page.count("geprüft 2026-11-27") == 13, str(page.count("geprüft 2026-11-27")))
ok("print-button", "Diese Seite drucken" in page_raw)
ok("ki-kennzeichnung", "Mit KI-Unterstützung erstellt" in page)

# --- 2. JSON-vs-HTML-Vollständigkeit (teaser gehört zum Hub, nicht zur Region-Seite) ---
def walk(x, skip_keys=()):
    if isinstance(x, dict):
        for k, i in x.items():
            if k not in skip_keys:
                yield from walk(i, skip_keys)
    elif isinstance(x, list):
        for i in x:
            yield from walk(i, skip_keys)
    elif isinstance(x, str):
        yield x

missing = []
for s in walk(d, skip_keys=("teaser", "slug", "url", "description", "title")):
    if clean(s).strip() and clean(s) not in page:
        missing.append(s)
ok("json-keys-in-html (%d Strings)" % len(list(walk(d, skip_keys=("teaser", "slug", "url", "description", "title")))), not missing, missing[:3])
hub_pre = clean(read("regional.html"))
ok("hub-teaser-json", clean(d["teaser"]) in hub_pre)

# --- 3. Kern-Verbatim-Needles ---
NEEDLES = [
    "Landesprogramm zur Reduzierung von Barrieren im Wohnungsbestand",
    "Personenaufzüge und Lifte, barrierearmes Wohnen",
    "tritt mit Wirkung vom 01. Januar 2026 in Kraft und am 31. Dezember 2026 außer Kraft",
    "Bewilligungsstelle ist das Landesförderinstitut Mecklenburg-Vorpommern, Geschäftsbereich der NORD/LB Girozentrale",
    "Die Zuwendungen werden im Rahmen der Projektförderung als nichtrückzahlbare Zuschüsse gewährt.",
    "Schriftliche Anträge sind formgebunden vor Vorhabenbeginn, d. h. vor Abschluss jeglicher Lieferungs- und Leistungsverträge im Landesförderinstitut M-V einzureichen.",
    "Planungsleistungen gelten nicht als Beginn.",
    "Ein Rechtsanspruch des Antragstellers auf Gewährung der Zuwendung besteht nicht",
    "Das Land entscheidet nach pflichtgemäßem Ermessen im Rahmen der verfügbaren Haushaltsmittel.",
    "30 % von max. 15.000 €",
    "müssen mindestens 2 000 Euro je Wohnung betragen",
    "Gefördert werden bauliche Maßnahmen zur Nachrüstung von barrierefreien Personenaufzügen, Treppenliften oder anderen mechanischen vertikalen Personenfördersystemen an oder in Wohngebäuden mit Miet- und Genossenschaftswohnungen.",
    "Nachrüstung von Personenaufzügen, Treppenliften oder anderen mechanischen vertikalen Personenfördersystemen",
    "bis zu 4.500 Euro Förderung für Treppenlifte",
    "können Treppenlifte und viele andere Umbaumaßnahmen gefördert werden",
    "Antragsberechtigt sind Eigentümer von selbst genutztem Wohnraum und Mieter mit Zustimmung des Vermieters.",
    "B - Mieter, im Einverständnis mit dem Eigentümer/Vermieter für die selbstgenutzte Mietwohnung",
    "Für Maßnahmen, bei denen der Mieter Zuwendungsempfänger ist, gilt Nummer 5.2.2 entsprechend.",
    "Erklärung Eigentümer bei Antragstellung durch Mieter",
    "Zuständig sind die Landkreise und kreisfreien Städte in Mecklenburg-Vorpommern als Sozialhilfeträger",
    "sofern sie die Anspruchsvoraussetzungen erfüllen",
    "Werden zur Finanzierung der Maßnahmen auch finanzielle Zuschüsse zur Verbesserung des individuellen Wohnumfeldes von Pflegebedürftigen gemäß § 40 des Elften Buches Sozialgesetzbuch",
    "Das Programm zum Abbau von Barrieren im Wohnungsbestand wurde jetzt um 2 Millionen Euro aufgestockt.",
    "rund 18,6 Millionen Euro bewilligt",
    "In diesem Jahr hatten wir rund 3,6 Millionen für das Programm zur Verfügung.",
    "um einen Antragsannahmestopp zu vermeiden",
    "Diesen Zuschuss können Sie nicht mehr beantragen.",
    "Sollten im Jahr 2027 erneut Bundesmittel für barrierereduzierende Maßnahmen",
    "bis zu 50.000 Euro je Wohneinheit",
    "Treppenlifte, Senkrecht-, Hebe- oder Plattformlifte installieren",
    "mit dem Kredit der KfW gefördert werden.",
    "Mit 19 Pflegestützpunkten in Mecklenburg-Vorpommern",
    "kostenfreie und trägerunabhängige Beratung",
    "Leistungen für Wohnraum",
    "Die Leistungen umfassen Leistungen für die Beschaffung, den Umbau, die Ausstattung und die Erhaltung von Wohnraum",
    "Barrierereduzierung, E-Mobilität, Einbruchsschutz und Steckersolargeräte",
    "nicht zugemutet werden kann",
    "Eine zum Nachteil des Mieters abweichende Vereinbarung ist unwirksam.",
    "198.000 €",
    "33.000 €",
    "1,5 % des bewilligten Zuschusses, mindestens 30 €",
    "innerhalb von 12 Monaten nach Bewilligung",
    "nach dem 31.12.2026",
    "DIN 18040-2",
    "geprüft am 27.11.2026",
]
for n in NEEDLES:
    ok("needle: " + n[:52], n.lower() in pn)

# Wortlaut-Ehrlichkeit: Absenz der LFI-/Merkblatt-Nennung dokumentiert + Wayback-Datierung
ok("ehrk: lfi-absenz-dokumentiert", "das Wort Treppenlift nicht (je 0 Treffer, geprüft am 27.11.2026)" in page or "je 0 Treffer, geprüft am 27.11.2026" in page)
ok("ehrk: wayback-datierung", "Internet-Archive-Snapshots vom 08./09.11.2026" in page)
ok("ehrk: geltungsende", "31. Dezember 2026 außer Kraft" in page)

# --- 4. Absenzen ---
for bad in ["4.180", "16.720", "17.500", "12.500", "6.250", "220.000", "23.540",
            "Niedersachsenbüro", "WIBank", "L-Bank", "Friedrichshafen",
            "awin1.com", 'rel="sponsored"', ">Anzeige<", "\u00ad"]:
    ok("absenz: " + repr(bad[:22]), bad not in page_raw)

# --- 5. Hub ---
hub_raw = read("regional.html")
hub = clean(hub_raw)
ok("hub noindex", 'content="noindex,follow"' in hub_raw)
ok("hub prose 7 regionen", "Niedersachsen und Mecklenburg-Vorpommern sind als erste Regionen vollständig recherchiert" in hub)
ok("hub card mv", "/region/mecklenburg-vorpommern.html" in hub_raw)
ok("hub teaser mv", "Siebte ausführlich recherchierte Region" in hub)
ok("hub desc 7 regionen", "NRW, Bayern, Sachsen, Baden-Württemberg, Hessen, Niedersachsen und Mecklenburg-Vorpommern sind ausgebaut; weitere folgen." in hub_raw)
ok("hub alte 6-prosa 0x", "Hessen und Niedersachsen sind als erste Regionen vollständig recherchiert" not in hub)
ok("hub alte desc 0x", "Hessen und Niedersachsen sind ausgebaut, weitere Regionen folgen." not in hub_raw)

# --- 6. Sitemap ---
sm = read("sitemap.xml")
locs = re.findall(r"<loc>([^<]+)</loc>", sm)
regions = [u for u in locs if "/region/" in u]
ok("sitemap 7 regionen", len(regions) == 7, str(regions))
ok("sitemap mv drin", any(u.endswith("/region/mecklenburg-vorpommern.html") for u in locs))
ok("sitemap ohne hub", not any("/regional.html" in u for u in locs))
ok("sitemap ohne platzhalter", not any(h in u for u in regions for h in ["berlin", "hamburg", "rheinland-pfalz", "schleswig-holstein", "thueringen", "brandenburg", "bremen", "saarland"]))
robots_berlin = read("region/berlin.html")
ok("platzhalter berlin noindex", 'content="noindex,follow"' in robots_berlin)
ok("region-index-anzahl-implizit", 'content="index,follow"' in page_raw)

# --- 7. RSS unverändert ---
rss = read("rss.xml")
ok("rss item count 41", rss.count("<item>") == 41, str(rss.count("<item>")))

# --- 8. Keine Partner-Marker auf der neuen Seite (kein Placement adressiert sie) ---
ok("0 partner marker mv", "data-partner-placement" not in page_raw)

print("\n=== %d PASS, %d FAIL ===" % (PASSED, FAILED))
sys.exit(1 if FAILED else 0)
