#!/usr/bin/env python3
"""Repariert die mangelnd-escapte Zeile 60 in research/llms-txt.py (Batch 15)."""
from pathlib import Path

p = Path("research/llms-txt.py")
lines = p.read_text(encoding="utf-8").split("\n")
i = 59  # 0-indexed = Zeile 60
assert "hausnotruf-schluesselhinterlegung" in lines[i], f"Zeile 60 unerwartet: {lines[i][:80]}"
fixed = [
    '    "hausnotruf-schluesselhinterlegung": "Die Schlüsselfrage beim Hausnotruf: vier Wege (Zweitschlüssel, Dienst-Verwahrung, Pflegedienst, Tresor) mit belegten, streuenden Kostenangaben, Notfall-Ablauf ohne Schlüssel (Feuerwehr-Faustregel, Schlüsseldienst-Abzocke, Urteilsberichte) und den Fragen fürs Einrichtungsgespräch.",',
    '    "treppenlift-finanzierung": "Treppenlift finanzieren: belegte Herstellermodelle (50/50 zinsfrei in 12 Monaten, easyCredit-Raten 2 bis 60 Monate, individuelle Vereinbarungen mit dokumentierten Widersprüchen), Verbraucherdarlehen-Rechte im Gesetzestext (Widerruf, Sondertilgung, Vorfälligkeit), die Null-Prozent-Nuance und die Kredit-Reform ab 20.11.2026.",',
]
lines[i:i + 1] = fixed
p.write_text("\n".join(lines), encoding="utf-8")
print("Zeile 60 repariert, neue Zeile 61:", lines[i + 1][:60])
