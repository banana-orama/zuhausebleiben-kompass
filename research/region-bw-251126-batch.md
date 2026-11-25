# Batch 26 (2026-11-25): Region BW (Baden-Württemberg) — Recherche-Protokoll (NUR Belege, kein Content)

Subagent-Lauf: Förderlandschaft BW für Wohnraumanpassung (Treppenlift, barrierearmes Bad)
exklusiv aus offiziellen Primärquellen. Schema-Vorgabe wie NRW/Bayern/Sachsen:
Weg 1 Pflegekasse (bundesweit, KEINE Beträge auf der Region-Seite), Weg 2 Landesprogramm,
Weg 3 Eingliederungshilfe, Weg 4 KfW-Stand. **Kern-Aufgabe war der fehlende
Landesprogramm-Beleg für BW — erledigt, siehe unten.**

## Pipeline
1. **L-Bank (Weg 2)**: Produktseite „Zusatzfinanzierung Barrierefreiheit“ + Produktinformationsblatt-PDF (01/25) + Konditionenübersicht-PDF (Stand 20.11.2026) + Z15-Darlehen-schwerbehinderte-Seite live gezogen (curl). Das gesuchte Landesprogramm ist ein **Darlehen bis 50.000 €** (Sollzins 1,00 %, 10 J. Zinsbindung, 3 % Tilgung, 2 tilgungsfreie Anlaufjahre) mit **Tilgungszuschuss 3 %/max. 1.500 € NUR bei vollständiger Barrierefreiheit nach DIN 18040-2**; Zugang (a) mit Z15-Basisförderung (Zusage ≤ 10 J.) oder (b) „Anpassungsförderung“ bei Schwerbehinderung ohne Basisförderung. Treppenlift **0× namentlich** auf der Produktseite — nur „Überwindung von Treppen und Stufen“; Bad = „Maßnahmen an Sanitärräumen“.
2. **Antragsweg Landesprogramm**: service-bw-Leistung 553 (JS-SPA, Browser-Render gesichert; Freigabe MLW 05.03.2026): Wohnraumförderungsstelle im Landratsamt/Bürgermeisteramt, L-Bank-Förderportal (Z15 Online-Antrag), GdB ≥ 50 für die Schwerbehinderten-Route, vorzeitiger Vorhabenbeginn = Ablehnung, keine Antragsfrist, Eigenleistung 25 %/15 %. MLW-Programmseite „Wohnungsbau BW 2022“ + Einkommensgrenzen-Erlass 01.12.2025 (Bezugsgröße 71.000 €, § 10 Abs. 3 LWoFG) inkl. Anlage-Tabelle.
3. **Weg 3 EGH**: § 113/§ 77 SGB IX (gesetze-im-internet, fresh), Sozialministerium-Seite („44 Stadt- und Landeskreise als Träger“), service-bw 1179 gerendert (Sozialamt/Landratsamt, Gesamtplan, Unterlagen, Kosten „keine“ + Einkommens-/Vermögenseinsatz; Freigabe SM 08.01.2026).
4. **Weg 1 Pflegekasse**: § 40 SGB XI (4 180 €/16 720 €-Wortlaut, 3/5-Wochen-Frist, Genehmigungsfiktion) + BMG-Seite (Treppenlifte als Beispielmaßnahme; zweimaliger Zuschuss bei veränderter Pflegesituation) — wie gehabt NUR Kontext für die Region-Seite, keine Beträge aufs Region-Layout.
5. **Beratung**: Pflegestützpunkte BW (Sozialministerium „unabhängig, neutral und kostenlos“ + Träger-Portal „in allen Stadt- und Landkreisen, trägerneutral und kostenfrei“).
6. **Weg 4 KfW**: 455-B weiter gestoppt („Diesen Zuschuss können Sie nicht mehr beantragen.“; 2027-Wiederaufnahme-Bedingung), Kredit 159 läuft (50.000 €/WE, „Treppenlifte, Senkrecht-, Hebe- oder Plattformlifte installieren“, Kombi-Ausnahme mit Pflegekassen-Zuschuss wörtlich).
7. **Kommunales Beispiel (gekennzeichnet)**: service-bw 531 Stadt Friedrichshafen — einziger BW-Beleg mit explizitem „Treppenlift“-Zuschuss (2.500 €, Sanitär 1.500 €), aber „freiwillige Sozialleistung“, „keine öffentlichen Mittel im Sinne des LWoFG“ → nur als Einzelfall-Kennzeichnung verwendbar.

## Verifikation (Subagent-Ebene, maschinell)
- `research/check_quotes_region_bw_251126.py` — **161/161 Zitate PASS** (Soft-Hyphen/Unicode normalisiert; Abschnitte mit Mapping-Warnung).
- `research/check_ledger_region_bw_251126.py` — **127/127 Strings PASS** (Ledger-Quotes + Absenz-Needles gegen Evidenz-Dateien), Ledger-JSON parse-ok, 20 Quellen.
- `research/verify_region_bw_251126_needles.py` — **60/60 PASS**.
- service-bw-Seiten sind JS-SPAs → Texte als `live-servicebw-*-rendered.txt` gesichert (Muster wie amt24 in Sachsen).

## Grenzen / offene Punkte (bewusst dokumentiert)
- **L-Bank Merkblatt + Maßnahmen- und Anforderungskatalog DIN 18040-2 nicht beziehbar**: Download-URLs weder im statischen HTML noch im gerenderten DOM (nur PIB + Konditionen sind echte Links; die übrigen „Download starten“-Buttons führen auf virtuelles-rathaus-Formulare bzw. sind clientseitig aufgelöst); der indexierte binaries-Link antwortet mit 404-Fehlerseite (9 Version-Indizes getestet). → Frage „nennt der Katalog Treppenlifte?“ **offen**; für die Region-Seite nur die Produktseiten-Formulierung verwenden.
- **VwV-Wohnungsbau BW 2022 Volltext** (landesrecht-bw.de, Neufassung 01.04.2025, GABl. 2025 S. 501): React-SPA in dieser Session nicht renderbar (Tab-Navigation hing in L-Bank-Session fest) → Treppenlift-Absenz in der VwV nicht geprüft. Erlasse/PDFs decken die Kernaussagen ab.
- **Einkommensgrenzen-Tabelle (Anlage 3-Ersatz)**: PDF-Spalten-Interleave — nur Betrags-Nadeln gesichert (74.550/78.100/84.050/87.600/93.550/97.100/103.050/106.600 € unter „Berechnungsbeispiele (mit schwerbehinderte/r Person)“); zeilengenaue Personenzahl→Betrag-Zuordnung NICHT belegt, keine zugeordneten Paare publizieren.
- **Konditionenübersicht-PDF** enthält aktuelle Zinszahlen aller Eigentumsförder-Programme → Volatilitäts-Politik der Region-Seiten (NRW/Bayern: 0 Zinszahlen) beibehalten; 1,00 % steht zwar wörtlich auf der offiziellen Produktseite (zitierbar wie SAB-Konditionen in Sachsen), aber PIB verweist für „Aktuelle Zinsen“ auf l-bank.de/z15 — Verfallrisiko dem Parent überlassen.
- **L-Bank-Wartezeit-Banner** („mindestens einem Jahr bis zur Bewilligung“) ist seitenweit, nicht programm-spezifisch — nur mit Abrufdatum zitieren.
- Treppenlift-EGH-Praxis eines einzelnen BW-Landkreises (NRW-Analog Kreis Recklinghausen) nicht recherchiert; service-bw 1179 nennt Treppenlift nicht.

## Evidenz-Bestand (research/evidence/region-bw-251126/, 25.11.2026)
20 Quellen, alle offiziell: l-bank.de ×4 (Produktseite, PIB-PDF, Konditionen-PDF, Z15-schwerbehinderte) + Neubau-Zusatzförderungsseite (Link-Check), service-bw ×3 (553/1179/531, gerendert), mlw.baden-wuerttemberg.de ×3 (Programmseite, Erlass-PDF, Anlage-PDF), sozialministerium.baden-wuerttemberg.de ×2 (EGH, Pflege-Beratung), bw-pflegestuetzpunkt.de, gesetze-im-internet ×3 (§ 113/§ 77 SGB IX, § 40 SGB XI), bundesgesundheitsministerium.de, kfw.de ×3 (455-B, 159, Zuschussportal-Stub), plus landesrecht-Stub/Sitemap/404-Belege. Gesamt 24 abgerufene URLs. Ledger: `research/region-bw-251126-ledger.json`.
