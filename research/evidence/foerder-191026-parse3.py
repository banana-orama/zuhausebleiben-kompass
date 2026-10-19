raw = open('foerder-191026-kfw-159.html', 'rb').read().decode('utf-8', errors='replace')
terms = ['Fachunternehmen', 'Nachfinanzierung', 'Rechtsanspruch', 'Haushaltsmittel',
         'Mindestanforderungen', 'Eigenleistung', 'Umschuldung', 'Vorbehalt']
for term in terms:
    print(term, '->', raw.count(term), 'x im Roh-HTML')

raw455 = open('foerder-191026-kfw-455b.html', 'rb').read().decode('utf-8', errors='replace')
print()
print('--- 455-B Roh-HTML ---')
for term in ['ausgeschöpft', '2027', 'reserviert', 'begonnen']:
    print(term, '->', raw455.count(term), 'x')

# Welcher Abschnitt der 159-Seite enthaelt die Förderbereiche/Ausschluesse (Kontext fuer Belegfuehrung)
import re
idx = raw.find('Förderbereich 3')
print()
print('Kontext Foerderbereich 3 (roh):')
print(re.sub(r'<[^>]+>', ' ', raw[idx-200:idx+400]).replace('&#160;', ' ')[:400])
