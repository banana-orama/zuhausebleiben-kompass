#!/usr/bin/env python3
"""ADCELL-Terms-Refresh 06.11.2026: HIRO 9440 + Pflegehase 10690 + Registrierungsseite.
Roh-HTML lokal, Text-Extrakt mit Entity-Decoding + Whitespace-Collapse, Assertion-Checks."""
import html
import re
import sys
import urllib.request
from pathlib import Path

OUT = Path(__file__).parent
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"

PAGES = {
    "hiro-lift": "https://www.adcell.de/partnerprogramme/hiro-lift",
    "pflegehase-hausnotruf": "https://www.adcell.de/partnerprogramme/pflegehase-hausnotruf",
    "adcell-affiliates-signup": "https://www.adcell.de/affiliates",
}

NEEDLES = {
    "hiro-lift": ["50,00", "90", "Freigabe", "Lead", "SEM", "Cookie", "Traffic"],
    "pflegehase-hausnotruf": ["25,00", "60", "Freigabe", "Lead", "10690", "Tunstall"],
    "adcell-affiliates-signup": ["Partner", "Registrieren", "ADCELL"],
}


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "de-DE,de;q=0.9"})
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.read().decode("utf-8", errors="replace")


def strip_to_text(raw: str) -> str:
    raw = re.sub(r"<script[\s\S]*?</script>", " ", raw, flags=re.I)
    raw = re.sub(r"<style[\s\S]*?</style>", " ", raw, flags=re.I)
    raw = re.sub(r"<[^>]+>", " ", raw)
    raw = html.unescape(raw)
    return re.sub(r"\s+", " ", raw).strip()


def main() -> int:
    fails = 0
    for name, url in PAGES.items():
        try:
            raw = fetch(url)
        except Exception as exc:  # noqa: BLE001
            print(f"FETCH-FAIL {name}: {exc}")
            fails += 1
            continue
        (OUT / f"{name}-061126.html").write_text(raw, encoding="utf-8")
        text = strip_to_text(raw)
        (OUT / f"{name}-061126.txt").write_text(text, encoding="utf-8")
        print(f"OK {name}: {len(raw)} bytes html, {len(text)} chars text")
        for needle in NEEDLES[name]:
            hit = needle.lower() in text.lower()
            print(f"  needle '{needle}': {'HIT' if hit else 'MISS'}")
            if not hit:
                fails += 1
    # Programm-ID-Kontextschnipsel fuer Belegfuehrung
    for name in ("hiro-lift", "pflegehase-hausnotruf"):
        f = OUT / f"{name}-061126.txt"
        if f.exists():
            t = f.read_text(encoding="utf-8")
            for pat in (r".{80}Provision.{160}", r".{60}Cookie.{160}", r".{60}Freigabe.{140}", r".{80}SEM.{140}", r".{60}werbemittel.{140}"):
                m = re.search(pat, t, flags=re.I)
                if m:
                    print(f"CTX {name}: …{m.group(0)}…")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
