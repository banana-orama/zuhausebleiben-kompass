# Aroundhome DE (Awin 68536) — Ablehnung + Fix + Cooldown (Stand 19.11.)

**19.11. Ablehnung:** Grund laut Panel: „Kein vollständiges Impressum (USt-IdNr. bzw. Kleinunternehmer-Status fehlen)".
**Fix 19.11. (live, CI 44533904631):** Impressum um USt-IdNr. DE305157036 (§ 27a UStG) ergänzt (Nutzer-Angabe 19.11., Widget-Antwort);
veraltete Aussage „Angebotsvermittlung ist noch nicht eingerichtet" aus Impressum + Footer + 40 Artikel-Leadzeilen entfernt
(ersetzt durch korrekte Affiliate-Kennzeichnungs-Angabe). Wichtig: neues Impressum-Wording ohne rohes rel="sponsored"-Attribut
(Partner-Marker-Gate). Cooldown im Panel: erneute Bewerbung erst **20.12.2026**.
**Artefact-Kommunikation:** Impressum-Fix-Mail 19.11. (SMTP 250) + Invite-Bitte (Programm-Einladung an PID 3124891 umgeht
die Sperrfrist) 19.11. (SMTP 250, CC Leidloff/Frank/Babajeva).
**Plan A:** Artefact lädt ein → sofort Platzierungen (partner-links.json Gate). **Plan B:** Re-Apply 20.12. mit Traffic-Update.

## Update 23.11.: Einladung angenommen (Nutzerbestätigung, NICHT plattform-verifiziert)

- Tobias hat die Awin-Einladung (Aroundhome DE 68536) selbst angenommen (Nutzerbestätigung an Jarvis 23.11.).
- Plattform-Readback aussteht: in dieser Sitzung keine GUI/Preview-Verfügbarkeit (TUI), kein Awin-API-Token konfiguriert (Keychain gesperrt, exit 36). Kein iPhone-Login als Mac-Session angenommen.
- Verifizierungspfad: Hermes-Desktop-Preview → ui.awin.com (Login tobias.batke@gmail.com) → merchant-profile/68536 → Status muss „Leave Programme" zeigen (vs. „Bewerbung offen" bzw. „Einladung"). Danach Tracker: awin1.com/cread.php?awinmid=68536&awinaffid=3124891&ued=<Landingpage> (30% Revenue Share, Cookie 30 Tage, Autobest. 30 Tage, Validierung ~8 Tage lt. Profil-Readback 17.11.).
- Nächster Aktivierungsschritt (Gate-Verfahren, nur nach Freigabe): Tracker verifizieren (302-Kette) → data/partner-links.json: aroundhome approved=true + placements (Badumbau-Cluster: bad-umbau-barrierefrei, wanne-zur-dusche, bodengleiche-dusche-altbau, badumbau-angebote-vergleichen, hilfsmittel-dusch-wc-uebernahme) → npm run test:partner → Deploy → Live-Readback. CTA-Text wegen Revenue-Share: „Kostenloses Angebot einholen" (kein CPL-Wert nennen).
- Blocker: GUI-Session fehlt in TUI-Kontext; Aktivierung blockiert bis Readback + Freigabe.

## Update 25.11. (Cron 09:23): Bestätigungsanfrage an Artefact gesendet (Sent 1033)

- Der Playbook-Beleg-Standard („Agency-Mail-Beleg ODER Awin-Login-Status 'zugelassen'") ist mit der reinen Nutzerbestätigung NICHT erfüllt → kein sichtbarer Link, kein Aktivierungs-Commit.
- Bestätigungsanfrage im bestehenden Thread gesendet: **Sent 1033** (25.11., 09:40, `operations/aroundhome-confirm-251126.eml`), To Katharina Folker, CC Leidloff/Frank/Babajeva + aroundhome@artefact.com. Bitte: bestätigen, dass die Partnerschaft für Publisher 3124891 zu AID 68536 aktiv angezeigt wird.
- **Ihre Antwort = fehlender Beleg → dann sofort Aktivierungs-Commit nach operations/aroundhome-activation-prep.md** (partner-links.json + DSE_META, Dry-Run 22/22 bereit, Gates + Live-Readback im Playbook). Entspricht dem in der Bestätigungsmail zugesagten Ablauf („Sobald wir diese Bestätigung haben, setzen wir die vorbereitete Textlink-Strecke live").
- Fallback, falls bis 20.12. keine Beleglage entsteht: Re-Apply-Pfad (Plan B) bleibt unverändert.
