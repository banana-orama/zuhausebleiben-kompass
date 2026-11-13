#!/usr/bin/env python3
"""Verbatim-Gate: jede Ledger-Quote muss in ihrer Evidence-Datei stehen.
Normalisierung: lowercase, Whitespace kollabieren, Soft-Hyphen (\u00ad) und
Zero-Width-Zeichen entfernen (KfW-Seiten verwenden weiche Trennstriche)."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "research/region-nrw-131126-ledger.json"
EV = ROOT / "research/evidence/region-nrw-131126"

def norm(s):
    s = s.replace("\u00ad", "").replace("\u200b", "").replace("\ufeff", "")
    s = s.lower()
    s = re.sub(r"\s+", " ", s)
    return s

fails, passes = [], 0
ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
for src in ledger["sources"]:
    path = EV / src["evidence"]
    if not path.exists():
        fails.append(f"Quelle {src['id']}: Evidence-Datei fehlt: {path.name}")
        continue
    hay = norm(path.read_text(encoding="utf-8", errors="replace"))
    for q in src.get("quotes", []):
        if norm(q) in hay:
            passes += 1
        else:
            fails.append(f"Quelle {src['id']} ({src['evidence']}): Zitat nicht verbatim: {q[:80]}…")
    for n in src.get("needles", []):
        if norm(n) in hay:
            passes += 1
        else:
            fails.append(f"Quelle {src['id']} ({src['evidence']}): Needle nicht gefunden: {n}")

print(f"region-nrw-131126 Ledger: {passes} Pässe über {len(ledger['sources'])} Quellen")
if fails:
    print("FAIL:", *fails, sep="\n  ")
    sys.exit(1)
print("verify_region_nrw_131126: ALL PASS")
