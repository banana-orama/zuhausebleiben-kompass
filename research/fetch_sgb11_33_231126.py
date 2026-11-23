#!/usr/bin/env python3
# 23.11.2026: § 33 SGB XI live abrufen (Quellenstand-Bump-Grundlage für hilfsmittel-pflegekasse)
# + rollator/duschwc sources[0]-checked_at lesen + Checklisten-Grep.
import html
import json
import pathlib
import re
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
EV = ROOT / "research/evidence/hilfsmittel-zuzahl-231126"
EV.mkdir(parents=True, exist_ok=True)

req = urllib.request.Request(
    "https://www.gesetze-im-internet.de/sgb_11/__33.html",
    headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"},
)
with urllib.request.urlopen(req, timeout=45) as r:
    data = r.read()
    status = r.status
(EV / "sgb11-33-231126.html").write_bytes(data)
print("sgb11-33 fetch:", status, len(data), "bytes")

raw = data.decode("iso-8859-1", errors="replace")
txt = re.sub(r"<[^>]+>", " ", raw)
txt = html.unescape(txt).replace("\xa0", " ")
txt = re.sub(r"\s+", " ", txt)
i = txt.find("Anspruch")
print("--- § 33 SGB XI (Anspruch-Kern) ---")
print(txt[i:i + 520])

for needle in ["auf Antrag", "mindestens zwei Jahre", "vor der Antragstellung"]:
    print(f"  '{needle}': {txt.count(needle)}")

for slug in ["rollator-auswahl-passform-kosten", "hilfsmittel-dusch-wc-uebernahme"]:
    d = json.loads((ROOT / f"content-ready/{slug}.json").read_text(encoding="utf-8"))
    s0 = d["sources"][0]
    print(f"{slug} sources[0]: {s0['title']} | {s0['url']} | {s0['checked_at']}")

hits = [p.name for p in (ROOT / "dist/checklisten").glob("*.html")
        if "7,50" in p.read_text(encoding="utf-8", errors="replace")]
print("Checklisten mit 7,50:", hits or "keine")
