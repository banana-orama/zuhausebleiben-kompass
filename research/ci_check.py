#!/usr/bin/env python3
"""CI-Status-Check fuer einen Commit: usage: ci_check.py <full-sha>"""
import json
import sys
import time
import urllib.request

sha = sys.argv[1]
url = f"https://api.github.com/repos/banana-orama/zuhausebleiben-kompass/commits/{sha}/check-runs"


def fetch():
    req = urllib.request.Request(url, headers={"User-Agent": "ci-check", "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


for attempt in range(30):
    d = fetch()
    runs = d.get("check_runs", [])
    if runs:
        print([(c["name"], c["status"], c["conclusion"]) for c in runs])
        if all(c["status"] == "completed" for c in runs):
            ok = all(c["conclusion"] == "success" for c in runs)
            print("CI:", "success" if ok else "NOT-GREEN")
            sys.exit(0 if ok else 1)
    time.sleep(15)
print("CI: timeout - runs not completed")
sys.exit(2)
