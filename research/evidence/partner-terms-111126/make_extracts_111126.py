#!/usr/bin/env python3
"""Decode evidence HTMLs to text extracts (.txt) for the 11.11. partner-terms ledger,
and scan the zentrum impressum for operator identity keywords."""
import re
from html import unescape
from pathlib import Path

D = Path("research/evidence/partner-terms-111126")

def text(p):
    raw = Path(p).read_text(encoding="utf-8", errors="replace")
    raw = re.sub(r"<script[^>]*>.*?</script>", "", raw, flags=re.S)
    raw = re.sub(r"<style[^>]*>.*?</style>", "", raw, flags=re.S)
    return re.sub(r"[ \t]+", " ", unescape(re.sub(r"<[^>]+>", " ", raw)))

extracts = {
    "malteser_awin_profile_111126.txt": "malteser.html",
    "lifta_awin_profile_111126.txt": "lifta.html",
    "hiro_adcell_111126.txt": "hiro_adcell.html",
    "lotse_100pp_111126.txt": "lotse_100pp.html",
    "lotse_home_111126.txt": "lotse_home.html",
    "lotse_impressum_111126.txt": "lotse_impressum.html",
    "zentrum_impressum_111126.txt": "zentrum_impressum.html",
    "live_hausnotruf_vergleich_111126.txt": "live_hausnotruf_vergleich.html",
}
for out, src in extracts.items():
    t = text(D / src)
    (D / out).write_text(t, encoding="utf-8")
    print(f"{out}: {len(t)} chars")

# zentrum impressum: find operator block
zt = (D / "zentrum_impressum_111126.txt").read_text(encoding="utf-8")
for kw in ["Vertreten", "GbR", "GmbH", "Umsatzsteuer", "USt", "Telefon"]:
    hits = [m.start() for m in re.finditer(kw, zt)]
    for h in hits[:2]:
        print(f"[zentrum {kw}] ...{zt[max(0, h - 80):h + 180]}...")
    if not hits:
        print(f"[zentrum {kw}] 0 hits")

# raw html cleanup marker (files stay local this session; not staged)
print("RAW_FILES_PRESENT:", sorted(p.name for p in D.glob("*.html")))
