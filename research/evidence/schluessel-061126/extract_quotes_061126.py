#!/usr/bin/env python3
"""Vollstaendige Saetze fuer verbatim-Quotes aus den Evidenz-Texten ziehen."""
import re, pathlib

D = pathlib.Path('research/evidence/schluessel-061126')
NEEDLES = {
 'vz-hausnotruf.txt': ['Schlüsselhinterlegung', 'Basistarif', 'ergänzende Leistungen', 'Vergleichen Sie', 'Kontrollrufe'],
 'malteser.txt': ['Bereitschaftsdienst', 'Wohnungsschlüssel', 'Sprechkontakt', 'auf Wunsch'],
 'easierlife.txt': ['drei gängig', 'Trotzdem', 'nicht inklusive', '35 bis 100 Euro', 'Zahlenkombination', 'Code des Schlüsseltresors', 'Nachbarn hinterlegen', 'Pflegedienst aufbewahren', 'Wohlfahrtsverband'],
 'pflegehelfer24.txt': ['15 Euro', 'Kombination', 'regelmäßig zu überprüfen', 'Sicherheits', 'Notrufzentrale', 'überschaubar'],
 'pflegeeinstieg.txt': ['am Handgelenk', 'von innen verriegelt', 'Ohne hinterlegten', 'demselben Gespräch', 'Code im Notfall', 'Kombiniere ruhig', 'Schlüsselsafe', 'Bereitschaftsdienst', 'Vollmacht', 'nachts'],
 'vz-schluesseldienst.txt': ['800 Euro', 'variieren', 'Tageszeit', 'Wochenend- und Nachtzuschläge', 'ortsansässige', 'Vorwahl'],
 'test-feuerwehr.txt': ['Faustregel', 'Staatskasse', 'Bundesland zu Bundesland', 'Gießen', '2 K 2103', 'spontan'],
 'haufe.txt': ['Hildburghausen', 'hinterlegten Schlüssel', '536a', 'gesundheitlichen Notfalls', '2957', 'Berlin-Mitte', 'Generalschlüssel'],
}
for fname, needles in NEEDLES.items():
    lines = [l.strip() for l in (D / fname).read_text(encoding='utf-8').split('\n') if l.strip()]
    print(f'===== {fname} =====')
    shown = set()
    for nd in needles:
        for l in lines:
            if nd in l and l not in shown and len(l) > 25:
                shown.add(l)
                print('  *', l[:400])
                break
