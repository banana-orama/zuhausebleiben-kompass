#!/usr/bin/env python3
"""Ledger-Verifikation für hausnotruf-smartwatch-als-ersatz (Briefing 27).

Prüft gegen research/smartwatch-161126-ledger.json:
1. Jedes Zitat verbatim (whitespace-normalisiert) in der Evidenz-Datei.
2. Absenz-Checks: ADAC/Alzheimer/VdK 0x 'Smartwatch', VZ 0x '30 bis 50' (Stale-Echo-Gegenprobe),
   alle 6 Evidenzen 0x Förderbeträge (4.180/16.720).
3. Artikel-Integrität: alle [n] lösen auf 1..6, jede Quelle >=1x zitiert, checked_at 16.11.,
   URLs == Ledger, Titel/Desc-Grenzen, Slug im Care-Cluster, kein awin, 6 FAQs, 10 Sections,
   Tabelle mit 3 Zeilen.
4. Kernzahlen/Wortlaute im Artikel-JSON.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LEDGER = json.loads((ROOT / "research" / "smartwatch-161126-ledger.json").read_text(encoding="utf-8"))
ART = json.loads((ROOT / "content-ready" / "hausnotruf-smartwatch-als-ersatz.json").read_text(encoding="utf-8"))

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

# 2. Absenz-Checks (lowercase-Nadeln, lowercase-Haystack)
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
check("Quellenzahl = 6", len(ART["sources"]) == 6, str(len(ART["sources"])))
for s in ART["sources"]:
    check(f"checked_at 2026-11-16: {s['url'][:48]}", s["checked_at"] == "2026-11-16", s["checked_at"])
urls_l = [s["url"] for s in LEDGER["sources"]]
check("Artikel-URLs == Ledger-URLs", [s["url"] for s in ART["sources"]] == urls_l)
art_dump = json.dumps(ART, ensure_ascii=False)

# 4. Kernzahlen/Wortlaute
for needle in ["27 und 40 Euro", "30 bis 80 Euro", "bis zu 27 Euro",
               "Pflegegrad 1", "ab bereits 50 Euro", "mehreren hundert Euro",
               "einfacher in der Bedienung als ein Telefon oder Handy",
               "unter bestimmten Voraussetzungen", "20 bis 25 Euro", "25,50 Euro",
               "nicht gezielt auslösen", "unkontrolliert betätigen",
               "seit 1. April 2026", "16.11.2026",
               "wer nimmt", "Nummernkette", "vorübergehend"]:
    check(f"Artikel enthält '{needle}'", needle in all_text or needle in art_dump)
check("Titel ≤ 40 Zeichen", len(ART["title"]) <= 40, str(len(ART["title"])))
check("Description ≤ 155", len(ART["description"]) <= 155, str(len(ART["description"])))
check("Slug-Care-Cluster (hausnotruf-Präfix)", ART["slug"].startswith("hausnotruf"))
check("Kein Partnerlink im Artikel", "awin1.com" not in art_dump)
check("Keine Förderbeträge im Artikel", "4.180" not in art_dump and "16.720" not in art_dump)
check("FAQs = 6", len(ART["faqs"]) == 6, str(len(ART["faqs"])))
check("Sections = 10", len(ART["sections"]) == 10, str(len(ART["sections"])))
check("Tabelle vorhanden", any("table" in s for s in ART["sections"]))
check("Tabelle hat 3 Zeilen", [len(s["table"]["rows"]) for s in ART["sections"] if "table" in s] == [3])
check("Checkliste vorhanden (bullets)", any(len(s.get("bullets", [])) >= 8 for s in ART["sections"]))

print()
print(f"{N - len(FAIL)}/{N} PASS" + ("  — ALL PASS" if not FAIL else f"  — {len(FAIL)} FAILS"))
sys.exit(1 if FAIL else 0)
