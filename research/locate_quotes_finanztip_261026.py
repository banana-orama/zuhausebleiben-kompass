#!/usr/bin/env python3
"""Locate candidate verbatim sentences in finanztip evidence for the ledger."""
import pathlib, re

d = pathlib.Path("research/evidence/steuer-261026")

def sentences(path):
    t = re.sub(r"\s+", " ", path.read_text(encoding="utf-8"))
    # crude sentence split on .!? followed by space+capital
    parts = re.split(r"(?<=[.!?])\s+(?=[A-ZÄÖÜ„“])", t)
    return [p.strip() for p in parts if 40 < len(p.strip()) < 600]

def find(path, kws, label):
    print(f"===== {label} ({path.name})")
    seen = set()
    for s in sentences(path):
        low = s.lower()
        if any(k in low for k in kws) and s not in seen:
            seen.add(s)
            print("·", s[:420])
            print()

find(d / "finanztip-handwerkerkosten.txt",
     ["20 %", "1.200", "arbeitskosten", "materialkosten", "rechnung", "überweis", "unbar",
      "kfW", "gefördert", "treppenlift", "höchstbetrag", "ergebnisrechnung"],
     "Handwerkerkosten")
find(d / "finanztip-aussergewoehnliche-belastungen.txt",
     ["zumutbare belastung", "arzt", "attest", "verordnung", "pflegekasse", "pflegegrad",
      "hilfsmittel", "treppenlift", "1 %", "5 %", "7 %", "aufbewahr"],
     "Außergewöhnliche Belastungen")
