#!/usr/bin/env python3
"""Build-Verifikation Checklisten/Launch: robots, sitemap, JSON-LD, RSS, llms.txt."""
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

root = Path(__file__).resolve().parent.parent
dist = root / "dist"
fails = []


def check(name, cond, detail=""):
    print(("PASS" if cond else "FAIL"), name, detail)
    if not cond:
        fails.append(name)


def robots(p):
    m = re.search(r'<meta name="robots" content="([^"]+)"', (dist / p).read_text())
    return m.group(1) if m else None


# LAUNCH build expected in dist right now
check("checklisten/index robots index", robots("checklisten/index.html") == "index,follow", robots("checklisten/index.html"))
check("checklisten sub robots index", robots("checklisten/tuerbreiten-schwellen-schnellcheck.html") == "index,follow")
check("homepage robots index", robots("index.html") == "index,follow")
check("no Vorschau prose on homepage", "als Vorschau" not in (dist / "index.html").read_text())
check("nav has Checklisten", "/checklisten/index.html" in (dist / "index.html").read_text())

# Sitemap: valid XML, includes all 7 checklist URLs exactly once
sm = (dist / "sitemap.xml").read_text()
ET.fromstring(sm)
locs = re.findall(r"<loc>([^<]+)</loc>", sm)
check_urls = [u for u in locs if "/checklisten/" in u]
check("sitemap has 7 checklist URLs", len(check_urls) == 7, str(len(check_urls)))
check("sitemap checklist URLs unique", len(set(check_urls)) == len(check_urls))
expected = {"/checklisten/index.html"} | {f"/checklisten/{s}.html" for s in [
    "pflegegrad-antrag-ablauf-fristen", "hilfsmittel-pflegekasse-uebernahme",
    "hausnotruf-kosten-anbieter-vergleich", "treppenlift-firmen-vergleich",
    "tuerbreiten-schwellen-schnellcheck", "badumbau-angebote-vergleichen"]}
have = {u.replace("https://zuhausebleiben-kompass.de", "") for u in check_urls}
check("sitemap checklist set exact", have == expected, str(have ^ expected))
check("draft not in sitemap", not any("treppenlift-angebote-vergleichen" in u for u in locs))

# JSON-LD on the overview parses with schema.org context
ld_text = re.search(r'<script type="application/ld\+json">(.*?)</script>',
                    (dist / "checklisten/index.html").read_text(), re.S).group(1)
ld = json.loads(ld_text)
check("JSON-LD context", ld.get("@context") == "https://schema.org", str(ld.get("@context")))
graph = ld.get("@graph", [])
check("JSON-LD CollectionPage+ItemList", [n.get("@type") for n in graph] == ["CollectionPage", "ItemList"])
check("JSON-LD 6 items", len(graph[1].get("itemListElement", [])) == 6)

# RSS: valid, new description, per-article items, no draft
rss = ET.parse(dist / "rss.xml")
items = rss.findall(".//item")
desc = rss.find(".//channel/description").text
check("rss new description", "im Aufbau. Noch keine" not in desc, desc[:50])
check("rss has 19 article items", len(items) == 19, str(len(items)))
check("rss no draft", not any("treppenlift-angebote-vergleichen" in (i.find("link").text or "") for i in items))
titles = [i.find("title").text for i in items]
check("rss includes briefing 9", any("Dusch-WC" in t for t in titles), str(len(titles)))

# llms.txt: all content-ready articles + legacy page, no draft
llms = (dist / "llms.txt").read_text()
ready = sorted(p.stem for p in (root / "content-ready").glob("*.json"))
missing = [s for s in ready if f"/{s}.html" not in llms]
check("llms covers all content-ready", not missing, str(missing))
check("llms legacy page", "/pflegegrad-beantragen.html" in llms)
check("llms no draft", "treppenlift-angebote-vergleichen" not in llms)

# Consent/no-loader contract on every checklist page
for s in ["index", "pflegegrad-antrag-ablauf-fristen", "hilfsmittel-pflegekasse-uebernahme",
          "hausnotruf-kosten-anbieter-vergleich", "treppenlift-firmen-vergleich",
          "tuerbreiten-schwellen-schnellcheck", "badumbau-angebote-vergleichen"]:
    html = (dist / "checklisten" / f"{s}.html").read_text()
    ok = ("window.gtag('consent', 'default'" in html
          and 'src="/assets/consent.mjs"' in html
          and "data-consent-settings" in html
          and "data-consent-withdraw" in html
          and not re.search(r"googletagmanager\.com|google-analytics\.com|stape\.io", html)
          and not re.search(r"<(?:script|iframe)[^>]+src=[\"']https?:", html))
    check(f"consent contract {s}", ok)

# Checklist content integrity: first bullet/header of each configured block is present
blocks_cfg = {
    "pflegegrad-antrag-ablauf-fristen": [["ol", 1], ["table", 2], ["ol", 3]],
    "hilfsmittel-pflegekasse-uebernahme": [["ol", 5], ["table", 2], ["table", 3]],
    "hausnotruf-kosten-anbieter-vergleich": [["ul", 5], ["table", 2]],
    "treppenlift-firmen-vergleich": [["table", 6], ["ol", 7], ["ul", 4]],
    "tuerbreiten-schwellen-schnellcheck": [["ul", 0], ["table", 2], ["ul", 6]],
    "badumbau-angebote-vergleichen": [["table", 2], ["ol", 7], ["ul", 0]],
}


def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"_{3,}", " ", s)).strip()


for slug, blocks in blocks_cfg.items():
    a = json.loads((root / "content-ready" / f"{slug}.json").read_text())
    html = norm(re.sub(r"<[^>]+>", "", (dist / "checklisten" / f"{slug}.html").read_text()))
    for t, sec in blocks:
        section = a["sections"][sec]
        if t in ("ol", "ul"):
            check(f"{slug} sec{sec} bullets", all(norm(b) in html for b in section["bullets"]))
        else:
            flat = [c for row in section["table"]["rows"] for c in row]
            check(f"{slug} sec{sec} table", all(norm(c) in html for c in section["table"]["headers"] + flat))

print()
print("RESULT:", "ALL PASS" if not fails else f"{len(fails)} FAILS: {fails}")
sys.exit(1 if fails else 0)
