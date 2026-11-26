#!/usr/bin/env python3
"""Reconstruct 2-column reading order for the WIBank Richtlinie PDF extract.

Takes the pdftotext -layout output, splits each physical line at multi-space
column boundaries, dehyphenates, and emits left-column-then-right-column text
per page. Result overwrites wibank-richtlinie.txt; the raw -layout output is
kept as wibank-richtlinie-layout.txt for reference.
"""
import re

SRC = "wibank-richtlinie-layout.txt"
DST = "wibank-richtlinie.txt"

with open(SRC, encoding="utf-8") as fh:
    layout = fh.read()

pages = layout.split("\f")
out_pages = []
for pno, page in enumerate(pages, 1):
    left, right = [], []
    for line in page.split("\n"):
        line = line.rstrip()
        if not line.strip():
            continue
        parts = re.split(r" {2,}", line)
        parts = [p.strip() for p in parts if p.strip()]
        if not parts:
            continue
        left.append(parts[0])
        if len(parts) > 1:
            right.append(" ".join(parts[1:]))
    def dehyph(lines):
        text, prev_hyph = [], False
        for ln in lines:
            if prev_hyph and text:
                text[-1] = text[-1] + ln
            else:
                text.append(ln)
            prev_hyph = ln.endswith("-")
        joined = " ".join(text)
        joined = re.sub(r"([a-zäöüß])- ([a-zäöüß])", r"\1\2", joined)
        return joined
    body = dehyph(left) + "\n\n" + dehyph(right)
    body = re.sub(r"[ \t]+", " ", body)
    out_pages.append(f"[Seite {pno}]\n{body}")

full = "\n\n".join(out_pages).replace("\u00ad", "")
with open(DST, "w", encoding="utf-8") as fh:
    fh.write(full)
print("wrote", DST, len(full), "chars")

QUOTES = [
    "Ein Mensch mit Behinderung im Sinne dieser Richtlinie ist eine Person, die einen Grad der Behinderung von 50 Prozent oder mehr bzw. eine Einstufung in den Pflegegrad 2 oder höher aufweist.",
    "Einbau von geeigneten Aufzügen (z. B. Treppenschrägaufzug, Plattformlift)",
    "barrierereduzierender Badumbau, z. B. Austausch der Badewanne gegen eine Dusche",
    "Die Förderung (Zuwendung) wird als Projektförderung im Wege der Anteilfinanzierung als nicht rückzahlbarer Zuschuss in Höhe von bis zu 50 Prozent der zuwendungsfähigen Ausgaben gewährt.",
    "Förderfähig sind Ausgaben in Höhe von bis zu 30.000 Euro je Wohneinheit, auch wenn die Ausgaben der baulichen Maßnahmen insgesamt höher sind. Dies entspricht einem Zuschuss in Höhe von maximal 15.000 Euro je Wohneinheit.",
    "Zuschüsse anderer Stellen (zum Beispiel Pflegekasse, Rehabilitationsträger, Stiftungen, Versicherungen) werden auf die zuwendungsfähigen Ausgaben angerechnet (Teil II Nr. 13).",
    "Für Maßnahmen, die nach dieser Richtlinie gefördert werden, dürfen in der Regel keine weiteren Fördermittel aus öffentlichen Haushalten in Anspruch genommen werden. Bei Inanspruchnahme von Fördermitteln öffentlicher Haushalte oder anderer Stellen wird der Zuschuss des Landes durch Anrechnung auf die zuwendungsfähigen Ausgaben reduziert (Teil I Nr. 5).",
    "Steht dem Magistrat/Kreisausschuss nur ein begrenztes Mittelkontingent zur Verfügung und reichen die Mittel nicht aus, um alle Anträge zu berücksichtigen, ist eine Auswahl nach sozialer Dringlichkeit vorzunehmen.",
    "Eine Förderung nach diesen Richtlinien wird nur für solche Vorhaben bewilligt, die noch nicht begonnen worden sind (Refinanzierungsverbot).",
    "Als Vorhabenbeginn ist grundsätzlich der Abschluss eines der Ausführung zuzurechnenden Lieferungs- und Leistungsvertrages zu werten, wenn dieser in direktem Zusammenhang mit dem Förderprojekt steht.",
    "beim Magistrat der kreisfreien Stadt, beim Magistrat von kreisangehörigen Städten mit mehr als 50.000 Einwohnerinnen und Einwohnern oder beim Kreisausschuss des Landkreises, in dessen Gebiet das Vorhaben durchgeführt werden soll, einzureichen.",
    "Wirtschafts- und Infrastrukturbank Hessen (WIBank)",
    "Die Bewilligungsbehörde erhebt nach § 13 HWoFG ein einmaliges Bearbeitungsentgelt von 1 Prozent des bewilligten Zuschusses, mindestens jedoch 25 Euro.",
    "Ein Rechtsanspruch auf Gewährung der Förderung besteht nicht.",
    "Die Anzahl der jährlich geförderten Wohnungen wird im jeweils geltenden Haushaltsplan des Landes Hessen unter Nr. 6 des Förderprodukts 87 „Förderung behindertengerechter Umbau“ bei Kap. 07 25 veranschlagt.",
    "Hessisches Ministerium für Wirtschaft, Energie, Verkehr, Wohnen und ländlichen Raum",
    "Wiesbaden, den 14.12.2021/01.09.2023",
    "Diese Richtlinie tritt am Tag nach der Veröffentlichung im Staatsanzeiger für das Land Hessen in Kraft.",
    "Richtlinie des Landes Hessen zur Förderung des behindertengerechten Umbaus von selbstgenutztem Wohneigentum",
    "Die Maßnahmen sollen nach Möglichkeit den Anforderungen der Norm DIN 18040 Teil 2 entsprechen.",
    "• Bad: Um-/Einbau 5.500 Euro",
    "• Küche: Um-/Einbau 5.500 Euro",
    "• Lift-/Aufzugeinbau 6.500 Euro",
    "Maßnahmen mit Ausgaben in Höhe von unter 1.500 Euro werden nicht gefördert.",
]

norm = lambda s: re.sub(r"\s+", " ", s).strip()
flat = norm(full)
fails = 0
for q in QUOTES:
    ok = norm(q) in flat
    if not ok:
        fails += 1
        print("MISSING:", q[:90])
print(f"{len(QUOTES)-fails}/{len(QUOTES)} quotes verbatim in reconstructed extract")
