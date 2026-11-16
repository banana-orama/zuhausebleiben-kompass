#!/usr/bin/env python3
"""Verify that every German-quote span („…") in QUOTES.md appears verbatim
in at least one raw-*.txt extract in this directory.

- Soft hyphens (U+00AD), zero-width chars are stripped; en/em dashes, German
  quotes normalized; whitespace collapsed — matching what a reader sees.
- " / " separators and parenthetical annotations in QUOTES.md sit OUTSIDE the
  „…" spans and are never checked.
Prints per-section results and a final summary."""
import re
from pathlib import Path

D = Path(__file__).parent

def norm(s: str) -> str:
    s = s.replace("\u00ad", "").replace("\u200b", "")
    s = s.replace("\u201e", '"').replace("\u201c", '"')
    s = s.replace("\u2013", "-").replace("\u2014", "-").replace("\u2010", "-")
    s = re.sub(r"\s+", " ", s)
    return s.lower()

texts = {p.name: norm(p.read_text(encoding="utf-8", errors="replace"))
         for p in sorted(D.glob("raw-*.txt"))}
md = (D / "QUOTES.md").read_text(encoding="utf-8")

section_spans = []  # (section_title, [fragment, ...])
cur_title = None
cur_spans = None
in_quotes = False
for line in md.splitlines():
    if line.startswith("## "):
        if cur_title and cur_spans:
            section_spans.append((cur_title, cur_spans))
        cur_title, cur_spans, in_quotes = line[3:].strip(), [], False
        continue
    if "- **Wörtliche Zitate:**" in line:
        in_quotes = True
        continue
    if line.startswith("- "):
        in_quotes = False  # any other bullet (Nicht gefunden, Einordnung, URL, ...) ends the list
        continue
    m = re.match(r"^\s*\d+\.\s+(.*)$", line)
    if m and in_quotes and cur_spans is not None:
        spans = re.findall(r"\u201e(.+?)\"", m.group(1), flags=re.S)
        cur_spans.extend(spans)
if cur_title and cur_spans:
    section_spans.append((cur_title, cur_spans))

total = ok = 0
problems = []
for title, spans in section_spans:
    for sp in spans:
        frag = norm(sp)
        total += 1
        hits = [n for n, t in texts.items() if frag in t]
        if hits:
            ok += 1
        else:
            problems.append((title, sp[:90]))
print(f"quote spans checked: {total}, verbatim confirmed: {ok}, NOT matched: {len(problems)}")
for t, s in problems:
    print(f"  [{t[:40]}] not found: {s}")
