#!/usr/bin/env python3
"""Ledger-Verifikation für hausnotruf-angehoerige-einrichten (Briefing 21).

Prüft gegen research/angehoerige-101126-ledger.json:
1. Jedes Zitat verbatim (whitespace- + Zeilenumbruch-normalisiert, ' .'→'.' auf beiden Seiten)
   in der Evidenz-Datei.
2. Artikel-Absenz-Checks: keine empfohlenen Anbieter, keine nicht zitierten Preis-Pauschalen,
   keine Einrichtungs-Dauer-Pauschale.
3. Artikel-Integrität: alle [n] lösen auf 1..7, jede Quelle ≥1× zitiert, checked_at 10.11.
4. Kernzahlen/Wortlaute im Artikel-JSON.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LEDGER = json.loads((ROOT / "research" / "angehoerige-101126-ledger.json").read_text(encoding="utf-8"))
ART = json.loads((ROOT / "content-ready" / "hausnotruf-angehoerige-einrichten.json").read_text(encoding="utf-8"))

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
    ev = (ROOT / src["evidence"]).read_text(encoding="utf-8")
    evn = norm(ev)
    for q in src["quotes"]:
        check(f"[{src['n']}] verbatim: {q[:58]}…", norm(q) in evn)

# 2. Artikel-Absenz-Checks (Empfehlungs-/Pauschal-Verbot)
art_blob = json.dumps(ART, ensure_ascii=False)
for needle in ["Testsieger", "beste Anbieter", "empfehlen wir", "0,89", "Testberichten",
               "Einrichtung dauert", "innerhalb von 2 Stunden", "garantiert", "immer kostenlos"]:
    check(f"Absenz Artikel: 0 × '{needle}'", art_blob.count(needle) == 0, str(art_blob.count(needle)))

# 3. Artikel-Integrität: Zitate auf Quellen, checked_at, Quellenabdeckung
cited = set()
for m in re.finditer(r"\[(\d+)\]", art_blob):
    cited.add(int(m.group(1)))
ns = {s["n"] for s in LEDGER["sources"]}
check("alle [n] lösen auf Ledger-Quellen", cited <= ns, str(cited - ns))
check("jede Quelle ≥1× zitiert", cited == ns, f"ungenutzt: {sorted(ns - cited)}")
check("checked_at 2026-11-10 überall",
      all(s.get("checked_at") == "2026-11-10" for s in ART["sources"]),
      str([s.get("checked_at") for s in ART["sources"]]))
check("Quellenzahl stimmt mit Ledger",
      len(ART["sources"]) == len(LEDGER["sources"]))

# 4. Kernzahlen/Wortlaute im Artikel-JSON
for needle in ["27 und 40 Euro", "bis zu 27 Euro", "drei Wochen", "fünf Wochen",
               "innerhalb einer Woche", "bis zu 50 Metern", "10 bis 20 Stunden",
               "30 bis 50 Euro", "30 bis 80 Euro", "Vorsorgevollmacht für Vermögenssorge",
               "Versorgungsvertrag nach § 78 SGB XI", "funktionsfertig", "reine Gesundheitsvollmacht",
               "Vertragspartner der Pflegekasse", "weniger geeignet", "Treppenlift" ]:
    if needle == "Treppenlift":
        continue  # Lift-Cluster darf hier bewusst nicht vorkommen (kein Kaninchen-CTA)
    check(f"Kernzahl/Wortlaut: '{needle}'", needle in art_blob)

# Negativ-Gate: der Artikel darf NICHT in den Lift-Cluster ausufern
check("Absenz Artikel: 0 × 'Treppenlift'", art_blob.count("Treppenlift") == 0, str(art_blob.count("Treppenlift")))

print(f"\n{N - len(FAIL)}/{N} PASS")
sys.exit(1 if FAIL else 0)
