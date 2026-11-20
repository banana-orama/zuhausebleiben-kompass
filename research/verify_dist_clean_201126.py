#!/usr/bin/env python3
"""Verify dist-Clean in generate.mjs (2026-11-20, paare-Orphan-Fix).

Fall 1: Eine planted Stale-Datei im DIST_DIR wird vom Build gelöscht (Orphan-Fehlerklasse).
Fall 2: DIST_DIR='.' (Repo-Root) bricht kontrolliert ab, statt zu löschen.
Fall 3: Vollständiger LAUNCH-Chain (generate + checklists) produziert konsistenten dist-Baum.
"""
import os, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIX = "dist-cleanfix-tmp"
fails = []

def check(name, ok, detail=""):
    print(("PASS" if ok else "FAIL"), name, detail)
    if not ok:
        fails.append(name)

def run_generate(dist_name, index=False, expect_fail=False):
    env = dict(os.environ)
    env["DIST_DIR"] = dist_name
    cmd = ["node", "generate.mjs"] + (["--index"] if index else [])
    r = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True, timeout=180)
    if expect_fail:
        return r
    if r.returncode != 0:
        print(r.stdout[-1500:]); print(r.stderr[-1500:])
        sys.exit(1)
    return r

try:
    # --- Fall 1: Stale-Datei wird weggeräumt ---
    out = ROOT / FIX
    if out.exists():
        shutil.rmtree(out)
    (out / "irgendein-staler-ordner").mkdir(parents=True)
    (out / "stale-orphan.html").write_text("<html>stale orphan</html>", encoding="utf-8")
    (out / "irgendein-staler-ordner" / "stale.txt").write_text("stale", encoding="utf-8")
    run_generate(FIX)
    check("stale-orphan.html entfernt", not (out / "stale-orphan.html").exists())
    check("stale-Unterordner entfernt", not (out / "irgendein-staler-ordner").exists())
    check("index.html gebaut", (out / "index.html").exists())
    check("robots.txt gebaut", (out / "robots.txt").exists())
    check("assets/images vorhanden", (out / "assets" / "images").is_dir())
    check(".nojekyll vorhanden", (out / ".nojekyll").exists())
    home = (out / "index.html").read_text(encoding="utf-8")
    check("PREVIEW-Modus noindex", 'name="robots" content="noindex,follow"' in home)
    shutil.rmtree(out)
finally:
    if (ROOT / FIX).exists():
        shutil.rmtree(ROOT / FIX)

# --- Fall 2: Repo-Root-Guard ---
env = dict(os.environ); env["DIST_DIR"] = "."
r = subprocess.run(["node", "generate.mjs"], cwd=ROOT, env=env, capture_output=True, text=True, timeout=60)
check("DIST_DIR='.' bricht ab (Exit != 0)", r.returncode != 0)
check("Guard-Meldung erscheint", "Repo-Root" in (r.stderr + r.stdout))

# --- Fall 3: LAUNCH-Kette inkl. Checklisten, dann Inventar-Screening auf Stale ---
r = subprocess.run(["npm", "run", "build:launch"], cwd=ROOT, capture_output=True, text=True, timeout=300)
if r.returncode != 0:
    print(r.stdout[-1500:]); print(r.stderr[-1500:]); sys.exit(1)
dist = ROOT / "dist"
check("LAUNCH-Chain Exit 0", r.returncode == 0)
check("dist/checklisten existiert", (dist / "checklisten" / "index.html").exists())
sm = (dist / "sitemap.xml").read_text(encoding="utf-8")
check("Sitemap enthält Checklisten", "/checklisten/" in sm)
locs = sm.count("<loc>")
check(f"Sitemap 53 locs (ist {locs})", locs == 53)
check("keine dist-cleanfix-Reste", not any(p.name.startswith("stale") for p in dist.rglob("*")))
check("indexnow-key.txt vorhanden", (dist / "indexnow-key.txt").exists())
check("llms.txt vorhanden", (dist / "llms.txt").exists())
check("CNAME vorhanden", (dist / "CNAME").exists())
check("vendor-CMP vorhanden", (dist / "assets" / "vendor" / "cookieconsent.esm.js").exists())

print(f"\n{'ALL PASS' if not fails else str(len(fails)) + ' FAILS: ' + ', '.join(fails)}")
sys.exit(1 if fails else 0)
