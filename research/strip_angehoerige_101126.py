#!/usr/bin/env python3
"""Strip competitor + source pages to text for reading (evidence dir angehoerige-101126)."""
import html, re, os, sys

d = os.path.dirname(os.path.abspath(__file__)) + "/evidence/angehoerige-101126"

def strip(path):
    raw = open(os.path.join(d, path), encoding="utf-8", errors="replace").read()
    raw = re.sub(r"<script[^>]*>.*?</script>", " ", raw, flags=re.S | re.I)
    raw = re.sub(r"<style[^>]*>.*?</style>", " ", raw, flags=re.S | re.I)
    raw = re.sub(r"<!--.*?-->", " ", raw, flags=re.S)
    raw = re.sub(r"<[^>]+>", "\n", raw)
    raw = html.unescape(raw)
    lines = [re.sub(r"\s+", " ", l).strip() for l in raw.splitlines()]
    return "\n".join(l for l in lines if len(l) > 25)

for f in ["hsp-angehoerige.html", "bewo-angehoerige.html", "notfallknopf-beantragen.html",
          "sanivia-beantragen.html", "vz-hausnotruf.html", "malteser-hausnotruf.html"]:
    out = os.path.join(d, f.replace(".html", ".txt"))
    txt = strip(f)
    open(out, "w", encoding="utf-8").write(txt)
    print(f"{f} -> {out}: {len(txt)} chars")
