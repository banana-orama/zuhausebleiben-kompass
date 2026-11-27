#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quote-Fragment-Verifikation fuer data/region-niedersachsen.json (27.11.2026).
Jedes geplante Verbatim-Fragment des Content-JSON gegen das Live-Original
(eigener Abruf heute; Serviceportal-SPA-Extrakt aus dem Browser-Render heute).
Exit != 0 bei FAIL."""
import html as html_mod
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.request

EV = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
P, F = 0, 0


def fetch(url, a=1):
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.read()
    except Exception:
        if a < 2:
            time.sleep(2)
            return fetch(url, a + 1)
        raise


def clean(s):
    s = html_mod.unescape(s)
    s = re.sub(r"<script[\s\S]*?</script>", " ", s, flags=re.I)
    s = re.sub(r"<style[\s\S]*?</style>", " ", s, flags=re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = s.replace("\u00ad", "").replace("\u00a0", " ").replace("\u202f", " ")
    return re.sub(r"\s+", " ", s).lower()


def page(url):
    raw = fetch(url)
    try:
        s = raw.decode("utf-8")
    except UnicodeDecodeError:
        s = raw.decode("latin-1")
    return clean(s)


def dehyph(s):
    return re.sub(r"([a-zäöüß])-\s+(?!(?:und|oder|der|die|das|bis|von|im|in|zu|auf)\b)([a-zäöüß])", r"\1\2", s)


def pdf_variants(url):
    raw = fetch(url)
    outs = []
    for mode in ([], ["-layout"], ["-raw"]):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            f.write(raw)
            p = f.name
        try:
            out = subprocess.run(["pdftotext", "-q"] + mode + [p, "-"], capture_output=True, timeout=120)
            t = out.stdout.decode("utf-8", "replace")
        finally:
            os.unlink(p)
        t = t.replace("\u00ad", "").replace("\u00a0", " ").replace("\u202f", " ")
        fl = re.sub(r"\s+", " ", t).lower()
        outs += [fl, dehyph(fl)]
    return outs


NBANK_PS = page("https://www.nbank.de/F%C3%B6rderprogramme/Aktuelle-F%C3%B6rderprogramme/Eigentumsf%C3%B6rderung-(Selbst-genutztes-Wohneigentum).html")
PI = pdf_variants("https://www.nbank.de/medien/nb-media/Downloads/Programminformation/Produktinformationen/Produktinformation-Modernisierung-von-selbstgenutztem-Wohneigentum.pdf")
RL = pdf_variants("https://www.nbank.de/medien/nb-media/Downloads/Rechtliche-Grundlagen/Richtlinien/Richtlinie-F%C3%B6rderung-von-selbst-genutztem-Wohneigentum-(RL-Wohneigentum-2026).pdf")
INVEST = pdf_variants("https://www.nbank.de/medien/nb-media/Downloads/Programminformation/Produktinformationen/Produktinformation-Modernisierung-von-Mietwohnungen-in-Mehrfamilienh%C3%A4usern.pdf")
EGH = page("https://soziales.niedersachsen.de/startseite/menschen_mit_behinderungen/eingliederungshilfe/wie_erhalte_ich_leistungen/-200447.html")
SPN = page("https://soziales.niedersachsen.de/startseite/soziales_amp_gesundheit/soziale_forderungen/forderung_von_senioren_und_pflegestutzpunkten_niedersachsen_spn/forderung-von-senioren-und-pflegestutzpunkten-niedersachsen-spn-179120.html")
SPA = clean(open(os.path.join(EV, "serviceportal-nds-egh-8664328-rendered-271126.txt"), encoding="utf-8").read())
NWB = page("https://neues-wohnen-nds.de/wohnberatung/fachinformationen/foerdermoeglichkeiten/")
MS = pdf_variants("https://www.ms.niedersachsen.de/download/194009/Wohnen_im_Alter_-_AM_LIEBSTEN_ZU_HAUSE.pdf")
SGB113 = page("https://www.gesetze-im-internet.de/sgb_9_2018/__113.html")
SGB77 = page("https://www.gesetze-im-internet.de/sgb_9_2018/__77.html")
BGB554 = page("https://www.gesetze-im-internet.de/bgb/__554.html")
KFW455 = page("https://www.kfw.de/inlandsfoerderung/Privatpersonen/Bestandsimmobilie/F%C3%B6rderprodukte/Altersgerecht-Umbauen-Investitionszuschuss-(455)/")
KFW159 = page("https://www.kfw.de/159")


def chk(label, cond):
    global P, F
    if cond:
        P += 1
        print("PASS %s" % label)
    else:
        F += 1
        print("FAIL %s" % label)


def inany(hays, n):
    return any(n in h for h in hays)


# --- NBank Produktseite ---
chk("ps wartezeit-satz", inany([NBANK_PS], "derzeit verzeichnen wir ein besonders hohes antragsaufkommen. dadurch kann sich die bearbeitung ihres antrags leider etwas verzögern"))
chk("ps wartezeit-schluss", inany([NBANK_PS], "wir bearbeiten alle anträge so schnell wie möglich und danken ihnen für ihre geduld und ihr verständnis"))

# --- Produktinformation ---
chk("pi 15.000-band-fragment", inany(PI, "barrierereduzierende modernisierung eines bestehenden gebäudes mit gesamtkosten von bis zu 15.000 euro"))
chk("pi eg-a-fragment", inany(PI, "einkommensgruppe a: bis zu 40 % der gesamtkosten, max. 6.000 euro"))
chk("pi eg-b+c-fragment", inany(PI, "einkommensgruppen b+c: bis zu 30 % der gesamtkosten, max. 4.500 euro"))
chk("pi bindung-satz", inany(PI, "bei der barrierereduzierenden modernisierung mit gesamtkosten ab 15.001 euro und bei der klimagerechten modernisierung ist die gewährung des zuschusses an die inanspruchnahme des darlehens gebunden"))
chk("pi bindung-satz-forts", inany(PI, "eine zuwendung ausschließlich in form des zuschusses bei diesen förderungen ist ausgeschlossen"))
chk("pi 0%-15-jahre", inany(PI, "jahr 1–15: 0%") or inany(RL, "für die dauer von 15 jahren zu einem zinssatz von 0 %"))
chk("pi eigenmittel-fragment", inany(PI, "die eigenmittel müssen 10 %, bei haushalten mit 2 oder mehr kindern sowie mit menschen mit behinderungen 7,5 %, der gesamtkosten (z. b. bargeld, guthaben, sach- und arbeitsleistungen) betragen"))
chk("pi antrag-fragment", inany(PI, "den antrag auf barrierereduzierende und/oder klimagerechte modernisierung selbstgenutzten wohneigentums stellen sie bitte bei der für ihren bauort zuständigen wohnraumförderstelle (landkreis, stadt, gemeinde)"))

# --- RL Wohneigentum 2026 ---
chk("rl zuwendungsart-fragment", inany(RL, "als ein anfänglich zinsloses, rückzahlbares darlehen und als ein nicht rückzahlbarer zuschuss in form einer anteilsfinanzierung zur projektförderung gewährt"))
chk("rl ermessen-fragment", inany(RL, "ein anspruch auf gewährung einer zuwendung besteht nicht, vielmehr entscheidet die bewilligungsbehörde aufgrund ihres pflichtgemäßen ermessens im rahmen der verfügbaren haushaltsmittel"))
chk("rl vorhabensbeginn-fragment", inany(RL, "bereits begonnene vorhaben werden nicht gefördert. als vorhabenbeginn ist grundsätzlich der abschluss eines dem vorhaben zuzurechnenden lieferungs-, leistungs-, kauf- oder werkvertrages zu werten"))
chk("rl 100k-ausnahme-fragment", inany(RL, "bei maßnahmen mit im antrag zugrunde gelegten zuwendungsfähigen ausgaben von weniger als 100 000 eur ist der vorhabenbeginn ab antragstellung zugelassen"))
chk("rl barrieren-fragment", inany(RL, "durch die baulichen maßnahmen muss eine verringerung bestehender barrieren erreicht werden, die die zugänglichkeit, bewegungsfreiheit oder nutzbarkeit des wohnraums für die bewohnerinnen und bewohner verbessert"))
chk("rl auszahlung-30-fragment", inany(RL, "bis zu 30 % nach beginn der baumaßnahme"))
chk("rl auszahlung-10-fragment", inany(RL, "10 % nach abschluss der modernisierungsmaßnahme und vorlage der schlussbescheinigung"))

# --- Investoren-Produktinfo ---
chk("investoren 5000-fragment", inany(INVEST, "in höhe von 5.000 euro für jede barrierefrei nutzbare wohnung gemäß din 18040-2"))

# --- Landesamt für Soziales (EGH) ---
chk("egh traeger-fragment", inany([EGH], "zuständig für die leistungen der eingliederungshilfe sind in niedersachsen die kommunen, das heißt die landkreise, die kreisfreien städte, die region hannover, die städte hannover, göttingen, hildesheim, lingen (ems) und lüneburg"))
chk("egh nur-antrag-fragment", inany([EGH], "leistungen der eingliederungshilfe erhalten sie nur auf antrag"))
chk("egh fristlos-fragment", inany([EGH], "antragstellung ist nicht an fristen gebunden"))
chk("egh monat-fragment", inany([EGH], "erst beginnend mit dem monat der antragstellung"))

# --- Serviceportal (SPA-Render heute) ---
chk("spa vorrang-fragment", inany([SPA], "sofern sie die erforderliche leistung nicht von anderen sozialleistungs- oder rehabilitationsträgern"))
chk("spa vorrang-forts", inany([SPA], "erhalten"))
chk("spa kosten-traeger-fragment", inany([SPA], "die kosten für die leistungen übernimmt der zuständige träger"))
chk("spa beitrag-fragment", inany([SPA], "bei den leistungen der eingliederungshilfe müssen sie grundsätzlich einen beitrag aus ihrem einkommen sowie aus ihrem vermögen, sofern es eine festgesetzte grenze überschreitet, zahlen"))

# --- SPN ---
chk("spn flaechendeckend-fragment", inany([SPN], "daher fördert das land die einrichtung und den betrieb eines senioren- und pflegestützpunktes niedersachsen oder eines seniorenstützpunktes niedersachsen in jedem landkreis und jeder kreisfreien stadt sowie in der region hannover, der landeshauptstadt hannover und der stadt göttingen"))

# --- Niedersachsenbüro ---
chk("nwb auslegung-fragment", inany([NWB], "gefördert wird, was über einzelmaßnahmen hinausgeht und wird im einzelfall entschieden. ein badumbau oder die verbreiterung mehrerer türen wird gefördert, auch der badumbau und treppenlift, aber nicht der alleinige treppenlift"))

# --- MS-Broschüre ---
chk("ms pflegekasse-fragment", inany(MS, "mit den wohnumfeldverbessernden maßnahmen gewährt ihnen die pflegekasse einen zuschuss zu baulichen maßnahmen wie z.b. türverbreiterungen, badumbau oder fest installierte rampen und treppenlifte"))

# --- Gesetze ---
chk("sgb113 wohnraum-fragment", inany([SGB113], "leistungen für wohnraum"))
chk("sgb77 fragment", inany([SGB77], "die leistungen umfassen leistungen für die beschaffung, den umbau, die ausstattung und die erhaltung von wohnraum, der den besonderen bedürfnissen von menschen mit behinderungen entspricht"))
chk("bgb554 titel-fragment", inany([BGB554], "barrierereduzierung, e-mobilität, einbruchsschutz und steckersolargeräte"))
chk("bgb554 gebrauch-fragment", inany([BGB554], "die dem gebrauch durch menschen mit behinderungen"))
chk("bgb554 zumutung-fragment", inany([BGB554], "nicht zugemutet werden kann"))

# --- KfW ---
chk("kfw455 stopp-fragment", inany([KFW455], "diesen zuschuss können sie nicht mehr beantragen"))
chk("kfw455 2027-fragment", inany([KFW455], "sollten im jahr 2027 erneut bundesmittel für barrierereduzierende maßnahmen bereitgestellt werden, wird eine antragstellung wieder möglich sein"))
chk("kfw159 50000-fragment", inany([KFW159], "bis zu 50.000 euro je wohneinheit"))
chk("kfw159 katalog-fragment", inany([KFW159], "treppenlifte, senkrecht-, hebe- oder plattformlifte installieren"))
chk("kfw159 kombi-fragment", inany([KFW159], "ausnahme: wird eine maßnahme (z. b. badumbau) mit dem zuschuss der pflegeversicherung gefördert, können andere maßnahmen (z. b. treppenlift) mit dem kredit der kfw gefördert werden"))

print("\n== QUOTE-VERIFY NDS: %d PASS, %d FAIL ==" % (P, F))
sys.exit(1 if F else 0)
