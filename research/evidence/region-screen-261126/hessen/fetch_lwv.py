#!/usr/bin/env python3
"""Fetch LWV-Hessen Leistungen für Wohnraum + Verwaltungsportal KfW-Investitionszuschuss page."""
import subprocess, os, re, html

os.chdir(os.path.dirname(os.path.abspath(__file__)))
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"

PAGES = {
    "lwv-wohnraum": "https://www.lwv-hessen.de/leben-wohnen/wohnen/leistungen-fuer-wohnraum.html",
    "vp-kfw-455": "https://verwaltungsportal.hessen.de/leistung?leistung_id=B100019_101338702",
}

def strip_html(raw):
    raw = re.sub(r'<script[^>]*>.*?</script>', ' ', raw, flags=re.S | re.I)
    raw = re.sub(r'<style[^>]*>.*?</style>', ' ', raw, flags=re.S | re.I)
    raw = re.sub(r'<noscript[^>]*>.*?</noscript>', ' ', raw, flags=re.S | re.I)
    raw = re.sub(r'<!--.*?-->', ' ', raw, flags=re.S)
    raw = re.sub(r'</(p|div|li|h[1-6]|tr|section|article|br)>', '\n', raw, flags=re.I)
    raw = re.sub(r'<(br|hr)[^>]*>', '\n', raw, flags=re.I)
    raw = re.sub(r'<[^>]+>', ' ', raw)
    raw = html.unescape(raw)
    raw = raw.replace('\u00ad', '')
    raw = re.sub(r'[ \t\u00a0\u200b\u200c\u200d\ufeff]+', ' ', raw)
    raw = re.sub(r'\n\s*\n+', '\n', raw)
    return raw.strip()

for stem, url in PAGES.items():
    raw_f = f"raw-{stem}.html"
    r = subprocess.run(["curl", "-sL", "-A", UA, "-w", "%{http_code}", "--max-time", "60", "-o", raw_f, url],
                       capture_output=True, text=True)
    code = r.stdout.strip()[-3:]
    size = os.path.getsize(raw_f) if os.path.exists(raw_f) else 0
    print(f"{stem}: HTTP {code} size={size}")
    if code == "200" and size > 4000:
        with open(raw_f, encoding="utf-8", errors="replace") as fh:
            t = strip_html(fh.read())
        with open(f"{stem}.txt", "w", encoding="utf-8") as fh:
            fh.write(t)
        print(f"  -> {stem}.txt chars={len(t)}")
        for n in ["Treppenlift", "Umbau", "Wohnraum", "Einkommen", "Vermögen", "Kosten", "455", "Investitionszuschuss",
                  "genehmigt", "Wochen"]:
            c = t.count(n)
            if c:
                print(f"   {n}: {c}")
