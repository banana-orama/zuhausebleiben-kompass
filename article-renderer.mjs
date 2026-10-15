import {readFileSync,readdirSync} from 'node:fs';
import {join} from 'node:path';
const esc=s=>String(s??'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const safeJson=d=>JSON.stringify(d).replace(/</g,'\\u003c');
export function renderArticles(root,base,closing){
 const url=p=>base.replace(/\/$/,'')+p;
 const articles=readdirSync(join(root,'content-ready')).filter(f=>f.endsWith('.json')).map(f=>JSON.parse(readFileSync(join(root,'content-ready',f),'utf8'))).filter(a=>a.status==='editorial-reviewed-preview');
 const slugs=new Set();
 for(const a of articles){
  if(slugs.has(a.slug)||!/^[a-z0-9-]+$/.test(a.slug))throw Error('Invalid/duplicate slug '+a.slug);slugs.add(a.slug);
  if(!a.sections?.length||a.sources?.length<2)throw Error('Missing content/source gate '+a.slug);
  if(!a.image?.src.startsWith('assets/images/'))throw Error('Invalid image '+a.slug);
  readFileSync(join(root,a.image.src));
 }
 return articles.map(a=>{
  const txt=s=>esc(s).replace(/\[(\d+)\]/g,(m,n)=>{
   if(!a.sources[Number(n)-1])throw Error('Missing citation '+a.slug+':'+n);
   return `<sup class="cite"><a href="#source-${n}" aria-label="Quelle ${n}">[${n}]</a></sup>`;
  });
  const svg=readFileSync(join(root,a.image.src),'utf8');
  const dims=svg.match(/viewBox="0 0 (\d+) (\d+)"/);
  if(!dims)throw Error('Missing image dimensions '+a.slug);
  const figure=`<figure class="editorial-figure"><a href="${url('/'+a.image.src)}" aria-label="Illustration vergrößern"><img src="${url('/'+a.image.src)}" alt="${esc(a.image.alt)}" width="${dims[1]}" height="${dims[2]}" loading="lazy" decoding="async"></a><figcaption>${esc(a.image.caption)} <a href="${url('/'+a.image.src)}">Großansicht öffnen</a></figcaption></figure>`;
  const toc=`<nav class="article-toc" aria-label="Inhaltsverzeichnis"><strong>In diesem Ratgeber</strong><ol>${a.sections.map((s,i)=>`<li><a href="#abschnitt-${i+1}">${esc(s.heading)}</a></li>`).join('')}</ol></nav>`;
  const content=a.sections.map((s,i)=>`<section id="abschnitt-${i+1}"><h2>${esc(s.heading)}</h2>${(s.paragraphs||[]).map(p=>`<p>${txt(p)}</p>`).join('')}${s.bullets?`<ul class="checklist">${s.bullets.map(p=>`<li>${txt(p)}</li>`).join('')}</ul>`:''}${s.table?`<div class="table-scroll" role="region" aria-label="${esc(s.heading)} – Tabelle" tabindex="0"><table><thead><tr>${s.table.headers.map(h=>`<th scope="col">${esc(h)}</th>`).join('')}</tr></thead><tbody>${s.table.rows.map(row=>`<tr>${row.map(c=>`<td>${txt(c)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`:''}</section>`).join('');
  const related=articles.filter(x=>x.slug!==a.slug).filter(x=>a.slug.includes('bad')||a.slug.includes('wanne') ? x.slug.includes('bad')||x.slug.includes('wanne')||x.slug.includes('zuschuss') : x.slug.startsWith('treppenlift')).slice(0,3);
  const checklistIndex=a.sections.findIndex(s=>/checkliste|fragenliste|angebotscheck|unterlagencheck|angebote vergleich|kostenaufstellung/i.test(s.heading));
  const checklistTarget='#abschnitt-'+(checklistIndex>=0?checklistIndex+1:1);
  const earlyCTA=`<div class="reader-actions" aria-label="Nächste Schritte"><a class="button" href="${checklistTarget}" data-cta-id="checklist_top" data-content-id="${esc(a.slug)}">${checklistIndex>=0?'Zur Checkliste':'Entscheidungshilfe lesen'}</a><a class="text-link" href="${url(a.slug==='bad-umbau-barrierefrei'?'/wanne-zur-dusche.html':a.slug.includes('wanne')?'/bad-umbau-barrierefrei.html':a.slug==='treppenlift-firmen-vergleich'?'/treppenlift-kosten.html':'/treppenlift-firmen-vergleich.html')}" data-cta-id="compare_top" data-content-id="${esc(a.slug)}">${a.slug==='bad-umbau-barrierefrei'?'Wannentausch planen':a.slug.includes('wanne')?'Badumbau planen':a.slug==='treppenlift-firmen-vergleich'?'Kosten vergleichen':'Anbieter prüfen'} →</a></div>`;
  const endCTA=`<aside class="next-step" aria-label="Ihr nächster Schritt"><span class="eyebrow">Gut vorbereitet weitergehen</span><h2>Nutzen Sie die Checkliste für Ihr Gespräch.</h2><p>Halten Sie offene Fragen fest und vergleichen Sie den schriftlichen Leistungsumfang. Unser Portal vermittelt derzeit noch keine Angebote.</p><div class="reader-actions"><button class="button" type="button" onclick="window.print()" data-cta-id="print_bottom" data-content-id="${esc(a.slug)}">Checkliste mit Ratgeber drucken</button><a class="text-link" href="mailto:anfragen@zuhausebleiben-kompass.de?subject=${encodeURIComponent('Frage zum Ratgeber: '+a.h1)}" data-cta-id="editorial_contact" data-content-id="${esc(a.slug)}">Frage zum Ratgeber senden →</a></div><p class="fine">Redaktioneller Kontakt, keine Notfallhilfe oder persönliche Fachberatung. Bitte keine Gesundheitsdaten oder vertraulichen Unterlagen per E-Mail senden.</p></aside>`;
  const schema={'@context':'https://schema.org','@graph':[{'@type':'Article','headline':a.h1,'description':a.description,'url':url('/'+a.slug+'.html'),'image':url('/'+a.image.src),'inLanguage':'de','publisher':{'@type':'Organization','name':'ZuhauseBleiben Kompass','url':url('/')}},{'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Startseite','item':url('/')},{'@type':'ListItem','position':2,'name':a.h1,'item':url('/'+a.slug+'.html')}]}]};
  return {path:a.slug+'.html',title:a.title+' — ZuhauseBleiben Kompass',desc:a.description,body:`<article><a class="fine" href="${url('/')}">Startseite / Ratgeber</a><h1>${esc(a.h1)}</h1><p class="article-meta">Herausgeber: <a href="${url('/impressum.html')}">Tobias Batke</a> · Mit KI-Unterstützung erstellt · Quellenstand: ${esc(a.sources[0].checked_at)}</p><p class="lead">${txt(a.intro)}</p><p class="fine">Allgemeine Orientierung, keine persönliche technische, medizinische oder rechtliche Beratung. Es werden derzeit keine Angebote vermittelt.</p>${earlyCTA}${toc}${figure}${content}${endCTA}<section class="faq"><h2>Häufige Fragen</h2>${a.faqs.map(f=>`<details><summary>${esc(f.question)}</summary><p>${txt(f.answer)}</p></details>`).join('')}</section><section class="sources"><h2>Quellen und Anbieterangaben</h2><p class="fine">Herstellerquellen beschreiben deren eigene Angebote; sie sind kein unabhängiger Produkttest.</p><ol>${a.sources.map((s,i)=>`<li id="source-${i+1}"><a href="${esc(s.url)}">${esc(s.title.replace(/^\[\d+\]\s*/,''))}</a><span class="fine"> — geprüft ${esc(s.checked_at)}</span></li>`).join('')}</ol></section><section class="related"><h2>Passend dazu</h2><ul>${related.map(r=>`<li><a href="${url('/'+r.slug+'.html')}">${esc(r.h1)}</a></li>`).join('')}</ul></section><button class="print-button" type="button" onclick="window.print()">Ratgeber &amp; Checklisten drucken</button></article>${closing}<script type="application/ld+json">${safeJson(schema)}</script>`};
 });
}
