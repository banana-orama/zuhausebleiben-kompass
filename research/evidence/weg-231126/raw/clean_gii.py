#!/usr/bin/env python3
"""Clean a gesetze-im-internet.de HTML page (ISO-8859-1, numeric entities) to plain text.

Usage: python3 clean_gii.py <input.html> [output.txt]
Cleaning steps (in order):
  1. decode bytes as ISO-8859-1 (site charset)
  2. drop <head>, script/style, dn:... metadata blocks
  3. strip all tags (replace with single space)
  4. decode HTML entities (named + numeric, incl. &nbsp;)
  5. collapse whitespace runs to single spaces, strip
"""
import html
import re
import sys

def clean(raw_bytes):
    text = raw_bytes.decode("iso-8859-1")
    # drop head and script/style blocks entirely
    text = re.sub(r"<head[\s\S]*?</head>", " ", text, flags=re.I)
    text = re.sub(r"<(script|style)[\s\S]*?</\1>", " ", text, flags=re.I)
    # strip tags
    text = re.sub(r"<[^>]+>", " ", text)
    # decode entities twice (catches double-encoded)
    text = html.unescape(text)
    text = html.unescape(text)
    # NBSP (U+00A0) and other protected spaces -> regular space
    text = text.replace("\u00a0", " ").replace("\u202f", " ").replace("\u2007", " ")
    # collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text

if __name__ == "__main__":
    data = open(sys.argv[1], "rb").read()
    out = clean(data)
    if len(sys.argv) > 2:
        with open(sys.argv[2], "w", encoding="utf-8") as fh:
            fh.write(out)
        print(f"wrote {sys.argv[2]} ({len(out)} chars)")
    else:
        print(out)
