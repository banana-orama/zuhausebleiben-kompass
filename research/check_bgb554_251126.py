#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Frische Prüfung § 554 BGB (Stand-Needle für die Mieter-Sektion, 25.11.2026)."""
import html as html_mod
import re
import sys
import urllib.request

url = "https://www.gesetze-im-internet.de/bgb/__554.html"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
raw = urllib.request.urlopen(req, timeout=60).read()
s = raw.decode("latin-1")
s = html_mod.unescape(s)
s = re.sub(r"<script[\s\S]*?</script>", " ", s, flags=re.I)
s = re.sub(r"<[^>]+>", " ", s)
s = s.replace("\u00ad", "").replace("\u00a0", " ")
s = re.sub(r"\s+", " ", s)

needles = [
    "Barrierereduzierung, E-Mobilität, Einbruchsschutz und Steckersolargeräte",
    "Der Mieter kann verlangen, dass ihm der Vermieter bauliche Veränderungen der Mietsache erlaubt, die dem Gebrauch durch Menschen mit Behinderungen, dem Laden elektrisch betriebener Fahrzeuge, dem Einbruchsschutz oder der Stromerzeugung durch Steckersolargeräte dienen",
    "Der Anspruch besteht nicht, wenn die bauliche Veränderung dem Vermieter auch unter Würdigung der Interessen des Mieters nicht zugemutet werden kann",
]
fails = 0
for n in needles:
    ok = n.lower() in s.lower()
    print(("PASS " if ok else "FAIL ") + n[:70])
    fails += 0 if ok else 1
out = "/Users/mac/agentic-business/barrierefrei-leads/research/evidence/region-bw-251126/bgb-554-251126.txt"
open(out, "w", encoding="utf-8").write(s)
print("saved:", out)
sys.exit(1 if fails else 0)
