#!/usr/bin/env python3
"""CI-Status für HEAD via öffentliche GitHub-API (kein Token nötig, öffentliches Repo)."""
import json, subprocess, sys, urllib.request

sha = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
url = f"https://api.github.com/repos/banana-orama/zuhausebleiben-kompass/actions/runs?head_sha={sha}"
with urllib.request.urlopen(url, timeout=30) as r:
    d = json.load(r)
runs = d.get("workflow_runs", [])
if not runs:
    print("NO RUNS YET for", sha)
    sys.exit(2)
for r in runs:
    print(r["id"], r["status"], r["conclusion"])
sys.exit(0 if all(x["status"] == "completed" and x["conclusion"] == "success" for x in runs) else 1)
