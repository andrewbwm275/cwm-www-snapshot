# carwashmgmt.com DNS record map (read-only discovery, 2026-10-19 PT)

Zone is on **Cloudflare** (Free plan, zone 28608fd463ce0a75b95398c9690de613, NS aaron/saanvi.ns.cloudflare.com;
moved from GoDaddy ns43/ns44.domaincontrol.com). Registrar GoDaddy (expires 2028-01-24, locked).
The box API token cannot read DNS records, so this map comes from public DNS plus the Access app list.
Export the full zone from the Cloudflare dashboard (DNS > Records > Export) to confirm before any change.

## Web (the ONLY records a cutover touches)
| Name | Type | Value (public) | Notes |
|---|---|---|---|
| @ | A/AAAA (proxied) | 104.21.56.150, 172.67.152.190 / 2606:4700:... | 301 to https://www.carwashmgmt.com/ (Cloudflare redirect rule or Worker) |
| www | proxied (CNAME -> andrewbwm275.github.io expected) | Cloudflare IPs | origin is **GitHub Pages**, repo andrewbwm275/cwm-www-snapshot (CNAME file = www.carwashmgmt.com) |

## DO NOT TOUCH: tunnel / Access hostnames (all proxied)
nas, ssh-optiplex, ssh-laptop (Access app "nas"), crm (Access "crm"), hooks (Access "hooks",
"hooks-cloudtalk-webhook"), bot (Access "fieldbot", "fieldbot-twilio-webhooks"), jarvis-fortyone.
legal = CNAME andrewbwm275.github.io (DNS-only, GitHub Pages legal site). _domainconnect TXT (Cloudflare).

## EMAIL (Google Workspace) - leave untouched
| Name | Type | TTL | Value |
|---|---|---|---|
| @ | MX | 300 | 1 aspmx.l.google.com.; 5 alt1/alt2; 10 alt3/alt4 .aspmx.l.google.com. |
| @ | TXT | 300 | `v=spf1 include:_spf.google.com` (**no `~all`/`-all` terminator**) |
| _dmarc | TXT | - | **none published** |
| google._domainkey | TXT | - | **none published** (no DKIM found on common selectors) |
| google-site-verification | TXT | - | none visible at apex |

Recommended (separate from cutover, Andrew's yes): add `~all` to SPF, publish Google DKIM, add DMARC `p=none` with reporting.

## Email signature images
https://www.carwashmgmt.com/email-signature/{cw-logo,cw-email,cw-phone,cw-web}.png are served by GitHub Pages
from the `main` branch of this repo (via the Cloudflare-proxied www). The apex URL 301s to www.
They must stay at the same URLs on any new host; the Pages preview serves them byte-identical.
