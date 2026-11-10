#!/usr/bin/env python3
"""Cannibalization check: what do existing hausnotruf articles cover re: Angehoerigen-Journey."""
import json, glob, os

d = "/Users/mac/agentic-business/barrierefrei-leads/content-ready"
needles = ["Angehörige", "Angehörigen", "einrichten", "Einrichtung", "bestellen",
           "Bestellung", "Beratungstermin", "aus der Ferne", "Vertragspartner",
           "Notfallkontakt", "Überzeug", "ansprechen"]
for f in sorted(glob.glob(os.path.join(d, "*.json"))):
    j = json.load(open(f))
    slug = os.path.basename(f).replace(".json", "")
    blob = json.dumps(j, ensure_ascii=False)
    hits = {n: blob.count(n) for n in needles if blob.count(n)}
    if "hausnotruf" in slug or "hilfsmittel" in slug:
        print(f"== {slug}")
        secs = [s.get("heading", "") for s in j.get("sections", [])]
        print("   headings:", " | ".join(secs)[:400])
        print("   hits:", {k: v for k, v in hits.items() if v})
