#!/usr/bin/env python3
"""Extract 632a text + print B24 article JSON schema and renderer integration points."""
import re, html as htmllib

E = "research/evidence/aufmass-131126"
raw = open(f"{E}/bgb-632a.html", encoding="utf-8", errors="replace").read()
raw = re.sub(r"<[^>]+>", "\n", raw)
raw = htmllib.unescape(raw)
lines = [re.sub(r"\s+", " ", ln).strip() for ln in raw.splitlines()]
lines = [ln for ln in lines if ln]
print("=== § 632a BGB ===")
for ln in lines[:30]:
    print(ln[:200])
