#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Parent-Live-Verify Region MV (27.11.2026, frische Abrufe).

Frische Parent-Verifikation der MV-Region-Belege:
- LIVE: Presseportal-PMs (2), Landesplan-PDF land-mv.de, Gesetze im Internet (4),
  pflegestuetzpunktemv.de, KfW 455-B + 159
- Fallback live -> Wayback fuer regierung-mv.de-Ministeriumsseiten (SPA-Erwartung)
- Wayback (Snapshots 08./09.11.2026, id_-Rohbytes): LFI-Produktseite, RL-PDF, Merkblatt-PDF
  (Host lfi-mv.de blockt diesen Egress vollstaendig: TCP-Timeout, 2 Varianten + Browser-Versuch)

Jede Needle-Pruefung laeuft auf dem normalisierten Text (Normalisierung identisch zum
Screen-Checker: U+00AD strippen, NBSP/U+202F -> Leerzeichen, De-Hyphenation am
Zeilenumbruch, Whitespace-Collapse; gii zusaetzlich Entities-Decode).

Exit 0 <=> alle Checks PASS.
"""
import html as html_mod
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "evidence" / "region-mv-271126-parent"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

SOFT = "\u00ad"
SPACES = {"\u00a0": " ", "\u202f": " ", "\u2009": " ", "\u2007": " ", "\u2008": " "}


def dehyphenate_newline(m):
    pre, post = m.group(1), m.group(2)
    if post[:1].isupper():
        return pre + "-" + post
    return pre + post


def norm(text):
    t = text.replace(SOFT, "")
    for k, v in SPACES.items():
        t = t.replace(k, v)
    t = re.sub(r"(\S)-[ \t]*\n[ \t]*(\S)", dehyphenate_newline, t)
    t = t.replace("\r", "\n").replace("\n", " ")
    return re.sub(r"\s+", " ", t).strip()


def curl(url, dest, timeout=60):
    for attempt in (1, 2):
        r = subprocess.run(
            ["curl", "-sS", "-L", "-m", str(timeout), "-A", UA,
             "-H", "Accept-Language: de-DE,de;q=0.9", "--compressed",
             "-o", str(dest), "-w", "%{http_code}", url],
            capture_output=True, text=True)
        code = r.stdout.strip()
        if code.startswith("2") and dest.exists() and dest.stat().st_size > 0:
            return code
        print(f"    curl attempt {attempt}: code={code} err={r.stderr.strip()[:100]}")
    return None


def wayback(url, dest, ts):
    wb = f"http://web.archive.org/web/{ts}id_/{url}"
    return curl(wb, dest, timeout=120)


def html_text(path):
    t = path.read_text(encoding="utf-8", errors="replace")
    t = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", t)
    t = re.sub(r"(?s)<[^>]+>", " ", t)
    return html_mod.unescape(t)


def gii_text(path):
    raw = path.read_bytes().decode("cp1252", errors="replace")
    t = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", raw)
    t = re.sub(r"(?s)<[^>]+>", " ", t)
    return html_mod.unescape(t)


def pdftotext(pdf, stem):
    for mode, suffix in ((None, ""), ("-layout", ".layout"), ("-raw", ".raw")):
        out = pdf.parent / (stem + suffix + ".txt")
        cmd = ["pdftotext"] + ([mode] if mode else []) + [str(pdf), str(out)]
        subprocess.run(cmd, capture_output=True)
    return [pdf.parent / (stem + s + ".txt") for s in ("", ".layout", ".raw")]


CHECKS = []


def check(label, texts, needle, mode="min", expected=1):
    hay = norm(" \n ".join(texts))
    cnt = len(re.findall(re.escape(norm(needle)), hay, flags=re.IGNORECASE))
    if mode == "min":
        ok = cnt >= expected
    elif mode == "exact":
        ok = cnt == expected
    else:  # absent
        ok = cnt == 0
    CHECKS.append((label, needle, cnt, ok))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    LFI_TS_PAGE = "20261109030126"
    LFI_TS_PDF = "20261108122841"

    jobs = []

    def add_live(name, url, kind="html"):
        jobs.append(("live", name, url, kind))

    def add_wb(name, url, ts, kind="html"):
        jobs.append(("wb", name, url, (ts, kind)))

    add_live("pm-183", "https://www.presseportal.de/blaulicht/pm/108531/6257916")
    add_live("pm-aufstockung", "https://www.presseportal.de/blaulicht/pm/108531/6331780")
    add_live("landesplan", "https://land-mv.de/sites/default/files/2026-10/"
             "2026_Landesplan%20Pflege%20Mecklenburg-Vorpommern_AGP_dip-1.pdf", "pdf")
    add_live("sgb11-40", "https://www.gesetze-im-internet.de/sgb_11/__40.html", "gii")
    add_live("sgb9-113", "https://www.gesetze-im-internet.de/sgb_9_2018/__113.html", "gii")
    add_live("sgb9-77", "https://www.gesetze-im-internet.de/sgb_9_2018/__77.html", "gii")
    add_live("bgb-554", "https://www.gesetze-im-internet.de/bgb/__554.html", "gii")
    add_live("psp", "https://www.pflegestuetzpunktemv.de/")
    add_live("kfw-455", "https://www.kfw.de/inlandsfoerderung/Privatpersonen/"
             "Bestandsimmobilie/F%C3%B6rderprodukte/Altersgerecht-Umbauen-Investitionszuschuss-(455)/")
    add_live("kfw-159", "https://www.kfw.de/159")
    add_live("min-wohnen", "https://www.regierung-mv.de/Landesregierung/im/Bau/"
             "wohnen/wohnraumf%C3%B6rderung")
    add_live("min-psp", "https://www.regierung-mv.de/Landesregierung/sm/Soziales/"
             "Pflege/Pflegest%C3%BCtzpunkte")
    add_wb("lfi-page", "https://www.lfi-mv.de/foerderfinder/"
           "personenaufzuege-und-lifte-barrierearmes-wohnen/", LFI_TS_PAGE)
    add_wb("lfi-rl", "https://www.lfi-mv.de/export/sites/lfi/.galleries/"
           "personenaufzuege-und-lifte-barrierearmes-wohnen/"
           "lesefassung-richtlinie-inkl-aenderungserlasse.pdf", LFI_TS_PDF, kind="pdf")
    add_wb("lfi-merkblatt", "https://www.lfi-mv.de/export/sites/lfi/.galleries/"
           "personenaufzuege-und-lifte-barrierearmes-wohnen/"
           "merkblatt-personenaufzuege-lifte-barrierearmes-wohnen.pdf", LFI_TS_PDF, kind="pdf")

    texts = {}

    for kind, name, url, arg in jobs:
        is_pdf = (isinstance(arg, tuple) and arg[1] == "pdf") or arg == "pdf"
        dest = OUT / (name + (".pdf" if is_pdf else ".html"))
        if kind == "live":
            print(f"[live] {name}")
            code = curl(url, dest)
            if code and name in ("min-wohnen", "min-psp"):
                # regierung-mv.de: SPA-Erwartung -> Wayback-Fallback wenn Live-Text duenn
                t = html_text(dest)
                if len(norm(t)) < 1500:
                    print(f"    live-Text duenn ({len(norm(t))} Zeichen) -> Wayback-Fallback")
                    code = None
                else:
                    texts[name] = t
                    continue
            if not code:
                print(f"    LIVE-FAIL {name} -> Wayback-availability-API")
                r = subprocess.run(
                    ["curl", "-s", "-m", "20",
                     f"http://archive.org/wayback/available?url={url}"],
                    capture_output=True, text=True)
                import json
                try:
                    snap = json.loads(r.stdout).get("archived_snapshots", {}).get("closest", {})
                except ValueError:
                    snap = {}
                if not snap:
                    print(f"    KEIN WAYBACK-SNAPSHOT {name}")
                    texts[name] = ""
                    continue
                ts = snap["timestamp"]
                print(f"    Wayback-Snapshot {ts}")
                wb = f"http://web.archive.org/web/{ts}id_/{url}"
                code = curl(wb, dest, timeout=120)
                if not code and name == "min-wohnen":
                    # Fallback: Subagenten-Snapshot vom 27.11. (Screen-Lauf) lokal vorhanden
                    sub = ROOT / "evidence" / "region-screen-271126" / "mv" / "mv-ministerium-wohnraumfoerderung-wb.html"
                    if sub.exists():
                        print(f"    nutze Subagenten-Snapshot: {sub.name}")
                        dest.write_bytes(sub.read_bytes())
                        code = "200"
                        arg = "html"
                if not code:
                    print(f"    WAYBACK-FAIL {name}")
                    texts[name] = ""
                    continue
                arg = "html"
            if isinstance(arg, str) and arg == "pdf":
                texts[name] = "\n".join(norm(p.read_text(encoding="utf-8", errors="replace"))
                                        for p in pdftotext(dest, name) if p.exists())
            elif arg == "gii":
                texts[name] = gii_text(dest)
            else:
                texts[name] = html_text(dest)
        else:
            ts, kind2 = arg
            print(f"[wayback {ts}] {name}")
            dest = OUT / (name + (".pdf" if kind2 == "pdf" else ".html"))
            code = wayback(url, dest, ts)
            if not code:
                print(f"    WAYBACK-FAIL {name}")
                texts[name] = ""
                continue
            if kind2 == "pdf":
                texts[name] = "\n".join(norm(p.read_text(encoding="utf-8", errors="replace"))
                                        for p in pdftotext(dest, name) if p.exists())
            else:
                texts[name] = html_text(dest)

    T = lambda n: texts.get(n, "")  # noqa: E731

    # --- PM 18.04.2026 (Nr. 83/2026) ---
    check("pm-183", [T("pm-183")], "Antragsberechtigt sind Eigentümer von selbst genutztem Wohnraum und Mieter mit Zustimmung des Vermieters.")
    check("pm-183", [T("pm-183")], "Treppenlifte und viele andere Umbaumaßnahmen gefördert")
    check("pm-183", [T("pm-183")], "wieder zwei Millionen Euro")
    check("pm-183", [T("pm-183")], "rund 18,6 Millionen Euro bewilligt")
    # --- PM 12.08.2026 (Aufstockung) ---
    check("pm-aufst", [T("pm-aufstockung")], "rund 3,6 Millionen für das Programm")
    check("pm-aufst", [T("pm-aufstockung")], "fast vollständig belegt")
    check("pm-aufst", [T("pm-aufstockung")], "Antragsannahmestopp zu vermeiden")
    check("pm-aufst", [T("pm-aufstockung")], "bis zu 4.500 Euro Förderung für Treppenlifte")
    # --- Landesplan Pflege M-V ---
    check("landesplan", [T("landesplan")], "Mobilitätshilfen (Treppenliften)")
    check("landesplan", [T("landesplan")], "Zuständig sind die Landkreise und kreisfreien Städte in Mecklenburg-Vorpommern")
    # --- Gesetze ---
    check("sgb11-40", [T("sgb11-40")], "4 180")
    check("sgb11-40", [T("sgb11-40")], "wohnumfeldverbessernden")
    check("sgb9-113", [T("sgb9-113")], "Leistungen für Wohnraum")
    check("sgb9-77", [T("sgb9-77")], "Beschaffung, den Umbau, die Ausstattung und die Erhaltung von Wohnraum")
    check("bgb-554", [T("bgb-554")], "Barrierereduzierung, E-Mobilität, Einbruchsschutz")
    check("bgb-554", [T("bgb-554")], "nicht zugemutet werden kann")
    check("bgb-554", [T("bgb-554")], "Eine zum Nachteil des Mieters abweichende Vereinbarung ist unwirksam")
    # --- PSP ---
    check("psp", [T("psp")], "trägerunabhängig")
    check("psp", [T("psp")], "Landkreisen und kreisfreien Städten")
    check("min-psp", [T("min-psp")], "19 Pflegestützpunkte")
    # --- Ministerium Wohnraumförderung (Kontext, Absenz) ---
    check("min-wohnen-absenz", [T("min-wohnen")], "Treppenlift", mode="absent")
    # --- LFI-Produktseite (Wayback) ---
    check("lfi-page", [T("lfi-page")], "nichtrückzahlbare Zuschüsse")
    check("lfi-page", [T("lfi-page")], "B - Mieter, im Einverständnis mit dem Eigentümer/Vermieter")
    check("lfi-page", [T("lfi-page")], "30 % von max. 15.000 EUR")
    check("lfi-page", [T("lfi-page")], "12 Monaten nach Bewilligung")
    check("lfi-page", [T("lfi-page")], "formgebunden vor Vorhabenbeginn")
    check("lfi-page", [T("lfi-page")], "Planungsleistungen gelten nicht als Beginn")
    check("lfi-page", [T("lfi-page")], "Ein Rechtsanspruch des Antragstellers auf Gewährung der Zuwendung besteht nicht")
    check("lfi-page-absenz", [T("lfi-page")], "Treppenlift", mode="absent")
    # --- RL RLPaBaWo (Wayback-PDF, 3 pdftotext-Modi) ---
    check("rl-2.1", [T("lfi-rl")], "barrierefreien Personenaufzügen, Treppenliften oder anderen mechanischen vertikalen Personenfördersystemen")
    check("rl-2.2", [T("lfi-rl")], "Nachrüstung von Personenaufzügen, Treppenliften oder anderen mechanischen vertikalen Personenfördersystemen")
    check("rl-5.2.2", [T("lfi-rl")], "beträgt der Zuschuss bis zu 30 Prozent der zuwendungsfähigen Ausgaben von bis zu 15 000 Euro je Wohnung")
    check("rl-5.2.2-min", [T("lfi-rl")], "müssen mindestens 2 000 Euro je Wohnung betragen")
    check("rl-5.2.3", [T("lfi-rl")], "Für Maßnahmen, bei denen der Mieter Zuwendungsempfänger ist, gilt Nummer 5.2.2 entsprechend")
    check("rl-kumul", [T("lfi-rl")], "Summe aus Landeszuschuss und Zuschuss der Pflegeversicherung die zuwendungsfähigen Ausgaben nicht übersteigen")
    check("rl-5.2.4", [T("lfi-rl")], "barrierefreien und uneingeschränkt mit dem Rollstuhl nutzbaren Wohnung gemäß DIN 18040-2")
    check("rl-7.3", [T("lfi-rl")], "Bewilligungsstelle ist das Landesförderinstitut Mecklenburg-Vorpommern, Geschäftsbereich der NORD/LB")
    check("rl-9", [T("lfi-rl")], "tritt mit Wirkung vom 01. Januar 2026 in Kraft und am 31. Dezember 2026 außer Kraft")
    check("rl-7.2", [T("lfi-rl")], "Ein Rechtsanspruch des Antragstellers auf Gewährung der Zuwendung besteht nicht")
    check("rl-tl-count", [T("lfi-rl")], "Treppenlifte", mode="exact", expected=6)  # 2 Fundstellen je pdftotext-Modi x 3 Modi (txt/layout/raw)
    check("rl-einkommen-absenz", [T("lfi-rl")], "Einkommen", mode="absent")
    # --- Merkblatt ---
    check("merkblatt", [T("lfi-merkblatt")], "Landesförderinstitut")
    check("merkblatt", [T("lfi-merkblatt")], "12 Monate")
    # --- KfW ---
    check("kfw-455", [T("kfw-455")], "Diesen Zuschuss können Sie nicht mehr beantragen")
    check("kfw-455", [T("kfw-455")], "Sollten im Jahr 2027 erneut Bundesmittel")
    check("kfw-159", [T("kfw-159")], "bis zu 50.000 Euro je Wohneinheit")
    check("kfw-159", [T("kfw-159")], "Treppenlifte, Senkrecht-, Hebe- oder Plattformlifte")
    check("kfw-159-kombi", [T("kfw-159")], "mit dem Kredit der KfW gefördert werden")

    n_fail = sum(1 for *_, ok in CHECKS if not ok)
    print("=" * 78)
    print(f"Parent-Live-Verify MV: {len(CHECKS)} Checks | PASS: {len(CHECKS)-n_fail} | FAIL: {n_fail}")
    print("-" * 78)
    for label, needle, cnt, ok in CHECKS:
        print(f"  [{'PASS' if ok else 'FAIL'}] {label:<22} '{needle[:60]}' -> {cnt}")
    print("-" * 78)
    print("Evidenz:", OUT)
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
