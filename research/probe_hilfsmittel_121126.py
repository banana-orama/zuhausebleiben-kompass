#!/usr/bin/env python3
"""Probe: Wo steht 'tragbar oder mitnehmbar' (Hilfsmittel-Definition)?"""
import re, html, pathlib
EVID = pathlib.Path('research/evidence/krankenhaus-121126')
for name in ['probe-__33.html', 'probe-__47.html']:
    raw = (EVID / name).read_bytes()
    head = raw[:2000].decode('utf-8', 'replace')
    enc = 'iso-8859-1' if ('charset=iso-8859-1' in head.lower() or 'charset=windows-1252' in head.lower()) else None
    try:
        s = raw.decode(enc or 'utf-8')
    except UnicodeDecodeError:
        s = raw.decode('iso-8859-1', 'replace')
    s = re.sub(r'(?s)<[^>]+>', ' ', s)
    s = html.unescape(s)
    s = re.sub(r'\s+', ' ', s)
    for m in re.finditer(r'[^.]*tragbar[^.]*\.', s):
        print(name, '->', m.group(0).strip()[:220])
    tit = re.search(r'§ ?\d+[a-z]? [A-ZÄÖÜ][^.(]{0,60}', s)
    print(name, 'TITEL:', tit.group(0) if tit else '?')
