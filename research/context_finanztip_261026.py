#!/usr/bin/env python3
"""Context around the 900-Euro sentence + KfW passage in finanztip handwerkerkosten."""
import pathlib, re

t = re.sub(r"\s+", " ", pathlib.Path("research/evidence/steuer-261026/finanztip-handwerkerkosten.txt").read_text(encoding="utf-8"))

for kw in ["900 Euro", "öffentlichen Hand", "KfW", "zinsverbilligt"]:
    for m in list(re.finditer(kw, t))[:3]:
        print(f"### Kontext '{kw}':")
        print("…", t[max(0, m.start()-700):m.start()+700], "…")
        print()
