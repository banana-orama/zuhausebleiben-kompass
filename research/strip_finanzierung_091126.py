#!/usr/bin/env python3
"""Strip Roh-HTML zu Evidenz-Txt für Briefing 20 (treppenlift-finanzierung).
gesetze-im-internet: ISO-8859-1 + numerische Entities → decode, Tags strippen,
Whitespace kollabieren (Tausendertrennzeichen bleiben geschütztes Leerzeichen)."""
import html
import re
import sys
from pathlib import Path

D = Path("research/evidence/finanzierung-091126")

def strip(raw: bytes, law: bool) -> str:
    if law:
        text = raw.decode("iso-8859-1", errors="replace")
    else:
        text = raw.decode("utf-8", errors="replace")
    # Skripte/Styles raus
    text = re.sub(r"<(script|style|noscript)[^>]*>.*?</\1>", " ", text, flags=re.S | re.I)
    # Kommentare raus (vermeidet `//-->`-Reste)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = text.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text

LAW = {"bgb-491", "bgb-492", "bgb-495", "bgb-500", "bgb-502", "bgb-312g", "bgb-356b"}
for f in sorted(D.glob("*.html")):
    stem = f.stem
    if stem.endswith("-home"):
        continue  # Navigations-Seiten nur für Link-Recherche
    out = D / f"{stem}.txt"
    raw = f.read_bytes()
    out.write_text(strip(raw, stem in LAW), encoding="utf-8")
    print(f"{out.name}: {out.stat().st_size} chars")
