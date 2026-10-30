// Printable checklist hub (link-magnet workstream) — standalone build, does NOT touch generate.mjs.
// Reads the 6 checklist-bearing content-ready JSONs, extracts their checklist bullets and
// comparison tables, and writes dist/checklisten/index.html plus dist/checklisten/<slug>.html.
// Wire-in for the parent: run `node scripts/build-checklists.mjs` after `node generate.mjs`
// (e.g. "build": "node generate.mjs && node scripts/build-checklists.mjs").
import {readFileSync, writeFileSync, mkdirSync} from 'node:fs';
import {join, dirname} from 'node:path';
import {fileURLToPath} from 'node:url';

const ROOT = dirname(dirname(fileURLToPath(import.meta.url)));
const OUT = join(ROOT, 'dist', 'checklisten');
// LAUNCH (--index) mirrors the parent generator's build modes: indexable pages + sitemap
// entries. Without the flag (PREVIEW) everything stays noindex and the sitemap is untouched.
const LAUNCH = process.argv.includes('--index');
const B = JSON.parse(readFileSync(join(ROOT, 'data/content.json'), 'utf8')).brand;
const CSS = readFileSync(join(ROOT, 'design.css'), 'utf8') + readFileSync(join(ROOT, 'cta.css'), 'utf8');
const CONSENT_DEFAULT = readFileSync(join(ROOT, 'consent-default.js'), 'utf8');

// --- Extraction config: one entry per checklist page -------------------------------
// blocks: {t:'ol'|'ul', sec:<section index>} for checklist bullets (numbered steps vs. ticks)
//         {t:'table', sec:<section index>} for the section's comparison/fill-in table.
const CHECKLISTS = [
  {
    slug: 'pflegegrad-antrag-ablauf-fristen',
    pageTitle: 'Checkliste: Pflegegrad-Antrag',
    pageDesc: 'Alle Schritte und Fristen des Pflegegrad-Antrags auf einem Blatt: beantragen, Begutachtung vorbereiten, Fristen der Pflegekasse im Blick.',
    kind: 'Pflegegrad beantragen',
    checklistTitle: 'Checkliste: Pflegegrad-Antrag von Anfang bis Bescheid',
    intro: 'Alle Schritte und Fristen des Pflegegrad-Antrags auf einem Blatt: formlos beantragen, Datum sichern, Begutachtung vorbereiten und die Fristen der Pflegekasse im Blick behalten.',
    howto: 'Haken Sie jeden erledigten Schritt ab. Die Fristen-Tabelle zeigt, was die Pflegekasse nach dem Antrag innerhalb welcher Zeit erledigen muss.',
    blocks: [
      {t: 'ol', sec: 1, title: 'Vor dem Antrag'},
      {t: 'table', sec: 2, title: 'Fahrplan mit allen Fristen nach der Antragstellung'},
      {t: 'ol', sec: 3, title: 'Für das Begutachtungsgespräch'}
    ]
  },
  {
    slug: 'hilfsmittel-pflegekasse-uebernahme',
    pageTitle: 'Checkliste: Hilfsmittel-Kostenübernahme',
    pageDesc: 'Für das Antragsgespräch mit der Pflegekasse: Voraussetzungen prüfen, Produkt benennen, Eigenanteil-Regeln kennen.',
    kind: 'Hilfsmittel',
    checklistTitle: 'Checkliste: Hilfsmittel-Kostenübernahme bei der Pflegekasse',
    intro: 'Das Wichtigste für das Antragsgespräch mit der Pflegekasse: Voraussetzungen prüfen, das richtige Produkt benennen und die Eigenanteil-Regeln kennen, bevor Sie unterschreiben.',
    howto: 'Gehen Sie die Fragen vor dem Anruf oder Schreiben an die Pflegekasse durch. Die Tabellen zeigen den Verfahrensablauf und die Zuzahlungsregeln.',
    blocks: [
      {t: 'ol', sec: 5, title: 'Vorbereitung des Antragsgesprächs'},
      {t: 'table', sec: 2, title: 'Verfahrensablauf und Fristen'},
      {t: 'table', sec: 3, title: 'Eigenanteil: Zuzahlung und Obergrenzen'}
    ]
  },
  {
    slug: 'hausnotruf-kosten-anbieter-vergleich',
    pageTitle: 'Checkliste: Hausnotruf vergleichen',
    pageDesc: 'Monatliche Gebühr, Basistarif, Zusatzleistungen und Vertrag: Hausnotruf-Anbieter nebeneinanderstellen und sehen, was enthalten ist.',
    kind: 'Hausnotruf',
    checklistTitle: 'Checkliste: Hausnotruf-Anbieter vergleichen',
    intro: 'Monatliche Gebühr, Basistarif, Zusatzleistungen und Vertrag: Mit dieser Vergleichscheckliste stellen Sie Hausnotruf-Anbieter Nebeneinander und erkennen, was wirklich enthalten ist.',
    howto: 'Tragen Sie die Antworten je Anbieter in die gleiche Zeile ein. Erst wenn zwei Anbieter alle Punkte schriftlich beantwortet haben, lohnt der Preisvergleich.',
    blocks: [
      {t: 'ul', sec: 5, title: 'Anbieter-Vergleichspunkte zum Abhaken'},
      {t: 'table', sec: 2, title: 'Zusatzleistungen klar vom Basistarif trennen'}
    ]
  },
  {
    slug: 'treppenlift-firmen-vergleich',
    pageTitle: 'Checkliste: Treppenlift-Anbieter',
    pageDesc: 'Drei Betriebe, dieselben Prüfpunkte: Matrix für Aufmaß, Endpreis und Servicekette plus acht Fragen fürs Beratungsgespräch.',
    kind: 'Treppenlift',
    checklistTitle: 'Checkliste: Treppenlift-Anbieter vergleichen (Entscheidungsmatrix + 8 Fragen)',
    intro: 'Drei Betriebe, dieselben Prüfpunkte: Diese Matrix hält Vertragspartner, Aufmaß, Endpreis und Servicekette nebeneinander. Die acht Fragen ergänzen das Beratungsgespräch.',
    howto: 'Drucken Sie die Matrix einmal pro Besuch aus und notieren Sie die Antworten zu Betrieb A, B und C. Entscheidend ist der Endpreis für den beschriebenen Umfang – nicht der Einstiegspreis.',
    blocks: [
      {t: 'table', sec: 6, title: 'Entscheidungsmatrix für bis zu drei Betriebe'},
      {t: 'ol', sec: 7, title: 'Acht Fragen für das Beratungsgespräch'},
      {t: 'ul', sec: 4, title: 'Servicekette vor dem Auftrag klären'}
    ]
  },
  {
    slug: 'tuerbreiten-schwellen-schnellcheck',
    pageTitle: 'Checkliste: Türbreiten & Schwellen',
    pageDesc: 'Messbogen für den Wohnungsrundgang: lichte Breiten, Schwellenhöhen und Bewegungsflächen in einem Durchgang erfassen.',
    kind: 'Türen & Schwellen',
    checklistTitle: 'Checkliste: Türbreiten und Schwellen schnell prüfen (Messbogen)',
    intro: 'Der Messbogen für den Rundgang durch die Wohnung: lichte Breiten, Schwellenhöhen und Bewegungsflächen in einem Durchgang erfassen – als Grundlage für Vermieter, Fachbetrieb und Pflegekassen-Antrag.',
    howto: 'Legen Sie Maßband oder Zollstock bereit und gehen Sie Tür für Tür vor. Übertragen Sie die Werte später in den Pflegekassen-Antrag; der Antrag kommt vor dem Auftrag.',
    blocks: [
      {t: 'ul', sec: 0, title: 'Messprotokoll: In fünf Minuten erfasst'},
      {t: 'table', sec: 2, title: 'Schwellen entschärfen: Ansatz je Ausgangslage'},
      {t: 'ul', sec: 6, title: 'Der Schnell-Check in einem Durchgang'}
    ]
  },
  {
    slug: 'badumbau-angebote-vergleichen',
    pageTitle: 'Checkliste: Badumbau-Angebote',
    pageDesc: 'Kostenaufstellungen Position für Position abgleichen und Fragen pro Betrieb — für vergleichbare Badumbau-Angebote.',
    kind: 'Badumbau',
    checklistTitle: 'Checkliste: Badumbau-Angebote vergleichen (Positionen + Fragen)',
    intro: 'Angebote für denselben Umbau können tausende Euro auseinanderliegen. Diese Checkliste gleicht Kostenaufstellungen Position für Position ab und liefert die Fragen pro Betrieb.',
    howto: 'Fordern Sie zunächst bei jedem Betrieb ein Angebot für dieselbe Beschreibung an. Prüfen Sie dann mit der Positionstabelle, was wirklich enthalten ist – und fragen Sie Lücken an, statt sie zu übersehen.',
    blocks: [
      {t: 'table', sec: 2, title: 'Kostenaufstellung Position für Position lesen'},
      {t: 'ol', sec: 7, title: 'Ihre Fragen pro Betrieb'},
      {t: 'ul', sec: 0, title: 'Kurz beantwortet: So vergleichen Sie richtig'}
    ]
  }
];

const esc = s => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const url = p => B.base_url.replace(/\/$/, '') + p;

// Inline citation markers [n] become superscripts that link into the source article's
// reference list (the checklist page itself repeats no sources; the article is the source).
const txt = s => esc(s).replace(/\[(\d+)\]/g, (m, n) => `<sup class="cite">[${n}]</sup>`);

const mark = `<svg class="brand-mark" viewBox="0 0 48 48" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M7 23 24 8l17 15M12 20v21h24V20M20 41V28h8v13"/><path d="m16 19 8-7 8 7"/></svg>`;

const CHECK_CSS = `
.check-hero{margin:6px 0 10px}
.check-hero .lead{max-width:760px}
.check-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:22px;margin:30px 0 40px;padding:0}
.check-card{background:#fff;border:1px solid var(--line);border-radius:4px;padding:24px;display:flex;flex-direction:column;gap:10px}
.check-card h2{font-size:22px;margin:0}
.check-card p{margin:0;font-size:16px;color:var(--muted);flex-grow:1}
.check-card .kind{font-size:13px;letter-spacing:2px;font-weight:700;text-transform:uppercase;color:var(--green)}
.check-card .to-article{font-size:15px}
.check-block{background:#fff;border:1px solid var(--line);border-radius:4px;padding:26px 28px;margin:0 0 26px}
.check-block h2{margin-top:4px}
.check-block>ol>li,.check-block>ul>li{margin-bottom:12px}
.check-block li::marker{color:var(--green);font-weight:700}
.check-block .checklist li{list-style:none;position:relative;padding:8px 0 8px 38px;border-bottom:1px solid var(--sand)}
.check-block .checklist li:last-child{border-bottom:0}
.check-block .checklist li::before{content:"";position:absolute;left:0;top:12px;width:20px;height:20px;border:2px solid var(--green);border-radius:3px;background:#fff}
.fill-line{display:inline-block;min-width:130px;border-bottom:1px solid var(--ink);vertical-align:baseline}
.check-meta{display:flex;flex-wrap:wrap;gap:12px 28px;align-items:center;background:var(--sand);border-radius:4px;padding:14px 18px;margin:0 0 26px;font-size:15px}
.check-meta span{display:inline-flex;align-items:center;gap:8px}
.check-meta .box{width:15px;height:15px;border:1.5px solid var(--muted);border-radius:3px;display:inline-block}
.source-back{background:#e8ede5;border-radius:4px;padding:20px 24px;margin:10px 0 34px;font-size:16px}
.source-back a{font-weight:600}
.print-hint{font-size:14px;color:var(--muted);margin:0 0 8px}
.check-footer{margin-top:40px;padding-top:18px;border-top:1px solid var(--line);font-size:14px;color:var(--muted);line-height:1.7}
.check-footer a{color:var(--green)}
.check-headerline{display:flex;flex-wrap:wrap;justify-content:space-between;gap:10px 24px;border-bottom:2px solid var(--ink);padding-bottom:10px;margin:0 0 22px;font-size:13px;letter-spacing:.05em;text-transform:uppercase;color:var(--muted)}
.check-headerline strong{color:var(--ink);letter-spacing:0;text-transform:none;font-size:15px}
@media print{
  @page{size:A4;margin:16mm 14mm}
  html{font-size:12pt}
  body{background:#fff;font-size:12pt;line-height:1.5}
  .topline,header.site-header,.skip,.print-button,.no-print,footer.site-footer{display:none!important}
  main{max-width:none;padding:0;margin:0}
  a{color:inherit;text-decoration:none}
  .check-card{break-inside:avoid;border-color:#bbb}
  .check-block{border:0;border-top:1px solid #999;border-radius:0;padding:14px 0 4px;break-inside:auto;margin-bottom:10px}
  .check-block li::marker{color:#333}
  .check-block .checklist li::before{border-color:#333;background:#fff}
  .check-meta{background:#f0f0f0;color:#000}
  .check-footer{position:fixed;bottom:0;left:0;right:0;border-top:1px solid #999;font-size:8.5pt;padding-top:4pt;text-align:left}
  h1{font-size:24pt;margin:14px 0}
  h2{font-size:15pt;break-after:avoid}
  tr{break-inside:avoid}
  .check-grid{grid-template-columns:1fr 1fr;gap:14px}
}
`;

// --- Content extraction ------------------------------------------------------------
function loadArticle(slug) {
  const a = JSON.parse(readFileSync(join(ROOT, 'content-ready', slug + '.json'), 'utf8'));
  if (a.status !== 'editorial-reviewed-preview') throw new Error('Not reviewed: ' + slug);
  return a;
}

function extractBlock(a, block, i) {
  const sec = a.sections[block.sec];
  if (!sec) throw new Error(a.slug + ': missing section ' + block.sec);
  let inner = '';
  if (block.t === 'ol' || block.t === 'ul') {
    if (!Array.isArray(sec.bullets) || !sec.bullets.length) throw new Error(a.slug + ': no bullets in section ' + block.sec);
    if (block.t === 'ol') {
      inner = `<ol>${sec.bullets.map(b => `<li>${txt(b)}</li>`).join('')}</ol>`;
    } else {
      // Fill-in blanks ("____") get a visible writable line for the printed sheet.
      const line = b => txt(b).replace(/_{3,}/g, '<span class="fill-line" aria-hidden="true"></span>');
      inner = `<ul class="checklist">${sec.bullets.map(b => `<li>${line(b)}</li>`).join('')}</ul>`;
    }
  } else if (block.t === 'table') {
    const tbl = sec.table;
    if (!tbl?.headers?.length) throw new Error(a.slug + ': no table in section ' + block.sec);
    inner = `<div class="table-scroll" role="region" aria-label="${esc(block.title)}" tabindex="0"><table><thead><tr>${tbl.headers.map(h => `<th scope="col">${txt(h)}</th>`).join('')}</tr></thead><tbody>${tbl.rows.map(r => `<tr>${r.map(c => `<td>${txt(c)}</td>`).join('')}</tr>`).join('')}</tbody></table></div><span class="tbl-cap">Tabelle aus dem Ratgeber; ausführliche Erläuterungen dort.</span>`;
  } else throw new Error('unknown block type ' + block.t);
  return `<section class="check-block" id="block-${i + 1}"><h2>${esc(block.title)}</h2>${inner}</section>`;
}

// --- Page shells (same head contract as generate.mjs: CMP default, local CSS, no external scripts)
function shell({title, desc, path, body, articlePath, articleTitle}) {
  return `<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${esc(title)}</title><meta name="description" content="${esc(desc)}"><meta name="robots" content="${LAUNCH ? 'index,follow' : 'noindex,follow'}"><link rel="canonical" href="${esc(url(path))}"><meta property="og:title" content="${esc(title)}"><meta property="og:description" content="${esc(desc)}"><script>${CONSENT_DEFAULT}</script><link rel="stylesheet" href="/assets/vendor/cookieconsent.css"><style>${CSS}${CHECK_CSS}</style><script type="module" src="/assets/consent.mjs"></script></head><body><a class="skip" href="#inhalt">Direkt zum Inhalt</a><div class="topline">Orientierung für ältere Menschen und ihre Angehörigen · Ratgeber im Aufbau</div><header class="site-header"><a class="brand" href="${url('/')}">${mark}<span>ZuhauseBleiben<small>Der Umbau-Kompass</small></span></a><nav aria-label="Hauptnavigation"><a href="${url('/treppenlift-kosten.html')}">Treppenlift</a><a href="${url('/bad-umbau-barrierefrei.html')}">Bad-Umbau</a><a href="${url('/treppenlift-zuschuss.html')}">Förderung</a><a href="${url('/checklisten/index.html')}">Checklisten</a></nav></header><main id="inhalt"><div class="article-body">${body}</div></main><footer class="site-footer"><div class="footer-inner"><div><span class="footer-title">Ein Zuhause, das zu Ihrem Leben passt.</span><p style="margin-top:14px">ZuhauseBleiben Kompass bietet eine erste Orientierung zu Treppenliften und barrierearmem Umbau. Keine technische, medizinische oder rechtliche Einzelfallberatung.</p></div><div><p>Dieser Ratgeber-Internetauftritt befindet sich im weiteren Aufbau; die Angebotsvermittlung ist noch nicht eingerichtet. Wie diese Seite arbeitet und misst, beschreibt die <a href="${url('/datenschutz.html')}">Datenschutzerklärung</a>.</p><div class="footer-links"><a href="${url('/impressum.html')}">Impressum</a><a href="${url('/datenschutz.html')}">Datenschutz</a><a href="${url('/#ueber-uns')}">Transparenz</a></div></div></div><div class="consent-controls"><button type="button" data-consent-settings>Datenschutzeinstellungen</button><button type="button" data-consent-withdraw>Einwilligung widerrufen</button><span data-consent-status role="status" aria-live="polite"></span><noscript>Ohne JavaScript ist keine optionale Messung aktiv; es wird keine Einwilligung gespeichert.</noscript></div></footer></body></html>`;
}

const today = () => new Date().toISOString().slice(0, 10);

function checkFooter(a) {
  if (!a.slug) return `<div class="check-footer">© ${new Date().getFullYear()} ZuhauseBleiben Kompass · Tobias Batke, ${esc(B.operator.postal_code)} ${esc(B.operator.city)} · Erstellt mit KI-Unterstützung, redaktionell geprüft · Stand: ${esc(a.sources[0].checked_at)} · Allgemeine Orientierung, keine individuelle Beratung · ${url('/checklisten/')}</div>`;
  return `<div class="check-footer">© ${new Date().getFullYear()} ZuhauseBleiben Kompass · Tobias Batke, ${esc(B.operator.postal_code)} ${esc(B.operator.city)} · Quelle: <a href="${url('/' + a.slug + '.html')}">${esc(a.h1)}</a> · Erstellt mit KI-Unterstützung, redaktionell geprüft · Stand: ${esc(a.sources[0].checked_at)} · Allgemeine Orientierung, keine individuelle Beratung · ${url('/checklisten/')}</div>`;
}

// --- Individual checklist pages -----------------------------------------------------
const pages = [];
for (const cfg of CHECKLISTS) {
  const a = loadArticle(cfg.slug);
  const articlePath = url('/' + a.slug + '.html');
  const blocks = cfg.blocks.map((b, i) => extractBlock(a, b, i)).join('');
  const printButton = `<button class="print-button no-print" type="button" onclick="window.print()">Checkliste drucken</button>`;
  const backLink = `<p class="no-print" style="margin-top:34px"><a href="${url('/checklisten/index.html')}">← Alle Checklisten im Überblick</a></p>`;
  const body = `
<p class="no-print"><a class="fine" href="${url('/')}">Startseite</a> / <a href="${url('/checklisten/index.html')}">Checklisten</a></p>
<p class="eyebrow">${esc(cfg.kind)}</p>
<h1>${esc(cfg.checklistTitle)}</h1>
<div class="check-hero"><p class="lead">${esc(cfg.intro)}</p></div>
${printButton}
<p class="print-hint no-print">Drucken ergibt ein A4-Arbeitsblatt mit Abhakkästchen, Schreiblinien und Quellenangabe – ohne Navigation und ohne Banner.</p>
<div class="check-headerline"><span><strong>${esc(a.h1)}</strong></span><span>Checkliste · Stand ${esc(a.sources[0].checked_at)}</span></div>
<div class="source-back"><strong>Woher stammt diese Checkliste?</strong> Aus dem ausführlichen Ratgeber <a href="${articlePath}">${esc(a.h1)}</a>. Dort finden Sie alle Begründungen, Quellen und Grenzen — diese Übersicht ersetzt die Lektüre nicht.</div>
${blocks}
<div class="check-meta"><span><span class="box" aria-hidden="true"></span>Erledigt am: <span class="fill-line"></span></span><span>Von: <span class="fill-line"></span></span></div>
${backLink}
<p class="fine no-print">Bullets in eckigen Klammern verweisen auf die Quellenliste im zugehörigen Ratgeber. Allgemeine Orientierung für ältere Menschen und Angehörige, keine individuelle rechtliche, medizinische oder pflegerische Beratung.</p>
${checkFooter(a)}`;
  pages.push({file: join(OUT, cfg.slug + '.html'), html: shell({title: (cfg.pageTitle || cfg.checklistTitle) + ' — ZuhauseBleiben Kompass', desc: cfg.pageDesc || cfg.intro, path: '/checklisten/' + cfg.slug + '.html', body}), a, cfg});
}

// --- Overview page -------------------------------------------------------------------
{
  const body = `
<p class="no-print"><a class="fine" href="${url('/')}">Startseite</a> / Checklisten</p>
<h1>Checklisten zum Ausdrucken.</h1>
<div class="check-hero"><p class="lead">Sechs Arbeitsblätter aus unseren Ratgebern: zum Abhaken, Eintragen und Mitnehmen zum Gespräch — mit Pflegekasse, Handwerker oder Anbieter. Kostenlos, ohne Kontaktformular, ohne Anmeldung.</p></div>
<button class="print-button no-print" type="button" onclick="window.print()">Diese Übersicht drucken</button>
<ul class="check-grid">
${CHECKLISTS.map(cfg => {
    return `<li class="check-card"><span class="kind">${esc(cfg.kind)}</span><h2><a href="${url('/checklisten/' + cfg.slug + '.html')}">${esc(cfg.checklistTitle.replace(/^Checkliste: /, ''))}</a></h2><p>${esc(cfg.intro)}</p><p class="to-article"><a href="${url('/' + cfg.slug + '.html')}">Zum zugehörigen Ratgeber →</a></p></li>`;
  }).join('\n')}
</ul>
<div class="check-block no-print"><h2>Warum es diese Checklisten gibt</h2><p>Gute Entscheidungen brauchen Vorbereitung — und Vorbereitung braucht etwas zum Anfassen. Jede Checkliste stammt aus einem ausführlichen Ratgeber auf dieser Website und bündelt dessen prüfenden Fragen, Fristen und Vergleichspunkte. Alle Inhalte sind allgemeine Orientierung; maßgeblich bleiben die Auskünfte der zuständigen Stellen und Betriebe.</p><p>Sie möchten die Zusammenhänge verstehen, bevor Sie abhaken? Jede Checkliste verlinkt auf den vollständigen Ratgeber mit Quellen und Erläuterungen.</p></div>
${checkFooter({slug: '', h1: 'Checklisten-Übersicht', sources: [{checked_at: today()}]})}
<script type="application/ld+json">{"@context":"https://schema.org","@graph":[{"@type":"CollectionPage","name":"Checklisten zum Ausdrucken","description":"Sechs druckbare Checklisten zu Pflegegrad-Antrag, Hilfsmittel, Hausnotruf, Treppenlift, Türen und Badumbau.","url":"${url('/checklisten/index.html')}","inLanguage":"de","isPartOf":{"@type":"WebSite","name":"ZuhauseBleiben Kompass","url":"${url('/')}"}},{"@type":"ItemList","itemListElement":[${CHECKLISTS.map((cfg, i) => `{"@type":"ListItem","position":${i + 1},"name":"${esc(cfg.checklistTitle.replace(/^Checkliste: /, ''))}","url":"${url('/checklisten/' + cfg.slug + '.html')}"}`).join(',')}]}]}</script>`;
  pages.push({file: join(OUT, 'index.html'), html: shell({title: 'Checklisten zum Ausdrucken — ZuhauseBleiben Kompass', desc: 'Sechs kostenlose druckbare Checklisten: Pflegegrad-Antrag, Hilfsmittel, Hausnotruf, Treppenlift, Tür-Messbogen und Badumbau — ohne Anmeldung.', path: '/checklisten/index.html', body})});
}

mkdirSync(OUT, {recursive: true});
for (const p of pages) writeFileSync(p.file, p.html);
// LAUNCH only: mirror the checklist pages into the parent generator's sitemap. Idempotent —
// generate.mjs does not clean dist, so any previously appended checklist URLs are stripped first.
if (LAUNCH) {
  const sitemapPath = join(ROOT, 'dist', 'sitemap.xml');
  let sm = readFileSync(sitemapPath, 'utf8');
  sm = sm.replace(/<url><loc>[^<]*\/checklisten\/[^<]*<\/loc><\/url>/g, '');
  const paths = ['/checklisten/index.html', ...CHECKLISTS.map(c => '/checklisten/' + c.slug + '.html')];
  sm = sm.replace('</urlset>', paths.map(p => `<url><loc>${url(p)}</loc></url>`).join('') + '</urlset>');
  writeFileSync(sitemapPath, sm);
  console.log(`Sitemap: ${paths.length} checklist URLs included.`);
}
console.log(`Built ${pages.length} checklist pages in dist/checklisten (${CHECKLISTS.length} checklists + overview). Mode: ${LAUNCH ? 'LAUNCH index' : 'PREVIEW noindex'}.`);
