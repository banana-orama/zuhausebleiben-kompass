#!/usr/bin/env python3
"""Phase-2-Gate 18.11.2026 (blitz-seo: interne Money-Anchor-Links + unslop-Pass Money-Page).

Laeuft gegen LAUNCH-dist (nach `npm run build:launch`). Prueft:
1. zuschuss.html: neue Description (Punkt statt Em-Dash), 3 Statuszellen mit ': ',
   0x U+2014 (Em-Dash) auf der ganzen Seite.
2. kosten.html: Inline-Link auf zuschuss mit Money-Anchor '4.180 Euro je Maßnahme'.
3. mieten.html: Inline-Link auf zuschuss mit Anchor 'der aktuelle Förderstatus'.
4. finanzierung.html: compare_top-CTA-Label 'Zuschuss bis 4.180 Euro zuerst prüfen',
   altes Label 0x.
5. angebote-vergleichen.html: 'Zuschuss-Förderstatus prüfen' (Variation, kein Duplikat).
6. steuerlich-absetzen.html: 'Pflegekassen-Zuschuss prüfen' (Variation, kein Duplikat).
7. Kontradiktion: auf den 5 geaenderten Artikeln ist das generische 'Förderung prüfen'
   als compare_top-Label 0x (Bad-Cluster-Fallback darf es behalten, geprüft wird
   nur pro Seite).
"""
import html as html_mod
import io
import pathlib
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
BASE = "https://zuhausebleiben-kompass.de"

fails = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f" | {detail}" if detail and not ok else ""))
    if not ok:
        fails.append(name)


def read(slug):
    raw = (DIST / f"{slug}.html").read_text(encoding="utf-8")
    return raw, html_mod.unescape(raw)


# 1. Money-Page: unslop-Ergebnis
raw_z, z = read("treppenlift-zuschuss")
check("desc: Punkt statt Em-Dash", "Unterlagen prüfen. Mit Förder-Entscheidungshilfe" in z)
check("desc alt 0x", "prüfen — mit" not in z)
for cell, old in [
    ("Offen: Anträge sind jederzeit möglich", "Offen — Anträge"),
    ("Gestoppt: keine neuen Anträge", "Gestoppt — keine neuen Anträge"),
    ("Offen: Kredit über einen Finanzierungspartner", "Offen — Kredit"),
]:
    check(f"zelle '{cell[:28]}…'", cell in z)
    check(f"zelle alt '{old}' 0x", old not in z)
# Em-Dash-Gate auf der ARTIKEL-Ebene (JSON): Template-Chrome (Titel-Suffix, „ — geprüft“-Quellenzeile,
# Related-h1s fremder Artikel) nutzt den Em-Dash sitewide und ist bewusst nicht Teil dieses Gates.
check("artikel-JSON 0x Em-Dash (U+2014)", "\u2014" not in (ROOT / "content-ready/treppenlift-zuschuss.json").read_text(encoding="utf-8"))

# 2-3. Inline-Money-Anchor-Links (LAUNCH rendert absolute hrefs)
for slug, label in [
    ("treppenlift-kosten", "4.180 Euro je Maßnahme"),
    ("treppenlift-mieten", "der aktuelle Förderstatus"),
]:
    raw, un = read(slug)
    pat = rf'<a href="{re.escape(BASE)}/treppenlift-zuschuss\.html">{re.escape(label)}</a>'
    m = re.search(pat, raw)
    check(f"{slug}: Inline-Link '{label}' → zuschuss", bool(m))
    check(f"{slug}: Inline-Label alt-generisch nicht neu", label not in ("Förderung",))

# 4-6. CTA-Label-Variationen
cta_specs = [
    ("treppenlift-finanzierung", "Zuschuss bis 4.180 Euro zuerst prüfen", "Förderung zuerst prüfen"),
    ("treppenlift-angebote-vergleichen", "Zuschuss-Förderstatus prüfen", None),
    ("treppenlift-steuerlich-absetzen", "Pflegekassen-Zuschuss prüfen", None),
]
for slug, new_label, old_label in cta_specs:
    raw, un = read(slug)
    check(f"{slug}: CTA '{new_label} →'", f'{new_label} →' in raw)
    if old_label:
        check(f"{slug}: altes Label '{old_label}' 0x", old_label not in raw)
    m = re.search(r'<a class="text-link" href="([^"]+)" data-cta-id="compare_top"', raw)
    check(f"{slug}: compare_top zielt auf zuschuss", bool(m) and "treppenlift-zuschuss.html" in (m.group(1) if m else ""))

# 7. Kein generisches 'Förderung prüfen' als compare_top auf den geaenderten Artikeln
for slug, _, _ in cta_specs:
    raw, _ = read(slug)
    seg = raw[raw.find('data-cta-id="compare_top"') : raw.find('data-cta-id="compare_top"') + 400]
    check(f"{slug}: compare_top-Label != 'Förderung prüfen'", "Förderung prüfen" not in seg)

print()
print(f"{len(fails)} FAILS")
sys.exit(1 if fails else 0)
