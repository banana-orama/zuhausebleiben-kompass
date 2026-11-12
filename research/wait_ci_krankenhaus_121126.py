#!/usr/bin/env python3
"""CI-Wait für Briefing 24. Pollt gh run list auf git rev-parse HEAD. Greppt die SHA-Zeile
nicht (dynamisch), validiert aber, dass der Commit unter Test == HEAD ist."""
import subprocess
import sys
import time

REPO = "/Users/mac/agentic-business/barrierefrei-leads"


def real_sha():
    out = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=REPO)
    return out.stdout.strip()


SHA = real_sha()
print("waiting on CI for", SHA)
DEADLINE = time.time() + 24 * 60

while time.time() < DEADLINE:
    out = subprocess.run(
        ["gh", "run", "list", "--commit", SHA, "--limit", "5",
         "--json", "databaseId,status,conclusion,name"],
        capture_output=True, text=True)
    if out.returncode != 0:
        print("gh error:", out.stderr[:200])
        time.sleep(20)
        continue
    runs = subprocess.run(["gh", "run", "list", "--commit", SHA, "--limit", "5"],
                          capture_output=True, text=True).stdout
    lines = [l for l in runs.strip().splitlines() if l.strip()]
    if not lines:
        print(time.strftime("%H:%M:%S"), "kein Run yet")
        time.sleep(20)
        continue
    status_line = lines[0]
    print(time.strftime("%H:%M:%S"), status_line[:110])
    if "completed" in status_line:
        if "success" in status_line:
            print("CI SUCCESS für", SHA)
            sys.exit(0)
        print("CI FAILED:", status_line)
        sys.exit(1)
    time.sleep(20)

print("TIMEOUT nach 24 min")
sys.exit(2)
