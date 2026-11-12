#!/usr/bin/env python3
"""Extract text from fetched sources + re-fetch BGB 312g with correct shortcode (bgb)."""
import subprocess, os, re, html as htmllib

E = "research/evidence/aufmass-121126"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"

# re-fetch 312g with correct shortcode
r = subprocess.run(["curl", "-sL", "-A", UA, "-m", "30",
                    "https://www.gesetze-im-internet.de/bgb/__312g.html",
                    "-o", f"{E}/bgb-312g.html", "-w", "%{http_code} %{size_download}"],
                   capture_output=True, text=True, timeout=40)
print("bgb-312g retry:", r.stdout.strip())


def strip_html(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    raw = re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>|<noscript[\s\S]*?</noscript>", " ", raw, flags=re.I)
    raw = re.sub(r"<[^>]+>", "\n", raw)
    raw = htmllib.unescape(raw)
    lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in raw.splitlines()]
    out, prev = [], None
    for ln in lines:
        if ln and ln != prev:
            out.append(ln)
        prev = ln
    return "\n".join(out)


KEY = re.compile(r"Aufmaß|Aufmass|Termin|Festpreis|Vermessung|ausmessen|Planungsunterlage|Schiene|Montage|Lieferzeit|Widerruf|Unterschrift|sofort", re.I)
for name in ["vz-planung", "ts-preise", "baethe", "chip", "lifta-haupt", "lifta-faq", "hiro-haupt", "bgb-312g", "bgb-632a"]:
    p = f"{E}/{name}.html"
    if not os.path.exists(p):
        print(f"{name}: missing")
        continue
    txt = strip_html(p)
    open(f"{E}/{name}.txt", "w", encoding="utf-8").write(txt)
    lines = txt.splitlines()
    hits = [i for i, ln in enumerate(lines) if KEY.search(ln)]
    print(f"== {name}: {len(lines)} lines, {len(hits)} keyword lines ==")
    for i in hits[:40]:
        print(f"  {i}: {lines[i][:160]}")
