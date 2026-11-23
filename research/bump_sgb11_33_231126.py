#!/usr/bin/env python3
# 23.11.2026: hilfsmittel-pflegekasse sources[0] (§ 33 SGB XI) checked_at -> 2026-11-23
# (heute live abgerufen + Needles verifiziert, s. fetch_sgb11_33_231126.py).
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
p = ROOT / "content-ready/hilfsmittel-pflegekasse-uebernahme.json"
t = p.read_text(encoding="utf-8")
RE = re.compile(r'("url": "https://www\.gesetze-im-internet\.de/sgb_11/__33\.html",\s*\n\s*"checked_at": ")([^"]+)(")')
m = RE.search(t)
assert m, "§ 33 SGB XI Block nicht gefunden"
assert m.group(2) != "2026-11-23", "bereits gebumpt"
t = RE.sub(r"\g<1>2026-11-23\g<3>", t, count=1)
json.loads(t)
p.write_text(t, encoding="utf-8")
print("§ 33 SGB XI checked_at:", m.group(2), "-> 2026-11-23, Parse OK")
