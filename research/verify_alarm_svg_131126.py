#!/usr/bin/env python3
"""SVG-Geometrie-Check für hausnotruf-alarmkette (Briefing 26).

Lädt die SVG-Datei direkt (Renderer bettet sie als <img src> ein):
1. Alle <text>-Elemente bleiben innerhalb der viewBox (getBBox).
2. Pairwise-Überlappung: Texte untereinander (getBBox sieht element-on-element
   Overlap nicht, deshalb pairwise).
3. Text vs. kleine Chip-/Badge-Rechtecke.
4. Screenshot zur Sichtkontrolle (Vision-Probe).
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SVG = ROOT / "dist" / "assets" / "images" / "hausnotruf-alarmkette.svg"
SHOT = ROOT / "research" / "evidence" / "alarm-131126" / "svg-shot.png"

from playwright.sync_api import sync_playwright

FAIL = []
N = 0


def check(label, cond, detail=""):
    global N
    N += 1
    print(("PASS " if cond else "FAIL ") + label + ("" if cond else f"  {detail}"))
    if not cond:
        FAIL.append(label)


with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 900, "height": 700})
    pg.goto(SVG.as_uri())
    pg.wait_for_load_state("load")
    svg = pg.locator("svg").first
    svg.wait_for(state="visible", timeout=15000)

    boxes = pg.evaluate(
        """() => {
        const svg = document.querySelector('svg');
        const vb = svg.viewBox.baseVal;
        const out = {vb: {w: vb.width, h: vb.height}, texts: [], rects: []};
        svg.querySelectorAll('text').forEach(t => {
            const b = t.getBBox();
            out.texts.push({s: (t.textContent || '').slice(0, 40), x: b.x, y: b.y, w: b.width, h: b.height});
        });
        svg.querySelectorAll('rect').forEach((r, i) => {
            if (i === 0) return;  // Hintergrund
            const b = r.getBBox();
            out.rects.push({i, x: b.x, y: b.y, w: b.width, h: b.height});
        });
        return out;
    }"""
    )

    vbw, vbh = boxes["vb"]["w"], boxes["vb"]["h"]
    check(f"viewBox {vbw}x{vbh}", vbw == 1200 and vbh == 800, f"{vbw}x{vbh}")

    # 1. Texte innerhalb der viewBox
    for t in boxes["texts"]:
        inside = 0 <= t["x"] and t["x"] + t["w"] <= vbw and 0 <= t["y"] and t["y"] + t["h"] <= vbh
        check(f"getBBox inside: '{t['s'][:32]}' ({t['w']:.0f}x{t['h']:.0f})", inside,
              f"x={t['x']:.0f} y={t['y']:.0f}")

    # 2. Pairwise: Text vs. Text
    tol = 1.0
    n_text = len(boxes["texts"])
    overlaps = []
    for i in range(n_text):
        for j in range(i + 1, n_text):
            ta, tb = boxes["texts"][i], boxes["texts"][j]
            ox = min(ta["x"] + ta["w"], tb["x"] + tb["w"]) - max(ta["x"], tb["x"])
            oy = min(ta["y"] + ta["h"], tb["y"] + tb["h"]) - max(ta["y"], tb["y"])
            if ox > tol and oy > tol:
                overlaps.append((ta["s"][:24], tb["s"][:24], round(ox, 1), round(oy, 1)))
    check("pairwise Text-Text 0 Overlaps (Toleranz 1px)", not overlaps, str(overlaps[:6]))

    # 3. Text vs. Chip-Rechtecke (nur die kleinen Badge-Rects/Circles-Boxen < 400px Breite)
    chip_overlaps = []
    for t in boxes["texts"]:
        for r in boxes["rects"]:
            if r["w"] >= 150:
                continue  # Inhaltsboxen (340/546/1112px) enthalten Text bewusst; echte Badges sind 52px-Kreise
            ox = min(t["x"] + t["w"], r["x"] + r["w"]) - max(t["x"], r["x"])
            oy = min(t["y"] + t["h"], r["y"] + r["h"]) - max(t["y"], r["y"])
            if ox > tol and oy > tol:
                chip_overlaps.append((t["s"][:24], round(ox, 1), round(oy, 1)))
    check("Text vs. kleine Chip-Rects 0 Overlaps", not chip_overlaps, str(chip_overlaps[:6]))

    pg.set_viewport_size({"width": 1240, "height": 840})
    pg.wait_for_timeout(300)
    pg.screenshot(path=str(SHOT), full_page=False)
    print(f"Screenshot: {SHOT}")

print(f"\n{N - len(FAIL)}/{N} checks PASS")
sys.exit(1 if FAIL else 0)
