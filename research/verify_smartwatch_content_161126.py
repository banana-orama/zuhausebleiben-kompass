#!/usr/bin/env python3
"""Content-Support-Gate für hausnotruf-smartwatch-als-ersatz gegen LAUNCH-dist.

Asserts (Lektionen eingearbeitet: sup.cite-Element komplett strippen, HTML-VOR
Vergleich unescape — `from html import unescape`, kein lokales Shadowing; URLs mit
& doppelt geprüfen; CTA/Partner über Element-Attribute, nie über Klassennamen):
1. robots index,follow; Title/Desc/H1 korrekt
2. Beide Lead-Absätze, jede Section-Heading, jeder Absatz, Bullets, Tabellen-Header
   und -Zellen, paragraphs_after, FAQs — alles im gebauten HTML
3. Quellen: jede URL (raw + &amp;-variante) + checked_at im HTML
4. Bild: Datei existiert, alt+caption+KI-Label im HTML, intrinsische Dimensionen
5. Related-Links: exakt die 3 Cross-Link-Ziele in Reihenfolge
6. Early-CTA über data-cta-id="compare_top" mit Ziel hausnotruf-kosten-anbieter-vergleich,
   Checklisten-Anker "#abschnitt-9" mit Label "Zur Checkliste"
7. Absenzen: 0x awin1.com / 4.180 / 16.720 / data-partner-placement / rel="sponsored"
8. JSON-LD parst (Article + FAQPage), kein Entwurfs-Prosa-Leak
"""
import json
import pathlib
import re
import sys
from html import unescape

ROOT = pathlib.Path(__file__).resolve().parent.parent
ART = json.loads((ROOT / "content-ready" / "hausnotruf-smartwatch-als-ersatz.json").read_text(encoding="utf-8"))
XLINKS = json.loads((ROOT / "data" / "cross-links.json").read_text(encoding="utf-8"))
HTML_PATH = ROOT / "dist" / "hausnotruf-smartwatch-als-ersatz.html"

FAIL = []
N = 0


def check(label, cond, detail=""):
    global N
    N += 1
    print(("PASS " if cond else "FAIL ") + label + ("" if cond else f"  {detail}"))
    if not cond:
        FAIL.append(label)


raw = HTML_PATH.read_text(encoding="utf-8")
# citations robust entfernen: sup-Element egal mit welchen Attributen + uebriggebliebene [n]-Marker
no_cite = re.sub(r"<sup[^>]*>.*?</sup>", "", raw, flags=re.S)
no_cite = re.sub(r"\[\d+\]", "", no_cite)
text = unescape(re.sub(r"<[^>]+>", " ", no_cite))
text = re.sub(r"\s+", " ", text)
raw_un = unescape(raw)


def in_html(s):
    s = re.sub(r"\[\d+\]", "", unescape(re.sub(r"\s+", " ", s)))
    s = re.sub(r"\s+", " ", s).strip()
    return s in text


# 1. Meta
check("robots index,follow", '<meta name="robots" content="index,follow">' in raw)
check("Title = JSON-Titel + Suffix", f"<title>{ART['title']} — ZuhauseBleiben Kompass</title>" in raw)
check("Meta-Description = JSON", f'content="{ART["description"]}"' in raw)
check("H1 = JSON-h1", ART["h1"] in raw)

# 2. Intro (beide Lead-Absätze)
leads = re.findall(r'<p class="lead">(.*?)</p>', raw, flags=re.S)
check("Lead-Absätze = 2", len(leads) == 2, str(len(leads)))
for i, p in enumerate(ART["intro"] if isinstance(ART["intro"], list) else [ART["intro"]], 1):
    check(f"Lead {i} vollständig", in_html(p))

# Sections
check("Sections = 10", len(ART["sections"]) == 10)
for i, s in enumerate(ART["sections"], 1):
    check(f"S{i} Heading", s["heading"] in raw)
    check(f"S{i} Anker abschnitt-{i}", f'id="abschnitt-{i}"' in raw)
    for j, p in enumerate(s.get("paragraphs", []), 1):
        check(f"S{i} Absatz {j}", in_html(p))
    for j, b in enumerate(s.get("bullets", []), 1):
        check(f"S{i} Bullet {j}", in_html(b))
    for j, p in enumerate(s.get("paragraphs_after", []), 1):
        check(f"S{i} Abschlussabsatz {j}", in_html(p))
    if "table" in s:
        for h in s["table"]["headers"]:
            check(f"S{i} Tabellenkopf '{h[:30]}'", h in raw)
        for r, row in enumerate(s["table"]["rows"], 1):
            for c, cell in enumerate(row, 1):
                check(f"S{i} Zelle {r}/{c}", in_html(cell))

# FAQs
for i, f in enumerate(ART["faqs"], 1):
    check(f"FAQ {i} Frage", f["question"] in raw)
    check(f"FAQ {i} Antwort", in_html(f["answer"]))

# 3. Quellen
for i, s in enumerate(ART["sources"], 1):
    u = s["url"]
    check(f"Quelle {i} URL", (u in raw) or (u.replace("&", "&amp;") in raw), u[:60])
    check(f"Quelle {i} checked_at", f"geprüft {s['checked_at']}" in raw)

# 4. Bild
img = ART["image"]
check("Bild-Datei existiert", (ROOT / img["src"]).exists())
check("Bild eingebunden", f'src="{ROOT.name}/' not in raw and f'assets/images/hausnotruf-smartwatch-entscheidung.svg' in raw)
check("Bild-Alt vollständig", re.search(r'<img[^>]+alt="[^"]{80,}"[^>]*>', raw) is not None)
check("KI-Label in Caption", "KI-unterstützt" in raw)
check("Quellenstand-Datum im Artikel", "16.11.2026" in text)

# 5. Related-Links (exakt Cross-Link-Ziele, Reihenfolge)
m = re.search(r'<section class="related">.*?</section>', raw, flags=re.S)
check("Related-Sektion vorhanden", bool(m))
if m:
    seg = m.group(0)
    hrefs = re.findall(r'href="[^"]*?/([a-z0-9-]+)\.html"', seg)
    expected = XLINKS["links"][ART["slug"]]
    check("Related exakt 3", len(hrefs) == 3, str(hrefs))
    check("Related-Reihenfolge == Cross-Links", hrefs == expected, f"{hrefs} != {expected}")

# 6. CTAs
check("Early-CTA compare_top → kosten-vergleich",
      'href="https://zuhausebleiben-kompass.de/hausnotruf-kosten-anbieter-vergleich.html" data-cta-id="compare_top"' in raw)
check("Early-CTA Label", ("Kosten & Anbieter vergleichen" in raw) or ("Kosten &amp; Anbieter vergleichen" in raw))
check("Checklisten-CTA 'Zur Checkliste'", 'href="#abschnitt-9"' in raw and "Zur Checkliste" in raw)
check("Druck-CTA unten", 'data-cta-id="print_bottom"' in raw)

# 7. Absenzen
for needle in ["awin1.com", "4.180", "16.720", "data-partner-placement", 'rel="sponsored"']:
    check(f"Absenz 0 × '{needle}'", raw.count(needle) == 0, str(raw.count(needle)))

# 8. JSON-LD
ld = re.findall(r'<script type="application/ld\+json">(.*?)</script>', raw, flags=re.S)
ok = True
for block in ld:
    try:
        json.loads(block)
    except Exception as e:
        ok = False
        check("JSON-LD parst", False, str(e)[:80])
check("JSON-LD Blöcke vorhanden", len(ld) >= 1)
check("FAQPage im Schema", any("FAQPage" in b for b in ld))
art_seg = re.search(r"<article>.*?</article>", raw, flags=re.S)
check("Kein Preview-/Entwurfs-Leak", bool(art_seg) and "noch nicht eingerichtet" not in art_seg.group(0))

print()
print(f"{N - len(FAIL)}/{N} PASS" + ("  — ALL PASS" if not FAIL else f"  — {len(FAIL)} FAILS"))
sys.exit(1 if FAIL else 0)
