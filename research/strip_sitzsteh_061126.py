#!/usr/bin/env python3
"""Strip HTML to plain text for evidence files (evidence dir, date-tagged)."""
import html as htmllib
import pathlib
import re
import sys

EVID = pathlib.Path(__file__).resolve().parent / "evidence" / "sitzsteh-061126"

def strip(raw: str) -> str:
    raw = re.sub(r"<script[\s\S]*?</script>", " ", raw, flags=re.I)
    raw = re.sub(r"<style[\s\S]*?</style>", " ", raw, flags=re.I)
    raw = re.sub(r"<!--[\s\S]*?-->", " ", raw)
    raw = re.sub(r"<(br|/p|/li|/h[1-6]|/tr|/div)[^>]*>", "\n", raw, flags=re.I)
    raw = re.sub(r"<[^>]+>", " ", raw)
    raw = htmllib.unescape(raw)
    raw = raw.replace("\xa0", " ").replace("\u202f", " ").replace("\u00ad", "")
    raw = re.sub(r"[ \t]+", " ", raw)
    raw = re.sub(r"\n\s*\n+", "\n", raw)
    raw = re.sub(r"\s+([,.:;!?])", r"\1", raw)  # Tag-Abfälle vor Satzzeichen entfernen
    return raw.strip()

def main() -> None:
    for name in sys.argv[1:]:
        p = EVID / f"{name}-061126.html"
        if not p.exists():
            print(f"MISSING: {p}")
            continue
        txt = strip(p.read_text(encoding="utf-8", errors="replace"))
        out = EVID / f"{name}-061126.txt"
        out.write_text(txt, encoding="utf-8")
        print(f"{name}: {len(txt)} chars -> {out.name}")

if __name__ == "__main__":
    main()
