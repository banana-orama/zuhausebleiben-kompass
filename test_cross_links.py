#!/usr/bin/env python3
"""Gate: Cross-/Related-Links.
Liest data/cross-links.json (dieselbe Quelle wie der Renderer) und prüft gegen den LAUNCH-Dist:
1. Jeder Artikel hat genau 3 Related-Links.
2. Whitelisted Cross-Ziele stehen vorne, in konfigurierter Reihenfolge.
3. Kein nicht-whitelisted Cross-Cluster-Paar (Cluster-Regel + Whitelist als einzige Ausnahme).
4. Config-Ziele existieren (kein toter Link, keine Selbst-Verlinkung).
Läuft gegen den dist-Stand an seiner Position in `npm test` (nach build:launch + test_site + test_articles).
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
DIST = ROOT / "dist"
CL = json.loads((ROOT / "data" / "cross-links.json").read_text(encoding="utf-8"))
LINKS = CL.get("links", {})

fails = []

def is_bad(s): return "bad" in s or "wanne" in s or "dusche" in s
def is_care(s): return bool(re.match(r"^(hausnotruf|pflegegrad|hilfsmittel|rollator|verhinderungspflege|tuerbreiten|beleuchtung)", s))
def is_lift(s): return s.startswith("treppenlift")
def cluster(s): return "bad" if is_bad(s) else "care" if is_care(s) else "lift"
def in_cluster(src, t):
    c = cluster(src)
    # Exakte Renderer-Regel: Bad-Pool schliesst treppenlift-zuschuss bewusst ein (Förderpfad), Care-Pool nicht.
    if c == "bad":
        return is_bad(t) or "zuschuss" in t
    if c == "care":
        return is_care(t)
    return is_lift(t)

articles = sorted(
    json.loads(p.read_text(encoding="utf-8"))["slug"]
    for p in (ROOT / "content-ready").glob("*.json")
    if json.loads(p.read_text(encoding="utf-8")).get("status") == "editorial-reviewed-preview"
)

# 4) Config-Integritaet
slug_set = set(articles)
for src, targets in LINKS.items():
    if src not in slug_set:
        fails.append(f"Config: unbekannter Quell-Slug {src}")
    for t in targets:
        if t not in slug_set:
            fails.append(f"Config: unbekanntes Ziel {src} -> {t}")
        if t == src:
            fails.append(f"Config: Selbst-Verlinkung {src}")

checked = 0
for slug in articles:
    path = DIST / f"{slug}.html"
    if not path.exists():
        fails.append(f"{slug}: dist/{slug}.html fehlt")
        continue
    html = path.read_text(encoding="utf-8")
    if 'class="related"' not in html:
        fails.append(f"{slug}: related-Sektion fehlt")
        continue
    start = html.index('class="related">')
    end = html.index("</section>", start)
    seg = html[start:end]
    rel = re.findall(r'href="(?:https://zuhausebleiben-kompass\.de/)?([a-z0-9-]+)\.html"', seg)
    checked += 1
    # 1) genau 3
    if len(rel) != 3:
        fails.append(f"{slug}: {len(rel)} Related-Links (erwartet 3): {rel}")
        continue
    # 2) Cross-Ziele vorne, in Reihenfolge
    expected = [t for t in LINKS.get(slug, []) if t in rel]
    for i, t in enumerate(expected):
        if rel[i] != t:
            fails.append(f"{slug}: Cross-Ziel {t} nicht an Position {i} (ist {rel[i]})")
    if expected and len(expected) < len(LINKS.get(slug, [])):
        fails.append(f"{slug}: Cross-Ziele unvollständig: {rel} vs. {LINKS.get(slug)}")
    # 3) Cluster-Regel mit Whitelist
    for t in rel:
        if not in_cluster(slug, t) and t not in LINKS.get(slug, []):
            fails.append(f"{slug}: nicht-whitelisted Cross-Cluster-Link -> {t}")

print(f"test_cross_links: {checked} Artikel geprüft, {len(LINKS)} Cross-Whitelist-Einträge")
if fails:
    print(f"FAIL ({len(fails)}):")
    for f in fails:
        print(" -", f)
    sys.exit(1)
print("PASS: 3 Related-Links je Artikel, Cross-Ziele vorne, keine ungewollten Cluster-Verstöße.")
