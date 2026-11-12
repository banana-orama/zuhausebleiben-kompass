#!/usr/bin/env python3
"""Dehyphenation + Whitespace-Norm des Rahmenvertrags-14.-AendVb-PDF-Texts (wie Batch 19
drucksache-21-8869.norm.txt): 'Kranken-\nhaus' -> 'Krankenhaus', Zeilenumbrueche -> Leerzeichen."""
import re, pathlib
EVID = pathlib.Path('research/evidence/krankenhaus-121126')
t = (EVID / 'rahmenvertrag-14aendvb.txt').read_text(encoding='utf-8')
t = re.sub(r'(\w)-\n(\w)', r'\1\2', t)          # hartes Dehyphen an Zeilenumbruechen
t = re.sub(r'\s*\n\s*', ' ', t)                 # Zeilenumbrueche -> Leerzeichen
t = re.sub(r'\s+', ' ', t)
(EVID / 'rahmenvertrag-14aendvb.norm.txt').write_text(t, encoding='utf-8')
print(len(t), 'chars normalized')
