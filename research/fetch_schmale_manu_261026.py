#!/usr/bin/env python3
"""Fetch manufacturer primary sources: Lifta schmale-treppe page, HIRO prices page."""
import urllib.request, html, re, pathlib

OUT = pathlib.Path("research/evidence/schmale-treppe-261026")
OUT.mkdir(parents=True, exist_ok=True)

TARGETS = {
    "lifta-schmale-treppe": "https://www.lifta.de/treppenlift/schmale-treppe",
    "hiro-preise": "https://hiro.de/preise/",
}

def clean(raw: bytes) -> str:
    txt = raw.decode("utf-8", errors="replace")
    txt = html.unescape(txt)
    txt = txt.replace("\u00ad", "")
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
        txt = clean(raw)
        (OUT / f"{name}.txt").write_text(txt, encoding="utf-8")
        print(f"== {name} :: {url} :: HTTP 200, {len(raw)} bytes raw, {len(txt)} chars clean")
        for marker in ["Breite", "Preis", "Preise"]:
            idx = txt.find(marker)
            if idx >= 0:
                print("   ...", txt[max(0, idx-80):idx+500].replace("\n", " ")[:560])
                break
    except Exception as e:
        print(f"!! {name} :: {url} :: FAILED {type(e).__name__}: {e}")
print("OK")
