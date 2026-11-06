#!/usr/bin/env python3
"""Kontextfenster aus den ADCELL-Textextrakten (06.11.2026)."""
import re
import sys
from pathlib import Path

BASE = Path(__file__).parent
QUERIES = {
    "hiro-lift-061126.txt": ["Provisionsbedingungen", "Bedingung", "SEM", "incenti", "Werbe", "Beschreibung", "Zielgruppe"],
    "pflegehase-hausnotruf-061126.txt": ["Provisionsbedingungen", "Bedingung", "SEM", "incenti", "Beschreibung", "Zielgruppe", "Werbemittel"],
    "adcell-affiliates-061126.txt": ["Registrieren", "Content, Blog", "Joint", "kontroll", "AGB"],
}
WIN = 300

for fname, keys in QUERIES.items():
    p = BASE / fname
    if not p.exists():
        print(f"FEHLT: {fname}")
        continue
    t = p.read_text(encoding="utf-8")
    print(f"######## {fname} ({len(t)} chars)")
    for k in keys:
        seen = []
        for m in re.finditer(re.escape(k), t, flags=re.I):
            s, e = max(0, m.start() - 90), min(len(t), m.end() + WIN)
            frag = t[s:e]
            if not any(frag[40:120] in x for x in seen):
                seen.append(frag)
            if len(seen) >= 3:
                break
        for i, frag in enumerate(seen):
            print(f"--[{k}#{i+1}]-- …{frag}…")
    print()
