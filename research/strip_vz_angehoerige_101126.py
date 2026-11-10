#!/usr/bin/env python3
"""Strip VZ 10566 + read-target helper for angehoerige evidence dir."""
import html, re, os

d = os.path.dirname(os.path.abspath(__file__)) + "/evidence/angehoerige-101126"
raw = open(os.path.join(d, "vz-10566.html"), encoding="utf-8", errors="replace").read()
raw = re.sub(r"<script[^>]*>.*?</script>", " ", raw, flags=re.S | re.I)
raw = re.sub(r"<style[^>]*>.*?</style>", " ", raw, flags=re.S | re.I)
raw = re.sub(r"<!--.*?-->", " ", raw, flags=re.S)
raw = re.sub(r"<[^>]+>", "\n", raw)
raw = html.unescape(raw)
lines = [re.sub(r"\s+", " ", l).strip() for l in raw.splitlines()]
txt = "\n".join(l for l in lines if len(l) > 25)
out = os.path.join(d, "vz-10566.txt")
open(out, "w", encoding="utf-8").write(txt)
print(f"vz-10566.txt: {len(txt)} chars")
