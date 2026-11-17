# Aroundhome-Partner-Thread: Stand 16.11.2026 (Einladung zum Test)

Quelle: Postfach-Verlauf, Belege `research/evidence/aroundhome-161126/` (Roh-Mail 11234).

## Verlauf (5 Nachrichten)

1. **13.11. 08:25 (ID 11233, Katharina Folker, Artefact):** Antwort auf die Bewerbung mit vier Qualifizierungsfragen (Volumen, Kanäle, Integration, Sitz). Unsere Antwort am 13.11. (Sent 1024): ehrliche Volumenangabe (neues Portal, keine erfundenen Leadzahlen), 100 % organisch, Präferenz **Textlinks über Awin** (deeplinks via cread.php auf Badezimmer-Kategorie), **„Kein iFrame, keine API-Leadübernahme — aus Überzeugung: Wir sammeln auf unserer Seite bewusst keinerlei Interessentendaten"**, DE-Sitz (Kleingewerbe Tobias Batke, Nümbrecht), Hinweis „Bewerbung auf Advertiser 68536 ist im Netzwerk eingereicht".
2. **16.11. 07:31 (ID 11234, Katharina Folker):** **Einladung zum Test**: „Dann lass uns das gerne testen, am Besten über Awin. Hier unser Profillink: https://ui.awin.com/merchant-profile/68536". Kernfakten wörtlich:
   - „Wir haben dort sowohl Banner, Textlinks als auch iFrames. Die iFrames konvertieren mit Abstand am Besten. Dort sind die Aroundhome-Fragebögen eingebunden, und der Kunde kann direkt auf deiner Seite alles ausfüllen und abschicken.  Deeplinking ist nicht freigeschaltet."
   - „Über Awin erhältst du einen Umsatzanteil von 30 %." (Revenue Share: Partner liefert Leads → Aroundhome qualifiziert intern im Callcenter → „sofern Kundenwünsche und Partner zueinander passen, wird dieser Lead gematcht. Die gematchten Leads führen zu einem direkten Umsatz, der zu fairen Sharings mit den Affiliate-Partnern geteilt wird.")
   - Frage: „Was meinst du, passt das so für dich?"
3. **16.11. (Sent 1026):** Antwort gesendet: Test über Awin bestätigt (Bewerbung liegt bereits vor, Freigabe im Netzwerk genügt), **Textlink-Start**, iFrame abgelehnt (Grundsatz aus Sent 1024 bekräftigt), drei offene Fragen gestellt: (a) erlaubte Zielseiten für Textlinks ohne Deeplink-Freischaltung (z. B. feste Badezimmer-Landingpage?), (b) Matching-Kriterien des Callcenters, (c) sinnvoller Testzeitraum.
4. **17.11. 08:45 (ID 11236, Katharina Folker; Roh-Mail `research/evidence/partner-terms-171126/aroundhome-publisher-id-11236.txt`):** „schick uns bitte einmal deine Publisher id. Leider kann ich deine Bewerbung nicht bei uns finden." — **die bislang als „eingereicht" geführte Bewerbung ist auf Agency-Seite nicht auffindbar.** Keine Beantwortung der drei offenen Fragen.
5. **17.11. (Sent 1027, Entwurf `operations/aroundhome-reply-171126.eml`):** Publisher-ID **3124891** (Account Tobias Batke, Portal zuhausebleiben-kompass.de) nachgereicht mit Bitte um direkte Freischaltung über die ID, falls die Bewerbung nicht auftaucht; Hinweis, dass die drei offenen Fragen (Zielseite, Matching, Zeitraum) parallel geklärt werden können.

## Bedeutung für den Partnerblocker

- Aroundhome ist damit der **zweite monetarisierte Pfad** neben Malteser — und der erste für den **Bad-Cluster** (badumbau-angebote-vergleichen, wanne-zu-dusche, bodengleiche-dusche-altbau, hilfsmittel-dusch-wc).
- Wirtschaftlich bleibt es eine Hypothese: 30 % vom Umsatz **gematchter** Leads, keine Fix-CPL-Zusage; Erlös je akzeptiertem Lead unbekannt bis zur ersten Abrechnung. Keine Prognose ableitbar (gleiche Regel wie 23.10.-Scan).
- **Deeplinking nicht freigeschaltet** ⇒ die geplanten cread.php-DeepLinks auf Kategorie-/Artikelebenen funktionieren nicht; CTA-Ziel muss eine von Aroundhome benannte Zielseite sein (Frage gestellt). `data/partner-links.json` bleibt approved=false bis zum Netzwerk-Readback (Freigabe im Awin-Login oder Analytics-Zugang).
- **iFrame-Angebot abgelehnt** (dokumentierter Grundsatz): Ein eingebetteter Fremd-Fragebogen würde Interessentendaten optisch auf unserer Seite sammeln → consent-gated Loader, DSE-Amendment und Betreiber-Entscheid nötig, bevor darüber überhaupt nachgedacht wird. Aus eigener Grenze: Gesundheits-/Pflegeangaben kommen nicht in Formulare auf unserer Seite.

## Aktivierungspfad (nach Netzwerk-Freigabe)

1. Freigabe-Readback aus dem Awin-Login („Leave Programme"-Link + freigeschaltete Creatives), wie bei Malteser dokumentiert.
2. Tracker/Link-Format: ohne Deeplinking vermutlich Standard-Textlink `awin1.com/cread.php?awinmid=68536&awinaffid=3124891&ued=<Zielseite>` — Zielseite lt. Agency-Antwort; 302-Readback auf die Destination mit `awc`-Parameter, dann erst Config.
3. `data/partner-links.json`: approved=true + approval_readback + Zielseite + placements NUR auf Bad-Cluster-Artikeln (Cluster-Regel des Renderer-Gates), kompensation_note auf „30 % Revenue Share auf gematchte Leads (Agency 16.11.)" aktualisieren.
4. DSE_META-Eintrag (Awin-DSE verlinkt, Cookie 30 T., geprüft-Datum) im selben Commit; Gate F bricht sonst den Build.
