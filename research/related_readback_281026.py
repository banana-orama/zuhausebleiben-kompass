#!/usr/bin/env python3
"""Related-Sektionen der betroffenen Artikel aus dem LAUNCH-Dist drucken."""
import pathlib, re

D = pathlib.Path("/Users/mac/agentic-business/barrierefrei-leads/dist")
for slug in [
    "treppenlift-mietwohnung",
    "hausnotruf-kosten-anbieter-vergleich",
    "hausnotruf-sturzerkennung-oder-knopf",
    "pflegegrad-antrag-ablauf-fristen",
    "beleuchtung-orientierung-im-alter",
    "wanne-zur-dusche",
    "rollator-auswahl-passform-kosten",
    "treppenlift-schmale-treppe",
]:
    html = (D / f"{slug}.html").read_text(encoding="utf-8")
    i = html.index('class="related">')
    j = html.index("</section>", i)
    seg = html[i:j]
    rel = re.findall(r'href="(?:https://zuhausebleiben-kompass\.de/)?([a-z0-9-]+)\.html"', seg)
    print(f"{slug} -> {rel}")
