#!/usr/bin/env python3
"""Textfassungen aller direct-partner-scan-281026-HTMLs erzeugen (Entities dekodiert, Tags gestrippt)."""
import re, html, pathlib

D = pathlib.Path(__file__).parent

def txt_of_html(path):
    b = pathlib.Path(path).read_bytes()
    s = None
    for enc in ("utf-8", "latin-1"):
        try:
            s = b.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    if s is None:
        s = b.decode("utf-8", errors="replace")
    s = re.sub(r"<!--[\s\S]*?-->", " ", s)
    s = re.sub(r"<script[\s\S]*?</script>", " ", s, flags=re.I)
    s = re.sub(r"<style[\s\S]*?</style>", " ", s, flags=re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = s.replace("\u00ad", "").replace("\xa0", " ")
    return re.sub(r"\s+", " ", s)

for html_file in sorted(D.glob("*.html")):
    out = html_file.with_suffix(".txt")
    body = txt_of_html(html_file)
    header = (f"Quelle: {html_file.name} (abgerufen 2026-10-28, Cron-Lauf)\n"
              "URL siehe research/direct-partner-scan-281026.md\n\n")
    out.write_text(header + body, encoding="utf-8")
    print(f"  {out.name}: {len(body)} chars")
