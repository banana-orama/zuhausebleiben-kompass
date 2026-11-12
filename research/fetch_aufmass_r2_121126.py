#!/usr/bin/env python3
"""Fetch round 2: VZ planung article, VZ umfrage PDF, Lifta landing/FAQ, BGB 312g, HIRO paths."""
import subprocess, os

E = "research/evidence/aufmass-121126"
os.makedirs(E, exist_ok=True)
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"

TARGETS = [
    ("vz-planung", "https://www.verbraucherzentrale.de/wissen/gesundheit-pflege/pflege-zu-hause/treppenlifte-das-muessen-sie-ueber-planung-und-umsetzung-wissen-10711"),
    ("lifta-haupt", "https://www.lifta.de/treppenlift/"),
    ("lifta-faq", "https://www.lifta.de/faq"),
    ("bgb-312g", "https://www.gesetze-im-internet.de/bgb_312g/__312g.html"),
    ("hiro-haupt", "https://www.hiro.de/treppenlifte"),
]

for name, url in TARGETS:
    out = f"{E}/{name}.html"
    r = subprocess.run(["curl", "-sL", "-A", UA, "-m", "30", url, "-o", out, "-w", "%{http_code} %{size_download}"],
                       capture_output=True, text=True, timeout=40)
    print(f"{name}: {r.stdout.strip()}  {url}")

# VZ Umfrage PDF
pdf = f"{E}/vz-umfrage.pdf"
r = subprocess.run(["curl", "-sL", "-A", UA, "-m", "60", 
                    "https://www.verbraucherzentrale.de/sites/default/files/2021-01/Auswertung_Treppenlift_Umfrage_online_0.pdf",
                    "-o", pdf, "-w", "%{http_code} %{size_download}"],
                   capture_output=True, text=True, timeout=70)
print(f"vz-umfrage.pdf: {r.stdout.strip()}")
r = subprocess.run(["pdftotext", pdf, f"{E}/vz-umfrage.txt"], capture_output=True, text=True)
print("pdftotext:", r.returncode, r.stderr[:200])
