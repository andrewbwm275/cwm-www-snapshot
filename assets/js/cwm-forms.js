/* CWM adapter: wires the static forms to SiteForms (Turnstile + honeypot + shared handler). */
(function () {
  var NAMES = { "": "Homepage lead", "index": "Homepage lead", "contact": "Contact",
                "equipment": "Equipment quote", "preventive-maintenance": "Preventive maintenance booking" };
  function pageKey() { return location.pathname.replace(/^\/+|\.html$|\/+$/g, "").split("/").pop() || ""; }
  function text(el) { return (el && el.textContent || "").replace(/\s+/g, " ").trim(); }
  function labelFor(ctrl, i) {
    if (ctrl.name) return ctrl.name;
    if (ctrl.id) { var l = document.querySelector('label[for="' + ctrl.id + '"]'); if (l) return text(l); }
    var wrap = ctrl.closest("label"); if (wrap) return text(wrap).slice(0, 120);
    var p = ctrl.parentElement;
    while (p && p.tagName !== "FORM") {
      var lab = p.querySelector(":scope > label"); if (lab) return text(lab);
      p = p.parentElement;
    }
    return ctrl.placeholder || (ctrl.type || ctrl.tagName.toLowerCase()) + "_" + i;
  }
  function collect(form) {
    var out = {};
    form.querySelectorAll("input, textarea, select").forEach(function (c, i) {
      if (c.id === "sf-hp-website" || c.type === "submit" || c.type === "button") return;
      var k = labelFor(c, i).replace(/\s*\*\s*$/, "");
      if (c.type === "checkbox" || c.type === "radio") { if (c.checked) out[k] = "Yes"; return; }
      if (c.value) out[k] = c.value;
    });
    form.querySelectorAll('button[aria-pressed="true"], button[data-selected="true"]').forEach(function (b, i) {
      out["Selected option " + (i + 1)] = text(b);
    });
    return out;
  }
  function wire(form) {
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var btn = form.querySelector('[type="submit"]'), label = btn && btn.innerHTML;
      if (btn) { btn.disabled = true; btn.textContent = "Sending..."; }
      window.SiteForms.submit(NAMES[pageKey()] || ("Form: " + pageKey()), collect(form)).then(function () {
        var ok = document.createElement("div");
        ok.setAttribute("role", "status");
        ok.className = "p-6 rounded-xl bg-green-50 border border-green-200 text-green-800 text-center";
        ok.textContent = "Thanks! Your message has been sent. We'll get back to you shortly.";
        form.replaceWith(ok);
      }, function () { if (btn) { btn.disabled = false; btn.innerHTML = label; } });
    });
  }
  function init() { window.SiteForms.honeypotValue(); document.querySelectorAll("form").forEach(wire); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
