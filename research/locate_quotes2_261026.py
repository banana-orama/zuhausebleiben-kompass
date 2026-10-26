#!/usr/bin/env python3
"""Exact verbatim sentences for the steuer ledger (whitespace-normalized prints)."""
import pathlib, re

d = pathlib.Path("research/evidence/steuer-261026")

def norm(p):
    t = p.read_text(encoding="utf-8").replace("\u00ad", "")
    return re.sub(r"\s+", " ", t)

fk = norm(d / "finanztip-handwerkerkosten.txt")
fa = norm(d / "finanztip-aussergewoehnliche-belastungen.txt")

needles_fk = [
    "Anlage Haushaltsnahe Aufwendungen",
    "Werkstatt entfällt",
    "Nebenkostenabrechnung Posten",
    "Die schriftliche Rechnung",
    "Juli 2026",
    "Höchstbetrag ist haushaltsbezogen",
    "Mieter Handwerkerleistungen",
    "Kombination",
]
for n in needles_fk:
    i = fk.find(n)
    print(f"### [{n}] → {'NOT FOUND' if i<0 else ''}")
    if i >= 0:
        print("   ", fk[max(0,i-160):i+340])
print()
needles_fa = [
    "zumutbare Belastung überschreiten",
    "nicht erstattet bekommst",
    "Paragraf 64",
    "Hilfsmittel müssen",
]
for n in needles_fa:
    i = fa.find(n)
    print(f"### FA[{n}] → {'NOT FOUND' if i<0 else ''}")
    if i >= 0:
        print("   ", fa[max(0,i-200):i+300])
