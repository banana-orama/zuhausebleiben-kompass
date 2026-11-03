#!/usr/bin/env python3
"""CI-Status für Commit 3bf52d1 via öffentlicher GitHub-API lesen; dann optional Live-Readback."""
import json, sys, time, urllib.request

SHA = sys.argv[1] if len(sys.argv) > 1 else '3bf52d1'
WAIT = len(sys.argv) > 2 and sys.argv[2] == '--wait'
if len(SHA) < 40:
    import urllib.request as _u
    with _u.urlopen(f'https://api.github.com/repos/banana-orama/zuhausebleiben-kompass/commits/{SHA}', timeout=30) as _r:
        SHA = json.load(_r)['sha']

def runs():
    url = f'https://api.github.com/repos/banana-orama/zuhausebleiben-kompass/actions/runs?head_sha={SHA}'
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r).get('workflow_runs', [])

for attempt in range(60):
    rs = runs()
    if rs:
        r = rs[0]
        print(f"attempt {attempt}: {r['name']} status={r['status']} conclusion={r['conclusion']} id={r['id']}")
        if r['status'] == 'completed':
            sys.exit(0 if r['conclusion'] == 'success' else 1)
    else:
        print(f'attempt {attempt}: noch kein Run')
    if not WAIT:
        sys.exit(2)
    time.sleep(15)
sys.exit(3)
