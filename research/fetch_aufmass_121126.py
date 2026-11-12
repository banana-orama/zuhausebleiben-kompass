#!/usr/bin/env python3
"""Fetch source pages for the Aufmass-Termin batch (B25). Saves raw HTML evidence."""
import subprocess, sys, os

E = "research/evidence/aufmass-121126"
os.makedirs(E, exist_ok=True)
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"

TARGETS = [
    ("vz-planung", "https://verbraucherzentrale.de/wissen/gesundheit-pflege/pflege-zu-hause/treppenlifte-das-muessen-sie-ueber-planung-umsetzung-wissen-10711"),
    ("ts-preise", "https://ts-treppenlifte.de/preise-kosten/"),
    ("baethe", "https://baethe.de/treppenlift"),
    ("chip", "https://unternehmen.chip.de/digitale-treppenlift-beratung.html"),
    ("hiro-termin", "https://www.hiro.de/treppenlift/termin-vereinbaren"),
    ("lifta-ablauf", "https://www.lifta.de/treppenlift/ablauf"),
]

for name, url in TARGETS:
    out = f"{E}/{name}.html"
    try:
        r = subprocess.run(
            ["curl", "-sL", "-A", UA, "-m", "30", url, "-o", out, "-w", "%{http_code} %{size_download}"],
            capture_output=True, text=True, timeout=40)
        print(f"{name}: {r.stdout.strip()}  {url}")
    except Exception as exc:
        print(f"{name}: ERROR {exc}")

# Find the VZ Umfrage URL from the unserioese ledger (same primary source, re-verify today)
import json
try:
    d = json.load(open("research/unserioese-101126-ledger.json"))
    srcs = d.get("sources", d if isinstance(d, list) else [])
    for s in srcs:
        u = str(s.get("url", ""))
        t = str(s.get("title", ""))
        if "umfrage" in u.lower() or "umfrage" in t.lower() or "2020" in u:
            print("UMFRAGE-LEDGER:", u, "|", t[:90])
except Exception as exc:
    print("ledger read error:", exc)
