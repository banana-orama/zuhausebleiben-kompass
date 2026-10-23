#!/usr/bin/env python3
"""Verifiziert: jedes Ledger-Zitat kommt verbatim (whitespace-normalisiert) im zugehörigen
Evidence-Extrakt in research/evidence/partner-scan-badumbau-231026/ vor."""
import json, pathlib, re, sys

ROOT = pathlib.Path("/Users/mac/agentic-business/barrierefrei-leads/research")
ledger = json.loads((ROOT / "partner-scan-badumbau-231026-ledger.json").read_text(encoding="utf-8"))
EVID = ROOT / "evidence" / "partner-scan-badumbau-231026"

URL2FILE = {
    "https://ui.awin.com/merchant-profile/68536": "awin-aroundhome-68536.txt",
    "https://www.aroundhome.de/badezimmer/": "aroundhome-badezimmer.txt",
    "https://www.aroundhome.de/": "aroundhome-home.txt",
    "https://badumbauheld.de/partner-werden": "badumbauheld-partner.txt",
    "https://seniovo.de/partner/": "seniovo-partner.txt",
    "https://app.hienergy.ai/a/aroundhome-de-hienergy-awin": "hienergy-aroundhome-awin.txt",
    "https://aaa.aroundhome.de/privacy-optout.do": "aroundhome-triplea.txt",
    "https://ewerle-gmbh.de/ratgeber/leadportale-handwerk-vergleich": "ewerle-leadportale.txt",
}

norm = lambda s: re.sub(r"\s+", " ", s).strip()

total = ok = 0
fails = []
for src in ledger["sources"]:
    fname = URL2FILE.get(src["url"])
    if not fname or not (EVID / fname).exists():
        fails.append((src["id"], src["url"], "EVIDENCE-FEHLT"))
        continue
    text = norm((EVID / fname).read_text(errors="ignore"))
    for q in src["quotes"]:
        total += 1
        if norm(q["text"]) in text:
            ok += 1
        else:
            fails.append((src["id"], src["url"], q["text"][:90]))

print(f"Zitate: {ok}/{total} verbatim verifiziert ({ledger['scan']})")
for f in fails:
    print("FAIL:", f)
sys.exit(1 if fails else 0)
