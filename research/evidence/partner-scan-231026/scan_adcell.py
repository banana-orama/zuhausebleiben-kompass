#!/usr/bin/env python3
"""ADCELL-Programmseiten: Konditionen/Bedingungen extrahieren."""
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

for name, keys in [
    ("adcell-pflegehase-hausnotruf.html", ["Provision", "Lead", "Cookie", "SEM", "Bedingungen", "aktualisiert", "Tunstall", "Pflegekasse", "Widerruf", "Storno", "25,00"]),
    ("adcell-pflegehase.html", ["Provision", "Lead", "Cookie", "SEM", "Bedingungen", "aktualisiert", "62", "70"]),
]:
    t = txt(raw(name))
    print(f"\n===== {name} ({len(t)} chars) =====")
    low = t.lower()
    for k in keys:
        i = low.find(k.lower())
        if i >= 0:
            print(f"  [{k}] ...{t[max(0,i-160):i+300]}...")
        else:
            print(f"  [{k}] NICHT GEFUNDEN")
