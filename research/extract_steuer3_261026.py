#!/usr/bin/env python3
"""Remainder of § 35a Abs. 5 verbatim + VZ site search via HTTP."""
import pathlib, re, urllib.request

t = pathlib.Path("research/evidence/steuer-261026/estg__35a.txt").read_text(encoding="utf-8")
i = t.find("eine Rechnung erhalten hat")
print("### Abs. 5 Satz 3 komplett:")
print(re.sub(r"\s+", " ", t[i:i+420]))
print()

url = "https://www.verbraucherzentrale.de/suche?q=Handwerkerleistungen"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"})
try:
    with urllib.request.urlopen(req, timeout=40) as r:
        raw = r.read().decode("utf-8", "replace")
    print("search page HTTP 200,", len(raw), "bytes")
    for m in re.finditer(r'href="(/wissen/[^"]+|https://www\.verbraucherzentrale\.de/wissen/[^"]+)"[^>]*>([^<]{10,120})<', raw):
        href, txt = m.group(1), re.sub(r"\s+", " ", m.group(2)).strip()
        if "steuer" in txt.lower() or "handwerker" in txt.lower() or "belastung" in txt.lower():
            print("-", txt, "→", href)
except Exception as e:
    print("VZ search failed:", repr(e))
