#!/usr/bin/env python3
"""Extract § 35a Abs. 5 (Nachweis/Zahlung) + Abs. 2 Satz 2 (Heim) from saved evidence."""
import pathlib, re

t = pathlib.Path("research/evidence/steuer-261026/estg__35a.txt").read_text(encoding="utf-8")
i = t.find("(5)")
print("### Abs. 5:")
print(re.sub(r"\s+", " ", t[i:i+700]))
print()
i2 = t.find("(2)")
seg = t[i2:i2+900]
j = seg.find("Heim")
print("### Abs. 2 Kontext Heim (falls vorhanden):")
print(re.sub(r"\s+", " ", seg[j-300:j+220]) if j >= 0 else "kein 'Heim' in Abs. 2")
