# Pinterest-Setup-Plan (Organic-First) — ZuhauseBleiben Kompass

Stand: 2026-10-19 · Ausgangslage: Awin Lifta 40988 + Malteser 112616 pending (Erstmail 15.10., Kontakt wieder ab 22.10. erreichbar). Kein Pinterest-Konto existiert.

## Kernentscheidung (und warum sie trägt)

Die frühere Regel „Pinterest erst nach Kanalfreigabe“ schützt den **Affiliate-/Lead-Pfad**. Organische Pins auf eigene, KI-gekennzeichnete Schema-Grafiken + eigene Artikel-URLs sind eine andere Kategorie: eigener Content, eigene Domain, keine Partnerlinks, keine Gesundheitsdaten, keine Produktdarstellung. Risiko bleibt trotzdem nicht null (Zielgruppen-/Werbekanäle-Verwechslung beim Partner), deshalb:

1. **Jetzt:** Nur organische Pins zu eigenen Artikeln, Bild = eigenes SVG-Asset (als PNG exportiert), Beschreibung = eigene, quellenbelegte Einleitung. Kein Partnername, keine Preiszahl, kein CTA zu Anbietern, keine Affiliate-Links.
2. **Im Liftstar-Follow-up (ab 22.10.)** getrennt erfragen: (a) Kanalfreigabe für organische Pinterest-Präsenz, (b) spätere Affiliate-Pins. Beide Antworten getrennt dokumentieren (PARTNER-OUTREACH-STATE.md).
3. **Nie** Pin-URLs auf Partner-/Checkout-Seiten zeigen, bis die Partnerfreigabe + Awin-Programmzusage schriftlich vorliegen.

## Schritt-für-Schritt: Business-Konto anlegen (Operator klickt)

1. Browser (normal, kein Inkognito): `https://business.pinterest.com/de/` → „Konto erstellen“. Falls bereits ein Privatkonto existierte: eher neues Business-Konto.
2. E-Mail: projektpostfach `anfragen@zuhausebleiben-kompass.de` (via Himalaya konfiguriert, Verifizierungsmail dort abrufbar). Passwort → macOS-Schlüsselbund, nicht im Chat/Repo.
3. Kontotyp: **Geschäftskonto**. Profilname: „ZuhauseBleiben Kompass“ (exakt wie Impressum).
4. Website-Claim: Einstellungen → „Website beanspruchen“ → `zuhausebleiben-kompass.de` via **HTML-Meta-Tag** (`<meta name="p:domain_verify" content="…">`). ACHTUNG: Der Einbau ins `<head>`-Template (layout() in generate.mjs) ist eine **Site-Änderung → Operator-Gate**. Alternative ohne Code: HTML-Datei-Upload geht bei GitHub Pages nur über Repo — also faktisch auch ein Build-Eingriff. → Zeitpunkt mit nächstem regulären Deploy koppeln.
5. Business-Feld „Anzeigenkonto“: **überspringen** (kein Werbebudget, kein Werbekonto anlegen).
6. Zielgruppe/Interessen im Onboarding: „Heimwerken“, „Innenarchitektur“, „Bau & Renovierung“ grob wählen — nur Kategorisierung, keine Verpflichtung.
7. 2FA aktivieren (Einstellungen → Sicherheit), Recovery-Codes im Schlüsselbund/Tresor ablegen.

## Board-Struktur (start: 4 Boards)

| Board | Beschreibung (Pinterest-SEO) | Pins zuerst |
|---|---|---|
| Treppenlift Ratgeber | Kosten, Zuschüsse, Mietwohnung, Vergleich — Ratgeber für Angehörige | 6 Lift-Artikel |
| Bad barrierefrei umbauen | Wanne-zur-Dusche, bodengleiche Dusche Altbau, Angebotsvergleich, Förderung | 4 Bad-Artikel |
| Pflegegrad & Hilfsmittel | Antrag, Fristen, Hilfsmittelkosten, Hausnotruf, Rollator | 6 Pflege-Artikel |
| Seniorenwohnung einrichten | Beleuchtung, Türbreiten, Orientierung im Alltag | 2 Wohnen-Artikel + später |

Hinweis: 18 Artikel → 18 Pins auf 4 Boards; jedes Board ≥ 4 Pins zum Start (kein Mini-Board). Reihenfolge so wählen, dass jedes Board beim Start ≥ 4 Pins hat.

## Pin-Reihenfolge & Verifizierung (Tag 1: 6 Pins, dann 2/Tag)

Tag 1 (nach Domain-Claim): treppenlift-kosten, treppenlift-zuschuss, bad-umbau-barrierefrei, pflegegrad-antrag-ablauf-fristen, hausnotruf-kosten-anbieter-vergleich, hilfsmittel-pflegekasse-uebernahme.
Danach 2 Pins/Tag bis 18/18. Pin-Titel ≤ 100 Zeichen, Beschreibung 150–300 Zeichen,hashtags? Nein: 2–3 thematische Hashtags max (z.B. #Treppenlift #Badumbau #Pflegegrad) —Pinterest-Tags haben geringe Wirkung; Keywords im Text zählen.

Pin-Beschreibung = erste Satz des Artikel-Intros (Sie-Form, ohne Hype) + Kernnutzen + URL. Beispiel (treppenlift-kosten):
> „Was gehört in ein Treppenlift-Angebot? Modellrechnung, Folgekosten und Fragenliste für Ihren Fachbetrieb-Termin. Ratgeber: zuhausebleiben-kompass.de/treppenlift-kosten.html“
> Tags: #Treppenlift #Ratgeber

Bild: das SVG des Artikels nach PNG (1000×1500 oder 1000×1000; Pinterest-Ideal 2:3). SVG→PNG-Konvertierung z.B. `rsvg-convert`/Inkscape oder Screenshot-Workflow im Browser (Operator-Entscheidung Tool). KI-Kennzeichnung: Bildbeschreibung im Pin nennt „Schema-Grafik (KI-unterstützt erstellt)“ — konsistent mit image-manifest „KI-Illustration · schematisch“.

## Cadence & Monitoring

- **2 Pins/Tag bis 18**, danach 2–3/Woche (z. B. Repins mit neuem Titel-Winkel, später neue Artikel automatisch).
- Zeitpunkte abends 19–21 Uhr testen; nicht mehr als 3 Pins/Tag (Spam-Signal).
- Analytics im Business-Konto prüfen (Impressions/Saves/Cliccks): nach 2 Wochen erster Readout; nach 4 Wochen gegen GA4 (sobald GA4-Empfang gefixt!) vergleichen. Vorher keine Budget-/Kanalentscheidungen.
- Alle Pin-URLs nach Pin-Erstellung einmal durchklicken (Rich-Pin-Vorschau, korrekte Zielseite).

## Was NOT getan wird (Risikogrenzen)

- Keine Affiliate-Links in Pins/Bio bis Awin-Zusage + Partnerkanal-Freigabe (doppelt abgesichert: Lifta-Antwort + Awin-Programmstatus).
- Keine Gesundheitsversprechen, keine Angst-Visuals, keine „Vorher/Nachher“-Fakes (Tone: ruhig, Sachlich).
- Kein Kauf von Pins/Followern, keine Pin-Farmen, keine Massen-Repins fremder Content-Verdopplung.
- KI-Grafiken nie als Produktfoto/Montage ausgeben (SEO-STRATEGIE Regel 7).

## Abhängigkeiten / To-do vor Tag 1

1. Domain-Verify-Meta-Tag → **Operator-Gate** (Build-Eingriff, mit Deploy koppeln). Ohne Claim: Pinning möglich, aber keine Site-Statistiken & weniger Trust-Badge.
2. SVG→PNG Konvertierung definieren (einmalig, dann Batch-Konvertierung aller 18).
3. Liftstar-Rückfrage (22.10.) um Pinterest-Frage erweitern (Draft in GROWTH-BACKLOG bzw. liftstar-followup-draft.txt ergänzen — Operator entscheidet).
4. GA4-Empfang muss vor Traffic-Auswertung stehen (sonst wird Kanalblindness produziert).
