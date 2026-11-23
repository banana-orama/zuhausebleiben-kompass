#!/usr/bin/env python3
"""Independent verifier for weg-231126 deliverables.
Re-reads ledger-legal.json and the cleaned source files from disk and checks:
  1. JSON schema: every entry has the 5 required keys, quote non-empty
  2. every quote is a literal substring of the corresponding cleaned text
  3. every quote appears inside a fenced block in legal-extracts.md
  4. no dotted-number patterns were used in verification (literal `in` only)
"""
import json
from pathlib import Path

EV = Path("/Users/mac/agentic-business/barrierefrei-leads/research/evidence/weg-231126")
RAW = EV / "raw"

ledger = json.loads((EV / "ledger-legal.json").read_text(encoding="utf-8"))
assert 20 <= len(ledger) <= 35, f"quote count {len(ledger)} outside 20-35"

# map source_id prefix -> cleaned text file
TXT = {
    "weg-": RAW / "wegg-full.txt",
}
def text_for(entry):
    sid = entry["source_id"]
    url = entry["url"]
    if "woeigg/__20" in url: return (RAW / "wegg__20.txt").read_text(encoding="utf-8")
    if "woeigg/__21" in url: return (RAW / "wegg__21.txt").read_text(encoding="utf-8")
    if "woeigg/__44" in url: return (RAW / "wegg__44.txt").read_text(encoding="utf-8")
    if "BJNR001750951" in url: return (RAW / "wegg-full.txt").read_text(encoding="utf-8")
    if "V_ZR__33-23.pdf" in url: return (RAW / "vzr-33-23.flat.txt").read_text(encoding="utf-8")
    if "V_ZR_244-22.pdf" in url: return (RAW / "vzr-244-22.flat.txt").read_text(encoding="utf-8")
    if "2024026.html" in url: return (RAW / "pm-026-2024.txt").read_text(encoding="utf-8")
    raise KeyError(url)

md = (EV / "legal-extracts.md").read_text(encoding="utf-8")

fail = 0
urls = set()
for e in ledger:
    for k in ("source_id", "url", "title", "quote", "context_note"):
        if not e.get(k) or not isinstance(e[k], str):
            print(f"FAIL {e.get('source_id')}: missing/empty {k}"); fail += 1
    t = text_for(e)
    q = e["quote"]
    if q not in t:  # literal containment only - no regex, no dotted patterns
        print(f"FAIL {e['source_id']}: quote NOT a literal substring of cleaned text")
        fail += 1
    if f"\n{q}\n" not in md:
        print(f"FAIL {e['source_id']}: quote not found verbatim inside md fenced block")
        fail += 1
    urls.add(e["url"])

print(f"entries: {len(ledger)} | distinct URLs: {len(urls)} | failures: {fail}")
for u in sorted(urls):
    print(" URL:", u)
# spot checks mandated by the task
t20 = (RAW / "wegg__20.txt").read_text(encoding="utf-8")
t21 = (RAW / "wegg__21.txt").read_text(encoding="utf-8")
assert "Stromerzeugung durch Steckersolargeräte" in t20          # current version, post 10.10.2024
assert "hat dieser Wohnungseigentümer zu tragen" in t21          # § 21 Abs. 1 Satz 1 cost sentence
t244 = (RAW / "vzr-244-22.flat.txt").read_text(encoding="utf-8")
assert "§ 275 Abs. 1 BGB" in t244
assert "ist unerheblich" in t244
t33 = (RAW / "vzr-33-23.flat.txt").read_text(encoding="utf-8")
assert "Regel-Ausnahme-Verhältnisses Rechnung zu tragen" in t33
print("spot checks: OK")
raise SystemExit(1 if fail else 0)
