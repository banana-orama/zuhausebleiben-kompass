#!/usr/bin/env python3
"""S1-Abs.-1-Quote [8] mit exakten pdftotext-Glyphen anhängen."""
import re, os, subprocess, sys

S = "/Users/mac/.hermes/skills/.archive/grounded-citations/scripts/sources.py"
os.environ["HERMES_CITATION_LEDGER"] = "/Users/mac/agentic-business/barrierefrei-leads/research/paare-191126-ledger.json"
EVID = "/Users/mac/agentic-business/barrierefrei-leads/research/evidence/paare-191126"

t = re.sub(r"\s+", " ", open(os.path.join(EVID, "gkv-hn-vertrag.txt")).read())
start = t.find("(1) Dieser Vertrag regelt die mehrkostenfreie")
end = t.find("Die Versorgung erfolgt ausschließlich", start)
exact = t[start:end].rstrip()
print("EXAKT:", repr(exact[-80:]))
r = subprocess.run([sys.executable, S, "quote", "8", "--text", exact,
                    "--from", os.path.join(EVID, "gkv-hn-vertrag.txt")],
                   capture_output=True, text=True)
print("PASS" if r.returncode == 0 else "FAIL", (r.stdout + r.stderr).strip()[:120])
