# Exakte Quote-Strings fürs Ledger extrahieren (Portalquellen)
import os
D = '/Users/mac/agentic-business/barrierefrei-leads/research/evidence/badumbau-kosten-171126'
QUOTES = {
    'badumbau-ratgeber': [
        'kostet heute häufig 6.000 bis 12.000 Euro',
        'Umbau Badewanne zur Dusche',
        '15.000 bis 30.000',
        'Bereits mit wenigen 1.000 Euro',
    ],
    'konstruktionsfuhrer': [
        'bodengleiche Dusche kostet meist 3.000 bis 7.000 Euro',
        'Teilumbau bei 8.000 bis 15.000',
        'unverbindliche Richtwerte',
        'vermitteln keine Handwerksbetriebe',
    ],
    'kostenwelt': [
        'meist zwischen 15.000 € und 25.000 €',
        'um bis zu 20 Prozent nach oben oder unten abweichen',
        '3.000 – 6.000 €',
        '1.000 € bis 2.500 €',
        'Standardgrößen',
    ],
    'pflege-panorama': [
        'Light-Umbau ab 8.000 Euro',
        '60 bis 180 Euro pro Stück',
        'Aroundhome',
        'Förderanträge',
        'Asbest',
    ],
    'bauguru': [
        '13.000–28.000',
        '13.000 – 28.000',
        'Bodenablauf',
    ],
    'badklar': [
        '12.000 und 25.000',
        '10.000',
        '30.000',
    ],
    'pflegekompass': [
        'gibt es nicht',
        'Summe laut Angebot minus Zuschuss',
        'Der KfW-Kredit 159',
        'Duschhocker',
    ],
}
for src, pats in QUOTES.items():
    txt = open(f'{D}/{src}.txt', encoding='utf-8').read().replace('\u00ad', '')
    lines = [l.replace('\u00ad', '') for l in txt.split('\n')]
    print(f'\n===== {src} =====')
    for pat in pats:
        hits = [l for l in lines if pat in l]
        if hits:
            print(f'  [{pat}]')
            for h in hits[:2]:
                print(f'    {h[:330]}')
        else:
            print(f'  [{pat}] NICHT GEFUNDEN')
