#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import html as html_mod, re, urllib.request
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}

def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    raw = urllib.request.urlopen(req, timeout=60).read()
    try: s = raw.decode("utf-8")
    except UnicodeDecodeError: s = raw.decode("latin-1")
    s = html_mod.unescape(s)
    s = re.sub(r"<script[\s\S]*?</script>", " ", s, flags=re.I)
    s = re.sub(r"<style[\s\S]*?</style>", " ", s, flags=re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = s.replace("\u00ad", "").replace("\u00a0", " ").replace("\u202f", " ")
    return re.sub(r"\s+", " ", s).lower()

def ctx(t, rx, w=120, n=3):
    seen = 0
    for m in re.finditer(rx, t):
        print("   …%s…" % t[max(0, m.start()-w):m.end()+w]); seen += 1
        if seen >= n: break
    if not seen: print("   (0 Treffer)")

print("== KfW 159: kombi ==")
ctx(fetch("https://www.kfw.de/159"), r"kombiniert|kombination|mit dem kredit der kwf")
print("== VP-EGH: keine kosten / fristen ==")
t = fetch("https://verwaltungsportal.hessen.de/leistung?leistung_id=L100001_8960876")
ctx(t, r"keine kosten")
ctx(t, r"wochen")
print("== WIA: fünf jahre satz ==")
ctx(fetch("https://wohnen-im-alter.hessen.de/wohnberatung/finanzierung/soziale-wohnraumfoerderung"), r"fünf jahren[^.]{0,160}")
print("== SOZ: 21 landkreise / organisationseinheiten ==")
t = fetch("https://soziales.hessen.de/leistungen-der-eingliederungshilfe-gemaess-sgb-ix")
ctx(t, r"21 landkreise|organisationseinheiten|kreisfreien städte")
print("== LWV: kosten-antwort ==")
ctx(fetch("https://www.lwv-hessen.de/leben-wohnen/wohnen/leistungen-fuer-wohnraum.html"), r"an den kosten beteiligen\?[^?]{0,300}")
