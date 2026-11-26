#!/usr/bin/env python3
"""Maschineller Verbatim-Check: Region-Screen Hessen (2026-11-26).

Prüft die Zitate und Absenz-Needles aus research/region-screen-261126-hessen-ledger.json
gegen die Evidenz-Dateien in research/evidence/region-screen-261126/hessen/.

Normalisierung (auf Zitat und Evidenz identisch angewendet):
- U+00AD (soft hyphen) entfernen
- Whitespace zu je einem Leerzeichen kollabieren
- Zeilenumbruch-Hyphens verbinden ('Projekt- foerder...' -> 'Projektförderung');
  konsistent auf beiden Seiten, daher auch echte Komposita-Hyphens ('Lieferungs- und')
- Tausendertrennzeichen zwischen Ziffern (Punkt, geschütztes/narrow space) entfernen
  ('4 180' und '4.180' -> '4180')

Needles: {"needle", "expect", "note"} — Count auf dem GESTRIPPTEM Text muss exakt
dem Sollwert entsprechen (Absenz-Checks: expect 0).
entities_check: Liste von Organisationsnamen — alle müssen im Text stehen.

Ausgabe: PASS/FAIL je Check + Summen; schreibt QUOTES.md ins Evidenz-Verzeichnis.
"""
import json
import os
import re
import sys
from datetime import date

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(REPO, "research", "region-screen-261126-hessen-ledger.json")
EVIDENCE = os.path.join(REPO, "research", "evidence", "region-screen-261126", "hessen")
QUOTES_MD = os.path.join(EVIDENCE, "QUOTES.md")


def normalize(s: str) -> str:
    s = s.replace("\u00ad", "")
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"(\w)- (?=\w)", r"\1", s)
    s = re.sub(r"(?<=\d)[.\u00a0\u202f\u2009 ](?=\d)", "", s)
    return s


def main() -> int:
    with open(LEDGER, encoding="utf-8") as fh:
        ledger = json.load(fh)

    cache: dict[str, str] = {}
    lines: list[str] = [f"# QUOTES — Region-Screen Hessen ({date.today().isoformat()})",
                        "",
                        f"Ledger: `{os.path.relpath(LEDGER, REPO)}` · generiert von "
                        f"`research/check_quotes_region_screen_261126_hessen.py`",
                        ""]

    total_pass = total_fail = 0
    q_pass = q_fail = n_pass = n_fail = e_pass = e_fail = 0

    for src in ledger["sources"]:
        fname = src["evidence"]
        path = os.path.join(EVIDENCE, fname)
        if fname not in cache:
            if not os.path.exists(path):
                print(f"[FAIL] Evidenz-Datei fehlt: {fname}")
                q_fail += len(src.get("quotes", []))
                total_fail += len(src.get("quotes", []))
                continue
            with open(path, encoding="utf-8", errors="replace") as fh:
                cache[fname] = normalize(fh.read())
        text = cache[fname]

        lines.append(f"## Quelle {src['id']}: {src['label']}")
        lines.append(f"URL: {src['url']}  ·  Evidenz: `{fname}`")
        lines.append("")

        for q in src.get("quotes", []):
            ok = normalize(q) in text
            q_pass += ok
            q_fail += not ok
            total_pass += ok
            total_fail += not ok
            mark = "PASS" if ok else "FAIL"
            lines.append(f"- [{mark}] „{q}“")
            if not ok:
                print(f"[FAIL] Zitat (Quelle {src['id']}, {fname}): {q[:90]}")

        for nd in src.get("needles", []):
            count = cache[fname].count(nd["needle"]) if nd["needle"] else text.count(nd["needle"])
            ok = count == nd["expect"]
            n_pass += ok
            n_fail += not ok
            total_pass += ok
            total_fail += not ok
            mark = "PASS" if ok else "FAIL"
            lines.append(f"- [{mark}] Needle „{nd['needle']}“: {count}× (Soll {nd['expect']}×) — {nd.get('note','')}")
            if not ok:
                print(f"[FAIL] Needle (Quelle {src['id']}, {fname}): '{nd['needle']}' "
                      f"ist {count}×, erwartet {nd['expect']}×")

        for ent in src.get("entities_check", []):
            ok = ent in text
            e_pass += ok
            e_fail += not ok
            total_pass += ok
            total_fail += not ok
            if not ok:
                print(f"[FAIL] Entity (Quelle {src['id']}, {fname}): '{ent}' fehlt")
        if "entities_check" in src:
            found = sum(1 for ent in src["entities_check"] if ent in text)
            want = len(src["entities_check"])
            lines.append(f"- [{'PASS' if found == want else 'FAIL'}] Entities: "
                         f"{found}/{want} Organisationseinheiten (26 Träger-Einheiten EGH)")
        lines.append("")

    lines.insert(4, f"**Ergebnis: {total_pass} PASS / {total_fail} FAIL** "
                    f"(Zitate {q_pass}/{q_pass + q_fail} · Needles {n_pass}/{n_pass + n_fail} · "
                    f"Entities {e_pass}/{e_pass + e_fail})\n")

    with open(QUOTES_MD, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    print(f"\nZitate:   {q_pass} PASS / {q_fail} FAIL")
    print(f"Needles:  {n_pass} PASS / {n_fail} FAIL")
    print(f"Entities: {e_pass} PASS / {e_fail} FAIL")
    print(f"TOTAL:    {total_pass} PASS / {total_fail} FAIL")
    print(f"QUOTES.md: {os.path.relpath(QUOTES_MD, REPO)}")
    return 0 if total_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
