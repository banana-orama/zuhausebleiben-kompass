#!/usr/bin/env python3
"""Deep-Greps: Netzwerk-Links (Pflegehase), Betreiber (hausnotruf.de), Acorn-Terms, Treppenlift-ME-Details."""
import re, pathlib

D = pathlib.Path(__file__).parent

def raw(name):
    b = (D / name).read_bytes()
    for enc in ("utf-8", "latin-1"):
        try:
            return b.decode(enc)
        except UnicodeDecodeError:
            continue
    return b.decode("utf-8", "replace")

print("== PFLEGEHASE: Anmelden-Hrefs + Netzwerk-Spalte ==")
h = raw("affmarketing-pflegehase.html")
for m in re.finditer(r'<a[^>]+href="([^"]+)"[^>]*>([^<]*Anmelden[^<]*|Anmelden)</a>', h):
    print("  href:", m.group(1))
for m in re.finditer(r'Netzwerk[^<]{0,200}', h):
    pass
# Netzwerk-Spalte: Tabellenzellen nach "Name & Netzwerk"
for m in re.finditer(r'Name &amp; Netzwerk:([^|<]{0,120})', h):
    print("  Netzwerkfeld:", m.group(1).strip()[:120])
# alle externen Netzwerk-Domains
for dom in sorted(set(re.findall(r'https?://([a-z0-9.-]+)\.([a-z]{2,})', h))):
    pass
for m in sorted(set(re.findall(r'href="https?://([^/"]+)"', h))):
    if "affiliate-marketing" not in m:
        print("  ext-link:", m)

print("\n== PFLEGEHASE: Pflegekasse-Zitat ==")
t = re.sub(r"<[^>]+>", " ", h)
t = re.sub(r"\s+", " ", t)
for m in re.finditer(r".{160}Pflegekasse.{200}", t):
    print("  ...", m.group(0), "...\n")

print("== HAUSNOTRUF.DE: Betreiber/Impressum ==")
h2 = raw("hausnotruf-de-partner.html")
t2 = re.sub(r"<[^>]+>", " ", h2); t2 = re.sub(r"\s+", " ", t2)
for k in ["in Zusammenarbeit", "Impressum", "GmbH", "e.V.", "Anschrift", "Straße", "Urheber", "Copyright", "©"]:
    for m in re.finditer(re.escape(k), t2):
        print(f"  [{k}] ...{t2[max(0,m.start()-120):m.start()+200]}...")
        break

print("\n== ACORN: Links/Terms-Seiten ==")
h3 = raw("acorn-de.html")
for m in sorted(set(re.findall(r'href="(/[^"]+|https?://[^"]+)"', h3))):
    print("  link:", m[:120])

print("\n== TREPPENLIFT-ME: Text mehr ==")
h4 = raw("treppenlift-me.html")
t4 = re.sub(r"<script[\s\S]*?</script>", " ", h4)
t4 = re.sub(r"<[^>]+>", " ", t4); t4 = re.sub(r"\s+", " ", t4)
for k in ["Auszahlung", "Abschluss", "Kontaktdaten", "Datenschutz", "Registrieren", "Cookie", "Domain"]:
    for m in re.finditer(re.escape(k), t4):
        print(f"  [{k}] ...{t4[max(0,m.start()-100):m.start()+250]}...")
        break

print("\n== AFFILITIZER SMARTVERSORGT: Addrevenue-Link ==")
h5 = raw("affilitizer-smartversorgt.html")
for m in sorted(set(re.findall(r'href="(https?://[^"]*addrevenue[^"]*)"', h5, re.I))):
    print("  ", m[:160])
