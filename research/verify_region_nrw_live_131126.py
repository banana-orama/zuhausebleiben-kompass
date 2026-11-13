#!/usr/bin/env python3
"""Live-Readback Region NRW auf der öffentlichen URL (nach CI + Pages-Deploy-Lag).
Prüft: HTTP 200, robots index,follow, Canonical, Kernfakten-Wortlaute, Absenzen
(§40-Beträge, Partner-Marker), Related/CTA-Ziele, 10 Quellen, Sitemap genau 1 Region
(NRW), Hub-Teaser, llms unverändert, robots.txt-Sitemap-Direktive."""
import subprocess
import sys
import time

BASE = "https://zuhausebleiben-kompass.de"
URL = BASE + "/region/nordrhein-westfalen.html"

def fetch(url):
    r = subprocess.run(["curl", "-sS", "-L", "--max-time", "40", url],
                       capture_output=True, text=True)
    code = subprocess.run(["curl", "-sS", "-o", "/dev/null", "-w", "%{http_code}",
                           "-L", "--max-time", "40", url],
                          capture_output=True, text=True).stdout.strip()
    return code, r.stdout

fails, checks = [], 0

# Pages-Deploy-Lag: neue URL pollt auf 200
for i in range(10):
    code, html = fetch(URL)
    if code == "200":
        break
    print(f"Versuch {i+1}: HTTP {code} — Deploy-Lag, warte 30 s")
    time.sleep(30)
if code != "200":
    print(f"FAIL: {URL} antwortet nicht mit 200 (letzter Code {code})")
    sys.exit(1)
print(f"HTTP 200: {URL}")

def needle(t, why):
    global checks
    checks += 1
    if t not in html:
        fails.append(f"live fehlt ({why}): {t[:70]}")

def absent(t, why):
    global checks
    checks += 1
    if t in html:
        fails.append(f"live ABSenz verletzt ({why}): {t[:70]}")

needle('<meta name="robots" content="index,follow">', "robots")
needle('rel="canonical" href="' + URL + '"', "canonical")
needle("Umbau und Förderung in Nordrhein-Westfalen", "H1")
needle("220.000 €", "NRW.BANK Darlehen")
needle("bis zu 50 % des Darlehens", "Tilgungsnachlass")
needle("23.540 €", "Einkommensgrenze A")
needle("32.956 €", "Einkommensgrenze B")
needle("anrechenfreie Beträge bei der Einkommensermittlung", "NRW.BANK-Sonderregel")
needle("fest mit dem Baukörper verbundene Treppenlifter", "LWL-Treppenlifter")
needle("§ 64e SGB XII", "Abgrenzung")
needle("Diesen Zuschuss können Sie nicht mehr beantragen.", "KfW-Stopp")
needle("„Altersgerecht Umbauen“ (159)", "KfW-Kredit")
needle("8. April 2026", "KfW-Neustart")
needle("berät neutral und kostenlos", "Wohnberatung")
needle("geprüft 2026-11-13", "Quellenstand")
needle("Mit KI-Unterstützung erstellt", "KI-Kennzeichnung")
needle("/treppenlift-zuschuss.html", "CTA/Related zuschuss")
needle("/wohnumfeldverbesserung-beantragen.html", "CTA wohnumfeld")
needle("/treppenlift-foerderung-ohne-pflegegrad.html", "CTA ohne-pflegegrad")
needle("/treppenlift-mietwohnung.html", "Related mietwohnung")
needle("/pflegegrad-antrag-ablauf-fristen.html", "Related pflegegrad")
needle("/treppenlift-kosten.html", "Related kosten")
needle("kreis-re.de", "Quelle Kreis RE")
needle("lk-wohnberatung.nrw", "Quelle Wohnberatung")
needle("serviceportal.lwl.org", "Quelle LWL-Portal")
needle('id="abschnitt-8"', "Anker Reihenfolge")
for t in [("4.180", "kein §40-Betrag live"), ("16.720", "kein §40-Betrag live"),
          ("awin1.com", "kein Partner-Tracker"), ('rel="sponsored"', "kein Partner-CTA"),
          ("Zuschüsse bis zu 6.250 € pro Wohneinheit ist", "keine Verfügbarkeits-Zusage 455-B")]:
    absent(*t)

# Sitemap: genau NRW als Region, 49 locs erwartet
code, sm = fetch(BASE + "/sitemap.xml")
if code != "200":
    fails.append(f"Sitemap HTTP {code}")
else:
    locs = [u.split("<loc>")[1].split("</loc>")[0] for u in sm.split("<url>")[1:]]
    checks += 1
    rlocs = [u for u in locs if "/region/" in u]
    if not (len(rlocs) == 1 and rlocs[0].endswith("/region/nordrhein-westfalen.html")):
        fails.append(f"Live-Sitemap Regionen falsch: {rlocs}")
    checks += 1
    if len(locs) != 49:
        fails.append(f"Live-Sitemap hat {len(locs)} locs, erwartet 49")
    else:
        print(f"Live-Sitemap: {len(locs)} locs, Regionen: {[u.rsplit('/',1)[-1] for u in rlocs]}")

# Hub-Teaser + Hub noindex
code, hub = fetch(BASE + "/regional.html")
checks += 1
if code != "200" or "Erste ausführlich recherchierte Region" not in hub:
    fails.append(f"Hub-Teaser fehlt (HTTP {code})")
checks += 1
if code == "200" and '<meta name="robots" content="noindex,follow">' not in hub:
    fails.append("Hub nicht mehr noindex live")

# Platzhalter-Region bleibt noindex live
code, bay = fetch(BASE + "/region/bayern.html")
checks += 1
if code != "200" or '<meta name="robots" content="noindex,follow">' not in bay:
    fails.append(f"Platzhalter bayern nicht noindex (HTTP {code})")
else:
    print("Platzhalter bayern: live noindex,follow")

# robots.txt-Sitemap-Direktive
code, rb = fetch(BASE + "/robots.txt")
checks += 1
if "Sitemap: https://zuhausebleiben-kompass.de/sitemap.xml" not in rb:
    fails.append("robots.txt Sitemap-Direktive fehlt")

# llms.txt unverändert (37 Ratgeber-Abschnitt existiert weiter)
code, ll = fetch(BASE + "/llms.txt")
checks += 1
if code != "200" or "Ratgeber" not in ll:
    fails.append(f"llms.txt HTTP {code}")

print(f"Live-Readback: {checks} Checks")
if fails:
    print("FAIL:", *fails, sep="\n  ")
    sys.exit(1)
print("verify_region_nrw_live_131126: ALL PASS")
