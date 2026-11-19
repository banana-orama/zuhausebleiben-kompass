# Aroundhome-Evidenz 19.11.2026 (kein Login nötig, alles öffentlich abgerufen)

## 1) Awin Public Profile 68536 (Drift-Check)
- URL: https://ui.awin.com/merchant-profile/68536 → HTTP 200 (Roh-HTML lokal: awin-profile-68536.html, uncommitted)
- **Umsatzbeteiligung: 30%** (weiterhin gelistet, unverändert zu 23.10./16.11.)
- **Cookie-Laufzeit: 30 Tage** (weiterhin gelistet)
- Kein Drift gegenüber research/partner-scan-badumbau-231026.md und Agency-Mail 16.11. (Sent-Antwort 1026).

## 2) Tracker ohne Deeplink — Pre-Approval-Format-Probe (19.11.)
- `https://www.awin1.com/cread.php?awinmid=68536&awinaffid=3124891` (KEIN ued-Parameter)
- Ergebnis: **HTTP 302** → `https://aaa.aroundhome.de/trck/eclick/566ef6a9daf85016ebaa038531c02e84?ext_publisher_id=3124891&sv1=affiliate&sv_campaign_id=3124891&awc=68536_1795094843_17a2d4fe6ceac68115bc457f6963cfaa`
- Deutung: Die vollständige Attribution-Kette (awc=68536_<ts>_<hash>) läuft **auch ohne Deeplink**; Einstieg ist der Aroundhome-Homepage-Level-Redirect über deren eigenes Tracking. Die offene Agency-Frage „erlaubte Textlink-Zielseite“ blockiert die Aktivierung damit NICHT — Homepage-Einstieg ist der Default; eine spätere Zielseite ist eine Ein-Zeilen-Änderung am Placement.
- Grenze: Probe vor Freischaltung — Format/Nachweis gültig, aber Links gehen erst NACH Freischalt-Readback live (Approved-Sites-Klausel).

## 3) Datenschutz-URL für DSE_META
- `https://www.aroundhome.de/datenschutzerklaerung/` → **HTTP 200** (verifiziert 19.11.)
- `https://www.aroundhome.de/datenschutz` → 404; `/datenschutz.html` → 404 — ausschließlich die /datenschutzerklaerung/-URL verwenden.

## 4) Zielkandidaten (Deeplinking bleibt gesperrt)
- `https://www.aroundhome.de/` → 200
- `https://www.aroundhome.de/badezimmer/` → 200 (Kandidat für später, NUR wenn die Agency Deeplink/Zielseite explizit erlaubt)

## 5) Mailbox-Stand (19.11.)
- Neueste Eingänge: 11237 (OOO-Autoreply Katharina Folker, Rückkehr **23.11.2026**), 11236 (17.11., Bewerbung nicht auffindbar → Publisher-ID 3124891 nachgereicht, Sent 1027). Keine neue substanzielle Antwort seit 17.11.

## 6) Aktivierungs-Dry-Run (19.11.)
- Skript: `research/verify_aroundhome_activation_dryrun_191126.py` → **22/22 PASS, 0 FAILS**
- Fixture: `partner-links-fixture-activation.json` (voll aktiviert, 2 Placements, DRYRUN-Platzhalter im approval_readback), `partner-links-fixture-partial.json` (Teilaktivierung, muss abbrechen — tut es)
- Beweis: Aktivierung am Freischalttag = **ein Commit** mit exakt 2 Dateien (data/partner-links.json + DSE_META in generate.mjs); ohne DSE_META-Zeile bricht der Build kontrolliert ab (Gate scharf, Same-Commit-Regel).
- Not-Gate-Lektionen beim Schreiben des Skripts: Tracker-URL im built HTML `&amp;`-escaped; generate-only-Build ohne Checklisten-URLs (45 locs bei 40 Artikeln) — beide im Skript abgehandelt.
