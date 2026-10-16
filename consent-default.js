// Local, synchronous bootstrap: must precede any future GTM loader.
window.dataLayer = window.dataLayer || [];
window.gtag = function () { window.dataLayer.push(arguments); };
window.gtag('consent', 'default', {
  analytics_storage: 'denied', ad_storage: 'denied',
  ad_user_data: 'denied', ad_personalization: 'denied'
});
(() => {
  let state = Object.freeze({analytics_storage: 'denied', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied'});
  // Getter returns a frozen snapshot; consumers cannot accidentally grant consent.
  // version 2: consent_version MUST match the shipped CMP revision (consent.mjs revision: 2)
  // and the server-side gate (client 5 / trigger 12 require consent_version === 2).
  window.zbkConsent = Object.freeze({
    version: 2,
    get state() { return state; },
    get analyticsAllowed() { return state.analytics_storage === 'granted'; },
    update(analytics) {
      state = Object.freeze({analytics_storage: analytics === true ? 'granted' : 'denied', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied'});
      window.gtag('consent', 'update', {...state});
      // GTM custom event MUST follow Consent Mode update; no network delivery here.
      window.dataLayer.push({event: 'zbk_consent_update', consent_version: 2, consent: {...state}});
      window.dispatchEvent(new CustomEvent('zbk:consent', {detail: {...state}}));
    }
  });
})();