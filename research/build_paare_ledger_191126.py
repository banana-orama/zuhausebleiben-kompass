#!/usr/bin/env python3
"""Ledger-Aufbau hausnotruf-fuer-paare (19.11.2026): 10 Quellen + Verbatim-Quotes."""
import subprocess, os, sys

S = "/Users/mac/.hermes/skills/.archive/grounded-citations/scripts/sources.py"
os.environ["HERMES_CITATION_LEDGER"] = "/Users/mac/agentic-business/barrierefrei-leads/research/paare-191126-ledger.json"
EVID = "/Users/mac/agentic-business/barrierefrei-leads/research/evidence/paare-191126"

def run(*args):
    r = subprocess.run([sys.executable, S, *args], capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip()
    if "FAIL" in out or r.returncode != 0:
        print("FAIL:", " ".join(args[:3]), "->", out[:200])
    return out

ADD = [
    ("https://www.gkv-spitzenverband.de/media/dokumente/pflegeversicherung/hausnotrufvertraege/Hausnotruf-Vertrag_mit_Verbaenden_und_Einzelleistungserbringern_Vertragstext_AC_TK_19_00_452.pdf",
     "GKV-Spitzenverband: Hausnotruf-Vertrag mit Verbänden und Einzelleistungserbringern (AC/TK 19/00/452, in Kraft 01.04.2026)"),
    ("https://www.gkv-spitzenverband.de/pflegeversicherung/pflegehilfsmittelvertraege/pflegehilfsmittelvertraege.jsp",
     "GKV-Spitzenverband: Pflegehilfsmittelverträge / Hausnotrufverträge"),
    ("https://www.gkv-90prozent.de/ausgabe/47/kurzmeldungen/47_hausnotruf/47_hausnotruf.html",
     "GKV-Spitzenverband e-Magazin 90 Prozent (Ausgabe 47): Neue bundesweite Hausnotruf-Verträge"),
]
for url, title in ADD:
    print(run("add", url, "--title", title).strip())

QUOTES = [
    (1, "Für die Nutzung benötigen Sie lediglich zwei kleine Geräte", "malteser.txt"),
    (1, "Der Notrufknopf ist handlich und kann als Armband am Handgelenk oder als Kette um den Hals getragen werden.", "malteser.txt"),
    (1, "der Malteser Hausnotruf funktioniert auch über Mobilfunk", "malteser.txt"),
    (2, "Mit Pflegegrad übernimmt die Pflegekasse bis zu 27 Euro monatlich.", "vz-10566.txt"),
    (2, "Seit dem 1. April 2026 liegen die bei 27 Euro monatlich.", "vz-10566.txt"),
    (2, "Wenn ein Pflegegrad vorhanden ist und die beantragende Person fast den ganzen Tag allein ist.", "vz-10566.txt"),
    (2, "Wenn die pflegebedürftige Person mit jemandem zusammenlebt, muss diese oft und länger abwesend sein, zum Beispiel, weil sie bei der Arbeit ist.", "vz-10566.txt"),
    (2, "Der Medizinische Dienst prüft für die Pflegekasse, ob die Voraussetzungen erfüllt sind.", "vz-10566.txt"),
    (2, "Liegen diese Voraussetzungen nicht vor, müssen Sie die Kosten selbst tragen. Eventuell ist Unterstützung durch das Sozialamt möglich.", "vz-10566.txt"),
    (2, "Der Hausnotrufanbieter muss Vertragspartner der Pflegekasse sein.", "vz-10566.txt"),
    (2, "Im Basistarif sind enthalten: Bereitstellung des Geräts Ausstattung mit Funksender (Armband oder Halskette mit Notfallknopf) Installation und Einweisung 24-Stunden-Erreichbarkeit der Notrufzentrale", "vz-10566.txt"),
    (2, "Je nach Situation werden dann Angehörige, Pflegedienste oder der Rettungsdienst oder Notarzt verständigt.", "vz-10566.txt"),
    (2, "Für Menschen mit Demenz ist er oft weniger geeignet, da sie den Knopf nicht immer gezielt betätigen können.", "vz-10566.txt"),
    (2, "Zusatzleistungen können die Kosten deutlich erhöhen. Diese müssen Sie selbst tragen.", "vz-10566.txt"),
    (2, "Sie benötigen einen Telefon- oder Internetanschluss sowie eine Steckdose für die Basisstation.", "vz-10566.txt"),
    (2, "Ein Gerät mit SIM-Karte und Akku ist empfehlenswert, damit das System auch bei Strom- oder Internetausfall funktioniert.", "vz-10566.txt"),
    (2, "Dazu gehören: Adresse und Zugang zur Wohnung, Gesundheitszustand und Medikamente sowie die Kontaktdaten von Angehörigen.", "vz-10566.txt"),
    (3, "ein Handsender, ein Basisgerät", "drk-bv.txt"),
    (3, "Bei Teilnehmenden mit anerkanntem Pflegegrad übernimmt die Pflegekasse in der Regel die Kosten des Basistarifs und die einmalige Anschlussgebühr.", "drk-bv.txt"),
    (3, "Bearbeitung aller eingehenden Alarme und Verständigung von Bezugspersonen, Hausärzten, Pflegediensten etc. per Telefon", "drk-bv.txt"),
    (6, "Hausnotruf kostenlos: 27,00 € monatliche Erstattung durch die Pflegekasse. Wir vermitteln geprüfte Anbieter und kümmern uns kostenlos um den Antrag.", "pflege-panorama.txt"),
    (6, "Der monatliche Zuschuss liegt derzeit bei bis zu 27,00 Euro pro Person. Dies bedeutet, dass bei einem Paartarif, bei dem beide Partner einen anerkannten Pflegegrad haben, bis zu 54 Euro monatlich von der Pflegekasse übernommen werden können.", "pflege-panorama.txt"),
    (6, "Ein Hausnotruf für Paare bietet nicht nur doppelte Sicherheit, sondern oft auch einen attraktiven Vorteilspreis.", "pflege-panorama.txt"),
    (7, "technische Ausstattung mit Basisstation, Handsender und Mobilgerät für Rundumschutz daheim und unterwegs.", "johanniter.txt"),
    (8, "(1) Dieser Vertrag regelt die mehrkostenfreie (beziehungsweise aufzahlungsfreie) Versorgung der Versicherten mit Hausnotrufsystemen/Hausnotrufleistungen der Produktgruppe 52 „Pflegehilfsmittel zur selbständigeren Lebensführung/Mobilität“ des Pflegehilfsmittelverzeichnisses gemäß § 78 Absatz 2 SGB XI, die einen Anspruch auf Leistungen der Pflegeversicherung nach § 40 Absatz 1 und Absatz 3 SGB XI haben.", "gkv-hn-vertrag.txt"),
    (8, "(2) Hausnotrufsysteme bestehen aus einem Hausnotrufgerät sowie einem Alarm-/Funksender und sind an eine Hausnotrufzentrale angeschlossen.", "gkv-hn-vertrag.txt"),
    (8, "(1) Dieser Vertrag tritt zum 01.04.2026 in Kraft. Er gilt für alle Bestandsversorgungen und Neuversorgungen ab dem Zeitpunkt des Inkrafttretens. Bei Bestandsversorgungen ist eine neue Genehmigung nicht erforderlich.", "gkv-hn-vertrag.txt"),
    (8, "Er stellt einen Nettopreis dar und beträgt exklusive der jeweils geltenden gesetzlichen Mehrwertsteuer pro Monat 27,00 EUR", "gkv-hn-vertrag.txt"),
    (8, "hat er nach § 33 Absatz 1 Satz 9 SGB V in Verbindung mit § 40 Absatz 1 Satz 3 SGB XI die Mehrkosten (Aufzahlung) selbst zu tragen.", "gkv-hn-vertrag.txt"),
    (8, "Dies betrifft auch dadurch bedingte höhere Folgekosten, wie z. B. für Zubehör, Folgeleistungen und Reparaturen.", "gkv-hn-vertrag.txt"),
    (8, "dass eine Versorgung ohne Mehrkosten möglich ist", "gkv-hn-vertrag.txt"),
    (9, "Der GKV-Spitzenverband hat zwischenzeitlich neue beitrittsfähige Verträge nach § 78 Absatz 1 SGB XI über die Versorgung der Versicherten mit Hausnotrufsystemen verhandelt und geschlossen, die am 01.04.2026 in Kraft getreten sind.", "raw-gkv-phmv.html"),
    (10, "Die neuen Verträge zu Hausnotrufsystemen sind am 1. April 2026 Kraft getreten und haben eine Mindestlaufzeit von zwei Jahren.", "raw-gkv-90prozent.html"),
]

fails = 0
for sid, text, fn in QUOTES:
    out = run("quote", str(sid), "--text", text, "--from", os.path.join(EVID, fn))
    if "FAIL" in out or "Error" in out:
        fails += 1
        print(f"QUOTE-FAIL [{sid}] {fn}: {out[:160]}")
print(f"\n{len(QUOTES)} Quote-Versuche, {fails} Fehlversuche")
print(run("list"))
