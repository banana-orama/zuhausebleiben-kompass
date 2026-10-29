#!/usr/bin/env python3
"""Live-Readback 291026 Link-Rot-Audit: oeffentliche URL nach Deploy pruefen."""
import subprocess, sys, json

BASE = "https://zuhausebleiben-kompass.de"
checks = []

def fetch(path):
    r = subprocess.run(
        ["curl", "-sS", "-L", "--max-time", "30", f"{BASE}{path}"],
        capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""

def check(name, ok, detail=""):
    checks.append((name, ok, detail))
    print(("PASS " if ok else "FAIL ") + name + (("  | " + detail) if detail else ""))

# 1) Hausnotruf-Seite: neue VZ-URL da, alte weg
html = fetch("/hausnotruf-kosten-anbieter-vergleich.html")
check("H1 seite 200+nichtleer", len(html) > 5000, f"{len(html)} bytes")
check("H2 neue VZ-URL 22947 im HTML", "vertraege-wirksam-widerrufen-per-email-sms-oder-fax" in html)
check("H3 alte VZ-URL 70049 entfernt", "widerruf-vertraege-rueckgaengig-machen-70049" not in html)
check("H4 neuer Quellen-Titel im HTML", "Verträge wirksam widerrufen" in html)

# 2) Nachbarn unveraendert und erreichbar
for slug, needle in [
    ("treppenlift-mietwohnung", "woeigg/__20.html"),
    ("hilfsmittel-dusch-wc-uebernahme", "rehadat-gkv.de/produkt"),
]:
    h = fetch(f"/{slug}.html")
    check(f"X {slug} 200+nichtleer", len(h) > 5000, f"{len(h)} bytes")
    check(f"X {slug} Zitat-URL da", needle in h)

# 3) Sitemap/RSS weiterhin konsistent
sm = fetch("/sitemap.xml")
check("S sitemap enthaelt hausnotruf", "hausnotruf-kosten-anbieter-vergleich" in sm)
check("S sitemap 48 locs", sm.count("<loc>") == 48, f"{sm.count('<loc>')}")

fails = [c for c in checks if not c[1]]
print(f"\n{len(checks)-len(fails)}/{len(checks)} PASS")
sys.exit(1 if fails else 0)
