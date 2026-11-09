#!/usr/bin/env python3
"""Förder-Prüflauf 09.11.2026: asserted jede im Live-Content zitierte Kernzahl
im heute (09.11.2026) abgerufenen Originaltext.

Quellen (Evidence: research/evidence/foerder-091126-*.html):
 - gesetze-im-internet.de/sgb_11/__40.html  (ISO-8859-1, Entities, geschützte Leerzeichen, U+00AD)
 - kfw.de 455-B / 159 (UTF-8, Soft-Hyphens U+00AD; zitierte Formen seit 02.11. kanonikal)
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


def load_raw(fname):
    return open(f'{EV}/{fname}', 'rb').read().decode('utf-8', errors='replace')


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
s40 = load_text('foerder-091126-sgb11-40.html', 'iso-8859-1')
print('=' * 90)
print('§ 40 SGB XI — gesetze-im-internet (Abruf 09.11.2026)')
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
k455 = load_text('foerder-091126-kfw-455b.html', 'utf-8')
print('=' * 90)
print('KfW 455-B — kfw.de (Abruf 09.11.2026)')
print('=' * 90)
assert_in('455-B Antragstopp', 'können Sie nicht mehr beantragen', k455)
assert_in('455-B Mittel ausgeschöpft', 'ausgeschöpft', k455)
assert_in('455-B laufende Anträge', 'Laufende Anträge nicht betroffen', k455)
assert_in('455-B Zusage reserviert', 'reserviert', k455)
assert_in('455-B 2027 Bundesmittel', '2027', k455)
assert_in('455-B nicht begonnen', 'noch nicht mit Ihrem Vorhaben begonnen', k455)
# Kanonikal-Rückcheck: zitierte Form (Bestandsimmobilie, kein Slash-Hinterbei) muss self-canonical sein
canon455 = re.search(r'<link[^>]+rel="canonical"[^>]+href="([^"]+)"', load_raw('foerder-091126-kfw-455b.html'))
print(f'info  455-B canonical: {canon455.group(1) if canon455 else "KEIN canonical gefunden"}')

# ---------- KfW 159 (zitierte Kanonikalform Umlaut+Slash) ----------
k159 = load_text('foerder-091126-kfw-159.html', 'utf-8')
print('=' * 90)
print('KfW 159 — kfw.de (Abruf 09.11.2026, kanonikal Umlaut+Slash)')
print('=' * 90)
assert_in('159 50.000/WE', '50.000 Euro', k159)
assert_in('159 Wohneinheit', 'Wohneinheit', k159)
assert_in('159 Haushaltsvorbehalt', 'Vorbehalt verfügbarer Haushaltsmittel', k159)
assert_in('159 kein Rechtsanspruch', 'Rechtsanspruch', k159)
assert_in('159 Fachunternehmen', 'Fachunternehmen', k159)
assert_in('159 vor Vertragsabschluss', 'vor dem Abschluss', k159)
assert_in('159 Treppenlifte', 'Treppenlifte', k159)
assert_in('159 Kombination ausgeschlossen', 'Kombination der Förderungen für die gleiche Maßnahme ist nicht möglich', k159)
assert_in('159 Nachfinanzierung ausgeschlossen', 'Nachfinanzierung', k159)
print('info  159 Zinssatz 2,19 im KfW-Text:', '2,19' in k159)
print('info  159 angezeigter Zinssatz laut KfW ("ab -,-- %"):', 'ab -,-- %' in k159)
canon159 = re.search(r'<link[^>]+rel="canonical"[^>]+href="([^"]+)"', load_raw('foerder-091126-kfw-159.html'))
print(f'info  159 canonical: {canon159.group(1) if canon159 else "KEIN canonical gefunden"}')

# ---------- BMG Zuschüsse Wohnungsanpassung ----------
bmg = load_text('foerder-091126-bmg-wohnanp.html', 'utf-8')
print('=' * 90)
print('BMG Zuschüsse zur Wohnungsanpassung (Abruf 09.11.2026)')
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
print('ERGEBNIS: alle Assertionen PASS — Live-Content-Zahlen stimmen zum Quellenstand 09.11.2026.')
