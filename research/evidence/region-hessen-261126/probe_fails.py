#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Probe: tatsaechliche Wortlaute der 11 FAIL-Stellen (26.11.2026)."""
import html as html_mod, re, subprocess, sys, tempfile, urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}

def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()

def norm(raw_bytes):
    try:
        s = raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        s = raw_bytes.decode("latin-1")
    s = html_mod.unescape(s)
    s = re.sub(r"<script[\s\S]*?</script>", " ", s, flags=re.I)
    s = re.sub(r"<style[\s\S]*?</style>", " ", s, flags=re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = s.replace("\u00ad", "").replace("\u00a0", " ").replace("\u202f", " ")
    s = re.sub(r"\s+", " ", s)
    return s.lower()

def pdf_norm(raw):
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        f.write(raw); p = f.name
    try:
        out = subprocess.run(["pdftotext", "-q", p, "-"], capture_output=True, timeout=120)
        t = out.stdout.decode("utf-8", "replace")
    finally:
        import os; os.unlink(p)
    t = t.replace("\u00ad", "").replace("\u00a0", " ")
    return re.sub(r"\s+", " ", t).lower()

def ctx(t, needle_re, width=90, n=3):
    hits = 0
    for m in re.finditer(needle_re, t):
        print("   …%s…" % t[max(0, m.start()-width):m.end()+width])
        hits += 1
        if hits >= n: break
    if not hits:
        print("   (kein Treffer für %s)" % needle_re)

print("== 1) WIBank Produktseite ==")
t = norm(fetch("https://www.wibank.de/wibank/behindertengerechter-umbau-von-wohneigentum"))
print("-- 15.000:", )
ctx(t, r"15[\.,\s]?000")
print("-- 50 prozent/proz.:")
ctx(t, r"50\s?prozent")
print("-- pflegegrad:")
ctx(t, r"pflegegrad")
print("-- behinderung:")
ctx(t, r"grad der behinderung")

print("== 2) Richtlinie-PDF ==")
t = pdf_norm(fetch("https://www.wibank.de/resource/blob/wibank/306346/39845aeb7d0d5a93fc4aa1b251a398e0/richtlinie-behindertengerechter-umbau-von-wohneigentum-data.pdf"))
print("-- anteilfinanzierung:")
ctx(t, r"anteilfinanzierung")
print("-- 15.000:")
ctx(t, r"15[\.,\s]?000")
print("-- pflegegrad 2:")
ctx(t, r"pflegegrad\s?2")
print("-- rechtsanspruch:")
ctx(t, r"rechtsanspruch")

print("== 3) LWV ==")
t = norm(fetch("https://www.lwv-hessen.de/leben-wohnen/wohnen/leistungen-fuer-wohnraum.html"))
print("-- kosten:")
ctx(t, r"kosten", n=5)

print("== 4) Verwaltungsportal EGH ==")
t = norm(fetch("https://verwaltungsportal.hessen.de/leistung?leistung_id=L100001_8960876"))
print("-- laenge:", len(t))
ctx(t, r"wohnraum|landeswohlfahrtverband")

print("== 5) HMWEVW ==")
t = norm(fetch("https://wirtschaft.hessen.de/wohnen-und-bauen/soziale-wohnraumfoerderung"))
print("-- umbau-nennungen:")
ctx(t, r"umbau")
