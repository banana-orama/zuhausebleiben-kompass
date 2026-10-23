#!/usr/bin/env python3
"""Verifiziert: jedes Ledger-Zitat kommt verbatim im zugehörigen Evidence-Extrakt vor."""
import json, pathlib, sys

ROOT = pathlib.Path("/Users/mac/agentic-business/barrierefrei-leads/research")
ledger = json.loads((ROOT / "partner-scan-231026-ledger.json").read_text(encoding="utf-8"))
EVID = ROOT / "evidence" / "partner-scan-231026"

URL2FILE = {
    "https://ui.awin.com/merchant-profile/112616": "awin-malteser-112616.txt",
    "https://ui.awin.com/merchant-profile/40988": "awin-lifta-40988.txt",
    "https://www.adcell.de/partnerprogramme/pflegehase-hausnotruf": "adcell-pflegehase-hausnotruf.txt",
    "https://www.adcell.de/partnerprogramme/pflegehase": "adcell-pflegehase.txt",
    "https://www.adcell.de/affiliates": "adcell-affiliates.txt",
    "https://www.affiliate-marketing.de/partnerprogramme/pflegehase.de": "affmarketing-pflegehase.txt",
    "https://www.affiliate-marketing.de/partnerprogramme/treppenlift-angebotsvergleich.de": "affmarketing-treppenlift-angebotsvergleich.txt",
    "https://www.affilitizer.com/programs/smartversorgt.de": "affilitizer-smartversorgt.txt",
    "https://addrevenue.io/app/advertisers/details/988118": "addrevenue-988118.txt",
    "https://www.hausnotruf.de/partnerprogramm/": "hausnotruf-de-partner.txt",
    "https://partner.treppenlifter.me/": "treppenlift-me.txt",
    "https://de.acornaffiliate.com/": "acorn-de.txt",
    "https://affi.io/m/libify": "affi-libify.txt",
    "https://www.100partnerprogramme.de/p/libify-de-20248/": "100pp-libify.txt",
    "https://pflegehase.de/": "pflegehase-home.txt",
    "https://pflegehase.de/hausnotruf/": "pflegehase-hausnotruf-page.txt",
}

total = ok = 0
fails = []
for src in ledger["sources"]:
    fname = URL2FILE.get(src["url"])
    if not fname:
        fails.append(f"KEINE EVIDENCE-MAPPING: {src['url']}")
        continue
    body = (EVID / fname).read_text(encoding="utf-8")
    body_norm = " ".join(
        body.replace("&nbsp;", " ").replace("&#216;", "ø").replace("&amp;", "&").split()
    )
    for q in src["quotes"]:
        total += 1
        q_norm = " ".join(q["text"].split())
        if q_norm in body_norm:
            ok += 1
        else:
            fails.append(f"[{src['id']}] NICHT VERBATIM in {fname}: {q['text'][:80]}")

print(f"{ok}/{total} Zitate verbatim verifiziert")
for f in fails:
    print("FAIL:", f)
sys.exit(1 if fails else 0)
