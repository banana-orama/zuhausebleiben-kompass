#!/usr/bin/env python3
"""Strip raw evidence HTML to plain text for verbatim quoting (smartwatch-161126)."""
import re, html, pathlib, sys

D = pathlib.Path(__file__).resolve().parent / "evidence" / "smartwatch-161126"

FILES = ["vz-10566.html", "gesund-bund.html", "adac.html", "vdk-hamburg.html",
         "alzheimer-technisch.html", "pflege-de-sturz.html", "pflege-net-smartwatch.html"]

def strip(raw: str) -> str:
    raw = re.sub(r"<script\b.*?</script>", " ", raw, flags=re.S | re.I)
    raw = re.sub(r"<style\b.*?</style>", " ", raw, flags=re.S | re.I)
    raw = re.sub(r"<noscript\b.*?</noscript>", " ", raw, flags=re.S | re.I)
    raw = re.sub(r"<!--.*?-->", " ", raw, flags=re.S)
    raw = re.sub(r"<(br|/p|/h[1-6]|/li|/tr|/div|/section|/article|/td)[^>]*>", "\n", raw, flags=re.I)
    raw = re.sub(r"<[^>]+>", " ", raw)
    raw = html.unescape(raw)
    raw = raw.replace("\xa0", " ")
    raw = re.sub(r"\s+([.,;:!?)\]])", r"\1", raw)
    raw = re.sub(r"([(])\s+", r"\1", raw)
    lines = [re.sub(r"[ \t]+", " ", l).strip() for l in raw.splitlines()]
    out, prev = [], None
    for l in lines:
        if not l:
            continue
        if l == prev:
            continue
        out.append(l)
        prev = l
    return "\n".join(out)

for name in FILES:
    p = D / name
    if not p.exists() or p.stat().st_size < 200:
        print(f"SKIP {name} (missing/too small)")
        continue
    raw = p.read_text(encoding="utf-8", errors="replace")
    # crude charset fix: many German CMS pages are utf-8; decode handled by errors=replace
    txt = strip(raw)
    out = D / (name.rsplit(".", 1)[0] + ".txt")
    out.write_text(txt, encoding="utf-8")
    print(f"OK {name} -> {out.name} {len(txt)} chars")
