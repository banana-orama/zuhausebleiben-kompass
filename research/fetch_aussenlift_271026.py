#!/usr/bin/env python3
"""Fetch source base for briefing 13 (Treppenlift fuer Aussentreppen / Aussenlift), save clean evidence.
Targets: 2 Fachportale + 2 weitere Portal-Spannen, HIRO/Lifta Herstellerseiten, Lifta Preis/FAQ, VZ Planung, Handicare-DE-Probe."""
import urllib.request, html, re, pathlib

OUT = pathlib.Path("research/evidence/aussenlift-271026")
OUT.mkdir(parents=True, exist_ok=True)

TARGETS = {
    "tlw-aussenlift": "https://www.treppenliftwissen.de/treppenlift/aussenlift/",
    "personenaufzuege-aussen": "https://www.personenaufzuege.com/treppenlift/aussen/",
    "trep-preise-aussen": "https://treppenlifte-preise.de/magazin/treppenlift-aussen/",
    "seniorenrat-aussen": "https://www.seniorenrat.de/ratgeber/treppenlift-aussen/",
    "hiro-aussen": "https://hiro.de/treppenlifte-aussen/",
    "lifta-aussenlifte": "https://www.lifta.de/treppenlift/aussenlifte",
    "lifta-treppenlift": "https://www.lifta.de/treppenlift",
    "lifta-faq": "https://www.lifta.de/faq",
    "vz-planung": "https://www.verbraucherzentrale.de/wissen/gesundheit-pflege/pflege-zu-hause/treppenlifte-das-muessen-sie-ueber-planung-und-umsetzung-wissen-10711",
    "handicare-de-probe": "https://www.handicare.com/de/treppenlifte/",
}

MARKERS = ["Außen", "Aussen", "Wetter", "IP44", "IP-", "IPX", "Frost", "Kälte", "Abdeck", "UV", "Edelstahl", "Korrosion", "6.500", "4.000", "3.500", "Aufschlag"]

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
        with urllib.request.urlopen(req, timeout=45) as r:
            raw = r.read()
        path = OUT / f"{name}.html"
        path.write_bytes(raw)
        txt = clean(raw)
        (OUT / f"{name}.txt").write_text(txt, encoding="utf-8")
        print(f"== {name} :: {url} :: HTTP 200, {len(raw)} bytes raw, {len(txt)} chars clean")
        shown = 0
        for marker in MARKERS:
            idx = txt.find(marker)
            if idx >= 0 and shown < 3:
                print("   [{}] ... {}".format(marker, txt[max(0, idx-120):idx+500].replace("\n", " ")[:620]))
                shown += 1
    except Exception as e:
        print(f"!! {name} :: {url} :: FAILED {type(e).__name__}: {e}")
print("OK")
