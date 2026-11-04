#!/usr/bin/env python3
"""Live-Readback vz-refresh-041126 auf der oeffentlichen URL (nach Deploy)."""
import re, sys, urllib.request, gzip, io

URL = "https://zuhausebleiben-kompass.de/hausnotruf-kosten-anbieter-vergleich.html"
req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)", "Accept-Encoding": "gzip"})
with urllib.request.urlopen(req, timeout=60) as r:
    status = r.status
    raw = r.read()
    if r.headers.get("Content-Encoding") == "gzip":
        raw = gzip.GzipFile(fileobj=io.BytesIO(raw)).read()
    html_text = raw.decode("utf-8", errors="replace")

fails = []
def check(label, ok):
    if not ok:
        fails.append(label)

check("HTTP 200", status == 200)
m = re.search(r'<meta name="robots" content="([^"]+)"', html_text)
check("robots index,follow", bool(m) and m.group(1) == "index,follow")
check("neue Spanne Body", "30 bis 80 Euro zusätzlich im Monat" in html_text)
check("neue Spanne FAQ", "30 bis 80 Euro monatlich dazukosten" in html_text)
check("alte Spanne weg", "30 bis 50 Euro oder mehr" not in html_text)
check("Quellenstand 04.11.", "Quellenstand: 2026-11-04" in html_text)
check("4x geprüft 04.11.", html_text.count("geprüft 2026-11-04") == 4)
sm = re.search(r'<script type="application/ld\+json">([\s\S]*?)</script>', html_text)
check("SchemaFAQ 30-80", bool(sm) and "30 bis 80 Euro" in sm.group(1))
n_cta = html_text.count("malteser_beratungstermin") + html_text.count("malteser_info_material")
check("beide Placement-IDs", n_cta >= 2)
has_sponsored = 'rel="sponsored' in html_text
check('rel="sponsored"', has_sponsored)
check("Beratungstermin-Tracker", "awinmid=112616" in html_text and "beratungstermin-buchen.html" in html_text)
check("Info-Material-Tracker", "informationen-anfordern.html" in html_text)
check("Basistarif unverändert", "27 bis 40 Euro" in html_text)
check("Pflegekasse unverändert", "bis zu 27 Euro" in html_text)

print(f"HTTP {status}, {len(html_text)}B")
print(f"Placement-Marker: {n_cta}, sponsored: {has_sponsored}")
if fails:
    print("FAILS:", fails)
    sys.exit(1)
print("LIVE-READBACK ALL PASS")
