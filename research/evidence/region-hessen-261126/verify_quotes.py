#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quote-Fragment-Verifikation fuer data/region-hessen.json (26.11.2026).
Jedes geplante Verbatim-Fragment gegen das Live-Original (eigener Abruf).
Exit != 0 bei FAIL."""
import html as html_mod, os, re, subprocess, sys, tempfile, time, urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
P, F = 0, 0

def fetch(url, a=1):
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.read()
    except Exception:
        if a < 2:
            time.sleep(2); return fetch(url, a + 1)
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
    try: s = raw.decode("utf-8")
    except UnicodeDecodeError: s = raw.decode("latin-1")
    return clean(s)

def dehyph(s):
    # Zeilenumbruch-Hyphens zurueckrollen ("förde- rung" -> "förderung"); legitime
    # Konstruktionen ("lieferungs- und") bleiben: Stopword-Nachlauf wird nicht vereint
    return re.sub(r"([a-zäöüß])-\s+(?!(?:und|oder|der|die|das|bis|von|im|in|zu|auf)\b)([a-zäöüß])", r"\1\2", s)

def pdf_variants(url):
    raw = fetch(url); outs = []
    for mode in ([], ["-layout"], ["-raw"]):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            f.write(raw); p = f.name
        try:
            out = subprocess.run(["pdftotext", "-q"] + mode + [p, "-"], capture_output=True, timeout=120)
            t = out.stdout.decode("utf-8", "replace")
        finally: os.unlink(p)
        t = t.replace("\u00ad", "").replace("\u00a0", " ").replace("\u202f", " ")
        fl = re.sub(r"\s+", " ", t).lower()
        outs += [fl, dehyph(fl)]
    return outs

WIBANK = page("https://www.wibank.de/wibank/behindertengerechter-umbau-von-wohneigentum")
RL = pdf_variants("https://www.wibank.de/resource/blob/wibank/306346/39845aeb7d0d5a93fc4aa1b251a398e0/richtlinie-behindertengerechter-umbau-von-wohneigentum-data.pdf")
WIA = page("https://wohnen-im-alter.hessen.de/wohnberatung/finanzierung/soziale-wohnraumfoerderung")
VP_EGH = page("https://verwaltungsportal.hessen.de/leistung?leistung_id=L100001_8960876")
SOZ = page("https://soziales.hessen.de/leistungen-der-eingliederungshilfe-gemaess-sgb-ix")
LWV = page("https://www.lwv-hessen.de/leben-wohnen/wohnen/leistungen-fuer-wohnraum.html")
VP_PK = page("https://verwaltungsportal.hessen.de/leistung?leistung_id=B100019_581678")

def chk(label, cond):
    global P, F
    if cond: P += 1; print("PASS %s" % label)
    else: F += 1; print("FAIL %s" % label)

def inany(hays, n):
    return any(n in h for h in hays)

# --- WIBank Produktseite ---
chk("wb zuschuss-kopfzeile-satz", inany([WIBANK], "zuschuss bis max. 15.000 euro für selbstgenutzten wohnraum"))
chk("wb aufzugsbeispiel-satz", inany([WIBANK], "einbau von geeigneten aufzügen (z.b. treppenschrägaufzug)"))
chk("wb foerderstelle-satz", inany([WIBANK], "bei der wohnungsbauförderstelle des kreises oder der kreisfreien stadt"))
chk("wb bad-kueche-5.500", inany([WIBANK], "5.500 euro"))
chk("wb lift-6.500-wort", inany([WIBANK], "aufzugseinbau 6.500 euro"))
chk("wb sonstige-3.000", inany([WIBANK], "3.000 euro"))
chk("wb unter-1.500", inany([WIBANK], "1.500 euro"))

# --- Richtlinie ---
chk("rl 30.000-satz", inany(RL, "förderfähig sind ausgaben in höhe von bis zu 30.000 euro je wohneinheit"))
chk("rl 15.000-satz", inany(RL, "dies entspricht einem zuschuss in höhe von maximal 15.000 euro je wohneinheit"))
chk("rl 50-prozent-satz", inany(RL, "nicht rückzahlbarer zuschuss in höhe von bis zu 50 prozent der zuwendungsfähigen ausgaben"))
chk("rl unter-1.500-satz", inany(RL, "maßnahmen mit ausgaben in höhe von unter 1.500 euro werden nicht gefördert"))
chk("rl bearbeitungsentgelt", inany(RL, "bearbeitungsentgelt von 1 prozent") and inany(RL, "mindestens jedoch 25 euro"))
chk("rl auszahlung-summe", inany(RL, "der zuschuss wird in einer summe nach abschluss der maßnahmen"))
chk("rl keine-auftraege-vor-bewilligung", inany(RL, "vor bewilligung"))
chk("rl vorhabensbeginn-lv-satz", inany(RL, "als vorhabenbeginn ist grundsätzlich der abschluss eines der ausführung zuzurechnenden lieferungs- und leistungsvertrages zu werten"))
chk("rl anrechnung-satz", inany(RL, "werden auf die zuwendungsfähigen ausgaben angerechnet"))
chk("rl dringlichkeit", inany(RL, "auswahl nach sozialer dringlichkeit"))
chk("rl din-satz", inany(RL, "nach möglichkeit den anforderungen der norm din 18040"))
chk("rl badewanne-dusche", inany(RL, "austausch der badewanne gegen eine dusche"))
chk("rl personenbezug-satz", inany(RL, "einstufung in den pflegegrad 2 oder höher"))

# --- wohnen-im-alter (Fachstelle) ---
chk("wia 5-jahres", inany([WIA], "innerhalb von fünf jahren"))
chk("wia 26-einheiten-oder-kreise", inany([WIA], "26") or inany([WIA], "landkreis"))

# --- VP EGH ---
chk("vp-egh lwv-satz", inany([VP_EGH], "für leistungen nach abschluss der schulausbildung ist der landeswohlfahrtverband hessen zuständig"))
chk("vp-egh fristen-wochen", inany([VP_EGH], "zwei wochen") or inany([VP_EGH], "3 wochen") or inany([VP_EGH], "drei wochen"))

# --- soziales.hessen.de EGH-Org ---
chk("soz 21-landkreise-wort", inany([SOZ], "21") or inany([SOZ], "landkreise"))

# --- LWV ---
chk("lwv treppenlift-satz", inany([LWV], "dies kann z. b. ein behindertengerechter bad- und/oder küchenumbau oder der einbau eines treppenlifts sein"))
chk("lwv vorrangig-satz", inany([LWV], "bevor leistungen der eingliederungshilfe bewilligt werden können, ist vorrangig zu klären"))

# --- VP Pflegekasse ---
chk("vp-pk treppenlift-beispiel-satz", inany([VP_PK], "das einbauen eines treppenlifts"))

print("\n== QUOTE-VERIFY: %d PASS, %d FAIL ==" % (P, F))
sys.exit(1 if F else 0)
