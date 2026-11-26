#!/usr/bin/env python3
"""CI-Wait für Commit 0db4948 (Region Hessen, 26.11.2026). SHA-Literal = git rev-parse HEAD."""
import json, subprocess, sys, time
SHA = "caafa0290dccf97d6ef84f77ccd6ca89aadebb87"
DEADLINE = time.time() + 20 * 60
while time.time() < DEADLINE:
    out = subprocess.run(["gh","run","list","--commit",SHA,"--limit","5","--json","databaseId,status,conclusion,headSha"],capture_output=True,text=True)
    if out.returncode != 0:
        print("gh error:", out.stderr[:200]); time.sleep(20); continue
    runs = [r for r in json.loads(out.stdout or "[]") if r["headSha"].startswith(SHA)]
    if not runs:
        print("no runs yet, retrying..."); time.sleep(20); continue
    for r in runs: print(f"run {r['databaseId']}: {r['status']} {r.get('conclusion') or ''}")
    if all(r["status"] == "completed" for r in runs):
        ok = all(r.get("conclusion") == "success" for r in runs)
        print(("CI SUCCESS" if ok else "CI FAILURE") + " für " + SHA)
        sys.exit(0 if ok else 1)
    time.sleep(20)
print("TIMEOUT"); sys.exit(2)
