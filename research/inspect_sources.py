#!/usr/bin/env python3
"""Print top-level source list for one or more article JSONs (cron-safe inspection)."""
import json, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
for slug in sys.argv[1:]:
    p = ROOT / "content-ready" / f"{slug}.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    print(f"=== {slug} === status={d.get('status')} image={d.get('image',{}).get('src')}")
    for i, s in enumerate(d.get("sources", []), 1):
        print(f"[{i}] {s.get('title')} | {s.get('url')} | checked_at={s.get('checked_at')}")
    print("keys:", sorted(d.keys()))
