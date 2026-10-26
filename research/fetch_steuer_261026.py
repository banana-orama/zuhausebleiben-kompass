#!/usr/bin/env python3
"""Fetch § 35a + § 33 EStG live from gesetze-im-internet, decode, save evidence.
Lesson from memory/cron: ISO-8859-1, numeric entities, protected spaces, soft hyphens."""
import urllib.request, html, re, sys, pathlib

OUT = pathlib.Path("research/evidence/steuer-261026")
OUT.mkdir(parents=True, exist_ok=True)

TARGETS = {
    "estg__35a": "https://www.gesetze-im-internet.de/estg/__35a.html",
    "estg__33": "https://www.gesetze-im-internet.de/estg/__33.html",
}

def clean(raw: bytes) -> str:
    txt = raw.decode("iso-8859-1", errors="replace")
    txt = html.unescape(txt)
    txt = txt.replace("\u00ad", "")          # soft hyphen
    txt = re.sub(r"<script.*?</script>", " ", txt, flags=re.S)
    txt = re.sub(r"<style.*?</style>", " ", txt, flags=re.S)
    txt = re.sub(r"<[^>]+>", " ", txt)
    txt = re.sub(r"[ \t\u00a0]+", " ", txt)
    txt = re.sub(r"\s*\n\s*", "\n", txt)
    return txt.strip()

for name, url in TARGETS.items():
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (research)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read()
    path = OUT / f"{name}.txt"
    path.write_text(clean(raw), encoding="utf-8")
    txt = path.read_text(encoding="utf-8")
    print(f"== {name} :: {url} :: HTTP 200, {len(raw)} bytes raw, {len(txt)} chars clean")
    # print the norm sections that carry the figures
    for marker in ["Steuerermäßigung", "zumutbare Belastung"]:
        idx = txt.find(marker)
        if idx >= 0:
            print("   ...", txt[max(0, idx-80):idx+700].replace("\n", " ")[:780])
            break
print("OK")
