const getRequestPath=require('getRequestPath');
const getRequestMethod=require('getRequestMethod');
const getRequestHeader=require('getRequestHeader');
const getRequestBody=require('getRequestBody');
const claimRequest=require('claimRequest');
const setResponseStatus=require('setResponseStatus');
const setResponseHeader=require('setResponseHeader');
const returnResponse=require('returnResponse');
const runContainer=require('runContainer');
const JSON=require('JSON');
// Embedded verbatim into the server client template: fail closed on missing/contradictory consent.
function sanitizeMeasurement(p, revision) {
  if (!p || p.analytics_allowed !== true || p.consent_version !== revision || !p.consent) return null;
  const c=p.consent;
  const keys=['event_name','event_id','client_id','content_id','cta_id','analytics_allowed','consent_version','consent'];
  for (const key in p) {if (keys.indexOf(key)<0) return null;}
  for (const key in c) {if (['analytics_storage','ad_storage','ad_user_data','ad_personalization'].indexOf(key)<0) return null;}
  const uuid = value => {
    if (typeof value!=='string' || value.length!==36) return false;
    for (let i=0;i<36;i++) {if ([8,13,18,23].indexOf(i)>=0 ? value[i]!=='-' : '0123456789abcdef'.indexOf(value[i])<0) return false;}
    return true;
  };
  if (!uuid(p.event_id) || !uuid(p.client_id)) return null;
  if (['site','c01','c02','c03','c04','c05','c06','c07'].indexOf(p.content_id)<0) return null;
  if (p.event_name==='page_view') {if (p.cta_id!=='') return null;}
  else if (p.event_name==='cta_click') {if (p.content_id==='site' || ['checklist_top','compare_top','print_bottom','editorial_contact'].indexOf(p.cta_id)<0) return null;}
  else return null;
  if (c.analytics_storage!=='granted' || c.ad_storage!=='denied' || c.ad_user_data!=='denied' || c.ad_personalization!=='denied') return null;
  return {event_name:p.event_name,event_id:p.event_id,client_id:p.client_id,content_id:p.content_id,cta_id:p.cta_id,analytics_allowed:true,consent_version:revision,consent:{analytics_storage:'granted',ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied'}};
}

if(getRequestPath()!=='/zbk/collect') return;
claimRequest();
const origin=getRequestHeader('origin');
if(origin!=='https://zuhausebleiben-kompass.de') {setResponseStatus(403);returnResponse();return;}
setResponseHeader('Access-Control-Allow-Origin','https://zuhausebleiben-kompass.de');
setResponseHeader('Vary','Origin');
setResponseHeader('Cache-Control','no-store');
if(getRequestMethod()!=='POST') {setResponseStatus(405);returnResponse();return;}
const body=getRequestBody();
if(!body || body.length>2048) {setResponseStatus(400);returnResponse();return;}
const event=sanitizeMeasurement(JSON.parse(body),2);
if(!event) {setResponseStatus(204);returnResponse();return;}
runContainer(event,()=>{setResponseStatus(204);returnResponse();});
