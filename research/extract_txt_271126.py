#!/usr/bin/env python3
# HTML -> Text-Extraktion (Region-Screen 271126 MV+RP): Tags strippen, Blöcke trennen, Whitespace normalisieren.
import html
import re
import sys
from pathlib import Path

def strip_html(raw: str) -> str:
    t = re.sub(r"<script[^>]*>.*?</script>", " ", raw, flags=re.S | re.I)
    t = re.sub(r"<style[^>]*>.*?</style>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<!--.*?-->", " ", t, flags=re.S)
    t = re.sub(r"(?i)<(br|/p|/div|/li|/h[1-6]|/tr|/table)[^>]*>", "\n", t)
    t = re.sub(r"(?i)<(p|div|li|h[1-6]|tr)[^>]*>", "\n", t)
    t = re.sub(r"(?i)</t[dh]>", " | ", t)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    t = t.replace("\u00ad", "").replace("\r", "\n")
    lines = [re.sub(r"[ \t\u00a0\u202f\u2009\u2007\u2008]+", " ", ln).strip() for ln in t.split("\n")]
    out, blank = [], 0
    for ln in lines:
        if not ln:
            blank += 1
            if blank <= 1:
                out.append("")
            continue
        blank = 0
        out.append(ln)
    return "\n".join(out).strip() + "\n"

def main() -> int:
    for arg in sys.argv[1:]:
        src = Path(arg)
        dst = src.with_suffix(".txt")
        raw_bytes = src.read_bytes()
        raw = raw_bytes.decode("utf-8", errors="replace")
        if "\ufffd" in raw:  # gesetze-im-internet u.a. liefern ISO-8859-1: erst sauber dekodieren
            raw = raw_bytes.decode("cp1252", errors="replace")
        dst.write_text(strip_html(raw), encoding="utf-8")
        print(f"{src.name} -> {dst.name} ({dst.stat().st_size}B)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
