#!/usr/bin/env python3
"""llms.txt generator for zuhausebleiben-kompass.de.

Usage:
    python3 research/llms-txt.py                     # writes dist/llms.txt
    python3 research/llms-txt.py --check             # exit 1 if dist/llms.txt stale
    python3 research/llms-txt.py --out /tmp/l.txt    # custom output path

Output follows the llmstxt.org spec: H1 title, blockquote summary, sections as
H2 with markdown links "title: 1-sentence summary". Plain static file, no SPOF
(the site works unchanged when the file is absent), honest content only — every
line derives from content-ready/*.json or a title verified against the built
dist HTML. Nothing invented.

Integration: wired into the build — generate.mjs calls write_llms_txt(dist_dir) after its
page writes; the file is regenerated on every `npm run build` / `build:launch`. Idempotent.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BASE = "https://zuhausebleiben-kompass.de"

# slug -> one-sentence summary (German, Sie-form, factual, no superlatives).
# Kept here (not scraped from articles) so the file only states what we verified.
SUMMARIES = {
    "treppenlift-kosten": "Welche Kosten in ein Treppenlift-Angebot gehören, mit Modellrechnung, Folgekosten und Fragenliste für den Fachbetrieb-Termin.",
    "treppenlift-angebote-vergleichen": "Treppenlift-Angebote Position für Position vergleichbar machen: Pflichtangaben-Checkliste, Beispielrechnung mit erfundenen Werten, typische Kostenfallen und Widerrufsrecht vor der Unterschrift.",
    "treppenlift-firmen-vergleich": "Treppenlift-Anbieter anhand von Modellwahl, Service und konkreten Vertragsfragen sachlich vergleichen, ohne Testsieger-Empfehlung.",
    "treppenlift-gebraucht-oder-neu": "Wann ein gebrauchter Treppenlift infrage kommt: Passform, Aufbereitung, Ersatzteile und Vertragsumfang prüfen.",
    "treppenlift-mieten": "Einmal- und Monatskosten, Mindestmietdauer und Pflegekassen-Zuschuss beim Treppenlift-Mieten mit Beispielrechnung.",
    "treppenlift-mietwohnung": "Wer beim Treppenlift-Einbau in der Mietwohnung zustimmen muss (§ 554 BGB, § 20 WEG) und wie Rückbau und Kosten geregelt werden.",
    "treppenlift-zuschuss": "Voraussetzungen und Unterlagen für Pflegekassen-Zuschuss und KfW-Programme inklusive aktuellem KfW-455-B-Antragstatus prüfen.",
    "treppenlift-steuerlich-absetzen": "Treppenlift und Badumbau steuerlich geltend machen: Handwerkerleistung (20 % der Arbeitskosten, max. 1.200 €) oder außergewöhnliche Belastung, Nachweise und Förderfalle § 35a Abs. 3.",
    "treppenlift-schmale-treppe": "Treppenlift auf schmaler Treppe: Gerätemindestbreiten ab 61 cm und Gebäudemaße 70–100 cm unterscheiden, richtig messen, Alternativen prüfen und das Aufmaß vorbereiten.",
    "treppenlift-maximalgewicht": "Tragkraft verstehen: die Grenze gilt für Person plus Zuladung, belegte Herstellerwerte von 125 bis 200 kg, Ausführung statt Modellpauschale fragen und das Angebot prüfen.",
    "treppenlift-aussentreppen-aussenlift": "Treppenlift für die Außentreppe: was einen Außenlift wetterfest macht, Preisspannen von Herstellern und Fachportalen mit dokumentierter Streuung, Winter-Praxis und Angebots-Checkliste.",
    "treppenlift-plattformlift-rollstuhllift": "Plattformlift für Rollstuhlfahrer: vier Bauarten getrennt (Hublift, gerade/kurvig, Homelift), Portal-Spannen und Herstellerpreise nebeneinander, Maße und Tragkraft mit dokumentierten Widersprüchen, Angebots-Checkliste.",
    "bad-umbau-barrierefrei": "Badumbau nach tatsächlichem Bedarf planen: Entscheidungsmatrix, Angebotscheckliste und geprüfte Förderorientierung.",
    "badumbau-angebote-vergleichen": "Badumbau-Angebote anhand von Umfang, Abdichtung, Zusatzarbeiten und Zahlungsregeln Position für Position vergleichen.",
    "bodengleiche-dusche-altbau": "Prüfpunkte, ob die bodengleiche Dusche im Altbau machbar ist: Aufbauhöhe, Fallrohrweg, Decke und Konstruktion.",
    "wanne-zur-dusche": "Varianten des Wannentauschs vergleichen, offene Baufragen klären und Angebote prüfen, inklusive Förderorientierung.",
    "pflegegrad-antrag-ablauf-fristen": "Pflegegrad beantragen: formloser Antrag, Begutachtung, Bescheidfrist 25 Arbeitstage, Widerspruch und Klage in Fristen.",
    "hilfsmittel-pflegekasse-uebernahme": "Pflegehilfsmittel über die Pflegekasse nach §§ 33/40 SGB XI: Hilfsmittelverzeichnis, Eigenanteil 10 % max. 25 €, 42-€-Pauschale.",
    "hilfsmittel-dusch-wc-uebernahme": "Dusch-WC über die Kasse: gelistete Toilettenaufsätze mit Wascheinrichtung (Produktgruppe 33.40.05) mit enger Arm- und Hand-Indikation über die Krankenkasse, komplette Anlagen als Wohnumfeld-Einzelfall der Pflegekasse, plus Antrags-Checkliste.",
    "rollator-auswahl-passform-kosten": "Rollator-Typen für drinnen und draußen, Griffhöhe messen, Bremsen verstehen und Kostenübernahme der Kassen prüfen.",
    "hausnotruf-kosten-anbieter-vergleich": "Hausnotruf-Kosten und Basistarif-Inhalte verstehen und mit Pflegekasse, Vertrag und Kündigung abgleichen.",
    "hausnotruf-sturzerkennung-oder-knopf": "Wie automatische Sturzerkennung funktioniert, welche Grenzen und Fehlalarme bleiben und für wen sich der Aufpreis lohnt.",
    "tuerbreiten-schwellen-schnellcheck": "Türbreite und Schwellenhöhe selbst messen und mit Rampe oder Umbau planen, inklusive Messprotokoll und Checkliste.",
    "beleuchtung-orientierung-im-alter": "Lichtplanung im Alter: Grundhelligkeit, Blendung vermeiden, Nachtlicht und Bewegungsmelder gezielt einsetzen.",
    "verhinderungspflege-tagespflege-ueberblick": "Verhinderungspflege (§ 39 SGB XI) und Tagespflege (§ 41): Ansprüche, Budgets und Entscheidungsmatrix.",
}

# Legacy-data entry page (not in content-ready/, built from data/content.json).
# Title is verified against the built dist HTML at generation time.
LEGACY_PAGES = {
    "pflegegrad-beantragen": {
        "title": "Pflegegrad: Wo Sie Unterstützung finden",
        "summary": "Anlaufstellen und erste Schritte bei Fragen zum Pflegegrad — die Pflegekasse ist die erste Kontaktstelle; dieses Portal bietet selbst keine Versicherungsberatung.",
    },
}

SECTION_MAP = [
    ("Treppenlift", ["treppenlift-kosten", "treppenlift-angebote-vergleichen", "treppenlift-firmen-vergleich", "treppenlift-gebraucht-oder-neu",
                     "treppenlift-mieten", "treppenlift-mietwohnung", "treppenlift-zuschuss", "treppenlift-steuerlich-absetzen",
                     "treppenlift-schmale-treppe", "treppenlift-maximalgewicht", "treppenlift-aussentreppen-aussenlift", "treppenlift-plattformlift-rollstuhllift"]),
    ("Bad barrierefrei umbauen", ["bad-umbau-barrierefrei", "badumbau-angebote-vergleichen",
                                  "bodengleiche-dusche-altbau", "wanne-zur-dusche"]),
    ("Pflegegrad, Hilfsmittel und Sicherheit", ["pflegegrad-antrag-ablauf-fristen", "pflegegrad-beantragen",
                                                "hilfsmittel-pflegekasse-uebernahme", "hilfsmittel-dusch-wc-uebernahme",
                                                "rollator-auswahl-passform-kosten",
                                                "hausnotruf-kosten-anbieter-vergleich", "hausnotruf-sturzerkennung-oder-knopf"]),
    ("Wohnen im Alltag", ["tuerbreiten-schwellen-schnellcheck", "beleuchtung-orientierung-im-alter",
                          "verhinderungspflege-tagespflege-ueberblick"]),
]


def clean(text: str) -> str:
    text = unicodedata.normalize("NFC", text or "")
    return re.sub(r"\s+", " ", text).strip()


def load_articles(content_ready: Path) -> list:
    arts = []
    for f in sorted(content_ready.glob("*.json")):
        j = json.loads(f.read_text(encoding="utf-8"))
        slug = j["slug"]
        if slug not in SUMMARIES:
            raise SystemExit(
                f"ERROR: no hand-written summary for slug '{slug}' — add it to SUMMARIES "
                "(honest-content policy: no auto-generated sentences)")
        arts.append({
            "slug": slug,
            "title": clean(j.get("title") or slug),
            "summary": SUMMARIES[slug],
            "status": j.get("status"),
        })
    return arts


def load_legacy(dist_dir: Path) -> dict:
    """Verify the legacy entry page against the built HTML before listing it."""
    page = LEGACY_PAGES["pflegegrad-beantragen"]
    html_path = dist_dir / "pflegegrad-beantragen.html"
    if not html_path.exists():
        raise SystemExit("ERROR: dist/pflegegrad-beantragen.html missing — remove it from LEGACY_PAGES")
    m = re.search(r"<title>(.*?)</title>", html_path.read_text(encoding="utf-8", errors="ignore"))
    live = clean(m.group(1)) if m else ""
    live = re.sub(r"\s*[—–-]\s*ZuhauseBleiben Kompass\s*$", "", live)
    if live != page["title"]:
        raise SystemExit(f"ERROR: title of pflegegrad-beantragen changed on page ('{live}') — update LEGACY_PAGES")
    return {"slug": "pflegegrad-beantragen", **page}


def build_llms_txt(dist_dir: Path) -> str:
    arts = load_articles(REPO / "content-ready")
    indexed = {a["slug"]: a for a in arts if a["status"] != "draft"}
    indexed["pflegegrad-beantragen"] = load_legacy(dist_dir)

    lines = [
        "# Zuhausebleiben-Kompass.de",
        "",
        "> Ratgeber für ältere Menschen und ihre Angehörigen zu Treppenlift, barrierefreiem Badumbau, "
        "Pflegegrad, Hilfsmittel und sicherem Wohnen zu Hause. Alle Artikel mit Quellenangaben "
        "(Gesetze, KfW, Verbraucherzentrale), Sie-Ansprache, ohne Produkttests und ohne individuelle Beratung.",
        "",
        f"Der Überblick steht auch als [Sitemap]({BASE}/sitemap.xml) und [RSS-Feed]({BASE}/rss.xml) bereit.",
        "",
    ]
    covered = set()
    for h2, slugs in SECTION_MAP:
        lines += [f"## {h2}", ""]
        for slug in slugs:
            a = indexed.get(slug)
            if not a:
                print(f"WARN: slug '{slug}' not found/indexed, skipped", file=sys.stderr)
                continue
            covered.add(slug)
            lines.append(f"- [{a['title']}]({BASE}/{slug}.html): {a['summary']}")
        lines.append("")
    missing = sorted(set(indexed) - covered)
    if missing:
        raise SystemExit(f"ERROR: articles missing from llms.txt sections: {missing}")
    lines += [
        "## Hinweise",
        "",
        "- Alle Inhalte sind allgemeine Orientierung, keine individuelle technische, medizinische oder Rechtsberatung.",
        "- Zahlen zu Leistungen und Förderung sind mit Abrufdatum belegt (siehe jeweiliger Artikel, Abschnitt Quellen).",
        "- Kontakt: anfragen@zuhausebleiben-kompass.de · Rechtliches: [Impressum](https://zuhausebleiben-kompass.de/impressum.html)",
    ]
    return "\n".join(lines).rstrip() + "\n"


def write_llms_txt(dist_dir: Path, name: str = "llms.txt") -> Path:
    out = dist_dir / name
    out.write_text(build_llms_txt(dist_dir), encoding="utf-8")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate dist/llms.txt from content-ready data")
    ap.add_argument("--out", default=None, help="output file (default: dist/llms.txt)")
    ap.add_argument("--check", action="store_true", help="exit 1 if the file is missing or stale")
    args = ap.parse_args()

    dist = REPO / "dist"
    if args.check:
        target = Path(args.out) if args.out else dist / "llms.txt"
        if not target.exists():
            print(f"STALE: {target} missing", file=sys.stderr)
            return 1
        tmp = target.parent / (target.name + ".check.tmp")
        tmp.write_text(build_llms_txt(dist), encoding="utf-8")
        try:
            if tmp.read_text(encoding="utf-8") != target.read_text(encoding="utf-8"):
                print("STALE: file differs from freshly generated content (re-run the generator)", file=sys.stderr)
                return 1
        finally:
            tmp.unlink()
        print(f"OK: {target} matches current content-ready data")
        return 0

    target = Path(args.out) if args.out else dist / "llms.txt"
    write_llms_txt(target.parent, target.name)
    print(f"wrote {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
