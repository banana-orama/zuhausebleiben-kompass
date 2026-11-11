#!/usr/bin/env python3
"""CI-Wait für den Partner-Terms-Lauf 11.11. Pollt gh run list auf die volle SHA 5f9e0c21d459398fd0c8e5c788d217e31e70c1b3."""
import json
import subprocess
import sys
import time

SHA = "5f9e0c21d459398fd0c8e5c788d217e31e70c1b3"
print("waiting on CI for", SHA)
DEADLINE = time.time() + 24 * 60

while time.time() < DEADLINE:
    out = subprocess.run(
        ["gh", "run", "list", "--commit", SHA, "--limit", "5",
         "--json", "databaseId,status,conclusion,name,headSha"],
        capture_output=True, text=True)
    if out.returncode != 0:
        print("gh error:", out.stderr[:200])
        time.sleep(20)
        continue
    runs = json.loads(out.stdout or "[]")
    runs = [r for r in runs if r.get("headSha") == SHA]
    if not runs:
        print("no runs yet for SHA, retrying...")
        time.sleep(20)
        continue
    for r in runs:
        print(r["databaseId"], r["name"][:40], r["status"], r.get("conclusion"))
    if all(r["status"] == "completed" for r in runs):
        bad = [r for r in runs if r.get("conclusion") != "success"]
        print("CI DONE", "OK" if not bad else f"FAILED: {bad}")
        sys.exit(0 if not bad else 1)
    time.sleep(30)
print("TIMEOUT waiting for CI")
sys.exit(2)
