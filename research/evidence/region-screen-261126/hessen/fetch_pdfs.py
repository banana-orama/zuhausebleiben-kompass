#!/usr/bin/env python3
"""Fetch WIBank PDFs, pdftotext, strip soft hyphens, needle-count."""
import subprocess, os, re, sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"

PDFS = {
    "wibank-richtlinie": "https://www.wibank.de/resource/blob/wibank/306346/39845aeb7d0d5a93fc4aa1b251a398e0/richtlinie-behindertengerechter-umbau-von-wohneigentum-data.pdf",
    "wibank-foerderstellen": "https://www.wibank.de/resource/blob/wibank/306310/fb82459dcaa2e32209314e2a623f8896/wohnungsbaufoerderstellen-hessen-baudarlehen-et-all-data.pdf",
}

NEEDLES = ["Treppenlift", "Treppenlifte", "Treppenlift-", "Lift", "Aufzug", "Treppenschrägaufzug",
           "15.000", "6.500", "5.500", "3.000", "30.000", "1.500", "50 %", "DIN 18040",
           "Einkommen", "Pflegegrad", "Grad der Behinderung", "Richtlinie", "Wohneinheit"]

for stem, url in PDFS.items():
    raw = f"raw-{stem}.pdf"
    if not os.path.exists(raw) or os.path.getsize(raw) < 10000:
        subprocess.run(["curl", "-sL", "-A", UA, "--max-time", "120", "-o", raw, url], check=True)
    kind = subprocess.run(["file", raw], capture_output=True, text=True).stdout.strip()
    print(f"{raw}: {kind[:80]} size={os.path.getsize(raw)}")
    subprocess.run(["pdftotext", "-layout", raw, f"{stem}-pdftotext.txt"], check=False)
    with open(f"{stem}-pdftotext.txt", encoding="utf-8", errors="replace") as fh:
        t = fh.read().replace("\u00ad", "")
    with open(f"{stem}.txt", "w", encoding="utf-8") as fh:
        fh.write(t)
    print(f"{stem}.txt chars: {len(t)}")
    for n in NEEDLES:
        c = t.count(n)
        if c:
            print(f"   {n}: {c}")
