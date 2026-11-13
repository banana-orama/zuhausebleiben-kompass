#!/usr/bin/env python3
"""IndexNow-Submission Region NRW (13.11.2026): neue indexierbare URL (+ Homepage).
Key aus dist/indexnow-key.txt (deployed); submit NACH dem Deploy."""
import json
import urllib.request
from pathlib import Path

key = Path("/Users/mac/agentic-business/barrierefrei-leads/dist/indexnow-key.txt").read_text().strip()
host = "zuhausebleiben-kompass.de"
urls = [
    "https://zuhausebleiben-kompass.de/region/nordrhein-westfalen.html",
    "https://zuhausebleiben-kompass.de/",
]
payload = {
    "host": host,
    "key": key,
    "keyLocation": f"https://{host}/indexnow-key.txt",
    "urlList": urls,
}
req = urllib.request.Request(
    "https://api.indexnow.org/indexnow",
    data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": "Mozilla/5.0 (indexnow-submit)"},
    method="POST",
)
with urllib.request.urlopen(req, timeout=30) as r:
    print("IndexNow HTTP", r.status)
    sys_exit = 0 if r.status == 200 else 1
raise SystemExit(sys_exit)
