#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Content-Gate Region Niedersachsen (27.11.2026) — gegen LAUNCH-dist.
Prüft: robots/Canonical/Title, alle Kernwordlaute im gebauten HTML (getaggt,
entities-unescape'd, Whitespace normalisiert, case-normalisiert), alle FAQ-Fragen,
alle 21 Quellen-URLs, Related-/CTA-Ziele absolut, Quellenstand, Absenzen
(Pflegekassen-Beträge 0×, Partner-Marker 0×, U+00AD 0×, alte Hub-Prosa 0×),
Hub 6 Regionen + noindex, Sitemap exakt 6 Region-URLs ohne Hub/Platzhalter.
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
        print("FAIL", label, str(detail)[:140])


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


page_raw = read("region/niedersachsen.html")
page = clean(page_raw)
pn = page.lower()
d = json.load(open(os.path.join(ROOT, "data", "region-niedersachsen.json"), encoding="utf-8"))

# --- Struktur ---
ok("robots index,follow", '<meta name="robots" content="index,follow"' in page_raw)
ok("canonical", 'href="%s/region/niedersachsen.html"' % BASE in page_raw.replace("&amp;", "&"))
ok("title", "<title>%s — ZuhauseBleiben Kompass</title>" % d["title"] in page_raw)
ok("h1", "<h1>%s</h1>" % d["h1"] in page_raw)
ok("desc meta", 'name="description" content="%s"' % d["description"] in page_raw)
ok("quellenstand", "Quellenstand: 2026-11-27" in page)
ok("geprueft 21x", page.count("geprüft 2026-11-27") == 21, str(page.count("geprüft 2026-11-27")))

# --- Kernwordlaute (Prosa-Schreibweise) ---
NEEDLES = [
    "Barrierereduzierende Modernisierung von selbstgenutztem Wohneigentum",
    "als ein anfänglich zinsloses, rückzahlbares Darlehen und als ein nicht rückzahlbarer Zuschuss in Form einer Anteilsfinanzierung zur Projektförderung gewährt",
    "Barrierereduzierende Modernisierung eines bestehenden Gebäudes mit Gesamtkosten von bis zu 15.000 Euro",
    "Einkommensgruppe A: bis zu 40 % der Gesamtkosten, max. 6.000 Euro",
    "Einkommensgruppen B+C: bis zu 30 % der Gesamtkosten, max. 4.500 Euro",
    "Bei der barrierereduzierenden Modernisierung mit Gesamtkosten ab 15.001 Euro und bei der klimagerechten Modernisierung ist die Gewährung des Zuschusses an die Inanspruchnahme des Darlehens gebunden",
    "eine Zuwendung ausschließlich in Form des Zuschusses bei diesen Förderungen ist ausgeschlossen",
    "für die Dauer von 15 Jahren zu einem Zinssatz von 0 %",
    "Tilgung von 2 %",
    "0,5 % vom jeweiligen Restschuldbetrag",
    "1 % des bewilligten Darlehens bzw. 0,75 % des bewilligten Zuschusses",
    "bis zu 35 Prozent vor (maximal 17.500 Euro)",
    "bis zu 25 Prozent (maximal 12.500 Euro)",
    "Den Antrag auf barrierereduzierende und/oder klimagerechte Modernisierung selbstgenutzten Wohneigentums stellen Sie bitte bei der für Ihren Bauort zuständigen Wohnraumförderstelle (Landkreis, Stadt, Gemeinde).",
    "Ihre zuständige Wohnraumförderstelle finden Sie hier",
    "Ein Anspruch auf Gewährung einer Zuwendung besteht nicht, vielmehr entscheidet die Bewilligungsbehörde aufgrund ihres pflichtgemäßen Ermessens im Rahmen der verfügbaren Haushaltsmittel",
    "Derzeit verzeichnen wir ein besonders hohes Antragsaufkommen. Dadurch kann sich die Bearbeitung Ihres Antrags leider etwas verzögern.",
    "Bereits begonnene Vorhaben werden nicht gefördert. Als Vorhabenbeginn ist grundsätzlich der Abschluss eines dem Vorhaben zuzurechnenden Lieferungs-, Leistungs-, Kauf- oder Werkvertrages zu werten.",
    "Bei Maßnahmen mit im Antrag zugrunde gelegten zuwendungsfähigen Ausgaben von weniger als 100 000 EUR ist der Vorhabenbeginn ab Antragstellung zugelassen.",
    "Durch die baulichen Maßnahmen muss eine Verringerung bestehender Barrieren erreicht werden, die die Zugänglichkeit, Bewegungsfreiheit oder Nutzbarkeit des Wohnraums für die Bewohnerinnen und Bewohner verbessert",
    "Freibetrag von 4.000 Euro",
    "21.250 Euro für einen Einpersonenhaushalt und 28.750 Euro für zwei Personen",
    "3.750 Euro hinzu",
    "um bis zu 40 %",
    "um bis zu 60 %",
    "675 Euro",
    "600 Euro je weiterem Haushaltsmitglied und 475 Euro je Kind",
    "Die Eigenmittel müssen 10 %, bei Haushalten mit 2 oder mehr Kindern sowie mit Menschen mit Behinderungen 7,5 %, der Gesamtkosten (z. B. Bargeld, Guthaben, Sach- und Arbeitsleistungen) betragen.",
    "bis zu 30 % nach Beginn der Baumaßnahme",
    "nach Abschluss und Schlussbescheinigung (Richtlinie)",
    "selbst genutzten Bestandsimmobilie",
    "in Höhe von 5.000 Euro für jede barrierefrei nutzbare Wohnung gemäß DIN 18040-2",
    "Das Wort Treppenlift kommt weder auf der NBank-Produktseite",
    "FORUM Gemeinschaftliches Wohnen e.V. und BAG Wohnungsanpassung e.V.",
    "auch der Badumbau und Treppenlift, aber nicht der alleinige Treppenlift",
    "nichtamtliche Wohnberatung (Träger laut Impressum: FORUM Gemeinschaftliches Wohnen e.V. und BAG Wohnungsanpassung e.V.)",
    "Die Landesförderbank in Sachsen nennt Treppenlifte in ihrem Programm ausdrücklich",
    "Zuständig für die Leistungen der Eingliederungshilfe sind in Niedersachsen die Kommunen, das heißt die Landkreise, die kreisfreien Städte, die Region Hannover, die Städte Hannover, Göttingen, Hildesheim, Lingen (Ems) und Lüneburg.",
    "Leistungen der Eingliederungshilfe erhalten Sie nur auf Antrag",
    "Antragstellung ist nicht an Fristen gebunden",
    "erst beginnend mit dem Monat der Antragstellung",
    "sofern Sie die erforderliche Leistung nicht von anderen Sozialleistungs- oder Rehabilitationsträgern",
    "Die Kosten für die Leistungen übernimmt der zuständige Träger",
    "Bei den Leistungen der Eingliederungshilfe müssen Sie grundsätzlich einen Beitrag aus Ihrem Einkommen sowie aus Ihrem Vermögen, sofern es eine festgesetzte Grenze überschreitet, zahlen.",
    "Die Leistungen umfassen Leistungen für die Beschaffung, den Umbau, die Ausstattung und die Erhaltung von Wohnraum",
    "Diesen Zuschuss können Sie nicht mehr beantragen.",
    "Sollten im Jahr 2027 erneut Bundesmittel für barrierereduzierende Maßnahmen",
    "Treppenlifte, Senkrecht-, Hebe- oder Plattformlifte installieren",
    "mit dem Kredit der KfW gefördert werden.",
    "bis zu 50.000 Euro je Wohneinheit",
    "Daher fördert das Land die Einrichtung und den Betrieb eines Senioren- und Pflegestützpunktes Niedersachsen oder eines Seniorenstützpunktes Niedersachsen in jedem Landkreis und jeder kreisfreien Stadt sowie in der Region Hannover, der Landeshauptstadt Hannover und der Stadt Göttingen.",
    "Barrierereduzierung, E-Mobilität, Einbruchsschutz und Steckersolargeräte",
    "nicht zugemutet werden kann",
    "die dem Gebrauch durch Menschen mit Behinderungen",
    "Mit den wohnumfeldverbessernden Maßnahmen gewährt Ihnen die Pflegekasse einen Zuschuss zu baulichen Maßnahmen wie z.B. Türverbreiterungen, Badumbau oder fest installierte Rampen und Treppenlifte.",
    "amtlich nicht dokumentiert — fragen Sie direkt nach",
    "RdErl. des Ministeriums für Wirtschaft, Verkehr und Bauen vom 25.06.2026, Nds. MBl. 2026 Nr. 317",
    "Investitions- und Förderbank des Landes",
    "Wohnen im Alter“ des niedersächsischen Sozialministeriums",
    "21.250 € (1 Person) bzw. 28.750 € (2 Personen)",
    "Eigenmittel 10 % beziehungsweise 7,5 %",
]
for n in NEEDLES:
    ok("needle: " + n[:52], n.lower() in pn)

# --- Treppenlift-Nennungslogik (Wortlaut-Ehrlichkeit): das Wort Treppenlift
# erscheint als Kontext/CTA/Broschüre/Vergleich, aber die Absenz im NDS-Landes-
# programm muss explizit dokumentiert UND die nichtamtliche Auslegung gekennzeichnet sein.
ok("absenz-dokumentation", "Das Wort Treppenlift kommt weder auf der NBank-Produktseite" in page)
ok("je-0-treffer-dokumentiert", "je 0 Treffer, geprüft am 27.11.2026" in page)
ok("nichtamtlich-kennzeichnung", "nichtamtliche" in page)
ok("nicht-bindend-hinweis", "für die Bewilligung nicht bindend" in page)

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
for bad in ["4.180", "16.720", "4 180", "16 720", "awin1.com", 'rel="sponsored"', ">Anzeige<", "\u00ad", "L-Bank", "Friedrichshafen", "WIBank"]:
    ok("absenz: " + repr(bad[:20]), bad not in page_raw)

# --- Hub ---
hub_raw = read("regional.html")
hub = clean(hub_raw)
ok("hub noindex", 'content="noindex,follow"' in hub_raw)
ok("hub prose nds", "Hessen und Niedersachsen sind als erste Regionen vollständig recherchiert" in hub)
ok("hub card nds", "/region/niedersachsen.html" in hub_raw)
ok("hub teaser nds", "Sechste ausführlich recherchierte Region" in hub)
ok("hub desc 6 regionen", "Nordrhein-Westfalen, Bayern, Sachsen, Baden-Württemberg, Hessen und Niedersachsen sind ausgebaut, weitere Regionen folgen." in hub_raw)
ok("hub alte 5-regionen-prosa 0x", "Baden-Württemberg und Hessen sind als erste Regionen" not in hub)

# --- Sitemap ---
sm = read("sitemap.xml")
locs = re.findall(r"<loc>([^<]+)</loc>", sm)
regions = [u for u in locs if "/region/" in u]
ok("sitemap 6 regionen", len(regions) == 6, str(regions))
ok("sitemap nds drin", any(u.endswith("/region/niedersachsen.html") for u in locs))
ok("sitemap ohne hub", not any("/regional.html" in u for u in locs))
ok("sitemap ohne platzhalter", not any(h in u for u in regions for h in ["berlin", "brandenburg", "thueringen", "rheinland-pfalz", "saarland", "schleswig-holstein", "hamburg", "bremen", "mecklenburg"]))

# --- RSS unverändert (keine Artikel-Änderung) ---
rss = read("rss.xml")
ok("rss item count 41", rss.count("<item>") == 41, str(rss.count("<item>")))

print("\n=== %d PASS, %d FAIL ===" % (PASSED, FAILED))
sys.exit(1 if FAILED else 0)
