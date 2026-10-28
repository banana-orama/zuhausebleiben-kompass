#!/usr/bin/env python3
"""Quote-Verifikation vorab: alle Ledger-Kandidaten als Kontext-Schnipsel ausgeben."""
import pathlib

D = pathlib.Path(__file__).parent

def ctx(name, needle, before=60, length=420):
    t = (D / name).read_text(encoding="utf-8")
    i = t.find(needle)
    print(f"--- {name} @ {needle[:45]!r} -> {'OK' if i >= 0 else 'FEHLT'}")
    if i >= 0:
        print(t[max(0, i - before):i + length])
    print()

ctx("affmarketing-liftstar.txt", "60,00")
ctx("affmarketing-liftstar.txt", "keine Partnerprogramme")
ctx("affmarketing-liftstar.txt", "15.000")
ctx("affmarketing-hiro.txt", "Stand:")
ctx("acorn-partnerportal.txt", "Rechnung an ACORN")
ctx("fital-partner.txt", "erkenntlich")
ctx("aroundhome-affiliate.txt", "zwischen 30-50%")
ctx("tke-partner.txt", "Online-Partner im Rahmen", 80, 380)
