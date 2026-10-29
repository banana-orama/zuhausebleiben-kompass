#!/usr/bin/env python3
"""Zitat-Link-Rot-Audit: alle externen Quellen-URLs aus dist/*.html extrahieren,
den Artikel zuordnen, dedupliziert auflisten."""
import json, re, glob, collections

def main():
    art2urls = collections.defaultdict(set)
    url2arts = collections.defaultdict(set)
    for path in sorted(glob.glob("dist/*.html")):
        slug = path.split("/")[-1].replace(".html", "")
        html = open(path, encoding="utf-8", errors="replace").read()
        # alle externen hrefs
        for href in re.findall(r'href="(https?://[^"]+)"', html):
            if "zuhausebleiben-kompass.de" in href:
                continue
            art2urls[slug].add(href)
            url2arts[href].add(slug)
    all_urls = sorted(url2arts)
    out = {
        "total_unique_urls": len(all_urls),
        "urls": [
            {"url": u, "articles": sorted(url2arts[u])} for u in all_urls
        ],
    }
    with open("research/linkrot-291026-urls.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("ARTIKEL:", len(art2urls))
    print("UNIQUE EXTERNE URLS:", len(all_urls))
    # Kurzliste
    for u in all_urls:
        print(f"{len(url2arts[u]):>2}  {u}")

if __name__ == "__main__":
    main()
