#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hygiene-Check region-baden-wuerttemberg.json: U+00AD, Längen, Schlüssel."""
import json
import sys

path = "/Users/mac/agentic-business/barrierefrei-leads/data/region-baden-wuerttemberg.json"
raw = open(path, encoding="utf-8").read()
fails = 0

if "\u00ad" in raw:
    # soft hyphen in geliefertem Text: für Onpage-Text entfernen (L-Bank-Wortlaute bewusst normalisiert)
    print("SOFT-HYPHEN found -> removing")
    raw = raw.replace("\u00ad", "")
    open(path, "w", encoding="utf-8").write(raw)
else:
    print("no soft hyphens")

d = json.loads(raw)
for k in ["slug", "name", "teaser", "title", "description", "h1", "leads", "sections", "faqs", "ctaEarly", "standLine", "sources", "related"]:
    if k not in d:
        print("FAIL missing key:", k)
        fails += 1

title_total = d["title"] + " — Zuhausebleiben Kompass"
print("title chars:", len(title_total), "| desc chars:", len(d["description"]))
if len(title_total) > 65:
    print("FAIL title >65")
    fails += 1
if len(d["description"]) > 160:
    print("FAIL desc >160")
    fails += 1
print("slug:", d["slug"], "| sections:", len(d["sections"]), "| faqs:", len(d["faqs"]), "| sources:", len(d["sources"]))
sys.exit(1 if fails else 0)
