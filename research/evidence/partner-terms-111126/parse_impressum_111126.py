#!/usr/bin/env python3
"""Parse impressum pages of Treppenlift-Lotse and Treppenlift-Zentrum (11.11.2026)."""
import re
from html import unescape

D = "research/evidence/partner-terms-111126"

def text(p):
    raw = open(p, encoding="utf-8", errors="replace").read()
    raw = re.sub(r"<script[^>]*>.*?</script>", "", raw, flags=re.S)
    raw = re.sub(r"<style[^>]*>.*?</style>", "", raw, flags=re.S)
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", raw)))

for f in ["lotse_impressum", "zentrum_impressum"]:
    try:
        t = text(f"{D}/{f}.html")
    except FileNotFoundError:
        print(f"== {f} == MISSING")
        continue
    i = max(t.find("Impressum"), 0)
    print(f"== {f} ==")
    print(t[i:i + 1000])
    print()
