#!/usr/bin/env python3
"""TKE-Affiliate-Abschnitt, Lotse-Netzwerk, FITAL-Kontaktdaten-Modell, Handicare-Einstufung."""
import pathlib

D = pathlib.Path(__file__).parent

def ctx(name, needle, before=100, length=1100, label=None):
    t = (D / name).read_text(encoding="utf-8")
    i = t.find(needle)
    print(f"=== {label or name} @ {needle!r} ===")
    print(t[max(0, i - before):i + length] if i >= 0 else "[nicht gefunden]")
    print()

ctx("tke-partner.txt", "Online-Partner", 300, 1500, "TKE Affiliate")
ctx("tke-partner.txt", "MobilPartner", 200, 900, "TKE MobilPartner")
ctx("lotse-100pp.txt", "Netzwerk direkt", 400, 700, "Lotse Netzwerk")
ctx("fital-partner.txt", "Sie entscheiden", 300, 900, "FITAL Kontaktmodell")
ctx("handicare-partner.txt", "Partner Portal", 300, 800, "Handicare")
ctx("acorn-partnerportal.txt", "Registrieren", 200, 800, "Acorn")
ctx("aroundhome-affiliate.txt", "30-50%", 300, 900, "Aroundhome Share")
