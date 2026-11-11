#!/usr/bin/env python3
"""Decode the two Bundestag pages to text extracts (11.11.2026)."""
import re
from html import unescape
from pathlib import Path

D = Path("research/evidence/partner-terms-111126")

def text(p):
    raw = Path(p).read_text(encoding="utf-8", errors="replace")
    raw = re.sub(r"<script[^>]*>.*?</script>", "", raw, flags=re.S)
    raw = re.sub(r"<style[^>]*>.*?</style>", "", raw, flags=re.S)
    return re.sub(r"[ \t]+", " ", unescape(re.sub(r"<[^>]+>", " ", raw)))

for out, src in {
    "hib_884_2026_111126.txt": "hib_884_2026.html",
    "bt_textarchiv_kw45_111126.txt": "bt_textarchiv_kw45.html",
}.items():
    t = text(D / src)
    (D / out).write_text(t, encoding="utf-8")
    print(f"{out}: {len(t)} chars")
