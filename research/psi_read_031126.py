#!/usr/bin/env python3
"""PSI-Baseline/-Nachmessung Audit #10 (perf/og) — liest gespeicherte PSI-JSONs aus."""
import json, sys, pathlib

EV = pathlib.Path(__file__).parent / 'evidence' / 'perf-og-031126'
for name in sys.argv[1:]:
    p = EV / name
    if not p.exists():
        print(f'{name}: FEHLT')
        continue
    d = json.loads(p.read_text())
    if 'error' in d:
        print(f'{name}: PSI-ERROR: {d["error"].get("message")}')
        continue
    lr = d.get('lighthouseResult', {})
    a = lr.get('audits', {})
    print(f'--- {name}: perf score={lr.get("score")}')
    for k in ['first-contentful-paint', 'largest-contentful-paint', 'total-blocking-time', 'speed-index', 'cumulative-layout-shift', 'interactive']:
        print(f'  {k}: {a.get(k, {}).get("displayValue")}')
    le = d.get('loadingExperience', {})
    print(f'  CrUX: {le.get("overall_category", "EMPTY")} metrics={list(le.get("metrics", {}).keys())}')
