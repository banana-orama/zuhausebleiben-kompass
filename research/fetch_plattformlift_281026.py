#!/usr/bin/env python3
"""Fetch Plattformlift source pages: raw HTML + cleaned TXT for ledger evidence."""
import re
import sys
import urllib.request
import html as htmlmod
from pathlib import Path

OUT = Path(__file__).parent / "evidence" / "plattformlift-281026"
OUT.mkdir(parents=True, exist_ok=True)

URLS = [
    ("personenaufzuege-kosten", "https://www.personenaufzuege.com/rollstuhllift/plattformlift/kosten/"),
    ("kostenwelt", "https://kostenwelt.de/plattformlift-kosten/"),
    ("treppenlifte-preise-magazin", "https://treppenlifte-preise.de/magazin/der-plattformlift/"),
    ("treppenlifto", "https://www.treppenlifto.de/plattformlifte-64.html"),
    ("seniorenrat", "https://www.seniorenrat.de/ratgeber/plattformlift/"),
    ("lehner-typen", "https://www.lehner-lifttechnik.com/plattformlift-kosten/"),
    ("bild", "https://www.bild.de/leben-im-alter/barrierefreies-wohnen/plattformlift"),
    ("treppenliftwissen", "https://www.treppenliftwissen.de/rollstuhllift/"),
]

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")


def clean(html_text: str) -> str:
    # drop script/style
    txt = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", html_text)
    txt = re.sub(r"(?is)<head[^>]*>.*?</head>", " ", txt)
    txt = re.sub(r"(?is)<[^>]+>", "\n", txt)
    txt = htmlmod.unescape(txt)
    txt = txt.replace("\u00ad", "").replace("\xa0", " ").replace("\u202f", " ").replace("\u2009", " ")
    lines = [re.sub(r"\s+", " ", ln).strip() for ln in txt.splitlines()]
    return "\n".join([ln for ln in lines if ln])


def main() -> int:
    ok, fail = [], []
    for name, url in URLS:
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": UA, "Accept": "text/html,application/xhtml+xml",
                "Accept-Language": "de-DE,de;q=0.9,en;q=0.5"})
            with urllib.request.urlopen(req, timeout=45) as r:
                raw = r.read().decode("utf-8", errors="replace")
                status = getattr(r, "status", 200)
            (OUT / f"{name}.html").write_text(raw, encoding="utf-8")
            (OUT / f"{name}.txt").write_text(clean(raw), encoding="utf-8")
            print(f"OK   {name} {status} {len(raw)} bytes")
            ok.append(name)
        except Exception as exc:
            print(f"FAIL {name} {type(exc).__name__}: {exc}")
            fail.append(name)
    print(f"done ok={len(ok)} fail={len(fail)}")
    return 0 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
