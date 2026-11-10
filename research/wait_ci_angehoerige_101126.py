#!/usr/bin/env python3
"""CI-Wait für Commit d214dd0 (Briefing 21, 10.11.2026). Pollt gh run list auf den SHA."""
import subprocess
import sys
import time

SHA = "d214dd0c766f55cf5373ec4ab4ae3480a551f26e"
DEADLINE = time.time() + 25 * 60

while time.time() < DEADLINE:
    out = subprocess.run(
        ["gh", "run", "list", "--commit", SHA, "--limit", "5",
         "--json", "databaseId,status,conclusion,name"],
        capture_output=True, text=True)
    if out.returncode != 0:
        print("gh error:", out.stderr[:200])
        time.sleep(20)
        continue
    import json
    runs = json.loads(out.stdout or "[]")
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
