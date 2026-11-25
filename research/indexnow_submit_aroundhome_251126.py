#!/usr/bin/env python3
"""IndexNow-Submit der Aroundhome-Aktivierung (25.11.2026, nach Deploy).
Geänderte Seiten: 5 Bad-Cluster-Artikel (neue Placements) + datenschutz.html
(neuer Abschnitt-6-Anbieter) + Homepage. Key aus dist/indexnow-key.txt."""
import json
import pathlib
import urllib.request

host = "zuhausebleiben-kompass.de"
key = pathlib.Path("/Users/mac/agentic-business/barrierefrei-leads/dist/indexnow-key.txt").read_text().strip()
payload = {
    "host": host,
    "key": key,
    "keyLocation": f"https://{host}/indexnow-key.txt",
    "urlList": [
        f"https://{host}/badumbau-angebote-vergleichen.html",
        f"https://{host}/bad-umbau-barrierefrei.html",
        f"https://{host}/badumbau-kosten.html",
        f"https://{host}/wanne-zur-dusche.html",
        f"https://{host}/bodengleiche-dusche-altbau.html",
        f"https://{host}/datenschutz.html",
        f"https://{host}/",
    ],
}
req = urllib.request.Request(
    "https://api.indexnow.org/indexnow",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": "Mozilla/5.0 (indexnow-submit)"},
)
with urllib.request.urlopen(req, timeout=30) as r:
    print("HTTP", r.status)
    print(len(payload["urlList"]), "URLs submitted")
