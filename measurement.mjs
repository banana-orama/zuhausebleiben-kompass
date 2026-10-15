// Inactive by default. Do not enable before TLS, GA4 retention and server Preview acceptance.
export const measurementConfig = Object.freeze({
  enabled:false, webContainer:'GTM-M9TZZPLQ',
  endpoint:'https://service.zuhausebleiben-kompass.de/zbk/collect',
  consentRevision:2, tlsVerified:false, serverGateVerified:false, destinationVerified:false
});
const contentIds = Object.freeze({
  'bad-umbau-barrierefrei':'c01', 'treppenlift-firmen-vergleich':'c02',
  'treppenlift-gebraucht-oder-neu':'c03', 'treppenlift-kosten':'c04',
  'treppenlift-mieten':'c05', 'treppenlift-zuschuss':'c06', 'wanne-zur-dusche':'c07'
});
const placements = new Set(['checklist_top','compare_top','print_bottom','editorial_contact']);

export function installMeasurement(config = measurementConfig) {
  if (window.zbkMeasurement || !config.enabled || !config.tlsVerified || !config.serverGateVerified || !config.destinationVerified) return;
  if (config.endpoint !== measurementConfig.endpoint || config.webContainer !== measurementConfig.webContainer) return;
  let loader, pageViewed=false, pending=[], clientId;
  const allowed = () => window.zbkConsent?.version === config.consentRevision && window.zbkConsent.analyticsAllowed && ['ad_storage','ad_user_data','ad_personalization'].every(k=>window.zbkConsent.state[k]==='denied');
  // Page-scoped random identity only. Never read or write a visitor-identifying cookie/storage.
  const randomId = () => crypto.randomUUID();
  const currentContent = () => contentIds[location.pathname.replace(/^\//,'').replace(/\.html$/,'')] || 'site';
  const flush = () => {
    if (!allowed()) {pending=[]; return;}
    for (const payload of pending.splice(0)) {
      if (!allowed()) break;
      fetch(config.endpoint,{method:'POST',body:JSON.stringify(payload),headers:{'Content-Type':'text/plain'},credentials:'omit',referrerPolicy:'no-referrer',keepalive:true}).catch(()=>{});
    }
  };
  window.zbkMeasurement=Object.freeze({flush});
  const enqueue = (eventName, ctaId='') => {
    if (!allowed()) return;
    clientId ||= randomId();
    const payload={event_name:eventName,event_id:randomId(),client_id:clientId,content_id:currentContent(),cta_id:ctaId,analytics_allowed:true,consent_version:config.consentRevision,consent:{...window.zbkConsent.state}};
    if (pending.length>=20) return;
    pending.push(payload);
    window.dataLayer.push({event:'zbk_measurement',analytics_allowed:true,consent_version:config.consentRevision,consent:{...window.zbkConsent.state},measurement:{event_name:eventName,content_id:payload.content_id,cta_id:ctaId}});
  };
  const sync = () => {
    if (!allowed()) {pending=[];clientId=undefined;return;}
    if (!loader) {
      loader=document.createElement('script');loader.async=true;loader.referrerPolicy='no-referrer';
      loader.src='https://www.googletagmanager.com/gtm.js?id='+config.webContainer;
      window.dataLayer.push({'gtm.start':Date.now(),event:'gtm.js'});
      document.head.append(loader);
    }
    if (!pageViewed) {pageViewed=true;enqueue('page_view');}
  };
  window.addEventListener('zbk:consent',sync);
  document.addEventListener('click',e=>{
    const element=e.target.closest?.('[data-cta-id]');
    if (!element || !placements.has(element.dataset.ctaId) || !contentIds[element.dataset.contentId] || contentIds[element.dataset.contentId]!==currentContent()) return;
    // Editorial mailto is an interaction, never a lead or successful contact.
    enqueue('cta_click',element.dataset.ctaId);
  });
  sync();
}
