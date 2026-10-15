import {test} from 'node:test';
import assert from 'node:assert/strict';
const load=()=>import('../measurement-policy.mjs');
test('server policy rejects unknown, PII-bearing, unbounded and lead events',async()=>{
 const {sanitizeMeasurement}=await load();
 for(const patch of [{email:'someone@example.org'},{page_location:'https://site/?email=someone@example.org'},{event_name:'generate_lead'},{content_id:'someone@example.org'},{cta_id:'mailto:someone@example.org'},{event_id:'bad'},{client_id:'private'},{event_name:'cta_click',cta_id:''},{event_name:'page_view',cta_id:'editorial_contact'}]) assert.equal(sanitizeMeasurement({...good(),...patch},2),null);
 const valid={...good(),event_name:'cta_click',cta_id:'editorial_contact'};assert.deepEqual(sanitizeMeasurement(valid,2),valid);
 assert.equal(sanitizeMeasurement({...good(),consent:{...good().consent,email:'private'}},2),null);
});
const good=()=>({event_name:'page_view',event_id:'b034d110-5136-4faf-91dd-dd23bfc533ac',client_id:'18141431-d9f9-488a-93ea-411272ade84c',content_id:'c04',cta_id:'',analytics_allowed:true,consent_version:2,consent:{analytics_storage:'granted',ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied'}});
test('server policy accepts only an explicit complete current analytics-only consent',async()=>{
  const {sanitizeMeasurement}=await load();
  assert.deepEqual(sanitizeMeasurement(good(),2),good());
  for(const key of Object.keys(good().consent)){
    for(const state of ['unknown',undefined,key==='analytics_storage'?'denied':'granted']){
      const p=good();p.consent[key]=state;assert.equal(sanitizeMeasurement(p,2),null);
    }
  }
  for(const value of [false,'true',1,undefined]){const p=good();p.analytics_allowed=value;assert.equal(sanitizeMeasurement(p,2),null);}
  for(const rev of [0,1,'2',undefined]){const p=good();p.consent_version=rev;assert.equal(sanitizeMeasurement(p,2),null);}
});
