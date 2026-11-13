#!/usr/bin/env python3
"""Content-Gate für die NRW-Region-Seite gegen den LAUNCH-Dist.
Prüft: Kernfakten (Needles), Absenzen (keine §40-Beträge, keine Partner-Marker,
keine KfW-Verfügbarkeitsbehauptung), Related-Links im Förder/Wohn-Cluster,
CTA-Ziele, Quellenliste mit checked_at, robots/canonical, H1-Einzigkeit.
DIST_DIR-Override wie bei den übrigen Gates."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = Path(__file__).resolve().parent.parent / (sys.argv[1] if len(sys.argv) > 1 else "dist")
page = DIST / "region" / "nordrhein-westfalen.html"
if not page.exists():
    print(f"FAIL: {page} fehlt im Build")
    sys.exit(1)
raw = page.read_text(encoding="utf-8")
body = raw

fails, checks = [], 0
def needle(text, why):
    global checks
    checks += 1
    if text not in raw:
        fails.append(f"Needle fehlt ({why}): {text[:70]}")

def absent(text, why):
    global checks
    checks += 1
    if text in raw:
        fails.append(f"Absenz verletzt ({why}): {text[:70]}")

# --- Robots/Canonical/Meta ---
checks += 1
if '<meta name="robots" content="index,follow">' not in raw:
    fails.append("NRW-Seite muss index,follow tragen (Launch-Build)")
checks += 1
m = re.search(r'rel="canonical" href="([^"]+)"', raw)
if not m or not m.group(1).endswith("/region/nordrhein-westfalen.html"):
    fails.append(f"Canonical falsch: {m.group(1) if m else 'keiner'}")
checks += 1
if len(re.findall(r"<h1[ >]", raw)) != 1:
    fails.append("H1-Zahl != 1")
checks += 1
tm = re.search(r"<title>([^<]+)</title>", raw)
if not tm or len(tm.group(1)) > 65:
    fails.append(f"Title >65: {tm.group(1) if tm else ''}")
checks += 1
dm = re.search(r'<meta name="description" content="([^"]+)"', raw)
if not dm or len(dm.group(1)) > 160:
    fails.append(f"Description >160: {dm.group(1)[:60] if dm else 'fehlt'}")

# --- Kernfakten (NRW.BANK / WFNG) ---
for t in [
    ("220.000 €", "NRW.BANK Darlehenshöhe"),
    ("bis zu 50 % des Darlehens", "Tilgungsnachlass"),
    ("festen Zinsen über 30 Jahre", "Zinsbindung"),
    ("anrechenfreie Beträge bei der Einkommensermittlung", "Schwerbehinderte/Pflegebedürftige"),
    ("§ 13", "WFNG-Einkommensgrenzen"),
    ("23.540 €", "EG Alleinstehend A"),
    ("32.956 €", "EG Alleinstehend B"),
    ("28.350 €", "EG 2 Personen A"),
    ("39.690 €", "EG 2 Personen B"),
    ("57.910 €", "EG 6 Personen A"),
    ("81.074 €", "EG 6 Personen B"),
    ("Bewilligungsbehörde", "Antragsweg Landesprogramm"),
    ("Eigentumsförderung – Modernisierung", "Programmname"),
]:
    needle(*t)

# --- Kernfakten (Eingliederungshilfe LVR/LWL) ---
for t in [
    ("fest mit dem Baukörper verbundene Treppenlifter", "LWL-Beispiel Treppenlifter"),
    ("§ 64e SGB XII", "Abgrenzung Hilfe zur Pflege"),
    ("Landschaftsverband", "Zuständigkeit"),
    ("LVR", "Rheinland"),
    ("LWL", "Westfalen-Lippe"),
    ("zwei Wochen", "Zuständigkeitsprüfung"),
    ("keine Antragsgebühren", "Kosten Eingliederungshilfe"),
    ("Kreis Recklinghausen", "Praxis-Beispiel"),
    ("abhängig von Einkommen und Vermögen", "Subsidiaritäts-/Bedürftigkeitsprüfung"),
]:
    needle(*t)

# --- Kernfakten (KfW-Stand + Wohnberatung) ---
for t in [
    ("Diesen Zuschuss können Sie nicht mehr beantragen.", "KfW-Stop-Wortlaut"),
    ("„Altersgerecht Umbauen“ (159)", "KfW-Kredit-Alternative"),
    ("8. April 2026", "Neustart-Datum"),
    ("2027", "bedingte Wiederaufnahme"),
    ("6.250 €", "Stale-Portal-Warnung"),
    ("berät neutral und kostenlos", "Wohnberatung"),
    ("digitalen Karte", "Stellen-Finder"),
    ("13.11.2026", "Quellenstand"),
    ("geprüft 2026-11-13", "checked_at-Format"),
    ("Mit KI-Unterstützung erstellt", "KI-Kennzeichnung"),
    ("keine Angebote vermittelt", "Vermittlungs-Offenheit"),
]:
    needle(*t)

# --- Absenzen ---
for t in [
    ("4.180", "§40-Betrag gehört nur in die spezialisierten Ratgeber"),
    ("16.720", "§40-Betrag"),
    ("awin1.com", "kein Partner-Tracker"),
    ('rel="sponsored"', "kein Partner-Placement"),
    ("data-partner-placement", "kein Partner-Placement"),
    ("beantragt werden kann", "keine Verfügbarkeits-Zusage für 455-B"),
    ("Genehmigung ist garantiert", "keine Fördergarantie"),
]:
    absent(*t)

# --- CTA/Related: Cluster-Konsistenz (Förderung/Wohn/Pflege, kein Bad-Funnel) ---
for slug in ["treppenlift-zuschuss", "wohnumfeldverbesserung-beantragen",
             "treppenlift-foerderung-ohne-pflegegrad", "treppenlift-mietwohnung",
             "pflegegrad-antrag-ablauf-fristen", "treppenlift-kosten"]:
    needle(f"/{slug}.html", f"Ziel-Link {slug}")
absent("/bad-umbau-barrierefrei.html#abschnitt", "kein Bad-Abschnitts-Funnel")

# --- Quellenliste: 10 Quellen mit URLs ---
for u in [
    "nrwbank.de/de/privatpersonen/wohneigentum-gestalten/barrierefrei-umbauen",
    "nrwbank.de/de/foerderung/foerderprodukte/15730",
    "kfw.de/inlandsfoerderung/Privatpersonen/Bestandsimmobilie",
    "News-Details_889024.html",
    "News-Details_903232.html",
    "lwl-inklusionsamt-soziale-teilhabe.de/de/hilfen/leistungen-fur-wohnraum",
    "serviceportal.lwl.org/de/soziale-teilhabe/eingliederungshilfe-fur-volljaehrige-menschen",
    "kreis-re.de/Inhalte/Buergerservice/_index2.asp?id=18979",
    "lk-wohnberatung.nrw/was-ist-wohnberatung",
    "lk-wohnberatung.nrw/wohnberatungsstellen",
]:
    needle(u, "Quellen-URL")

# --- Struktur: Abschnitts-Anker, FAQ-details, Formular-Hinweis sitewide ---
for t in ['id="abschnitt-1"', 'id="abschnitt-8"', "<details>", "Häufige Fragen",
          "Passend dazu", "Quellen und offizielle Angaben"]:
    needle(t, "Struktur")

# --- Hub-Karte: NRW-Teaser real, andere Platzhalter ---
hub = (DIST / "regional.html").read_text(encoding="utf-8")
checks += 1
if "Erste ausführlich recherchierte Region" not in hub:
    fails.append("Hub: NRW-Teaser fehlt")
checks += 1
if '<meta name="robots" content="noindex,follow">' not in hub:
    fails.append("Hub muss noindex bleiben")

# --- Sitemap: genau NRW als Region ---
sm = (DIST / "sitemap.xml").read_text(encoding="utf-8")
locs = [u.split("<loc>")[1].split("</loc>")[0] for u in sm.split("<url>")[1:]]
checks += 1
rlocs = [u for u in locs if "/region/" in u or u.endswith("/regional.html")]
if not (len(rlocs) == 1 and rlocs[0].endswith("/region/nordrhein-westfalen.html")):
    fails.append(f"Sitemap-Regionen falsch: {rlocs}")

print(f"region-nrw Content-Gate: {checks} Checks")
if fails:
    print("FAIL:", *fails, sep="\n  ")
    sys.exit(1)
print("verify_region_nrw_content_131126: ALL PASS")
