#!/usr/bin/env python3
"""Clean BGH press-release HTML (UTF-8) to plain text.
Usage: python3 clean_bgh.py <input.html> [output.txt]
Steps: UTF-8 decode -> drop head/script/style -> strip tags -> unescape
entities -> protected spaces to space -> collapse whitespace.
"""
import html
import re
import sys

raw = open(sys.argv[1], "rb").read()
try:
    text = raw.decode("utf-8")
except UnicodeDecodeError:
    text = raw.decode("iso-8859-1")
text = re.sub(r"<head[\s\S]*?</head>", " ", text, flags=re.I)
text = re.sub(r"<(script|style)[\s\S]*?</\1>", " ", text, flags=re.I)
text = re.sub(r"<[^>]+>", " ", text)
text = html.unescape(html.unescape(text))
for ch in ("\u00a0", "\u202f", "\u2007", "\u2009"):
    text = text.replace(ch, " ")
# BGH pages use U+00AD soft hyphens inside words for line breaking: remove
text = text.replace("\u00ad", "")
text = re.sub(r"\s+", " ", text).strip()
if len(sys.argv) > 2:
    with open(sys.argv[2], "w", encoding="utf-8") as fh:
        fh.write(text)
    print(f"wrote {sys.argv[2]} ({len(text)} chars)")
else:
    print(text)
