#!/usr/bin/env python3
"""Locate candidate verbatim quotes for briefing 13 ledger (Aussenlift). Prints exact context windows from saved evidence."""
import pathlib, re

E = pathlib.Path("research/evidence/aussenlift-271026")
NEEDLES = {
    "tlw-aussenlift": ["4.000", "IP", "Frost", "Akku", "Batterie", "Abdeck", "Temperatur", "Untergrund", "Salz", "gebrauch", "kosten", "3.500"],
    "personenaufzuege-aussen": ["Aufschlag", "gedichtet", "Abdeckhaube", "Beschichtung", "Korrosion", "Material"],
    "trep-preise-aussen": ["etwas über", "dasselbe", "100–250", "40 Prozent", "Untergrund", "Stromzuführung", "Fundament", "Vereiste", "kein Luxus", "Outdoo"],
    "seniorenrat-aussen": ["3.500–6.500", "IP-Schutzklasse", "Edelstahl", "Abdeck", "rost", "4.180"],
    "hiro-aussen": ["wasserdicht", "Sturm", "100 %", "160 AIR", "Abdeck", "Abdeckung", "Wartung"],
    "lifta-aussenlifte": ["Abschließbar", "Schutzhaube", "UV-beständig", "Gekapselte", "Versiegelte", "Alu-Schiene", "Abdeckung", "GTL", "Fernbedienung", "Schloss"],
    "lifta-treppenlift": ["GTL 320", "extremer Kälte"],
    "lifta-faq": ["Gerade Treppe, Treppenlift außen", "inklusive Einbau"],
    "vz-planung": ["Wartungsverträgen", "Hilfsmittel-Börse", "3.500 und 15.000", "Rechnungen", "mehrere Angebote"],
}

def window(txt, needle, before=80, after=420):
    out = []
    start = 0
    low = txt.lower()
    n = needle.lower()
    while True:
        idx = low.find(n, start)
        if idx < 0:
            break
        out.append(txt[max(0, idx - before):idx + after].replace("\n", " "))
        start = idx + len(n)
        if len(out) >= 3:
            break
    return out

for name, needles in NEEDLES.items():
    p = E / f"{name}.txt"
    if not p.exists():
        print(f"## {name}: MISSING")
        continue
    txt = p.read_text(encoding="utf-8")
    print(f"\n===== {name} =====")
    for needle in needles:
        wins = window(txt, needle)
        if not wins:
            print(f"  -- [{needle}] NOT FOUND")
            continue
        for i, w in enumerate(wins):
            print(f"  -- [{needle}] #{i}: {w[:500]}")
print("\nDONE")
