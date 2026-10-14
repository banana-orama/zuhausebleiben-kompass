import {readFileSync,readdirSync} from 'node:fs';
import {join} from 'node:path';
const esc=s=>String(s??'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const safeJson=d=>JSON.stringify(d).replace(/</g,'\\u003c');
export function renderArticles(root,base,closing){
 const url=p=>base.replace(/\/$/,'')+p;
 const articles=readdirSync(join(root,'content-ready')).filter(f=>f.endsWith('.json')).map(f=>JSON.parse(readFileSync(join(root,'content-ready',f),'utf8')));
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
  const schema={'@context':'https://schema.org','@graph':[{'@type':'Article','headline':a.h1,'description':a.description,'url':url('/'+a.slug+'.html'),'image':url('/'+a.image.src),'inLanguage':'de','publisher':{'@type':'Organization','name':'ZuhauseBleiben Kompass','url':url('/')}},{'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Startseite','item':url('/')},{'@type':'ListItem','position':2,'name':a.h1,'item':url('/'+a.slug+'.html')}]}]};
  return {path:a.slug+'.html',title:a.title+' — ZuhauseBleiben Kompass',desc:a.description,body:`<article><a class="fine" href="${url('/')}">Startseite / Ratgeber</a><h1>${esc(a.h1)}</h1><p class="article-meta">Herausgeber: <a href="${url('/impressum.html')}">Tobias Batke</a> · Mit KI-Unterstützung erstellt · Quellenstand: ${esc(a.sources[0].checked_at)}</p><p class="lead">${txt(a.intro)}</p><p class="fine">Allgemeine Orientierung, keine persönliche technische, medizinische oder rechtliche Beratung. Es werden derzeit keine Angebote vermittelt.</p>${toc}${figure}${content}<section class="faq"><h2>Häufige Fragen</h2>${a.faqs.map(f=>`<details><summary>${esc(f.question)}</summary><p>${txt(f.answer)}</p></details>`).join('')}</section><section class="sources"><h2>Quellen und Anbieterangaben</h2><p class="fine">Herstellerquellen beschreiben deren eigene Angebote; sie sind kein unabhängiger Produkttest.</p><ol>${a.sources.map((s,i)=>`<li id="source-${i+1}"><a href="${esc(s.url)}">${esc(s.title.replace(/^\[\d+\]\s*/,''))}</a><span class="fine"> — geprüft ${esc(s.checked_at)}</span></li>`).join('')}</ol></section><section class="related"><h2>Passend dazu</h2><ul>${related.map(r=>`<li><a href="${url('/'+r.slug+'.html')}">${esc(r.h1)}</a></li>`).join('')}</ul></section><button class="print-button" type="button" onclick="window.print()">Ratgeber &amp; Checklisten drucken</button></article>${closing}<script type="application/ld+json">${safeJson(schema)}</script>`};
 });
}
