#!/usr/bin/env python3
"""Finde die fehlgeschlagenen Quote-Needles [6]+[8] und hänge sie korrekt an."""
import re, os, subprocess, sys

S = "/Users/mac/.hermes/skills/.archive/grounded-citations/scripts/sources.py"
os.environ["HERMES_CITATION_LEDGER"] = "/Users/mac/agentic-business/barrierefrei-leads/research/paare-191126-ledger.json"
EVID = "/Users/mac/agentic-business/barrierefrei-leads/research/evidence/paare-191126"

def flat(fn):
    return re.sub(r"\s+", " ", open(os.path.join(EVID, fn)).read())

vz_ct = flat("gkv-hn-vertrag.txt")
pp = flat("pflege-panorama.txt")

needles8 = [
    "(1) Dieser Vertrag regelt die mehrkostenfreie",
    "(2) Hausnotrufsysteme bestehen aus einem Hausnotrufgerät",
    "(1) Dieser Vertrag tritt zum 01.04.2026 in Kraft",
    "Er stellt einen Nettopreis dar und beträgt exklusive der jeweils geltenden gesetzlichen Mehrwertsteuer pro Monat 27,00 EUR",
    "hat er nach § 33 Absatz 1 Satz 9 SGB V in Verbindung mit § 40 Absatz 1 Satz 3 SGB XI die Mehrkosten (Aufzahlung) selbst zu tragen.",
    "Dies betrifft auch dadurch bedingte höhere Folgekosten, wie z. B. für Zubehör, Folgeleistungen und Reparaturen.",
    "dass eine Versorgung ohne Mehrkosten möglich ist",
]
for n in needles8:
    print("OK " if n in vz_ct else "MISS", repr(n[:60]))

ok6 = "Hausnotruf kostenlos: 27,00 € monatliche Erstattung durch die Pflegekasse." in pp
print("PP-Kurzquote:", "OK" if ok6 else "MISS")

def attach(sid, text, fn):
    r = subprocess.run([sys.executable, S, "quote", str(sid), "--text", text,
                        "--from", os.path.join(EVID, fn)], capture_output=True, text=True)
    print(f"[{sid}]", "PASS" if r.returncode == 0 else "FAIL", ":", (r.stdout + r.stderr).strip()[:120])

# [6]: nur der erste Satz (zweiter Satz liegt in anderem Block)
attach(6, "Hausnotruf kostenlos: 27,00 € monatliche Erstattung durch die Pflegekasse.", "pflege-panorama.txt")
# [8]: fehlenden Needle in exakter pdftotext-Form anhängen — teste beide Kandidaten
for n in needles8[4:5]:
    attach(8, n, "gkv-hn-vertrag.txt")
