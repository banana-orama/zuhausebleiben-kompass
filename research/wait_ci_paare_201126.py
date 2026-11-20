#!/usr/bin/env python3
"""Wait for CI run of commit 2fafb93b34ad235588ab2598467e515e983bfded (gh CLI, head-sha match)."""
import subprocess
import sys
import time

SHA = "2fafb93b34ad235588ab2598467e515e983bfded"
DEADLINE = time.time() + 480
last = None
while time.time() < DEADLINE:
    r = subprocess.run(
        ["gh", "run", "list", "--commit", SHA, "--json", "status,conclusion,databaseId,displayTitle", "--limit", "3"],
        capture_output=True, text=True)
    if r.stdout.strip() and r.stdout.strip() != last:
        last = r.stdout.strip()
        print(time.strftime("%H:%M:%S"), last, flush=True)
    if '"status":"completed"' in last or '"conclusion": "success"' in last or '"conclusion":"success"' in last or '"conclusion": "failure"' in last or '"conclusion":"failure"' in last:
        break
    time.sleep(15)
final = subprocess.run(["gh", "run", "list", "--commit", SHA, "--json", "status,conclusion,databaseId", "--limit", "3"],
                       capture_output=True, text=True)
print("FINAL:", final.stdout.strip())
sys.exit(0 if "success" in final.stdout else 1)
