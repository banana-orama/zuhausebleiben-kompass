#!/usr/bin/env python3
"""CI-Wait für Commit fe7f225 (Region NRW, 13.11.2026). Pollt gh run list auf den SHA.
SHA-Literal gegen git rev-parse HEAD des Commits geprüft (Pitfall: sed-geerbte Stale-SHA)."""
import subprocess
import sys
import time
import json

SHA = "fe7f22584f13d011347879f240205b255ccab74e"
DEADLINE = time.time() + 25 * 60

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
    runs = [r for r in runs if r["headSha"].startswith(SHA)]
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
    time.sleep(20)
print("TIMEOUT waiting for CI")
sys.exit(1)
