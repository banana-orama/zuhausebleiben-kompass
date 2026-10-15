import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
const out=new URL('./operations/measurement/',import.meta.url);mkdirSync(out,{recursive:true});
const policy=readFileSync(new URL('./measurement-policy.mjs',import.meta.url),'utf8').replace('export function','function');
const permission=(id,params=[])=>({instance:{key:{publicId:id,versionId:'1'},param:params},isRequired:true});
const val=(key,string)=>({key,value:{type:1,string}});
const source=`const getRequestPath=require('getRequestPath');
const getRequestMethod=require('getRequestMethod');
const getRequestHeader=require('getRequestHeader');
const getRequestBody=require('getRequestBody');
const claimRequest=require('claimRequest');
const setResponseStatus=require('setResponseStatus');
const setResponseHeader=require('setResponseHeader');
const returnResponse=require('returnResponse');
const runContainer=require('runContainer');
const JSON=require('JSON');
${policy}
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
`;
const info={type:'CLIENT',id:'cvt_temp_public_id',version:1,securityGroups:[],displayName:'ZBK — strict consent and event allowlist',description:'Project-only analytics consent gate. No forwarding, logging or cookies.',containerContexts:['SERVER']};
const permissions=[permission('read_request',[val('requestAccess','any'),val('headerAccess','specific'),{key:'allowedHeaders',value:{type:2,listItem:[{type:1,string:'origin'}]}},val('queryParameterAccess','none')]),permission('return_response'),permission('access_response',[val('writeResponseAccess','any'),val('writeHeaderAccess','any')]),permission('run_container')];
const tpl='___INFO___\n'+JSON.stringify(info,null,2)+'\n\n___TEMPLATE_PARAMETERS___\n[]\n\n___SANDBOXED_JS_FOR_SERVER___\n'+source+'\n___SERVER_PERMISSIONS___\n'+JSON.stringify(permissions,null,2)+'\n\n___TESTS___\nscenarios: []\n';
writeFileSync(new URL('consent-client.tpl',out),tpl);
writeFileSync(new URL('consent-client.js',out),source);
writeFileSync(new URL('client-template-create.json',out),JSON.stringify({workspacePath:'accounts/572865630/containers/267197767/workspaces/2',name:info.displayName,templateData:tpl,confirm:true},null,2));
console.log('Generated strict gate template; no GA4 destination or forwarding.');
