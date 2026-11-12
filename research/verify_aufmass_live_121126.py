#!/usr/bin/env python3
"""Live-Readback für treppenlift-aufmass-termin (Briefing 25) auf der öffentlichen URL."""
import sys
import time
import urllib.request

HOST = "https://zuhausebleiben-kompass.de"
UA = {"User-Agent": "Mozilla/5.0 (live-readback)"}

FAIL = []
N = 0


def check(label, cond, detail=""):
    global N
    N += 1
    print(("PASS " if cond else "FAIL ") + label + ("" if cond else f"  {detail}"))
    if not cond:
        FAIL.append(label)


def fetch(path, binary=False):
    req = urllib.request.Request(HOST + path, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    return data if binary else data.decode("utf-8", errors="replace")


# Pages-Deploy-Lag: Artikel-URL poll'en bis 200 (max 6 Min)
art_url = "/treppenlift-aufmass-termin.html"
status = None
for _ in range(18):
    try:
        req = urllib.request.Request(HOST + art_url, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            status = r.status
        if status == 200:
            break
    except Exception:
        pass
    time.sleep(20)

html_raw = fetch(art_url) if status == 200 else ""
check("Artikel live HTTP 200", status == 200, str(status))
if status != 200:
    sys.exit("Artikel nicht erreichbar — Deploy-Lag oder Build-Problem")

html = html_raw
check("robots index,follow", 'name="robots" content="index,follow"' in html.replace(", ", ","))
check("title live", "Treppenlift-Aufmaß richtig vorbereiten" in html)
check("h1 live", "Treppenlift-Aufmaß-Termin: was passiert" in html)
check("Quellenstand 12.11.2026", "geprüft 2026-11-12" in html)

for needle in ["Festpreis inklusive Montage", "innerhalb von 24 Stunden",
               "zwei bis drei Stunden", "maximal fünf Stunden",
               "14-tägiges Widerrufsrecht", "12 Monate und 14 Tage",
               "gleichem Leistungsumfang", "Unterschreiben Sie nicht vorschnell",
               "46 von 123", "Kostenvoranschlag für die Pflegekasse"]:
    check(f"live Kernwortlaut: {needle[:36]}", needle in html)

check("related 1 angebote-vergleichen", "treppenlift-angebote-vergleichen.html" in html.split("Passend dazu")[1][:600])
check("related 2 unserioese", "treppenlift-unserioese-anbieter.html" in html.split("Passend dazu")[1][:600])
check("related 3 schmale-treppe", "treppenlift-schmale-treppe.html" in html.split("Passend dazu")[1][:600])
check("early CTA firmen-vergleich", "Anbieter für Aufmaß vergleichen" in html and 'href="https://zuhausebleiben-kompass.de/treppenlift-firmen-vergleich.html"' in html)
check("checklist anchor abschnitt-8", 'href="#abschnitt-8"' in html)
check("0 Partner-Marker", "data-partner-placement" not in html and "awin1.com" not in html)
check("0 €-Zeichen", "€" not in html)
check("0 Förderbeträge", "4.180" not in html and "16.720" not in html and "KfW" not in html)

svg = fetch("/assets/images/treppenlift-aufmass-termin-ablauf.svg", binary=True)
check("SVG live 200 + bytes", len(svg) > 3000, str(len(svg)))

sm = fetch("/sitemap.xml")
check("sitemap enthält Artikel", "treppenlift-aufmass-termin.html" in sm)
locs = sm.count("<loc>")
check("sitemap 47 locs", locs == 47, str(locs))

rss = fetch("/rss.xml")
check("rss enthält Artikel", "treppenlift-aufmass-termin" in rss)
items = rss.count("<item>")
check("rss 36 items", items == 36, str(items))

home = fetch("/")
check("Homepage listet Artikel", "treppenlift-aufmass-termin.html" in home)
llms = fetch("/llms.txt")
check("llms.txt listet Artikel", "treppenlift-aufmass-termin" in llms)

print(f"\n{N - len(FAIL)}/{N} Pässe")
if FAIL:
    for f in FAIL:
        print(" -", f)
    sys.exit(1)
print("ALL PASS")
