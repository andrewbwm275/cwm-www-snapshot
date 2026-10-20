/* site-forms client: Turnstile + honeypot + POST to the shared site-forms Worker.
   Config comes from window.__SITE_FORMS__ = { endpoint, sitekey, site }. No secrets here. */
(function () {
  var cfg = window.__SITE_FORMS__ || {};
  var tsLoading = null;

  function loadTurnstile() {
    if (window.turnstile) return Promise.resolve(window.turnstile);
    if (tsLoading) return tsLoading;
    tsLoading = new Promise(function (resolve, reject) {
      var s = document.createElement("script");
      s.src = "https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit";
      s.async = true;
      s.onload = function () { resolve(window.turnstile); };
      s.onerror = function () { tsLoading = null; reject(new Error("turnstile_load_failed")); };
      document.head.appendChild(s);
    });
    return tsLoading;
  }

  // Fresh single-use token per submission. The widget only shows itself if Cloudflare needs interaction.
  function getToken() {
    return loadTurnstile().then(function (ts) {
      return new Promise(function (resolve, reject) {
        var box = document.createElement("div");
        box.setAttribute("data-site-forms-turnstile", "");
        box.style.cssText = "position:fixed;left:50%;bottom:16px;transform:translateX(-50%);z-index:2147483647";
        document.body.appendChild(box);
        var done = function (fn, v) { try { ts.remove(id); } catch (e) {} box.remove(); fn(v); };
        var id = ts.render(box, {
          sitekey: cfg.sitekey,
          appearance: "interaction-only",
          callback: function (t) { done(resolve, t); },
          "error-callback": function () { done(reject, new Error("turnstile_error")); },
          "timeout-callback": function () { done(reject, new Error("turnstile_timeout")); }
        });
      });
    });
  }

  function honeypotValue() {
    var hp = document.getElementById("sf-hp-website");
    if (!hp) {
      hp = document.createElement("input");
      hp.type = "text"; hp.name = "website"; hp.id = "sf-hp-website"; hp.tabIndex = -1;
      hp.autocomplete = "off"; hp.setAttribute("aria-hidden", "true");
      hp.style.cssText = "position:absolute;left:-10000px;top:auto;width:1px;height:1px;overflow:hidden";
      document.body.appendChild(hp);
    }
    return hp.value || "";
  }

  function submit(form, fields) {
    var hp = honeypotValue();
    var tok = hp ? Promise.resolve("") : getToken().catch(function (e) {
      alert("Sorry, the spam check could not load. Please try again."); e.shown = true; throw e; });
    return tok.then(function (token) {
      return fetch(cfg.endpoint, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ site: cfg.site, form: form, fields: fields || {}, page: location.href,
                               hp: hp, turnstileToken: token })
      });
    }).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (b) {
        if (!r.ok || !b.ok) {
          var msg = r.status === 429 ? "Too many submissions. Please try again in a few minutes."
                  : "Sorry, your message could not be sent. Please email us or call.";
          alert(msg);
          var err = new Error(b.error || ("http_" + r.status)); err.shown = true; throw err;
        }
        return b;
      });
    }, function (e) {
      if (!e.shown) alert("Sorry, your message could not be sent. Please email us or call.");
      throw e;
    });
  }

  window.SiteForms = { submit: submit, honeypotValue: honeypotValue };
})();
