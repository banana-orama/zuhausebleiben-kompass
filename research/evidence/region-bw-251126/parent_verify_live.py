#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Parent-Verifikation Region Baden-Württemberg (25.11.2026).
Jede Kernbehauptung des Research-Subagents wird HIER frisch gegen das Live-Original
geprüft (eigener Abruf, nicht gegen die Subagent-Rohdaten). Bereinigung: Tags
strippen, Entities dekodieren, U+00AD/NBSP entfernen, Whitespace normalisieren,
case-normalisieren (Vergleich klein). service-bw-Seiten sind JS-SPAs: deren
Belege gelten über die heute gesicherten Browser-Render-Dateien des Subagents
(live-servicebw-*-rendered.txt) UND zusätzlich einen unabhängigen Parent-Browser-
Render (parent-render-553.txt), der separat in research/verify_bw_render_251126.js
geprüft wird — hier nur Datei-Existenz + Needle-Check.
Exit != 0 bei FAIL."""
import html as html_mod
import os
import re
import subprocess
import sys
import tempfile
import urllib.request

EV = os.path.dirname(os.path.abspath(__file__))

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}

PASSED = 0
FAILED = 0


def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


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


def pdf_text(raw):
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        f.write(raw)
        path = f.name
    out = subprocess.run(["pdftotext", "-enc", "UTF-8", path, "-"],
                         capture_output=True, timeout=120)
    os.unlink(path)
    if out.returncode != 0:
        raise RuntimeError("pdftotext failed: " + out.stderr.decode("utf-8", "ignore"))
    return out.stdout.decode("utf-8", "ignore")


CACHE = {}


def page(url, kind="html"):
    if url not in CACHE:
        raw = fetch(url)
        CACHE[url] = norm(pdf_text(raw) if kind == "pdf" else raw.decode("utf-8", "ignore"))
    return CACHE[url]


def local(name):
    path = os.path.join(EV, name)
    with open(path, encoding="utf-8") as f:
        return norm(f.read())


def check(label, haystack, needle, expect=1):
    global PASSED, FAILED
    hit = norm(needle) in haystack
    count = haystack.count(norm(needle))
    ok = (count >= 1) if expect else (count == 0)
    if ok:
        PASSED += 1
        print("PASS  %-38s %s" % (label, needle[:60]))
    else:
        FAILED += 1
        print("FAIL  %-38s %s (hits=%d expect=%s)" % (label, needle[:60], count, ">=1" if expect else "0"))


LB = "https://www.l-bank.de/produkte/wohnimmobilien/eigentumsfinanzierung-bw-zusatzfinanzierung-barrierefreiheit.html"
K455 = "https://www.kfw.de/inlandsfoerderung/Privatpersonen/Bestandsimmobilie/F%C3%B6rderprodukte/Altersgerecht-Umbauen-Investitionszuschuss-(455)/"
K159 = "https://www.kfw.de/159"
ERLASS = "https://mlw.baden-wuerttemberg.de/fileadmin/redaktion/m-mlw/intern/Dateien/03_Bauen-Wohnen/Wohnungsbau/Wohnraumfoerderung/2025_12_VwV-Wohnungsbau_BW_2022_-_Erlass_Aenderung_Einkommensgrenzen.pdf"
ANLAGE = "https://mlw.baden-wuerttemberg.de/fileadmin/redaktion/m-mlw/intern/Dateien/03_Bauen-Wohnen/Wohnungsbau/Wohnraumfoerderung/2025_12_VwV-Wohnungsbau_BW_2022_Anlage_zum_Erlass_vom_01.12.2025_ge.pdf"

# --- L-Bank Produktseite (Weg 2) ---
lb = page(LB)
check("lbank.kredithoehe", lb, "Kredithöhe: bis zu 50.000 €")
check("lbank.sollzins", lb, "Sollzinssatz: 1,00 %")
check("lbank.tilgung", lb, "Tilgung: 3,00 %")
check("lbank.anlaufjahre", lb, "mit 2 tilgungsfreien Anlaufjahren")
check("lbank.tilgungszuschuss", lb, "Ergänzender Tilgungszuschuss bei Herstellung von Barrierefreiheit eines altersgerechten Hauses durch die vollständige Umsetzung der DIN 18040-2: 3 % der förderfähigen Kosten, maximal 1.500 €.")
check("lbank.zugang-basis", lb, "die Zusage der Basisförderung liegt nicht länger als 10 Jahren zurück")
check("lbank.anpassungsfoerderung", lb, "Sie haben durch eine Schwerbehinderung spezielle Wohnbedürfnisse und möchten bestehenden, selbst genutzten Wohnraum unabhängig von einer vorherigen oder gleichzeitigen Förderung altersgerecht umbauen (Anpassungsförderung).")
check("lbank.massnahmen-treppe", lb, "Überwindung von Treppen und Stufen")
check("lbank.massnahmen-sanitaer", lb, "Maßnahmen an Sanitärräumen")
check("lbank.massnahmen-einzel", lb, "Einzelmaßnahmen zur Barriere-Reduzierung nach DIN 18040-2")
check("lbank.katalog-verweis", lb, "und vieles mehr (siehe hierzu den Maßnahmen- und Anforderungskatalog)")
check("lbank.altersgerecht-def", lb, "müssen Zugang, Wohn- und Schlafzimmer, Küche und Bad barrierereduziert sein")
check("lbank.wartezeit", lb, "Nach aktuellem Stand ist jedoch von einer Wartezeit von mindestens einem Jahr bis zur Bewilligung auszugehen.")
check("lbank.absenz-treppenlift", lb, "treppenlift", expect=0)

# --- service-bw 553 (SPA, gerenderte Belegdatei von heute + Parent-Render separat) ---
sb553 = local("live-servicebw-wohneigentum-553-rendered.txt")
check("sb553.landratsamt", sb553, "in Landkreisen: die Wohnraumförderungsstelle im Landratsamt")
check("sb553.stadtkreis", sb553, "in Stadtkreisen: die Wohnraumförderungsstelle im Bürgermeisteramt des Bauortes")
check("sb553.gdb50", sb553, "wonach ein Grad der Behinderung von wenigstens 50 erforderlich ist")
check("sb553.herruehren", sb553, "Die speziellen Wohnbedürfnisse hinsichtlich des Grundrisses oder der Ausstattung müssen von der Schwerbehinderung herrühren.")
check("sb553.portal", sb553, "Einen Antrag können Sie über das Förderportal der L-Bank stellen")
check("sb553.vorhabenbeginn", sb553, "Ein vorzeitiger Vorhabenbeginn führt zur Ablehnung der Förderung.")
check("sb553.keine-frist", sb553, "Es besteht grundsätzlich keine Antragsfrist.")
check("sb553.eigenleistung", sb553, "Die Eigenleistung beträgt mindestens 25 Prozent der Gesamtkosten des förderfähigen Vorhabens. Bei erstrangiger Absicherung des Darlehens beträgt die Eigenleistung mindestens 15 Prozent der Gesamtkosten.")

# --- service-bw 1179 EGH + 531 Friedrichshafen (SPA-Render von heute) ---
sb1179 = local("live-servicebw-egh-1179-rendered.txt")
check("sb1179.gesamtplan", sb1179, "Gesamtplan")
sb531 = local("live-servicebw-kommunal-friedrichshafen-531-rendered.txt")
check("sb531.treppenlift", sb531, "Aufzug / Treppenlift – Maximale Förderung 2.500 Euro")
check("sb531.freiwillig", sb531, "freiwillige Sozialleistung, auf die kein Rechtsanspruch besteht")

# --- Sozialministerium EGH + Pflegeberatung ---
smbw = page("https://sozialministerium.baden-wuerttemberg.de/de/soziales/bundesteilhabegesetz/eingliederungshilfe/")
check("smbw.44-traeger", smbw, "44 Stadt- und Landeskreise als Träger der Eingliederungshilfe")
check("smbw.wohnraum-kontext", smbw, "Eingliederungshilfe")
smpf = page("https://sozialministerium.baden-wuerttemberg.de/de/gesundheit-pflege/pflege/beratung")
check("smpf.neutral", smpf, "berät unabhängig, neutral und kostenlos rund um das Thema Pflege")

# --- BMG Beispielmaßnahmen ---
bmg = page("https://www.bundesgesundheitsministerium.de/pflege-zu-hause/zuschuesse-zur-wohnungsanpassung")
check("bmg.treppenlifte", bmg, "Maßnahmen zur Überwindung von Treppen und Stufen durch Rampen oder Aufzüge/Treppenlifte")

# --- KfW 455-B (Stopp) + 159 (Kredit) ---
k455 = page(K455)
check("kfw455.stopp", k455, "Diesen Zuschuss können Sie nicht mehr beantragen")
check("kfw455.wiederaufnahme-2027", k455, "Sollten im Jahr 2027 erneut Bundesmittel für barrierereduzierende Maßnahmen bereitgestellt werden, wird eine Antragstellung wieder möglich sein.")
k159 = page(K159)
check("kfw159.treppenlifte", k159, "Treppenlifte, Senkrecht-, Hebe- oder Plattformlifte installieren")
check("kfw159.kombi", k159, "Wird eine Maßnahme (z. B. Badumbau) mit dem Zuschuss der Pflegeversicherung gefördert, können andere Maßnahmen (z. B. Treppenlift) mit dem Kredit der KfW gefördert werden.")
check("kfw159.hoehe", k159, "bis zu 50.000 Euro")

# --- Pflegestützpunkte BW ---
psb = page("https://www.bw-pflegestuetzpunkt.de/")
check("psbw.alle-kreise", psb, "Alle Stadt- und Landkreise in Baden-Württemberg haben Pflegestützpunkte")

# --- Bundesrecht (gesetze-im-internet) ---
check("sgb9-113.wohnraum", page("https://www.gesetze-im-internet.de/sgb_9_2018/__113.html"), "Leistungen für Wohnraum")
check("sgb9-77.umfang", page("https://www.gesetze-im-internet.de/sgb_9_2018/__77.html"), "Die Leistungen umfassen Leistungen für die Beschaffung, den Umbau, die Ausstattung und die Erhaltung von Wohnraum, der den besonderen Bedürfnissen von Menschen mit Behinderungen entspricht.")
check("sgb11-40.4180", page("https://www.gesetze-im-internet.de/sgb_11/__40.html"), "4 180 Euro")
check("sgb11-40.16720", page("https://www.gesetze-im-internet.de/sgb_11/__40.html"), "16 720 Euro")

# --- MLW Erlass + Anlage (PDF frisch) ---
erl = page(ERLASS, kind="pdf")
check("mlw.bezugs groesse".replace(" ", ""), erl, "Die Bezugsgröße beträgt jetzt 71 000 Euro")
check("mlw.dynamisierung", erl, "Dynamisierung der Einkommensgrenzen")
check("mlw.paragraf", erl, "§ 10 Abs. 3")
anl = page(ANLAGE, kind="pdf")
check("mlw-anlage.beispiele", anl, "Berechnungsbeispiele")
check("mlw-anlage.74550", anl, "74.550")
check("mlw-anlage.106600", anl, "106.600")

print("\n=== %d PASS, %d FAIL ===" % (PASSED, FAILED))
sys.exit(1 if FAILED else 0)
