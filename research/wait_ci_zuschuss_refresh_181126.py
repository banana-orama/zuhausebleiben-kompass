#!/usr/bin/env python3
"""Wait for CI run of commit a1d03a2 (gh CLI, head-sha match, volle SHA)."""
import subprocess
import sys
import time

FULL = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
if not FULL.startswith("a1d03a2"):
    print("HEAD ist nicht a1d03a2:", FULL)
    sys.exit(4)
print("Warte auf CI fuer", FULL, flush=True)
DEADLINE = time.time() + 540
last = None
while time.time() < DEADLINE:
    out = subprocess.run(
        ["gh", "run", "list", "--repo", "banana-orama/zuhausebleiben-kompass",
         "--commit", FULL, "--json", "databaseId,status,conclusion,name", "--limit", "3"],
        capture_output=True, text=True)
    rows = out.stdout.strip()
    if rows and rows != last:
        print(rows, flush=True)
        last = rows
    if '"status":"completed"' in rows:
        if '"conclusion":"success"' in rows:
            print("CI SUCCESS")
            sys.exit(0)
        if '"conclusion":"failure"' in rows or '"conclusion":"failed"' in rows:
            print("CI FAILED")
            sys.exit(2)
    time.sleep(20)
print("CI TIMEOUT nach 540s")
sys.exit(3)
