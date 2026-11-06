#!/usr/bin/env python3
"""CI-Status für Commit f45f50f abfragen (öffentliche API, bis completed oder Timeout)."""
import json
import time
import urllib.request

SHA = "f45f50fe679e5af5e814d9bb64a20c609fec67d2"
URL = f"https://api.github.com/repos/banana-orama/zuhausebleiben-kompass/actions/runs?head_sha={SHA}"
deadline = time.time() + 540
last = None
while time.time() < deadline:
    with urllib.request.urlopen(URL, timeout=30) as r:
        data = json.loads(r.read())
    runs = data.get("workflow_runs", [])
    if runs:
        run = runs[0]
        last = (run["status"], run["conclusion"], run["html_url"])
        if run["status"] == "completed":
            print("CI:", run["status"], run["conclusion"], run["html_url"])
            break
    time.sleep(20)
else:
    print("CI-TIMEOUT, letzter Stand:", last)
    raise SystemExit(2)
if last and last[1] != "success":
    raise SystemExit(1)
