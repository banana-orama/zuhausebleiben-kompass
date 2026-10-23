#!/usr/bin/env python3
"""Extract keyword-context quotes from badumbau partner-scan evidence HTML files."""
import re, html, pathlib, json, sys

d = pathlib.Path(__file__).resolve().parent  # research/

ev = d / 'evidence' / 'partner-scan-badumbau-231026'  # d = research/


def txt(f):
    h = (ev / f).read_text(errors='ignore')
    h = re.sub(r'<script[\s\S]*?</script>|<style[\s\S]*?</style>', ' ', h)
    t = re.sub(r'<[^>]+>', ' ', h)
    t = html.unescape(t)
    return re.sub(r'\s+', ' ', t)

for f, kws in [
    ('badumbauheld-partner.html', ['Vergütung', 'vergüt', 'Vermittlung', 'Partnerbetrieb', 'Handwerker', 'Affiliate', 'Publisher', 'Lead', 'Anfrage']),
    ('seniovo-partner.html', ['Vergüt', 'Partner', 'Fachpartner', 'Publisher', 'Affiliate', 'Vermittelt', 'Anfrage', 'Badumbau']),
    ('aroundhome-triplea.html', ['Affiliate', 'Partner', 'Cookie', 'Vergüt', 'easy.affiliate', 'Artefact']),
    ('hienergy-aroundhome-awin.html', ['commission', 'Awin', 'cookie', 'category', 'bathroom', 'Badezimmer', 'affiliate']),
]:
    t = txt(f)
    print(f'===== {f} ({len(t)} chars text) =====')
    for kw in kws:
        hits = list(re.finditer(re.escape(kw), t, re.I))
        if not hits:
            continue
        m = hits[0]
        s = max(0, m.start() - 140)
        print(f'  [{kw}] x{len(hits)} …{t[s:m.end() + 170]}…')
