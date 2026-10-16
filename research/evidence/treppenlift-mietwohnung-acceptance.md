# Freigabeprotokoll: Inhaltliche Selbstprüfung Artikel treppenlift-mietwohnung

Datum: 2026-10-16. Prüfer: Agent-Lauf (Hermes/GLM). Gegenstand: content-ready/treppenlift-mietwohnung.json vor Integration in den Renderer.

## Behauptungen gegen Live-Originale (Stichprobe jeder Kernaussage)

| # | Behauptung im Artikel | Beleg | Ergebnis |
|---|---|---|---|
| 1 | Mieter können Erlaubnis verlangen (§ 554 I 1) | bgb554.html (Abruf 16.10.) | wörtlich verifiziert |
| 2 | Zumutbarkeitsvorbehalt (§ 554 I 2) | bgb554.html | wörtlich verifiziert |
| 3 | Besondere Sicherheitsleistung möglich (§ 554 I 3) | bgb554.html | wörtlich verifiziert |
| 4 | Abweichende Vereinbarung unwirksam (§ 554 II) | bgb554.html | wörtlich verifiziert |
| 5 | Bauliche Veränderungen durch Beschluss (§ 20 I WEG) | weg20c.html | wörtlich verifiziert |
| 6 | Anspruch bei Menschen mit Behinderungen (§ 20 II WEG) | weg20c.html | wörtlich verifiziert |
| 7 | Zuschuss subsidiär/Ermessen, max. 4.180 € (§ 40 IV SGB XI) | sgb40.html | wörtlich verifiziert |
| 8 | Fristen 3/5 Wochen + Genehmigungsfiktion (§ 40 VII SGB XI) | sgb40.html | wörtlich verifiziert |
| 9 | Mehrparteienhaus: Miteigentümer/andere Mieter + Baugenehmigung je Bundesland | vz-treppenlifte.html / vz-PDF | wörtlich verifiziert |
| 10 | Erlaubnis des Eigentümers bei Miete | vz-Entscheidungshilfe-PDF | wörtlich verifiziert |
| 11 | Festpreis vs. Kostenvoranschlag 20 % | vz-treppenlifte.html | wörtlich verifiziert |
| 12 | Brandschutz häufigster Ablehnungsgrund; Antrag konkret (Modell/Firma/Strom); Rückbaupflicht | pflegenet-mietwohnung.txt | wörtlich verifiziert |
| 13 | Sicherheit getrennt von Kaution; AG Pankow 2012 als Portalangabe | treppenliftwissen.txt | wörtlich verifiziert (Urteil selbst nicht im Volltext geprüft — im Artikel offen ausgewiesen) |
| 14 | Erlaubnis vor Förderantrag | treppenliftwissen.txt | wörtlich verifiziert |

## Ethische/compliance Checks

- Keine Erfolgs- oder Bewilligungszusage (Pflegekasse: „kann“, „Ermessen“, „keine Zusage“ im Text).
- Keine Rechtsberatung: mehrfach explizit; Interpretationen mit `*` markiert (Legende im Renderer: „*“ = redaktionelle Ergänzung).
- Keine Gesundheitsdaten, kein Formular, keine Partnerlinks, keine Angebotsvermittlung.
- Betreiber transparent benannt (Renderer-Metazeile), KI-Unterstützung ausgewiesen.
- KI-Grafik als „Schematische KI-Illustration“ gecaptioned; keine Montage/Kundenreferenz behauptet.
- Sie-Ansprache durchgehend; kurze Sätze; Tabelle nur als Vergleichsstruktur; keine Angstwerbung.

## Technische Checks

- Slug einzigartig (kein Duplikat in content-ready), Muster ^[a-z0-9-]+$.
- 8 Sektionen, 6 FAQs, 7 Quellen mit checked_at 2026-10-16, Bild-Pfad assets/images/, viewBox 1000×780 → Renderer-Dims OK.
- Alle Inline-Zitate [1]–[7] existieren in a.sources (Renderer würde sonst werfen).
- Anchor: TOC #abschnitt-1..8 vorhanden (test_articles.py prüft alle Refs).
- Build-Zähler test_articles.py 11→12 im selben Commit.

Ergebnis: FREIGEGEBEN für Renderer-Integration (Status editorial-reviewed-preview, Launch-Index wie bestehende Ratgeber; Webseite bleibt im Launch-Modus, Formular deaktiviert).
