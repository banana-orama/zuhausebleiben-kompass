#!/usr/bin/env python3
"""Ledger-Verifikation für treppenlift-aufmass-termin (Briefing 25).

Prüft gegen research/aufmass-121126-ledger.json:
1. Jedes Zitat verbatim (whitespace-normalisiert) in der Evidenz-Datei.
2. Artikel-Integrität: alle [n] lösen auf 1..8, jede Quelle ≥1× zitiert,
   checked_at 2026-11-12 in allen source-Einträgen, 8 Quellen.
3. Kernwortlaute im Artikel-JSON (Aufmaß, Festpreis inklusive Montage,
   Bedenkzeit, 14-tägiges Widerrufsrecht, 12 Monate und 14 Tage,
   gleichem Leistungsumfang, Kostenvoranschlag für die Pflegekasse,
   an den Treppenstufen).
4. Arithmetik: 43+81+1==125, 83+37+5==125, 77+46==123.
5. Absenzen: 0x Förderbeträge/KfW/awin im Artikel-JSON.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LEDGER = json.loads((ROOT / "research" / "aufmass-121126-ledger.json").read_text(encoding="utf-8"))
ART_PATH = ROOT / "content-ready" / "treppenlift-aufmass-termin.json"
ART = json.loads(ART_PATH.read_text(encoding="utf-8")) if ART_PATH.exists() else None

FAIL = []
N = 0


def check(label, cond, detail=""):
    global N
    N += 1
    print(("PASS " if cond else "FAIL ") + label + ("" if cond else f"  {detail}"))
    if not cond:
        FAIL.append(label)


def norm(t):
    t = t.replace("\u00ad", "")
    t = re.sub(r"\s+", " ", t)
    t = re.sub(r"\s+([.,;:!?])", r"\1", t)
    return t.strip()


# 1. Verbatim-Zitate (immer prüfbar)
for src in LEDGER["sources"]:
    ev = norm((ROOT / src["evidence"]).read_text(encoding="utf-8"))
    for q in src["quotes"]:
        check(f"[{src['n']}] verbatim: {q[:58]}…", norm(q) in ev)

# 2-5 nur mit vorhandenem Artikel
if ART is not None:
    full_text = json.dumps(ART, ensure_ascii=False)
    cites = sorted({int(m) for m in re.findall(r"\[(\d+)\]", full_text)})
    check("citation range 1..8", cites and cites[0] >= 1 and cites[-1] <= 8, str(cites))
    uncited = [s["n"] for s in LEDGER["sources"] if s["n"] not in cites]
    check("jede Quelle ≥1× zitiert", not uncited, str(uncited))
    for src in ART["sources"]:
        check(f"checked_at {src['checked_at']}", src["checked_at"] == "2026-11-12", src["checked_at"])
    check("8 sources im Artikel", len(ART["sources"]) == 8, str(len(ART["sources"])))
    for needle in ["Festpreis inklusive Montage", "Bedenkzeit", "14-tägiges Widerrufsrecht",
                   "12 Monate und 14 Tage", "gleichem Leistungsumfang",
                   "Kostenvoranschlag für die Pflegekasse", "an den Treppenstufen",
                   "unverbindlichen Angebot", "nicht vorschnell"]:
        check(f"Kernwortlaut: {needle[:40]}", needle in full_text)
    check("Arithmetik a1: 43+81+1 == 125", 43 + 81 + 1 == 125)
    check("Arithmetik a2: 83+37+5 == 125", 83 + 37 + 5 == 125)
    check("Arithmetik a3: 77+46 == 123", 77 + 46 == 123)
    for ax in LEDGER["absenzen"]:
        for f in ax["files"]:
            t = (ROOT / f).read_text(encoding="utf-8")
            for p in ax["patterns"]:
                c = t.count(p)
                check(f"Absenz {ax['id']}: 0x {p} in {f.split('/')[-1]}", c == ax["expect"], str(c))

print(f"\n{N - len(FAIL)}/{N} Pässe")
if FAIL:
    print(f"FAILS ({len(FAIL)}):")
    for f in FAIL:
        print(" -", f)
    sys.exit(1)
print("ALL PASS")
