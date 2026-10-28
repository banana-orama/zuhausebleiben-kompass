import {readFileSync,readdirSync} from 'node:fs';
import {join} from 'node:path';
const esc=s=>String(s??'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const safeJson=d=>JSON.stringify(d).replace(/</g,'\\u003c');
function loadPartnerConfig(root){
 const p=process.env.PARTNER_LINKS_CONFIG||join(root,'data/partner-links.json');
 return JSON.parse(readFileSync(p,'utf8'));
}
// Partner-Link-Map: rendert NUR Platzierungen zugelassener Partner mit echter Tracker-URL.
// active!=true, approved!=true oder fehlende URL => nichts im HTML (kein Platzhalter, kein erfundener Link).
// Widersprüche (URL ohne Zusage, Zusage ohne URL, unbekannte Slugs) brechen den Build.
function buildPartnerIndex(PC,slugs){
 const bySlug=new Map();
 if(!PC||PC.active!==true)return bySlug;
 const seen=new Set();
 for(const partner of (PC.partners||[])){
  if(partner.approved===true&&!(partner.placements||[]).length)throw Error('Approved partner '+(partner.id||'?')+' has no placements');
  for(const pl of (partner.placements||[])){
   if(!/^[a-z0-9_]+$/.test(pl.placement_id||''))throw Error('Invalid placement_id '+(pl.placement_id||'(missing)'));
   if(seen.has(pl.placement_id))throw Error('Duplicate placement_id '+pl.placement_id);
   seen.add(pl.placement_id);
   const list=pl.articles||[];
   if(!list.length)throw Error('Placement without articles '+pl.placement_id);
   for(const s of list)if(!slugs.has(s))throw Error('Placement '+pl.placement_id+' references unknown slug '+s);
   if(pl.url){
    if(partner.approved!==true)throw Error('Placement '+pl.placement_id+' has a URL but partner '+(partner.id||'?')+' is not approved');
    if(!/^https:\/\//.test(pl.url))throw Error('Placement '+pl.placement_id+' URL must be https');
    if(!pl.label||!pl.cta_text)throw Error('Placement '+pl.placement_id+' missing label/cta_text');
    for(const s of list){if(!bySlug.has(s))bySlug.set(s,[]);bySlug.get(s).push({partner,pl});}
   }else if(partner.approved===true){
    throw Error('Approved partner '+(partner.id||'?')+' placement '+pl.placement_id+' has no URL yet');
   }
  }
 }
 return bySlug;
}
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
 const PC=loadPartnerConfig(root);
 const partnerBySlug=buildPartnerIndex(PC,slugs);
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
  const content=a.sections.map((s,i)=>`<section id="abschnitt-${i+1}"><h2>${esc(s.heading)}</h2>${(s.paragraphs||[]).map(p=>`<p>${txt(p)}</p>`).join('')}${s.bullets?`<ul class="checklist">${s.bullets.map(p=>`<li>${txt(p)}</li>`).join('')}</ul>`:''}${s.table?`<div class="table-scroll" role="region" aria-label="${esc(s.heading)} – Tabelle" tabindex="0"><table><thead><tr>${s.table.headers.map(h=>`<th scope="col">${esc(h)}</th>`).join('')}</tr></thead><tbody>${s.table.rows.map(row=>`<tr>${row.map(c=>`<td>${txt(c)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`:''}${(s.paragraphs_after||[]).map(p=>`<p>${txt(p)}</p>`).join('')}</section>`).join('');
  const isBad=s=>s.includes('bad')||s.includes('wanne')||s.includes('dusche');
  const isCare=s=>/^(hausnotruf|pflegegrad|hilfsmittel|rollator|verhinderungspflege|tuerbreiten|beleuchtung)/.test(s);
  const isLift=s=>s.startsWith('treppenlift');
  const cluster=isBad(a.slug)?'bad':isCare(a.slug)?'care':'lift';
  const inCluster=x=>cluster==='bad'?(isBad(x.slug)||x.slug.includes('zuschuss')):cluster==='care'?isCare(x.slug):isLift(x.slug);
  const relatedPool=articles.filter(x=>x.slug!==a.slug).filter(inCluster);
  if(cluster==='care'&&relatedPool.length<3)for(const s of ['treppenlift-zuschuss','treppenlift-kosten']){const y=articles.find(x=>x.slug===s);if(y&&!relatedPool.includes(y))relatedPool.push(y);}
  const related=relatedPool.slice(0,3);
  const checklistIndex=a.sections.findIndex(s=>/checkliste|fragenliste|angebotscheck|unterlagencheck|angebote vergleich|kostenaufstellung/i.test(s.heading));
  const checklistTarget='#abschnitt-'+(checklistIndex>=0?checklistIndex+1:1);
  const specialMap=[['bad-umbau-barrierefrei','/wanne-zur-dusche.html','Wannentausch planen'],['wanne-zur-dusche','/bad-umbau-barrierefrei.html','Badumbau planen'],['badumbau-angebote-vergleichen','/bad-umbau-barrierefrei.html','Badumbau planen'],['bodengleiche-dusche-altbau','/treppenlift-mietwohnung.html','Mietwohnung: Zustimmungen klären'],['treppenlift-firmen-vergleich','/treppenlift-kosten.html','Kosten vergleichen'],['treppenlift-angebote-vergleichen','/treppenlift-zuschuss.html','Förderung prüfen'],['treppenlift-steuerlich-absetzen','/treppenlift-zuschuss.html','Förderung prüfen'],['treppenlift-schmale-treppe','/treppenlift-firmen-vergleich.html','Anbieter für Aufmaß vergleichen'],['treppenlift-maximalgewicht','/treppenlift-angebote-vergleichen.html','Angebote vergleichen'],['treppenlift-aussentreppen-aussenlift','/treppenlift-firmen-vergleich.html','Anbieter für Außenlift vergleichen'],['treppenlift-plattformlift-rollstuhllift','/treppenlift-firmen-vergleich.html','Anbieter für Rollstuhllifte vergleichen'],['pflegegrad-antrag-ablauf-fristen','/hilfsmittel-pflegekasse-uebernahme.html','Hilfsmittel-Kostenübernahme prüfen'],['rollator-auswahl-passform-kosten','/hilfsmittel-pflegekasse-uebernahme.html','Kostenübernahme prüfen'],['hilfsmittel-dusch-wc-uebernahme','/hilfsmittel-pflegekasse-uebernahme.html','Hilfsmittel-Grundlagen nachlesen']];
  const hit=specialMap.find(([s])=>a.slug===s);
  const cmp=hit?[hit[1],hit[2]]:cluster==='bad'?['/treppenlift-zuschuss.html','Förderung prüfen']:cluster==='care'?['/pflegegrad-antrag-ablauf-fristen.html','Pflegegrad-Antrag vorbereiten']:['/treppenlift-firmen-vergleich.html','Anbieter prüfen'];
  const earlyCTA=`<div class="reader-actions" aria-label="Nächste Schritte"><a class="button" href="${checklistTarget}" data-cta-id="checklist_top" data-content-id="${esc(a.slug)}">${checklistIndex>=0?'Zur Checkliste':'Entscheidungshilfe lesen'}</a><a class="text-link" href="${url(cmp[0])}" data-cta-id="compare_top" data-content-id="${esc(a.slug)}">${cmp[1]} →</a></div>`;
  const endCTA=`<aside class="next-step" aria-label="Ihr nächster Schritt"><span class="eyebrow">Gut vorbereitet weitergehen</span><h2>Nutzen Sie die Checkliste für Ihr Gespräch.</h2><p>Halten Sie offene Fragen fest und vergleichen Sie den schriftlichen Leistungsumfang. Unser Portal vermittelt derzeit noch keine Angebote.</p><div class="reader-actions"><button class="button" type="button" onclick="window.print()" data-cta-id="print_bottom" data-content-id="${esc(a.slug)}">Checkliste mit Ratgeber drucken</button><a class="text-link" href="mailto:anfragen@zuhausebleiben-kompass.de?subject=${encodeURIComponent('Frage zum Ratgeber: '+a.h1)}" data-cta-id="editorial_contact" data-content-id="${esc(a.slug)}">Frage zum Ratgeber senden →</a></div><p class="fine">Redaktioneller Kontakt, keine Notfallhilfe oder persönliche Fachberatung. Bitte keine Gesundheitsdaten oder vertrauliche Unterlagen per E-Mail senden.</p></aside>`;
  const partnerBlocks=(partnerBySlug.get(a.slug)||[]).map(({partner,pl})=>`<aside class="partner-cta" data-partner-placement="${esc(pl.placement_id)}"><span class="eyebrow">Anzeige · Kooperation mit ${esc(partner.name)}</span><h2>${esc(pl.label)}</h2>${pl.subline?`<p>${esc(pl.subline)}</p>`:''}<div class="reader-actions"><a class="button" href="${esc(pl.url)}" rel="sponsored noopener" target="_blank" data-cta-id="partner_${esc(partner.id)}" data-placement-id="${esc(pl.placement_id)}" data-content-id="${esc(a.slug)}">${esc(pl.cta_text)} →</a></div><p class="fine">Partnerlink (Anzeige): Beim Klick verlassen Sie unser Angebot und gelangen zum Anbieter. Wir können bei einer anschließenden Anfrage eine Vergütung erhalten. Die Entscheidung bleibt Ihre.</p></aside>`).join('');
  const schema={'@context':'https://schema.org','@graph':[{'@type':'Article','headline':a.h1,'description':a.description,'url':url('/'+a.slug+'.html'),'image':url('/'+a.image.src),'inLanguage':'de','publisher':{'@type':'Organization','name':'ZuhauseBleiben Kompass','url':url('/')}},{'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Startseite','item':url('/')},{'@type':'ListItem','position':2,'name':a.h1,'item':url('/'+a.slug+'.html')}]}]};
  return {path:a.slug+'.html',title:a.title+' — ZuhauseBleiben Kompass',desc:a.description,body:`<article><a class="fine" href="${url('/')}">Startseite / Ratgeber</a><h1>${esc(a.h1)}</h1><p class="article-meta">Herausgeber: <a href="${url('/impressum.html')}">Tobias Batke</a> · Mit KI-Unterstützung erstellt · Quellenstand: ${esc(a.sources[0].checked_at)}</p><p class="lead">${txt(a.intro)}</p><p class="fine">Allgemeine Orientierung, keine persönliche technische, medizinische oder rechtliche Beratung. Es werden derzeit keine Angebote vermittelt.</p>${earlyCTA}${toc}${figure}${content}${endCTA}${partnerBlocks}<section class="faq"><h2>Häufige Fragen</h2>${a.faqs.map(f=>`<details><summary>${esc(f.question)}</summary><p>${txt(f.answer)}</p></details>`).join('')}</section><section class="sources"><h2>Quellen und Anbieterangaben</h2><p class="fine">Herstellerquellen beschreiben deren eigene Angebote; sie sind kein unabhängiger Produkttest.</p><ol>${a.sources.map((s,i)=>`<li id="source-${i+1}"><a href="${esc(s.url)}">${esc(s.title.replace(/^\[\d+\]\s*/,''))}</a><span class="fine"> — geprüft ${esc(s.checked_at)}</span></li>`).join('')}</ol></section><section class="related"><h2>Passend dazu</h2><ul>${related.map(r=>`<li><a href="${url('/'+r.slug+'.html')}">${esc(r.h1)}</a></li>`).join('')}</ul></section><button class="print-button" type="button" onclick="window.print()">Ratgeber &amp; Checklisten drucken</button></article>${closing}<script type="application/ld+json">${safeJson(schema)}</script>`};
 });
}
