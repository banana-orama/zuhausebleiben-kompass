#!/usr/bin/env python3
"""IndexNow-Submit Phase-2 18.11.2026: 6 geaenderte URLs (blitz-seo interne Links + unslop)."""
import json
import pathlib
import urllib.request

host = "zuhausebleiben-kompass.de"
key = pathlib.Path("indexnow-key.txt").read_text().strip()
urls = [
    "https://zuhausebleiben-kompass.de/treppenlift-zuschuss.html",
    "https://zuhausebleiben-kompass.de/treppenlift-kosten.html",
    "https://zuhausebleiben-kompass.de/treppenlift-mieten.html",
    "https://zuhausebleiben-kompass.de/treppenlift-finanzierung.html",
    "https://zuhausebleiben-kompass.de/treppenlift-angebote-vergleichen.html",
    "https://zuhausebleiben-kompass.de/treppenlift-steuerlich-absetzen.html",
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
    print("IndexNow HTTP", r.status, f"({len(urls)} URLs)")
