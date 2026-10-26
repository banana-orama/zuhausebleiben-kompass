#!/usr/bin/env python3
"""Fetch source base for briefing 11 (treppenlift schmale Treppe), save clean evidence.
Targets: VZ Planungsartikel, treppenliftwissen (schmale Treppe), altersgerecht-modernisieren (schmale Treppen)."""
import urllib.request, html, re, sys, pathlib

OUT = pathlib.Path("research/evidence/schmale-treppe-261026")
OUT.mkdir(parents=True, exist_ok=True)

TARGETS = {
    "vz-planung": "https://www.verbraucherzentrale.de/wissen/gesundheit-pflege/pflege-zu-hause/treppenlifte-das-muessen-sie-ueber-planung-und-umsetzung-wissen-10711",
    "tlw-schmale-treppe": "https://www.treppenliftwissen.de/treppenlift/schmale-treppe/",
    "am-schmale-treppen": "https://altersgerecht-modernisieren.de/treppenlift/schmale-treppen/",
}

def clean(raw: bytes) -> str:
    txt = raw.decode("utf-8", errors="replace")
    txt = html.unescape(txt)
    txt = txt.replace("\u00ad", "")          # soft hyphen
    txt = re.sub(r"<script.*?</script>", " ", txt, flags=re.S)
    txt = re.sub(r"<style.*?</style>", " ", txt, flags=re.S)
    txt = re.sub(r"<[^>]+>", " ", txt)
    txt = re.sub(r"[ \t\u00a0]+", " ", txt)
    txt = re.sub(r"\s*\n\s*", "\n", txt)
    return txt.strip()

for name, url in TARGETS.items():
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"})
        with urllib.request.urlopen(req, timeout=40) as r:
            raw = r.read()
        path = OUT / f"{name}.html"
        path.write_bytes(raw)
        txt = clean(raw)
        (OUT / f"{name}.txt").write_text(txt, encoding="utf-8")
        print(f"== {name} :: {url} :: HTTP 200, {len(raw)} bytes raw, {len(txt)} chars clean")
        # show the sections that carry width/space claims
        for marker in ["Breite", "Aufmaß", "Maß"]:
            idx = txt.find(marker)
            if idx >= 0:
                print("   ...", txt[max(0, idx-100):idx+600].replace("\n", " ")[:700])
                break
    except Exception as e:
        print(f"!! {name} :: {url} :: FAILED {type(e).__name__}: {e}")
print("OK")
