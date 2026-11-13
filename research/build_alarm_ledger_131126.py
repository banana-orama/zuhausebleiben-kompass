#!/usr/bin/env python3
"""Baut research/alarm-ablauf-131126-ledger.json (Briefing 26).

Jedes Zitat wird gegen die Evidence-Textdatei verbatim geprüft
(Whitespace-normalisiert); ein einziger Missmatch bricht den Build ab.
Format wie research/mietwohnung-ledger.json.
"""
import json
import pathlib
import re
import sys

EV = pathlib.Path(__file__).resolve().parent.parent / "research" / "evidence" / "alarm-131126"


def norm(t: str) -> str:
    t = t.replace("\u00a0", " ")
    return re.sub(r"\s+", " ", t)


SOURCES = [
    (1, "https://n-tv.de/regionales/sachsen/Wenn-ein-Knopfdruck-das-Leben-retten-kann-id31502587.html",
     "dpa-Bericht (n-tv): „Wenn ein Knopfdruck das Leben retten kann“ — DRK-Hausnotrufzentrale Sachsen", "ntv-dpa"),
    (2, "https://www.bv-hausnotruf.de/hausnotruf/ablauf-eines-notrufs",
     "Bundesverband Hausnotruf: Ablauf eines Hausnotrufs", "bv-ablauf"),
    (3, "https://www.malteser.de/hausnotruf/faq.html",
     "Malteser (Herstellerangabe): Hausnotruf-FAQ", "malteser-faq"),
    (4, "https://gesund.bund.de/hausnotruf",
     "gesund.bund.de (BMG-Portal): Hausnotruf", "gesundbund"),
    (5, "https://www.sieversgruppe.de/autavie-hausnotruf/massnahmenplan-hausnotruf-so-wird-im-notfall-geholfen",
     "Sieversgruppe/autavie (Herstellerangabe): Maßnahmenplan Hausnotruf", "sievers"),
    (6, "https://datenbank.nwb.de/Dokument/697288/",
     "BGH, Urteil v. 11.05.2017 - III ZR 92/16 (Hausnotrufvertrag, Leitsatz/Urteilstext via NWB-Datenbank)", "bgh-nwb"),
    (7, "https://stange.de/2017/05/11/bgh-hausnotrufvertrag110317/",
     "BGH-Pressemitteilung Nr. 071/2017 vom 11.05.2017 (Sachverhalt, wiedergegeben bei stange.de)", "bgh-stange"),
    (8, "https://medivato.de/ratgeber/notrufzentrale-erklaert-was-passiert-nach-dem-knopfdruck",
     "medivato (Anbieter-Magazin): Notrufzentrale erklärt — was passiert nach dem Knopfdruck", "medivato"),
    (9, "https://www.verbraucherzentrale.de/wissen/gesundheit-pflege/pflege-zu-hause/hausnotrufsysteme-erklaert-so-helfen-sie-im-notfall-funktionen-vorteile-kosten-10566",
     "Verbraucherzentrale: Hausnotrufsysteme erklärt (Basistarif-Inhalte, 24-Stunden-Zentrale)", "vz"),
]

QUOTES = {
 1: [
  "Wenn sie drücken und wir nichts hören, kommt immer jemand",
  "Das Ziel sei, möglichst jeden Alarm innerhalb von 30 Sekunden anzunehmen, sagt Küttner. Die DRK-Vorgabe liege bei 90 Prozent.",
  "Tatsächlich schafften es die Mitarbeiter in Sachsen nach ihren Angaben, mehr als 94 Prozent der Alarmmeldungen innerhalb dieser Zeit entgegenzunehmen.",
  "Bei 80 Prozent Fehlalarm, Probealarm sind wir schon",
  "etwa beim Anziehen eines Pullovers oder wenn eine Notrufkette beim Vorbeugen gegen den Körper gedrückt werde",
  "Wir sind weder der Rettungsdienst noch ist der Rettungsdienst ein Fahrdienst",
  "Nach Angaben des Bundesverbands Hausnotruf nutzten 2024 mehr als 1,2 Millionen Menschen in Deutschland einen Hausnotruf",
  "Täglich gingen etwa 11.000 Rufe ein, aus denen rund 3.600 Einsätze vor Ort entstünden",
  "Rund 350 Alarmmeldungen aus Sachsen",
  "Wir fragen zum Schluss eigentlich klassisch das ab, was auch jede Leitstelle abfragen würde, wenn man die 112 anruft",
  "Manchmal brauche jemand lediglich Unterstützung, um wieder in seinen Sessel zu gelangen",
  "Ärger müssten die Nutzer deshalb nicht befürchten",
  "Lieber einmal zu oft als einmal zu wenig",
  "Denn hinter einem stillen Notruf kann ein harmloser Fehlalarm stecken",
  "Nach Angaben von Eichholz insgesamt rund 23.000 Teilnehmer",
 ],
 2: [
  "Das Drücken des Notrufknopfs löst eine vorab mit dem Hausnotruf-Nutzer abgestimmte Alarmkette aus",
  "An erster Stelle steht die Entgegennahme des Notrufs",
  "indem Angehörige, Nachbarn, der Pflegedienst oder Rettungsdienst verständigt werden",
  "Der Mitarbeiter in der Notrufzentrale sieht auf seinem Bildschirm mit dem eingehenden Anruf die hinterlegten Daten der Hausnotruf-Nutzerin",
  "Da die Nutzerin über Schmerzen klagt, alarmiert der Mitarbeiter den Rettungsdienst",
 ],
 3: [
  "Sollte einmal im Notfall nach Auslösen des Alarms der Sprechkontakt nicht zustande kommen, alarmiert unsere Notrufzentrale in jedem Fall den Bereitschafts- oder Rettungsdienst",
  "Der Sprechkontakt mit der Notrufzentrale der Malteser funktioniert über den eingebauten Lautsprecher und ein empfindliches Mikrofon in der Basisstation",
  "ist so eine Verständigung mit unserer Notrufzentrale auch aus angrenzenden Räumen möglich",
  "Im medizinischen Notfall alarmieren wir umgehend den Rettungsdienst für Sie",
  "Die Hausnotrufzentrale kann jede Art von Rettungskräften, also auch Feuerwehr und Polizei, alarmieren",
  "24 oder 12 Stunden lang nicht über die Tagestaste melden, löst Ihr Gerät automatisch einen Alarm aus",
 ],
 4: [
  "Durch Testrufe lässt sich üben, wie ein Notruf ausgelöst wird",
  "Das gibt Sicherheit für den Ernstfall",
  "dass man versehentlich einen Notruf auslöst. Das ist kein Problem",
  "wird im Gespräch mit der Mitarbeiterin oder dem Mitarbeiter der Hausnotruf-Zentrale geklärt",
  "Die Mitarbeitenden der Hausnotruf-Zentrale sehen trotzdem, wer den Alarm ausgelöst hat und organisieren die notwendige Hilfe",
  "Hausnotruf ohne Zentrale",
  "kann es jedoch in Notsituationen zu unnötigen Verzögerungen kommen",
 ],
 5: [
  "Der Maßnahmenplan legt fest, was nach einem ausgelösten Notruf passiert",
  "Soll bei fehlendem Sprechkontakt zunächst versucht werden, die teilnehmende Person telefonisch zu erreichen",
  "Er ersetzt nicht die individuelle Einschätzung der Situation durch die Fachkraft in der Notrufzentrale",
  "Die Angabe zum Krankheitsbild ist freiwillig",
  "Ob und wie ein hinterlegter Schlüssel genutzt wird, richtet sich nach dem vereinbarten Ablauf und der konkreten Situation",
 ],
 6: [
  "Wer eine besondere Berufs- oder Organisationspflicht, die dem Schutz von Leben und Gesundheit anderer dient, grob vernachlässigt hat, kann nach Treu und Glauben die Folgen der Ungewissheit, ob der Schaden abwendbar war, nicht dem Geschädigten aufbürden.",
  "Den ihm obliegenden Entlastungsbeweis ( § 280 Abs. 1 Satz 2 BGB ) hat er nicht geführt.",
  "die in der konkreten Situation erforderliche Sorgfalt in besonders schwerem Maße verletzt",
  "der Streithelferin an einer mindestens 16 Stunden umfassenden Ausbildung in Erster Hilfe erfolgreich teilgenommen haben und wurde jährlich darin fortgebildet",
 ],
 7: [
  "Der den Anruf entgegennehmende Mitarbeiter des Beklagten vernahm minutenlang lediglich ein Stöhnen",
  "ein nicht mehr ganz frischer, wahrscheinlich ein bis drei Tage zurückliegender Schlaganfall diagnostiziert wurde",
  "Dessen gravierende Folgen wären vermieden worden, wenn der den Notruf entgegennehmende Mitarbeite",
  "Der 1934 geborene Kläger",
  "lebte er allein in einer Wohnung in einem Seniorenwohnheim bei Pflegestufe 2",
  "Nr. 071/2017 vom 11.05.2017",
 ],
 8: [
  "Ein Hausnotruf ersetzt nicht die Notrufnummer 112",
  "per Knopfdruck am Funkarmband / Notrufgerät / an der Basisstation",
  "automatisch durch eine Sturzerkennung",
  "lieber einmal zu früh als zu spät",
 ],
 9: [
  "24-Stunden-Erreichbarkeit der Notrufzentrale",
  "Bereitstellung des Geräts",
  "rund um die Uhr besetzten Notrufzentrale",
 ],
}

ledger = {"version": 1, "sources": []}
fails = []
for sid, url, title, fname in SOURCES:
    text = norm((EV / f"{fname}.txt").read_text(errors="ignore"))
    quotes = []
    for q in QUOTES[sid]:
        if norm(q) in text:
            quotes.append({"text": q, "added": "2026-11-13"})
        else:
            fails.append((sid, q[:70]))
    ledger["sources"].append({
        "id": sid, "url": url, "title": title, "accessed": "2026-11-13", "quotes": quotes,
    })

out = pathlib.Path(__file__).resolve().parent.parent / "research" / "alarm-ablauf-131126-ledger.json"
out.write_text(json.dumps(ledger, ensure_ascii=False, indent=1), encoding="utf-8")
total = sum(len(s["quotes"]) for s in ledger["sources"])
print(f"ledger: {out} — {total} Zitate verbatim verifiziert, {len(fails)} FAILS")
for sid, q in fails:
    print(f"  FAIL [{sid}] {q}")
sys.exit(1 if fails else 0)
