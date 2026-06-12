/* ================================================
   hostazar.com — Cookie Consent Manager
   DSGVO-konformes Einwilligungsmanagement
   ================================================ */
(function () {
  'use strict';

  var STORAGE_KEY = 'hostazar_consent';
  var CONSENT_EXPIRY_DAYS = 365; // 12 Monate gemäß DSGVO

  // Categories
  var CATEGORIES = {
    necessary: {
      label: 'Notwendig',
      desc: 'Technisch erforderliche Cookies (CDN, Sicherheit). Immer aktiv.'
    },
    adsense: {
      label: 'Google AdSense',
      desc: 'Personalisierte Werbung. Google kann Cookies setzen und Daten zur Anzeigenpersonalisierung verwenden.'
    },
    amazon: {
      label: 'Amazon PartnerNet',
      desc: 'Affiliate-Cookies zur Zuordnung von Provisionen bei Klicks auf Amazon-Links.'
    }
  };

  // Current consent state
  var consent = null;

  /* ---- Storage Helpers ---- */
  function loadConsent() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return null;
      var data = JSON.parse(raw);
      // Check expiry
      if (data.expires && Date.now() > data.expires) {
        localStorage.removeItem(STORAGE_KEY);
        return null;
      }
      return data;
    } catch (e) {
      return null;
    }
  }

  function saveConsent(preferences) {
    var data = {
      preferences: preferences,
      expires: Date.now() + CONSENT_EXPIRY_DAYS * 24 * 60 * 60 * 1000,
      timestamp: new Date().toISOString()
    };
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
      // Also set old-style key for compatibility with data/script.js
      localStorage.setItem('hostazar_cookie_consent', '1');
    } catch (e) {
      // localStorage full or unavailable
    }
    consent = data;
  }

  function clearConsent() {
    try {
      localStorage.removeItem(STORAGE_KEY);
    } catch (e) {}
    consent = null;
  }

  /* ---- Conditional Script Loading ---- */
  function getAdSenseScripts() {
    // Find scripts that have data-hz-src set for AdSense
    return document.querySelectorAll('script[data-hz-src]');
  }

  function loadAdSense() {
    var scripts = getAdSenseScripts();
    scripts.forEach(function (script) {
      if (script.getAttribute('data-hz-loaded')) return;
      script.setAttribute('src', script.getAttribute('data-hz-src'));
      script.removeAttribute('data-hz-src');
      script.setAttribute('data-hz-loaded', '1');
    });
  }

  function unloadAdSense() {
    // We can't truly "unload" a script once executed, but we remove the ad iframes
    // This is best-effort: the page should be reloaded to fully remove ads
    var adIframes = document.querySelectorAll('iframe[src*="googlesyndication"], ins.adsbygoogle');
    adIframes.forEach(function (el) {
      el.style.display = 'none';
    });
  }

  function applyConsent(preferences) {
    if (!preferences) {
      // No consent given — don't load marketing scripts
      unloadAdSense();
      return;
    }

    if (preferences.adsense === true) {
      loadAdSense();
    } else {
      unloadAdSense();
    }
    // Amazon Affiliates work via regular links — no script to load/unload
  }

  /* ---- Banner ---- */
  function createBanner() {
    var banner = document.createElement('div');
    banner.className = 'hz-consent-banner';
    banner.id = 'hzConsentBanner';
    banner.innerHTML =
      '<div class="hz-banner-inner">' +
        '<p>🍪 Diese Website verwendet Cookies und Dienste wie Google AdSense sowie Amazon Affiliate-Links. Mit Klick auf "Alle akzeptieren" stimmst du der Verwendung zu. <a href="/datenschutz.html">Mehr erfahren</a></p>' +
        '<div class="hz-banner-buttons">' +
          '<button class="hz-btn hz-btn-accept" id="hzAcceptAll">Alle akzeptieren</button>' +
          '<button class="hz-btn hz-btn-reject" id="hzRejectAll">Ablehnen</button>' +
          '<button class="hz-btn hz-btn-settings" id="hzOpenSettings">Einstellungen</button>' +
        '</div>' +
      '</div>';
    document.body.appendChild(banner);

    // Show after a short delay
    setTimeout(function () {
      banner.classList.add('show');
    }, 500);

    // Bind events
    document.getElementById('hzAcceptAll').addEventListener('click', function () {
      acceptAll();
      hideBanner();
    });
    document.getElementById('hzRejectAll').addEventListener('click', function () {
      rejectAll();
      hideBanner();
    });
    document.getElementById('hzOpenSettings').addEventListener('click', function () {
      openModal();
    });

    return banner;
  }

  function hideBanner() {
    var banner = document.getElementById('hzConsentBanner');
    if (banner) {
      banner.classList.remove('show');
      setTimeout(function () {
        if (banner.parentNode) banner.parentNode.removeChild(banner);
      }, 400);
    }
  }

  /* ---- Modal ---- */
  function createModal() {
    var overlay = document.createElement('div');
    overlay.className = 'hz-modal-overlay';
    overlay.id = 'hzModalOverlay';

    var catsHtml = '';
    var catKeys = Object.keys(CATEGORIES);
    catKeys.forEach(function (key) {
      var cat = CATEGORIES[key];
      var checked = consent && consent.preferences && consent.preferences[key] === true;
      var disabled = key === 'necessary' ? ' disabled checked' : '';
      var toggleClass = key === 'necessary' ? ' hz-toggle-required' : '';
      catsHtml +=
        '<div class="hz-category">' +
          '<div class="hz-category-info">' +
            '<h4>' + cat.label + '</h4>' +
            '<p>' + cat.desc + '</p>' +
          '</div>' +
          '<label class="hz-toggle' + toggleClass + '">' +
            '<input type="checkbox" id="hzCat_' + key + '"' +
              (checked || key === 'necessary' ? ' checked' : '') +
              disabled + '>' +
            '<span class="hz-toggle-slider"></span>' +
          '</label>' +
        '</div>';
    });

    overlay.innerHTML =
      '<div class="hz-modal">' +
        '<div class="hz-modal-header">' +
          '<h2>Cookie-Einstellungen</h2>' +
          '<button class="hz-modal-close" id="hzModalClose">&times;</button>' +
        '</div>' +
        '<div class="hz-modal-body">' +
          '<p>Wähle aus, welche Cookies und Dienste du zulassen möchtest. Notwendige Cookies sind immer aktiv.</p>' +
          catsHtml +
        '</div>' +
        '<div class="hz-modal-footer">' +
          '<button class="hz-btn hz-btn-accept" id="hzSaveSettings">Auswahl speichern</button>' +
          '<button class="hz-btn hz-btn-accept" id="hzModalAcceptAll">Alle akzeptieren</button>' +
          '<button class="hz-btn hz-btn-reject" id="hzModalRejectAll">Alle ablehnen</button>' +
        '</div>' +
      '</div>';

    document.body.appendChild(overlay);

    // Bind events
    document.getElementById('hzModalClose').addEventListener('click', closeModal);
    document.getElementById('hzSaveSettings').addEventListener('click', function () {
      saveFromModal();
      closeModal();
      hideBanner();
    });
    document.getElementById('hzModalAcceptAll').addEventListener('click', function () {
      acceptAll();
      closeModal();
      hideBanner();
    });
    document.getElementById('hzModalRejectAll').addEventListener('click', function () {
      rejectAll();
      closeModal();
      hideBanner();
    });

    // Close on overlay click
    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) closeModal();
    });

    return overlay;
  }

  function openModal() {
    var overlay = document.getElementById('hzModalOverlay');
    if (!overlay) {
      overlay = createModal();
    }
    // Sync checkboxes with current consent
    if (consent && consent.preferences) {
      var catKeys = Object.keys(CATEGORIES);
      catKeys.forEach(function (key) {
        var cb = document.getElementById('hzCat_' + key);
        if (cb && key !== 'necessary') {
          cb.checked = consent.preferences[key] === true;
        }
      });
    }
    overlay.classList.add('open');
  }

  function closeModal() {
    var overlay = document.getElementById('hzModalOverlay');
    if (overlay) overlay.classList.remove('open');
  }

  function saveFromModal() {
    var prefs = {};
    var catKeys = Object.keys(CATEGORIES);
    catKeys.forEach(function (key) {
      var cb = document.getElementById('hzCat_' + key);
      prefs[key] = cb ? cb.checked : false;
    });
    saveConsent(prefs);
    applyConsent(prefs);
    showToast('Deine Einstellungen wurden gespeichert.');
  }

  /* ---- Consent Actions ---- */
  function acceptAll() {
    var prefs = {};
    var catKeys = Object.keys(CATEGORIES);
    catKeys.forEach(function (key) {
      prefs[key] = true;
    });
    saveConsent(prefs);
    applyConsent(prefs);
    showToast('✅ Alle Cookies akzeptiert.');
  }

  function rejectAll() {
    var prefs = {};
    var catKeys = Object.keys(CATEGORIES);
    catKeys.forEach(function (key) {
      prefs[key] = key === 'necessary'; // only necessary
    });
    saveConsent(prefs);
    applyConsent(prefs);
    showToast('Nur notwendige Cookies aktiv.');
  }

  /* ---- Toast Notification ---- */
  function showToast(message) {
    var existing = document.getElementById('hzToast');
    if (existing) {
      existing.parentNode.removeChild(existing);
    }
    var toast = document.createElement('div');
    toast.className = 'hz-toast';
    toast.id = 'hzToast';
    toast.innerHTML = '<p>' + message + '</p>';
    document.body.appendChild(toast);
    // Trigger animation
    requestAnimationFrame(function () {
      toast.classList.add('show');
    });
    // Auto-hide after 4 seconds
    setTimeout(function () {
      toast.classList.remove('show');
      setTimeout(function () {
        if (toast.parentNode) toast.parentNode.removeChild(toast);
      }, 300);
    }, 4000);
  }

  /* ---- Withdrawal Function (public) ---- */
  window.hzWithdrawConsent = function () {
    clearConsent();
    applyConsent(null);
    // Show banner again
    var existingBanner = document.getElementById('hzConsentBanner');
    if (existingBanner) {
      existingBanner.parentNode.removeChild(existingBanner);
    }
    createBanner();
    // Remove modal if open
    closeModal();
    showToast('Einwilligung zurückgezogen. Bitte Seite neu laden, um Änderungen zu aktivieren.');
  };

  /* ---- Reopen Banner Function (public) ---- */
  window.hzReopenBanner = function () {
    // Clear existing consent to force banner
    var existing = loadConsent();
    if (!existing) {
      // No consent at all — just create the banner if not visible
      var banner = document.getElementById('hzConsentBanner');
      if (!banner || !banner.classList.contains('show')) {
        if (banner) banner.parentNode.removeChild(banner);
        createBanner();
      }
    } else {
      // Consent exists — show the modal for settings
      openModal();
    }
  };

  /* ---- Init ---- */
  function init() {
    var saved = loadConsent();
    if (saved && saved.preferences) {
      // Consent already given — apply it silently
      consent = saved;
      applyConsent(saved.preferences);
    } else {
      // No consent yet — show banner, block marketing scripts
      applyConsent(null);
      createBanner();
    }
  }

  // Run on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
