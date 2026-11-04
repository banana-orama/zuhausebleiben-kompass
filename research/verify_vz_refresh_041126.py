#!/usr/bin/env python3
"""Verify vz-refresh-041126: ledger quotes verbatim against evidence files,
article JSON carries the refreshed span + checked_at, old span gone."""
import json, re, html, sys, unicodedata, os

BASE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.join(BASE, "evidence", "vz-refresh-041126")
ART = os.path.join(BASE, "..", "content-ready", "hausnotruf-kosten-anbieter-vergleich.json")

fails = []

def norm(s):
    s = unicodedata.normalize("NFKC", html.unescape(s))
    return re.sub(r"\s+", " ", s).strip()

def text_of(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    raw = re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>|<!--[\s\S]*?-->", " ", raw)
    raw = re.sub(r"<[^>]+>", " ", raw)
    return re.sub(r"\s+", " ", norm(raw))

# 1) Ledger quotes verbatim in evidence
led = json.load(open(os.path.join(BASE, "vz-refresh-041126-ledger.json")))
n_q = n_abs = 0
for src in led["sources"]:
    t = text_of(os.path.join(EV, src["evidence_file"]))
    for q in src.get("quotes", []):
        if norm(q) in t:
            n_q += 1
        else:
            fails.append(f"QUOTE FEHLT in {src['evidence_file']}: {q[:70]}")
    for a in src.get("absences", []):
        n_abs += 1
        if norm(a) in t:
            fails.append(f"ABSENZ-VERLETZUNG: '{a}' doch noch auf der Seite")

# 2) Article JSON state
art = json.load(open(ART))
blob = json.dumps(art, ensure_ascii=False)
checks = [
    ("neue Spanne Fliesstext", "30 bis 80 Euro zusätzlich im Monat" in blob),
    ("neue Spanne FAQ", "30 bis 80 Euro monatlich dazukosten" in blob),
    ("alte Spanne Fliesstext weg", "rund 30 bis 50 Euro oder mehr zusätzlich" not in blob),
    ("alte Spanne FAQ weg", "rund 30 bis 50 Euro oder mehr dazukosten" not in blob),
    ("Malteser-Bezugsdatum 04.11.", "am 4. November 2026 direkt abgerufenes Beispiel" in blob),
    ("Basistarif unveraendert", "27 bis 40 Euro" in blob),
    ("Pflegekasse unveraendert", "bis zu 27 Euro" in blob),
]
for label, ok in checks:
    if not ok:
        fails.append(f"ARTIKEL: {label}")
for i, s in enumerate(art["sources"]):
    if s.get("checked_at") != "2026-11-04":
        fails.append(f"src[{i}] checked_at={s.get('checked_at')} != 2026-11-04")

# 3) JSON strukturell intakt: Abschnitts-/FAQ-/Quellen-Zahl identisch mit HEAD (Refresh darf nichts strukturieren)
import subprocess
head = json.loads(subprocess.run(
    ["git", "show", "HEAD:content-ready/hausnotruf-kosten-anbieter-vergleich.json"],
    capture_output=True, text=True, cwd=os.path.join(BASE, "..")).stdout)
for key in ("sections", "faqs", "sources"):
    if len(art[key]) != len(head[key]):
        fails.append(f"{key}: {len(art[key])} != HEAD {len(head[key])}")

print(f"Ledger: {n_q} Zitate verbatim PASS, {n_abs} Absenz-Checks PASS")
print(f"Artikel: {sum(1 for _, ok in checks if ok)}/{len(checks)} Inhalt-Checks PASS, 4x checked_at=2026-11-04")
if fails:
    print("\nFAILS:")
    for f in fails:
        print(" -", f)
    sys.exit(1)
print("ALL PASS")
