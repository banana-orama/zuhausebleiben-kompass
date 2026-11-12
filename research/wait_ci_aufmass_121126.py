#!/usr/bin/env python3
"""Wait for CI run of commit b07a8569212cd1dee429857e5d8422a733a149de (gh CLI, head-sha match)."""
import subprocess
import sys
import time

SHA = "b07a8569212cd1dee429857e5d8422a733a149de"
DEADLINE = time.time() + 480
last = None

local = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd="/Users/mac/agentic-business/barrierefrei-leads").stdout.strip()
assert local == SHA, f"SHA mismatch: local {local} != pinned {SHA}"

while time.time() < DEADLINE:
    r = subprocess.run(
        ["gh", "run", "list", "--repo", "banana-orama/zuhausebleiben-kompass", "--commit", SHA,
         "--json", "databaseId,status,conclusion,workflowName", "--limit", "5"],
        capture_output=True, text=True)
    if r.returncode == 0 and r.stdout.strip():
        import json
        runs = json.loads(r.stdout)
        if runs:
            last = runs
            done = [x for x in runs if x["status"] == "completed"]
            if len(done) >= 1:
                for x in runs:
                    print(x["status"], x.get("conclusion"), x["databaseId"], x["workflowName"])
                bad = [x for x in done if x["conclusion"] != "success"]
                if bad:
                    sys.exit(f"CI failed: {bad}")
                print("CI SUCCESS")
                sys.exit(0)
    print("waiting…", flush=True)
    time.sleep(20)
print("TIMEOUT; last:", last)
sys.exit(2)
