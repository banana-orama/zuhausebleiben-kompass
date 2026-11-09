#!/usr/bin/env python3
"""Wartet auf den CI-Run des Förder-Prüflauf-Commits 1279a39 (volle SHA-Assertion)
und gibt Status/Conclusion aus. Exit 0 nur bei conclusion == success."""
import subprocess
import sys
import time

FULL_SHA = sys.argv[1] if len(sys.argv) > 1 else '1279a3902f09d5695970161aa8be9ac3bd88bc26'
head = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True, cwd='/Users/mac/agentic-business/barrierefrei-leads').stdout.strip()
if head != FULL_SHA:
    print(f'FEHLER: lokale HEAD {head} != Commit unter Test {FULL_SHA}')
    sys.exit(2)

deadline = time.time() + 900
while time.time() < deadline:
    r = subprocess.run(
        ['gh', 'run', 'list', '--commit', FULL_SHA, '--limit', '5',
         '--json', 'databaseId,status,conclusion,displayTitle'],
        capture_output=True, text=True)
    if r.returncode != 0:
        print(f'gh run list Fehler: {r.stderr.strip()}')
        sys.exit(2)
    import json
    runs = json.loads(r.stdout or '[]')
    if not runs:
        print('… noch kein Run für SHA registriert, warte')
        time.sleep(20)
        continue
    run = runs[0]
    print(f"run {run['databaseId']}: {run['status']} {run.get('conclusion') or ''}")
    if run['status'].lower() == 'completed':
        if (run.get('conclusion') or '').lower() == 'success':
            print(f'CI SUCCESS für {FULL_SHA[:12]} (run {run["databaseId"]})')
            sys.exit(0)
        print(f'CI FEHLGESCHLAGEN: conclusion={run.get("conclusion")}')
        sys.exit(1)
    time.sleep(20)
print('TIMEOUT nach 900 s — CI-Status ungeklärt')
sys.exit(3)
