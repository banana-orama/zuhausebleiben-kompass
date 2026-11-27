#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Parent-Verifikation Region Niedersachsen (27.11.2026).
Jede Kernbehauptung der Region-Seite wird HIER frisch gegen das Live-Original
geprüft (eigener Abruf, nicht gegen die Screen-Rohdaten vom 26.11.).
Bereinigung: Tags strippen, Entities dekodieren, U+00AD/NBSP entfernen,
Whitespace normalisieren, case-normalisieren. PDFs in 3 pdftotext-Modi
(inkl. -raw gegen Spalten-Interleave) mit De-Hyphenation.
Exit != 0 bei FAIL."""
import html as html_mod
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}

PASSED = 0
FAILED = 0
FAILS = []


def fetch(url, attempt=1):
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.read()
    except Exception as e:
        if attempt < 2:
            time.sleep(2)
            return fetch(url, attempt + 1)
        raise


def clean(s):
    s = html_mod.unescape(s)
    s = re.sub(r"<script[\s\S]*?</script>", " ", s, flags=re.I)
    s = re.sub(r"<style[\s\S]*?</style>", " ", s, flags=re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = s.replace("\u00ad", "").replace("\u00a0", " ").replace("\u202f", " ")
    s = re.sub(r"\s+", " ", s)
    return s


def norm(s):
    return clean(s).lower()


def page_text(url):
    raw = fetch(url)
    try:
        s = raw.decode("utf-8")
    except UnicodeDecodeError:
        s = raw.decode("latin-1")
    return norm(s)


def dehyph(s):
    # Zeilenumbruch-Hyphens zurueckrollen; legitime Compound-Nachlaeufe bleiben
    return re.sub(r"([a-zäöüß])-\s+(?!(?:und|oder|der|die|das|bis|von|im|in|zu|auf)\b)([a-zäöüß])", r"\1\2", s)


def pdf_variants(url):
    """Zweispaltige PDFs: 3 pdftotext-Modi, je mit/ohne De-Hyphenation."""
    raw = fetch(url)
    outs = []
    for mode in ([], ["-layout"], ["-raw"]):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            f.write(raw)
            path = f.name
        try:
            out = subprocess.run(["pdftotext", "-q"] + mode + [path, "-"], capture_output=True, timeout=120)
            txt = out.stdout.decode("utf-8", "replace")
        finally:
            os.unlink(path)
        txt = txt.replace("\u00ad", "").replace("\u00a0", " ").replace("\u202f", " ")
        flat = re.sub(r"\s+", " ", txt).lower()
        outs.append(flat)
        outs.append(dehyph(flat))
    return outs


def check(label, cond, detail=""):
    global PASSED, FAILED
    if cond:
        PASSED += 1
        print("PASS %s" % label)
    else:
        FAILED += 1
        FAILS.append("%s %s" % (label, detail))
        print("FAIL %s %s" % (label, detail))


def anyv(variants, needle):
    return any(needle in v for v in variants)


def anycnt_raw(variants, word):
    # Counts nur auf Raw-Varianten (ohne Dehyph), Index 0/2/4
    return max(variants[i].count(word) for i in range(0, len(variants), 2))


# ---------- 1) NBank Produktseite ----------
try:
    t = page_text("https://www.nbank.de/F%C3%B6rderprogramme/Aktuelle-F%C3%B6rderprogramme/Eigentumsf%C3%B6rderung-(Selbst-genutztes-Wohneigentum).html")
    check("nbank-ps wartezeit-satz", anyv([t], "derzeit verzeichnen wir ein besonders hohes antragsaufkommen"))
    check("nbank-ps wartezeit-ende", anyv([t], "danken ihnen für ihre geduld und ihr verständnis"))
    check("nbank-ps programm-scope", anyv([t], "barrierereduzierende modernisierung"))
    check("nbank-ps foerderstelle", anyv([t], "wohnraumförderstelle (landkreis, stadt, gemeinde)"))
    check("nbank-ps treppenlift-absenz 0x", t.count("treppenlift") == 0, "count=%d" % t.count("treppenlift"))
except Exception as e:
    check("nbank-ps fetch", False, repr(e))

# ---------- 2) NBank Produktinfo PDF ----------
try:
    v = pdf_variants("https://www.nbank.de/medien/nb-media/Downloads/Programminformation/Produktinformationen/Produktinformation-Modernisierung-von-selbstgenutztem-Wohneigentum.pdf")
    check("pi 15.000-band", anyv(v, "barrierereduzierende modernisierung eines bestehenden gebäudes mit gesamtkosten von bis zu 15.000 euro"))
    check("pi eg-a-band", anyv(v, "einkommensgruppe a: bis zu 40 % der gesamtkosten, max. 6.000 euro"))
    check("pi eg-b+c-band", anyv(v, "einkommensgruppen b+c: bis zu 30 % der gesamtkosten, max. 4.500 euro"))
    check("pi darlehen-bindung", anyv(v, "ist die gewährung des zuschusses an die inanspruchnahme des darlehens gebunden"))
    check("pi kein-reiner-zuschuss-ab-15.001", anyv(v, "eine zuwendung ausschließlich in form des zuschusses bei diesen förderungen ist ausgeschlossen"))
    check("pi eigenmittel-satz", anyv(v, "die eigenmittel müssen 10 %, bei haushalten mit 2 oder mehr kindern sowie mit menschen mit behinderungen 7,5 %, der gesamtkosten"))
    check("pi vorhabensbeginn", anyv(v, "als vorhabenbeginn ist grundsätzlich der abschluss eines dem vorhaben zuzurechnenden lieferungs-, leistungs-, kauf- oder werkvertrages zu werten"))
    check("pi antrag-foerderstelle", anyv(v, "den antrag auf barrierereduzierende und/oder klimagerechte modernisierung selbstgenutzten wohneigentums stellen sie bitte bei der für ihren bauort zuständigen wohnraumförderstelle"))
    check("pi tragbarkeit 675", anyv(v, "675 euro"))
    check("pi tragbarkeit 600", anyv(v, "600 euro"))
    check("pi tragbarkeit 475", anyv(v, "475 euro"))
    check("pi tilgung 2%", anyv(v, "tilgung: 2%"))
    check("pi verwaltungskostenbetrag", anyv(v, "vom jeweiligen darlehensrestschuldbetrag"))
    check("pi bearbeitungsentgelt", anyv(v, "1 % des bewilligten darlehens und/oder 0,75 % des bewilligten zuschusses"))
    check("pi treppenlift-absenz 0x", anycnt_raw(v, "treppenlift") == 0, "count=%d" % anycnt_raw(v, "treppenlift"))
except Exception as e:
    check("produktinfo fetch", False, repr(e))

# ---------- 3) RL Wohneigentum 2026 PDF ----------
try:
    v = pdf_variants("https://www.nbank.de/medien/nb-media/Downloads/Rechtliche-Grundlagen/Richtlinien/Richtlinie-F%C3%B6rderung-von-selbst-genutztem-Wohneigentum-(RL-Wohneigentum-2026).pdf")
    check("rl zuwendungsart", anyv(v, "als ein anfänglich zinsloses, rückzahlbares darlehen und als ein nicht rückzahlbarer zuschuss"))
    check("rl anteilfinanzierung", anyv(v, "in form einer anteilsfinanzierung zur projektförderung gewährt"))
    check("rl ermessen", anyv(v, "ein anspruch auf gewährung einer zuwendung besteht nicht"))
    check("rl ermessen-forts", anyv(v, "pflichtgemäßen ermessens im rahmen der verfügbaren haushaltsmittel"))
    check("rl eg-b-40", anyv(v, "um bis zu 40 % überschreitet"))
    check("rl eg-c-60", anyv(v, "um bis zu 60 % überschreitet"))
    check("rl vorhabensbeginn-grundregel", anyv(v, "bereits begonnene vorhaben werden nicht gefördert"))
    check("rl vorhabensbeginn-lvkaufwerk", anyv(v, "lieferungs-, leistungs-, kauf- oder werkvertrages zu werten"))
    check("rl 100k-ausnahme", anyv(v, "von weniger als 100 000 eur ist der vorhabenbeginn ab antragstellung zugelassen"))
    check("rl barrieren-definition", anyv(v, "durch die baulichen maßnahmen muss eine verringerung bestehender barrieren erreicht werden"))
    check("rl definition-forts", anyv(v, "die zugänglichkeit, bewegungsfreiheit oder nutzbarkeit des wohnraums für die bewohnerinnen und bewohner verbessert"))
    check("rl eg-a-35%-17500", anyv(v, "35 % 17 500 eur") or anyv(v, "35 % 17 500 eur".replace(" ", " ")))
    check("rl eg-b+c-25%-12500", anyv(v, "25 % 12 500 eur"))
    check("rl darlehen 15j-0%", anyv(v, "für die dauer von 15 jahren zu einem zinssatz von 0 %"))
    check("rl 5-jahres-deckel", anyv(v, "endet der zuwendungszeitraum bei maßnahmen mit gesamtkosten bis 15 000 eur nach ablauf von fünf jahren"))
    check("rl auszahlung 30%", anyv(v, "bis zu 30 % nach beginn der baumaßnahme"))
    check("rl auszahlung 10%", anyv(v, "nach abschluss der modernisierungsmaßnahme und vorlage der schlussbescheinigung"))
    check("rl treppenlift-absenz 0x", anycnt_raw(v, "treppenlift") == 0, "count=%d" % anycnt_raw(v, "treppenlift"))
    check("rl rollstuhl-absenz 0x", anycnt_raw(v, "rollstuhl") == 0, "count=%d" % anycnt_raw(v, "rollstuhl"))
except Exception as e:
    check("rl fetch", False, repr(e))

# ---------- 4) GVBl NWoFG-Änderung 2025 ----------
try:
    v = pdf_variants("https://www.nbank.de/medien/nb-media/Downloads/Rechtliche-Grundlagen/Landesrecht/%C3%84nderung-NWoFG-(Nieders%C3%A4chsisches-Wohnraum-und-Wohnquartierf%C3%B6rdergesetz-)-%E2%80%93-g%C3%BCltig-ab-01.03.2025.pdf")
    check("gvbl titel", anyv(v, "gesetz zur änderung des niedersächsischen wohnraum- und wohnquartierfördergesetzes"))
    check("gvbl 30.01.2025", anyv(v, "vom 30. januar 2025"))
    check("gvbl 21.250", anyv(v, "21 250"))
    check("gvbl 28.750", anyv(v, "28 750"))
    check("gvbl 3.750", anyv(v, "3 750"))
    check("gvbl ersetzt-formel", anyv(v, "durch die angabe"))
    check("gvbl inkrafttreten", anyv(v, "tritt am ersten des monats"))
except Exception as e:
    check("gvbl fetch", False, repr(e))

# ---------- 5) DVO-NWoFG 2025 ----------
try:
    v = pdf_variants("https://www.nbank.de/medien/nb-media/Downloads/Rechtliche-Grundlagen/Richtlinien/DVO-NWoFG-Verordnung-zur-Durchf%C3%BChrung-des-Nieders%C3%A4chsischen-Wohnraum-und-Wohnraumquartierf%C3%B6rdergesetzes-(G%C3%BCltig-ab-01.09.2025).pdf")
    check("dvo freibetrag-titel", anyv(v, "verordnung zur durchführung des niedersächsischen wohnraum- und wohnquartierfördergesetzes"))
    check("dvo 4000-euro", anyv(v, "4 000 euro für jede dem haushalt angehörende person"))
    check("dvo gdb wenigstens 50", anyv(v, "grad der behinderung von wenigstens 50"))
    check("dvo pg-2-5", anyv(v, "pflegegrads 2, 3, 4 oder 5"))
    check("dvo deckel-pro-person", anyv(v, "höchstens 4 000 euro pro person"))
    check("dvo 40%-ueberschreitung", anyv(v, "um bis zu 40 prozent überschritten werden dürfen"))
    check("dvo inkrafttreten", anyv(v, "01. september 2025 in kraft"))
except Exception as e:
    check("dvo fetch", False, repr(e))

# ---------- 6) VV NWoFG ----------
try:
    v = pdf_variants("https://www.nbank.de/medien/nb-media/Downloads/Rechtliche-Grundlagen/Landesrecht/Verwaltungsvorschrift-zum-Vollzug-der-%C2%A7%C2%A7-5-und-7-bis-14-des-Nieders%C3%A4chsischen-Wohnraum-und-Wohnquartierf%C3%B6rdergesetzes-(VV-NWoFG).pdf")
    check("vv foerderstelle-definition", anyv(v, "der begriff wohnraumförderstelle bezeichnet die nach § 21 abs. 1 satz 1 nwofg zuständige stelle"))
    check("vv treppenlift-absenz 0x", anycnt_raw(v, "treppenlift") == 0, "count=%d" % anycnt_raw(v, "treppenlift"))
except Exception as e:
    check("vv fetch", False, repr(e))

# ---------- 7) NBank Beratungsstellen ----------
try:
    t = page_text("https://www.nbank.de/Service/Beratungssstellen/")
    check("nbank-beratung foerderstelle-hier", anyv([t], "ihre zuständige wohnraumförderstelle finden sie hier"))
    check("nbank-beratung kontaktdaten", anyv([t], "kontaktdaten von wohnraumförderstellen"))
except Exception as e:
    check("nbank-beratung fetch", False, repr(e))

# ---------- 8) NBank Investoren-Mietwohnungen PDF ----------
try:
    v = pdf_variants("https://www.nbank.de/medien/nb-media/Downloads/Programminformation/Produktinformationen/Produktinformation-Modernisierung-von-Mietwohnungen-in-Mehrfamilienh%C3%A4usern.pdf")
    check("investoren 5000-euro-satz", anyv(v, "zusätzliche zuschüsse in höhe von 5.000 euro für jede barrierefrei nutzbare wohnung gemäß din 18040-2"))
except Exception as e:
    check("investoren fetch", False, repr(e))

# ---------- 9) MW-Ministeriumsseite (nur Verweis + ALT-Dokumentation) ----------
try:
    t = page_text("https://www.mw.niedersachsen.de/startseite/bauen_wohnen/wohnraumforderung/eigentumsforderung/eigentumsforderung-217032.html")
    check("mw eigentumsfoerderung-verweis", anyv([t], "eigentumsförderung"))
    check("mw alt-marker-15prozent", anyv([t], "15 prozent der gesamtkosten"))
except Exception as e:
    check("mw fetch", False, repr(e))

# ---------- 10) soziales.niedersachsen.de EGH ----------
try:
    t = page_text("https://soziales.niedersachsen.de/startseite/menschen_mit_behinderungen/eingliederungshilfe/wie_erhalte_ich_leistungen/-200447.html")
    check("egh-traeger-satz", anyv([t], "zuständig für die leistungen der eingliederungshilfe sind in niedersachsen die kommunen"))
    check("egh-traeger-staedte", anyv([t], "die städte hannover, göttingen, hildesheim, lingen (ems) und lüneburg"))
    check("egh nur-auf-antrag", anyv([t], "leistungen der eingliederungshilfe erhalten sie nur auf antrag"))
    check("egh fristlos", anyv([t], "die antragstellung ist nicht an fristen gebunden"))
    check("egh monat-der-antragstellung", anyv([t], "erst beginnend mit dem monat der antragstellung"))
    check("egh treppenlift-absenz 0x", t.count("treppenlift") == 0, "count=%d" % t.count("treppenlift"))
except Exception as e:
    check("egh fetch", False, repr(e))

# ---------- 11) SPN-Förderseite ----------
try:
    t = page_text("https://soziales.niedersachsen.de/startseite/soziales_amp_gesundheit/soziale_forderungen/forderung_von_senioren_und_pflegestutzpunkten_niedersachsen_spn/forderung-von-senioren-und-pflegestutzpunkten-niedersachsen-spn-179120.html")
    check("spn flaechendeckend-satz", anyv([t], "daher fördert das land die einrichtung und den betrieb eines senioren- und pflegestützpunktes niedersachsen"))
    check("spn region-hannover-hannover-goettingen", anyv([t], "der region hannover, der landeshauptstadt hannover und der stadt göttingen"))
except Exception as e:
    check("spn fetch", False, repr(e))

# ---------- 12) Niedersachsenbüro Neues Wohnen (nichtamtlich) ----------
try:
    t = page_text("https://neues-wohnen-nds.de/wohnberatung/fachinformationen/foerdermoeglichkeiten/")
    check("nwb auslegung-komplett", anyv([t], "auch der badumbau und treppenlift, aber nicht der alleinige treppenlift"))
    check("nwb einzelfall-vorsatz", anyv([t], "gefördert wird, was über einzelmaßnahmen hinausgeht"))
    check("nwb eg-a-echo", anyv([t], "bis zu 40 % der gesamtkosten, max. 6.000 euro"))
    check("nwb treppenlift-count>=3", t.count("treppenlift") >= 3, "count=%d" % t.count("treppenlift"))
except Exception as e:
    check("nwb foerdermoeglichkeiten fetch", False, repr(e))
try:
    raw = fetch("https://neues-wohnen-nds.de/impressum/").decode("utf-8", "replace").lower()
    # Träger-Namen stehen in den IMG-ALT-Attributen der Träger-Logos (Screen-Befund 26.11.):
    # deshalb auf dem Roh-HTML prüfen, nicht auf dem getaggten Text.
    check("nwb-impressum traeger-satz", "träger des niedersachsenbüro neues wohnen im alter" in clean(raw))
    check("nwb-impressum fwg", "forum gemeinschaftliches wohnen" in raw)
    check("nwb-impressum bag", "bag wohnungsanpassung" in raw)
except Exception as e:
    check("nwb-impressum fetch", False, repr(e))

# ---------- 13) MS-Broschüre PDF ----------
try:
    v = pdf_variants("https://www.ms.niedersachsen.de/download/194009/Wohnen_im_Alter_-_AM_LIEBSTEN_ZU_HAUSE.pdf")
    check("ms-broschuere titel", anyv(v, "wohnen im alter am liebsten zu hause"))
    check("ms-broschuere treppenlift-satz", anyv(v, "können sie die treppe nicht mehr zu fuß überwinden, kann ein treppenlift helfen"))
    check("ms-broschuere pflegekasse-satz", anyv(v, "mit den wohnumfeldverbessernden maßnahmen gewährt ihnen die pflegekasse einen zuschuss"))
    check("ms-broschuere rampen-treppenlifte", anyv(v, "fest installierte rampen und treppenlifte"))
except Exception as e:
    check("ms-broschuere fetch", False, repr(e))

# ---------- 14) KfW ----------
try:
    t = page_text("https://www.kfw.de/inlandsfoerderung/Privatpersonen/Bestandsimmobilie/F%C3%B6rderprodukte/Altersgerecht-Umbauen-Investitionszuschuss-(455)/")
    check("kfw455 stopp-wortlaut", anyv([t], "diesen zuschuss können sie nicht mehr beantragen"))
    check("kfw455 2027-bedingung", anyv([t], "im jahr 2027 erneut bundesmittel"))
except Exception as e:
    check("kfw455 fetch", False, repr(e))
try:
    t = page_text("https://www.kfw.de/159")
    check("kfw159 treppenlifte-katalog", anyv([t], "treppenlifte, senkrecht-, hebe- oder plattformlifte installieren"))
    check("kfw159 50.000 je we", anyv([t], "50.000 euro je wohneinheit"))
    check("kfw159 kombi-ausnahme", anyv([t], "mit dem kredit der kfw gefördert werden"))
except Exception as e:
    check("kfw159 fetch", False, repr(e))

# ---------- 15) Gesetze (ISO-8859-1 + Entities) ----------
try:
    t = page_text("https://www.gesetze-im-internet.de/sgb_9_2018/__113.html")
    check("sgb9-113 wohnraum", anyv([t], "leistungen für wohnraum"))
except Exception as e:
    check("sgb9-113 fetch", False, repr(e))
try:
    t = page_text("https://www.gesetze-im-internet.de/sgb_9_2018/__77.html")
    check("sgb9-77 beschaffung-umbau", anyv([t], "beschaffung, den umbau, die ausstattung und die erhaltung"))
except Exception as e:
    check("sgb9-77 fetch", False, repr(e))
try:
    t = page_text("https://www.gesetze-im-internet.de/sgb_11/__40.html")
    check("sgb11-40 wohnumfeld", anyv([t], "wohnumfeldverbessernden maßnahmen"))
    check("sgb11-40 4180-geschützt", anyv([t], "4 180"), "kein '4 180' in normiertem Text")
    check("sgb11-40 16720-geschützt", anyv([t], "16 720"))
except Exception as e:
    check("sgb11-40 fetch", False, repr(e))
try:
    t = page_text("https://www.gesetze-im-internet.de/bgb/__554.html")
    check("bgb-554 enumeration", anyv([t], "barrierereduzierung, e-mobilität, einbruchsschutz und steckersolargeräte"))
    check("bgb-554 zumutbarkeitsgrenze", anyv([t], "nicht zugemutet werden kann"))
    check("bgb-554 gebrauch-behinderungen", anyv([t], "die dem gebrauch durch menschen mit behinderungen"))
except Exception as e:
    check("bgb-554 fetch", False, repr(e))

# ---------- Summary ----------
print("\n== PARENT VERIFY NDS: %d PASS, %d FAIL ==" % (PASSED, FAILED))
if FAILS:
    print("Fails:")
    for f in FAILS:
        print(" -", f)
sys.exit(1 if FAILED else 0)
