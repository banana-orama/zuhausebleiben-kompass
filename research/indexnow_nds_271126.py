#!/usr/bin/env python3
"""IndexNow-Submission Region Niedersachsen, 27.11. (neue Region + Homepage; key aus dist/indexnow-key.txt)."""
import json, urllib.request, urllib.error
from pathlib import Path
key = Path("dist/indexnow-key.txt").read_text().strip()
host = "zuhausebleiben-kompass.de"
base = f"https://{host}"
urls = [base + "/region/niedersachsen.html", base + "/"]
payload = json.dumps({"host": host, "key": key, "keyLocation": base + "/indexnow-key.txt", "urlList": urls}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=payload, headers={"Content-Type": "application/json; charset=utf-8"})
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        print("IndexNow HTTP", r.status)
except urllib.error.HTTPError as e:
    print("IndexNow HTTP", e.code, e.read()[:200])
