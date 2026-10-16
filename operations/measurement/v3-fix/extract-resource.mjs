// Extract the "resource" object from gtm.js and dump predicates/macros/rules/tags wiring.
import { readFileSync, writeFileSync } from 'node:fs';

const src = readFileSync('operations/measurement/v3-fix/gtm-v4.js', 'utf8');
const start = src.indexOf('var data = {');
if (start < 0) { console.error('no data object'); process.exit(1); }
const objStart = start + 'var data = '.length;

// bracket-balance scan (strings aware) to find the end of the object literal
let depth = 0, inStr = null, esc = false, end = -1;
for (let i = objStart; i < src.length; i++) {
  const c = src[i];
  if (inStr) {
    if (esc) esc = false;
    else if (c === '\\') esc = true;
    else if (c === inStr) inStr = null;
    continue;
  }
  if (c === '"' || c === "'") { inStr = c; continue; }
  if (c === '{' || c === '[') depth++;
  else if (c === '}' || c === ']') {
    depth--;
    if (depth === 0) { end = i + 1; break; }
  }
}
if (end < 0) { console.error('unbalanced'); process.exit(1); }
const literal = src.slice(objStart, end);
const data = eval(`(${literal})`);
const res = data.resource;

writeFileSync('operations/measurement/v3-fix/v4-resource.json', JSON.stringify(res, null, 1));
console.log('resource keys:', Object.keys(res).join(','));
console.log('version:', res.version);
console.log('macros:');
res.macros.forEach((m, i) => console.log(' ', i, m.function, JSON.stringify(m).slice(0, 140)));
console.log('predicates:');
res.predicates.forEach((p, i) => console.log(' ', i, JSON.stringify(p)));
console.log('rules:', JSON.stringify(res.rules));
console.log('tags:');
res.tags.forEach((t, i) => console.log(' ', i, JSON.stringify(t).slice(0, 400)));
