#!/usr/bin/env python3
"""Fix #7 (SEO-Audit seo-audit-zbk, X3/X4): Titel auf Keyword-Kopf kürzen (Live-<title> ≤65
inkl. Suffix „ — ZuhauseBleiben Kompass" ⇒ JSON-Titel ≤40) und Meta-Descriptions benefit-first
auf ≤155. Re-derivation gegen die LIVE-Site 30.10.2026 (nicht der Audit-Snapshot 19.10.).
H1, Inhalte und Quellen bleiben unangetastet — reine Copy-Edits auf title/description."""
import json, sys
from pathlib import Path

TITLE_MAX = 40   # + 25 Zeichen Suffix = ≤65 im <title>
DESC_MAX = 155

# slug -> neue Felder (nur geänderte Felder)
EDITS = {
    "bad-umbau-barrierefrei": {"title": "Bad barrierefrei umbauen: Planung"},
    "badumbau-angebote-vergleichen": {
        "title": "Badumbau-Angebote richtig vergleichen",
        "description": "Badumbau-Angebote vergleichbar machen: Umfang, Abdichtung, Zusatzarbeiten und Zahlungsregeln gleich benennen — mit Positionstabelle und DIN-18534-Fragen."},
    "bodengleiche-dusche-altbau": {
        "title": "Bodengleiche Dusche im Altbau möglich?",
        "description": "Ob die bodengleiche Dusche im Altbau möglich ist, entscheidet die Prüfung vor Ort: Aufbauhöhe, Fallrohr, Decke. Mit Prüffahrplan und Fragenliste."},
    "hausnotruf-kosten-anbieter-vergleich": {"title": "Hausnotruf: Kosten, Anbieter & Vertrag"},
    "hausnotruf-sturzerkennung-oder-knopf": {"title": "Hausnotruf: Sturzerkennung oder Knopf?"},
    "hilfsmittel-dusch-wc-uebernahme": {
        "title": "Dusch-WC: Was Krankenkassen übernehmen",
        "description": "Dusch-WC: Toilettenaufsätze mit Wascheinrichtung sind als Hilfsmittel gelistet (PG 33.40.05) — mit enger Indikation. Kriterien für Antrag und Selbstkauf."},
    "hilfsmittel-pflegekasse-uebernahme": {"title": "Hilfsmittel: Was die Pflegekasse zahlt"},
    "pflegegrad-antrag-ablauf-fristen": {"title": "Pflegegrad beantragen: Ablauf & Fristen"},
    "rollator-auswahl-passform-kosten": {"title": "Rollator auswählen: Typen & Passform"},
    "treppenlift-angebote-vergleichen": {
        "title": "Treppenlift-Angebote vergleichen",
        "description": "Welche Positionen ein Treppenlift-Angebot enthalten muss und wie Sie zwei Angebote wirklich vergleichbar machen — mit Beispielaufstellung und Fallen."},
    "treppenlift-aussentreppen-aussenlift": {
        "title": "Treppenlift für die Außentreppe",
        "description": "Was einen Außenlift wetterfest macht, was Hersteller und Fachportale zum Preis sagen und welche Zusatzposten draußen dazukommen — mit Angebots-Checkliste."},
    "treppenlift-firmen-vergleich": {"title": "Treppenlift-Firmen im Vergleich"},
    "treppenlift-gebraucht-oder-neu": {"title": "Treppenlift gebraucht oder neu?"},
    "treppenlift-kosten": {"title": "Treppenlift-Kosten: Angebot & Beispiele"},
    "treppenlift-maximalgewicht": {
        "title": "Treppenlift Maximalgewicht / Tragkraft",
        "description": "Die zulässige Tragkraft hängt an Modell und Ausführung, nicht an einer Pauschalzahl. Belegte Herstellerwerte und was das Aufmaß klärt."},
    "treppenlift-mieten": {"title": "Treppenlift mieten: Kosten & Vertrag"},
    "treppenlift-mietwohnung": {
        "title": "Treppenlift in der Mietwohnung",
        "description": "Wer beim Treppenlift-Einbau in der Mietwohnung zustimmen muss (§ 554 BGB, § 20 WEG) und wie Rückbau, Sicherheitsleistung und Pflegekasse geregelt sind."},
    "treppenlift-plattformlift-rollstuhllift": {
        "title": "Plattformlift (Rollstuhllift): Kosten",
        "description": "Was ein Plattformlift kostet (Portale 6.000–30.000 €, Hersteller ab 11.000 €), welche Bauart passt und welche Maße das Aufmaß klären."},
    "treppenlift-schmale-treppe": {"title": "Treppenlift für schmale Treppen"},
    "treppenlift-steuerlich-absetzen": {
        "title": "Treppenlift steuerlich absetzen",
        "description": "Handwerkerleistungen: 20 Prozent der Arbeitskosten, max. 1.200 Euro. Welche Route für Treppenlift und Badumbau gilt — mit Nachweis-Checkliste."},
    "treppenlift-zuschuss": {
        "title": "Treppenlift-Zuschuss: Pflegekasse & KfW",
        "description": "Bis zu 4.180 Euro je Maßnahme sind keine automatische Zusage. Voraussetzungen, KfW-Status und Unterlagen prüfen — mit Förder-Entscheidungshilfe."},
    "tuerbreiten-schwellen-schnellcheck": {"title": "Türbreiten & Schwellen: Schnell-Check"},
    "verhinderungspflege-tagespflege-ueberblick": {"title": "Verhinderungspflege & Tagespflege"},
    "wanne-zur-dusche": {"title": "Wanne zur Dusche umbauen: Varianten"},
}

SUFFIX = " — ZuhauseBleiben Kompass"
fails = []
changed = 0
import re
for path in sorted(Path("content-ready").glob("*.json")):
    slug = path.stem
    data = json.loads(path.read_text(encoding="utf-8"))
    edit = EDITS.get(slug)
    if not edit:
        continue
    old_t, old_d = data.get("title", ""), data.get("description", "")
    for field, max_len in (("title", TITLE_MAX), ("description", DESC_MAX)):
        if field in edit:
            new = edit[field]
            if len(new) > max_len:
                fails.append(f"{slug}.{field} = {len(new)} > {max_len}: {new}")
                continue
            data[field] = new
    # Live-Tag-Vorhersage nach dem Suffix
    live_t = data["title"] + SUFFIX
    if len(live_t) > 65:
        fails.append(f"{slug}: live title {len(live_t)} > 65: {live_t}")
    if len(data["description"]) > DESC_MAX:
        fails.append(f"{slug}: desc {len(data['description'])} > {DESC_MAX}")
    # Chirurgisch: nur die Top-Level-Zeilen ersetzen (2-Space-Einzug), kein JSON-Roundtrip —
    # der schreibte kompakte Arrays der neueren Artikel in ausdifferenzierte Einzeltrommeln um.
    raw = path.read_text(encoding="utf-8")
    if field_edit := edit.get("title"):
        raw, n = re.subn(r'^  "title": ".*",$', '  "title": ' + json.dumps(field_edit, ensure_ascii=False) + ",", raw, count=1, flags=re.M)
        if n != 1: fails.append(f"{slug}: title-Zeile nicht eindeutig ersetzt (n={n})")
    if desc_edit := edit.get("description"):
        raw, n = re.subn(r'^  "description": ".*",$', '  "description": ' + json.dumps(desc_edit, ensure_ascii=False) + ",", raw, count=1, flags=re.M)
        if n != 1: fails.append(f"{slug}: description-Zeile nicht eindeutig ersetzt (n={n})")
    path.write_text(raw, encoding="utf-8")
    print(f"{slug}\n  title {len(old_t)}->{len(data['title'])}: {data['title']!r} (live {len(live_t)})")
    if data["description"] != old_d:
        print(f"  desc {len(old_d)}->{len(data['description'])}")
    changed += 1

# Duplikat-/Kollisionsprüfung der neuen Titel
titles = {}
for path in sorted(Path("content-ready").glob("*.json")):
    data = json.loads(path.read_text(encoding="utf-8"))
    titles.setdefault(data["title"], []).append(data["slug"])
for t, slugs in titles.items():
    if len(slugs) > 1:
        fails.append(f"Doppelter Titel {t!r}: {slugs}")

if fails:
    print("\nFAIL:", *fails, sep="\n  ")
    sys.exit(1)
print(f"\nOK: {changed} JSONs aktualisiert; alle Live-Titel ≤65, Descriptions ≤{DESC_MAX}, keine Duplikate.")
