#!/usr/bin/env python3
"""Ledger-Verifikation für treppenlift-foerderung-ohne-pflegegrad (Briefing 23).

Prüft gegen research/ohne-pflegegrad-111126-ledger.json:
1. Jedes Zitat verbatim (whitespace-/soft-hyphen-normalisiert) in der Evidenz-Datei.
2. Artikel-Integrität: alle [n] lösen auf 1..28, jede Quelle ≥1× zitiert,
   checked_at 2026-11-11 in allen source-Einträgen.
3. Kernzahlen/Wortlaute im Artikel-JSON (85/75/60 %, 150 %, Vorvorjahr,
   zwei Wochen, sechs Monate, 15 bis unter 30, § 64e, Treppensteigen).
4. Absenzen: keine Pflegekassen-Beträge (4.180/16.720), kein awin/sponsored,
   kein '12,5'-NBA-Punktwert (Reform-Schwelle nur als Entwurf 15 zitiert).
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LEDGER = json.loads((ROOT / "research" / "ohne-pflegegrad-111126-ledger.json").read_text(encoding="utf-8"))
ART = json.loads((ROOT / "content-ready" / "treppenlift-foerderung-ohne-pflegegrad.json").read_text(encoding="utf-8"))

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
check("citation range 1..28", cites and cites[0] >= 1 and cites[-1] <= 28, str(cites[:5]) + "…" + str(cites[-3:]))
uncited = [s["n"] for s in LEDGER["sources"] if s["n"] not in cites]
check("jede Quelle ≥1× zitiert", not uncited, str(uncited))
for src in ART["sources"]:
    check(f"checked_at {src['checked_at']}", src["checked_at"] == "2026-11-11", src["checked_at"])
check("28 sources im Artikel", len(ART["sources"]) == 28, str(len(ART["sources"])))

# 3. Kernzahlen/Wortlaute im Artikel-JSON
for needle in ["85 Prozent der jährlichen Bezugsgröße", "75 Prozent", "60 Prozent",
               "150 Prozent der jährlichen Bezugsgröße", "Einkünfte des Vorvorjahres",
               "innerhalb von zwei Wochen", "Dauer von sechs Monaten",
               "15 bis unter 30 Gesamtpunkten", "§ 64e SGB XII", "Treppensteigen",
               "vor der Haus- bzw. vor der Wohnungstür",
               "die Pflegegrade 1 bis 3 zielgenauer vergeben werden",
               "Drucksache 21/8869", "nicht beschlossen",
               "Teilhabeservice", "Persönliches Budget", "Gesamtplanverfahren",
               "Internationalen Klassifikation der Funktionsfähigkeit"]:
    check(f"JSON enthält \"{needle[:48]}\"", needle in full_text)

# 4. Absenzen
for bad in ["4.180", "16.720", "awin1.com", "rel=\"sponsored", "12,5"]:
    check(f"Absenz \"{bad}\"", bad not in full_text and bad not in (ART.get("description", "")))
check("status editorial-reviewed-preview", ART["status"] == "editorial-reviewed-preview")
check("image asset existiert", (ROOT / ART["image"]["src"]).exists(), ART["image"]["src"])
check("caption KI-Kennzeichnung", "KI-Illustration" in ART["image"]["caption"])

print(f"\n{N} checks, {len(FAIL)} FAILS")
sys.exit(1 if FAIL else 0)
