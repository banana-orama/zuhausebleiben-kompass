#!/usr/bin/env python3
"""Wartet auf den GitHub-Actions-Run und meldet den Endstatus."""
import subprocess, sys, time

RUN = sys.argv[1] if len(sys.argv) > 1 else "40695302305"
REPO = "banana-orama/zuhausebleiben-kompass"
deadline = time.time() + 480
status = None
while time.time() < deadline:
    out = subprocess.run(
        ["gh", "run", "view", RUN, "--repo", REPO, "--json", "status,conclusion"],
        capture_output=True, text=True,
    ).stdout.strip()
    if '"status":"completed"' in out.replace(" ", ""):
        print("RUN COMPLETE:", out)
        status = out
        break
    time.sleep(20)
else:
    print("TIMEOUT: Run nicht abgeschlossen innerhalb 480s")
    sys.exit(2)
if '"conclusion":"success"' in status.replace(" ", ""):
    print("CONCLUSION: success")
else:
    print("CONCLUSION: NICHT success")
    sys.exit(1)
