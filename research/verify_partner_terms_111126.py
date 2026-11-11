#!/usr/bin/env python3
"""Machine re-verification of the 11.11.2026 partner-terms ledger:
1) every ledger quote appears verbatim in the committed evidence extract,
2) live funnel order: beratungstermin placement before info_material,
3) sources block in the memo matches the ledger ids.
Exit 0 = all pass. Convention: research/verify_*_YYYYMMDD.py."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "research/partner-terms-111126-ledger.json"
EVID = ROOT / "research/evidence/partner-terms-111126"
MEMO = ROOT / "research/accepted-lead-economics-111126.md"

EVIDENCE_FILES = {
    1: "malteser_awin_profile_111126.txt",
    2: "lifta_awin_profile_111126.txt",
    3: "hiro_adcell_111126.txt",
    4: "lotse_100pp_111126.txt",
    5: "lotse_impressum_111126.txt",
    6: "zentrum_impressum_111126.txt",
    7: "live_hausnotruf_vergleich_111126.txt",
    8: "hib_884_2026_111126.txt",
    9: "bt_textarchiv_kw45_111126.txt",
}

def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().lower()

fails = 0
data = json.loads(LEDGER.read_text(encoding="utf-8"))
entries = data if isinstance(data, list) else data.get("sources", data)
by_id = {}
for e in entries:
    sid = e.get("id") or e.get("n")
    by_id[int(sid)] = e

# 1) verbatim quotes
for sid, fname in sorted(EVIDENCE_FILES.items()):
    hay = norm((EVID / fname).read_text(encoding="utf-8"))
    quotes = by_id[sid].get("quotes", [])
    if not quotes:
        print(f"FAIL [{sid}] no quotes attached")
        fails += 1
        continue
    for q in quotes:
        text = q.get("text") if isinstance(q, dict) else q
        if norm(text) not in hay:
            print(f"FAIL [{sid}] quote not verbatim: {text!r}")
            fails += 1
    print(f"[{sid}] {len(quotes)} quote(s) verbatim in {fname}")

# 2) funnel order on live extract
live = (EVID / "live_hausnotruf_vergleich_111126.txt").read_text(encoding="utf-8")
i_bt = live.find("Kostenlosen Beratungstermin anfragen")
i_im = live.find("Infos per Post anfordern")
if i_bt == -1 or i_im == -1:
    print("FAIL funnel: button text missing on live extract")
    fails += 1
elif i_bt > i_im:
    print("FAIL funnel: beratungstermin CTA renders AFTER info_material (paying action not primary)")
    fails += 1
else:
    print(f"funnel order OK: beratungstermin@{i_bt} < info_material@{i_im}")

# 3) memo sources block ids == ledger ids
memo = MEMO.read_text(encoding="utf-8")
block = memo[memo.find("## Sources"):] if "## Sources" in memo else ""
block_ids = sorted(set(int(m) for m in re.findall(r"^\[(\d+)\]", block, re.M)))
memo_ids = sorted(set(int(m) for m in re.findall(r"\.\[(\d+)\]", memo)))
missing_in_block = [i for i in memo_ids if i not in block_ids]
unknown = [i for i in memo_ids if i not in by_id]
if unknown:
    print(f"FAIL memo cites unknown ids: {unknown}")
    fails += 1
if missing_in_block:
    print(f"FAIL memo ids missing from Sources block: {missing_in_block}")
    fails += 1
print(f"memo: {len(memo_ids)} distinct inline ids, Sources block covers {len(block_ids)}")

if fails:
    print(f"\nRESULT: {fails} FAIL(s)")
    sys.exit(1)
print("\nRESULT: ALL PASS")
