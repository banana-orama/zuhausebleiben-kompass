#!/usr/bin/env python3
"""Vollstaendige Source-Eintraege + Inline-Zitierkontext der 5 betroffenen Quellen."""
import json, re

jobs = [
    ("content-ready/hausnotruf-kosten-anbieter-vergleich.json", "widerruf-vertraege-rueckgaengig-machen-70049"),
    ("content-ready/hausnotruf-sturzerkennung-oder-knopf.json", "pflege.net/hausnotruf-sturzsensor"),
    ("content-ready/hilfsmittel-dusch-wc-uebernahme.json", "rehadat-gkv.de"),
    ("content-ready/treppenlift-mieten.json", "pflege.net/ratgeber/treppenlift-mieten-oder-kaufen"),
    ("content-ready/treppenlift-mietwohnung.json", "pflege.net/ratgeber/treppenlift-in-der-mietwohnung"),
]
for path, needle in jobs:
    data = json.load(open(path, encoding="utf-8"))
    print("=" * 90)
    print(path)
    srcs = data.get("sources", [])
    idx = None
    for i, s in enumerate(srcs):
        if needle in json.dumps(s):
            idx = i + 1
            print(f"SOURCE [{i+1}]:", json.dumps(s, ensure_ascii=False))
    # Inline-Kontext: alle Strings, die [idx] als Zitat tragen
    raw = json.dumps(data, ensure_ascii=False, indent=1)
    pat = re.compile(r"\[" + str(idx) + r"\]")
    for line in raw.splitlines():
        if pat.search(line) and "url" not in line:
            print("INLINE:", line.strip()[:400])
