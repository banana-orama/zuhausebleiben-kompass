#!/usr/bin/env python3
"""SVG-Geometrie-Check für treppenlift-aufmass-termin-ablauf (Briefing 25).

Lädt die SVG-Datei direkt (Renderer bettet sie als <img src> ein — die
Artikelseite enthält sie nicht inline):
1. Alle <text>-Elemente bleiben innerhalb der viewBox (getBBox).
2. Pairwise-Überlappung: Texte untereinander und Text vs. Chip-Rechteck
   (getBBox allein sieht element-on-element Overlap nicht).
3. Screenshot zur Sichtkontrolle (Vision-Probe manuell).
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SVG = ROOT / "dist" / "assets" / "images" / "treppenlift-aufmass-termin-ablauf.svg"
SHOT = ROOT / "research" / "evidence" / "aufmass-121126" / "svg-shot.png"

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
    pg = b.new_page(viewport={"width": 820, "height": 640})
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
    check(f"viewBox {vbw}x{vbh}", vbw == 780 and vbh == 570, f"{vbw}x{vbh}")

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

    # 3. Text vs. Chip-Rechtecke (nur die kleinen Chip-Rects < 300px Breite)
    chip_overlaps = []
    chips = [r for r in boxes["rects"] if r["w"] < 300]
    for r in chips:
        for t in boxes["texts"]:
            ox = min(r["x"] + r["w"], t["x"] + t["w"]) - max(r["x"], t["x"])
            oy = min(r["y"] + r["h"], t["y"] + t["h"]) - max(r["y"], t["y"])
            # Der Chip-Label-Text liegt IN seinem Rechteck — das ist erlaubt.
            inside_chip = t["x"] >= r["x"] - 2 and t["x"] + t["w"] <= r["w"] + r["x"] + 2 and \
                t["y"] >= r["y"] - 2 and t["y"] + t["h"] <= r["h"] + r["y"] + 2
            if ox > tol and oy > tol and not inside_chip:
                chip_overlaps.append((r["i"], t["s"][:24], round(ox, 1), round(oy, 1)))
    check(f"pairwise Text-Chip 0 Overlaps ({len(chips)} Chips)", not chip_overlaps, str(chip_overlaps[:6]))

    pg.screenshot(path=str(SHOT))
    print(f"Screenshot: {SHOT}")
    b.close()

print(f"\n{N - len(FAIL)}/{N} Pässe")
if FAIL:
    for f in FAIL:
        print(" -", f)
    sys.exit(1)
print("ALL PASS")
