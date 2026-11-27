#!/usr/bin/env python3
"""Tabellenbreiten-Messung NDS vs. Hessen bei 900px + 1200px (Scroll-Container-Frage)."""
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent

def measure(path, label):
    with sync_playwright() as p:
        b = p.chromium.launch()
        rows = []
        for w in (900, 1200):
            d = b.new_page(viewport={'width': w, 'height': 1000})
            d.goto(path.as_uri())
            d.wait_for_load_state('load')
            d.wait_for_timeout(200)
            m = d.evaluate("""() => {
              return [...document.querySelectorAll('.table-scroll')].map(t => {
                const inner = t.querySelector('table');
                return {container: Math.round(t.getBoundingClientRect().width),
                        inner: inner ? Math.round(inner.getBoundingClientRect().width) : null,
                        scrollable: inner ? inner.getBoundingClientRect().width > t.clientWidth + 1 : false};
              });
            }""")
            rows.append((w, m))
            d.close()
        b.close()
    print(label, rows)

measure(ROOT / 'dist/region/niedersachsen.html', 'NDS:')
measure(ROOT / 'dist/region/hessen.html', 'Hessen:')
