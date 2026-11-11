#!/usr/bin/env python3
"""Reconstruct the Joomla-cloaked e-mail address from the Lotse impressum raw HTML."""
import re
from html import unescape
from pathlib import Path

raw = Path("research/evidence/partner-terms-111126/lotse_impressum.html").read_text(encoding="utf-8", errors="replace")

# The cloak defines addy<hash> parts and an assembly script; dump every assignment line.
for m in re.finditer(r"addy[a-f0-9]{32}\s*=\s*'([^']*)'", raw):
    print("ASSIGN:", unescape(m.group(1)))

# Assembly calls like addyX = addyX + '...' appear as separate statements too.
seg = raw[raw.find("addybe7059ec0b96f2077c8ae273115f2929"):][:1200]
print("CONTEXT:", seg)
