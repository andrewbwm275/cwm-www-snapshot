# CWM www snapshot (carwashmgmt.com)

Static copy of **www.carwashmgmt.com**. The `main` branch is what GitHub Pages serves today at
www.carwashmgmt.com (behind the Cloudflare proxy), including `/email-signature/*.png` used in
email signatures. **Do not break `main` or the CNAME file** until the Cloudflare Pages cutover is approved.

Proof URL (no custom domain bound): https://andrewbwm275.github.io/cwm-www-snapshot/
Do not edit [legal.carwashmgmt.com](https://legal.carwashmgmt.com/).

## Branch `cloudflare-pages-preview`
- Base44-hosted images moved local (no Base44 dependency left): favicon `2732c3225_9png.png` (14 pages),
  `10a2161d8_bg-.png` (about), `96fef0b92_Aboutbg.png` (solutions).
- Cloudflare Pages deploy root = repo minus `.git`, `workers/`, `README.md`, `CNAME`, `.gitignore`, `.nojekyll`.
  Project: `cwm-www` (*.pages.dev, no custom domain).
- `COMPARE-PAGES-PREVIEW.md`: live vs preview, all 14 pages + signature image identical.
- `DNS-RECORDS.md`: record map; cutover touches only apex/www.

## Known gaps (same on live)
- The 4 forms (index, contact, equipment, preventive-maintenance) have no action/backend.
- Broken links: fixed on branch `fix/404-and-dead-links` (Contact?type=chemistry -> contact.html; dead product/blog/testimonial links removed, cards kept).
- `404.html` (branch `fix/404-and-dead-links`): Pages returns it with HTTP 404 for unknown paths instead of the SPA-style index.html fallback.
- Touch Free booklet PDF still on Duda (irp.cdn-website.com, 47 MB, over Pages' 25 MiB/file limit).
- preventive-maintenance.html is live but not linked from any page.

## Branch `redesign` (Design direction A, first preview build)
- Built off `fix/404-and-dead-links` (keeps 404 handling and the `/api/submit` forms wiring). Local commits only; IT deploys.
- Source: `_build/build.py` (plain Python 3, no deps) + `_build/site.css` (inlined into every page). Run `python3 _build/build.py`
  from the repo root; it writes `index.html`, `<page>/index.html`, `404.html`, `sitemap.xml`, `robots.txt`, `_redirects`, `_headers`.
  `_build/` holds no secrets; IT may exclude it from the deploy root like `workers/`.
- Pages: `/`, `/car-wash-equipment-repair/`, `/car-wash-equipment-installation/`, `/car-wash-maintenance-plans/`,
  `/urgent-car-wash-repair/` (old `/emergency-car-wash-repair/` 301s here), `/equipment/`, `/service-area/`, `/chemistry/`, `/about/`, `/contact/`, `/thank-you/` (noindex), `404.html`.
  Old .html pages were removed and 301/302 to their new equivalents via `_redirects`. `privacy-policy.html` / `terms-and-conditions.html`
  are kept untouched (noindex via `_headers`); the footer links the legal.carwashmgmt.com copies.
- Fonts: Archivo + Inter (SIL OFL 1.1, licences in `assets/cwm/fonts/`), self-hosted, Latin subset, variable ranges trimmed.
- Form: `form[data-cwm-request]` -> `assets/cwm/js/cwm.js` -> `window.SiteForms.submit("Service request", fields)` (Turnstile + honeypot,
  unchanged `assets/js/site-forms.js` + `forms-config.js`). Success -> `/thank-you/`.
- Conversion events: `events-config.js` (`enabled:false`). When IT ships `POST /api/event`, set `enabled:true`.
  Payload `{"type":"tel_click|sms_click|form_submit","page":"/path/"}`; a 404/405 disables it for the session.
- All proof (photos, before/after, reviews, service area, chemistry offer, after-hours, callback time) is labeled PLACEHOLDER.
