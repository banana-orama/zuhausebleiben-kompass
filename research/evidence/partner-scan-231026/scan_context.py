#!/usr/bin/env python3
"""Kontext-Greps: ADCELL-Bezug Pflegehase, Pflegehase-Homepage, Addrevenue-Programmseite."""
import re, pathlib

D = pathlib.Path(__file__).parent

def raw(name):
    b = (D / name).read_bytes()
    for enc in ("utf-8", "latin-1"):
        try:
            return b.decode(enc)
        except UnicodeDecodeError:
            continue
    return b.decode("utf-8", "replace")

def txt(s):
    s = re.sub(r"<script[\s\S]*?</script>", " ", s, flags=re.I)
    s = re.sub(r"<style[\s\S]*?</style>", " ", s, flags=re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", s)

print("== ADCELL-Kontext in Verzeichnisseite ==")
h = raw("affmarketing-pflegehase.html")
for m in re.finditer(r"ADCELL", h, re.I):
    ctx = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h[max(0, m.start()-400):m.start()+400]))
    print("  ...", ctx[:400], "...\n")

print("== PFLEGEHASE.DE Homepage: Kern ==")
t = txt(raw("pflegehase-home.html"))
print("LEN", len(t))
for k in ["Hausnotruf", "Partnerprogramm", "Affiliate", "Impressum", "GmbH", "Pflegekasse", "Angebot"]:
    hits = [m.start() for m in re.finditer(re.escape(k), t)][:2]
    for i in hits:
        print(f"  [{k}] ...{t[max(0,i-120):i+220]}...\n")

print("== ADDREVENUE 988118: Details ==")
t2 = txt(raw("addrevenue-988118.html"))
print("LEN", len(t2))
print(t2[:1800])
