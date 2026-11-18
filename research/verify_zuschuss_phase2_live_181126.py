#!/usr/bin/env python3
"""Live-Readback Phase-2 18.11.2026: 6 Seiten auf der oeffentlichen URL nach dem Deploy.
Pollt treppenlift-kosten bis der neue Inline-Money-Anchor live ist, dann alle Assertions."""
import subprocess
import sys
import time

BASE = "https://zuhausebleiben-kompass.de"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126.0 Safari/537.36"
fails, passes = [], []


def get(url):
    r = subprocess.run(["curl", "-sSL", "--fail", "-A", UA, url], capture_output=True, text=True, timeout=60)
    return r.returncode == 0, r.stdout


# 1. Deploy-Lag abwarten: Kosten-Seite traegt den neuen Inline-Anchor
poll_html = None
for attempt in range(10):
    ok, poll_html = get(f"{BASE}/treppenlift-kosten.html")
    if ok and "Der Betrag darf <a href=" in poll_html and "4.180 Euro je Maßnahme</a>" in poll_html:
        print(f"Neuer Inline-Anchor live nach Poll {attempt + 1}")
        break
    time.sleep(30)
if not poll_html or "4.180 Euro je Maßnahme</a>" not in poll_html:
    print("FAIL: neuer Inline-Anchor nach 5 min nicht live")
    sys.exit(2)


def check_page(slug, name, needles, absents):
    ok, h = get(f"{BASE}/{slug}.html")
    if not ok:
        fails.append((f"{name}: fetch", slug, 0))
        return
    for n in needles:
        (passes if n in h else fails).append((f"{name}: '{n[:60]}'", 1 if n in h else 0, h.count(n)))
    for n in absents:
        (passes if n not in h else fails).append((f"{name}: absent '{n[:60]}'", 0 if n not in h else 1, h.count(n)))


# Money-Page: unslop-Zellen + Description live
check_page("treppenlift-zuschuss", "zuschuss", [
    '<meta name="robots" content="index,follow"',
    "Unterlagen prüfen. Mit Förder-Entscheidungshilfe",
    "Offen: Anträge sind jederzeit möglich",
    "Gestoppt: keine neuen Anträge",
    "Offen: Kredit über einen Finanzierungspartner",
], ["prüfen — mit", "Offen — Anträge", "Gestoppt — keine neuen Anträge", "Offen — Kredit"])

# Inline-Money-Anchor-Links
check_page("treppenlift-kosten", "kosten", [
    '<a href="https://zuhausebleiben-kompass.de/treppenlift-zuschuss.html">4.180 Euro je Maßnahme</a>',
], [])
check_page("treppenlift-mieten", "mieten", [
    '<a href="https://zuhausebleiben-kompass.de/treppenlift-zuschuss.html">der aktuelle Förderstatus</a>',
], [])

# CTA-Variationen (Label + Ziel, altes Label weg)
check_page("treppenlift-finanzierung", "finanzierung", [
    'href="https://zuhausebleiben-kompass.de/treppenlift-zuschuss.html" data-cta-id="compare_top"',
    "Zuschuss bis 4.180 Euro zuerst prüfen →",
], ["Förderung zuerst prüfen"])
check_page("treppenlift-angebote-vergleichen", "angebote-vergl", [
    "Zuschuss-Förderstatus prüfen →",
], ["Förderung prüfen →"])
check_page("treppenlift-steuerlich-absetzen", "steuer", [
    "Pflegekassen-Zuschuss prüfen →",
], ["Förderung prüfen →"])

# Site-Metrik unverändert
ok_s, sitemap = get(f"{BASE}/sitemap.xml")
locs = sitemap.count("<loc>")
(passes if ok_s and locs == 52 else fails).append(("sitemap-52", locs, ok_s))
ok_r, rss = get(f"{BASE}/rss.xml")
(passes if ok_r and rss.count("<item>") == 39 else fails).append(("rss-39", rss.count("<item>"), ok_r))

print()
for name, exp, got in fails:
    print(f"FAIL {name} expected={exp} got={got}")
print(f"{len(passes)} PASS / {len(fails)} FAIL")
sys.exit(1 if fails else 0)
