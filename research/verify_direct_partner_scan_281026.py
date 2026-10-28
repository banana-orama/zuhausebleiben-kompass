#!/usr/bin/env python3
"""Verifiziert: jedes Ledger-Zitat kommt verbatim im zugehörigen Evidence-Extrakt vor.
Zusätzlich 2 Abwesenheits-Checks (keine €/EUR/Euro-Angabe) für TKE + X4d."""
import json, pathlib, sys

ROOT = pathlib.Path("/Users/mac/agentic-business/barrierefrei-leads/research")
ledger = json.loads((ROOT / "direct-partner-scan-281026-ledger.json").read_text(encoding="utf-8"))
EVID = ROOT / "evidence" / "direct-partner-scan-281026"

URL2FILE = {
    "https://www.adcell.de/partnerprogramme/hiro-lift": "adcell-hiro-lift.txt",
    "https://hiro.de/affiliate/": "hiro-affiliate.txt",
    "https://www.tke-homesolutions.de/preise/partner/": "tke-partner.txt",
    "https://www.affiliate-marketing.de/partnerprogramme/hiro.de": "affmarketing-hiro.txt",
    "https://www.100partnerprogramme.de/p/hiro/": "100pp-hiro.txt",
    "https://www.100partnerprogramme.de/p/treppenlift-zentrum-de-18014/": "lotse-100pp.txt",
    "https://www.fital-treppenlifte.de/partner.html": "fital-partner.txt",
    "https://handicare-treppenlifte.de/ueber-handicare/handicare-partner/": "handicare-partner.txt",
    "https://de.acornpartner.com/": "acorn-partnerportal.txt",
    "https://www.aroundhome.de/affiliateprogramm/": "aroundhome-affiliate.txt",
    "https://www.x4d.de/treppenlift-partnerprogramm": "x4d-partner.txt",
    "https://www.affiliate-marketing.de/partnerprogramme/treppenlift-angebot.de": "affmarketing-liftstar.txt",
}

total = ok = 0
fails = []
for src in ledger["sources"]:
    fname = URL2FILE.get(src["url"])
    if not fname:
        fails.append(f"KEINE EVIDENCE-MAPPING: {src['url']}")
        continue
    body = (EVID / fname).read_text(encoding="utf-8")
    body_norm = " ".join(body.split())
    for q in src["quotes"]:
        total += 1
        q_norm = " ".join(q["text"].split())
        if q_norm in body_norm:
            ok += 1
        else:
            fails.append(f"[{src['id']}] NICHT VERBATIM in {fname}: {q['text'][:80]}")

# Abwesenheits-Checks: TKE + X4d nennen keine Verguetungshoehe in Euro
for fname in ("tke-partner.txt", "x4d-partner.txt"):
    body = (EVID / fname).read_text(encoding="utf-8")
    hits = sum(body.count(tok) for tok in ("€", "EUR", "Euro", "euro"))
    if hits == 0:
        print(f"ABSENZ OK: {fname} enthaelt keine Euro-Angabe (Verguetung nicht oeffentlich belegt)")
    else:
        fails.append(f"ABSENZ FAIL: {fname} enthaelt {hits} Euro-Tokens - Pruefung anpassen")

print(f"{ok}/{total} Zitate verbatim verifiziert")
for f in fails:
    print("FAIL:", f)
sys.exit(1 if fails else 0)
