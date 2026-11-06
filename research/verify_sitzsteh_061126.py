#!/usr/bin/env python3
"""Ledger-Verifikation für treppenlift-sitzlift-oder-stehlift (Batch 9 / Briefing 18).

Prüft gegen research/sitzsteh-061126-ledger.json:
1. Jedes Zitat verbatim (whitespace-normalisiert) in der zugehörigen Evidenz-Datei.
2. Absenz-Checks: HIRO ×2 und TKE ×2 enthalten 0 × stehlift/stehhilfe (case-insensitive).
3. Artikel-Integrität: alle [n] im content-ready-JSON lösen auf 1..len(sources);
   jede Quelle wird mindestens einmal zitiert; checked_at = 2026-11-06.
4. Kernzahlen/Wortlaute im Artikel-JSON: 80 cm, 55 cm, 4.000, 12 Monate, gängigste,
   Gewähr-Hinweis, Absenz-Datierung.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LEDGER = json.loads((ROOT / "research" / "sitzsteh-061126-ledger.json").read_text(encoding="utf-8"))
ART = json.loads((ROOT / "content-ready" / "treppenlift-sitzlift-oder-stehlift.json").read_text(encoding="utf-8"))

FAIL = []
N = 0


def check(label, cond, detail=""):
    global N
    N += 1
    print(("PASS " if cond else "FAIL ") + label + ("" if cond else f"  {detail}"))
    if not cond:
        FAIL.append(label)


def norm(t):
    return re.sub(r"\s+", " ", t).strip()


# 1. Verbatim-Zitate
for src in LEDGER["sources"]:
    ev = (ROOT / src["evidence"]).read_text(encoding="utf-8")
    evn = norm(ev)
    for q in src["quotes"]:
        check(f"[{src['n']}] verbatim: {q[:58]}…", norm(q) in evn)

# 2. Absenz-Checks
for ac in LEDGER["absenz_checks"]:
    for f in ac["files"]:
        txt = (ROOT / f).read_text(encoding="utf-8").lower()
        for nd in ac["needles"]:
            check(f"Absenz {pathlib.Path(f).name}: 0 × '{nd}'", txt.count(nd) == ac["expected"], str(txt.count(nd)))

# 3. Artikel-Integrität
body_texts = list(ART["intro"])
for s in ART["sections"]:
    body_texts += s.get("paragraphs", []) + s.get("bullets", []) + s.get("paragraphs_after", [])
    if "table" in s:
        for row in s["table"]["rows"]:
            body_texts += row
body_texts += [f["answer"] for f in ART["faqs"]]
all_text = " ".join(body_texts)
cited = set(int(m) for m in re.findall(r"\[(\d+)\]", all_text))
n_sources = len(ART["sources"])
check("Alle [n] lösen auf", all(1 <= n <= n_sources for n in cited), str(sorted(cited)))
check("Jede Quelle zitiert", cited == set(range(1, n_sources + 1)), f"missing={sorted(set(range(1, n_sources + 1)) - cited)}")
check("checked_at 2026-11-06 überall", all(s["checked_at"] == "2026-11-06" for s in ART["sources"]))

# Ledger-URLs = Artikel-URLs (Drift-Schutz)
for src in LEDGER["sources"]:
    a = ART["sources"][src["n"] - 1]
    check(f"URL sync [{src['n']}]", a["url"] == src["url"], a["url"])

# 4. Kernzahlen/Wortlaute
for needle in ["Mindestbreite von 80 cm", "Mindestens 55 cm", "etwa 4.000 Euro",
               "12 Monate und 14 Tage", "gängigste Art", "ohne Gewähr",
               "06.11.2026", "skriptgeprüft"]:
    check(f"Artikel enthält '{needle}'", needle in all_text)

print(f"\n{N - len(FAIL)}/{N} PASS")
sys.exit(1 if FAIL else 0)
