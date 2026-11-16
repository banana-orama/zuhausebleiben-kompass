#!/usr/bin/env python3
"""Strip HTML evidence files to readable text (batch: region-bayern-161126).

Encoding-aware (utf-8 with cp1252/latin-1 fallback) and collapses markup
artifacts like " ," -> ", " so stripped text matches what a reader sees."""
import html as html_mod
import re
import sys
from pathlib import Path

D = Path(__file__).parent

def strip(path):
    raw_bytes = Path(path).read_bytes()
    try:
        raw = raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raw = raw_bytes.decode("cp1252", errors="replace")
    s = re.sub(r"<script[\s\S]*?</script>", " ", raw, flags=re.I)
    s = re.sub(r"<style[\s\S]*?</style>", " ", s, flags=re.I)
    s = re.sub(r"<noscript[\s\S]*?</noscript>", " ", s, flags=re.I)
    s = re.sub(r"<!--[\s\S]*?-->", " ", s)
    # keep some block structure
    s = re.sub(r"<(br|/p|/div|/li|/h[1-6]|/tr)[^>]*>", "\n", s, flags=re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html_mod.unescape(s)
    s = s.replace("\xa0", " ")
    s = s.replace("\u00ad", "")  # soft hyphen: rendering artifact
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n", s)
    # closing tag before punctuation leaves " ," / " ." / " ;"
    s = re.sub(r" ([,.;:!?])", r"\1", s)
    return s.strip()

if __name__ == "__main__":
    for name in sys.argv[1:]:
        p = D / name
        out = D / (p.stem + ".txt")
        txt = strip(p)
        out.write_text(txt, encoding="utf-8")
        print(f"{name} -> {out.name}: {len(txt)} chars")
