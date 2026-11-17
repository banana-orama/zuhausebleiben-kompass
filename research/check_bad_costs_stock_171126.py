# Bestands-Check: Wie viel Kosten-Coverage steckt in den 5 Bad-Cluster-Artikeln?
import json, glob, re

targets = ['bad-umbau-barrierefrei', 'badumbau-angebote-vergleichen',
           'bodengleiche-dusche-altbau', 'wanne-zur-dusche',
           'hilfsmittel-dusch-wc-uebernahme']

for slug in targets:
    d = json.load(open(f'content-ready/{slug}.json'))
    blob = json.dumps(d, ensure_ascii=False).lower()
    print(f"== {slug}")
    print("  title:", d.get('title'))
    for kw in ['kosten', 'euro', 'preise', 'budget']:
        print(f"  {kw}: {blob.count(kw)}")
