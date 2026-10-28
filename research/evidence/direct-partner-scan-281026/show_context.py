#!/usr/bin/env python3
"""Kernaussagen der Scan-Seiten als Kontext-Schnipsel ausgeben."""
import pathlib

D = pathlib.Path(__file__).parent

def show(name, anchor, before=150, length=1200):
    t = (D / name).read_text(encoding="utf-8")
    i = t.find(anchor)
    print(f"=== {name} @ {anchor!r} ===")
    print(t[max(0, i - before):i + length] if i >= 0 else f"[anchor nicht gefunden] Anfang: {t[:1200]}")
    print()

show("adcell-hiro-lift.txt", "Was kann i", 0, 1000)
show("tke-partner.txt", "Als Online-Partner", 400, 1400)
show("100pp-hiro.txt", "Provisionsmodell", 200, 1500)
show("affmarketing-hiro.txt", "Stand:", 200, 1200)
show("lotse-100pp.txt", "Provisionen", 200, 900)
