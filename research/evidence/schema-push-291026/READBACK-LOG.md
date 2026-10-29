# Live-Readback: Schema-Deploy b120a2e — 29.10.2026, ~14:20 CET

Ziel: Verifikation, dass der gestrandete Commit b120a2e (FAQPage-Schema, Organization+WebSite-Graph,
Article-Dates/Author) nach Push + CI (Run success, head_sha b120a2e) tatsächlich auf der
öffentlichen URL ausgeliefert wird.

## Ablauf
1. Lokal: `npm test` komplett grün (Exit 0) vor dem Push eines fremden Commits.
2. Eigenes Schema-Gate `research/verify_schema_push_291026.py` gegen den frischen dist-Build: ALL PASS
   (26/26 ld+json parse-valide, FAQPage 25/25 Artikel, Home-Graph Organization+WebSite,
   datePublished=ISO, keine Zitationsmarker in Schema-Texten, keine Sanitizer-Korruption).
3. Push 3bc269a..b120a2e, CI-Warteschleife: `status=completed, conclusion=success` nach ~2 min.
4. Live-Readback: alle 26 öffentlichen Seiten (25 Ratgeber + Home) via curl gezogen (alle HTTP 200,
   Kopien in diesem Verzeichnis, nach der Verifikation entfernt — reproduzierbar per curl),
   dasselbe Gate mit DIST_DIR auf die Live-Kopien:

## Ergebnis (öffentlich URL, 29.10. ~14:20 CET)
```
ld+json-Bloecke parse-valide: 26
Artikel mit FAQPage-Schema: 25
Home-Graph-Typen: ['Organization', 'WebSite']
ALL PASS
```

## Regressionen (unverändert korrekt)
- robots.txt: Sitemap-Direktive vorhanden
- sitemap.xml: 48 <loc>
- llms.txt: HTTP 200
- rss.xml: 25 <item>

## Audit-Abgleich (seo-audit-zbk, Evidenz-Snapshot 19.10., Analyse 29.10.)
- Fix #1 (FAQPage) und #8 (Org+WebSite Home) und Fix #6a (Article-Dates/Author): **live** (dieser Deploy).
- Finding #2 „llms.txt 404": **veraltet** — live 200 text/plain (seit 21.10. im Build/Deploy).
- Finding #3 „Checklisten orphaned": **veraltet** — Home verlinkt /checklisten/index.html (absoluter
  href; der Audit-Grep auf relative hrefs griff nicht), Hub in Sitemap enthalten.
- Finding #4 „datenschutz.html fehlt in Sitemap": **noch wahr** (0 Treffer in sitemap.xml, Seite
  resolviert 200) — kleinster echter Restfix.
- Weiterhin offen: #5 Region-Seiten verdichten/noindex, #6b PNG/WebP ≥1200 px (og:image-tauglich),
  #7 Titel ≤65 Zeichen + Meta-Descs, #9 pflegegrad-beantragen-Stub, #10 Performance/og-Tags.

## Hinweis
- b120a2e enthält dist/-Churn und die seo-audit-zbk-Evidenz (181 Dateien) vom 11:15-Lauf; bewusst
  nicht zurückgerollt (CI baut dist selbst, Push unwiderruflich nach Verifikation). Konvention
  „nur eigene Dateien stagen" für kommende Commits bestätigt.
