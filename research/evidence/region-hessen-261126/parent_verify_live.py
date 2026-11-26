#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Parent-Verifikation Region Hessen (26.11.2026).
Jede Kernbehauptung des Screen-Subagents wird HIER frisch gegen das Live-Original
geprüft (eigener Abruf, nicht gegen die Subagent-Rohdaten). Bereinigung: Tags
strippen, Entities dekodieren, U+00AD/NBSP entfernen, Whitespace normalisieren,
case-normalisieren (Vergleich klein). gesetze-im-internet antwortet ISO-8859-1.
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
    # Zeilenumbruch-Hyphens zurueckrollen ("förde- rung" -> "förderung");
    # nur fuer Needle-Suche, nie fuer Absenz/Counts (kollidiert mit "lieferungs- und")
    return re.sub(r"([a-zäöüß])-\s+(?=[a-zäöüß])", r"\1", s)


def pdf_norm_variants(url):
    """Zweispaltige PDFs: Raw- und Layout-Extrakt, jeweils mit/ohne De-Hyphenation.
    Liefert (alle_variants_fuer_has, raw_variants_fuer_counts)."""
    raw = fetch(url)
    outs = []
    for mode in ([], ["-layout"], ["-raw"]):  # -raw = Inhaltsstrom-Lesereihenfolge (heilt Spalten-Interleave)
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
    return outs, outs[0::2]


def check(label, cond, detail=""):
    global PASSED, FAILED
    if cond:
        PASSED += 1
        print("PASS %s" % label)
    else:
        FAILED += 1
        FAILS.append("%s %s" % (label, detail))
        print("FAIL %s %s" % (label, detail))


def has(t, needle):
    return needle in t


# ---------- 1) WIBank Produktseite ----------
try:
    t = page_text("https://www.wibank.de/wibank/behindertengerechter-umbau-von-wohneigentum")
    check("wibank produkt titel", has(t, "behindertengerechter umbau von wohneigentum"))
    check("wibank 15.000 kopfzeile", has(t, "15.000 euro"))
    check("wibank zuschuss-kopfzeile", has(t, "zuschuss"))
    check("wibank treppenlift-absenz 0x", t.count("treppenlift") == 0, "count=%d" % t.count("treppenlift"))
    check("wibank treppenschraegaufzug", has(t, "treppenschrägaufzug"))
    check("wibank din 18040", has(t, "din 18040"))
    check("wibank foerderstelle", has(t, "wohnungsbauförderstelle"))
except Exception as e:
    check("wibank produktseite fetch", False, repr(e))

# ---------- 2) Richtlinie PDF ----------
RL = "https://www.wibank.de/resource/blob/wibank/306346/39845aeb7d0d5a93fc4aa1b251a398e0/richtlinie-behindertengerechter-umbau-von-wohneigentum-data.pdf"
try:
    variants, raw_variants = pdf_norm_variants(RL)
    def anyv(needle):
        return any(has(v, needle) for v in variants)
    def anycnt(word):
        return max(v.count(word) for v in raw_variants)
    check("rl zuschuss nicht rueckzahlbar", anyv("nicht rückzahlbarer zuschuss"))
    check("rl 50 prozent anteilfinanzierung", anyv("50 prozent der zuwendungsfähigen ausgaben"))
    check("rl 30.000 euro je we", anyv("30.000 euro je wohneinheit"))
    check("rl 15.000 euro je we", anyv("15.000 euro je wohneinheit"))
    check("rl personenbezug gdb", anyv("grad der behinderung von 50 prozent"))
    check("rl personenbezug pg2", anyv("pflegegrad 2 oder höher"))
    check("rl einkommen-absenz 0x", anycnt("einkommen") == 0, "count=%d" % anycnt("einkommen"))
    check("rl anrechnung pflegekasse", anyv("pflegekasse"))
    check("rl anrechnung reduziert", anyv("reduziert"))
    check("rl rechtsanspruch-nein", anyv("rechtsanspruch auf gewährung der förderung besteht nicht"))
    check("rl vorhabensbeginn lv", anyv("lieferungs- und leistungsvertrages"))
    check("rl magistrat", anyv("magistrat"))
    check("rl kreisausschuss", anyv("kreisausschuss"))
    check("rl treppenlift-absenz 0x", anycnt("treppenlift") == 0, "count=%d" % anycnt("treppenlift"))
    check("rl plattformlift 1x", anycnt("plattformlift") == 1, "count=%d" % anycnt("plattformlift"))
    check("rl treppenschraegaufzug", anyv("treppenschrägaufzug"))
    check("rl badumbau", anyv("badumbau"))
    check("rl din 18040", anyv("din 18040"))
except Exception as e:
    check("richtlinie fetch", False, repr(e))

# ---------- 3) LWV Wohnraum ----------
try:
    t = page_text("https://www.lwv-hessen.de/leben-wohnen/wohnen/leistungen-fuer-wohnraum.html")
    check("lwv treppenlift-explicit", has(t, "einbau eines treppenlifts"))
    check("lwv bad-kueche-umbau", has(t, "bad- und/oder küchenumbau"))
    check("lwv subsidiaritaet", has(t, "vorrangig zu klären"))
    check("lwv wibank-prioritaet", has(t, "wirtschafts- und infrastrukturbank hessen"))
    check("lwv kostenbeteiligung-frage", has(t, "muss ich mich an den kosten beteiligen"))
except Exception as e:
    check("lwv fetch", False, repr(e))

# ---------- 4) Pflegestützpunkte ----------
try:
    t = page_text("https://www.pflege-in-hessen.de/beratung-und-information/pflegestuetzpunkte/")
    check("pst 26 stuetzpunkte", has(t, "26 pflegestützpunkte"))
    check("pst je kreis", has(t, "in jedem landkreis und in jeder kreisfreien stadt"))
    check("pst neutral", has(t, "neutral"))
    check("pst kostenlos", has(t, "kostenlos"))
except Exception as e:
    check("pflegestuetzpunkte fetch", False, repr(e))

# ---------- 5) EGH-Organisationsuebersicht (21 + 5 = 26) ----------
try:
    t = page_text("https://soziales.hessen.de/leistungen-der-eingliederungshilfe-gemaess-sgb-ix")
    for city in ["darmstadt", "frankfurt am main", "kassel", "offenbach am main", "wiesbaden"]:
        check("egh-org kreisfreie stadt %s" % city, has(t, city))
    check("egh-org landkreis-wort", has(t, "landkreis"))
except Exception as e:
    check("egh-org fetch", False, repr(e))

# ---------- 6) Verwaltungsportal: EGH-Leistung ----------
try:
    t = page_text("https://verwaltungsportal.hessen.de/leistung?leistung_id=L100001_8960876")
    check("vp-egh lwv nach schulausbildung", has(t, "landeswohlfahrtverband hessen"))
except Exception as e:
    check("vp-egh fetch", False, repr(e))

# ---------- 7) Verwaltungsportal: Pflegekasse Wohnumfeld ----------
try:
    t = page_text("https://verwaltungsportal.hessen.de/leistung?leistung_id=B100019_581678")
    check("vp-pflege treppenlift", t.count("treppenlift") >= 1, "count=%d" % t.count("treppenlift"))
    check("vp-pflege wohnumfeld", has(t, "wohnumfeld"))
except Exception as e:
    check("vp-pflege fetch", False, repr(e))

# ---------- 8) Ministerium ----------
try:
    t = page_text("https://wirtschaft.hessen.de/wohnen-und-bauen/soziale-wohnraumfoerderung")
    check("hmwevw programm-nennung", has(t, "umbau von selbstgenutztem wohneigentum"))
    check("hmwevw volumen 2025", has(t, "4,0 mio") or has(t, "4,0 millionen"), "")
except Exception as e:
    check("hmwevw fetch", False, repr(e))

# ---------- 9) Land-Fachstelle wohnen-im-alter ----------
try:
    t = page_text("https://wohnen-im-alter.hessen.de/wohnberatung/finanzierung/soziale-wohnraumfoerderung")
    check("wia programm-nennung", has(t, "behindertengerechter umbau"))
except Exception as e:
    check("wohnen-im-alter fetch", False, repr(e))

# ---------- 10) Bad Homburg (gekennzeichnet kommunal) ----------
try:
    t = page_text("https://www.bad-homburg.de/de/stadt/aktuelles/land-hessen-foerdert-den-behindertengerechten-umbau-von-wohneigentum-ov8e4kbakn")
    check("homburg treppenlift-zeile", has(t, "treppenlift oder aufzug: bis zu 6.500 euro"))
except Exception as e:
    check("bad-homburg fetch", False, repr(e))

# ---------- 11) KfW ----------
try:
    t = page_text("https://www.kfw.de/inlandsfoerderung/Privatpersonen/Bestandsimmobilie/F%C3%B6rderprodukte/Altersgerecht-Umbauen-Investitionszuschuss-(455)/")
    check("kfw455 stopp-wortlaut", has(t, "diesen zuschuss können sie nicht mehr beantragen"))
    check("kfw455 2027-bedingung", has(t, "im jahr 2027 erneut bundesmittel"))
except Exception as e:
    check("kfw455 fetch", False, repr(e))
try:
    t = page_text("https://www.kfw.de/159")
    check("kfw159 treppenlifte-katalog", has(t, "treppenlifte, senkrecht-, hebe- oder plattformlifte installieren"))
    check("kfw159 50.000 je we", has(t, "50.000 euro je wohneinheit"))
except Exception as e:
    check("kfw159 fetch", False, repr(e))

# ---------- 12) Gesetze (ISO-8859-1 + Entities) ----------
try:
    t = page_text("https://www.gesetze-im-internet.de/sgb_9_2018/__113.html")
    check("sgb9-113 wohnraum", has(t, "leistungen für wohnraum"))
except Exception as e:
    check("sgb9-113 fetch", False, repr(e))
try:
    t = page_text("https://www.gesetze-im-internet.de/sgb_9_2018/__77.html")
    check("sgb9-77 beschaffung-umbau", has(t, "beschaffung, den umbau, die ausstattung und die erhaltung"))
except Exception as e:
    check("sgb9-77 fetch", False, repr(e))
try:
    t = page_text("https://www.gesetze-im-internet.de/sgb_11/__40.html")
    check("sgb11-40 4180-geschützt", has(t, "4 180"), "kein '4 180' in normiertem Text")
    check("sgb11-40 16720-geschützt", has(t, "16 720"))
except Exception as e:
    check("sgb11-40 fetch", False, repr(e))

# ---------- Summary ----------
print("\n== PARENT VERIFY HESSEN: %d PASS, %d FAIL ==" % (PASSED, FAILED))
if FAILS:
    print("Fails:")
    for f in FAILS:
        print(" -", f)
sys.exit(1 if FAILED else 0)
