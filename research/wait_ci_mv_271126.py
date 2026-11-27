#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wartet auf CI-Run der vollen SHA 5d46c135314cc9075fde0a1ab972d5f834f82db5 und gibt das Ergebnis aus."""
import json
import sys
import time
import urllib.request

SHA = "5d46c135314cc9075fde0a1ab972d5f834f82db5"
REPO = "banana-orama/zuhausebleiben-kompass"
UA = {"User-Agent": "ci-wait", "Accept": "application/vnd.github+json"}

deadline = time.time() + 15 * 60
seen = {}
while time.time() < deadline:
    try:
        req = urllib.request.Request(
            f"https://api.github.com/repos/{REPO}/commits/{SHA}/check-runs", headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read())
        runs = data.get("check_runs", [])
        summary = {}
        for c in runs:
            summary[c["name"]] = (c["status"], c.get("conclusion"))
        key = json.dumps(summary, sort_keys=True)
        if key != seen.get("last"):
            print(time.strftime("%H:%M:%S"), summary, flush=True)
            seen["last"] = key
        done = [c for c in runs if c["status"] == "completed"]
        if runs and len(done) == len(runs):
            fails = [c["name"] for c in done if c.get("conclusion") != "success"]
            if fails:
                print("CI FAILED:", fails)
                sys.exit(1)
            print("CI SUCCESS auf voller SHA (%d runs)" % len(done))
            sys.exit(0)
    except Exception as e:
        print("poll-err", e, flush=True)
    time.sleep(20)
print("TIMEOUT ohne abgeschlossene CI")
sys.exit(2)
