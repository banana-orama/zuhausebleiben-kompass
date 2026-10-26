#!/usr/bin/env python3
"""Live-Readback nach Batch-7-Deploy: Steuer-Artikel öffentlich, indexierbar, vollständig;
Sitemap 44 locs; RSS 21 Items; Homepage listet Artikel; Grafik 200; PREVIEW-Asserts bleiben unverändert."""
import re
import sys
import urllib.request

BASE = "https://zuhausebleiben-kompass.de"
fails = []


def get(path):
    req = urllib.request.Request(BASE + path, headers={"Cache-Control": "no-cache", "User-Agent": "zbk-live-readback/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, r.read().decode("utf-8", "replace")


def check(name, cond, detail=""):
    print(("PASS" if cond else "FAIL"), name, detail)
    if not cond:
        fails.append(name)


SLUG = "treppenlift-steuerlich-absetzen"
s, pg = get(f"/{SLUG}.html")
check("artikel 200", s == 200, str(s))
check("robots index,follow", 'content="index,follow"' in pg)
check("kein ENTWURF-Badge", "Entwurf" not in pg)
check("H1", "Treppenlift und Badumbau steuerlich absetzen" in pg)
for needle, label in [
    ("Renovierungs-, Erhaltungs- und Modernisierungsmaßnahmen", "§35a-Maßnahmentypen"),
    ("höchstens jedoch um 1.200 Euro", "20 %/1.200 €"),
    ("Dies gilt nicht für öffentlich geförderte Maßnahmen", "Förder-Ausnahme"),
    ("Referentenentwurf des Einkommensteuerreformgesetzes 2027", "Entwurf 2027 getrennt"),
    ("gesetze-im-internet.de/estg/__35a.html", "Quelle 1 verlinkt"),
    ("Anlage Haushaltsnahe Aufwendungen", "Formular-Hinweis"),
    ("560 Euro", "Beispielrechnung"),
]:
    check(label, needle in pg)
check("Grafik referenziert", "assets/images/treppenlift-steuer-weg.svg" in pg)
check("KI-Label", "KI-unterstützt erstellte Schema-Grafik" in pg)
check("4 Quellen", pg.count('id="source-') == 4, str(pg.count('id="source-')))
check("keine Formulare", "<form" not in pg)
check("kein Tracking-Loader", not re.search(r"googletagmanager\.com|stape\.io", pg))

s2, svg = get("/assets/images/treppenlift-steuer-weg.svg")
check("svg 200+xml", s2 == 200 and svg.lstrip().startswith("<?xml") or svg.lstrip().startswith("<svg"), str(s2))

s3, sm = get("/sitemap.xml")
locs = re.findall(r"<loc>([^<]+)</loc>", sm)
check("sitemap 44 locs", len(locs) == 44, str(len(locs)))
check("artikel in sitemap", any(SLUG in u for u in locs))

s4, rss = get("/rss.xml")
check("rss 21 items", rss.count("<item>") == 21, str(rss.count("<item>")))
check("artikel in rss", SLUG in rss)

s5, home = get("/")
check("home listet artikel", SLUG in home)

print()
if fails:
    print(f"ERGEBNIS: {len(fails)} FAIL: {fails}")
    sys.exit(1)
print("ERGEBNIS: LIVE-READBACK ALL PASS")
