#!/usr/bin/env python3
"""Show exact top-level JSON schema of an article: keys and one compact sample per collection."""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1] / "content-ready"
slug = sys.argv[1] if len(sys.argv) > 1 else "treppenlift-maximalgewicht"
d = json.loads((ROOT / f"{slug}.json").read_text(encoding="utf-8"))
print("TOP-KEYS:", list(d.keys()))
print("title:", d["title"])
print("h1:", d["h1"])
print("description[:120]:", d["description"][:120])
print("intro[0]:", json.dumps(d["intro"][0], ensure_ascii=False)[:200])
s0 = d["sections"][0]
print("SECTION-KEYS:", list(s0.keys()))
for k in s0:
    v = json.dumps(s0[k], ensure_ascii=False)
    print(f"  {k}: {v[:260]}")
if len(d["sections"]) > 1:
    print("OTHER-SECTION-HEADING-TYPES:", sorted({tuple(sorted(s.keys())) for s in d["sections"]}))
fq = d["faqs"][0]
print("FAQ-KEYS:", list(fq.keys()), "| sample:", json.dumps(fq, ensure_ascii=False)[:200])
print("n_sections:", len(d["sections"]), "n_faqs:", len(d["faqs"]))
src = d["sources"][0]
print("SOURCE-KEYS:", list(src.keys()), "| sample:", json.dumps(src, ensure_ascii=False)[:220])
img = d["image"]
print("IMAGE:", json.dumps(img, ensure_ascii=False)[:300])
print("status:", d["status"])
