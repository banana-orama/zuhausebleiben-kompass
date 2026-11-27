#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Maschineller Verbatim-Check fuer Region-Screen Berlin+Bremen (27.11.2026).

Prueft JEDES Zitat aus research/region-screen-271126-berlin-bremen-ledger.json
verbatim gegen die gespeicherte Evidenz in
research/evidence/region-screen-271126/{berlin,bremen,shared}/.

Normalisierung (dokumentiert, deterministisch, identisch fuer Evidenz UND Zitat):
1. Soft-Hyphen (U+00AD) strippen (IBB/KfW-Falle).
2. Geschuetzte Leerzeichen (U+00A0 NBSP, U+202F schmales NBSP, U+2009) -> normales Leerzeichen.
3. De-Hyphenation am Zeilenumbruch: "Wort-\nrest" -> "Wortrest", AUSSER wenn das
   erste Zeichen des Nachlaufs ein Grossbuchstabe ist (echter Compound, z.B. "DVO-\nNWoFG").
4. Alle Whitespace-Laeufe -> je ein Leerzeichen; newlines -> Leerzeichen
   (pdftotext -layout und HTML-Extrakte erzeugen Tabellen-/Umbruchsabstaende).
5. case-sensitive Substring-Pruefung des normalisierten Zitats im normalisierten
   Evidenztext; Needles werden zusaetzlich case-insensitive gezaehlt.

Exit-Code 0 <=> alle Zitate PASS.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LEDGER = ROOT / "region-screen-271126-berlin-bremen-ledger.json"
EVIDENCE_DIR = ROOT / "evidence" / "region-screen-271126"

SOFT = "\u00ad"
SPACES = {"\u00a0": " ", "\u202f": " ", "\u2009": " ", "\u2007": " ", "\u2008": " "}


def dehyphenate_newline(m: "re.Match") -> str:
    pre, post = m.group(1), m.group(2)
    if post[:1].isupper():
        return pre + "-" + post
    return pre + post


def norm(text: str) -> str:
    t = text.replace(SOFT, "")
    for k, v in SPACES.items():
        t = t.replace(k, v)
    t = re.sub(r"(\S)-[ \t]*\n[ \t]*(\S)", dehyphenate_newline, t)
    t = t.replace("\r", "\n")
    t = t.replace("\n", " ")
    t = re.sub(r"\s+", " ", t)
    return t.strip()


def count_ci(haystack: str, needle: str) -> int:
    return len(re.findall(re.escape(needle), haystack, flags=re.IGNORECASE))


def main() -> int:
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    ev_dir = ROOT.parent / ledger.get(
        "evidence_dir", "research/evidence/region-screen-271126"
    )
    if not ev_dir.exists():
        ev_dir = ROOT / ledger.get("evidence_dir", "research/evidence/region-screen-271126")
    total, passed, failed = 0, 0, []
    needle_rows = []
    n_total, n_pass = 0, 0

    for src in ledger["sources"]:
        ev_names = src["evidence"] if isinstance(src["evidence"], list) else [src["evidence"]]
        ev_paths = [ev_dir / name for name in ev_names]
        if not any(p.exists() for p in ev_paths):
            failed.append((src["id"], src["label"], f"EVIDENZ-FEHLT: {ev_names}"))
            continue
        ev = " \n ".join(
            norm(p.read_text(encoding="utf-8", errors="replace"))
            for p in ev_paths
            if p.exists()
        )
        for q in src.get("quotes", []):
            total += 1
            if norm(q) in ev:
                passed += 1
            else:
                failed.append((src["id"], src["label"], f"QUOTE NICHT GEFUNDEN: {q[:120]}..."))
        for needle in src.get("needles", []) or []:
            cnt = count_ci(ev, needle)
            needle_rows.append(f"  src {src['id']:>2} Count-Needle '{needle}' -> {cnt} Treffer (Fallcount)")
        for needle, expected_count in (src.get("needles_absent") or {}).items():
            cnt = count_ci(ev, needle)
            ok = cnt == expected_count
            n_total += 1
            if ok:
                n_pass += 1
            needle_rows.append(
                f"  src {src['id']:>2} ABSenz-Needle '{needle}' -> {cnt} Treffer "
                f"(erwartet {expected_count}) {'PASS' if ok else 'FAIL'}"
            )

    print("=" * 78)
    print("Verbatim-Check Region-Screen Berlin+Bremen 271126")
    print(
        f"Quellen: {len(ledger['sources'])} | Zitate: {total} | PASS: {passed} | FAIL: {total - passed}"
        f" | Needles: {n_total} | Needle-PASS: {n_pass}"
    )
    print("-" * 78)
    for row in needle_rows:
        print(row)
    print("-" * 78)
    if failed:
        print(f"FAILS ({len(failed)}):")
        for fid, label, msg in failed:
            print(f"  src {fid} [{label[:60]}]: {msg}")
        return 1
    print("ALLE ZITATE PASS.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
