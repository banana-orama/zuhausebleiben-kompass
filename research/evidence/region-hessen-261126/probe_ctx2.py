#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kontexte fuer die 2 offenen Fragmente (26.11.)."""
import html as html_mod, os, re, subprocess, tempfile, urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}

def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=60).read()

def clean(s):
    s = html_mod.unescape(s)
    s = re.sub(r"<script[\s\S]*?</script>", " ", s, flags=re.I)
    s = re.sub(r"<style[\s\S]*?</style>", " ", s, flags=re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = s.replace("\u00ad", "").replace("\u00a0", " ").replace("\u202f", " ")
    return re.sub(r"\s+", " ", s).lower()

def ctx(t, rx, w=100, n=6):
    seen = 0
    for m in re.finditer(rx, t):
        print("   …%s…" % t[max(0, m.start()-w):m.end()+w]); seen += 1
        if seen >= n: break
    if not seen: print("   (0 Treffer)")

print("== WIBank Produktseite: 6.500 / aufzug ==")
t = clean(fetch("https://www.wibank.de/wibank/behindertengerechter-umbau-von-wohneigentum").decode("utf-8", "replace"))
ctx(t, r"6\.500")
ctx(t, r"aufzug")

RL = "https://www.wibank.de/resource/blob/wibank/306346/39845aeb7d0d5a93fc4aa1b251a398e0/richtlinie-behindertengerechter-umbau-von-wohneigentum-data.pdf"
raw = fetch(RL)
outs = []
for mode in ([], ["-raw"]):
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        f.write(raw); p = f.name
    try:
        out = subprocess.run(["pdftotext", "-q"] + mode + [p, "-"], capture_output=True, timeout=120)
        txt = out.stdout.decode("utf-8", "replace")
    finally: os.unlink(p)
    t = txt.replace("\u00ad", "").replace("\u00a0", " ")
    outs.append((mode, re.sub(r"\s+", " ", t).lower()))

for mode, t in outs:
    print("== RL mode %s: vorhabenbeginn ==" % (mode,))
    ctx(t, r"vorhabenbeginn[^.]{0,140}", w=60, n=4)
