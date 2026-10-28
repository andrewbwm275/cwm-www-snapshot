/* Car Wash Management site script: first-party conversion events + service-request form.
   No third-party trackers. Form posts through window.SiteForms (assets/js/site-forms.js:
   Turnstile + honeypot + POST /api/submit, same contract as the existing forms). */
(function () {
  "use strict";
  // ---- Conversion events (feature flag, off by default) ----
  var ev = window.__CWM_EVENTS__ || {};
  function track(type) {
    if (!ev.enabled || !ev.endpoint) return;
    try { if (sessionStorage.getItem("cwm_ev_off")) return; } catch (e) {}
    var body = JSON.stringify({ type: type, page: location.pathname });
    try {
      fetch(ev.endpoint, { method: "POST", headers: { "content-type": "application/json" }, body: body, keepalive: true })
        .then(function (r) { if (r.status === 404 || r.status === 405) { try { sessionStorage.setItem("cwm_ev_off", "1"); } catch (e) {} } })
        .catch(function () {});
    } catch (e) {}
  }
  window.CWMTrack = track;
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("[data-evt]");
    if (a) track(a.getAttribute("data-evt"));
  });

  // ---- Service-request form ----
  function val(f, n) { var el = f.elements[n]; return el ? String(el.value || "").trim() : ""; }
  function radio(f, n) { var el = f.querySelector('input[name="' + n + '"]:checked'); return el ? el.value : ""; }
  function utm() {
    var out = {}, q = new URLSearchParams(location.search);
    ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "gclid"].forEach(function (k) { if (q.get(k)) out[k] = q.get(k).slice(0, 200); });
    return out;
  }
  function fieldsOf(f) {
    var consent = f.elements.consent;
    var sms = f.elements.sms_consent;
    var o = {
      name: val(f, "name"), business_site: val(f, "business_site"), email: val(f, "email"), phone: val(f, "phone"),
      city: val(f, "city"), request_type: val(f, "request_type"), equipment_brand: val(f, "equipment_brand"),
      message: val(f, "message"), preferred_contact: radio(f, "preferred_contact"),
      consent: consent && consent.checked ? "Yes" : "No",
      consent_text: consent ? (consent.closest("label").textContent || "").replace(/\s+/g, " ").trim() : "",
      sms_consent: sms && sms.checked ? "Yes" : "No",
      sms_consent_text: sms ? (sms.closest("label").textContent || "").replace(/\s+/g, " ").trim() : "",
      form_location: f.getAttribute("data-form-location") || location.pathname,
      referrer: document.referrer ? document.referrer.slice(0, 300) : ""
    };
    var u = utm(); for (var k in u) o[k] = u[k];
    return o;
  }
  function showErrors(f) {
    var first = null;
    f.querySelectorAll("input,select,textarea").forEach(function (c) {
      var wrap = c.closest(".field") || c.closest(".check");
      if (!wrap || !c.willValidate) return;
      var bad = !c.validity.valid;
      wrap.classList.toggle("invalid", bad);
      var msg = wrap.querySelector(".err");
      if (msg) msg.textContent = bad ? (c.getAttribute("data-err") || c.validationMessage) : "";
      if (bad && !first) first = c;
    });
    if (first) first.focus();
    return !first;
  }
  function wire(f) {
    f.setAttribute("novalidate", "");
    f.addEventListener("input", function (e) {
      var w = e.target.closest(".field, .check");
      if (w && w.classList.contains("invalid") && e.target.validity.valid) { w.classList.remove("invalid"); var m = w.querySelector(".err"); if (m) m.textContent = ""; }
    });
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!showErrors(f)) return;
      if (!window.SiteForms) { alert("Sorry, the form could not load. Please call or text (808) 465-2291."); return; }
      var btn = f.querySelector('[type="submit"]'), label = btn ? btn.innerHTML : "";
      if (btn) { btn.disabled = true; btn.textContent = "Sending..."; }
      window.SiteForms.submit("Service request", fieldsOf(f)).then(function () {
        track("form_submit");
        location.href = "/thank-you/";
      }, function () { if (btn) { btn.disabled = false; btn.innerHTML = label; } });
    });
  }
  window.CWMForm = { fieldsOf: fieldsOf };
  function init() { if (window.SiteForms && document.querySelector("form[data-cwm-request]")) window.SiteForms.honeypotValue(); document.querySelectorAll("form[data-cwm-request]").forEach(wire); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
