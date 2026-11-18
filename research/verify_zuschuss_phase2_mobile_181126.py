#!/usr/bin/env python3
"""Mobile-Check Phase-2 18.11.2026: 390px Overflow = 0 auf allen 6 berührten Seiten,
Screenshots (Money-Page Status-Tabelle, Finanzierung-CTA) für die Sichtkontrolle."""
import io
import pathlib
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "research/evidence/zuschuss-phase2-181126"
OUT.mkdir(parents=True, exist_ok=True)

PAGES = [
    "treppenlift-zuschuss",
    "treppenlift-kosten",
    "treppenlift-mieten",
    "treppenlift-finanzierung",
    "treppenlift-angebote-vergleichen",
    "treppenlift-steuerlich-absetzen",
]

fails = []
with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 390, "height": 844})
    for slug in PAGES:
        page.goto((ROOT / f"dist/{slug}.html").as_uri())
        page.wait_for_load_state("load")
        page.wait_for_timeout(300)
        m = page.evaluate(
            """() => {
              const d = document.documentElement;
              const overflow = Math.max(d.scrollWidth, document.body.scrollWidth) - d.clientWidth;
              const cta = document.querySelector('[data-cta-id="compare_top"]');
              const ctaRect = cta ? cta.getBoundingClientRect() : null;
              const inline = [...document.querySelectorAll('a[href*="treppenlift-zuschuss.html"]')]
                .filter(a => !a.closest('.related') && a.dataset.ctaId === undefined).length;
              return {overflow, ctaW: ctaRect ? Math.round(ctaRect.width) : null,
                      ctaRight: ctaRect ? Math.round(ctaRect.right) : null, inlineLinks: inline};
            }"""
        )
        ok = m["overflow"] == 0
        print(("PASS " if ok else "FAIL ") + f"{slug}: overflow={m['overflow']}px ctaW={m['ctaW']} inlineZuschussLinks={m['inlineLinks']}")
        if not ok:
            fails.append(slug)

    # Sichtkontrolle: Money-Page Sektion 2 + Finanzierung Early-CTA
    page.goto((ROOT / "dist/treppenlift-zuschuss.html").as_uri())
    page.wait_for_load_state("load")
    page.locator("#abschnitt-2").scroll_into_view_if_needed()
    page.wait_for_timeout(200)
    page.screenshot(path=str(OUT / "mobile-zuschuss-status-tabelle.png"))
    page.goto((ROOT / "dist/treppenlift-finanzierung.html").as_uri())
    page.wait_for_load_state("load")
    page.wait_for_timeout(200)
    page.screenshot(path=str(OUT / "mobile-finanzierung-cta.png"))
    b.close()

print()
print(f"{len(fails)} FAILS {fails}")
sys.exit(1 if fails else 0)
