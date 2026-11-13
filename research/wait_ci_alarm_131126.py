#!/usr/bin/env python3
"""Wait for CI run of commit b643b4f (gh CLI, head-sha match, volle SHA)."""
import subprocess
import sys
import time

SHA = "b643b4f30ecc87ee044a16676ecba9b13dec583d"
DEADLINE = time.time() + 540
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
        if '"conclusion":"success"' in rows:
            print("CI SUCCESS")
            sys.exit(0)
        if '"conclusion":"failure"' in rows or '"conclusion":"failed"' in rows:
            print("CI FAILED")
            sys.exit(2)
    time.sleep(20)
print("CI TIMEOUT nach 540s")
sys.exit(3)
