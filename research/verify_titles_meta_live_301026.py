#!/usr/bin/env python3
"""Live-Readback Fix #7 (30.10.2026): öffentliche URL nach Deploy prüfen —
neue kurzen Titel/Descriptions wirklich live, robots unverändert index,follow,
llms.txt/RSS frisch. Distinguish commit/push von abgeschlossenem Deploy."""
import sys
import urllib.request

import re
import html as H

BASE = "https://zuhausebleiben-kompass.de"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
fails, passed = [], 0

def get(path):
    return urllib.request.urlopen(urllib.request.Request(BASE + path, headers=UA), timeout=25).read().decode("utf-8", "replace")

def check(name, cond, detail=""):
    global passed
    if cond:
        passed += 1
        print(f"PASS {name}")
    else:
        fails.append(name)
        print(f"FAIL {name} {detail}")

ARTICLES = {
    "treppenlift-kosten": ("Treppenlift-Kosten: Angebot & Beispiele", None),
    "treppenlift-aussentreppen-aussenlift": ("Treppenlift für die Außentreppe", None),
    "treppenlift-plattformlift-rollstuhllift": ("Plattformlift (Rollstuhllift): Kosten", "Portale 6.000–30.000"),
    "treppenlift-steuerlich-absetzen": ("Treppenlift steuerlich absetzen", "20 Prozent der Arbeitskosten"),
    "treppenlift-zuschuss": ("Treppenlift-Zuschuss: Pflegekasse & KfW", "Bis zu 4.180 Euro"),
    "pflegegrad-antrag-ablauf-fristen": ("Pflegegrad beantragen: Ablauf & Fristen", None),
    "wanne-zur-dusche": ("Wanne zur Dusche umbauen: Varianten", None),
    "hilfsmittel-dusch-wc-uebernahme": ("Dusch-WC: Was Krankenkassen übernehmen", None),
}
for slug, (title, desc_needle) in ARTICLES.items():
    h = get(f"/{slug}.html")
    t = H.unescape(re.search(r"<title[^>]*>(.*?)</title>", h, re.S).group(1)).strip()
    d = H.unescape(re.search(r'<meta name="description" content="([^"]*)"', h).group(1)).strip()
    r = re.search(r'<meta name="robots" content="([^"]*)"', h).group(1)
    check(f"{slug}: title==='{title} — …' ({len(t)}≤65)", t == title + " — ZuhauseBleiben Kompass" and len(t) <= 65, t)
    if desc_needle:
        check(f"{slug}: desc hält Kernzahl ({len(d)}≤160)", desc_needle in d and len(d) <= 160, d[:90])
    check(f"{slug}: robots index,follow", r == "index,follow", r)

x4 = get("/pflegegrad-beantragen.html")
d = H.unescape(re.search(r'<meta name="description" content="([^"]*)"', x4).group(1)).strip()
check("X4: Stub-Desc benefit-first, kein 242er-Disclaimer", d.startswith("Wo Sie beim Pflegegrad") and len(d) <= 160, f"{len(d)}: {d[:80]}")

hub = get("/checklisten/index.html")
t = H.unescape(re.search(r"<title[^>]*>(.*?)</title>", hub, re.S).group(1)).strip()
d = H.unescape(re.search(r'<meta name="description" content="([^"]*)"', hub).group(1)).strip()
check("Checklisten-Hub Titel 51", t == "Checklisten zum Ausdrucken — ZuhauseBleiben Kompass" and len(t) <= 65, f"{len(t)}: {t}")
check("Checklisten-Hub Desc ≤160", len(d) <= 160, f"{len(d)}")

sub = get("/checklisten/tuerbreiten-schwellen-schnellcheck.html")
t = H.unescape(re.search(r"<title[^>]*>(.*?)</title>", sub, re.S).group(1)).strip()
check("Checklisten-Unterseite kurzer Titel, H1 lang", t == "Checkliste: Türbreiten & Schwellen — ZuhauseBleiben Kompass" and "Türbreiten und Schwellen schnell prüfen (Messbogen)" in sub, t)

rss = get("/rss.xml")
check("RSS kurze Item-Titel (mit Suffix)", "<title>Treppenlift-Kosten: Angebot &amp; Beispiele — ZuhauseBleiben Kompass</title>" in rss)
llms = get("/llms.txt")
check("llms.txt frisch (neuer Titel)", "[Treppenlift-Kosten: Angebot & Beispiele]" in llms)
sm = get("/sitemap.xml")
check("Sitemap 49 locs", sm.count("<loc>") == 49, str(sm.count("<loc>")))
check("H1 unverändert (Kosten-Ratgeber)", "Treppenlift-Kosten: So planen Sie Anschaffung und laufende Ausgaben" in get("/treppenlift-kosten.html"))

print(f"\n{passed} PASS, {len(fails)} FAIL")
if fails:
    print("FAILS:", fails)
    sys.exit(1)
print("LIVE-READBACK titles-meta 301026: ALL PASS")
