#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quick-Build-Check Region Niedersachsen (27.11.2026) — LAUNCH-dist.
Robots/Title/H1/Sitemap/Hub/Keyneedles/Absenzen auf einen Blick."""
import re
import sys

DIST = "dist"
h = open(DIST + "/region/niedersachsen.html", encoding="utf-8").read()
hub = open(DIST + "/regional.html", encoding="utf-8").read()
sm = open(DIST + "/sitemap.xml", encoding="utf-8").read()

fails = []


def chk(label, cond, detail=""):
    print(("PASS" if cond else "FAIL"), label, detail if not cond else "")
    if not cond:
        fails.append(label)


robots = re.search(r'robots" content="([^"]+)"', h)
chk("robots index,follow", robots and robots.group(1) == "index,follow", robots.group(1) if robots else "?")
chk("title", "<title>Umbau-Förderung in Niedersachsen — ZuhauseBleiben Kompass</title>" in h)
chk("h1", "<h1>Umbau und Förderung in Niedersachsen</h1>" in h)
chk("canonical", 'href="https://zuhausebleiben-kompass.de/region/niedersachsen.html"' in h)
locs = re.findall(r"<loc>([^<]+)</loc>", sm)
regions = [u for u in locs if "/region/" in u]
chk("sitemap 6 regionen", len(regions) == 6, str(regions))
chk("sitemap nds drin", any(u.endswith("/region/niedersachsen.html") for u in locs))
chk("sitemap ohne hub", not any("/regional.html" in u for u in locs))
chk("hub nds karte", "/region/niedersachsen.html" in hub)
chk("hub teaser", "Sechste ausführlich recherchierte Region" in hub)
chk("hub prose 6", "Hessen und Niedersachsen sind als erste Regionen" in hub)
chk("hub noindex", 'content="noindex,follow"' in hub)
pn = h.lower()
chk("treppenlift count >= 8 (Ehrlichkeit-Kontexte)", pn.count("treppenlift") >= 8, str(pn.count("treppenlift")))
for needle in [
    "Das Wort Treppenlift kommt weder auf der NBank-Produktseite",
    "bis zu 40 % der Gesamtkosten, max. 6.000 Euro",
    "bis zu 30 % der Gesamtkosten, max. 4.500 Euro",
    "21.250 Euro",
    "4.000 Euro",
    "nicht der alleinige Treppenlift",
    "FORUM Gemeinschaftliches Wohnen e.V.",
    "geprüft 2026-11-27",
]:
    chk("needle: " + needle[:50], needle in h)
for bad in ["4.180", "16.720", "awin1.com", 'rel="sponsored"', ">Anzeige<", "‑", "\u00ad"]:
    chk("absenz: " + repr(bad), bad not in h)
chk("kein U+00AD", "\u00ad" not in h)

print("\n== QUICK BUILD CHECK: %d FAILS ==" % len(fails))
sys.exit(1 if fails else 0)
