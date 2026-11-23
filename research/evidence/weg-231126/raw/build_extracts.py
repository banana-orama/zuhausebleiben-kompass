#!/usr/bin/env python3
"""Build legal-extracts.md + ledger-legal.json for weg-231126.

Every quote is extracted from the cleaned source text by literal start/end
anchors (never hand-copied), then verified as a literal substring.
Quote policy: statutes = exact cleaned text; PDF/PM quotes = de-hyphenated,
whitespace-collapsed text (cleaning steps documented per section).
"""
import html
import json
import re
from pathlib import Path

RAW = Path(__file__).resolve().parent
OUT = RAW.parent
FETCHED = "2026-11-23"

# ---------------------------------------------------------------- cleaners
def clean_gii(path):
    raw = Path(path).read_bytes().decode("iso-8859-1")
    raw = re.sub(r"<head[\s\S]*?</head>", " ", raw, flags=re.I)
    raw = re.sub(r"<(script|style)[\s\S]*?</\1>", " ", raw, flags=re.I)
    raw = re.sub(r"<[^>]+>", " ", raw)
    raw = html.unescape(html.unescape(raw))
    for ch in ("\u00a0", "\u202f", "\u2007"):
        raw = raw.replace(ch, " ")
    return re.sub(r"\s+", " ", raw).strip()

def clean_bgh_html(path):
    raw = Path(path).read_bytes()
    try:
        raw = raw.decode("utf-8")
    except UnicodeDecodeError:
        raw = raw.decode("iso-8859-1")
    raw = re.sub(r"<head[\s\S]*?</head>", " ", raw, flags=re.I)
    raw = re.sub(r"<(script|style)[\s\S]*?</\1>", " ", raw, flags=re.I)
    raw = re.sub(r"<[^>]+>", " ", raw)
    raw = html.unescape(html.unescape(raw))
    for ch in ("\u00a0", "\u202f", "\u2007", "\u2009"):
        raw = raw.replace(ch, " ")
    raw = raw.replace("\u00ad", "")  # BGH soft hyphens
    return re.sub(r"\s+", " ", raw).strip()

def flat_pdf(path):
    """pdftotext -layout output -> single-line text with de-hyphenation.
    Rule: '-<NL>' + lowercase continuation -> join without hyphen;
    otherwise keep the hyphen (intentional compound hyphen at line end)."""
    t = Path(path).read_text(encoding="utf-8")
    t = t.replace("\f", "\n")
    lines = []
    for ln in t.split("\n"):
        s = ln.strip()
        if re.fullmatch(r"-\s*\d+\s*-", s):        # page number footer
            continue
        if s.startswith("ECLI:DE:BGH:"):            # ECLI line between pages
            continue
        lines.append(ln)
    t = "\n".join(lines)
    t = re.sub(r"-\n\s*(?=[a-z\u00e4\u00f6\u00fc\u00df])", "", t)  # de-hyphenate
    t = re.sub(r"-\n\s*", "-", t)                                  # keep compound hyphen
    return re.sub(r"\s+", " ", t).strip()

# ---------------------------------------------------------------- prepare texts
texts = {}
texts["weg20"] = clean_gii(RAW / "wegg__20.html")
texts["weg21"] = clean_gii(RAW / "wegg__21.html")
texts["weg44"] = clean_gii(RAW / "wegg__44.html")
texts["wegfull"] = clean_gii(RAW / "wegg-full.html")
texts["vzr33"] = flat_pdf(RAW / "vzr-33-23.txt")
texts["vzr244"] = flat_pdf(RAW / "vzr-244-22.txt")
texts["pm"] = clean_bgh_html(RAW / "pm-026-2024.html")

# persist cleaned working texts for provenance
names = {"weg20": "wegg__20.txt", "weg21": "wegg__21.txt", "weg44": "wegg__44.txt",
         "wegfull": "wegg-full.txt", "vzr33": "vzr-33-23.flat.txt",
         "vzr244": "vzr-244-22.flat.txt", "pm": "pm-026-2024.txt"}
for k, fn in names.items():
    (RAW / fn).write_text(texts[k], encoding="utf-8")

# ---------------------------------------------------------------- sources
SRC = {
    "weg20": dict(url="https://www.gesetze-im-internet.de/woeigg/__20.html",
        title="§ 20 WEG Bauliche Veränderungen (Gesetz über das Wohnungseigentum und das Dauerwohnrecht)",
        raw="raw/wegg__20.html + raw/wegg__20.txt",
        clean="ISO-8859-1 decode; <head>/script/style entfernt; HTML-Tags entfernt; HTML-Entities decodiert (&#228;→ä, &nbsp;→Leerzeichen); geschützte Leerzeichen (U+00A0/U+202F) → Leerzeichen; Whitespace kollabiert."),
    "weg21": dict(url="https://www.gesetze-im-internet.de/woeigg/__21.html",
        title="§ 21 WEG Nutzungen und Kosten bei baulichen Veränderungen",
        raw="raw/wegg__21.html + raw/wegg__21.txt",
        clean="wie § 20 (ISO-8859-1, Entities, Whitespace)"),
    "weg44": dict(url="https://www.gesetze-im-internet.de/woeigg/__44.html",
        title="§ 44 WEG Beschlussklagen",
        raw="raw/wegg__44.html + raw/wegg__44.txt",
        clean="wie § 20 (ISO-8859-1, Entities, Whitespace)"),
    "wegfull": dict(url="https://www.gesetze-im-internet.de/woeigg/BJNR001750951.html",
        title="WEG – Gesamtausgabe (Titel-/Standangaben)",
        raw="raw/wegg-full.html + raw/wegg-full.txt",
        clean="wie § 20 (ISO-8859-1, Entities, Whitespace)"),
    "vzr33": dict(url="https://www.bundesgerichtshof.de/SharedDocs/Entscheidungen/DE/Zivilsenate/V_ZS/2023/V_ZR__33-23.pdf?__blob=publicationFile&v=1",
        title="BGH, Urteil vom 9. Februar 2024 – V ZR 33/23 (LG Köln) – Terrasse/Rampe, Barrierefreiheit",
        raw="raw/vzr-33-23.pdf + raw/vzr-33-23.txt + raw/vzr-33-23.flat.txt",
        clean="PDF (offizielles BGH-Dokument, %PDF-1.5, 16 Seiten) mit pdftotext -layout extrahiert; Seitenzahlen ('- 2 -') und ECLI-Zeilen entfernt; Zeilenumbruch-Trennstriche aufgelöst (unbil‑/lig → unbillig); erhaltene Komposita-Bindestriche (Bund-Länder-Arbeitsgruppe) beibehalten; Whitespace kollabiert."),
    "vzr244": dict(url="https://www.bundesgerichtshof.de/SharedDocs/Entscheidungen/DE/Zivilsenate/V_ZS/2022/V_ZR_244-22.pdf?__blob=publicationFile&v=1",
        title="BGH, Urteil vom 9. Februar 2024 – V ZR 244/22 (LG München I) – Personenaufzug Hinterhaus München",
        raw="raw/vzr-244-22.pdf + raw/vzr-244-22.txt + raw/vzr-244-22.flat.txt",
        clean="PDF (offizielles BGH-Dokument, %PDF-1.5, 27 Seiten) mit pdftotext -layout extrahiert; Seitenzahlen und ECLI-Zeilen entfernt; Trennstriche aufgelöst (wie V ZR 33/23); Whitespace kollabiert."),
    "pm": dict(url="https://www.bundesgerichtshof.de/SharedDocs/Pressemitteilungen/DE/2024/2024026.html",
        title="BGH Pressemitteilung Nr. 026/2024 vom 9. Februar 2024 – Zulässigkeit von baulichen Veränderungen des Gemeinschaftseigentums zur Barrierereduzierung",
        raw="raw/pm-026-2024.html + raw/pm-026-2024.txt",
        clean="UTF-8 HTML; Tags entfernt; Entities decodiert; Soft-Hyphen (U+00AD, 'Kon­takt') entfernt; geschützte Leerzeichen → Leerzeichen; Whitespace kollabiert."),
}

# ---------------------------------------------------------------- quotes
# (quote_id, text_key, Rn./Absatz label, start_anchor, end_anchor or None, context_note)
Q = [
 # ---------- WEG § 20 ----------
 ("weg-20-abs1", "weg20", "§ 20 Abs. 1",
  "§ 20 Bauliche Veränderungen (1) Maßnahmen, die über die ordnungsmäßige Erhaltung des gemeinschaftlichen Eigentums hinausgehen (bauliche Veränderungen), können beschlossen oder einem Wohnungseigentümer durch Beschluss gestattet werden.",
  None,
  "Generalklausel: bauliche Veränderungen sind per Mehrheitsbeschluss möglich oder einem Einzelnen zu gestatten. Basis für Treppenlift-Beschlüsse."),
 ("weg-20-abs2", "weg20", "§ 20 Abs. 2 Satz 1 Nr. 1-5, Satz 2",
  "(2) Jeder Wohnungseigentümer kann angemessene bauliche Veränderungen verlangen, die",
  "Über die Durchführung ist im Rahmen ordnungsmäßiger Verwaltung zu beschließen.",
  "Kernanspruch: Individualanspruch auf angemessene bauliche Veränderungen für 5 privilegierte Zwecke; Nr. 1 'Gebrauch durch Menschen mit Behinderungen' ist die Anspruchsgrundlage für Treppenlift/Barrierefreiheit. Nr. 5 lautet in der aktuellen Fassung 'Stromerzeugung durch Steckersolargeräte' (geändert durch Art. 1 G v. 10.10.2024; WEMoG-Fassung v. 01.12.2020 hatte 'Solargeräte'). Satz 2 = Grundlagen-/Durchführungsbeschluss."),
 ("weg-20-abs3", "weg20", "§ 20 Abs. 3",
  "(3) Unbeschadet des Absatzes 2 kann jeder Wohnungseigentümer verlangen, dass ihm eine bauliche Veränderung gestattet wird, wenn alle Wohnungseigentümer, deren Rechte durch die bauliche Veränderung über das bei einem geordneten Zusammenleben unvermeidliche Maß hinaus beeinträchtigt werden, einverstanden sind.",
  None,
  "Gestattungsanspruch bei Einverständnis aller Betroffenen (ergänzt Abs. 2)."),
 ("weg-20-abs4", "weg20", "§ 20 Abs. 4",
  "(4) Bauliche Veränderungen, die die Wohnanlage grundlegend umgestalten oder einen Wohnungseigentümer ohne sein Einverständnis gegenüber anderen unbillig benachteiligen, dürfen nicht beschlossen und gestattet werden; sie können auch nicht verlangt werden.",
  None,
  "Absolute Grenze (2 Alt.) für Beschluss, Gestattung und Individualanspruch; zentral in BGH V ZR 33/23 und V ZR 244/22."),
 # ---------- WEG § 21 ----------
 ("weg-21-abs1", "weg21", "§ 21 Abs. 1 Satz 1 und 2",
  "(1) Die Kosten einer baulichen Veränderung, die einem Wohnungseigentümer gestattet oder die auf sein Verlangen nach § 20 Absatz 2 durch die Gemeinschaft der Wohnungseigentümer durchgeführt wurde, hat dieser Wohnungseigentümer zu tragen. Nur ihm gebühren die Nutzungen.",
  None,
  "Kostentragung des verlangenden/privilegierten Eigentümers: bei Gestattung oder Durchführung auf § 20-Abs.-2-Verlangen trägt ER die Kosten allein; Nutzungen (z.B. Miet­einnahmen aus einem eingebauten Aufzug) stehen nur ihm zu."),
 ("weg-21-abs2", "weg21", "§ 21 Abs. 2",
  "(2) Vorbehaltlich des Absatzes 1 haben alle Wohnungseigentümer die Kosten einer baulichen Veränderung nach dem Verhältnis ihrer Anteile (§ 16 Absatz 1 Satz 2) zu tragen,",
  "Für die Nutzungen gilt § 16 Absatz 1.",
  "Ausnahme: Kostenumlage auf alle bei 2/3-Mehrheit (+ Mehrheit der MEA) bzw. amortisationsfähigen Maßnahmen; schafft den Rahmen für Gemeinschaftsfinanzierung."),
 ("weg-21-abs5", "weg21", "§ 21 Abs. 5",
  "(5) Die Wohnungseigentümer können eine abweichende Verteilung der Kosten und Nutzungen beschließen. Durch einen solchen Beschluss dürfen einem Wohnungseigentümer, der nach den vorstehenden Absätzen Kosten nicht zu tragen hat, keine Kosten auferlegt werden.",
  None,
  "Abweichende Kostenverteilung durch Beschluss möglich, aber Schutz vor Kostenüberwälzung auf nicht zahlungspflichtige Eigentümer."),
 # ---------- WEG § 44 ----------
 ("weg-44-abs1", "weg44", "§ 44 Abs. 1 Satz 1 und 2",
  "(1) Das Gericht kann auf Klage eines Wohnungseigentümers einen Beschluss für ungültig erklären (Anfechtungsklage) oder seine Nichtigkeit feststellen (Nichtigkeitsklage). Unterbleibt eine notwendige Beschlussfassung, kann das Gericht auf Klage eines Wohnungseigentümers den Beschluss fassen (Beschlussersetzungsklage).",
  None,
  "Rechtsschutz: Anfechtungs-/Nichtigkeitsklage gegen Beschlüsse; Beschlussersetzungsklage, wenn die Versammlung eine Entscheidung unterlässt (z.B. Verweigerung eines § 20-Abs.-2-Grundlagenbeschlusses; so der Fall in V ZR 244/22)."),
 # ---------- WEG Vollzitat/Stand ----------
 ("weg-vollzitat", "wegfull", "Titelangabe",
  "Vollzitat: \"Wohnungseigentumsgesetz in der Fassung der Bekanntmachung vom 12. Januar 2021 (BGBl. I S. 34), das zuletzt durch Artikel 1 des Gesetzes vom 10. Oktober 2024 (BGBl. 2024 I Nr. 306) geändert worden ist\"",
  None,
  "Verifizierte Zitierfähigkeit: aktuelle Gesamtausgabe = WEG in der Fassung der Bek. v. 12.01.2021 (WEMoG-Neufassung, in Kraft seit 01.12.2020), zuletzt geändert Art. 1 G v. 10.10.2024 (BGBl. 2024 I Nr. 306)."),
 ("weg-stand", "wegfull", "Standangabe",
  "Stand: Neugefasst durch Bek. v. 12.1.2021 I 34; zuletzt geändert durch Art. 1 G v. 10.10.2024 I Nr. 306",
  None,
  "Standangabe der Gesamtausgabe; belegt, dass §§ 20/21/44 in der seit 01.12.2020 geltenden WEMoG-Fassung zitiert werden."),
 # ---------- BGH V ZR 33/23 ----------
 ("vzr33-ls-a", "vzr33", "Leitsatz a)",
  "a) Beschließen die Wohnungseigentümer die Durchführung oder Gestattung",
  "Beschlussmangel leidet.",
  "Anfechtungsklage gegen einen § 20-Abs.-2-Stattgebungsbeschluss: nur prüfbar sind § 20 Abs. 4-Grenzen und allgemeine Beschlussmängel; NICHT die Anspruchsvoraussetzungen des § 20 Abs. 2 im Einzelnen."),
 ("vzr33-ls-b", "vzr33", "Leitsatz b)",
  "b) Ob die Anspruchsvoraussetzungen des § 20 Abs. 2 WEG im Einzelnen vorliegen",
  "weiterverfolgt.",
  "Die Anspruchsvoraussetzungen (inkl. Angemessenheit) sind nur relevant bei Negativbeschluss (Anfechtungs-/Beschlussersetzungsklage des Verlangenden)."),
 ("vzr33-ls-c", "vzr33", "Leitsatz c)",
  "c) Eine grundlegende Umgestaltung der Wohnanlage ist bei einer Maßnahme,",
  "Rechnung zu tragen.",
  "Regel-Ausnahme-Verhältnis: privilegierte Maßnahmen (§ 20 Abs. 2 Satz 1) sind typischerweise keine grundlegende Umgestaltung i.S.d. § 20 Abs. 4 Halbs. 1 Alt. 1."),
 ("vzr33-rn15", "vzr33", "Rn. 15 (bb)",
  "bb) In diesem Rahmen ist die Beurteilung des Berufungsgerichts zu beanstanden.",
  "enger zu verstehen als der Begriff der Änderung der Eigenart im bisherigen Recht (vgl. BT-Drucks. 19/18791 S. 66).",
  "Begriffsabgrenzung: 'grundlegende Umgestaltung' (§ 20 Abs. 4) ist enger als 'Änderung der Eigenart' (§ 22 Abs. 2 Satz 1 WEG aF) – wichtig für die Abgrenzung Altrecht/Neurecht im Artikel."),
 ("vzr33-rn18", "vzr33", "Rn. 18",
  "Das angefochtene Urteil kann danach keinen Bestand haben",
  "noch ist er nichtig.",
  "Outcome Terrasse/Barrierefreiheit: BGH hebt Berufungsurteil auf, weist Anfechtungsklage ab; der Gestattungsbeschluss ist weder anfechtbar noch nichtig."),
 ("vzr33-rn19", "vzr33", "Rn. 19",
  "Eine grundlegende Umgestaltung i.S.d. § 20 Abs. 4 Halbs. 1 Alt. 1 WEG ist mit der beschlossenen baulichen Veränderung nicht verbunden.",
  "wobei die Errichtung einer Terrasse schon nach der Teilungserklärung erlaubt ist.",
  "Subsumtion Terrasse/Rampe: Barrierefreiheit (§ 20 Abs. 2 Satz 1 Nr. 1) → nur außergewöhnliche Umstände könnten grundlegende Umgestaltung begründen; 65-cm-Terrasse + Rampe = untergeordneter Anbau, terrassenrechtlich durch Teilungserklärung gedeckt."),
 ("vzr33-rn22", "vzr33", "Rn. 22 (b)",
  "b) Diese Voraussetzungen liegen auf der Grundlage der Feststellungen",
  "bereits in der Teilungserklärung angelegt.",
  "Keine unbillige Benachteiligung (§ 20 Abs. 4 Halbs. 1 Alt. 2): fehlende Vergleichsmöglichkeiten der Obergeschoss-Eigentümer genügen nicht; Ungleichbehandlung durch Sondernutzungsrechte der TE angelegt."),
 # ---------- BGH V ZR 244/22 ----------
 ("vzr244-ls-vorb", "vzr244", "Leitsatz (Vorbemerkung zu § 20 Abs. 1)",
  "Die Wohnungseigentümer können nach dem seit dem 1. Dezember 2020 geltenden Wohnungseigentumsrecht",
  "ZWE 2017, 224 Rn. 30 ff.).",
  "Neurecht seit 01.12.2020: Beschluss (statt Vereinbarung) genügt auch bei Zuweisung ausschließlicher Nutzungsbefugnis am Gemeinschaftseigentum – zentral für Treppenlift/Aufzug am Gemeinschaftseigentum."),
 ("vzr244-ls-a", "vzr244", "Leitsatz a)",
  "a) Eine bauliche Veränderung, die einem der in § 20 Abs. 2 Satz 1 Nr. 1 bis 4 WEG aufgeführten Zwecke dient, ist regelmäßig angemessen.",
  "deren Unangemessenheit.",
  "Angemessenheitsvermutung für privilegierte Maßnahmen; Unangemessenheit nur ausnahmsweise bei außer Verhältnis stehenden Nachteilen."),
 ("vzr244-ls-b", "vzr244", "Leitsatz b)",
  "b) Die Darlegungs- und Beweislast für die tatsächlichen Umstände der Angemessenheit",
  "sich nicht bereits aus dem Begehren selbst ergeben.",
  "Darlegungs-/Beweislast: Verlangender trägt die primäre Last (Zweck), Gemeinschaft sekundäre Darlegungslast für atypische Nachteile."),
 ("vzr244-ls-alt2", "vzr244", "Leitsatz zu § 20 Abs. 4 Halbs. 1 Alt. 2",
  "Eine unbillige Benachteiligung eines Wohnungseigentümers setzt voraus,",
  "Rn. 14).",
  "Definition der unbilligen Benachteiligung (Abwägung Zumutbarkeit; Fortführung V ZR 64/19) – in V ZR 33/23 Rn. 21 ausdrücklich in Bezug genommen."),
 ("vzr244-rn8", "vzr244", "Rn. 8 (a)",
  "Die Beschlussersetzungsklage gemäß § 44 Abs. 1 Satz 2 WEG ist begründet,",
  "NJW 2023, 63 Rn. 8 f.).",
  "Beschlussersetzungsklage (§ 44 Abs. 1 Satz 2): Anspruch auf Grundlagenbeschluss (das 'Ob') genügt; das 'Wie' bleibt der Gemeinschaft vorbehalten."),
 ("vzr244-rn18", "vzr244", "Rn. 18 (a)",
  "Dem Gebrauch durch Menschen mit Behinderungen dienen alle baulichen Veränderungen,",
  "selbst nicht gehbehindert sind, ist unerheblich.",
  "Schlüssel-Leitsatzstelle (Rn. 18): Personenaufzug dient § 20 Abs. 2 Satz 1 Nr. 1, auch wenn der Verlangende selbst nicht auf die Maßnahme angewiesen ist; persönliche Gehbehinderung der Kläger 'unerheblich' (München: nicht gehbehinderte Kläger, Außenaufzug Hinterhaus)."),
 ("vzr244-rn15", "vzr244", "Rn. 15 (1)",
  "Die Zuweisung einer ausschließlichen Nutzungsbefugnis ist nunmehr",
  "ZWE 2019, 429, 445).",
  "Kosten-/Nutzungslogik: § 21 Abs. 1 Satz 1 (Kosten beim Verlangenden) und Satz 2 (Nutzungen nur ihm, § 100 BGB); Reformziel: Beschlussfassung mit ausschließlicher Nutzungsbefugnis möglich."),
 ("vzr244-rn24", "vzr244", "Rn. 24 (3)",
  "Die Kosten der baulichen Veränderung sind dagegen grundsätzlich",
  "die Angemessenheit der Maßnahme nicht entfallen lassen.",
  "Kosten (§ 21 Abs. 1 Satz 1) stehen dem § 20-Abs.-2-Anspruch nicht entgegen; auch Folgekosten (Versicherung, Wartung, Kontrolle) entfallen Angemessenheit grds. nicht."),
 ("vzr244-rn33", "vzr244", "Rn. 33 (Ausklang)",
  "Ist ein unter § 20 Abs. 2 Satz 1 WEG fallendes Verlangen eines Wohnungseigentümers etwa bauordnungsrechtlich unzulässig,",
  "Rn. 201, 361).",
  "Öffentlich-rechtliche Vorgaben: bauordnungsrechtliche Unzulässigkeit → Verlangen widerspricht regelmäßig ordnungsmäßiger Verwaltung; Anspruch kann ohne Angemessenheitsprüfung ausscheiden (Bauordnungsrecht/§ 275-Kontext für Treppenlift-Genehmigungen)."),
 ("vzr244-rn34", "vzr244", "Rn. 34 (2)",
  "Im Rahmen von § 20 Abs. 2 Satz 1 WEG ist die Einhaltung der das",
  "WEG, 15. Aufl., § 20 Rn. 191).",
  "Grundlagenbeschluss vs. Ausführung (§ 20 Abs. 2 Satz 2): öffentlich-rechtliche Einhaltung darf der späteren Durchführungsbeschlussfassung vorbehalten bleiben, jedenfalls bei umfangreichen Maßnahmen wie einem Personenaufzug (Fachplanung)."),
 ("vzr244-rn35", "vzr244", "Rn. 35 (3)",
  "Ein Grundlagenbeschluss darf allerdings dann nicht gefasst oder ersetzt werden,",
  "aber nicht dargelegt.",
  "Absolute Grenze: Grundlagenbeschluss unzulässig, wenn Unmöglichkeit i.S.d. § 275 Abs. 1 BGB von vornherein feststeht (in jedem Fall/bei jeder Ausführung gegen öffentlich-rechtliche Vorschriften); hier von Beklagter nicht dargelegt."),
 # ---------- PM 026/2024 ----------
 ("pm-026-intro", "pm", "PM, Einleitung",
  "Der unter anderem für das Wohnungseigentumsrecht zuständige V. Zivilsenat",
  "verlangt wurden.",
  "PM-Rahmen: zwei Urteile vom 09.02.2024 zur Barrierereduzierung – Personenaufzug (V ZR 244/22) und 65 cm erhöhte Terrasse nebst Zufahrtsrampe (V ZR 33/23)."),
 ("pm-026-mehrheit", "pm", "PM, V ZR 33/23",
  "Infolgedessen dürfen die Wohnungseigentümer eine bauliche Veränderung auch dann durch Mehrheitsbeschluss gestatten,",
  "oder jedenfalls Zweifel hieran hegen.",
  "Kernaussage: Mehrheit darf privilegierte Maßnahme gestatten, obwohl sie die § 20-Abs.-2-Voraussetzungen nicht als gegeben ansieht oder Zweifel hat."),
 ("pm-026-einfmehr", "pm", "PM, V ZR 33/23",
  "Nunmehr können die Wohnungseigentümer nach § 20 Abs. 1 WEG im Gegensatz zu der Regelung in § 22 WEG aF Maßnahmen, die über die ordnungsmäßige Erhaltung des gemeinschaftlichen Eigentums hinausgehen (bauliche Veränderungen), jeweils mit einfacher Stimmenmehrheit beschließen.",
  None,
  "Einfache Stimmenmehrheit nach § 20 Abs. 1 (statt 3/4-Mehrheit nach § 22 Abs. 2 WEG aF) – Kernelement der WEMoG-Reform für den Artikel."),
 ("pm-026-kosten", "pm", "PM, V ZR 244/22",
  "Die Kosten der baulichen Veränderung sind für das Bestehen eines Anspruchs nach § 20 Abs. 2 Satz 1 WEG grundsätzlich ohne Bedeutung,",
  "von dem verlangenden Wohnungseigentümer zu tragen sind.",
  "PM-Fassung der Kostenaussage (§ 21 Abs. 1 Satz 1): hohe Kosten verhindern den Anspruch nicht, weil der Verlangende sie selbst trägt."),
 ("pm-026-umgestaltung", "pm", "PM, beide Verfahrensteile",
  "Nach nunmehr geltendem Recht ist bei einer Maßnahme, die der Verwirklichung eines Zweckes i.S.d. § 20 Abs. 2 Satz 1 WEG dient, eine grundlegende Umgestaltung der Wohnanlage zumindest typischerweise nicht anzunehmen.",
  "Regel-Ausnahme-Verhältnisses Rechnung zu tragen.",
  "PM-Kernaussage: keine grundlegende Umgestaltung bei privilegierten Maßnahmen (in beiden Verfahrensteilen der PM in gleicher Formulierung) + Regel-Ausnahme-Verhältnis."),
 ("pm-026-outcome33", "pm", "PM, V ZR 33/23",
  "Entscheidung des Bundesgerichtshofs: Die Revision hat Erfolg gehabt.",
  "die Anfechtungsklage abgewiesen.",
  "Outcome V ZR 33/23 laut PM: Berufungsurteil aufgehoben, Anfechtungsklage abgewiesen (Gestattungsbeschluss für Terrasse/Rampe hält stand)."),
 ("pm-026-aufzug", "pm", "PM, V ZR 244/22",
  "Die von den Klägern erstrebte Errichtung eines Personenaufzugs stellt eine angemessene bauliche Veränderung dar, die dem Gebrauch durch Menschen mit Behinderungen dient (§ 20 Abs. 2 Satz 1 Nr. 1 WEG).",
  None,
  "Personenaufzug = angemessene bauliche Veränderung i.S.d. § 20 Abs. 2 Satz 1 Nr. 1 – direkte Analogie für Treppenlift-Artikel (Aufzug/Hebetechnik als privilegierte Barrierefreiheitsmaßnahme)."),
]

# ---------------------------------------------------------------- extraction
def extract(text, start, end):
    i = text.find(start)
    assert i >= 0, f"START NOT FOUND: {start[:70]!r}"
    if end is None:
        return start
    j = text.find(end, i + len(start) - 1)
    assert j >= 0, f"END NOT FOUND after start: {end[:70]!r}"
    return text[i:j + len(end)]

ledger = []
errors = []
for qid, key, label, start, end, note in Q:
    try:
        quote = extract(texts[key], start, end)
    except AssertionError as e:
        errors.append((qid, str(e)))
        continue
    assert quote in texts[key]
    ledger.append({
        "source_id": qid,
        "url": SRC[key]["url"],
        "title": SRC[key]["title"],
        "quote": quote,
        "context_note": f"[{label}] {note}",
    })

print(f"extracted: {len(ledger)} / {len(Q)} quotes")
for qid, err in errors:
    print("ERROR", qid, err)
print()
for e in ledger:
    print(f"--- {e['source_id']} ---")
    print(e["quote"])
    print()
if errors:
    raise SystemExit("fix anchors before writing files")

# ---------------------------------------------------------------- write ledger
(OUT / "ledger-legal.json").write_text(
    json.dumps(ledger, ensure_ascii=False, indent=2), encoding="utf-8")

# ---------------------------------------------------------------- write markdown
md = []
md.append("# WEG-Artikel (Treppenlift & bauliche Veränderungen, WEG) – offizielle Rechtsquellen, wörtliche Zitate\n")
md.append(f"Alle Quellen am {FETCHED} (CET) abgerufen. Umfang: {len(ledger)} wörtliche Zitate aus 7 Dokumenten (3+x WEG-Einzelnormen, 2 BGH-Urteile als offizielle PDFs, 1 BGH-Pressemitteilung). Jedes Zitat ist maschinell gegen den bereinigten Quelltext verifiziert (literaler Teilstring-Nachweis); Rohdateien unter `raw/`; strukturiertes Gegenstück: `ledger-legal.json`.\n")
md.append("**Wichtige Korrektur zum Projektwissen:** Die Shortcode-Annahme 'wegg' für das WEG auf gesetze-im-internet.de ist falsch. Die Titelsuche des Seiteneigenen Systems (`/cgi-bin/htsearch?config=Titel_bmjhome2005&words=Wohnungseigentumsgesetz`) liefert den Shortcode **`woeigg`** (Wohnungseigentumsgesetz = 'Gesetz über das Wohnungseigentum und das Dauerwohnrecht'); `wegg/` und `weg/` liefern HTTP 404. Die Einzelnormen liegen unter `/woeigg/__N.html`. Verifizierte Version: Fassung der Bekanntmachung vom 12.01.2021 (BGBl. I S. 34, WEMoG-Neufassung; Geltung ab 01.12.2020), zuletzt geändert durch Art. 1 G v. 10.10.2024 (BGBl. 2024 I Nr. 306, Steckersolargeräte in § 20 Abs. 2 Nr. 5).\n")
md.append("**Doku Versuch V ZR 244/22 (offizielles PDF):** Direkter Zugriff scheiterte zunächst am Namensschema: `.../V_ZS/2022/V_ZR__244-22.pdf` (Doppel-Unterstrich, analog V_ZR__33-23.pdf) → HTTP 404; Varianten mit Jahr 2023/2024 im Pfad → HTTP 200 mit text/html (Soft-404-Fehlerseite, 29.958 Bytes). Über die Entscheidungssuche des BGH (`SiteGlobals/Forms/Suche/EntscheidungssucheBGH_Formular.html?templateQueryString=V+ZR+244/22`) wurde die offizielle URL mit **einem** Unterstrich gefunden: `V_ZS/2022/V_ZR_244-22.pdf?__blob=publicationFile&v=1` → HTTP 200, application/pdf, 238.872 Bytes, 27 Seiten. gesetze.co-Spiegel (nicht-offiziell) wurde daher nicht benötigt.\n")

section_order = ["weg20", "weg21", "weg44", "wegfull", "vzr244", "vzr33", "pm"]
sec_titles = {
    "weg20": "1) WEG § 20 – Bauliche Veränderungen (gesetze-im-internet.de, Shortcode woeigg)",
    "weg21": "2) WEG § 21 – Nutzungen und Kosten bei baulichen Veränderungen",
    "weg44": "3) WEG § 44 – Beschlussklagen",
    "wegfull": "4) WEG – Vollzitat und Stand (Gesamtausgabekopf)",
    "vzr244": "5) BGH, Urteil vom 09.02.2024 – V ZR 244/22 (Personenaufzug, München) – offizielles BGH-PDF",
    "vzr33": "6) BGH, Urteil vom 09.02.2024 – V ZR 33/23 (Terrasse/Rampe, Köln) – offizielles BGH-PDF",
    "pm": "7) BGH Pressemitteilung Nr. 026/2024 vom 09.02.2024",
}
for key in section_order:
    src = SRC[key]
    md.append(f"\n## {sec_titles[key]}\n")
    md.append(f"- **URL:** {src['url']}")
    md.append(f"- **Abgerufen (fetch date):** {FETCHED}")
    md.append(f"- **Rohdateien:** `{src['raw']}`")
    md.append(f"- **Bereinigung (cleaning steps):** {src['clean']}\n")
    for e in ledger:
        if e["url"] != src["url"]:
            continue
        md.append(f"### `{e['source_id']}` — {e['context_note'].split('] ')[0][1:]}\n")
        md.append(f"**Kontext:** {e['context_note'].split('] ', 1)[1]}\n")
        md.append("```\n" + e["quote"] + "\n```\n")

(OUT / "legal-extracts.md").write_text("\n".join(md), encoding="utf-8")
print(f"\nwrote {OUT/'legal-extracts.md'} ({sum(len(e['quote']) for e in ledger)} quote chars) and {OUT/'ledger-legal.json'} ({len(ledger)} entries)")
