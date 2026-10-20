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
