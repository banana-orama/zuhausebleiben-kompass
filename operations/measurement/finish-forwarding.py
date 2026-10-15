#!/usr/bin/env python3
"""Scoped own server draft extension; no publish and no global context."""
import json,pathlib,subprocess,time
OUT=pathlib.Path(__file__).parent
S='accounts/572865630/containers/267197767/workspaces/2'
def call(tool,args,mutation=False):
    assert any(str(v).startswith(S) for v in args.values()),args
    cmd=['/Users/mac/.local/bin/gtm','--json','tool','call',tool,'--args-json',json.dumps(args)]
    if mutation:cmd+=['--confirm']
    r=subprocess.run(cmd,capture_output=True,text=True,timeout=180)
    obj=json.loads(r.stdout)
    with (OUT/'forwarding-provisioning.jsonl').open('a') as f:f.write(json.dumps({'tool':tool,'args':args,'result':obj})+'\n')
    if not obj['ok']:raise RuntimeError(obj)
    return obj['data']
def condition(a,b):return {'type':'equals','parameter':[{'key':'arg0','type':'template','value':a},{'key':'arg1','type':'template','value':b}]}
t=call('gtm_get_trigger',{'triggerPath':S+'/triggers/12'})
if not any('Client Name' in str(x) for x in t['filter']):
    t['filter'].append(condition('{{Client Name}}','ZBK — opt-in analytics receiver'))
    call('gtm_update_trigger',{'triggerPath':t['path'],'fingerprint':t['fingerprint'],'triggerConfig':{'name':t['name'],'type':t['type'],'filter':t['filter'],'customEventFilter':t['customEventFilter']}},True)
vs=call('gtm_list_variables',{'workspacePath':S})
entries=vs if isinstance(vs,list) else vs.get('variables',[])
for key in ['event_id','content_id','cta_id']:
    if not any(v['name']=='ZBK ED - '+key for v in entries):
        call('gtm_create_variable',{'workspacePath':S,'name':'ZBK ED - '+key,'type':'ed','parameter':[{'key':'keyPath','type':'template','value':key}]},True)
tag=call('gtm_get_tag',{'tagPath':S+'/tags/14'})
params=[p for p in tag['parameter'] if p['key']!='eventParameters']
params.append({'type':'list','key':'eventParameters','list':[{'type':'map','map':[{'type':'template','key':'fieldName','value':k},{'type':'template','key':'value','value':v}]} for k,v in [('event_id','{{ZBK ED - event_id}}'),('content_id','{{ZBK ED - content_id}}'),('cta_id','{{ZBK ED - cta_id}}'),('debug_mode','{{Debug Mode}}'),('non_personalized_ads','true')]]})
call('gtm_update_tag',{'tagPath':tag['path'],'fingerprint':tag['fingerprint'],'tagConfig':{'name':tag['name'],'type':tag['type'],'firingTriggerId':['12'],'parameter':params}},True)
readback={k:call(tool,{arg:path}) for k,tool,arg,path in [('tag','gtm_get_tag','tagPath',S+'/tags/14'),('trigger','gtm_get_trigger','triggerPath',S+'/triggers/12')]}
(OUT/'forwarding-exact-readback.json').write_text(json.dumps(readback,indent=2))
print(json.dumps(readback,indent=2))
