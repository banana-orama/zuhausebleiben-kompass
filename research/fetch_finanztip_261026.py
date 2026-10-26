#!/usr/bin/env python3
"""Fetch finanztip secondary sources (Handwerkerkosten + außergewöhnliche Belastungen) as evidence."""
import pathlib, re, urllib.request, html

OUT = pathlib.Path("research/evidence/steuer-261026")
OUT.mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"}

def clean(txt: str) -> str:
    txt = html.unescape(txt.replace("\u00ad", ""))
    txt = re.sub(r"<script.*?</script>", " ", txt, flags=re.S)
    txt = re.sub(r"<style.*?</style>", " ", txt, flags=re.S)
    txt = re.sub(r"<[^>]+>", " ", txt)
    return re.sub(r"[ \t\u00a0]+", " ", txt)

for slug in ["handwerkerkosten", "aussergewoehnliche-belastungen"]:
    url = f"https://www.finanztip.de/{slug}/"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=45) as r:
            raw = r.read().decode("utf-8", "replace")
        path = OUT / f"finanztip-{slug}.txt"
        path.write_text(clean(raw), encoding="utf-8")
        print(f"== {url} HTTP 200, {len(raw)} bytes raw, {path.stat().st_size} chars clean")
    except Exception as e:
        print(f"== {url} FAILED: {e!r}")
