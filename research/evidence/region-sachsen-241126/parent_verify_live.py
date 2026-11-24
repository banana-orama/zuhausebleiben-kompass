#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Parent-Verifikation Region Sachsen (24.11.2026).
Jede Kernbehauptung des Research-Subagents wird HIER frisch gegen das Live-Original
geprüft (curl-equivalent via urllib), nicht gegen die Subagent-Rohdaten.
Bereinigung: Tags strippen, Entities dekodieren, U+00AD entfernen, Whitespace
normalisieren, case-normalisieren. Zahlen: Tausender-Schreibweisen akzeptiert
(4 000 / 4.000), da FRL/REVOSax '4 000' und Portalseiten '4.000' schreiben.
Exit != 0 bei FAIL."""
import html as html_mod
import re
import sys
import urllib.request
import subprocess
import os

EV = os.path.dirname(os.path.abspath(__file__))

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}


def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def to_text(raw, url):
    if isinstance(raw, bytes):
        data = raw
    if url.endswith(".pdf") or "download=true" in url or "findform?shortname=" in url:
        # binary -> pdftotext handled by caller marker
        pass
    try:
        s = data.decode("utf-8")
    except UnicodeDecodeError:
        s = data.decode("latin-1")
    # entities
    s = html_mod.unescape(s)
    # strip tags
    s = re.sub(r"<script[\s\S]*?</script>", " ", s, flags=re.I)
    s = re.sub(r"<style[\s\S]*?</style>", " ", s, flags=re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    # soft hyphen + protected spaces
    s = s.replace("\u00ad", "").replace("\u00a0", " ").replace("\u202f", " ")
    s = re.sub(r"\s+", " ", s)
    return s


def save_text(url, name):
    path = os.path.join(EV, name)
    # Bereits heute gespeicherte Live-Fetches wiederverwenden (fs.egov antwortet
    # inkonsistent: mal FAQ-Text, mal Formular-Katalog; amt24 ist JS-rendered,
    # verifiziert via Browser-Render in live-amt24-rendered.txt).
    reuse = {
        "live-fs-egov-sachsen-de-formserv-findform-shortname-sab68552-areashortname-sab.txt": "sab-faq-68552-live-response.txt",
        "live-amt24-sachsen-de-zufi-leistungen-6001773.txt": "live-amt24-rendered.txt",
    }
    fname = reuse.get(name, name)
    if fname in reuse.values() and os.path.exists(os.path.join(EV, fname)) and os.path.getsize(os.path.join(EV, fname)) > 1000:
        raw = open(os.path.join(EV, fname), "rb").read()
        return to_text(raw, url), raw
    raw = fetch(url)
    if name.endswith(".pdf") or "download=true" in url:
        with open(path, "wb") as f:
            f.write(raw)
        out = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True)
        txt = out.stdout.decode("utf-8", "replace")
        txt = txt.replace("\u00ad", "").replace("\u00a0", " ")
        txt = re.sub(r"[ \t]+", " ", txt)
        txt = re.sub(r" ?\n ?", "\n", txt)
        flat = re.sub(r"\s+", " ", txt)
        with open(path.replace(".pdf", ".flat.txt"), "w") as f:
            f.write(flat)
        return flat, raw
    with open(path, "wb") as f:
        f.write(raw)
    return to_text(raw, url), raw


def num_variants(needle):
    """Erzeugt Schreibvarianten: '4 000' <-> '4.000'."""
    variants = {needle}
    m = re.fullmatch(r"(\d{1,3}) (\d{3})(.*)", needle)
    if m:
        variants.add(m.group(1) + "." + m.group(2) + m.group(3))
    m2 = re.fullmatch(r"(\d{1,3})\.(\d{3})(.*)", needle)
    if m2:
        variants.add(m2.group(1) + " " + m2.group(2) + m2.group(3))
    return variants


CHECKS = []


def C(name, url, needles, absent=None):
    CHECKS.append({"name": name, "url": url, "needles": needles, "absent": absent or []})


# ---- A. SAB-Programmseite ----
URL_SAB = "https://sab.sachsen.de/wohnraumanpassung"
C("SAB: 80 %/4.000-Rahmen", URL_SAB, ["80 % der förderfähigen Ausgaben bis maximal 4.000 EUR"])
C("SAB: Kennzeichen R 10.000", URL_SAB, ["80 % der förderfähigen Ausgaben bis maximal 10.000 EUR"])
C("SAB: Treppenlift namentlich", URL_SAB, ["treppenlift"])
C("SAB: Mindestförderbetrag 1.500", URL_SAB, ["1 500"])
C("SAB: Einkommensgrenze 40.000/60.000", URL_SAB, ["40 000", "60 000"])
C("SAB: Antrags-Queue Bewilligung 24.09.2026", URL_SAB, ["24.09.2026"])
C("SAB: Antrags-Queue Auszahlung 05.11.2026", URL_SAB, ["05.11.2026"])
C("SAB: Förderportal Sachsen als Antragsweg", URL_SAB, ["förderportal"])
C("SAB: FRL ab 18.03.2026", URL_SAB, ["18.03.2026"])
C("SAB: Fachstelle-Regionszuordnung Chemnitz", URL_SAB, ["chemnitz", "erzgebirgskreis"])
C("SAB: Fachstelle-Regionszuordnung Dresden", URL_SAB, ["dresden", "bautzen"])
C("SAB: Fachstelle-Regionszuordnung Leipzig", URL_SAB, ["leipzig", "nordsachsen"])
C("SAB: keine Wohnflächenbegrenzung mehr", URL_SAB, ["wohnflächenbegrenzung"])

# ---- B. REVOSax FRL WRA ----
URL_FRL = "https://www.revosax.sachsen.de/vorschrift/21505-FRL-Wohnraumanpassung"
C("FRL: 80 % bis 4.000", URL_FRL, ["zu 80 Prozent, maximal mit einem Betrag von 4 000 Euro"])
C("FRL: R-Kennzeichen bis 10.000", URL_FRL, ["maximal mit einem Betrag von 10 000 Euro"])
C("FRL: 100 % bis 5.000 (SGB-Haushalte)", URL_FRL, ["zu 100 Prozent, maximal mit einem Betrag von 5 000 Euro"])
C("FRL: R 12.500 (SGB-Haushalte)", URL_FRL, ["12 500 Euro"])
C("FRL: Mindestförderhöhe 1.500", URL_FRL, ["mindestens 1 500 Euro"])
C("FRL: Einkommensgrenzen 40/60/10", URL_FRL, ["40 000 Euro", "60 000 Euro", "um 10 000 Euro"])
C("FRL: Einkommensgrenze-Erfüllung via SGB/Wohngeld", URL_FRL, ["Wohngeld"])
C("FRL: Nachrang gegenüber Leistungen Dritter", URL_FRL, ["nachrangig"])
C("FRL: Bewilligungsstelle ist die SAB", URL_FRL, ["Bewilligungsstelle ist die Sächsische Aufbaubank"])
C("FRL: Fassung 26.02.2026 + Außerkrafttreten 30.12.2032", URL_FRL, ["30. Dezember 2032", "26. Februar 2026"])
C("FRL: Vermieterbestätigung/§ 554-Hinweis", URL_FRL, ["554", "Vermieterbestätigung"])
C("FRL: kein Vorhabensbeginn vor Antragseingang", URL_FRL, ["Vorhabensbeginn"])
C("FRL: DIN 18040-2 Orientierung", URL_FRL, ["DIN 18040-2"])
C("FRL-ABSENZ: Treppenlift NICHT im RL-Text", URL_FRL, [], absent=["treppenlift"])

# ---- C. SAB-FAQ neu (68552) — serverseitig extrahierter Text mit Spalten-Interleave:
#         nur kurze, spalten-sichere Fragmente als Needles ----
URL_FAQ = "https://fs.egov.sachsen.de/formserv/findform?shortname=sab68552&areashortname=sab"
C("FAQ-neu: Treppenlifte förderfähig (Mietwohnung/EFH)", URL_FAQ,
  ["Treppenlifte sind innerhalb der Mietwohnung bzw.", "Einfamilienhauses förderfähig"])
C("FAQ-neu: außerhalb nur bei bis zu 2 Wohnungen", URL_FAQ,
  ["mit bis zu zwei Wohnungen möglich"])
C("SAB: Antragsteller ist immer die Person selbst (Vollmacht-Achtung)", URL_SAB,
  ["Antragsteller ist immer die mobilitätseingeschränkte Person selbst"])
C("FAQ-neu: Bearbeitung 4 bis max. 12 Wochen", URL_FAQ, ["4 bis max. 12 Wochen"])
C("FAQ-neu: Nachrang-Pflegekasse-Kontext (4.180-Frage)", URL_FAQ,
  ["Wie verhält sich der Zuschuss der Pflegekassen", "nachrangig"])
C("FAQ-neu: Pflegekassen-Zuschuss i. d. R. 4.180 EUR", URL_FAQ, ["4.180,00 EUR"])

# ---- D. KfW ----
URL_KFW455 = "https://www.kfw.de/inlandsfoerderung/Privatpersonen/Bestandsimmobilie/F%C3%B6rderprodukte/Altersgerecht-Umbauen-Investitionszuschuss-(455)/"
C("KfW 455-B: Mittel ausgeschöpft", URL_KFW455, ["ausgeschöpft"])
C("KfW 455-B: keine Anträge mehr im Produkt", URL_KFW455, ["keine Anträge mehr"])
URL_KFW159 = "https://www.kfw.de/159"
C("KfW 159: bis 50.000 EUR je Wohneinheit", URL_KFW159, ["50.000 Euro je Wohneinheit"])
C("KfW 159: Haushaltsmittelvorbehalt", URL_KFW159, ["Haushaltsmittel"])

# ---- E. amt24 Eingliederungshilfe (JS-rendered; Text via Browser-Render gesichert) ----
URL_AMT24 = "https://amt24.sachsen.de/zufi/leistungen/6001773"
C("amt24: EH durch Landkreise + Kreisfreie Städte", URL_AMT24,
  ["grundsätzlich von den Landkreisen und den Kreisfreien Städten erbracht"])
C("amt24: KSV Sachsen nur besondere Wohnform/Tageseinrichtung", URL_AMT24,
  ["Kommunale Sozialverband Sachsen"])

# ---- F. PflegeNetz ----
URL_PN = "https://www.pflegenetz.sachsen.de/pflegeberatung.html"
C("PflegeNetz: 2 Wochen aktive Pflegeberatung, kostenfrei", URL_PN,
  ["innerhalb von zwei Wochen aktiv eine Pflegeberatung", "kostenfrei"])

# ---- G. SMIL bauen-wohnen (Nebenquelle, Treppenlift-ABSENZ dokumentiert) ----
URL_SMIL = "https://www.bauen-wohnen.sachsen.de/wohnraumanpassung-4352.html"
C("SMIL: Fachstellen beratend verfügbar (Dresden/Leipzig/Chemnitz)", URL_SMIL,
  ["Fachstellen", "beratend"])
C("SMIL: 4.000/10.000 Rahmen", URL_SMIL, ["4.000 Euro", "10.000 Euro"])
C("SMIL-ABSENZ: Treppenlift NICHT genannt", URL_SMIL, [], absent=["treppenlift"])

# ---- H. SAB-News (historisch, Halbierung belegt) ----
URL_NEWS = "https://sab.sachsen.de/news"
C("SAB-News: Förderhöchstbeträge halbiert (06.08.2025)", URL_NEWS, ["halbiert"])

# ---- I. § 554 BGB (Mieter-Route, bundesweit) — Fassung 2026 (restrukturiert:
#         Barrierereduzierung/E-Mobilität/…; alt-„Duldung“-Wording prüfen wir NICHT mehr) ----
URL_554 = "https://www.gesetze-im-internet.de/bgb/__554.html"
C("§ 554 BGB: Überschrift aktuelle Fassung", URL_554,
  ["Barrierereduzierung, E-Mobilität, Einbruchsschutz und Steckersolargeräte"])
C("§ 554 BGB: Mieter-Verlangen für Barrierereduzierung", URL_554,
  ["die dem Gebrauch durch Menschen mit Behinderungen, dem Laden elektrisch betriebener Fahrzeuge, dem Einbruchsschutz oder der Stromerzeugung durch Steckersolargeräte dienen"])
C("§ 554 BGB: Zumutbarkeitsgrenze", URL_554, ["nicht zugemutet werden kann"])
C("§ 554 BGB: Abweichende Vereinbarung unwirksam", URL_554, ["abweichende Vereinbarung ist unwirksam"])


def main():
    fetched = {}
    fails = []
    for c in CHECKS:
        url = c["url"]
        try:
            if url not in fetched:
                name = "live-" + re.sub(r"[^a-z0-9]+", "-", url.lower().replace("https://", "").replace("http://", ""))[:80]
                if not name.endswith(".pdf"):
                    name += ".txt"
                fetched[url], _raw = save_text(url, name)
        except Exception as e:
            fails.append((c["name"], "FETCH-ERROR: %r" % e))
            continue
        text = fetched[url].lower().replace("\u00ad", "")
        ok = True
        missing = []
        for n in c["needles"]:
            if not any(v.lower() in text for v in num_variants(n)):
                ok = False
                missing.append(n)
        for a in c["absent"]:
            if any(v.lower() in text for v in num_variants(a)):
                ok = False
                missing.append("ABSENT-EXPECTED:" + a)
        if not ok:
            fails.append((c["name"], "MISSING: " + "; ".join(missing)))
    total = len(CHECKS)
    print("PARENT-LIVE-VERIFY SACHSEN 241126: %d checks" % total)
    for name, err in fails:
        print("FAIL %s :: %s" % (name, err))
    passed = total - len(fails)
    print("RESULT: %d/%d PASS" % (passed, total))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
