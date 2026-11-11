#!/usr/bin/env python3
"""Extract key term passages from partner-term evidence pages (11.11.2026)."""
import re
from html import unescape

D = "research/evidence/partner-terms-111126"

def text(p):
    raw = open(p, encoding="utf-8", errors="replace").read()
    raw = re.sub(r"<script[^>]*>.*?</script>", "", raw, flags=re.S)
    raw = re.sub(r"<style[^>]*>.*?</style>", "", raw, flags=re.S)
    t = unescape(re.sub(r"<[^>]+>", " ", raw))
    return re.sub(r"\s+", " ", t)

def probe(label, fname, kws):
    t = text(f"{D}/{fname}")
    print(f"== {label} == ({len(t)} chars)")
    for kw in kws:
        hits = [m.start() for m in re.finditer(re.escape(kw), t)]
        for h in hits[:2]:
            snippet = t[max(0, h - 100): h + 160]
            print(f"  [{kw}] ...{snippet}...")
        if not hits:
            print(f"  [{kw}] 0 hits")
    print()

probe("HIRO @ ADCELL (11.11.)", "hiro_adcell.html",
      ["50,00", "90 Tagen", "Freigabe", "Storno", "Direct Linking", "SEM",
       "incentiviert", "Lead", "Bewerbung", "DeepLink"])

probe("Treppenlift-Zentrum/Lotse @ 100partnerprogramme (11.11.)", "lotse_100pp.html",
      ["60,00", "120,00", "Netzwerk", "Treppenlift-Zentrum", "Tracking",
       "Update", "Stand", "aktiv", "Lead"])
