#!/usr/bin/env python3
"""Ledger-Verify für Briefing 20 (treppenlift-finanzierung), Prüfdatum 09.11.2026.
Jedes Zitat muss wörtlich (modulo Whitespace) in der Evidenz-Txt stehen.
Absenz-Checks: Lifta-Seite ohne zinsfrei/0-%-Angabe (gerenderter Text).
Arithmetik: Rechenbeispiel Restbetrag (fiktiv, im Artikel deklariert)."""
import re
import sys
from pathlib import Path

D = Path("research/evidence/finanzierung-091126")
results = []


def norm(s: str) -> str:
    s = re.sub(r"\s+", " ", s).strip()
    # Strip-Artefakt: Leerzeichen vor Satzzeichen entfernen (Wortlaut bleibt identisch)
    return re.sub(r"\s+([,.:;!?])", r"\1", s)


def check(name: str, ok: bool, detail: str = "") -> None:
    results.append((name, ok, detail))
    print(("PASS" if ok else "FAIL") + f" | {name}" + (f" | {detail}" if detail and not ok else ""))


def quote(src: str, span: str, label: str = "") -> None:
    t = norm((D / src).read_text(encoding="utf-8"))
    check(f"{src}: {label or span[:50]}...", norm(span) in t)


# --- TK Home Solutions (Herstellerangabe) ---
q = "tke-finanzierung.txt"
for s, l in [
    ("Nur 50 % des Kaufpreises bei Montage", "TK 50/50-Modell"),
    ("Die restlichen 50 % innerhalb eines Jahres – ohne Zinsen", "TK Restzahlung zinsfrei"),
    ("Entweder als monatliche Raten oder als Einmalzahlung", "TK Raten/Einmalzahlung"),
    ("Keine zusätzlichen Gebühren oder versteckten Kosten", "TK keine Gebühren"),
    ("Sie können Ihren Treppenlift auf verschiedene Weise finanzieren. Zum Beispiel bietet TK Home Solutions ein Modell, bei dem Sie 50 % des Kaufpreises bei Montage und die restlichen 50 % zinsfrei innerhalb eines Jahres zahlen – wahlweise in Raten oder als Einmalzahlung.", "TK Modell-Satz"),
    ("Achten Sie auf Zinsen, Bearbeitungsgebühren und mögliche Zusatzkosten (z. B. Restschuldversicherung)", "TK Bank-Hinweis"),
    ("Ein guter Indikator für ein günstiges Darlehen ist der effektive Jahreszins (je niedriger, desto besser)", "TK eff. Jahreszins"),
    ("Falls Sie finanziellen Spielraum haben, ist ein Direktkauf oft die günstigere Option. Falls Sie jedoch Flexibilität bevorzugen, kann eine zinsenfreie Finanzierung eine ideale Lösung sein.", "TK Empfehlung"),
    ("Effektiver Zinssatz ab 2,35 % p.a.", "TK KfW-Zins-Echo (historisch)"),
    ("können Sie einen Zuschuss von bis zu 4.180 € erhalten", "TK Zuschuss-Angabe"),
]:
    quote(q, s, l)

# --- HIRO LIFT (Herstellerangabe) ---
q = "hiro-finanzierung.txt"
for s, l in [
    ("Treppenlift-Finanzierung: Ratenzahlung mit easyCredit", "HIRO Titel"),
    ("Über unseren Finanzierungspartner easyCredit können Sie Ihren Treppenlift bequem in monatlichen Raten bezahlen.", "HIRO easyCredit"),
    ("Die Ratenzahlung wickelt die TeamBank AG ab, der Anbieter von easyCredit.", "HIRO TeamBank"),
    ("Ihren HIRO Treppenlift zahlen Sie über eine Laufzeit von 2 bis 60 Monaten ab.", "HIRO Laufzeit 2–60"),
    ("Im selben Termin besprechen Sie eine mögliche Ratenzahlung und Zuschüsse.", "HIRO Termin-Logik"),
    ("nimmt die Pflegekasse bis zu 4.180 € pro Hausbewohner, den verbleibenden Betrag können Sie in Raten zahlen", "HIRO Restbetrag-Raten"),
]:
    quote(q, s, l)

# --- Lifta (Herstellerangabe) ---
q = "lifta-finanzierung.txt"
for s, l in [
    ("individuelle Finanzierungsangebote zu günstigen Raten, die zu Ihren finanziellen Möglichkeiten passen", "Lifta individuell"),
    ("Unsere Finanzierungsexperten erstellen für Sie eine individuelle Finanzierungsvereinbarung.", "Lifta Vereinbarung"),
    ("Anzahlung und monatliche Raten kalkulieren wir passend zu Ihrer finanziellen Situation.", "Lifta Anzahlung+Raten"),
    ("können maximal vier pflegebedürftige Bewohner ihre", "Lifta WG-Kontext"),
]:
    quote(q, s, l)

# Absenz: gerenderter Lifta-Text ohne zinsfrei/0-%-Angabe
lifta = (D / "lifta-finanzierung.txt").read_text(encoding="utf-8")
for pat in ["0 %", "0%", "zinsfrei", "zinslos", "ohne Zinsen"]:
    check(f"lifta ABSENZ '{pat}'", pat not in lifta)

# --- Nord-Ostsee Liftteam (Händlerangabe) ---
q = "liftteam-ratenkauf.txt"
for s, l in [
    ("Sie möchten Ihren Treppenlift lieber in 12 bis 60 monatlichen Raten zahlen?", "Liftteam 12–60"),
    ("Für einen Gesamtbetrag bis max. 10.000€", "Liftteam 10k-Grenze"),
    ("Für einen Restbetrag bis max. 10.000€ nach Abzug des Zuschusses der Pflegekasse", "Liftteam Restbetrag-nach-Zuschuss"),
    ("Für einen beliebigen Teilbetrag bis max. 10.000€", "Liftteam Teilbetrag"),
]:
    quote(q, s, l)

# --- Der Treppenlift (Angebotsvermittlung) ---
q = "der-tl-ratenzahlung.txt"
for s, l in [
    ("Zinslose Ratenzahlung 0 % Effektivzins 12 bis 60 Monate Laufzeit ab 100 € Monatsrate", "der-tl Konditionenkasten"),
    ("Sie zahlen lediglich eine Anzahlung von mind. 50 % des Preises für einen Treppenlift und verteilen den Restbetrag auf 11 Teilzahlungen.", "der-tl 11 Teilzahlungen (Intra-Widerspruch)"),
    ("Dieses beinhaltet die zinslose Ratenzahlung direkt über Der Treppenlift.", "der-tl zinslos direkt"),
]:
    quote(q, s, l)

# --- gebrauchttreppenlifte (Händlerangabe) ---
# Ledger-Note: das SERP-Snippet zeigte eine veraltete "4000,- Euro"-Zeile; die LIVE-Seite
# nennt 4.180 Euro — Zitate nur aus dem Live-Text (Snippet-Stale-Falle dokumentiert).
q = "gebrauchtl-finanzieren.txt"
for s, l in [
    ("individuelle Laufzeiten und Sondertilgungen ohne Zinsen", "gebrauchtl zinslos+Sondertilgung"),
    ("bis zu 4.180 Euro von Ihrer Pflegekasse erhalten", "gebrauchtl 4.180 (konsistent)"),
]:
    quote(q, s, l)

# --- Verbraucherzentrale: Kreditverträge-Rechte ---
q = "vz-kreditrechte.txt"
for s, l in [
    ("Sie können einen Verbraucherkreditvertrag grundsätzlich innerhalb von 14 Tagen widerrufen.", "VZ 14 Tage"),
    ("gibt es ein gesetzliches Widerrufsrecht, wenn die vereinbarte Kreditsumme mindestens 200 Euro beträgt", "VZ 0%-Widerruf ≥200 €"),
    ("Damit ist auch sichergestellt, dass bei vorzeitiger Ablösung einer Null-Prozent-Finanzierung keine Vorfälligkeitsentschädigung berechnet werden darf.", "VZ keine Vorfälligkeit bei 0%"),
    ("In diesem Fall reduzieren sich die Gesamtkosten des Kredits um die Zinsen und weiteren Kreditkosten entsprechend der verbleibenden Laufzeit des Vertrags.", "VZ Gesamtkosten-Reduktion"),
]:
    quote(q, s, l)

# --- vzhh ---
q = "vzhh-nullprozent.txt"
for s, l in [
    ("Null-Prozent-Finanzierungen können binnen 14 Tagen ab Vertragsschluss widerrufen werden.", "vzhh 14 Tage ab Abschluss"),
    ("Wurde beim Abschluss der Null-Prozent-Finanzierung die Widerrufsbelehrung vergessen oder war sie falsch, haben Sie gemäß § 356d BGB sogar ein Jahr und 14 Tage lang Zeit, um Ihren Kreditvertrag zu widerrufen.", "vzhh § 356d 1J+14T"),
]:
    quote(q, s, l)

# --- vzbv (Urteilsbericht) ---
q = "vzbv-nullprozent.txt"
for s, l in [
    ("Bei der Vereinbarung einer Null-Prozent-Finanzierung", "vzbv Kontext"),
    ("um einen unentgeltlichen Darlehensvertrag mit eingeschränktem Widerrufsrecht", "vzbv Kernbefund"),
]:
    quote(q, s, l)

# --- evz.de (Verbraucherzentrale-Netz, aktualisiert 30.10.2026) ---
q = "evz-kreditrichtlinie.txt"
for s, l in [
    ("Ab dem 20. November 2026 gelten in Deutschland neue Regeln für Verbraucherkredite.", "evz Stichtag"),
    ("Dazu gehören bestimmte zinsfreie Darlehen, kurzfristige Kredite mit einer Laufzeit von weniger als drei Monaten und Darlehen mit einem Nettokreditbetrag von weniger als 200 Euro.", "evz erfasste Formen"),
    ("Kreditwürdigkeit prüfen: Vor der Kreditvergabe müssen Kreditgeber genauer prüfen, ob Verbraucher den Kredit voraussichtlich zurückzahlen können.", "evz Bonitätsprüfung"),
    ("Persönliche Daten schützen: Bei der Kreditwürdigkeitsprüfung dürfen bestimmte Daten nicht verwendet werden.", "evz Datenschutz"),
    ("Die neuen Vorschriften gelten in Deutschland ab dem 20. November 2026", "evz Vorschriften-Satz"),
    ("Aktualisiert am 30 Oktober 2026", "evz Stand"),
]:
    quote(q, s, l)

# --- Bundestag (Textarchiv) ---
q = "bundestag-kredite.txt"
for s, l in [
    ("Dem Entwurf zufolge sollen Kleinkredite bis 200 Euro, zins- und gebührenfreie Kredite, Kredite mit einer Laufzeit bis zu drei Monaten sowie sogenannte", "Bundestag Entwurf Teil 1"),
    ("-Modelle in die verbraucherschützenden Regelungen für Kreditverträge einbezogen werden.", "Bundestag Entwurf Teil 2"),
]:
    quote(q, s, l)

# --- Bundesgesetzblatt (Titel-/Verkündungsseite) ---
quote("bgbl-139.txt", "Gesetz zur Umsetzung der Richtlinie (EU) 2023/2225 über Verbraucherkreditverträge und zur Regelung der Förderung klimaneutraler Mobilität", "BGBl Titel")

# --- BGB- und SGB-XI-Einzelnormen (gesetze-im-internet) ---
quote("bgb-491.txt", "Allgemein-Verbraucherdarlehensverträge sind entgeltliche Darlehensverträge zwischen einem Unternehmer als Darlehensgeber und einem Verbraucher als Darlehensnehmer.", "§ 491 Abs. 2")
quote("bgb-491.txt", "weniger als 200 Euro beträgt", "§ 491 Abs. 2 Nr. 1")
quote("bgb-491.txt", "binnen drei Monaten zurückzuzahlen hat und nur geringe Kosten vereinbart sind", "§ 491 Abs. 2 Nr. 3")
quote("bgb-492.txt", "Verbraucherdarlehensverträge sind, soweit nicht eine strengere Form vorgeschrieben ist, schriftlich abzuschließen.", "§ 492 Abs. 1")
quote("bgb-492.txt", "Nach Vertragsschluss stellt der Darlehensgeber dem Darlehensnehmer eine Abschrift des Vertrags zur Verfügung.", "§ 492 Abs. 3")
quote("bgb-492.txt", "kann der Darlehensnehmer vom Darlehensgeber jederzeit einen Tilgungsplan", "§ 492 Abs. 3 Tilgungsplan")
quote("bgb-495.txt", "Dem Darlehensnehmer steht bei einem Verbraucherdarlehensvertrag ein Widerrufsrecht nach § 355 zu.", "§ 495 Abs. 1")
quote("bgb-500.txt", "Der Darlehensnehmer kann seine Verbindlichkeiten aus einem Verbraucherdarlehensvertrag jederzeit ganz oder teilweise vorzeitig erfüllen.", "§ 500 Abs. 2")
quote("bgb-502.txt", "wenn der Darlehensnehmer zum Zeitpunkt der Rückzahlung Zinsen zu einem gebundenen Sollzinssatz schuldet", "§ 502 Abs. 1")
quote("bgb-502.txt", "1 Prozent des vorzeitig zurückgezahlten Betrags oder, wenn der Zeitraum zwischen der vorzeitigen und der vereinbarten Rückzahlung ein Jahr nicht überschreitet, 0,5 Prozent des vorzeitig zurückgezahlten Betrags", "§ 502 Abs. 3 Grenzen")
quote("bgb-312g.txt", "Dem Verbraucher steht bei außerhalb von Geschäftsräumen geschlossenen Verträgen und bei Fernabsatzverträgen ein Widerrufsrecht gemäß § 355 zu.", "§ 312g Abs. 1")
quote("bgb-312g.txt", "Verträge zur Lieferung von Waren, die nicht vorgefertigt sind und für deren Herstellung eine individuelle Auswahl oder Bestimmung durch den Verbraucher maßgeblich ist oder die eindeutig auf die persönlichen Bedürfnisse des Verbrauchers zugeschnitten sind", "§ 312g Abs. 2 Nr. 1")
quote("bgb-356b.txt", "Die Widerrufsfrist beginnt auch nicht, bevor der Darlehensgeber dem Darlehensnehmer eine für diesen bestimmte Vertragsurkunde", "§ 356b Abs. 1")
quote("bgb-356b.txt", "beginnt die Frist erst mit Nachholung dieser Angaben gemäß § 492 Absatz 6", "§ 356b Abs. 2 Nachholung")
quote("bgb-356b.txt", "In den Fällen der Sätze 1 und 2 beträgt die Widerrufsfrist einen Monat.", "§ 356b Abs. 2 Frist 1 Monat")
quote("bgb-40.txt", "Die Zuschüsse dürfen einen Betrag in Höhe von 4 180 Euro je Maßnahme nicht übersteigen.", "SGB XI § 40 Abs. 4")

# --- Arithmetik (Rechenbeispiel im Artikel: fiktiv 8.000 €) ---
check("Arithmetik 8000-4180=3820", 8000 - 4180 == 3820)
check("Arithmetik 3820/24=159,17", round((8000 - 4180) / 24, 2) == 159.17)
check("Arithmetik 8000/48=166,67", round(8000 / 48, 2) == 166.67)

fails = [r for r in results if not r[1]]
print(f"\n{len(results) - len(fails)}/{len(results)} LEDGER-PÄSSE, {len(fails)} FAILS")
sys.exit(1 if fails else 0)
