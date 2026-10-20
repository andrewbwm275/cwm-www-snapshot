# Form handler (previews only)

- Endpoint: same-origin `POST /api/submit` on each Pages project (`functions/api/submit.js` -> `lib/site-forms.js`).
  Source of truth: `/workspace/site-forms/src/index.js` (also deployable as a standalone Worker once the token has Workers Scripts:Edit).
- Order: size/field limits -> site allowlist -> rate limit (5 / IP-hash / site / 10 min, D1) -> honeypot (`website`, stored as spam, no email)
  -> Turnstile siteverify -> INSERT into D1 `site-forms.submissions` (status pending) -> email -> UPDATE email_status (sent|failed).
- D1: `site-forms` 764f62e9-cb8b-4c4f-8531-49734bd31d54, one table, `site` column.
- Turnstile: widget sitekey 0x4AAAAAAFc4clI_QPR6kbAo (public), secret only in Pages secrets (production env). Preview env secret is a random value = preview branches fail closed.
- Email: NOT live yet. `EMAIL` (send_email) binding is commented out in wrangler.toml until Cloudflare Email Sending is onboarded on forms.carwashmgmt.com
  (needs Andrew's yes for 4 DNS records under the forms. subdomain; root MX untouched). Until then rows are stored with email_status=failed / E_NOT_CONFIGURED.
- No auto-reply to submitters. Subject: `Website lead: <form> – <site>`, To andrew@carwashmgmt.com, Reply-To = submitter.
- AMBR: Zapier webhook removed from the copy (rotate it in Zapier; it was public in the live bundle). Sign In buttons hidden.
