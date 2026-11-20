#!/usr/bin/env python3
"""Live-Readback dist-Clean-Commit 5a18bf9 (20.11.): Regressionsscope, kein Content-Change."""
import re, subprocess, sys, time

BASE = "https://zuhausebleiben-kompass.de"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
fails = []

def check(name, ok, detail=""):
    print(("PASS" if ok else "FAIL"), name, detail)
    if not ok:
        fails.append(name)

def fetch(path):
    r = subprocess.run(["curl", "-sS", "-A", UA, "-w", "\n%{http_code}", BASE + path],
                       capture_output=True, text=True, timeout=45)
    body, _, code = r.stdout.rpartition("\n")
    return code.strip(), body

# Deploy-Lag abwarten: neuer Build kann kurz 404/alt bleiben; poll auf Homepage 200.
for attempt in range(1, 13):
    code, home = fetch("/")
    print(f"Homepage poll {attempt}: {code}")
    if code == "200":
        break
    time.sleep(40)

check("Homepage 200", code == "200")
check("Homepage robots index,follow", 'name="robots" content="index,follow"' in home)
check("Homepage listet paare-Ratgeber", "Hausnotruf für Paare" in home)

code_sm, sm = fetch("/sitemap.xml")
locs = sm.count("<loc>")
check("Sitemap 200", code_sm == "200")
check(f"Sitemap exakt 53 locs (ist {locs})", locs == 53)
check("Sitemap enthält paare", "hausnotruf-fuer-paare.html" in sm)
check("Sitemap enthält Checklisten", "/checklisten/" in sm)
check("Sitemap ohne noindex-Regionen", "/region/schleswig-holstein.html" not in sm)

code_rss, rss = fetch("/rss.xml")
items = rss.count("<item>")
check(f"RSS 200 mit 40 Items (ist {items})", code_rss == "200" and items == 40)

code_pa, paare = fetch("/hausnotruf-fuer-paare.html")
check("paare-Artikel 200", code_pa == "200")
check("paare robots index,follow", 'name="robots" content="index,follow"' in paare)
check("paare Johanniter-Satz [7] live", "Johanniter" in paare)
check("paare 27,00 EUR live", "27,00 EUR" in paare)

for path, label in [("/treppenlift-zuschuss.html", "Money-Page"),
                    ("/checklisten/index.html", "Checklisten-Hub"),
                    ("/datenschutz.html", "Datenschutz"),
                    ("/region/nordrhein-westfalen.html", "Region NRW"),
                    ("/indexnow-key.txt", "IndexNow-Key")]:
    c, body = fetch(path)
    check(f"{label} 200", c == "200", f"({c})")

code_r, robots = fetch("/robots.txt")
check("robots.txt mit Sitemap-Direktive", code_r == "200" and "Sitemap:" in robots)

print(f"\n{'ALL PASS' if not fails else str(len(fails)) + ' FAILS: ' + ', '.join(fails)}")
sys.exit(1 if fails else 0)
