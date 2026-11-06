#!/usr/bin/env python3
"""Ledger-Verifikation für hausnotruf-schluesselhinterlegung (Briefing 19).

Prüft gegen research/schluessel-061126-ledger.json:
1. Jedes Zitat verbatim (whitespace- + Soft-Hyphen-normalisiert) in der Evidenz-Datei.
2. Absenz-Checks: Malteser 0×Tresor/0×Schlüsseldienst/0×Hinterlegung, VZ 0×'15 Euro'/
   0×Tresor, Pflege-Einstieg 0×Euro.
3. Artikel-Integrität: alle [n] lösen auf 1..8, jede Quelle ≥1× zitiert, checked_at 06.11.
4. Kernzahlen/Wortlaute im Artikel-JSON.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LEDGER = json.loads((ROOT / "research" / "schluessel-061126-ledger.json").read_text(encoding="utf-8"))
ART = json.loads((ROOT / "content-ready" / "hausnotruf-schluesselhinterlegung.json").read_text(encoding="utf-8"))

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
ns = [s["n"] for s in LEDGER["sources"]]
check("Artikel-Zitationen gültig", cited <= set(ns), str(sorted(cited - set(ns))))
check("Alle Quellen zitiert", set(ns) <= cited, str(sorted(set(ns) - cited)))
check("Quellenzahl = 8", len(ART["sources"]) == 8, str(len(ART["sources"])))
for s in ART["sources"]:
    check(f"checked_at 2026-11-06: {s['url'][:48]}", s["checked_at"] == "2026-11-06", s["checked_at"])
urls_l = [s["url"] for s in LEDGER["sources"]]
check("Artikel-URLs == Ledger-URLs", [s["url"] for s in ART["sources"]] == urls_l)

# 4. Kernzahlen/Wortlaute
for needle in ["2.957,21", "fast 800 Euro", "etwa 15 Euro", "30 bis 80 Euro",
               "35 bis 100 Euro", "27 und 40 Euro", "§ 536a BGB", "2 K 2103/23.GI",
               "AG Hildburghausen", "AG Berlin-Mitte", "nicht von der Pflegekasse bezuschusst",
               "kostenpflichtig und müssen privat finanziert werden",
               "06.11.2026", "in demselben Gespräch",
               "schneller am Einsatzort", "kein Generalschlüssel"]:
    check(f"Artikel enthält '{needle}'", needle in all_text or needle in json.dumps(ART, ensure_ascii=False))
check("Titel ≤ 40 Zeichen", len(ART["title"]) <= 40, str(len(ART["title"])))
check("Description ≤ 155", len(ART["description"]) <= 155, str(len(ART["description"])))
check("Slug-Care-Cluster (hausnotruf-Präfix)", ART["slug"].startswith("hausnotruf"))
check("Keine Partner-Marker-Absicht (kein Partnerlink im Artikel)", "awin1.com" not in json.dumps(ART, ensure_ascii=False))
check("FAQs = 6", len(ART["faqs"]) == 6, str(len(ART["faqs"])))
check("Sections = 10", len(ART["sections"]) == 10, str(len(ART["sections"])))
check("Tabelle vorhanden (4 Wege)", any("table" in s for s in ART["sections"]))
check("Tabelle hat 4 Zeilen", [len(s["table"]["rows"]) for s in ART["sections"] if "table" in s] == [4])

print()
print(f"{N - len(FAIL)}/{N} PASS" + ("  — ALL PASS" if not FAIL else f"  — {len(FAIL)} FAILS"))
sys.exit(1 if FAIL else 0)
