// site-forms: shared form handler for the ambrsystems.com and carwashmgmt.com static copies.
// Flow: CORS check -> size/shape validation -> rate limit -> honeypot -> Turnstile ->
//       INSERT into D1 -> email andrew@ via Email Service binding -> UPDATE email_status.
// No auto-reply is ever sent to the submitter.

const SITES = new Set(["ambrsystems.com", "carwashmgmt.com"]);
const MAX_BODY = 32 * 1024;
const MAX_FIELDS = 60;
const MAX_VALUE = 5000;
const RATE_WINDOW_MIN = 10;
const RATE_MAX = 5; // per IP per site per 10 minutes

const json = (data, status, cors) =>
  new Response(JSON.stringify(data), {
    status,
    headers: { "content-type": "application/json", "cache-control": "no-store", ...cors },
  });

function corsHeaders(origin, env) {
  const allowed = (env.ALLOWED_ORIGINS || "").split(",").map((s) => s.trim()).filter(Boolean);
  const ok = origin && allowed.some((a) => a === origin ||
    (a.startsWith("https://*.") && origin.startsWith("https://") && origin.endsWith(a.slice("https://*".length))));
  if (!ok) return null;
  return {
    "access-control-allow-origin": origin,
    "access-control-allow-methods": "POST, OPTIONS",
    "access-control-allow-headers": "content-type",
    "access-control-max-age": "86400",
    vary: "Origin",
  };
}

async function sha256(s) {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

function clean(v) {
  if (v === null || v === undefined) return "";
  if (typeof v === "boolean") return v ? "Yes" : "No";
  if (typeof v === "object") v = JSON.stringify(v);
  return String(v).slice(0, MAX_VALUE);
}

function pick(fields, re) {
  for (const [k, v] of Object.entries(fields)) if (re.test(k) && v) return v;
  return null;
}

async function verifyTurnstile(token, ip, env) {
  if (!token) return { success: false, "error-codes": ["missing-input-response"] };
  const body = new FormData();
  body.append("secret", env.TURNSTILE_SECRET);
  body.append("response", token);
  if (ip) body.append("remoteip", ip);
  body.append("idempotency_key", crypto.randomUUID());
  const r = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", { method: "POST", body });
  return r.json();
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const origin = request.headers.get("origin");
    const cors = corsHeaders(origin, env);

    if (url.pathname === "/health") return json({ ok: true }, 200, {});
    if (url.pathname !== "/submit" && url.pathname !== "/api/submit") return json({ ok: false, error: "not_found" }, 404, {});
    if (!cors) return json({ ok: false, error: "origin_not_allowed" }, 403, {});
    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: cors });
    if (request.method !== "POST") return json({ ok: false, error: "method_not_allowed" }, 405, cors);

    const raw = await request.text();
    if (raw.length > MAX_BODY) return json({ ok: false, error: "too_large" }, 413, cors);
    let p;
    try { p = JSON.parse(raw); } catch { return json({ ok: false, error: "bad_json" }, 400, cors); }

    const site = String(p.site || "");
    const form = String(p.form || "").slice(0, 80).trim();
    if (!SITES.has(site) || !form || typeof p.fields !== "object" || !p.fields)
      return json({ ok: false, error: "bad_request" }, 400, cors);
    const entries = Object.entries(p.fields).slice(0, MAX_FIELDS);
    const fields = Object.fromEntries(entries.map(([k, v]) => [String(k).slice(0, 120), clean(v)]));

    const ip = request.headers.get("cf-connecting-ip") || "";
    const ipHash = await sha256(`${env.IP_HASH_SALT || "site-forms"}|${ip}`);

    // Basic rate limit (D1-backed, per IP + site).
    const recent = await env.DB.prepare(
      `SELECT COUNT(*) AS n FROM submissions WHERE ip_hash = ?1 AND site = ?2
       AND created_at > strftime('%Y-%m-%dT%H:%M:%fZ','now', ?3)`
    ).bind(ipHash, site, `-${RATE_WINDOW_MIN} minutes`).first();
    if (recent && recent.n >= RATE_MAX) return json({ ok: false, error: "rate_limited" }, 429, cors);

    const name = pick(fields, /(^|_|\s)(full[_ ]?name|name|first[_ ]?name)$/i);
    const email = pick(fields, /e-?mail/i);
    const phone = pick(fields, /phone|tel/i);
    const meta = [site, form, JSON.stringify(fields), name, email, phone,
      clean(p.page).slice(0, 500), origin, ipHash, (request.headers.get("user-agent") || "").slice(0, 300)];

    // Honeypot: store for audit, return a normal-looking success, never email.
    if (p.hp) {
      await env.DB.prepare(
        `INSERT INTO submissions (site, form, fields_json, name, email, phone, page_url, origin, ip_hash, user_agent,
          turnstile_ok, spam_reason, email_status) VALUES (?1,?2,?3,?4,?5,?6,?7,?8,?9,?10,0,'honeypot','skipped')`
      ).bind(...meta).run();
      return json({ ok: true }, 200, cors);
    }

    const ts = await verifyTurnstile(p.turnstileToken, ip, env);
    if (!ts.success) return json({ ok: false, error: "turnstile_failed", codes: ts["error-codes"] || [] }, 403, cors);

    // 1) Store first.
    const ins = await env.DB.prepare(
      `INSERT INTO submissions (site, form, fields_json, name, email, phone, page_url, origin, ip_hash, user_agent,
        turnstile_ok, email_status) VALUES (?1,?2,?3,?4,?5,?6,?7,?8,?9,?10,1,'pending') RETURNING id`
    ).bind(...meta).first();
    const id = ins.id;

    // 2) Email Andrew (no auto-reply to the submitter).
    const subject = `Website lead: ${form} – ${site}`;
    const lines = Object.entries(fields).map(([k, v]) => `${k}: ${v}`);
    const text = [`Site: ${site}`, `Form: ${form}`, `Page: ${clean(p.page)}`, `Submission ID: ${id}`,
      `Received: ${new Date().toISOString()}`, "", "Fields:", ...lines].join("\n");
    const validEmail = email && /^[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+$/.test(email) ? email : undefined;
    try {
      if (!env.EMAIL) throw Object.assign(new Error("email binding not configured (Email Sending not onboarded yet)"), { code: "E_NOT_CONFIGURED" });
      const res = await env.EMAIL.send({
        to: env.LEAD_TO,
        from: { email: env.LEAD_FROM, name: "Website Leads" },
        subject,
        text,
        ...(validEmail ? { replyTo: validEmail } : {}),
      });
      await env.DB.prepare(
        `UPDATE submissions SET email_status='sent', email_message_id=?2, emailed_at=strftime('%Y-%m-%dT%H:%M:%fZ','now') WHERE id=?1`
      ).bind(id, (res && res.messageId) || null).run();
      return json({ ok: true, id, email: "sent" }, 200, cors);
    } catch (e) {
      await env.DB.prepare(`UPDATE submissions SET email_status='failed', email_error=?2 WHERE id=?1`)
        .bind(id, `${e.code || ""} ${e.message || e}`.slice(0, 500)).run();
      // Lead is safely stored, so the visitor still gets a success response.
      return json({ ok: true, id, email: "failed_stored" }, 200, cors);
    }
  },
};
