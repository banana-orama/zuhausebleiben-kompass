#!/usr/bin/env python3
"""Content-Gate zuschuss-refresh 18.11.2026 (LAUNCH-dist):
alle JSON-Keys der neuen Status-Sektion (Absätze, Tabellenkopf, 12 Zellen, Absatz nach der Tabelle),
Inline-Region-Links absolut, Quellen 6/7 gerendert, Quellenstand-Meta, Roboter, Absenzen.
Muster: verify_badumbau_kosten_171126.py (LAUNCH-dist, Strip-sup-Normalisierung)."""
import re, sys
from pathlib import Path

D = Path(__file__).resolve().parent.parent / 'dist/treppenlift-zuschuss.html'
h = D.read_text(encoding='utf-8')
plain = re.sub(r'<sup[^>]*>.*?</sup>', '', h, flags=re.S)  # Zitationen raus (Renderer-Anchor liegt IM sup)
plain = re.sub(r'<[^>]+>', ' ', plain)
plain = re.sub(r'\s+', ' ', plain)
fails, passes = [], []

def ok(name):
    passes.append(name)

def need(name, needle, text=h, min_count=1):
    if text.count(needle) >= min_count:
        ok(name)
    else:
        fails.append((name, needle[:90], text.count(needle)))

# 1. Neue Sektion komplett
need('heading-status', 'Förderstatus heute: Was ist beantragbar?')
need('status-intro-datum', 'beim direkten Abruf der verlinkten offiziellen Seiten am 18. November 2026', plain)
need('tbl-header-status', 'Status am 18.11.2026', plain)
need('cell-pflegekasse-status', 'Offen: Anträge sind jederzeit möglich', plain)
need('cell-455b-status', 'Gestoppt: keine neuen Anträge', plain)
need('cell-159-status', 'Offen: Kredit über einen Finanzierungspartner', plain)
need('cell-landes-status', 'Je Bundesland unterschiedlich', plain)
need('cell-455b-verbatim', 'Diesen Zuschuss können Sie nicht mehr beantragen', plain)
need('cell-159-bedingungen', 'Antrag vor dem Abschluss von Lieferungs- oder Leistungsverträgen', plain)
need('cell-159-haushalt', 'Vorbehalt verfügbarer Haushaltsmittel', plain)
need('cell-nrw-betrag', 'zinsgünstige Darlehen bis 220.000 Euro', plain)
need('cell-bayern-betrag', 'leistungsfreies Baudarlehen bis 10.000 Euro', plain)
need('para-after', 'Für Bundesländer ohne eigenen Ratgeber ist der bundesweite Weg über die Pflegekasse der verlässliche Startpunkt', plain)
need('cell-4180', 'Höchstbetrag 4.180 Euro je Maßnahme', plain)

# 2. Inline-Region-Links (absolut im LAUNCH-Build)
need('link-nrw-absolut', '<a href="https://zuhausebleiben-kompass.de/region/nordrhein-westfalen.html">NRW-Ratgeber ansehen</a>')
need('link-bayern-absolut', '<a href="https://zuhausebleiben-kompass.de/region/bayern.html">Bayern-Ratgeber ansehen</a>')

# 3. Quellen 6/7 + Zitationsanker
need('source-6-anchor', 'id="source-6"')
need('source-7-anchor', 'id="source-7"')
need('cite-6-ref', 'href="#source-6"', min_count=1)
need('cite-7-ref', 'href="#source-7"', min_count=1)
need('src-nrwbank-url', 'https://www.nrwbank.de/de/privatpersonen/wohneigentum-gestalten/barrierefrei-umbauen')
need('src-stmb-url', 'https://www.stmb.bayern.de/wohnen/wohnraum_nutzen/barrierefreieswohnen/')

# 4. Prosa-Datums-Konsistenz (455-B heute geprüft)
need('kfw-455-prosa-datum', 'Die KfW-Produktseite wurde am 18. November 2026 direkt abgerufen und geprüft', plain)
need('kfw-455-faq-datum', 'Beim direkten Abruf am 18. November 2026 lautete die KfW-Aussage', plain)
need('quellenstand', 'Quellenstand: 2026-11-18')

# 5. Struktur: 9 Abschnitts-Anker, Tabelle scrollbar
for i in range(1, 10):
    need(f'anchor-abschnitt-{i}', f'id="abschnitt-{i}"')
need('table-scroll-region', 'role="region" aria-label="Förderstatus heute: Was ist beantragbar? – Tabelle"')

# 6. Absenzen (Partner/Förder-Gesetzesschreibweise/Stale-Datum)
def absent(name, needle):
    if needle in h:
        fails.append((name, needle[:90], h.count(needle)))
    else:
        ok(name)

absent('absent-partner-placement', 'data-partner-placement')
absent('absent-sponsored', 'rel="sponsored"')
absent('absent-awin', 'awin1.com')
absent('absent-gesetz-schreibweise', '4 180')
absent('absent-stale-datum', '16. November 2026')

# 7. JSON-LD intakt (FAQPage + Article, parse-valide, Datum aktualisiert)
import json
schemas = []
for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, flags=re.S):
    try:
        schemas.append(json.loads(m.group(1)))
    except Exception as e:
        fails.append(('jsonld-parse', str(e)[:90], 0))
g = [n for s in schemas for n in s.get('@graph', [])]
types = {n.get('@type') for n in g}
if {'Article', 'FAQPage'} <= types:
    ok('jsonld-types')
else:
    fails.append(('jsonld-types', str(types), 0))
art = next((n for n in g if n.get('@type') == 'Article'), {})
if str(art.get('dateModified', '')).startswith('2026-11-18'):
    ok('jsonld-dateModified')
else:
    fails.append(('jsonld-dateModified', str(art.get('dateModified')), 0))
faq = next((n for n in g if n.get('@type') == 'FAQPage'), {})
faq_txt = json.dumps(faq, ensure_ascii=False)
if '16. November 2026' not in faq_txt and '18. November 2026' in faq_txt:
    ok('faq-schema-datum')
else:
    fails.append(('faq-schema-datum', 'stale or missing date', 0))

# 8. Robots LAUNCH
if '<meta name="robots" content="noindex' not in h:
    ok('robots-indexable')
else:
    fails.append(('robots-indexable', 'noindex found', 1))

print(f"CONTENT-GATE: {len(passes)} PASS / {len(fails)} FAIL")
for name, needle, n in fails:
    print(f"FAIL {name}: {needle!r} count={n}")
sys.exit(1 if fails else 0)
