#!/usr/bin/env python3
"""Partner-Scan 23.10.: HTML-Evidenzdateien -> Text -> Konditions-Greps."""
import html.parser, re, sys, pathlib

class TextExtract(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript"):
            self.skip += 1
    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript") and self.skip:
            self.skip -= 1
    def handle_data(self, data):
        if not self.skip and data.strip():
            self.parts.append(data.strip())

def text_of(path):
    raw = pathlib.Path(path).read_bytes()
    for enc in ("utf-8", "latin-1"):
        try:
            s = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    p = TextExtract()
    p.feed(s)
    return re.sub(r"\s+", " ", " ".join(p.parts))

D = pathlib.Path(__file__).parent
KEY = {
    "awin-malteser-112616.html": ["112616", "CPL", "31.10.2026", "Informationsmaterial", "Beratungstermin", "Cookie", "paidmedia"],
    "awin-lifta-40988.html": ["40988", "Lead", "Auftrag", "Cookie", "Provision"],
    "affmarketing-pflegehase.html": ["Netzwerk", "Lead", "Hausnotru", "Provision", "Anmelden", "SEM"],
    "affmarketing-treppenlift-angebotsvergleich.html": ["Netzwerk", "Lead", "Provision", "Anmelden", "SEM", "Cookie"],
    "hausnotruf-de-partner.html": ["Provision", "Vergütung", "Lead", "Partner"],
    "acorn-de.html": ["Provision", "Treppenlift", "Vergütung", "Lead", "Stufe"],
    "treppenlift-me.html": ["250", "Provision", "Empfehlung", "Bedingungen", "Website"],
    "affilitizer-smartversorgt.html": ["Addrevenue", "Active", "Network", "988118"],
}
for name, keys in KEY.items():
    t = text_of(D / name)
    print(f"\n===== {name} ({len(t)} chars) =====")
    low = t.lower()
    for k in keys:
        idx = low.find(k.lower())
        if idx >= 0:
            print(f"  [{k}] ...{t[max(0,idx-140):idx+220]}...")
        else:
            print(f"  [{k}] NICHT GEFUNDEN")
