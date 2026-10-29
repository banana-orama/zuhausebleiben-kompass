#!/usr/bin/env python3
"""Kontext der betroffenen Zitate zeigen: welche Quelle, welcher Satz. 291026 Link-Rot-Audit."""
import json, glob, re

targets = {
    "widerruf-vertraege-rueckgaengig-machen-70049",
    "pflege.net/hausnotruf-sturzsensor",
    "pflege.net/ratgeber/treppenlift-in-der-mietwohnung",
    "pflege.net/ratgeber/treppenlift-mieten-oder-kaufen",
    "rehadat-gkv.de",
}

def walk(obj, path, hits):
    if isinstance(obj, dict):
        for k, v in obj.items():
            walk(v, f"{path}.{k}", hits)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            walk(v, f"{path}[{i}]", hits)
    elif isinstance(obj, str):
        for t in targets:
            if t in obj:
                hits.append((path, t, obj))

for path in sorted(glob.glob("content-ready/*.json")):
    data = json.load(open(path, encoding="utf-8"))
    hits = []
    walk(data, "$", hits)
    if hits:
        print("=" * 80)
        print(path)
        for p, t, s in hits:
            print(f"--- {t} @ {p}")
            print(s[:600])
