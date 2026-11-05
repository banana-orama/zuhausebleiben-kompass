#!/usr/bin/env python3
"""Live-Readback Briefing 17: öffentliche URL nach CI-Deploy prüfen
(Commit/CI ist nicht Deployment — der Live-Abgleich zählt)."""
import re
import ssl
import urllib.request

BASE = "https://zuhausebleiben-kompass.de"
CTX = ssl.create_default_context()
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
FAIL = []


def check(label, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + label + ("" if cond else f"  {detail}"))
    if not cond:
        FAIL.append(label)


def get(path):
    req = urllib.request.Request(BASE + path, headers=UA)
    with urllib.request.urlopen(req, timeout=40, context=CTX) as r:
        return r.status, r.read().decode("utf-8", "replace")


st, html = get("/hausnotruf-kuendigen.html")
check("page 200", st == 200, str(st))
check("robots index,follow", 'name="robots" content="index,follow"' in html)
check("h1 correct", "Hausnotruf kündigen: Fristen, Wege und Sonderfälle" in html)
check("canonical", 'rel="canonical" href="https://zuhausebleiben-kompass.de/hausnotruf-kuendigen.html"' in html)
hay = re.sub(r"\s+", " ", html).lower()
for needle in ["14 tage", "27 euro", "zwei jahre", "verträge hier kündigen", "vertragspartner der pflegekasse",
               "zwölf monate und 14 tage"]:
    check(f"live needle: {needle}", needle in hay)
check("source §312k live", "gesetze-im-internet.de/bgb/__312k.html" in html)
check("related -> vergleich live", "hausnotruf-kosten-anbieter-vergleich.html" in html)
check("CTA compare_top live", 'data-cta-id="compare_top"' in html)
check("svg embedded live", "hausnotruf-kuendigen-wege.svg" in html)

st2, svg = get("/assets/images/hausnotruf-kuendigen-wege.svg")
check("svg 200", st2 == 200, str(st2))
check("svg fixed startband", "startband" in svg)

st3, sm = get("/sitemap.xml")
check("sitemap 200", st3 == 200, str(st3))
check("in sitemap", "hausnotruf-kuendigen.html" in sm)
st4, rss = get("/rss.xml")
check("rss item live", "hausnotruf-kuendigen" in rss)
st5, llms = get("/llms.txt")
check("llms entry live", "/hausnotruf-kuendigen.html" in llms)

print()
print(f"RESULT: {'ALL PASS' if not FAIL else f'{len(FAIL)} FAILS: {FAIL}'}")
raise SystemExit(1 if FAIL else 0)
