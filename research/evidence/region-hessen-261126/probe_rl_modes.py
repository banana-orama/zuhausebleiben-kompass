#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RL-PDF: alle Extraktions-Modi, Kontexte um die 4 offenen Needles."""
import re, subprocess, tempfile, os, urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
RL = "https://www.wibank.de/resource/blob/wibank/306346/39845aeb7d0d5a93fc4aa1b251a398e0/richtlinie-behindertengerechter-umbau-von-wohneigentum-data.pdf"

req = urllib.request.Request(RL, headers=UA)
raw = urllib.request.urlopen(req, timeout=60).read()
with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
    f.write(raw); p = f.name

def flat(t):
    t = t.replace("\u00ad", "").replace("\u00a0", " ")
    return re.sub(r"\s+", " ", t).lower()

for mode in ([], ["-layout"], ["-raw"], ["-nopgbrk"]):
    out = subprocess.run(["pdftotext", "-q"] + mode + [p, "-"], capture_output=True, timeout=120)
    t = flat(out.stdout.decode("utf-8", "replace"))
    dh = re.sub(r"([a-zäöüß])-\s+(?=[a-zäöüß])", r"\1", t)
    print("== mode %s (len %d) ==" % (mode, len(t)))
    for label, rx in [("15.000", r"15\.?000[^.]{0,80}"),
                      ("50 prozent", r"50\s*prozent[^.]{0,80}"),
                      ("pflegegrad", r"pflegegrad[^.]{0,80}"),
                      ("rechtsanspruch", r"rechtsanspruch[^.]{0,100}")]:
        found = False
        for hay, tag in ((t, "raw"), (dh, "dh")):
            m = re.search(rx, hay)
            if m:
                print("  [%s/%s] …%s…" % (label, tag, m.group(0)[:110]))
                found = True
                break
        if not found:
            print("  [%s] NICHT GEFUNDEN" % label)
os.unlink(p)
