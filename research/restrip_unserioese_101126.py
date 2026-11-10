#!/usr/bin/env python3
"""Re-Strip mit Zeilen-Schwelle 12 für Klage-Seite + VZ-Pillar (kurze Tabellen-/Listen-Zeilen)."""
import html
import os
import re

D = "/Users/mac/agentic-business/barrierefrei-leads/research/evidence/unserioese-101126"


def strip_html(raw):
    raw = re.sub(r"<script[^>]*>.*?</script>", " ", raw, flags=re.S | re.I)
    raw = re.sub(r"<style[^>]*>.*?</style>", " ", raw, flags=re.S | re.I)
    raw = re.sub(r"<!--.*?-->", " ", raw, flags=re.S)
    raw = re.sub(r"<[^>]+>", "\n", raw)
    raw = html.unescape(raw)
    lines = [re.sub(r"\s+", " ", l).strip() for l in raw.splitlines()]
    return "\n".join(l for l in lines if len(l) > 12)


for name in ["vz-verbandsklage-mobilae", "vz-treppenlifte-10711"]:
    b = open(os.path.join(D, name + ".html"), "rb").read()
    try:
        raw = b.decode("utf-8")
    except UnicodeDecodeError:
        raw = b.decode("iso-8859-1", errors="replace")
    txt = strip_html(raw)
    out = os.path.join(D, name + ".txt")
    open(out, "w", encoding="utf-8").write(txt)
    print(f"{name}.txt re-stripped: {len(txt)} chars")
