#!/usr/bin/env python3
# 23.11.2026: GKV-SV-PM als committed Extrakt (Roh-HTML bleibt uncommitted).
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
EV = ROOT / "research/evidence/hilfsmittel-zuzahl-231126"
raw = (EV / "gkvsp-pm-2293952-231126.html").read_bytes().decode("utf-8", errors="replace")
t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S | re.I)
t = re.sub(r"<[^>]+>", " ", t)
t = t.replace("\xa0", " ")
t = re.sub(r"[ \t]+", " ", t)
lines = [l.strip() for l in t.splitlines() if l.strip()]
out = ["GKV-Spitzenverband Pressemitteilung 2293952 (27.07.2026) — Extrakt 23.11.2026,",
       "Roh-HTML uncommitted; Zitate verbatim gegen diese Datei geprüft (verify_hilfsmittel_zuzahl_231126.py).", ""]
keep = []
for i, l in enumerate(lines):
    if "Zuzahlung" in l or "ab 2027" in l:
        keep.append(lines[max(0, i - 1): i + 2])
seen = set()
for grp in keep:
    for l in grp:
        if l not in seen and len(l) > 60:
            seen.add(l)
            out.append(l)
            out.append("")
(EV / "gkvsp-pm-extract-231126.txt").write_text("\n".join(out), encoding="utf-8")
print("Extrakt geschrieben:", len("\n".join(out)), "Zeichen,", len(seen), "Absätze")
for needle in ["mindestens 5 Euro (ab 2027: 7,50 Euro)", "höchstens 10 Euro (ab 2027: 15 Euro)"]:
    print(f"  '{needle}':", "\n".join(out).count(needle))
