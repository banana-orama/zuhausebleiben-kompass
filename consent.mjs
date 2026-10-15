import * as CookieConsent from './vendor/cookieconsent.esm.js';

const sync = () => window.zbkConsent.update(CookieConsent.acceptedCategory('analytics'));
await CookieConsent.run({
  mode: 'opt-in', revision: 1, hideFromBots: false,
  disablePageInteraction: false, manageScriptTags: false,
  cookie: {name: 'zbk_consent', path: '/', domain: location.hostname, sameSite: 'Lax', expiresAfterDays: 180},
  guiOptions: {
    consentModal: {layout: 'box wide', position: 'bottom center', equalWeightButtons: true},
    preferencesModal: {layout: 'box', equalWeightButtons: true}
  },
  onConsent: sync, onChange: sync,
  categories: {
    necessary: {enabled: true, readOnly: true},
    analytics: {enabled: false, autoClear: {cookies: [{name: /^_ga/}, {name: '_gid'}, {name: /^_gat/}]}}
  },
  language: {default: 'de', translations: {de: {
    consentModal: {
      title: 'Ihre Privatsphäre zählt',
      description: 'Wir speichern Ihre Auswahl in einem notwendigen Cookie. Optionale Statistik ist freiwillig und derzeit noch nicht aktiv: Auch bei Zustimmung werden noch keine Analyse- oder Werbedienste geladen. Sie können Ihre Auswahl jederzeit im Fußbereich ändern oder widerrufen.',
      acceptAllBtn: 'Alle akzeptieren', acceptNecessaryBtn: 'Alle ablehnen', showPreferencesBtn: 'Einstellungen',
      footer: '<a href="/datenschutz.html">Datenschutz</a> <a href="/impressum.html">Impressum</a>'
    },
    preferencesModal: {
      title: 'Datenschutzeinstellungen', acceptAllBtn: 'Alle akzeptieren', acceptNecessaryBtn: 'Alle ablehnen',
      savePreferencesBtn: 'Auswahl speichern', closeIconLabel: 'Schließen',
      sections: [
        {title: 'Sie entscheiden', description: 'Ablehnen und Akzeptieren sind gleichwertig. Die Ratgeber bleiben ohne optionale Einwilligung nutzbar. Ihre Auswahl gilt 180 Tage und kann jederzeit geändert werden.'},
        {title: 'Notwendige Speicherung', linkedCategory: 'necessary', description: 'Das selbst gehostete CookieConsent speichert Ihre Auswahl und deren Zeitpunkt im Cookie zbk_consent (180 Tage, nur diese Website). Keine Übertragung an einen CMP-Anbieter.'},
        {title: 'Optionale Statistik (noch nicht aktiv)', linkedCategory: 'analytics', description: 'Diese Auswahl steuert ausschließlich analytics_storage. Google Analytics 4, Google Tag Manager und Stape sind noch nicht eingebunden. Ihre Zustimmung aktiviert derzeit keine Messung. Vor einer Aktivierung werden Anbieter, Zwecke und Speicherfristen ergänzt und Ihre Einwilligung erneut abgefragt. Werbung, Werbedaten und personalisierte Werbung bleiben immer abgelehnt.'}
      ]
    }
  }}}
});
document.querySelector('[data-consent-settings]').addEventListener('click', () => CookieConsent.showPreferences());
document.querySelector('[data-consent-withdraw]').addEventListener('click', () => {
  CookieConsent.acceptCategory([]);
  CookieConsent.hide();
  CookieConsent.hidePreferences();
  document.querySelector('[data-consent-status]').textContent = 'Optionale Einwilligung widerrufen. Es bleiben nur notwendige Speicherungen.';
});
