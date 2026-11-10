#!/usr/bin/env python3
"""Ledger-Verifikation für treppenlift-unserioese-anbieter (Briefing 22).

Prüft gegen research/unserioese-101126-ledger.json:
1. Jedes Zitat verbatim (whitespace- + soft-hyphen-normalisiert) in der Evidenz-Datei.
2. Umfrage-Arithmetik: Chart-Zeilen summieren auf 125.
3. Klausel-Count der Verbandsklage-Seite = 18 (zwischen Register-Markern).
4. Artikel-Integrität: alle [n] lösen auf 1..9, jede Quelle ≥1× zitiert, checked_at 10.11.
5. Kernzahlen/Wortlaute im Artikel-JSON + Absenzen (keine Förderbeträge, keine Empfehlungen).
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LEDGER = json.loads((ROOT / "research" / "unserioese-101126-ledger.json").read_text(encoding="utf-8"))
ART = json.loads((ROOT / "content-ready" / "treppenlift-unserioese-anbieter.json").read_text(encoding="utf-8"))

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

# 2. Umfrage-Arithmetik (Chart-Zeilen, PDF-Text)
pdf = norm((ROOT / LEDGER["sources"][1]["evidence"]).read_text(encoding="utf-8"))
rows = {
    "Widerrufsbelehrung": ("Wurden Sie über Ihr Widerrufsrecht belehrt?", 83, 37, 5),
    "sofort unterschrieben": ("Sollten Sie das Angebot sofort unterschreiben?", 43, 81, 1),
    "Werbeversprechen": ("Wurden Werbeversprechen gebrochen?", 29, 93, 3),
}
for label, (needle, ja, nein, ka) in rows.items():
    m = re.search(re.escape(needle) + r"\s+(\d+)\s+(\d+)\s+(\d+)", pdf)
    ok = m and int(m.group(1)) == ja and int(m.group(2)) == nein and int(m.group(3)) == ka
    check(f"Umfrage-Chart: {label} = {ja}+{nein}+{ka} = 125", bool(ok),
          m.group(0) if m else "Zeile nicht gefunden")
m = re.search(r"77\s+46\s+2", pdf)
check("Umfrage-Chart: Planungsunterlagen = 77+46+2 = 125",
      bool(m) and "Planungsunterlagen übergeben?" in pdf,
      "Zeile nicht gefunden")

# 3. Klausel-Count Verbandsklage-Seite = 18
klage = (ROOT / LEDGER["sources"][3]["evidence"]).read_text(encoding="utf-8")
marker_start = "sich auf diese Klauseln zu berufen:"
marker_end = "Alle Verbandsklagen"
i0 = klage.find(marker_start)
i1 = klage.find(marker_end)
kl = [l for l in klage[i0 + len(marker_start):i1].splitlines() if l.strip()]
check("Verbandsklage: 18 Klauseln gelistet", len(kl) == 18, f"gefunden: {len(kl)}")
check("Verbandsklage: 65-%- und 25-%-Pauschale je 1×",
      klage.count("in Höhe von 65 % der Bruttoauftragssumme") == 1
      and klage.count("in Höhe von 25 % der Bruttoauftragssumme") == 1)

# 4. Artikel-Integrität
art_blob = json.dumps(ART, ensure_ascii=False)
cited = set()
for m in re.finditer(r"\[(\d+)\]", art_blob):
    cited.add(int(m.group(1)))
ns = {s["n"] for s in LEDGER["sources"]}
check("alle [n] lösen auf Ledger-Quellen", cited <= ns, str(cited - ns))
check("jede Quelle ≥1× zitiert", cited == ns, f"ungenutzt: {sorted(ns - cited)}")
check("checked_at 2026-11-10 überall",
      all(s.get("checked_at") == "2026-11-10" for s in ART["sources"]),
      str([s.get("checked_at") for s in ART["sources"]]))
check("Quellenzahl stimmt mit Ledger", len(ART["sources"]) == len(LEDGER["sources"]))
check("Beschreibung ≤155 Zeichen", len(ART["description"]) <= 155, str(len(ART["description"])))
check("Titel-Kopf ≤40 Zeichen", len(ART["title"]) <= 40, str(len(ART["title"])))

# 5. Kernzahlen/Wortlaute im Artikel-JSON
for needle in ["125 ausgefüllte Umfragebögen", "12 Monate und 14 Tage", "I-13 UKl 17/26",
               "08. Oktober 2026", "8. Oktober 2026", "18 Vertragsklauseln",
               "in Höhe von 65 % der Bruttoauftragssumme", "in Höhe von 25 % der Bruttoauftragssumme",
               "Maßanfertigung und Lieferung sofort",
               "Keinesfalls sollten Sie sich zu einem Vertragsabschluss drängen lassen",
               "geistige und körperliche Beeinträchtigungen, das Alter",
               "ohne dessen vorherige ausdrückliche Einwilligung",
               "höchste Vorsicht geboten",
               "zahlen Sie erst, wenn der Lift eingebaut und funktionstüchtig ist",
               "An keiner Stelle war erkennbar", "PractiComfort",
               "bis zu 20 Prozent ohne Anzeige möglich", "zwei Jahre lang",
               "130 Nennungen", "4/5 der Verbraucher:innen", "10. Dezember 2020",
               "Werkvertrag", "Verbandsklageregister", "Oberlandesgericht Hamm"]:
    check(f"Kernzahl/Wortlaut: '{needle}'", needle in art_blob)

# Absenz-Gates: keine Förderbeträge (bewusst nur Verweis), keine Empfehlungen, keine Herstellernummern
for needle in ["4.180", "16.720", "Testsieger", "empfehlen wir", "empfohlen", "beste Anbieter",
               "Preis ab", "garantiert genehmigt"]:
    check(f"Absenz Artikel: 0 × '{needle}'", art_blob.count(needle) == 0, str(art_blob.count(needle)))

# Keine Firma wird selbst als unseriös etikettiert (Quellen sprechen, wir sortieren)
check("Absenz Artikel: 0 × 'unseriöser Anbieter Mobilae'", art_blob.count("unseriöser Anbieter Mobilae") == 0)

print(f"\n{N - len(FAIL)}/{N} PASS")
sys.exit(1 if FAIL else 0)
