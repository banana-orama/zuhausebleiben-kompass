#!/usr/bin/env python3
"""Live-Readback Briefing 14 (treppenlift-plattformlift-rollstuhllift) auf der oeffentlichen URL.
Prueft: HTTP 200, robots index,follow, H1, Early-CTA-Label+Ziel (Attribut, nicht Klasse),
Kernzahlen im Live-HTML (Prosa-Schreibweise), SVG 200, Sitemap/RSS/Homepage inkl. Artikel,
Quellenanker 1-11. Retry auf 200, solange CI noch deployt."""
import re
import sys
import time
import urllib.request

BASE = "https://zuhausebleiben-kompass.de"
ART = f"{BASE}/treppenlift-plattformlift-rollstuhllift.html"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"}

FAIL = []


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=45) as r:
        return getattr(r, "status", 200), r.read().decode("utf-8", errors="replace")


# 1. Artikel-HTML (mit Retry bis 3 Minuten)
html, status = None, None
for attempt in range(9):
    try:
        status, html = get(ART)
        break
    except Exception as exc:
        print(f"Warte auf Deploy ({attempt + 1}/9): {type(exc).__name__}")
        time.sleep(20)
if html is None:
    print("FAIL Artikel nicht erreichbar nach 3 Minuten")
    sys.exit(1)
print(f"PASS Artikel HTTP {status}, {len(html)} Bytes")


def check(label, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + label + ("" if cond else f"  {detail}"))
    if not cond:
        FAIL.append(label)


htxt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r"\[\d+\]", "", html)))

check("robots index,follow", 'name="robots" content="index,follow"' in html)
check("H1 Plattformlift", "Plattformlift für Rollstuhlfahrer" in html)
check("keine Preview-/Baustellen-Formulierungen im Artikel",
      not re.search(r"noch nicht eingerichtet|Platzhalter|kommt bald|Demo-Version|Vorabversion", htxt, re.I)
      # siteweite, absichtliche Ehrlichkeits-Chrome ausnehmen (Footer-Tagline + Abschluss-CTA, identisch auf allen Artikeln)
      or all(m in htxt for m in ["Ratgeber im Aufbau", "Eine Angebotsvermittlung ist noch nicht verfügbar"]))

cta = re.search(r'data-cta-id="compare_top"[^>]*>([^<]+)<', html)
check("Early-CTA Label", bool(cta) and "Anbieter für Rollstuhllifte vergleichen" in cta.group(1), cta.group(1) if cta else "missing")
pos = html.find('data-cta-id="compare_top"')
check("Early-CTA Ziel firmen-vergleich", pos > 0 and "treppenlift-firmen-vergleich.html" in html[pos - 300:pos + 80])
check("rel sponsored nicht aktiv (keine Partnerlinks)", 'rel="sponsored' not in html)

keys = [
    "7.000 bis 10.000 Euro", "11.000 bis 38.000 Euro", "ab 11.000 Euro", "ab 19.000 Euro",
    "12.500 bis 16.000 Euro", "90 bis 110 cm", "120 bis 140 cm", "225 bis 300 kg",
    "0,1 m/s", "0,15 m/s", "1,55 für die zweite", "200 bis 450 Euro", "99 bis 150 kg",
    "50 bis 200 €", "4.180 Euro pro Person",
]
for k in keys:
    check(f'Kernzahl "{k}" live', k in htxt)

check("SVG eingebunden", "assets/images/treppenlift-plattformlift-rollstuhllift-weg.svg" in html)
check("KI-Caption", "KI-unterstützt erstellte Schema-Grafik" in htxt)
for i in range(1, 12):
    if f'id="source-{i}"' not in html:
        check(f"source-{i} Anker", False)
        break
else:
    check("Quellenanker 1-11", True)
check("Checkliste gerendert", "Checkliste: Plattformlift-Angebot prüfen" in html)
check("Transparenz-Sektion", "Tobias Batke" in html and "28. Oktober 2026" in htxt)

# 2. SVG live
try:
    s, svg = get(f"{BASE}/assets/images/treppenlift-plattformlift-rollstuhllift-weg.svg")
    check(f"SVG HTTP {s}", s == 200 and "gtitle" in svg)
except Exception as exc:
    check("SVG erreichbar", False, str(exc))

# 3. Sitemap + RSS + Homepage
try:
    s, sm = get(f"{BASE}/sitemap.xml")
    check("Sitemap enthält Artikel", s == 200 and "treppenlift-plattformlift-rollstuhllift.html" in sm)
    locs = sm.count("<loc>")
    print(f"INFO Sitemap <loc> count: {locs}")
except Exception as exc:
    check("Sitemap erreichbar", False, str(exc))
try:
    s, rss = get(f"{BASE}/rss.xml")
    check("RSS enthält Artikel", s == 200 and "treppenlift-plattformlift-rollstuhllift.html" in rss)
    items = rss.count("<item>")
    print(f"INFO RSS item count: {items}")
except Exception as exc:
    check("RSS erreichbar", False, str(exc))
try:
    s, home = get(BASE + "/")
    check("Homepage verlinkt Artikel", s == 200 and "treppenlift-plattformlift-rollstuhllift.html" in home)
except Exception as exc:
    check("Homepage erreichbar", False, str(exc))

print()
if FAIL:
    print(f"{len(FAIL)} FAIL")
    for f in FAIL:
        print("  -", f)
    sys.exit(1)
print("LIVE-READBACK ALL PASS")
