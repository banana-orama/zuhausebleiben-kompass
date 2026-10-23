#!/usr/bin/env python3
"""Print exact candidate quote strings from badumbau evidence txt files."""
import re, pathlib, json, sys

ev = pathlib.Path(__file__).resolve().parent / 'evidence' / 'partner-scan-badumbau-231026'

CANDIDATES = {
    'awin-aroundhome-68536.txt': [
        'Aroundhome DE ID | 68536',
        'Attributionszeitraum (Cookielaufzeit) 30 Tage',
        'Faire Lead-Provisionen mit Umsatzbeteiligung Cookie-Laufzeit: 30 Tage',
        'Sehr schnelle Validierung der Leads (durchschnittlich 8 Tage)',
        'Vergütung auf Basis einer Umsatzbeteiligung : Generieren wir Umsatz mit Ihrem Lead, erhalten Sie einen festen Prozentsatz davon (im Regelfall 30%)',
        'Nicht jeder eingegangene Lead generiert automatisch Umsatz!',
        'echte Kontaktdaten, keine doppelten und nur exklusive Anfragen, keine Testanfragen, keine Auslandsanfragen',
        'In unserem Partnerprogramm werden Ihre Leads in Echtzeit getrackt.',
        'aroundhome-all-aff-de@artefact.com',
        'affiliateprogramm@aroundhome.de',
        'Bis zu 3 individuelle Angebote von lokalen Firmen',
        'Heute erreichen das Unternehmen jeden Monat über 120.000 Kundenanfragen. Das Anbieternetzwerk umfasst über 16.000 Unternehmen in ganz Deutschland.',
    ],
    'aroundhome-badezimmer.txt': [
        'barrierefreien Badezimmerumbau? Schnell und unkompliziert zum passenden Fachbetrieb',
        'Experten finden und Angebot einholen',
        'Badewanne oder Dusche? Moderne Duschen sind oft ebenerdig und bieten barrierefreien Komfort',
        'barrierefreies Badezimmer ermöglicht maximale Selbstständigkeit und Komfort – unabhängig von körperlichen Einschränkungen',
    ],
    'aroundhome-home.txt': [
        'Beliebte Services Badezimmer Fenster Garage Heizung Immobilienverkauf Küche Solaranlage Terrassenüberdachung Treppenlift',
    ],
    'badumbauheld-partner.txt': [
        'Als Partnerbetrieb erhalten Sie qualifizierte Anfragen aus Ihrer Region, ohne Grundgebühr und ohne Klickkosten. Sie zahlen eine Provision nur, wenn aus der Anfrage ein Auftrag wird.',
        'Badumbauheld ist ein Vermittlungsservice. Wir leiten Anfragen an geprüfte Fachbetriebe weiter.',
    ],
    'seniovo-partner.txt': [
        'bereits über 500 vermittelte Kund:innen die große Kompetenz, Freundlichkeit & Kommunikation auf Augenhöhe des gesamten Seniovo-Teams',
    ],
    'hienergy-aroundhome-awin.txt': [
        'Aroundhome DE · Awin · CID 68536',
    ],
    'aroundhome-triplea.txt': [
        'Triple A from Artefact Germany GmbH is based on the easy.affiliate software from EASY Marketing GmbH',
    ],
    'ewerle-leadportale.txt': [
        'Leadportale kosten Handwerksbetriebe je nach Gewerk und Auftragsgröße zwischen 8 und 120 € pro Kundenanfrage.',
        'Aroundhome Festpreis je qualifizierter Anfrage Festpreis je Anfrage, produktabhängig, erst im Vertragsprozess einsehbar. Ausdrücklich keine Provision auf Ihren Projektumsatz max. 3 Fachpartner je Anfrage (Angabe des Anbieters) meist monatlich kündbar',
    ],
}

norm = lambda s: re.sub(r'\s+', ' ', s)
fails = 0
for fname, quotes in CANDIDATES.items():
    t = norm((ev / fname).read_text(errors='ignore'))
    print(f'== {fname} ==')
    for q in quotes:
        ok = norm(q) in t
        if not ok:
            fails += 1
            print(f'  MISS: {q[:80]}')
        else:
            print(f'  OK  : {q[:80]}')
print(f'\nFAILS: {fails}')
sys.exit(1 if fails else 0)
