#!/usr/bin/env python3
"""Pull exact fixed-window snippets from evidence txt for handcrafting ledger quotes."""
import pathlib
import re

EVID = pathlib.Path(__file__).resolve().parent / "evidence" / "sitzsteh-061126"

def text(name: str) -> str:
    t = (EVID / f"{name}-061126.txt").read_text(encoding="utf-8")
    return re.sub(r"\s+", " ", t)

QUERIES = [
    ("lifta-stehlift", "auf einer kleinen Plattform stehend befördert", 40, 220),
    ("lifta-stehlift", "reine Anlehnlifte", 40, 300),
    ("lifta-stehlift", "ist eine Mischform", 120, 300),
    ("lifta-stehlift", "ähnlich wie bei einem Barhocker", 40, 260),
    ("lifta-stehlift", "Gelenke nicht gänzlich beugen", 160, 120),
    ("lifta-stehlift", "insbesondere für Menschen konzipiert", 20, 320),
    ("lifta-stehlift", "Mindestbreite von 80 cm", 180, 160),
    ("lifta-stehlift", "praktisch hochklappen", 140, 220),
    ("lifta-stehlift", "Transport von Personen mit Rollstuhl geeignet", 40, 220),
    ("lifta-stehlift", "Senkrechtlifte die bessere Option", 20, 220),
    ("lifta-stehlift", "rutschfesten Material", 220, 140),
    ("lifta-stehlift", "stabile Plattform aufsteigen", 160, 120),
    ("lifta-sitzlifte", "allermeisten Fällen ein Sitzlift gemeint", 60, 200),
    ("lifta-sitzlifte", "gängigste Art von Treppenlift", 60, 220),
    ("lifta-sitzlifte", "eigenständig auf dem Sitz Platz nehmen", 120, 100),
    ("lifta-sitzlifte", "Umstieg deutlich schwieriger", 100, 300),
    ("lifta-sitzlifte", "Bedienfeld", 200, 140),
    ("lifta-sitzlifte", "über eine Fernbedienung", 40, 220),
    ("lifta-sitzlifte", "entweder mit Strom oder per Akku", 60, 220),
    ("lifta-sitzlifte", "Gurt an", 120, 140),
    ("hiro", "Produktlinie HIRO 160", 60, 200),
    ("hiro-preise", "maßgeblich von der Treppenform", 80, 260),
    ("hiro-preise", "beginnen die Preise bei etwa 4.000", 80, 200),
    ("hiro-preise", "kurvig oder über mehrere Stockwerke", 60, 120),
    ("hiro-preise", "Sitzlifte sind kostengünstiger", 60, 220),
    ("hiro-preise", "Beratung, Planung, Maßanfertigung", 80, 200),
    ("vz", "14-tägiges Widerrufsrecht", 160, 60),
    ("vz", "Werkvertrag anzusehen", 120, 140),
    ("vz", "nachdem der Antrag bewilligt wurde", 100, 140),
    ("rtl", "Mindestens 55 cm", 100, 160),
    ("rtl", "ohne Gewähr", 60, 40),
    ("tlw", "nicht seriös beziffern", 140, 60),
    ("tlw", "Treppenform den Preis stärker", 80, 200),
]

t_cache = {}
for name, needle, back, fwd in QUERIES:
    if name not in t_cache:
        t_cache[name] = text(name)
    t = t_cache[name]
    i = t.find(needle)
    if i < 0:
        print(f"[{name}] NICHT GEFUNDEN: {needle}")
    else:
        s = max(0, i - back)
        print(f"[{name}] …{t[s:i + fwd]}…")
    print()
