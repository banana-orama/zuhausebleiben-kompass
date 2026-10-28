#!/usr/bin/env node
// Ist-Analyse: aktuelle Related-Links je Artikel (Renderer-Logik repliziert) + betroffene Gates.
import { readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const root = process.cwd();
const articles = readdirSync(join(root, 'content-ready')).filter(f => f.endsWith('.json'))
  .map(f => JSON.parse(readFileSync(join(root, 'content-ready', f), 'utf8')))
  .filter(a => a.status === 'editorial-reviewed-preview');

const isBad = s => s.includes('bad') || s.includes('wanne') || s.includes('dusche');
const isCare = s => /^(hausnotruf|pflegegrad|hilfsmittel|rollator|verhinderungspflege|tuerbreiten|beleuchtung)/.test(s);
const isLift = s => s.startsWith('treppenlift');

for (const a of articles) {
  const cluster = isBad(a.slug) ? 'bad' : isCare(a.slug) ? 'care' : 'lift';
  const inCluster = x => cluster === 'bad' ? (isBad(x.slug) || x.slug.includes('zuschuss')) : cluster === 'care' ? isCare(x.slug) : isLift(x.slug);
  const pool = articles.filter(x => x.slug !== a.slug).filter(inCluster);
  if (cluster === 'care' && pool.length < 3) for (const s of ['treppenlift-zuschuss', 'treppenlift-kosten']) {
    const y = articles.find(x => x.slug === s); if (y && !pool.includes(y)) pool.push(y);
  }
  const related = pool.slice(0, 3).map(x => x.slug);
  console.log(`${a.slug} [${cluster}] -> ${related.join(', ')}`);
}
console.log(`\nArtikel gesamt: ${articles.length}`);
