#!/usr/bin/env python3
"""P1-Refresh 30.10.: Oeffentliche Partnerprofil-Readbacks ohne Login.
Prueft: Awin-Profil Malteser 112616 (1-EUR-Fenster bis 31.10. noch aktiv?),
Awin-Profil Lifta 40988 (50 EUR/Lead unverändert?), ADCELL HIRO 9440 (50 EUR/Lead).
Schreibt Rohdaten nach /tmp, extrahiert Keyword-Kontexte, KEINEContent-Aenderung."""
import re, html, urllib.request, sys

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"}

TARGETS = [
    ("malteser_112616", "https://ui.awin.com/merchant-profile/112616",
     ["1€", "1 €", "CPL", "31.10", "Oktober 2026", "Aktion", "Informationsmaterial",
      "Beratungstermin", "Cookie-Laufzeit", "Cookie", "Lead"]),
    ("lifta_40988", "https://ui.awin.com/merchant-profile/40988",
     ["50", "CPL", "Lead", "Cookie-Laufzeit", "30 Tage", "Auftrag", "500"]),
    ("hiro_adcell_9440", "https://www.adcell.de/partnerprogramme/hiro/",
     ["50", "Lead", "90", "Cookie", "SEM", "incentiviert", "DeepLink"]),
]

def strip_tags(t: str) -> str:
    t = re.sub(r"<script[^>]*>.*?</script>", " ", t, flags=re.S)
    t = re.sub(r"<style[^>]*>.*?</style>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    return re.sub(r"\s+", " ", t)

def main() -> int:
    rc = 0
    for name, url, kws in TARGETS:
        req = urllib.request.Request(url, headers=UA)
        try:
            raw = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
        except Exception as e:  # noqa: BLE001 - Report, nicht crashen
            print(f"== {name}: FETCH FAIL {e}")
            rc = 1
            continue
        path = f"/tmp/partner_{name}_301026.html"
        open(path, "w", encoding="utf-8").write(raw)
        text = strip_tags(raw)
        print(f"== {name}: HTTP OK, {len(raw)} bytes -> {path}")
        seen = set()
        for kw in kws:
            m = re.search(re.escape(kw), text, re.I)
            if not m:
                print(f"   [{kw}] ABSENT")
                continue
            s = max(0, m.start() - 100)
            snippet = text[s:m.end() + 120].strip()[:230]
            if snippet in seen:
                continue
            seen.add(snippet)
            print(f"   [{kw}] {snippet}")
    return rc

if __name__ == "__main__":
    sys.exit(main())
