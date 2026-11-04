#!/usr/bin/env python3
"""Strip fetched HTML evidence to plain text for verbatim quote checks.
Briefing 16 — Mobiler Hausnotruf (04.11.2026)."""
import html as html_mod
import re
from pathlib import Path

D = Path("research/evidence/hausnotruf-mobil-041126")

def strip(path: Path) -> str:
    raw = path.read_bytes()
    # gesetze-im-internet is ISO-8859-1; everything else modern UTF-8
    enc = "iso-8859-1" if "sgb" in path.name else "utf-8"
    txt = raw.decode(enc, errors="replace")
    txt = re.sub(r"(?is)<script.*?</script>", " ", txt)
    txt = re.sub(r"(?is)<style.*?</style>", " ", txt)
    txt = re.sub(r"(?is)<noscript.*?</noscript>", " ", txt)
    txt = re.sub(r"(?is)<!--.*?-->", " ", txt)
    txt = re.sub(r"(?i)<br\s*/?>", "\n", txt)
    txt = re.sub(r"(?i)</(p|div|h[1-6]|li|tr|table|section|article)>", "\n", txt)
    txt = re.sub(r"(?s)<[^>]+>", " ", txt)
    txt = html_mod.unescape(txt)
    txt = txt.replace("\u00a0", " ").replace("\u202f", " ")
    txt = re.sub(r"[ \t]+", " ", txt)
    txt = re.sub(r"\n\s*\n+", "\n", txt)
    return txt.strip()

for f in sorted(D.glob("*.html")):
    out = f.with_suffix(".txt")
    text = strip(f)
    out.write_text(text, encoding="utf-8")
    print(f"{out.name}: {len(text)} chars")
