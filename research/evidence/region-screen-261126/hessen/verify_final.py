#!/usr/bin/env python3
"""Final verification for the Hessen region-screen run."""
import json, os, subprocess, sys

repo = "/Users/mac/agentic-business/barrierefrei-leads"
r = subprocess.run([sys.executable, os.path.join(repo, "research",
                   "check_quotes_region_screen_261126_hessen.py")],
                   capture_output=True, text=True, cwd=repo)
print(r.stdout.strip())
print("checker EXIT =", r.returncode)

d = json.load(open(os.path.join(repo, "research", "region-screen-261126-hessen-ledger.json")))
print("ledger ok:", d["batch"], d["checked_at"], len(d["sources"]), "sources,",
      d["sources_checked"], "URLs checked")

ev = os.path.join(repo, "research", "evidence", "region-screen-261126", "hessen")
files = sorted(os.listdir(ev))
print(f"\nevidence dir: {len(files)} files")
for f in files:
    print(" ", f, os.path.getsize(os.path.join(ev, f)))

for f in ["region-screen-261126-hessen.md", "region-screen-261126-hessen-ledger.json",
          "check_quotes_region_screen_261126_hessen.py"]:
    p = os.path.join(repo, "research", f)
    print(f, os.path.getsize(p), "bytes")
