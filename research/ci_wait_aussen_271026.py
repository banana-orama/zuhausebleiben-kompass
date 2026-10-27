#!/usr/bin/env python3
"""CI-Status des neuesten Commits via oeffentliche GitHub-API."""
import json
import pathlib
import subprocess
import time
import urllib.request

REPO = 'banana-orama/zuhausebleiben-kompass'
sha = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True, cwd=pathlib.Path(__file__).resolve().parent.parent).stdout.strip()
print('HEAD:', sha[:10])

deadline = time.time() + 420
while time.time() < deadline:
    with urllib.request.urlopen(f'https://api.github.com/repos/{REPO}/actions/runs?head_sha={sha}&per_page=5', timeout=45) as r:
        d = json.load(r)
    runs = d.get('workflow_runs', [])
    if runs:
        for w in runs:
            print(w['name'], '|', w['status'], '|', w['conclusion'])
        if all(w['status'] == 'completed' for w in runs):
            ok = all(w['conclusion'] == 'success' for w in runs)
            print('CI DONE:', 'success' if ok else 'FAILURE')
            raise SystemExit(0 if ok else 1)
    else:
        print('noch kein Run fuer HEAD, warte...')
    time.sleep(30)
print('TIMEOUT: CI nicht abgeschlossen')
raise SystemExit(2)
