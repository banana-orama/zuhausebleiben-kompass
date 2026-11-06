#!/usr/bin/env python3
"""IndexNow-Submission fuer Briefing 18 (Artikel + Homepage; key aus dist/indexnow-key.txt)."""
import json
import urllib.request
from pathlib import Path

key = Path("/Users/mac/agentic-business/barrierefrei-leads/dist/indexnow-key.txt").read_text().strip()
host = "zuhausebleiben-kompass.de"
urls = [
    "https://zuhausebleiben-kompass.de/treppenlift-sitzlift-oder-stehlift.html",
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
