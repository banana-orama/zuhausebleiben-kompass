#!/usr/bin/env python3
"""Fetch alle Quellen für Briefing 22 (unseriöse Treppenlift-Anbieter), Stand 10.11.2026."""
import os
import subprocess
import sys

D = "/Users/mac/agentic-business/barrierefrei-leads/research/evidence/unserioese-101126"
os.makedirs(D, exist_ok=True)

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"

SOURCES = [
    # (name, url)
    ("vz-treppenlifte-10711", "https://www.verbraucherzentrale.de/wissen/gesundheit-pflege/pflege-zu-hause/treppenlifte-das-muessen-sie-ueber-planung-und-umsetzung-wissen-10711"),
    ("vz-umfrage-auswertung", "https://www.verbraucherzentrale.de/sites/default/files/2021-01/Auswertung_Treppenlift_Umfrage_online_0.pdf"),
    ("vz-verbandsklage-mobilae", "https://www.verbraucherzentrale.de/verbandsklagen/klage-gegen-mobilae-126325"),
    ("uwg-4", "https://www.gesetze-im-internet.de/uwg/__4.html"),
    ("uwg-4a", "https://www.gesetze-im-internet.de/uwg/__4a.html"),
    ("uwg-5", "https://www.gesetze-im-internet.de/uwg/__5.html"),
    ("uwg-5a", "https://www.gesetze-im-internet.de/uwg/__5a.html"),
    ("bgb-312g", "https://www.gesetze-im-internet.de/bgb/__312g.html"),
    ("testde-windige-anbieter", "https://www.test.de/Treppenlift-Rechtslage-Kosten-Zuschuesse-Einbau-5848147-5848982/"),
]

ext_by_name = {"vz-umfrage-auswertung": "pdf"}
ok, fail = [], []
for name, url in SOURCES:
    ext = ext_by_name.get(name, "html")
    out = os.path.join(D, f"{name}.{ext}")
    cmd = ["curl", "-sL", "--max-time", "60", "-A", UA, "-w", "%{http_code}", "-o", out, url]
    r = subprocess.run(cmd, capture_output=True, text=True)
    code = r.stdout.strip()
    size = os.path.getsize(out) if os.path.exists(out) else 0
    status = "OK" if code == "200" and size > 2000 else "CHECK"
    print(f"{name}: HTTP {code}, {size} bytes -> {status}")
    (ok if status == "OK" else fail).append(name)

print(f"\nOK: {len(ok)}, CHECK: {len(fail)}: {fail}")
sys.exit(0)
