#!/usr/bin/env python3
"""One-off scoped draft provisioning. Never publish; never read global workspace context."""
import json,subprocess,pathlib
CLI='/Users/mac/.local/bin/gtm'
OUT=pathlib.Path(__file__).parent
WEB='accounts/572865630/containers/267198165/workspaces/2'
SERVER='accounts/572865630/containers/267197767/workspaces/2'
def call(tool,args,mutate=False):
    assert args.get('workspacePath') in (WEB,SERVER)
    if mutate: args['confirm']=True
    command=[CLI,'--json','tool','call',tool,'--args-json',json.dumps(args)]
    if mutate: command+=['--confirm']
    r=subprocess.run(command,text=True,capture_output=True,timeout=180)
    result=json.loads(r.stdout)
    log=OUT/'draft-provisioning.jsonl'
    with log.open('a') as f:f.write(json.dumps({'tool':tool,'scope':args['workspacePath'],'result':result})+'\n')
    if not result['ok']:raise RuntimeError(result.get('error'))
    return result['data']
def variable(scope,name,key,typ):
    existing=call('gtm_list_variables',{'workspacePath':scope})
    entries=existing if isinstance(existing,list) else existing.get('variables',[])
    if any(x['name']==name for x in entries):return
    params=[{'key':'name' if typ=='v' else 'keyPath','type':'template','value':key}]
    if typ=='v':params.append({'key':'dataLayerVersion','type':'integer','value':'2'})
    result=call('gtm_create_variable',{'workspacePath':scope,'name':name,'type':typ,'parameter':params},True)
    print(result['path'])
for key in ['analytics_allowed','consent_version','consent.analytics_storage','consent.ad_storage','consent.ad_user_data','consent.ad_personalization']:
    variable(WEB,'ZBK DLV - '+key,key,'v')
    variable(SERVER,'ZBK ED - '+key,key,'ed')
def condition(left,right,typ='equals'):
    return {'type':typ,'parameter':[{'key':'arg0','type':'template','value':left},{'key':'arg1','type':'template','value':right}]}
for scope,prefix in [(WEB,'ZBK DLV - '),(SERVER,'ZBK ED - ')]:
    filters=[condition('{{'+prefix+'analytics_allowed}}','true'),condition('{{'+prefix+'consent_version}}','2')]
    for key,value in [('analytics_storage','granted'),('ad_storage','denied'),('ad_user_data','denied'),('ad_personalization','denied')]:
        filters.append(condition('{{'+prefix+'consent.'+key+'}}',value))
    name='ZBK — sanitized analytics-only events'
    existing=call('gtm_list_triggers',{'workspacePath':scope})
    entries=existing if isinstance(existing,list) else existing.get('triggers',[])
    trigger=next((x for x in entries if x['name']==name),None)
    if not trigger:
        trigger=call('gtm_create_trigger',{'workspacePath':scope,'name':name,'type':'customEvent','customEventFilter':[condition('{{_event}}','zbk_measurement' if scope==WEB else '^(page_view|cta_click)$','equals' if scope==WEB else 'matchRegex')],'filter':filters},True)
    print(trigger['path'])
    if scope==WEB:
        existing=call('gtm_list_tags',{'workspacePath':scope})
        entries=existing if isinstance(existing,list) else existing.get('tags',[])
        if not any(x['name']=='ZBK — dispatch permitted queue to Stape' for x in entries):
            tag=call('gtm_create_tag',{'workspacePath':scope,'name':'ZBK — dispatch permitted queue to Stape','type':'html','firingTriggerId':[trigger['triggerId']],'parameter':[{'key':'html','type':'template','value':'<script>if(window.zbkConsent && window.zbkConsent.analyticsAllowed && window.zbkMeasurement){window.zbkMeasurement.flush();}</script>'},{'key':'supportDocumentWrite','type':'boolean','value':'false'}]},True)
            print(tag['path'])
print('Draft setup only. No version creation, publish or GA4 forwarding.')
