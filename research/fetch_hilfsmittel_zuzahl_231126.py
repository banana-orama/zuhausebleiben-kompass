#!/usr/bin/env python3
# 23.11.2026: Hilfsmittel-Zuzahlung § 61 SGB V — Live-Law-Text + GKV-SV-PM abrufen
# Prüffrage: trägt der LIVE-Text § 61 SGB V bereits 7,50/15 Euro (GKV-BStabG schon in Kraft)
# oder noch 5/10 Euro (Änderung zum 01.01.2027 ausstehend)?
import urllib.request, html, re, os, sys

OUT = os.path.join(os.path.dirname(__file__), "evidence", "hilfsmittel-zuzahl-231126")
os.makedirs(OUT, exist_ok=True)

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}

TARGETS = {
    "sgb5-61-231126.html": "https://www.gesetze-im-internet.de/sgb_5/__61.html",
    "sgb5-33-231126.html": "https://www.gesetze-im-internet.de/sgb_5/__33.html",
    "gkvsp-pm-2293952-231126.html": "https://www.gkv-spitzenverband.de/gkv_spitzenverband/presse/pressemitteilungen_und_statements/pressemitteilung_2293952.jsp",
}

def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=45) as r:
        data = r.read()
        return r.status, data

def clean(data):
    raw = data.decode("iso-8859-1", errors="replace")
    txt = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S | re.I)
    txt = re.sub(r"<[^>]+>", " ", txt)
    txt = html.unescape(txt).replace("\xa0", " ")
    txt = re.sub(r"\s+", " ", txt)
    return txt

status_report = {}
for fn, url in TARGETS.items():
    try:
        st, data = fetch(url)
        open(os.path.join(OUT, fn), "wb").write(data)
        status_report[fn] = (st, len(data))
    except Exception as e:
        status_report[fn] = ("ERR", str(e))
        sys.exit(f"FETCH FAILED: {url}: {e}")

t61 = clean(open(os.path.join(OUT, "sgb5-61-231126.html"), "rb").read())
t33 = clean(open(os.path.join(OUT, "sgb5-33-231126.html"), "rb").read())
tpm = clean(open(os.path.join(OUT, "gkvsp-pm-2293952-231126.html"), "rb").read())

print("=== STATUS ===")
for k, v in status_report.items():
    print(f"  {k}: {v}")

print("\n=== § 61 SGB V (live, decoded) — Zuzahlungs-Sätze ===")
idx = t61.find("Zuzahlung")
print(t61[max(0, idx - 100): idx + 2200] if idx >= 0 else "NO 'Zuzahlung' FOUND — head:\n" + t61[:800])

print("\n=== § 61 Needles (live text) ===")
for n in ["mindestens 5 Euro", "höchstens 10 Euro", "mindestens 7,50 Euro", "höchstens 15 Euro",
          "5 Euro", "10 Euro", "7,50", "15 Euro", "zum Verbrauch bestimmte", "Volljährige"]:
    print(f"  '{n}': {t61.count(n)}")

print("\n=== § 33 SGB V Abs. 1 (Hilfsmittel-Definition, kurz) ===")
i33 = t33.find("(1)")
print(t33[i33: i33 + 900] if i33 >= 0 else t33[:800])

print("\n=== GKV-SV PM — Zuzahlungs-Passagen ===")
for m in re.finditer(r'.{200}?(?:Zuzahlung|ab 2027).{300}', tpm):
    print("  …" + m.group(0) + "…")
    print("  ---")
