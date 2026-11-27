#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quote-Verify Region MV (27.11.): JEDES „...“-Verbatim des Region-JSON gegen die
frische Parent-Evidenz (research/evidence/region-mv-271126-parent/), mit expliziter
Quellen-Zuordnung je Zitat + Absenz-/Count-Needles. Exit 0 <=> alle PASS."""
import html as html_mod
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EV = ROOT / "evidence" / "region-mv-271126-parent"
SOFT = "\u00ad"
SPACES = {"\u00a0": " ", "\u202f": " ", "\u2009": " ", "\u2007": " ", "\u2008": " "}


def dehyph(m):
    pre, post = m.group(1), m.group(2)
    return pre + "-" + post if post[:1].isupper() else pre + post


def norm(text):
    t = text.replace(SOFT, "")
    for k, v in SPACES.items():
        t = t.replace(k, v)
    t = re.sub(r"(\S)-[ \t]*\n[ \t]*(\S)", dehyph, t)
    t = t.replace("\r", "\n").replace("\n", " ")
    t = re.sub(r" +([,.;:!?])", r"\1", t)  # Tag-Strip-Artefakt: Leerzeichen vor Satzzeichen
    return re.sub(r"\s+", " ", t).strip()


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


FILES = {
    "lfi-page": html_text(EV / "lfi-page.html"),
    "lfi-rl": "\n".join((EV / f"lfi-rl{s}.txt").read_text(encoding="utf-8", errors="replace")
                        for s in ("", ".layout", ".raw")),
    "lfi-merkblatt": "\n".join((EV / f"lfi-merkblatt{s}.txt").read_text(encoding="utf-8", errors="replace")
                               for s in ("", ".layout", ".raw")),
    "pm-183": html_text(EV / "pm-183.html"),
    "pm-aufstockung": html_text(EV / "pm-aufstockung.html"),
    "landesplan": "\n".join((EV / f"landesplan{s}.txt").read_text(encoding="utf-8", errors="replace")
                            for s in ("", ".layout", ".raw")),
    "psp": html_text(EV / "psp.html"),
    "sgb11-40": gii_text(EV / "sgb11-40.html"),
    "sgb9-113": gii_text(EV / "sgb9-113.html"),
    "sgb9-77": gii_text(EV / "sgb9-77.html"),
    "bgb-554": gii_text(EV / "bgb-554.html"),
    "kfw-455": html_text(EV / "kfw-455.html"),
    "kfw-159": html_text(EV / "kfw-159.html"),
}
NORM = {k: norm(v) for k, v in FILES.items()}

QUOTE_MAP = [
    # (prefix-des-Join-Texts im JSON, Quell-Datei)
    ("tritt mit Wirkung vom 01. Januar 2026 in Kraft und am 31. Dezember 2026 außer Kraft", "lfi-rl"),
    ("Bewilligungsstelle ist das Landesförderinstitut Mecklenburg-Vorpommern, Geschäftsbereich der NORD/LB Girozentrale", "lfi-rl"),
    ("Die Zuwendungen werden im Rahmen der Projektförderung als nichtrückzahlbare Zuschüsse gewährt.", "lfi-page"),
    ("Schriftliche Anträge sind formgebunden vor Vorhabenbeginn, d. h. vor Abschluss jeglicher Lieferungs- und Leistungsverträge im Landesförderinstitut M-V einzureichen.", "lfi-page"),
    ("Planungsleistungen gelten nicht als Beginn.", "lfi-page"),
    ("Baumaßnahme sollte innerhalb von 12 Monaten nach Bewilligung fertiggestellt sein", "lfi-page"),
    ("Ein Rechtsanspruch des Antragstellers auf Gewährung der Zuwendung besteht nicht", "lfi-page"),
    ("Das Land entscheidet nach pflichtgemäßem Ermessen im Rahmen der verfügbaren Haushaltsmittel.", "lfi-page"),
    ("müssen mindestens 2 000 Euro je Wohnung betragen", "lfi-rl"),
    ("nachgewiesenem Bedarf an einer barrierefreien und uneingeschränkt mit dem Rollstuhl nutzbaren Wohnung gemäß DIN 18040-2", "lfi-rl"),
    ("die Summe aus Landeszuschuss und Zuschuss der Pflegeversicherung die zuwendungsfähigen Ausgaben nicht übersteigen", "lfi-rl"),
    ("Werden zur Finanzierung der Maßnahmen auch finanzielle Zuschüsse zur Verbesserung des individuellen Wohnumfeldes von Pflegebedürftigen gemäß § 40 des Elften Buches Sozialgesetzbuch - Soziale Pflegeversicherung - eingesetzt, darf die Summe aus Landeszuschuss und Zuschuss der Pflegeversicherung die zuwendungsfähigen Ausgaben nicht übersteigen.", "lfi-rl"),
    ("wieder zwei Millionen Euro", "pm-183"),
    ("Seit dem Jahr 2018 wurden rund 18,6 Millionen Euro bewilligt.", "pm-183"),
    ("Das Programm zum Abbau von Barrieren im Wohnungsbestand wurde jetzt um 2 Millionen Euro aufgestockt.", "pm-aufstockung"),
    ("In diesem Jahr hatten wir rund 3,6 Millionen für das Programm zur Verfügung. Bereits Ende Juli war es fast vollständig belegt, sodass wir aufstocken müssen, um einen Antragsannahmestopp zu vermeiden", "pm-aufstockung"),
    ("Gefördert werden bauliche Maßnahmen zur Nachrüstung von barrierefreien Personenaufzügen, Treppenliften oder anderen mechanischen vertikalen Personenfördersystemen an oder in Wohngebäuden mit Miet- und Genossenschaftswohnungen.", "lfi-rl"),
    ("Nachrüstung von Personenaufzügen, Treppenliften oder anderen mechanischen vertikalen Personenfördersystemen", "lfi-rl"),
    ("können Treppenlifte und viele andere Umbaumaßnahmen gefördert werden", "pm-183"),
    ("bis zu 4.500 Euro Förderung für Treppenlifte", "pm-aufstockung"),
    ("Antragsberechtigt sind Eigentümer von selbst genutztem Wohnraum und Mieter mit Zustimmung des Vermieters.", "pm-183"),
    ("A - Eigentümer, deren Grundstücke mit selbst genutztem Wohneigentum bebaut sind", "lfi-page"),
    ("B - Mieter, im Einverständnis mit dem Eigentümer/Vermieter für die selbstgenutzte Mietwohnung", "lfi-page"),
    ("Für Maßnahmen, bei denen der Mieter Zuwendungsempfänger ist, gilt Nummer 5.2.2 entsprechend.", "lfi-rl"),
    ("Erklärung Eigentümer bei Antragstellung durch Mieter", "lfi-page"),
    ("Zuständig sind die Landkreise und kreisfreien Städte in Mecklenburg-Vorpommern als Sozialhilfeträger", "landesplan"),
    ("Auch Menschen mit Demenz im Erwerbsalter haben grundsätzlich als Menschen mit Behinderungen Anspruch auf Leistungen der Eingliederungshilfe nach dem SGB IX, sofern sie die Anspruchsvoraussetzungen erfüllen.", "landesplan"),
    ("Leistungen für Wohnraum", "sgb9-113"),
    ("Die Leistungen umfassen Leistungen für die Beschaffung, den Umbau, die Ausstattung und die Erhaltung von Wohnraum, der den besonderen Bedürfnissen von Menschen mit Behinderungen entspricht.", "sgb9-77"),
    ("Diesen Zuschuss können Sie nicht mehr beantragen.", "kfw-455"),
    ("Sollten im Jahr 2027 erneut Bundesmittel für barrierereduzierende Maßnahmen bereitgestellt werden, wird eine Antragstellung wieder möglich sein.", "kfw-455"),
    ("bis zu 50.000 Euro je Wohneinheit", "kfw-159"),
    ("Treppenlifte, Senkrecht-, Hebe- oder Plattformlifte installieren", "kfw-159"),
    ("Ausnahme: Wird eine Maßnahme (z. B. Badumbau) mit dem Zuschuss der Pflegeversicherung gefördert, können andere Maßnahmen (z. B. Treppenlift) mit dem Kredit der KfW gefördert werden.", "kfw-159"),
    ("Mit 19 Pflegestützpunkten in Mecklenburg-Vorpommern bieten die Kranken- und Pflegekassen gemeinsam mit den Landkreisen und kreisfreien Städten allen Ratsuchenden eine kostenfreie und trägerunabhängige Beratung, wenn es um Fragen rund um das Thema Pflege geht.", "psp"),
    ("Barrierereduzierung, E-Mobilität, Einbruchsschutz und Steckersolargeräte", "bgb-554"),
    ("nicht zugemutet werden kann", "bgb-554"),
    ("Eine zum Nachteil des Mieters abweichende Vereinbarung ist unwirksam.", "bgb-554"),
    # Partials/Sonderformen aus FAQ, Table, Sources-Labels
    ("Mieter, im Einverständnis mit dem Eigentümer/Vermieter für die selbstgenutzte Mietwohnung", "lfi-page"),
    ("formgebunden vor Vorhabenbeginn, d. h. vor Abschluss jeglicher Lieferungs- und Leistungsverträge", "lfi-page"),
    ("Diese Verwaltungsvorschrift tritt mit Wirkung vom 01. Januar 2026 in Kraft und am 31. Dezember 2026 außer Kraft.", "lfi-rl"),
    ("Landesprogramm zur Reduzierung von Barrieren im Wohnungsbestand", "pm-183"),
    ("Reduzierung von Barrieren im Wohnungsbestand", "pm-183"),
    ("Barrieren im Wohnungsbestand", "pm-183"),
    ("um 2 Millionen Euro aufgestockt", "pm-aufstockung"),
    ("rund 3,6 Millionen", "pm-aufstockung"),
    ("Bereits Ende Juli war es fast vollständig belegt", "pm-aufstockung"),
    ("um einen Antragsannahmestopp zu vermeiden", "pm-aufstockung"),
    ("Seit dem Jahr 2018 wurden rund 18,6 Millionen Euro bewilligt", "pm-183"),
    ("Mieter mit Zustimmung des Vermieters", "pm-183"),
    ("der Einbau von Mobilitätshilfen (Treppenliften)", "landesplan"),
    ("Personenaufzüge und Lifte", "lfi-rl"),
    ("Personenaufzüge und Lifte, barrierearmes Wohnen", "lfi-page"),
    ("Altersgerecht Umbauen", "kfw-159"),
    ("Barrierereduzierung – Investitionszuschuss (455-B)", "kfw-455"),
    ("Barrierereduzierung – Investitionszuschuss", "kfw-455"),
    ("Altersgerecht Umbauen – Kredit (159)", "kfw-159"),
]

NEEDLES = [
    # (Beschreibung, Datei, Needle, Modus, Erwartung)
    ("Absenz-Claim leads/FAQ: RL 'Einkommen' 0x", "lfi-rl", "Einkommen", "absent", 0),
    ("Absenz-Claim: lfi-page 'Treppenlift' 0x", "lfi-page", "Treppenlift", "absent", 0),
    ("Absenz-Claim: merkblatt 'Treppenlift' 0x", "lfi-merkblatt", "Treppenlift", "absent", 0),
    ("RL benennt Treppenlift 2x (je Modus x3)", "lfi-rl", "Treppenlifte", "exact", 6),
    ("Mieter-Formular vorhanden", "lfi-page", "Erklärung Eigentümer bei Antragstellung durch Mieter", "min", 1),
    ("Landesplan Treppenlift-Kontext", "landesplan", "Mobilitätshilfen (Treppenliften)", "min", 1),
    ("§ 554 Titelfassung", "bgb-554", "Barrierereduzierung, E-Mobilität, Einbruchsschutz", "min", 1),
]


def main():
    data = json.loads((ROOT.parent / "data" / "region-mecklenburg-vorpommern.json").read_text(encoding="utf-8"))

    def walk_strings(x):
        if isinstance(x, str):
            yield x
        elif isinstance(x, list):
            for i in x:
                yield from walk_strings(i)
        elif isinstance(x, dict):
            for i in x.values():
                yield from walk_strings(i)

    # 1) Vollständigkeit: jedes QUOTE_MAP-Zitat muss im JSON vorkommen (kein verwaister Check)
    all_json = " \n ".join(walk_strings(data))
    missing_in_json = [q for q, _ in QUOTE_MAP if norm(q) not in norm(all_json)]

    # 2) Umgekehrt: jedes „...“-Fragment im JSON muss in der Quote-Map stehen (Deckungsgleichheit)
    # „...“-Fragments im JSON, die bewusst KEIN Quellzitat sind (whitelist)
    WHITELIST = {"einkommen"}
    json_quotes = set()
    for s in walk_strings(data):
        for m in re.finditer(r"„([^„”]+)“", s):
            nq = norm(m.group(1))
            if nq.lower() not in WHITELIST:
                json_quotes.add(nq)
    mapped = {norm(q) for q, _ in QUOTE_MAP}
    unmapped = [q for q in json_quotes if q not in mapped]

    total, failed = 0, []
    for q, f in QUOTE_MAP:
        total += 1
        if norm(q) in NORM[f]:
            continue
        failed.append(f"QUOTE fehlt in {f}: {q[:90]}...")
    n_pass = 0
    for label, f, needle, mode, exp in NEEDLES:
        cnt = len(re.findall(re.escape(norm(needle)), NORM[f], flags=re.IGNORECASE))
        ok = (cnt == 0) if mode == "absent" else (cnt == exp if mode == "exact" else cnt >= exp)
        n_pass += 1 if ok else 0
        total += 1
        if not ok:
            failed.append(f"NEEDLE [{label}] '{needle[:50]}' in {f}: {cnt} (erwartet {mode} {exp})")
    tot = total + len(missing_in_json) + len(unmapped)
    print(f"Quote-Verify MV: {tot} Checks | PASS: {tot - len(failed)} | FAIL: {len(failed)}")
    print(f"  Zitate geprüft: {len(QUOTE_MAP)} | Needles: {len(NEEDLES)} PASS: {n_pass}")
    if missing_in_json:
        print(f"  WARN: {len(missing_in_json)} Quote-Map-Einträge nicht im JSON:")
        for q in missing_in_json:
            print("   -", q[:90])
    if unmapped:
        print(f"  WARN: {len(unmapped)} „...“-Fragments im JSON ohne Quote-Map-Check:")
        for q in unmapped:
            print("   -", q[:90])
    if failed:
        print("FAILS:")
        for f_ in failed:
            print("  ", f_)
        return 1
    print("ALLE QUOTES + NEEDLES PASS.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
