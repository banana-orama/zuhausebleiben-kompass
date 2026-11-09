#!/usr/bin/env python3
"""Wait for CI run of commit 80501f7415cd1e8f13f614349729a98e3dacf10d (gh CLI, head-sha match)."""
import subprocess
import sys
import time

SHA = "80501f7415cd1e8f13f614349729a98e3dacf10d"
DEADLINE = time.time() + 480
last = None
while time.time() < DEADLINE:
    out = subprocess.run(
        ["gh", "run", "list", "--repo", "banana-orama/zuhausebleiben-kompass",
         "--commit", SHA, "--json", "databaseId,status,conclusion,name", "--limit", "3"],
        capture_output=True, text=True)
    rows = out.stdout.strip()
    if rows and rows != last:
        print(rows, flush=True)
        last = rows
    if '"status":"completed"' in rows.replace("\\", ""):
        concl = [r for r in rows.split('"conclusion":"') if False]
        if '"conclusion":"success"' in rows:
            print("CI SUCCESS")
            sys.exit(0)
        if '"conclusion":"failure"' in rows or '"conclusion":"failed"' in rows:
            print("CI FAILED")
            sys.exit(2)
    time.sleep(20)
print("CI TIMEOUT nach 480s")
sys.exit(3)
