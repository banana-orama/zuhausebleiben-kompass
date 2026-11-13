#!/usr/bin/env python3
"""Strip HTML evidence files to readable text (batch: region-nrw-131126)."""
import html as html_mod
import re
import sys
from pathlib import Path

D = Path(__file__).parent

def strip(path):
    raw = Path(path).read_text(encoding="utf-8", errors="replace")
    s = re.sub(r"<script[\s\S]*?</script>", " ", raw, flags=re.I)
    s = re.sub(r"<style[\s\S]*?</style>", " ", s, flags=re.I)
    s = re.sub(r"<noscript[\s\S]*?</noscript>", " ", s, flags=re.I)
    s = re.sub(r"<!--[\s\S]*?-->", " ", s)
    # keep some block structure
    s = re.sub(r"<(br|/p|/div|/li|/h[1-6]|/tr)[^>]*>", "\n", s, flags=re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html_mod.unescape(s)
    s = s.replace("\xa0", " ")
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n", s)
    return s.strip()

for name in sys.argv[1:]:
    p = D / name
    out = D / (p.stem + ".txt")
    out.write_text(strip(p), encoding="utf-8")
    print(f"{name} -> {out.name}: {len(strip(p))} chars")
