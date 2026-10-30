#!/usr/bin/env python3
"""Gate für SEO-Audit-Fix #7 (X3/X4): JEDE gebaute Seite hält <title> ≤65 Zeichen
(sichtbarer Text nach Entity-Unescape) und Meta-Description ≤160; Titles/Descriptions
sind je sitewide eindeutig; og:title spiegelt <title>. Läuft gegen den LAUNCH-Dist
(In-Kette nach test_cross_links.py, vor dem Preview-Rebuild)."""
import html as H
import re
import sys
from pathlib import Path

TITLE_MAX = 65   # X3: kein SERP-Abschneiden der Differentiatoren
DESC_MAX = 160   # X4: benefit-first Snippet, Disclaimer gehören in den Seitenkörper

DIST = Path("dist")
if not DIST.exists():
    print("FAIL: dist/ fehlt — erst npm run build:launch")
    sys.exit(1)

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S)
DESC_RE = re.compile(r'<meta name="description" content="([^"]*)"')
OG_RE = re.compile(r'<meta property="og:title" content="([^"]*)"')

pages, fails = [], []
for path in sorted(DIST.rglob("*.html")):
    raw = path.read_text(encoding="utf-8", errors="replace")
    rel = str(path.relative_to(DIST))
    t = TITLE_RE.search(raw)
    d = DESC_RE.search(raw)
    og = OG_RE.search(raw)
    if not t:
        fails.append(f"{rel}: kein <title>")
        continue
    title = H.unescape(t.group(1)).strip()
    desc = H.unescape(d.group(1)).strip() if d else ""
    if len(title) > TITLE_MAX:
        fails.append(f"{rel}: title {len(title)} > {TITLE_MAX}: {title}")
    if not desc:
        fails.append(f"{rel}: keine Meta-Description")
    elif len(desc) > DESC_MAX:
        fails.append(f"{rel}: description {len(desc)} > {DESC_MAX}: {desc[:80]}…")
    if og and H.unescape(og.group(1)).strip() != title:
        fails.append(f"{rel}: og:title != title")
    pages.append((rel, title, desc))

for label, idx in (("title", 1), ("description", 2)):
    seen = {}
    for rel, title, desc in pages:
        # region/*-Platzhalter teilen bewusst eine Description — deren expand-or-noindex-
        # Entscheidung ist Audit-Fix #5 (offen) und wird dort mitgezogen, nicht hier.
        if label == "description" and rel.startswith("region/"):
            continue
        seen.setdefault((title if label == "title" else desc), []).append(rel)
    for value, rels in seen.items():
        if len(rels) > 1:
            fails.append(f"doppelte {label} ({value[:60]}…): {', '.join(sorted(rels))}")

print(f"Gescannte HTML-Seiten: {len(pages)}")
print(f"{'Seite':46s} {'T':>3s} {'D':>3s}  Title")
for rel, title, desc in pages:
    print(f"{rel:46s} {len(title):3d} {len(desc):3d}  {title[:58]}")
over = [p for p in pages if len(p[1]) > TITLE_MAX or len(p[2]) > DESC_MAX]
print(f"\nVerletzungen: {len(over)} | Gate-Fehler: {len(fails)}")
if fails:
    print("FAIL:", *fails, sep="\n  ")
    sys.exit(1)
print("test_titles_meta: ALL PASS")
