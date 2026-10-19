import re
t40 = open('foerder-191026-sgb11-40.txt').read()
print('Belastungsgrenze in §40 heute:', 'GEFUNDEN' if 'Belastungsgrenze' in t40 else 'NICHT GEFUNDEN')
i = t40.find('Belastungsgrenze')
if i >= 0:
    print('...', t40[max(0, i-220):i+160])
