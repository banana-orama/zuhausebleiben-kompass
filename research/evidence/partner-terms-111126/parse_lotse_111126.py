#!/usr/bin/env python3
"""Parse Treppenlift-Lotse/Zentrum pages: operator identity, network, partner-programme links."""
import re
from html import unescape

D = "research/evidence/partner-terms-111126"

def text(p):
    raw = open(p, encoding="utf-8", errors="replace").read()
    raw = re.sub(r"<script[^>]*>.*?</script>", "", raw, flags=re.S)
    raw = re.sub(r"<style[^>]*>.*?</style>", "", raw, flags=re.S)
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", raw)))

def links(p):
    raw = open(p, encoding="utf-8", errors="replace").read()
    return re.findall(r'href="([^"]+)"[^>]*>([^<]{0,60})', raw)

for label, fname in [("lotse_home", "lotse_home.html"), ("zentrum_home", "zentrum_home.html")]:
    t = text(f"{D}/{fname}")
    print(f"== {label} == ({len(t)} chars)")
    print(t[:500])
    for kw in ["Partner", "Netzwerk", "Affiliate", "Impressum", "Kontakt", "vermitteln", "Vergütung", "Provision"]:
        hits = [m.start() for m in re.finditer(kw, t, re.I)]
        for h in hits[:2]:
            print(f"  [{kw}] ...{t[max(0,h-90):h+140]}...")
        if not hits:
            print(f"  [{kw}] 0 hits")
    print("  -- partnerish links --")
    for href, txt in links(f"{D}/{fname}"):
        if re.search(r"partner|affiliate|impressum|kontakt", href, re.I) or re.search(r"[Pp]artner|[Aa]ffiliate|[Ii]mpressum", txt):
            print(f"    {href} | {txt.strip()[:60]}")
    print()
