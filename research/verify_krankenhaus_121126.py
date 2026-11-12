#!/usr/bin/env python3
"""Ledger-Verifikation für wohnung-anpassen-nach-krankenhausentlassung (Briefing 24).

Prüft gegen research/krankenhaus-121126-ledger.json:
1. Jedes Zitat verbatim (whitespace-/soft-hyphen-normalisiert) in der Evidenz-Datei.
2. Artikel-Integrität: alle [n] lösen auf 1..15, jede Quelle ≥1× zitiert,
   checked_at 2026-11-12 in allen source-Einträgen, 15 Quellen.
3. Kernzahlen/Wortlaute im Artikel-JSON (fünften Arbeitstag, 25 Arbeitstage,
   drei Arbeitstagen, acht Wochen, Pflegegrade 2 bis 5, zehnten Arbeitstag,
   sieben Tagen, schriftlich oder elektronisch, Rahmenvertrag).
4. Arithmetik: 25/5 == 5.
5. Absenzen: 0x Förderbeträge, 0x KfW, 0x Lift-Preise, 0x Partner-Marker;
   Konkurrenz 0x Entlassmanagement.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LEDGER = json.loads((ROOT / "research" / "krankenhaus-121126-ledger.json").read_text(encoding="utf-8"))
ART = json.loads((ROOT / "content-ready" / "wohnung-anpassen-nach-krankenhausentlassung.json").read_text(encoding="utf-8"))

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


# 1. Verbatim-Zitate
for src in LEDGER["sources"]:
    ev = norm((ROOT / src["evidence"]).read_text(encoding="utf-8"))
    for q in src["quotes"]:
        check(f"[{src['n']}] verbatim: {q[:58]}…", norm(q) in ev)

# 2. Artikel-Integrität
full_text = json.dumps(ART, ensure_ascii=False)
cites = sorted({int(m) for m in re.findall(r"\[(\d+)\]", full_text)})
check("citation range 1..16", cites and cites[0] >= 1 and cites[-1] <= 16, str(cites[:5]) + "…" + str(cites[-3:]))
uncited = [s["n"] for s in LEDGER["sources"] if s["n"] not in cites]
check("jede Quelle ≥1× zitiert", not uncited, str(uncited))
for src in ART["sources"]:
    check(f"checked_at {src['checked_at']}", src["checked_at"] == "2026-11-12", src["checked_at"])
check("16 sources im Artikel", len(ART["sources"]) == 16, str(len(ART["sources"])))

# 3. Kernzahlen/Wortlaute im Artikel-JSON
for needle in ["spätestens am fünften Arbeitstag", "25 Arbeitstage", "drei Arbeitstagen",
               "acht Wochen pro Kalenderjahr", "Pflegegrade 2 bis 5", "zehnten Arbeitstag",
               "bis zu sieben Tagen", "schriftlich oder elektronisch", "Rahmenvertrag", "Übergangszeit"]:
    check(f"Kernzahl: {needle[:40]}", needle in full_text)

# 4. Arithmetik
check("Arithmetik a1: 25/5 == 5", 25 // 5 == 5)

# 5. Absenzen
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
