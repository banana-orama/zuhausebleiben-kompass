# Key-Passagen aus den Badumbau-Kosten-Quellen anzeigen
import os, re
D = '/Users/mac/agentic-business/barrierefrei-leads/research/evidence/badumbau-kosten-171126'

QUERIES = {
    'badumbau-ratgeber': ['6.000 bis 12.000', 'Euro', 'Dusche', 'Fliesen', 'Haltegriff'],
    'pflegekompass': ['drei Dinge', 'Einzelpositionen', 'Steuervorteil', 'Euro', 'Selbst zu zahlen'],
    'kostenwelt': ['2.000', '25.000', 'Euro', 'Dusche'],
    'pflege-panorama': ['Kosten', 'Reihenfolge', 'Euro', 'Förderung', 'Dusche'],
    'konstruktionsfuhrer': ['DIN 18040', 'Euro', 'Kosten', 'Förderung'],
    'vz-handwerker': ['Festpreis', '20 Prozent', 'Kostenvoranschlag', 'nachträglich'],
    'kfw-455b': ['nicht mehr beantragen', '2027', 'Zuschuss'],
    'kfw-159': ['Altersgerecht', 'zinswerte', 'Darlehen', 'Maßnahmen'],
    'bauguru': ['13.000', '28.000', 'Euro', '6–8'],
    'badklar': ['12.000', '25.000', 'Euro', 'Dusche', 'Fliesen'],
    'estg-35a': ['Handwerkerleistungen', '20', '1.200', 'Arbeitskosten', 'Renovierung'],
    'sgb11-40': ['wohnumfeldverbessernden', '4 180', '16 720', 'Ermessen', 'satzung'],
}

for src, pats in QUERIES.items():
    p = f'{D}/{src}.txt'
    if not os.path.exists(p):
        print(f'!! {src} fehlt'); continue
    txt = open(p, encoding='utf-8').read()
    lines = txt.split('\n')
    print(f'\n========== {src} ==========')
    seen = set()
    for pat in pats:
        for i, ln in enumerate(lines):
            if pat.lower() in ln.lower() and ln not in seen and len(ln) > 30:
                seen.add(ln)
                print(f'  [{pat}] {ln[:280]}')
                if len(seen) > 26:
                    break
