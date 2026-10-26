#!/usr/bin/env python3
"""Extract the load-bearing sentences from the fetched § 35a / § 33 EStG evidence text."""
import pathlib, re

d = pathlib.Path("research/evidence/steuer-261026")
t35a = (d / "estg__35a.txt").read_text(encoding="utf-8")
t33 = (d / "estg__33.txt").read_text(encoding="utf-8")

print("### 35a Abs-2 und Abs-3 Kernsätze")
for m in re.finditer(r"(20 Prozent, höchstens\s?[\d\s\xa0\u00a0]+?Euro)", t35a):
    s = max(0, m.start() - 260)
    print("—", re.sub(r"\s+", " ", t35a[s:m.end() + 40]).strip()[:420])
    print()

print("### 35a Abs. 3 vollständiger Anfang (Handwerkerleistungen)")
i = t35a.find("(3)")
print(re.sub(r"\s+", " ", t35a[i:i+1100]))

print()
print("### 35a Abs. 3 Formulierung 'Erhaltung'/'Renovierung'")
for kw in ["Renovierungs", "Erhaltung", "Anpassung"]:
    j = t35a.find(kw)
    if j >= 0:
        print(kw, "→", re.sub(r"\s+", " ", t35a[j-120:j+260]))

print()
print("### 33 Abs. 3 zumutbare Belastung (Prozentsätze)")
i = t33.find("(3)")
print(re.sub(r"\s+", " ", t33[i:i+1500]))
