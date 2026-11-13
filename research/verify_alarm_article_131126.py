#!/usr/bin/env python3
"""Acceptance für Briefing 26 (hausnotruf-alarm-ablauf) gegen LAUNCH-dist."""
import json
import re
import sys
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
SLUG = "hausnotruf-alarm-ablauf"

fails = []
n = 0


def check(label, cond, detail=""):
    global n
    n += 1
    print(("PASS " if cond else "FAIL ") + label + (f"  {detail}" if (detail and not cond) else ""))
    if not cond:
        fails.append(label)


html = (DIST / f"{SLUG}.html").read_text()

# 1. Launch-mode robots + canonical
check("robots index,follow", 'content="index,follow"' in html)
check("canonical", 'rel="canonical" href="https://zuhausebleiben-kompass.de/hausnotruf-alarm-ablauf.html"' in html)
check("H1 einmalig", html.count("<h1>") == 1)

# 2. Content-Support: jeder JSON-Key im HTML
a = json.loads((ROOT / "content-ready" / f"{SLUG}.json").read_text())


def strip_cite(t):
    t = re.sub(r"<sup class=\"cite\">.*?</sup>", "", t, flags=re.S)
    t = re.sub(r"\[\d+\]", "", t)
    return unescape(re.sub(r"<[^>]+>", " ", t))


body = strip_cite(html)
body_norm = re.sub(r"\s+", " ", unescape(html))
body = re.sub(r"\s+", " ", body)


def in_html(text, label):
    probe = re.sub(r"\[\d+\]", "", unescape(text))
    probe = re.sub(r"\s+", " ", probe).strip()
    ok = probe in body_norm or probe in body
    check(label, ok, probe[:70])


for i, p in enumerate(a["intro"]):
    in_html(p, f"intro[{i}] im HTML")
for si, s in enumerate(a["sections"]):
    check(f"section {si}: h2 im HTML", unescape(s["heading"]) in body_norm)
    for pi, p in enumerate(s.get("paragraphs", [])):
        in_html(p, f"section {si} para {pi} im HTML")
    for bi, b in enumerate(s.get("bullets", [])):
        in_html(b, f"section {si} bullet {bi} im HTML")
    if "table" in s:
        for h in s["table"]["headers"]:
            check(f"table header '{h[:24]}'", unescape(h) in body_norm)
for fi, f in enumerate(a["faqs"]):
    check(f"faq {fi} question", unescape(f["question"]) in body_norm)
    in_html(f["answer"], f"faq {fi} answer im HTML")

# 3. Kernzahlen/Needles (case-normalized)
low = body_norm.lower()
for needle in [
    "94 prozent", "30 sekunden", "80 prozent",
    "1,2 millionen", "11.000 rufe", "3.600 einsätze", "16 stunden",
    "iii zr 92/16", "bereitschafts- oder rettungsdienst",
    "maßnahmenplan", "tagestaste", "stiller alarm",
]:
    check(f"needle '{needle}'", needle in low)

# 4. Quellen-URLs im HTML (escaped & unescaped)
for s in a["sources"]:
    u1 = s["url"].replace("&", "&amp;")
    check(f"quelle: {s['url'][:60]}", s["url"] in html or u1 in html)

# 5. Partner-Placement auf dieser Seite, keins auf mobil-gps
check("partner placement gerendert", 'data-placement-id="malteser_beratungstermin"' in html)
check("partner rel sponsored", 'rel="sponsored noopener"' in html)
check("partner Anzeige-Label", "Anzeige · Kooperation mit Malteser" in body_norm)
other = (DIST / "hausnotruf-mobil-gps-unterwegs.html").read_text()
check("kein partner marker auf mobil-gps", 'data-placement-id' not in other)
disclosure = (DIST / "datenschutz.html").read_text()
check("DSE nennt Malteser", "Malteser" in disclosure)

# 6. Early-CTA specialMap + Checklisten-Anker
check("compare_top Ziel", 'data-cta-id="compare_top"' in html and "/hausnotruf-kosten-anbieter-vergleich.html" in html)
m = re.search(r'<a[^>]*data-cta-id="checklist_top"[^>]*href="([^"]+)"', html) or \
    re.search(r'<a[^>]*href="([^"]+)"[^>]*data-cta-id="checklist_top"', html)
check("checklist_top Anker existiert", bool(m) and html.count(f'id="{m.group(1).lstrip("#")}"') >= 1, str(m.group(1) if m else "n/a"))

# 7. Related links im Care-Cluster (nur Slugs aus content-ready, Footer raus)
CARE = re.compile(r"^(hausnotruf|pflegegrad|hilfsmittel|rollator|verhinderungspflege|tuerbreiten|beleuchtung|wohnumfeld|wohnung-anpassen)")
ready = {p.stem for p in (ROOT / "content-ready").glob("*.json")}
rel_slugs = set()
if "Passend dazu" in html:
    seg = html[html.find("Passend dazu"):]
    seg = seg[:seg.find("</section>")] if "</section>" in seg else seg
    rel_slugs = {s for s in re.findall(r'href="https://zuhausebleiben-kompass\.de/([a-z0-9-]+)\.html"', seg) if s in ready}
check("3 Related-Links", len(rel_slugs) >= 3, str(sorted(rel_slugs)))
check("Related im Care-Cluster", all(CARE.match(s) or s in ("treppenlift-zuschuss", "treppenlift-kosten") for s in rel_slugs), str(sorted(rel_slugs)))

# 8. SVG-Asset verlinkt mit Dimensionen
check("svg img mit width/height", bool(re.search(r'<img[^>]+hausnotruf-alarmkette\.svg[^>]+width="1200"[^>]+height="800"', html)))
check("svg caption KI-Label", "KI-unterstützt" in body_norm)
check("kein Vorschau-Prosa-Leak", "Entwurf zur ersten Orientierung" not in html)

print(f"\n{n - len(fails)}/{n} checks PASS")
sys.exit(1 if fails else 0)
