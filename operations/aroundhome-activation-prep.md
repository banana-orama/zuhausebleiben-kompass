# Aroundhome-Aktivierungs-Playbook (textfertig, 19.11.2026) — **AUSGEFÜHRT 25.11.2026**

**Receipt 25.11.:** Beleg = Agency-Mail 11239 (25.11. 10:10, „ich kann bestätigen, dass ihr nun als Publisher zugelassen seid", `research/evidence/aroundhome-251126/artefact-confirm-11239.txt`). Commit `10e6966` (volle SHA 10e696664f9920198bca800f17170ae939f59174, exakt die 2 Dateien + Gates/Evidenz), CI-Run 45623941761 success, **öffentlicher Live-Readback 42/0 PASS** (`research/verify_aroundhome_live_251126.py`: 5 Artikel mit Marker/rel/tracker/Anzeige + robots index,follow, datenschutz spiegelt Aroundhome mit „Profil geprüft am 25. November 2026", Malteser intakt, 0 Leaks, Sitemap 57 locs unverändert), Activation-Gate 85/0 (`research/verify_aroundhome_activation_251126.py`), Mobile 390 px 0 px Overflow + CTA-Screenshot-Vision sauber (`research/verify_aroundhome_mobile_251126.py`), Tracker 302+awc re-verifiziert, IndexNow 200 (7 URLs). Rest offen: Awin-Login-Readback (erste Klick-Tests im Tracker-Inventory), Zielseiten-/Matching-/Testzeitraum-Fragen.

Zweck: Wenn die Agency (Artefact, Katharina Folker, zurück ab **23.11.**) über Publisher-ID 3124891 freischaltet, ist die Aktivierung **ein Commit mit exakt 2 Dateien** — vollständig vortestet am 19.11. (Dry-Run 22/22 PASS). Kein Warten, kein Explorieren am Freischalttag.

## Ausgangslage (alle Punkte heute verifiziert, Evidenz: research/evidence/aroundhome-191126/)
- Bewerbung 68536: formal eingereicht (Bewerbung offen); Agency konnte sie zunächst nicht finden → Publisher-ID 3124891 nachgereicht (Sent 1027, 17.11.).
- Konditionen (öffentlich, 19.11. re-gelesen): **Umsatzbeteiligung 30 %** auf gematchte Leads (kein Fix-CPL), **Cookie 30 Tage**, Lead-Validierung ~8 Tage, Callcenter-Qualifizierung vor Matching; Lead-Kriterien: echte, exklusive Kontaktdaten, keine Test-/Auslandsanfragen.
- Vereinbarter Start: **Textlink**, kein iFrame (abgelehnt, Grundsatz Sent 1024: keine Interessentendaten auf unserer Seite), **Deeplinking nicht freigeschaltet**.
- **Technik bewiesen:** Tracker ohne Deeplink funktioniert — `cread.php?awinmid=68536&awinaffid=3124891` → 302 auf Aroundhomes eigenen Eclick-Einstieg MIT vollständiger Attribution (`awc=68536_<ts>_<hash>`). Die offene Zielseiten-Frage blockiert nicht; Homepage-Einstieg ist Default.

## Der Aktivierungs-Commit (2 Dateien, gleicher Commit — sonst bricht der Build)

### Datei 1: data/partner-links.json — aroundhome-Eintrag
```json
{
  "id": "aroundhome",
  "name": "Aroundhome DE",
  "awin_advertiser_id": 68536,
  "approved": true,
  "approval_readback": {
    "date": "<Datum der Freischaltung>",
    "evidence": "<echter Readback: Agency-Mail-Beleg ODER Awin-Login-Status 'zugelassen'; bei Login: 'Leave Programme' + unlocked Creatives>"
  },
  "compensation_note": "Umsatzbeteiligung (Regelfall 30%), kein Fix-CPL — CTA-Text entsprechend formuliert",
  "placements": [ siehe research/evidence/aroundhome-191126/partner-links-fixture-activation.json:
    aroundhome_badumbau_angebote → badumbau-angebote-vergleichen, bad-umbau-barrierefrei
    aroundhome_badumbau_planung  → badumbau-kosten, wanne-zur-dusche, bodengleiche-dusche-altbau
    beides Textlinks, url = https://www.awin1.com/cread.php?awinmid=68536&awinaffid=3124891 ]
}
```

### Datei 2: generate.mjs — DSE_META ergänzen (Zeile 58, exakt)
```js
const DSE_META={malteser:{...bestehend...},aroundhome:{desc:'Badumbau-Vermittlung',cookie:'30 Tage',checked:'19. November 2026',url:'https://www.aroundhome.de/datenschutzerklaerung/'}};
```
(`checked` nur bei tatsächlicher Re-Verifizierung des Profils am Aktivierungstag ändern.)

## Nach dem Commit (Acceptance, in dieser Reihenfolge)
1. `npm test` (Exit 0 — enthält test:partner mit der scharfen Kontradiktion-Logik)
2. `npm run build:launch` (CI baut selbst; lokal nur für Gates gegen LAUNCH-dist)
3. Gates gegen LAUNCH-dist: beide Placements auf genau den 5 adressierten Artikeln (`data-partner-placement`-Attribut, `rel="sponsored noopener"`, Anzeige-Kennzeichnung, escapete Tracker-URL), 0 Aroundhome-Marker auf allen anderen Artikeln, datenschutz.html Abschnitt 5+6 mit Aroundhome-Zeile (Cookie 30 Tage + verifizierte DSE-URL)
4. Mobile 390 px auf den 5 Seiten (0 px Overflow) + Screenshot/Vision-Kontrolle der CTA-Blöcke (Rendering-Pfad identisch zum seit 02.11. live bewiesenen Malteser-Block)
5. Push → CI abwarten (volle SHA prüfen) → **öffentlicher Live-Readback** auf den 5 URLs + datenschutz.html
6. Awin-Login-Readback nachtragen: erste Klick-Tests im Tracker-Inventory sichtbar?

## Bewusst offen (ändert nur Placement-Inhalte, nicht den Mechanismus)
- **Zielseiten-Frage** (gestellt 16.11., unbeantwortet): erlaubte Textlink-Zielseiten ohne Deeplink. Default bis Antwort: Homepage-Tracker (bewiesen). Wird /badezimmer/ erlaubt → Ein-Zeilen-Änderung (`&ued=<encoded>` NUR mit ausdrücklicher Erlaubnis).
- **Matching-Kriterien** und **Testzeitraum** (gestellt 16.11./17.11., unbeantwortet).
- Wirtschaftlichkeit ehrlich: 30 % auf GEMATCHTE Leads nach Callcenter-Qualifizierung; Ablehnungsgründe (Test/Duplikat/Ausland) dokumentiert; **keine Umsatzzusage ableitbar** — erste gematchten Leads abwarten, bevor mehr Bad-Artikel Placements bekommen.

## Verbote (unverändert)
- Kein sichtbarer Link vor Freischalt-Readback (Approved-Sites-Klausel: Verstoß = Ausschluss + Clawback).
- Kein iFrame/kein Formular-Embed, keine Interessenten-PII auf unserer Seite.
- Kein SEM/Anzeigen-Traffic (wir bleiben 100 % organisch).
