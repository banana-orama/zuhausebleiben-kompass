#!/usr/bin/env python3
"""Print context windows around key passages for verbatim quote building."""
E = "research/evidence/aufmass-121126"

def window(name, center, before=2, after=6):
    lines = open(f"{E}/{name}.txt", encoding="utf-8").read().splitlines()
    lo, hi = max(0, center - before), min(len(lines), center + after)
    print(f"--- {name} [{lo}:{hi}] ---")
    for i in range(lo, hi):
        print(f"  {i}: {lines[i]}")

def grep_ctx(name, needle, before=1, after=5, limit=6):
    lines = open(f"{E}/{name}.txt", encoding="utf-8").read().splitlines()
    n = 0
    for i, ln in enumerate(lines):
        if needle.lower() in ln.lower():
            n += 1
            window(name, i, before, after)
            print()
            if n >= limit:
                break

print("=== VZ-Umfrage: Zahlenblöcke ===")
umf = open(f"{E}/vz-umfrage.txt", encoding="utf-8").read().splitlines()
for i, ln in enumerate(umf):
    if any(k in ln for k in ["unterschreiben", "Unterschreiben", "Planungsunterlagen", "Widerrufsrecht belehrt", "Geschäftsbedingungen"]):
        lo, hi = max(0, i-3), min(len(umf), i+10)
        for j in range(lo, hi):
            print(f"  {j}: {umf[j]}")
        print("  ...")

print()
print("=== ts-preise: Aufmaß/Lieferzeit-Sektion ===")
grep_ctx("ts-preise", "Aufmaß vor Ort", 3, 12, 3)
grep_ctx("ts-preise", "Lieferzeit", 2, 10, 3)

print()
print("=== lifta-haupt: Montagezeit / Termin / Bedenkzeit / widerrufbar ===")
grep_ctx("lifta-haupt", "Montagezeit auf einer geraden", 2, 8, 2)
grep_ctx("lifta-haupt", "tagesaktuell", 3, 6, 2)
grep_ctx("lifta-haupt", "Bedenkzeit", 4, 4, 2)
grep_ctx("lifta-haupt", "widerrufbar", 3, 4, 2)

print()
print("=== lifta-faq: Einbau-Dauer komplett ===")
grep_ctx("lifta-faq", "nur wenige Stunden", 2, 8, 2)

print()
print("=== chip: Rabatte-Absatz + Vor-Ort ===")
grep_ctx("chip", "Reputationsproblem", 1, 8, 2)

print()
print("=== baethe: Aufmaßservice-Satz ===")
grep_ctx("baethe", "Aufmaßservice", 2, 4, 2)

print()
print("=== vz-planung: Absatz um 309-314 ===")
window("vz-planung", 305, 1, 12)
window("vz-planung", 250, 2, 12)

print()
print("=== bgb-312g: Text ===")
print(open(f"{E}/bgb-312g.txt", encoding="utf-8").read()[:1600])

print()
print("=== hiro-haupt: Termin/Aufmaß-Treffer ===")
grep_ctx("hiro-haupt", "Termin", 1, 3, 8)
