#!/usr/bin/env python3
# Ledger-Verify zuschuss-refresh 18.11.2026: alle Statusbehauptungen der neuen Ampel-Tabelle
# gegen heute abgerufene Originale (Evidenz research/evidence/zuschuss-refresh-181126/).
# Exit 0 = alle Pässe. ISO-8859-1-Pipeline für gesetze-im-internet, Soft-Hyphen-Normalisierung für KfW/NRW.BANK/StMB.
import re, html, sys
from pathlib import Path

D = Path(__file__).resolve().parent / 'evidence/zuschuss-refresh-181126'
fails = []
passes = []

def clean(p, iso=False):
    raw = p.read_bytes().decode('iso-8859-1') if iso else p.read_text(encoding='utf-8', errors='replace')
    txt = re.sub(r'<script.*?</script>', ' ', raw, flags=re.S)
    txt = re.sub(r'<style.*?</style>', ' ', txt, flags=re.S)
    txt = re.sub(r'<[^>]+>', ' ', txt)
    txt = html.unescape(txt).replace('\u00ad', '')
    return re.sub(r'\s+', ' ', txt)

def check(src, needle, text, min_count=1):
    n = text.count(needle)
    ok = n >= min_count
    (passes if ok else fails).append((src, needle[:80], n, ok))

sgb = clean(D / 'sgb11-40.html', iso=True)
check('sgb11-40', '4 180', sgb)
check('sgb11-40', '16 720', sgb)
check('sgb11-40', 'subsidiär', sgb)
check('sgb11-40', 'wohnumfeldverbessernden Maßnahmen', sgb)

k455 = clean(D / 'kfw-455b.html')
check('kfw-455b', 'Diesen Zuschuss können Sie nicht mehr beantragen', k455)
check('kfw-455b', 'ausgeschöpft', k455)
check('kfw-455b', '2027', k455)

k159 = clean(D / 'kfw-159.html')
check('kfw-159', '50.000 Euro', k159)
check('kfw-159', 'Die Arbeiten müssen von einem Fachunternehmen durchgeführt werden', k159)
check('kfw-159', 'Eigenleistungen sind nicht förderfähig', k159)
check('kfw-159', 'Die Förderung steht unter dem Vorbehalt verfügbarer Haushaltsmittel', k159)
check('kfw-159', 'Ein Rechtsanspruch hierauf besteht grundsätzlich nicht', k159)
check('kfw-159', 'Sprechen Sie vor dem Abschluss von Lieferungs- oder Leistungsverträgen oder dem Kaufvertrag mit einem Finanzierungspartner', k159)

nrw = clean(D / 'nrwbank-barrierefrei.html')
check('nrwbank', 'Eigentumsförderung - Modernisierung', nrw)
check('nrwbank', 'Zinsgünstige Darlehen bis 220.000 € mit einem Finanzierungsanteil von bis zu 100%', nrw)
check('nrwbank', 'Barrierefrei umbauen', nrw)

stmb = clean(D / 'stmb-bayern-barrierefrei.html')
check('stmb', 'leistungsfreien Baudarlehen von bis zu 10.000 Euro', stmb)
check('stmb', 'Landratsamt oder bei der kreisfreien Stadt', stmb)
check('stmb', 'Einkommensgrenzen', stmb)

for p in ['live-zuschuss.html', 'live-region-nrw.html', 'live-region-bayern.html']:
    t = clean(D / p)
    check(p, 'ZuhauseBleiben', t)

print(f"LEDGER: {len(passes)} PASS / {len(fails)} FAIL")
for src, needle, n, ok in passes + fails:
    if not ok:
        print(f"FAIL {src}: {needle!r} count={n}")
sys.exit(1 if fails else 0)
