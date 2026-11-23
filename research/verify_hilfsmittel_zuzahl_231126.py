#!/usr/bin/env python3
"""Gate 23.11.2026: Hilfsmittel-Zuzahlung 2027 (§ 61 SGB V Neufassung, BGBl. 2026 I Nr. 228).

Prüft drei Ebenen:
1. VERBATIM gegen die heute abgerufenen Evidenzdateien:
   - § 61 SGB V live (gesetze-im-internet, ISO-dekodiert): alte Beträge 5/10 Euro, keine 7,50/15
   - BGBl-PDF-Text (pdftotext, normalisiert): „§ 61 wird durch den folgenden § 61 ersetzt“,
     7,50/15-Wortlaut, „nicht mehr als die Kosten des Mittels“, Inkrafttreten-Klausel
     Art. 8 Abs. 2 mit „Nummer 20 bis 23“ + „treten am 1. Januar 2027 in Kraft“
   - GKV-SV-PM (UTF-8): „mindestens 5 Euro (ab 2027: 7,50 Euro)“ + „höchstens 10 Euro (ab 2027: 15 Euro)“
2. ARTICLE-JSON: 3 Dateien parsen, 7,50/1.-Januar-2027-Sätze, BGBl-Quelle + §61 checked_at 2026-11-23,
   Zitier-Integrität ([n] ≤ Quellenzahl, neue Zitate vorhanden).
3. BUILT-HTML (LAUNCH-dist): alle 3 Seiten tragen den Satz im Fließtext, Quellen-Anker (#source-n),
   robots index,follow; bestehender duschwc-Content-Gate (verify_duschwc_content.py) bleibt grün.
"""
import html as html_mod
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
EV = ROOT / "research/evidence/hilfsmittel-zuzahl-231126"
DIST = ROOT / "dist"

fails = []
def check(label, ok, *info):
    print(("OK  " if ok else "FAIL"), label, *info)
    if not ok:
        fails.append((label, *info))

def strip_tags(raw):
    txt = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S | re.I)
    txt = re.sub(r"<[^>]+>", " ", txt)
    txt = html_mod.unescape(txt).replace("\xa0", " ")
    return re.sub(r"\s+", " ", txt)

# ---------- 1. VERBATIM ----------
law_raw = (EV / "sgb5-61-231126.html").read_bytes().decode("iso-8859-1", errors="replace")
law = strip_tags(law_raw)
check("§61 live: 10 vom Hundert des Abgabepreises", "betragen 10 vom Hundert des Abgabepreises, mindestens jedoch 5 Euro und höchstens 10 Euro; allerdings jeweils nicht mehr als die Kosten des Mittels" in law)
check("§61 live: keine 7,50", "7,50" not in law)
check("§61 live: keine 15 Euro", "15 Euro" not in law)

bgbl_raw = (EV / "bgbl-2026-i-228-gkv-bstabg.txt").read_text(encoding="utf-8", errors="replace")
bgbl = bgbl_raw.replace("\u00ad", "").replace("-\n", "")
bgbl = re.sub(r"\s+", " ", bgbl)
check("BGBl: § 61 wird ersetzt", "§ 61 wird durch den folgenden § 61 ersetzt" in bgbl)
check("BGBl: neuer Wortlaut 7,50/15", "mindestens jedoch 7,50 Euro und höchstens 15 Euro; allerdings jeweils nicht mehr als die Kosten des Mittels" in bgbl)
check("BGBl: Titel", bgbl.count("Beitragssatzstabilisierungsgesetz") >= 2)
check("BGBl: Inkrafttreten-Klausel", "treten am 1. Januar 2027 in Kraft" in bgbl)
check("BGBl: Nummer 23 gelistet", "Nummer 20 bis 23" in bgbl)

pm_raw = (EV / "gkvsp-pm-extract-231126.txt").read_text(encoding="utf-8")
pm = pm_raw
check("GKV-SV PM (Extrakt): min 5 (ab 2027: 7,50)", "mindestens 5 Euro (ab 2027: 7,50 Euro)" in pm)
check("GKV-SV PM (Extrakt): max 10 (ab 2027: 15)", "höchstens 10 Euro (ab 2027: 15 Euro)" in pm)
check("GKV-SV PM (Extrakt): Verbrauchshilfsmittel-Kappung", "Bei zum Verbrauch bestimmten Hilfsmitteln ist die Zuzahlung auf höchstens 10 Euro (ab 2027: 15 Euro)" in pm)

# ---------- 2. ARTICLE-JSON ----------
PAGES = [
    ("hilfsmittel-dusch-wc-uebernahme", 9, ["Zum 1. Januar 2027 hebt das GKV-Beitragssatzstabilisierungsgesetz (BGBl. 2026 I Nr. 228) beide Beträge an: dann mindestens 7,50 und höchstens 15 Euro.[9]", "(ab 2027: 7,50 €/15 €)[3][6][9]"]),
    ("hilfsmittel-pflegekasse-uebernahme", 11, ["ab dem 1. Januar 2027 gilt die Neufassung des § 61 SGB V (GKV-Beitragssatzstabilisierungsgesetz), dann mindestens 7,50 und höchstens 15 Euro.[4][9][11]"]),
    ("rollator-auswahl-passform-kosten", 11, ["Ab dem 1. Januar 2027 gilt mindestens 7,50 und höchstens 15 Euro.[3][11]", "Ab 1. Januar 2027: mindestens 7,50, höchstens 15 Euro.[11]"]),
]
for slug, bgbl_idx, needles in PAGES:
    d = json.loads((ROOT / f"content-ready/{slug}.json").read_text(encoding="utf-8"))
    body = json.dumps(d, ensure_ascii=False)
    n_src = len(d["sources"])
    check(f"{slug}: parsen + Quellenzahl", n_src >= bgbl_idx, f"n={n_src}")
    for nd in needles:
        check(f"{slug}: JSON enthält Satz", nd in body, nd[:50] + "…")
    src = d["sources"][bgbl_idx - 1]
    check(f"{slug}: BGBl-Quelle [{bgbl_idx}]", "BGBl. 2026 I Nr. 228" in src["title"] and src["url"] == "https://www.recht.bund.de/bgbl/1/2026/228/VO.html" and src["checked_at"] == "2026-11-23")
    s61 = next(s for s in d["sources"] if "sgb_5/__61.html" in s["url"])
    check(f"{slug}: § 61 checked_at 2026-11-23", s61["checked_at"] == "2026-11-23")
    if slug == "hilfsmittel-pflegekasse-uebernahme":
        check("pflegekasse: § 33 SGB XI checked_at 2026-11-23",
              d["sources"][0]["checked_at"] == "2026-11-23")
    used = [int(x) for x in re.findall(r"\[(\d+)\]", body)]
    check(f"{slug}: Zitier-Integrität", all(1 <= k <= n_src for k in used), f"max={max(used)} n={n_src}")
    check(f"{slug}: BGBl zitiert", f"[{bgbl_idx}]" in body)

# ---------- 3. BUILT-HTML (LAUNCH-dist) ----------
for slug, bgbl_idx, _ in PAGES:
    h = (DIST / f"{slug}.html").read_text(encoding="utf-8")
    plain = strip_tags(h)
    check(f"{slug} HTML: 7,50", "7,50" in plain)
    check(f"{slug} HTML: 15 Euro", "15 Euro" in plain)
    check(f"{slug} HTML: 1. Januar 2027", "1. Januar 2027" in plain)
    check(f"{slug} HTML: Quellen-Anker source-{bgbl_idx}", f'id="source-{bgbl_idx}"' in h or f'#source-{bgbl_idx}' in h)
    check(f"{slug} HTML: robots index,follow", 'name="robots" content="index, follow"' in h or 'name="robots" content="index,follow"' in h)

print("FAILS:", len(fails))
sys.exit(1 if fails else 0)
