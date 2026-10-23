#!/usr/bin/env python3
"""ADCELL-Affiliate-Seite: Registrierungsformular-Felder extrahieren + alle Evidence-Texte erzeugen."""
import re, pathlib

D = pathlib.Path(__file__).parent

def txt_of_html(path):
    b = pathlib.Path(path).read_bytes()
    for enc in ("utf-8", "latin-1"):
        try:
            s = b.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    s = re.sub(r"<script[\s\S]*?</script>", " ", s, flags=re.I)
    s = re.sub(r"<style[\s\S]*?</style>", " ", s, flags=re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", s)

# 1) ADCELL /affiliates Kern
t = txt_of_html(D / "adcell-affiliates.html")
print("ADCELL /affiliates:", t[:1500])
print()

# 2) Evidence-Texte für alle HTMLs erzeugen
for html_file in sorted(D.glob("*.html")):
    out = html_file.with_suffix(".txt")
    body = txt_of_html(html_file)
    header = f"Quelle: {html_file.name} (abgerufen 2026-10-23, Cron-Lauf)\nURL siehe research/partner-scan-231026.md\nExtrahierte Textfassung (HTML-Entitäten dekodiert): \n\n"
    out.write_text(header + body, encoding="utf-8")
    print(f"  {out.name}: {len(body)} chars")
