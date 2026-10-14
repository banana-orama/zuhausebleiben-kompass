// ZuhauseBleiben-Kompass — Seitengenerator
// Aus data/content.json -> statische Seiten in dist/ (GitHub-Pages-kompatibel)
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = dirname(fileURLToPath(import.meta.url));
const OUT = join(ROOT, "dist");
const C = JSON.parse(readFileSync(join(ROOT, "data/content.json"), "utf8"));
const B = C.brand;

const esc = (s) => String(s ?? "").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
const url = (p="/") => `${B.base_url}${p}`;
const STAND = esc(B.stand);

const FORM = `
<section class="leadbox" id="angebote">
  <h2>Kostenlose Angebote einholen</h2>
  <p>Unverbindlich &amp; kostenlos: Passende Fachbetriebe aus deiner Region melden sich mit Angebot — max. 3, kein Telefonterror.</p>
  <form class="leadform" method="POST" action="${esc(B.form_endpoint)}">
    <label>PLZ <input name="plz" required pattern="[0-9]{5}" inputmode="numeric" placeholder="z. B. 44135"></label>
    <label>Bundesland
      <select name="bundesland" required>
        <option>Baden-Württemberg</option><option>Bayern</option><option>Berlin</option><option>Brandenburg</option>
        <option>Bremen</option><option>Hamburg</option><option>Hessen</option><option>Mecklenburg-Vorpommern</option>
        <option>Niedersachsen</option><option>Nordrhein-Westfalen</option><option>Rheinland-Pfalz</option>
        <option>Saarland</option><option>Sachsen</option><option>Sachsen-Anhalt</option>
        <option>Schleswig-Holstein</option><option>Thüringen</option>
      </select>
    </label>
    <label>Was brauchst du?
      <select name="thema" required>
        <option>Treppenlift</option>
        <option>Barrierefreier Bad-Umbau</option>
        <option>Beides / Wohnraumanpassung komplett</option>
        <option>Noch unklar — erst beraten lassen</option>
      </select>
    </label>
    <label>Pflegegrad vorhanden? 
      <select name="pflegegrad">
        <option>Ja</option><option>Nein, aber Antrag läuft</option><option>Nein</option><option>Weiß nicht</option>
      </select>
    </label>
    <label>Zeitpunkt
      <select name="zeitpunkt">
        <option>So schnell wie möglich</option><option>In 1–3 Monaten</option><option>Nur erst informieren</option>
      </select>
    </label>
    <label>Kürze deine Situation (optional) <textarea name="nachricht" rows="3" placeholder="z. B. Gerade Treppe, 13 Stufen, für meine Mutter (79)"></textarea></label>
    <label class="consent"><input type="checkbox" required> Ich stimme zu, dass meine Anfrage an passende Fachbetriebe weitergegeben wird. <a href="/datenschutz.html">Datenschutz</a></label>
    <button type="submit">Angebote anfordern — kostenlos</button>
    <p class="tiny">Ohne Pflegegrad? Kein Problem — die Betriebe beraten auch zur Pflegegrad-Beantragung.</p>
  </form>
</section>`;

const CSS = `
:root{--bg:#fbf9f6;--card:#ffffff;--txt:#26303b;--mut:#5b6b7a;--acc:#0e7a5f;--acc2:#c2571b;--line:#e4ddd2}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--txt);font:18px/1.7 Georgia,'Times New Roman',serif}
a{color:var(--acc)}a:hover{text-decoration:underline}
header{background:var(--card);border-bottom:2px solid var(--line);padding:14px 20px;display:flex;gap:18px;align-items:baseline;flex-wrap:wrap}
.brand{font-size:21px;font-weight:700;color:var(--acc);text-decoration:none}
nav{margin-left:auto;display:flex;gap:16px;flex-wrap:wrap}nav a{color:var(--mut);text-decoration:none;font-size:16px}
main{max-width:760px;margin:0 auto;padding:26px 20px 70px}
h1{font-size:33px;line-height:1.25;margin:14px 0 10px}h2{font-size:24px;margin:34px 0 8px}
p{margin:10px 0}.lead{font-size:20px;color:var(--mut)}
.notice{background:#fdf3e7;border:1px solid #eccfa8;border-radius:10px;padding:12px 16px;margin:16px 0}
.okbox{background:#eef7f2;border:1px solid #bfe0d2;border-radius:10px;padding:12px 16px;margin:16px 0}
.leadbox{background:var(--card);border:2px solid var(--acc);border-radius:14px;padding:22px;margin:34px 0}
.leadbox h2{margin-top:0}
.leadform label{display:block;margin:12px 0;font-weight:700}
.leadform input,.leadform select,.leadform textarea{width:100%;padding:10px;font:inherit;margin-top:4px;border:1px solid var(--line);border-radius:8px;background:#fff}
.leadform .consent{font-weight:400;font-size:15px}
.leadform button{background:var(--acc);color:#fff;border:0;border-radius:10px;padding:14px 22px;font-size:19px;width:100%;margin-top:10px;cursor:pointer}
.tiny{font-size:14px;color:var(--mut)}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:14px;margin:18px 0}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px}
.card h3{margin:0 0 6px;font-size:19px}.card h3 a{color:var(--txt)}
.card p{color:var(--mut);font-size:15.5px;margin:4px 0 0}
footer{border-top:2px solid var(--line);background:var(--card);padding:20px;margin-top:40px}
footer .wrap{max-width:760px;margin:0 auto;color:var(--mut);font-size:15px}
.pill{display:inline-block;background:#eef7f2;color:var(--acc);border-radius:999px;padding:2px 12px;font-size:15px;margin:0 6px 8px 0}
table{width:100%;border-collapse:collapse;margin:14px 0;background:var(--card)}td,th{border:1px solid var(--line);padding:9px 12px;text-align:left}th{background:#f2ede4}
`;

function layout(title, desc, body, path) {
  return `<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>${esc(title)}</title><meta name="description" content="${esc(desc)}">
<link rel="canonical" href="${esc(url(path))}">
<meta property="og:title" content="${esc(title)}"><meta property="og:description" content="${esc(desc)}">
<style>${CSS}</style>
</head>
<body>
<header>
  <a class="brand" href="/">ZuhauseBleiben Kompass</a>
  <nav>
    <a href="/treppenlift-kosten.html">Kosten</a>
    <a href="/treppenlift-zuschuss.html">Zuschüsse</a>
    <a href="/bad-umbau-barrierefrei.html">Bad-Umbau</a>
    <a href="/regional.html">Region</a>
    <a href="/#angebote">Angebote</a>
  </nav>
</header>
<main>${body}</main>
<footer><div class="wrap">
  <p><strong>ZuhauseBleiben Kompass</strong> — unabhängiger Ratgeber. Stand: ${STAND}. Alle Angaben ohne Gewähr; maßgeblich sind die Auskünfte der Kostenträger und KfW.</p>
  <p><a href="/impressum.html">Impressum</a> · <a href="/datenschutz.html">Datenschutz</a> · <a href="/rss.xml">RSS</a></p>
</div></footer>
</body></html>`;
}

const pages = [];

/* Index */
pages.push({ path: "index.html", title: `${B.name} — ${B.claim}`, desc: B.description, body: `
<h1>Treppenlift &amp; barrierefreier Umbau — ohne Verwirrung.</h1>
<p class="lead">${esc(B.description)}</p>
<div class="okbox"><strong>🟢 Pflegekasse zahlt aktuell zuverlässig: bis 4.180 € Zuschuss</strong> für Treppenlift &amp; Bad-Umbau (§ 40 SGB XI, ab Pflegegrad 1). <a href="/treppenlift-zuschuss.html">So bekommst du ihn →</a></div>
<div class="notice"><strong>🔴 KfW 455-B „Altersgerecht Umbauen“: seit 31.07.2026 geschlossen</strong> — Bundesmittel erschöpft. Viele Portale bewerben ihn noch. Wir prüfen wöchentlich, ob er wieder öffnet.</div>
<h2>Die wichtigsten Fragen</h2>
<div class="cards">
${C.pages.filter(p=>p.type==="article").map(p=>`<div class="card"><h3><a href="/${p.slug}.html">${esc(p.h1.split(":")[0])}</a></h3><p>${esc(p.description.slice(0,110))}…</p></div>`).join("\n")}
<div class="card"><h3><a href="/regional.html">Regionale Betriebe</a></h3><p>Fachbetriebe &amp; Landesförderung — nach Bundesland.</p></div>
</div>
${FORM}
`});

/* Artikel */
for (const p of C.pages.filter(p=>p.type==="article")) {
  const body = `<h1>${esc(p.h1)}</h1><p class="lead">Stand: ${STAND} · von uns wöchentlich geprüft</p>` +
    p.sections.map(s=>`<h2>${esc(s.h2)}</h2>` + s.p.map(t=>`<p>${t}</p>`).join("")).join("\n") + FORM;
  pages.push({ path: `${p.slug}.html`, title: p.title, desc: p.description, body });
}

/* Regional */
const reg = C.pages.find(p=>p.type==="regional");
pages.push({ path: "regional.html", title: reg.title, desc: reg.description, body: `
<h1>${esc(reg.h1)}</h1>
<p class="lead">Wähle dein Bundesland — wir zeigen Förderprogramme und vermitteln Fachbetriebe aus deiner Region.</p>
<div class="cards">
${reg.regions.map(r=>`<div class="card"><h3><a href="/region/${r.slug}.html">${esc(r.name)}</a></h3><p>Treppenlift &amp; Bad-Umbau in ${esc(r.name)}: Betriebe, Landesförderung, Pflegekassen-Zuschuss.</p></div>`).join("\n")}
</div>${FORM}`});

for (const r of reg.regions) {
  pages.push({ path: `region/${r.slug}.html`, title: `Treppenlift ${r.name}: Kosten, Förderung, Fachbetriebe (${B.stand})`,
    desc: `Treppenlift & barrierefreier Bad-Umbau in ${r.name}: Pflegekasse zahlt bis 4.180 €, Landesprogramme, kostenlose Angebote von regionalen Fachbetrieben.`,
    body: `
<h1>Treppenlift &amp; Barrierefrei-Umbau in ${esc(r.name)}</h1>
<p class="lead">Der Pflegekassen-Zuschuss (bis 4.180 €, ab Pflegegrad 1) gilt bundesweit — auch in ${esc(r.name)}. Zusätzlich gibt es in vielen Bundesländern eigene Programme; die aktuellen Konditionen für ${esc(r.name)} liefert die Angebotsanfrage gleich mit.</p>
<div class="okbox"><strong>Kostenlose Angebote aus ${esc(r.name)}:</strong> Fachbetriebe mit Barrierefrei-Erfahrung, max. 3 Angebote, unverbindlich.</div>
${FORM}`});
}

/* Impressum & Datenschutz als Platzhalter (Muss vom Nutzer finalisiert werden) */
pages.push({ path: "impressum.html", title: "Impressum", desc: "Impressum", body: `
<h1>Impressum</h1>
<div class="notice"><strong>Platzhalter — vor Live-Schaltung durch echte Betreiberdaten ersetzen (Rechtspflicht!).</strong></div>
<p>Angaben gemäß § 5 TMG / § 18 MStV:<br>[Name / Firma]<br>[Adresse]<br>[E-Mail]</p>`});
pages.push({ path: "datenschutz.html", title: "Datenschutzerklärung", desc: "Datenschutzerklärung", body: `
<h1>Datenschutzerklärung</h1>
<div class="notice"><strong>Platzhalter — vor Live-Schaltung finalisieren.</strong> Kernpunkte der Endversion: Verantwortlicher, Zweck der Lead-Weitergabe an Fachbetriebe, Rechtsgrundlage Einwilligung (Art. 6 Abs. 1 lit. a DSGVO), Widerrufsrecht, Empfänger, Speicherdauer, Kontaktformular-Dienstleister (Formspree/Alternative) mit AVV.</div>
<p>Es gelten diestandardmäßigen Pflichtangaben nach DSGVO. Diese Seite verwendet kein Tracking, keine Cookies, keine externen Analyse-Skripte.</p>`});

/* RSS (Status-Updates Förderung) */
pages.push({ path: "rss.xml", raw: `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
<title>ZuhauseBleiben Kompass — Förder-Status</title>
<link>${url("/")}</link>
<description>Aktuelle Zuschüsse für Treppenlift &amp; Barrierefrei-Umbau: Pflegekasse, KfW-Status, Länder.</description>
<language>de</language>
<pubDate>${new Date().toUTCString()}</pubDate>
<item><title>Pflegekasse: 4.180 € Wohnraumanpassung weiter zuverlässig verfügbar</title><link>${url("/treppenlift-zuschuss.html")}</link><guid>${url("/treppenlift-zuschuss.html")}#p1</guid><pubDate>${new Date().toUTCString()}</pubDate><description>Bis 4.180 € Zuschuss ab Pflegegrad 1 (§ 40 Abs. 4 SGB XI). Antrag vor Kauf stellen.</description></item>
<item><title>KfW 455-B bleibt geschlossen — Bundesmittel erschöpft</title><link>${url("/treppenlift-zuschuss.html")}</link><guid>${url("/treppenlift-zuschuss.html")}#k1</guid><pubDate>${new Date().toUTCString()}</pubDate><description>Seit 31.07.2026 keine neuen Anträge möglich. Laufende Zusagen bleiben gültig.</description></item>
</channel></rss>`});

/* Sitemap */
const slugs = ["/", ...C.pages.filter(p=>p.type==="article").map(p=>`/${p.slug}.html`), "/regional.html", ...reg.regions.map(r=>`/region/${r.slug}.html`), "/impressum.html", "/datenschutz.html"];
pages.push({ path: "sitemap.xml", raw: `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${slugs.map(s=>`  <url><loc>${url(s)}</loc></url>`).join("\n")}
</urlset>`});

/* robots */
pages.push({ path: "robots.txt", raw: `User-agent: *\nAllow: /\nSitemap: ${url("/sitemap.xml")}\n` });

/* write */
mkdirSync(OUT, { recursive: true });
writeFileSync(join(OUT, ".nojekyll"), "", "utf8");
for (const pg of pages) {
  const fp = join(OUT, pg.path);
  mkdirSync(dirname(fp), { recursive: true });
  writeFileSync(fp, pg.raw ?? layout(pg.title, pg.desc, pg.body, "/" + pg.path.replace("index.html","")), "utf8");
}
console.log(`OK: ${pages.length} Seiten gebaut (davon ${reg.regions.length} Regional-Landingpages).`);
