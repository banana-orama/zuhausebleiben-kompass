// Pivoted 2026-10-16 to consent-gated client-side GA4 (operator decision): Stape Free quota
// exhausted (18,432/10,000), container disablement imminent, no paid upgrade approved.
// After analytics consent, ONE Web-GTM loader (GTM-M9TZZPLQ) is injected; the container's
// consent-gated GA4 tags (G-5738T8FHWW, auto page_view OFF) receive only minimal events
// (page_view once per page, cta_click with content_id/cta_id). No server endpoint, no Stape,
// no first-party proxy: the browser talks directly to googletagmanager.com/Google.
export const measurementConfig = Object.freeze({
  enabled:true, webContainer:'GTM-M9TZZPLQ', measurementId:'G-5738T8FHWW',
  consentRevision:2, mode:'client'
});
const contentIds = Object.freeze({
  'bad-umbau-barrierefrei':'c01', 'treppenlift-firmen-vergleich':'c02',
  'treppenlift-gebraucht-oder-neu':'c03', 'treppenlift-kosten':'c04',
  'treppenlift-mieten':'c05', 'treppenlift-zuschuss':'c06', 'wanne-zur-dusche':'c07'
});
const placements = new Set(['checklist_top','compare_top','print_bottom','editorial_contact']);

export function installMeasurement(config = measurementConfig) {
  if (window.zbkMeasurement || !config.enabled || config.mode !== 'client') return;
  if (config.webContainer !== measurementConfig.webContainer || config.measurementId !== measurementConfig.measurementId) return;
  if (config.consentRevision !== measurementConfig.consentRevision) return;
  let loader=false, pageViewed=false;
  const allowed = () => window.zbkConsent?.version === config.consentRevision && window.zbkConsent.analyticsAllowed && ['ad_storage','ad_user_data','ad_personalization'].every(k=>window.zbkConsent.state[k]==='denied');
  const currentContent = () => contentIds[location.pathname.replace(/^\//,'').replace(/\.html$/,'')] || 'site';
  window.zbkMeasurement=Object.freeze({});
  const enqueue = (eventName, ctaId='') => {
    if (!allowed()) return;
    if (eventName==='page_view') {if (pageViewed) return; pageViewed=true;}
    // Strict minimal payload; GTM trigger 9 re-checks the same consent allowlist.
    window.dataLayer.push({event:'zbk_measurement',analytics_allowed:true,consent_version:config.consentRevision,
      consent:{...window.zbkConsent.state},measurement:{event_name:eventName,content_id:currentContent(),cta_id:ctaId}});
  };
  const sync = () => {
    if (!allowed()) return;
    if (!loader) {
      loader=true;
      // Single consent-gated loader with no referrer; never sent without consent.
      const script=document.createElement('script');script.async=true;script.referrerPolicy='no-referrer';
      script.src='https://www.googletagmanager.com/gtm.js?id='+config.webContainer;
      window.dataLayer.push({'gtm.start':Date.now(),event:'gtm.js'});
      document.head.append(script);
    }
    enqueue('page_view');
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
