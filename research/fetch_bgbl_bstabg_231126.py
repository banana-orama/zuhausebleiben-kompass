#!/usr/bin/env python3
# 23.11.2026: BGBl GKV-Beitragssatzstabilisierungsgesetz (2026 I Nr. 228) laden
# und § 61 SGB V-Änderung + Inkrafttreten extrahieren (pdftotext, verbatim).
import urllib.request, os, subprocess, sys

OUT = os.path.join(os.path.dirname(__file__), "evidence", "hilfsmittel-zuzahl-231126")
os.makedirs(OUT, exist_ok=True)
PDF = os.path.join(OUT, "bgbl-2026-i-228-gkv-bstabg.pdf")
from urllib.parse import quote
URL = "https://www.kvn.de/media/Mitglieder/Verordnungen/Arzneimittel/Gesetze_Vereinbarungen/2026-07-29_V" + "%C3%96" + "_BGBlatt_GKV-BStabG.pdf"

if not os.path.exists(PDF):
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    open(PDF, "wb").write(data)
    print(f"saved {len(data)} bytes")
else:
    print("cached")

txt_path = os.path.join(OUT, "bgbl-2026-i-228-gkv-bstabg.txt")
subprocess.run(["pdftotext", "-layout", PDF, txt_path], check=True)
txt = open(txt_path, encoding="utf-8", errors="replace").read()
print(f"pdftotext: {len(txt)} chars")

# Header/Erkennung
for needle in ["Beitragssatzstabilisierungsgesetz", "Nr. 228", "24. Juli 2026", "29. Juli 2026"]:
    print(f"  header '{needle}': {txt.count(needle)}")

# § 61 Änderung
i = txt.find("§ 61")
print("\n=== Kontext um '§ 61' (Änderungsanweisung) ===")
if i >= 0:
    print(txt[max(0, i - 600): i + 1400])
else:
    print("'§ 61' NICHT gefunden — Suche nach 'Zuzahlungen' …")
    j = txt.find("Zuzahlungen")
    print(txt[max(0, j - 400): j + 1200] if j >= 0 else "auch nicht")

print("\n=== Inkrafttreten ===")
k = txt.find("Inkrafttreten")
print(txt[k - 200: k + 900] if k >= 0 else "kein 'Inkrafttreten'-Wort")

print("\n=== Betrags-Needles im PDF-Text ===")
for n in ["7,50 Euro", "15 Euro", "5 Euro", "10 Euro", "mindestens", "höchstens", "10 vom Hundert"]:
    print(f"  '{n}': {txt.count(n)}")
