#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Maschineller Verbatim-Check fuer Region-Screen Niedersachsen (26.11.2026).

Prueft JEDES Zitat aus research/region-screen-261126-nds-ledger.json
verbatim gegen die gespeicherte Evidenz in
research/evidence/region-screen-261126/nds/.

Normalisierung (dokumentiert, deterministisch, identisch fuer Evidenz UND Zitat):
1. Soft-Hyphen (U+00AD) strippen (KfW/NBank-Falle).
2. Geschuetzte Leerzeichen (U+00A0 NBSP, U+202F schmales NBSP, U+2009) -> normales Leerzeichen
   (geschuetzte Tausendertrennzeichen-Falle).
3. De-Hyphenation am Zeilenumbruch: "Wort-\nrest" -> "Wortrest", AUSSER wenn das
   erste Zeichen des Nachlaufs ein Grossbuchstabe ist (dann echter Bindestrich-Compound,
   z. B. "DVO-\nNWoFG" -> "DVO-NWoFG").
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
LEDGER = ROOT / "region-screen-261126-nds-ledger.json"
EVIDENCE_DIR = ROOT / "evidence" / "region-screen-261126" / "nds"

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
    # evidence_dir ist repo-relativ (z. B. "research/evidence/..."), ROOT = research/
    ev_dir = ROOT.parent / ledger.get("evidence_dir", "research/evidence/region-screen-261126/nds")
    if not ev_dir.exists():
        ev_dir = ROOT / ledger.get("evidence_dir", "research/evidence/region-screen-261126/nds")
    total, passed, failed = 0, 0, []
    needle_rows = []

    for src in ledger["sources"]:
        ev_names = src["evidence"] if isinstance(src["evidence"], list) else [src["evidence"]]
        ev_paths = []
        for name in ev_names:
            p = ev_dir / name
            if not p.exists():
                alt = ev_dir / "nds" / name
                if alt.exists():
                    p = alt
            ev_paths.append(p)
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
            n_total, n_pass = 0, 0
            cnt = count_ci(ev, needle)
            expected = src.get("needle_expect", "count")
            if expected == "absent":
                ok = cnt == 0
                n_total, n_pass = 1, 1 if ok else 0
                needle_rows.append(
                    f"  src {src['id']:>2} ABSenz-Needle '{needle}' -> {cnt} Treffer "
                    f"({'PASS' if ok else 'FAIL (erwartet 0)'})"
                )
            else:
                needle_rows.append(f"  src {src['id']:>2} Count-Needle '{needle}' -> {cnt} Treffer (Fallcount)")
        for needle, expected_count in (src.get("needles_absent") or {}).items():
            cnt = count_ci(ev, needle)
            ok = cnt == expected_count
            n_total, n_pass = 1, 1 if ok else 0
            needle_rows.append(
                f"  src {src['id']:>2} ABSenz-Needle '{needle}' -> {cnt} Treffer "
                f"(erwartet {expected_count}) {'PASS' if ok else 'FAIL'}"
            )

    print("=" * 78)
    print(f"Verbatim-Check Region-Screen NDS 261126")
    print(f"Quellen: {len(ledger['sources'])} | Zitate: {total} | PASS: {passed} | FAIL: {total - passed}")
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
