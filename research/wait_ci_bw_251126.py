#!/usr/bin/env python3
"""CI-Wait für den Region-BW-Commit (25.11.2026). SHA wird beim Aufruf via git rev-parse geprüft."""
import json
import subprocess
import sys
import time

SHA = sys.argv[1] if len(sys.argv) > 1 else ""
assert len(SHA) == 40, "volle SHA als Argument übergeben"
head = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
assert head == SHA, f"SHA-Argument {SHA} != HEAD {head} — falscher Commit unter Test"

DEADLINE = time.time() + 20 * 60
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
        print(f"run {r['databaseId']}: {r['status']} {r.get('conclusion') or ''}")
    if all(r["status"] == "completed" for r in runs):
        ok = all(r.get("conclusion") == "success" for r in runs)
        print(("CI SUCCESS" if ok else "CI FAILURE") + f" für {SHA}")
        sys.exit(0 if ok else 1)
    time.sleep(20)
print("timeout — CI nicht abgeschlossen")
sys.exit(2)
