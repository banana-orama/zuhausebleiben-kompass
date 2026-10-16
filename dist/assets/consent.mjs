import * as CookieConsent from './vendor/cookieconsent.esm.js';
import {installMeasurement} from './measurement.mjs';

// revision 2: invalidates all revision-1 selections (vanilla-cookieconsent re-shows the banner
// and stores the new revision). The consent-gated Web-GTM container accepts consent_version 2 only.
const sync = () => window.zbkConsent.update(CookieConsent.acceptedCategory('analytics'));
await CookieConsent.run({
  mode: 'opt-in', revision: 2, hideFromBots: false,
  disablePageInteraction: false, manageScriptTags: false,
  cookie: {name: 'zbk_consent', path: '/', domain: location.hostname, sameSite: 'Lax', expiresAfterDays: 180},
  guiOptions: {
    consentModal: {layout: 'box wide', position: 'bottom center', equalWeightButtons: true},
    preferencesModal: {layout: 'box', equalWeightButtons: true}
  },
  onConsent: () => { sync(); installMeasurement(); },
  onChange: () => { sync(); installMeasurement(); },
  categories: {
    necessary: {enabled: true, readOnly: true},
    analytics: {enabled: false, autoClear: {cookies: [{name: /^_ga/}, {name: '_gid'}, {name: /^_gat/}]}}
  },
  language: {default: 'de', translations: {de: {
    consentModal: {
      title: 'Ihre Privatsphäre zählt',
      description: 'Wir speichern Ihre Auswahl in einem notwendigen Cookie. Optional laden wir bei Ihrer Zustimmung Google Analytics 4 (Google Ireland Ltd.) über unseren eigenen Web-Google-Tag-Manager: Ihr Browser sendet die Messdaten dann direkt an Google. Es werden nur ereignisbezogene Klick- und Seitenaufrufdaten ohne Seiten-URLs, Suchbegriffe oder personenbezogene Inhalte übertragen; Ihre IP-Adresse wird dabei übertragen und von Google gekürzt. Details: Datenschutzerklärung. Sie können Ihre Auswahl jederzeit im Fußbereich ändern oder widerrufen.',
      acceptAllBtn: 'Alle akzeptieren', acceptNecessaryBtn: 'Alle ablehnen', showPreferencesBtn: 'Einstellungen',
      footer: '<a href="/datenschutz.html">Datenschutz</a> <a href="/impressum.html">Impressum</a>'
    },
    preferencesModal: {
      title: 'Datenschutzeinstellungen', acceptAllBtn: 'Alle akzeptieren', acceptNecessaryBtn: 'Alle ablehnen',
      savePreferencesBtn: 'Auswahl speichern', closeIconLabel: 'Schließen',
      sections: [
        {title: 'Sie entscheiden', description: 'Ablehnen und Akzeptieren sind gleichwertig. Die Ratgeber bleiben ohne optionale Einwilligung voll nutzbar. Ihre Auswahl gilt 180 Tage und kann jederzeit geändert oder widerrufen werden. Neu: Nach dieser Klarstellung des Einsatzes fragen wir erneut; eine frühere Auswahl ist damit widerrufen.'},
        {title: 'Notwendige Speicherung', linkedCategory: 'necessary', description: 'Das selbst gehostete CookieConsent speichert Ihre Auswahl und deren Zeitpunkt im Cookie zbk_consent (180 Tage, nur diese Website). Keine Übertragung an einen CMP-Anbieter.'},
        {title: 'Optionale Statistik', linkedCategory: 'analytics', description: 'Bei Zustimmung laden wir Google Analytics 4 (Google Ireland Ltd.) über unseren eigenen Web-Google-Tag-Manager (Google Ireland Ltd.): Ihr Browser sendet die Messdaten dann selbst und unmittelbar an Google; eigene Server- oder Proxy-Dienste sind nicht dazwischengeschaltet. Übertragen werden nur Seitenaufrufe und anonyme Klick-Ereignisse mit zufälligen Kennungen (keine Analyse-Cookies, keine Seiten-URLs, Suchbegriffe oder Eingaben). Ihre IP-Adresse wird bei der Übertragung an Google übermittelt und von Google bei der Erfassung gekürzt; Ereignisdaten werden bei Google nach 2 Monaten gelöscht. Werbung und personalisierte Werbung bleiben immer abgelehnt. Rechtsgrundlage ist Ihre Einwilligung (Art. 6 Abs. 1 lit. a DSGVO, § 25 Abs. 1 TDDDG); ein Widerruf beendet die Übertragungen sofort.'}
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
