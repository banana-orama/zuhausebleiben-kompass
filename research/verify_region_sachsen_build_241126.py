#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Content-Gate Region Sachsen (24.11.2026).
Läuft gegen den LAUNCH-Dist (DIST_DIR override möglich). Prüft:
- Alle Kernzahlen/Wortlaute in dist/region/sachsen.html (in UNSERER Prosa-Schreibweise)
- Neue §-554-Fassung in nrw/bayern, alte Fassung abwesend
- Hub-Updates (regional.html, 3 Regionen)
- Sitemap exakt 3 Region-URLs, robots der Region indexable
- CTA/Related-Ziele existieren; title/desc-Längen
- Quellenstand 2026-11-24, 13 Quellen
Exit != 0 bei FAIL."""
import json
import os
import re
import sys

ROOT = os.environ.get("ZBK_ROOT", "/Users/mac/agentic-business/barrierefrei-leads")
DIST = os.environ.get("DIST_DIR", os.path.join(ROOT, "dist"))
FAILS = []


def read(p):
    with open(os.path.join(DIST, p), encoding="utf-8") as f:
        return f.read()


def strip_tags(html):
    html = re.sub(r"<script[\s\S]*?</script>", " ", html)
    html = re.sub(r"<style[\s\S]*?</style>", " ", html)
    html = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", html)


def check(name, cond, detail=""):
    if not cond:
        FAILS.append("%s :: %s" % (name, detail))


sachsen = read("region/sachsen.html")
sx = strip_tags(sachsen)

# --- Kernzahlen/Wortlaute (Prosa + Tabelle) ---
needles = [
    # FRL-Rahmen (Prosa-Verbatim, Gesetzesschreibweise mit Leerzeichen)
    "grundsätzlich zu 80 Prozent, maximal mit einem Betrag von 4 000 Euro",
    "maximal mit einem Betrag von 10 000 Euro gefördert",
    "100 % der förderfähigen Ausgaben, max. 5.000 €",
    "max. 12.500 €",
    "100 %/5.000 € bzw. 12.500 €",
    "mindestens 1 500 Euro",
    # Treppenlift (FAQ-Verbatim)
    "Treppenlifte sind innerhalb der Mietwohnung bzw. eines Einfamilienhauses förderfähig",
    "Außerhalb von Wohnungen (im Treppenhaus oder im Zugangsbereich) ist die Förderung nur bei vom Zuwendungsempfänger als Eigentümer oder Erbbauberechtigtem selbstgenutzten Wohngebäuden mit bis zu zwei Wohnungen möglich",
    # Nachrang (FRL-Verbatim)
    "Die Förderung ist nachrangig gegenüber Leistungen Dritter",
    "reduzieren die zuwendungsfähigen Ausgaben",
    # Einkommen (FRL + Tabelle)
    "Summe der positiven Einkünfte des Haushalts eines Jahres gemäß § 2 Absatz 2 Einkommensteuergesetz",
    "40 000 Euro",
    "60 000 Euro",
    "40.000 €",
    "60.000 €",
    "+ 10.000 €",
    "Die Einhaltung der Einkommensgrenze gilt als erfüllt",
    # Antragsweg + Fristen
    "Bewilligungsstelle ist die Sächsische Aufbaubank",
    "Förderportal Sachsen",
    "Auftragserteilung an eine Fachfirma",
    "ca. 4 bis max. 12 Wochen",
    "24.09.2026",
    "05.11.2026",
    "Antragsteller ist immer die mobilitätseingeschränkte Person selbst",
    # Außenmaßnahmen (FRL)
    "abschließbare Boxen",
    "von der Grundstücksgrenze bis zu einer Hauseingangstür",
    # Weg 3 EH (amt24-Verbatim)
    "grundsätzlich von den Landkreisen und den Kreisfreien Städten erbracht",
    "Kommunale Sozialverband Sachsen",
    "formlos per E-Mail",
    # Fachstellen-Regionen
    "Erzgebirgskreis",
    "Bautzen",
    "Nordsachsen",
    # PflegeNetz
    "innerhalb von zwei Wochen aktiv eine Pflegeberatung",
    "Diese Beratung ist kostenfrei",
    # KfW (Verbatim)
    "Wegen der hohen Nachfrage sind die Fördermittel für Maßnahmen zur Barrierereduzierung bereits ausgeschöpft",
    "50.000 Euro je Wohneinheit",
    # § 554 neue Fassung
    "die dem Gebrauch durch Menschen mit Behinderungen dienen",
    "nicht zugemutet werden kann",
    # Mieter-Zielgruppe
    "Vermieterbestätigung",
    # Zielgruppe Eigentümer/Mieter
    "Mieter sind adressiert",
]
for n in needles:
    check("NEEDLE %r" % n[:70], n in sx, "nicht in sachsen.html gefunden")
# historische 8.000/20.000-Zahlen dürfen NICHT als aktive Kondition auftauchen
check("ALT-ZAHLEN 8.000-€-Kondition abwesend", "maximal 8 000 Euro" not in sx and "max. 8.000 €" not in sx, "alte Beträge live")
check("ALT-ZAHLEN 20.000-€-Kondition abwesend", "maximal 20 000 Euro" not in sx and "max. 20.000 €" not in sx, "alte Beträge live")
check("News-Datum nur im Quellen-Label (historisch markiert)", sx.count("01.08.2025") == 1, "Vorkommen: %d" % sx.count("01.08.2025"))

# --- Struktur ---
check("Quellenstand 2026-11-24", "Quellenstand: 2026-11-24" in sachsen)
check("13 Quellen gerendert", sachsen.count("— geprüft 2026-11-24") == 13, str(sachsen.count("— geprüft 2026-11-24")))
check("H1", "<h1>Umbau und Förderung in Sachsen</h1>" in sachsen)
check("FAQ-Sektion", "<h2>Häufige Fragen</h2>" in sachsen and sachsen.count("<details>") == 6, str(sachsen.count("<details>")))
check("Early-CTA Ziel", 'href="https://zuhausebleiben-kompass.de/treppenlift-zuschuss.html"' in sachsen or 'href="/treppenlift-zuschuss.html"' in sachsen)
check("Weg1-CTA Ziel wohnumfeld", "/wohnumfeldverbesserung-beantragen.html" in sachsen)
check("Weg3-CTA Ziel ohne-pflegegrad", "/treppenlift-foerderung-ohne-pflegegrad.html" in sachsen)
for slug in ["treppenlift-mietwohnung", "wohnumfeldverbesserung-beantragen", "treppenlift-kosten"]:
    check("Related-Ziel %s" % slug, ("/%s.html" % slug) in sachsen)
check("table.note Weg2 gerendert", "mindestens 1 500 Euro" in sx and "Stand: 24.11.2026" in sx)
check("print-button", "Diese Seite drucken" in sachsen)
check("KI-Kennzeichnung", "Mit KI-Unterstützung erstellt" in sachsen)
# robots/canonical
m = re.search(r'<meta name="robots" content="([^"]+)"', sachsen)
check("robots indexable", m and m.group(1) == "index,follow", m.group(0) if m else "missing")
m = re.search(r'<link rel="canonical" href="([^"]+)"', sachsen)
check("canonical", m and m.group(1).endswith("/region/sachsen.html"), m.group(1) if m else "missing")

# --- § 554 Fix in NRW/Bayern ---
old = "verlangen die Duldung bzw. Zustimmung des Vermieters nach § 554 BGB, mit klaren Ausnahme- und Interessenabwägungsregeln"
new = "die dem Gebrauch durch Menschen mit Behinderungen dienen"
for p in ["region/nordrhein-westfalen.html", "region/bayern.html"]:
    t = strip_tags(read(p))
    check("§554-ALT abwesend in %s" % p, old not in t, "alte Fassung noch live")
    check("§554-NEU in %s" % p, new in t, "neue Fassung fehlt")
    check("§554-Fassung-Hinweis in %s" % p, "Barrierereduzierung" in t)

# --- Hub ---
hub = read("regional.html")
hx = strip_tags(hub)
check("Hub-Prosa 3 Regionen", "Nordrhein-Westfalen, Bayern und Sachsen sind als erste Regionen vollständig recherchiert" in hx)
check("Hub-Desc 3 Regionen", "Nordrhein-Westfalen, Bayern und Sachsen sind ausgebaut" in hub)
check("Hub-Teaser Sachsen", "Dritte ausführlich recherchierte Region" in hx)
check("Hub bleibt noindex", 'content="noindex,follow"' in hub)

# --- Sitemap ---
sm = read("sitemap.xml")
locs = re.findall(r"<loc>([^<]+)</loc>", sm)
region_locs = [u for u in locs if "/region/" in u]
check("Sitemap: genau 3 Region-URLs", len(region_locs) == 3, str(region_locs))
check("Sitemap: sachsen enthalten", any(u.endswith("/region/sachsen.html") for u in locs))
check("Sitemap: Hub nicht enthalten", not any(u.endswith("/regional.html") for u in locs))
check("Sitemap: Platzhalter nicht enthalten", not any(u.endswith("/region/baden-wuerttemberg.html") for u in locs))

# --- title/desc Längen ---
t = re.search(r"<title>([^<]*)</title>", sachsen).group(1)
check("Titel ≤65", len(t) <= 65, "%d: %s" % (len(t), t))
d = re.search(r'<meta name="description" content="([^"]+)"', sachsen).group(1)
check("Desc ≤155", len(d) <= 155, "%d: %s" % (len(d), d))

print("VERIFY REGION SACHSEN BUILD 241126")
for f in FAILS:
    print("FAIL", f)
print("RESULT: %d checks, %d FAIL" % (len(needles) + 32, len(FAILS)))
sys.exit(1 if FAILS else 0)
