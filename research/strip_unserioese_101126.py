#!/usr/bin/env python3
"""Strip alle Briefing-22-Quellen zu Evidenz-Txt (Stand 10.11.2026).

- HTML: tags raus, entities dekodiert, kurze Zeilen verworfen.
- gesetze-im-internet: ISO-8859-1 + Entities (bekannte Falle).
- PDF (VZ-Umfrage): pdftotext, sonst pypdf, sonst pip --user pypdf.
"""
import html
import os
import re
import subprocess
import sys

D = "/Users/mac/agentic-business/barrierefrei-leads/research/evidence/unserioese-101126"

LAW_FILES = ["uwg-4", "uwg-4a", "uwg-5", "uwg-5a", "bgb-312g"]  # ISO-8859-1
HTML_FILES = ["vz-treppenlifte-10711", "vz-verbandsklage-mobilae",
              "testde-windige-anbieter", "vsforum-mobilae"]


def strip_html(raw, lowchars=False):
    raw = re.sub(r"<script[^>]*>.*?</script>", " ", raw, flags=re.S | re.I)
    raw = re.sub(r"<style[^>]*>.*?</style>", " ", raw, flags=re.S | re.I)
    raw = re.sub(r"<!--.*?-->", " ", raw, flags=re.S)
    raw = re.sub(r"<[^>]+>", "\n", raw)
    raw = html.unescape(raw)
    lines = [re.sub(r"\s+", " ", l).strip() for l in raw.splitlines()]
    return "\n".join(l for l in lines if len(l) > (12 if lowchars else 25))


def read_bytes(path):
    b = open(path, "rb").read()
    try:
        return b.decode("utf-8")
    except UnicodeDecodeError:
        return b.decode("iso-8859-1", errors="replace")


for name in HTML_FILES:
    p = os.path.join(D, name + ".html")
    txt = strip_html(read_bytes(p))
    out = os.path.join(D, name + ".txt")
    open(out, "w", encoding="utf-8").write(txt)
    print(f"{name}.txt: {len(txt)} chars")

for name in LAW_FILES:
    p = os.path.join(D, name + ".html")
    txt = strip_html(read_bytes(p), lowchars=True)
    out = os.path.join(D, name + ".txt")
    open(out, "w", encoding="utf-8").write(txt)
    print(f"{name}.txt: {len(txt)} chars")

# PDF
pdf = os.path.join(D, "vz-umfrage-auswertung.pdf")
out = os.path.join(D, "vz-umfrage-auswertung.txt")
txt = ""
try:
    r = subprocess.run(["pdftotext", "-layout", pdf, out], capture_output=True, text=True)
    if r.returncode == 0:
        txt = open(out, encoding="utf-8", errors="replace").read()
        print(f"vz-umfrage-auswertung.txt: {len(txt)} chars (pdftotext)")
    else:
        raise FileNotFoundError("pdftotext failed")
except (FileNotFoundError, FileNotFoundError) as e:
    try:
        from pypdf import PdfReader
        reader = PdfReader(pdf)
        txt = "\n\n".join((page.extract_text() or "") for page in reader.pages)
        open(out, "w", encoding="utf-8").write(txt)
        print(f"vz-umfrage-auswertung.txt: {len(txt)} chars (pypdf)")
    except ImportError:
        print("pypdf fehlt -> pip install --user pypdf")
        r = subprocess.run([sys.executable, "-m", "pip", "install", "--user", "--quiet", "pypdf"],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print("pip failed:", r.stderr[-300:])
            sys.exit(1)
        from pypdf import PdfReader
        reader = PdfReader(pdf)
        txt = "\n\n".join((page.extract_text() or "") for page in reader.pages)
        open(out, "w", encoding="utf-8").write(txt)
        print(f"vz-umfrage-auswertung.txt: {len(txt)} chars (pypdf nach install)")

print("\nDONE")
