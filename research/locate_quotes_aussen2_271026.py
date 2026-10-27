#!/usr/bin/env python3
"""Extract full passages for remaining briefing-13 quotes + IP-absence proof on manufacturer pages."""
import pathlib, re

E = pathlib.Path("research/evidence/aussenlift-271026")

def show(name, needle, before=60, after=900, n=1):
    txt = (E / f"{name}.txt").read_text(encoding="utf-8")
    low = txt.lower()
    start = 0
    for i in range(n):
        idx = low.find(needle.lower(), start)
        if idx < 0:
            print(f"[{name}:{needle}] NOT FOUND")
            return
        print(f"== {name} [{needle}] #{i}:\n{txt[max(0, idx-before):idx+after]}\n")
        start = idx + len(needle)

show("tlw-aussenlift", "Funktioniert ein Außenlift im Winter", after=700)
show("personenaufzuege-aussen", "Kann man einen Treppenlift für außen mieten", after=800)
show("personenaufzuege-aussen", "Sitz-Treppenlifte für außen liegen insgesamt", after=400)
show("trep-preise-aussen", "Für den Betrieb genügt ein 230-Volt-Anschluss", after=500)
show("lifta-faq", "Gerade Treppe, Treppenlift innen", after=520)
show("lifta-aussenlifte", "Wie der Name verrät", after=800)

print("\n===== IP-ABSCHAZ-PROOF (Herstellerseiten) =====")
for name in ["hiro-aussen", "lifta-aussenlifte", "lifta-treppenlift"]:
    txt = (E / f"{name}.txt").read_text(encoding="utf-8")
    hits = re.findall(r".{50}IP[- ]?(?:4|5|6|X|Schutz|54|65|67).{50}", txt, flags=re.I)
    print(f"  {name}: {len(hits)} IP-Treffer")
    for h in hits[:3]:
        print("   >", h)

print("\n===== 'Außen'-Vorkommen im Treppenlift-/FAQ-Kontext (Lifta Preise komplett) =====")
txt = (E / "lifta-faq.txt").read_text(encoding="utf-8")
for m in re.finditer(r"[^.]*Treppenlift außen[^.]*\.", txt):
    print("  FAQ>", m.group(0)[:200])
