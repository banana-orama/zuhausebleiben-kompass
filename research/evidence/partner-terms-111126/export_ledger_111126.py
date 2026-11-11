#!/usr/bin/env python3
"""Export the grounded-citations ledger to the project evidence ledger JSON (11.11.2026)."""
import json
import subprocess
import sys
from pathlib import Path

S = str(Path.home() / ".hermes/profiles/milo/skills/research/grounded-citations/scripts/sources.py")
out = subprocess.run([sys.executable, S, "list", "--json"], capture_output=True, text=True)
data = json.loads(out.stdout)
dest = Path("research/partner-terms-111126-ledger.json")
dest.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
entries = data if isinstance(data, list) else data.get("sources", data)
n = len(entries)
quotes = sum(len(e.get("quotes", [])) for e in entries) if isinstance(entries, list) else "?"
print(f"exported: {dest} ({n} sources, {quotes} quotes)")
