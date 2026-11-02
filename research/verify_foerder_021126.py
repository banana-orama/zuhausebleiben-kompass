#!/usr/bin/env python3
"""Förder-Prüflauf 02.11.2026: asserted jede im Live-Content zitierte Kernzahl
im heute (02.11.2026) abgerufenen Originaltext.

Quellen (Evidence: research/evidence/foerder-021126-*.html):
 - gesetze-im-internet.de/sgb_11/__40.html  (ISO-8859-1, Entities, geschützte Leerzeichen, U+00AD)
 - kfw.de 455-B / 159 (UTF-8, Soft-Hyphens U+00AD; 159 per 301 → trailing slash, kanonisch Umlaut+Slash)
 - bundesgesundheitsministerium.de zuschuesse-zur-wohnungsanpassung

Soft-Hyphens (U+00AD) werden vor dem Matching entfernt. Exit 1 bei fehlender Assertion.
"""
import html as htmllib
import re
import sys

EV = '/Users/mac/agentic-business/barrierefrei-leads/research/evidence'


def load_text(fname, charset):
    raw = open(f'{EV}/{fname}', 'rb').read()
    txt = raw.decode(charset, errors='replace')
    txt = htmllib.unescape(txt)
    txt = re.sub(r'<script[^>]*>.*?</script>', ' ', txt, flags=re.S | re.I)
    txt = re.sub(r'<style[^>]*>.*?</style>', ' ', txt, flags=re.S | re.I)
    txt = re.sub(r'<[^>]+>', ' ', txt)
    txt = txt.replace('\xa0', ' ').replace('\u202f', ' ').replace('\u00ad', '')
    txt = re.sub(r'\s+', ' ', txt)
    return txt


FAIL = []


def assert_in(label, needle, text, ctx_before=90, ctx_after=90):
    pos = text.find(needle)
    if pos < 0:
        FAIL.append(label)
        print(f'FAIL  {label}: NOT FOUND: {needle!r}')
        return
    a = max(0, pos - ctx_before)
    print(f'PASS  {label}')
    print(f'      …{text[a:pos + len(needle) + ctx_after]}…')


# ---------- § 40 SGB XI (ISO-8859-1) ----------
s40 = load_text('foerder-021126-sgb40.html', 'iso-8859-1')
print('=' * 90)
print('§ 40 SGB XI — gesetze-im-internet (Abruf 02.11.2026)')
print('=' * 90)
assert_in('§40 Abs.2 42-Euro-Grenze', 'den Betrag von 42 Euro nicht übersteigen', s40)
assert_in('§40 Abs.2 Kostenerstattung', 'Kostenerstattung', s40)
assert_in('§40 Abs.3 zehn vom Hundert', 'zehn vom Hundert', s40)
assert_in('§40 Abs.3 25-Euro-Deckel', 'höchstens jedoch 25 Euro je Pflegehilfsmittel', s40)
assert_in('§40 Abs.4 subsidiär', 'subsidiär', s40)
assert_in('§40 Abs.4 Zweckformel', 'häusliche Pflege ermöglicht oder erheblich erleichtert', s40)
assert_in('§40 Abs.4 Selbständigkeit', 'selbständige Lebensführung des Pflegebedürftigen wiederhergestellt', s40)
assert_in('§40 Abs.4 4.180/Maßnahme', '4 180 Euro je Maßnahme', s40)
assert_in('§40 Abs.4 16.720 gesamt', '16 720 Euro', s40)
assert_in('§40 Abs.4 >4 anteilig', 'anteilig auf die Versicherungsträger', s40)
assert_in('§40 Abs.7 drei Wochen', 'drei Wochen', s40)
assert_in('§40 Abs.7 fünf Wochen', 'fünf Wochen', s40)
assert_in('§40 Abs.7 Genehmigungsfiktion', 'als genehmigt', s40)
assert_in('§40 Fußnote Betragsstand 1.1.2025', 'ab dem 1.1.2025', s40)

# ---------- KfW 455-B ----------
k455 = load_text('foerder-021126-kfw455b.html', 'utf-8')
print('=' * 90)
print('KfW 455-B — kfw.de (Abruf 02.11.2026)')
print('=' * 90)
assert_in('455-B Antragstopp', 'können Sie nicht mehr beantragen', k455)
assert_in('455-B Mittel ausgeschöpft', 'ausgeschöpft', k455)
assert_in('455-B laufende Anträge', 'Laufende Anträge nicht betroffen', k455)
assert_in('455-B Zusage reserviert', 'reserviert', k455)
assert_in('455-B 2027 Bundesmittel', '2027', k455)
assert_in('455-B nicht begonnen', 'noch nicht mit Ihrem Vorhaben begonnen', k455)

# ---------- KfW 159 (beide URL-Varianten nach Redirect-Kette) ----------
for variant in ('foerder-021126-kfw159.html', 'foerder-021126-kfw159-umlaut.html'):
    k159 = load_text(variant, 'utf-8')
    print('=' * 90)
    print(f'KfW 159 — kfw.de (Abruf 02.11.2026, {variant})')
    print('=' * 90)
    assert_in(f'{variant}: 159 50.000/WE', '50.000 Euro', k159)
    assert_in(f'{variant}: 159 Wohneinheit', 'Wohneinheit', k159)
    assert_in(f'{variant}: 159 Haushaltsvorbehalt', 'Vorbehalt verfügbarer Haushaltsmittel', k159)
    assert_in(f'{variant}: 159 kein Rechtsanspruch', 'Rechtsanspruch', k159)
    assert_in(f'{variant}: 159 Fachunternehmen', 'Fachunternehmen', k159)
    assert_in(f'{variant}: 159 vor Vertragsabschluss', 'vor dem Abschluss', k159)
    assert_in(f'{variant}: 159 Treppenlifte', 'Treppenlifte', k159)
    assert_in(f'{variant}: 159 Kombination ausgeschlossen', 'Kombination der Förderungen für die gleiche Maßnahme ist nicht möglich', k159)
    assert_in(f'{variant}: 159 Nachfinanzierung ausgeschlossen', 'Nachfinanzierung', k159)
    print('info  159 Zinssatz 2,19 im KfW-Text:', '2,19' in k159)
    print('info  159 angezeigter Zinssatz laut KfW ("ab -,-- %"):', 'ab -,-- %' in k159)

# ---------- BMG Zuschüsse Wohnungsanpassung ----------
bmg = load_text('foerder-021126-bmg-zuschuss.html', 'utf-8')
print('=' * 90)
print('BMG Zuschüsse zur Wohnungsanpassung (Abruf 02.11.2026)')
print('=' * 90)
assert_in('BMG 4.180', '4.180 Euro', bmg)
assert_in('BMG 16.720', '16.720 Euro', bmg)
assert_in('BMG PG 1-5', 'Pflegegrade 1 bis 5', bmg)
assert_in('BMG Zweitzuschuss', 'zweites Mal', bmg)
print('info  BMG 2.090 Wohngemeinschaft:', '2.090' in bmg)
pos = bmg.find('2,19')
if pos >= 0:
    print(f'info  BMG Zins-2,19-Kontext: …{bmg[max(0, pos - 220):pos + 220]}…')
else:
    print('FAIL-info  BMG Zins 2,19 NICHT mehr gefunden — offener Punkt aus 26.10. prüfen!')
    FAIL.append('BMG Zins 2,19 (offener Punkt 26.10.)')

print('=' * 90)
if FAIL:
    print(f'ERGEBNIS: {len(FAIL)} Assertion(s) FEHLGESCHLAGEN: {FAIL}')
    sys.exit(1)
print('ERGEBNIS: alle Assertionen PASS — Live-Content-Zahlen stimmen zum Quellenstand 02.11.2026.')
