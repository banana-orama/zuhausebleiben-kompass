#!/usr/bin/env python3
# 23.11.2026: Hilfsmittel-Zuzahlung 2027 — § 61 SGB V Neufassung (BGBl. 2026 I Nr. 228,
# Art. 1 Nr. 23; Inkrafttreten 01.01.2027 lt. Art. 8 Abs. 2) in 3 Artikel einarbeiten.
# Chirurgische Text-Ersetzungen (kein json round-trip); jede Ersetzung assertiert 1×.
import json, re, os, sys

BASE = os.path.join(os.path.dirname(__file__), "..", "content-ready")
SRC_BGBL = {
    "title": "Bundesgesetzblatt Teil I: GKV-Beitragssatzstabilisierungsgesetz vom 24. Juli 2026 (BGBl. 2026 I Nr. 228, Art. 1 Nr. 23 – neuer § 61 SGB V)",
    "url": "https://www.recht.bund.de/bgbl/1/2026/228/VO.html",
    "checked_at": "2026-11-23",
}

# (datei, [alte_zeichenkette, neue_zeichenkette]) — Prosa/Tabellen/FAQ
EDITS = {
    "hilfsmittel-dusch-wc-uebernahme.json": {
        "new_idx": 9,
        "replacements": [
            (
                "an den Anbieter zahlen Volljährige eine Zuzahlung von 10 Prozent – mindestens 5, höchstens 10 Euro.[3][6]",
                "an den Anbieter zahlen Volljährige eine Zuzahlung von 10 Prozent – mindestens 5, höchstens 10 Euro.[3][6] Zum 1. Januar 2027 hebt das GKV-Beitragssatzstabilisierungsgesetz (BGBl. 2026 I Nr. 228) beide Beträge an: dann mindestens 7,50 und höchstens 15 Euro.[9]",
            ),
            (
                "\"Sachleistung; Zuzahlung 10 %, min. 5 €, max. 10 €[3][6]\"",
                "\"Sachleistung; Zuzahlung 10 %, min. 5 €, max. 10 € (ab 2027: 7,50 €/15 €)[3][6][9]\"",
            ),
            (
                "Dann ist der Aufsatz eine Sachleistung; Volljährige zahlen 10 Prozent, mindestens 5, höchstens 10 Euro an der Abgabestelle.[3][6]",
                "Dann ist der Aufsatz eine Sachleistung; Volljährige zahlen 10 Prozent, mindestens 5, höchstens 10 Euro an der Abgabestelle.[3][6] Ab dem 1. Januar 2027: mindestens 7,50, höchstens 15 Euro.[9]",
            ),
            (
                "An der Abgabestelle zahlen Volljährige 10 Prozent des Abgabepreises – mindestens 5, höchstens 10 Euro; nie mehr als die Kosten des Produkts.[3][6]",
                "An der Abgabestelle zahlen Volljährige 10 Prozent des Abgabepreises – mindestens 5, höchstens 10 Euro; nie mehr als die Kosten des Produkts.[3][6] Ab dem 1. Januar 2027 gelten mindestens 7,50 und höchstens 15 Euro.[9]",
            ),
        ],
    },
    "hilfsmittel-pflegekasse-uebernahme.json": {
        "new_idx": 11,
        "replacements": [
            (
                "deren Zuzahlung liegt bei 10 Prozent, mindestens 5 und höchstens 10 Euro.[4][9]",
                "deren Zuzahlung liegt bei 10 Prozent, mindestens 5 und höchstens 10 Euro; ab dem 1. Januar 2027 gilt die Neufassung des § 61 SGB V (GKV-Beitragssatzstabilisierungsgesetz), dann mindestens 7,50 und höchstens 15 Euro.[4][9][11]",
            ),
        ],
    },
    "rollator-auswahl-passform-kosten.json": {
        "new_idx": 11,
        "replacements": [
            (
                "mindestens 5 Euro und höchstens 10 Euro – jeweils nicht mehr als die Kosten des Mittels.[3]",
                "mindestens 5 Euro und höchstens 10 Euro – jeweils nicht mehr als die Kosten des Mittels.[3] Ab dem 1. Januar 2027 gilt mindestens 7,50 und höchstens 15 Euro.[3][11]",
            ),
            (
                "Bei Volljährigen beträgt die Zuzahlung 10 Prozent, mindestens 5 Euro, höchstens 10 Euro – nicht mehr als die Kosten des Mittels.[3]",
                "Bei Volljährigen beträgt die Zuzahlung 10 Prozent, mindestens 5 Euro, höchstens 10 Euro – nicht mehr als die Kosten des Mittels.[3] Ab 1. Januar 2027: mindestens 7,50, höchstens 15 Euro.[11]",
            ),
        ],
    },
}

RE_61_BLOCK = re.compile(
    r'("url": "https://www\.gesetze-im-internet\.de/sgb_5/__61\.html",\s*\n\s*"checked_at": ")([^"]+)(")'
)

def edit_file(fn, cfg):
    path = os.path.join(BASE, fn)
    txt = open(path, encoding="utf-8").read()
    orig = txt
    for old, new in cfg["replacements"]:
        if new in txt:
            print(f"{fn}: bereits angewendet, überspringe: {old[:60]}…")
            continue
        n = txt.count(old)
        assert n == 1, f"{fn}: Ersetzung-Treffer {n} != 1 für: {old[:80]}…"
        txt = txt.replace(old, new)
    if SRC_BGBL["url"] in txt:
        print(f"{fn}: BGBl-Quelle bereits vorhanden")
    else:
        m = RE_61_BLOCK.search(txt)
        assert m, f"{fn}: § 61-Quellenblock nicht gefunden"
        assert m.group(2) != "2026-11-23", f"{fn}: checked_at bereits 2026-11-23"
        txt = RE_61_BLOCK.sub(r"\g<1>2026-11-23\g<3>", txt, count=1)
        # Quelle ans Ende des sources-Arrays einfügen (erste "  ],"-Zeile nach "sources": [)
        i = txt.find('"sources": [')
        assert i >= 0, f"{fn}: sources-Array fehlt"
        j = txt.find("\n  ],", i)
        assert j >= 0, f"{fn}: sources-Array-Ende nicht gefunden"
        src_json = json.dumps(SRC_BGBL, ensure_ascii=False, indent=6)
        src_json = src_json.replace("\n", "\n    ").rstrip()
        insertion = ",\n    " + src_json
        txt = txt[:j] + insertion + txt[j:]
        print(f"{fn}: §61 checked_at {m.group(2)}→2026-11-23, Quelle [{cfg['new_idx']}] BGBl angehängt")
    json.loads(txt)  # Parse-Validierung (kein Rewrite)
    d = json.loads(txt)
    assert len(d["sources"]) >= cfg["new_idx"], f"{fn}: Quellenzahl < {cfg['new_idx']}"
    open(path, "w", encoding="utf-8").write(txt)
    print(f"{fn}: OK — Parse OK")

for fn, cfg in EDITS.items():
    edit_file(fn, cfg)

# Finaler Zitier-Integritätscheck über alle 3 Dateien
for fn, cfg in EDITS.items():
    d = json.load(open(os.path.join(BASE, fn), encoding="utf-8"))
    body = json.dumps(d, ensure_ascii=False)
    idx = cfg["new_idx"]
    assert f"[{idx}]" in body, f"{fn}: [{idx}] wird nicht zitiert"
    n_src = len(d["sources"])
    used = set(int(x) for x in re.findall(r"\[(\d+)\]", body) if 0 < int(x) <= n_src)
    unused = [k for k in range(1, n_src + 1) if k not in used and f"[{k}]" not in body]
    # Titel-Strings der Quellen dürfen [..] enthalten — nur echte Prosa-Zitierprüfung:
    print(f"{fn}: Quellen n={n_src}, Zitat [{idx}] vorhanden")
print("ALLE EDITS OK")
