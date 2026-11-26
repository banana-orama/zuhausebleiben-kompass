#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import html as html_mod, re, urllib.request
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
req = urllib.request.Request("https://www.wibank.de/wibank/behindertengerechter-umbau-von-wohneigentum", headers=UA)
raw = urllib.request.urlopen(req, timeout=60).read()
try:
    s = raw.decode("utf-8")
    print("decode: utf-8 ok")
except UnicodeDecodeError:
    s = raw.decode("latin-1")
    print("decode: latin-1")
s = html_mod.unescape(s)
s = re.sub(r"<script[\s\S]*?</script>", " ", s, flags=re.I)
s = re.sub(r"<style[\s\S]*?</style>", " ", s, flags=re.I)
s = re.sub(r"<[^>]+>", " ", s)
s = s.replace("\u00ad", "").replace("\u00a0", " ").replace("\u202f", " ")
s = re.sub(r"\s+", " ", s).lower()
i = s.find("6.500")
print("pos 6.500:", i)
if i >= 0:
    seg = s[i-60:i+40]
    print("repr:", repr(seg))
    print("enthält 'aufzugeinbau':", "aufzugeinbau" in s, "| 'lift-/aufzug':", "lift-/aufzug" in s)
for probe in ["lift-/aufzugeinbau", "aufzugeinbau", "lift"]:
    print(probe, "->", s.count(probe))
