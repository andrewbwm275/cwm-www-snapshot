#!/usr/bin/env python3
"""Car Wash Management redesign (Design direction A): static HTML generator.
Run from the repo root:  python3 _build/build.py
Writes index.html, <page>/index.html, 404.html, sitemap.xml, robots.txt, _redirects, _headers.
Plain Python 3, no dependencies. Shared header/footer live here; page copy lives in PAGES below.
Rules: confirmed facts only; all proof is labeled PLACEHOLDER; no stats, testimonials or logos invented."""
import html, json, pathlib, re, datetime, sys
sys.dont_write_bytecode = True
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from brands import CATS as BRAND_CATS
ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://www.carwashmgmt.com"
LASTMOD = "2026-10-20"
PHONE_D, PHONE_T = "(808) 465-2291", "+18084652291"
EMAIL = "info@carwashmgmt.com"
HOURS = "Mon–Fri 8 AM–5 PM PT"
BRANDS_URL = "/car-wash-equipment-brands/"
TM = ("Brand names are trademarks of their respective owners. Car Wash Management is an independent service company "
      "and is not affiliated with or endorsed by these manufacturers.")
# SMS opt-in small print: kept exactly as on the current site (fix/404-and-dead-links footer), option (a).
SMS_OPTIN = """<aside id="sms-opt-in" class="sms-optin">
  <p>The only way to opt in to Car Wash Management customer-care texts is to text the keyword <strong>START</strong> to <strong>+1 619-914-6819</strong>. Keyword-only. No website form, checkbox, paper form, or in-person consent. Consent is not a condition of purchase.</p>
  <p>Reply <strong>STOP</strong> to opt out. Reply <strong>HELP</strong> for help, email <a href="mailto:info@carwashmgmt.com">info@carwashmgmt.com</a>, or call <a href="tel:+18084652291" data-evt="tel_click">808-465-2291</a>. Message frequency varies. You may receive up to 8 customer-care messages per month, plus replies. Message and data rates may apply.</p>
  <p>We do not share, sell, or provide your mobile phone number or messaging consent data to third parties or affiliates for marketing or promotional purposes. <a href="https://legal.carwashmgmt.com/privacy-policy.html">Privacy Policy</a> · <a href="https://legal.carwashmgmt.com/terms-and-conditions.html">Terms &amp; Conditions</a>.</p>
</aside>"""
NAV = [("/car-wash-equipment-repair/", "Repair"), ("/car-wash-equipment-installation/", "Installation"),
       ("/car-wash-maintenance-plans/", "Maintenance Plans"), (BRANDS_URL, "Brands"),
       ("/service-area/", "Service Area"), ("/chemistry/", "Chemistry"), ("/about/", "About")]
I_PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>'
I_SMS = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>'
I_ARR = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 5l7 7-7 7"/></svg>'
I_MENU = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'

def call_btn(cls="btn btn-blue", label=f"Call {PHONE_D}"):
    return f'<a class="{cls}" href="tel:{PHONE_T}" data-evt="tel_click">{I_PHONE} {label}</a>'
def text_btn(cls="btn btn-ghost", label="Text us"):
    return f'<a class="{cls}" href="sms:{PHONE_T}" data-evt="sms_click">{I_SMS} {label}</a>'
def ph(label, dark=False, cls=""):
    return f'<div class="ph{" dark" if dark else ""} {cls}" role="img" aria-label="Placeholder: {html.escape(label)}"><span>PLACEHOLDER: {label}</span></div>'
def tag(t): return f'<span class="tag-ph">{t}</span>'

# Photos (Design manifest /workspace/brand/cwm-redesign/images/manifest.csv: PICK rows + Andrew's real-job strip).
# key: (alt text from manifest, large w, large h, small w, small h, stock credit or None). Stock is never captioned as our work.
IMG_DIR = "/assets/cwm/img/photos/"
PEXELS = ("Pexels License", "https://www.pexels.com/license/")
UNSPLASH = ("Unsplash License", "https://unsplash.com/license")
IMG = {
 "home-hero": ("Red car in an automatic tunnel wash between red and blue cloth brushes, covered in soap", 1600, 900, 800, 450,
               ("Pixabay (via Pexels)", "https://www.pexels.com/photo/red-and-black-banner-210627/", *PEXELS)),
 "chemistry-page-hero": ("Close-up of blue soap foam bubbles", 1600, 900, 800, 450,
               ("Julia Ly", "https://unsplash.com/photos/blue-bubbles-on-a-white-surface-lkp-b-kfdwc", *UNSPLASH)),
 "hero-repair": ("Wrap brush and swing arm inside a car wash tunnel", 1600, 900, 800, 450, None),
 "hero-installation": ("New shrink-wrapped cloth brushes staged for installation", 1600, 900, 800, 450, None),
 "hero-maintenance": ("Inside a car wash tunnel: brushes, conveyor and overhead plumbing", 1600, 900, 800, 450, None),
 "hero-urgent": ("Wash stopped with the conveyor pit open, tech standing by (no face visible)", 1600, 900, 800, 450, None),
 "card-repair": ("Blue foam wrap brush on its swing arm inside a car wash tunnel", 1200, 649, 600, 324, None),
 "card-installation": ("New green and black cloth brushes still in shrink wrap, ready for installation", 1200, 649, 600, 324, None),
 "card-support": ("Inside a car wash tunnel: red top brush, wrap brushes, conveyor and overhead plumbing", 1200, 649, 600, 324, None),
 "chemistry": ("Car covered in thick white foam with red paint showing through, wheel in the foreground", 1200, 739, 600, 370,
               ("Erik Mclean", "https://www.pexels.com/photo/red-acura-integra-car-covered-in-foam-20856507/", *PEXELS)),
 "job-01": ("Red cloth brush during a tunnel repair", 1200, 771, 600, 386, None),
 "job-02": ("New blue cloth strips laid out before install", 1200, 771, 600, 386, None),
 "job-03": ("Close-up of a blue foam wrap brush hub", 1200, 771, 600, 386, None),
 "job-04": ("Open conveyor pit during a repair, tech standing by (no face visible)", 1200, 771, 600, 386, None),
 "job-05": ("Close-up of a new green and black brush hub", 1200, 771, 600, 385, None),
 "job-06": ("Self-serve bay meter with an out-of-order notice for spot-free rinse", 1200, 771, 600, 386, None),
}
def img(key, sizes, cls="", lazy=True, prio=False):
    alt, w, h, sw, _sh, _c = IMG[key]
    srcset = f"{IMG_DIR}{key}-{w}w.webp {w}w, {IMG_DIR}{key}-{sw}w.webp {sw}w"
    attrs = (' fetchpriority="high"' if prio else "") + (' loading="lazy" decoding="async"' if lazy else "")
    c = f' class="{cls}"' if cls else ""
    return f'<img{c} src="{IMG_DIR}{key}-{sw}w.webp" srcset="{srcset}" sizes="{sizes}" width="{w}" height="{h}" alt="{html.escape(alt)}"{attrs}>'
def hero_bg(key):
    return f'<picture class="hbg">{img(key, "100vw", lazy=False, prio=True)}</picture>'
PAGE_HERO = {"/car-wash-equipment-repair/": "hero-repair", "/car-wash-equipment-installation/": "hero-installation",
             "/car-wash-maintenance-plans/": "hero-maintenance", "/urgent-car-wash-repair/": "hero-urgent", "/chemistry/": "chemistry-page-hero"}

CSS = (ROOT / "_build/site.css").read_text()
CSS = re.sub(r"/\*.*?\*/", "", CSS, flags=re.S); CSS = re.sub(r"\s*\n\s*", "", CSS)

def header(path):
    nav = "".join(f'<a href="{u}"{" aria-current=\"page\"" if u == path else ""}>{t}</a>' for u, t in NAV)
    mnav = "".join(f'<a href="{u}">{t}</a>' for u, t in NAV) + '<a href="/urgent-car-wash-repair/">Urgent repair</a><a href="/contact/">Request service</a>'
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="hdr"><div class="wrap"><a class="logo" href="/"><img src="/assets/cwm/img/cwm-logo-horizontal-white.png" alt="Car Wash Management" width="133" height="44"></a>
<nav class="main" aria-label="Main">{nav}</nav>
<div class="cta"><a class="btn btn-ghost ico" href="sms:{PHONE_T}" data-evt="sms_click" aria-label="Text us at {PHONE_D}">{I_SMS}</a><a class="btn btn-white btn-req" href="/contact/">Request Service</a><a class="btn btn-blue" href="tel:{PHONE_T}" data-evt="tel_click" aria-label="Call {PHONE_D}">{I_PHONE}<span><span class="t">Call </span>{PHONE_D}</span></a>
<details class="mnav"><summary aria-label="Menu">{I_MENU}</summary><nav aria-label="Mobile">{mnav}</nav></details></div></div></header>'''

def footer():
    return f'''<footer class="foot"><div class="wrap fgrid">
<div><a class="logo" href="/"><img src="/assets/cwm/img/cwm-logo-stacked-white.png" alt="Car Wash Management" width="111" height="96"></a><p style="margin-top:14px;max-width:300px">Service and repair for any car wash equipment, plus installation and replacement of equipment and components.</p>
<p style="margin-top:16px"><a href="tel:{PHONE_T}" data-evt="tel_click">{PHONE_D}</a> · <a href="sms:{PHONE_T}" data-evt="sms_click">call or text</a></p><p><a href="mailto:{EMAIL}">{EMAIL}</a></p><p>Hours: {HOURS}</p></div>
<div><h2>Services</h2><p><a href="/car-wash-equipment-repair/">Car wash equipment repair</a></p><p><a href="/car-wash-equipment-installation/">Installation &amp; replacement</a></p><p><a href="/car-wash-maintenance-plans/">Maintenance plans</a></p><p><a href="/urgent-car-wash-repair/">Urgent repair</a></p><p><a href="/chemistry/">Chemistry</a></p></div>
<div><h2>Company</h2><p><a href="/car-wash-equipment-brands/">Brands we service</a></p><p><a href="/equipment/">Equipment types</a></p><p><a href="/service-area/">Service area</a></p><p><a href="/about/">About</a></p><p><a href="/contact/">Request service</a></p></div>
<div><h2>Brands we service</h2>{"".join(f'<p><a href="{BRANDS_URL}#{cid}">{short}</a></p>' for cid, _, short, _ in BRAND_CATS)}<p><a href="{BRANDS_URL}">All brands →</a></p></div>
</div><div class="wrap">{SMS_OPTIN}
<div class="fbot">© 2026 Car Wash Management · carwashmgmt.com · <a href="https://legal.carwashmgmt.com/privacy-policy.html">Privacy Policy</a> · <a href="https://legal.carwashmgmt.com/terms-and-conditions.html">Terms &amp; Conditions</a> · <a href="/credits/">Photo credits</a><p class="tm-foot">{TM}</p></div></div></footer>
<div class="mbar">{call_btn("btn btn-blue", "Call")}{text_btn("btn btn-ghost", "Text")}<a class="btn btn-white" href="/contact/">Request</a></div>'''

REQ_TYPES = ["Repair", "Installation or replacement", "Maintenance plan", "Urgent / wash is down", "Chemistry", "Other"]
def form(fid, loc, heading="Request service or a quote", hlevel="h2", flat=False):
    opts = "".join(f"<option>{t}</option>" for t in REQ_TYPES)
    f = lambda n: f"{fid}-{n}"
    return f'''<form class="form{" flat" if flat else ""}" id="{fid}" data-cwm-request data-form-location="{loc}" action="/contact/" method="post">
<{hlevel}>{heading}</{hlevel}><p class="sub">Tell us what’s going on. We reply the same business day.</p>
<div class="row2"><div class="field"><label for="{f("name")}">Your name <span class="req">*</span></label><input id="{f("name")}" name="name" autocomplete="name" required maxlength="120" data-err="Please enter your name."><span class="err"></span></div>
<div class="field"><label for="{f("biz")}">Business / wash site <span class="req">*</span></label><input id="{f("biz")}" name="business_site" autocomplete="organization" required maxlength="160" data-err="Please enter your business or wash name."><span class="err"></span></div></div>
<div class="row2"><div class="field"><label for="{f("email")}">Email <span class="req">*</span></label><input id="{f("email")}" name="email" type="email" autocomplete="email" required maxlength="160" data-err="Please enter a valid email address."><span class="err"></span></div>
<div class="field"><label for="{f("phone")}">Phone <span class="req">*</span></label><input id="{f("phone")}" name="phone" type="tel" autocomplete="tel" required minlength="7" maxlength="40" pattern="[0-9+()\\-. ]{{7,40}}" data-err="Please enter a phone number we can reach you on."><span class="err"></span></div></div>
<div class="row2"><div class="field"><label for="{f("city")}">City</label><input id="{f("city")}" name="city" autocomplete="address-level2" maxlength="120"><span class="err"></span></div>
<div class="field"><label for="{f("type")}">Request type <span class="req">*</span></label><select id="{f("type")}" name="request_type" required data-err="Please choose a request type."><option value="">Choose one</option>{opts}</select><span class="err"></span></div></div>
<div class="field"><label for="{f("equip")}">Equipment or brand</label><input id="{f("equip")}" name="equipment_brand" maxlength="200" placeholder="e.g. tunnel conveyor, in-bay automatic, pay station"><span class="err"></span></div>
<div class="field"><label for="{f("msg")}">Message</label><textarea id="{f("msg")}" name="message" maxlength="4000" placeholder="What’s happening? A photo can be texted to {PHONE_D}."></textarea><span class="err"></span></div>
<div class="field"><fieldset><legend>Preferred contact</legend><div class="radios"><label><input type="radio" name="preferred_contact" value="Phone call" checked> Phone call</label><label><input type="radio" name="preferred_contact" value="Email"> Email</label></div></fieldset></div>
<div class="check"><label><input type="checkbox" name="consent" required data-err="Please tick the box so we can contact you about this request."> <span>I agree that Car Wash Management may contact me by phone or email about this request. This does not sign me up for text messages.</span></label><span class="err"></span></div>
<button class="btn btn-blue" type="submit">Send request {I_ARR}</button>
<p class="alt">Faster? Call or text <a href="tel:{PHONE_T}" data-evt="tel_click">{PHONE_D}</a></p></form>'''

def ld(*objs):
    return "".join(f'<script type="application/ld+json">{json.dumps(o, ensure_ascii=False, separators=(",", ":"))}</script>' for o in objs)
ORG = {"@context": "https://schema.org", "@graph": [
    {"@type": "Organization", "@id": BASE + "/#org", "name": "Car Wash Management", "url": BASE + "/",
     "logo": BASE + "/assets/cwm/img/cwm-logo-horizontal.png", "telephone": "+1-808-465-2291", "email": EMAIL},
    {"@type": "HomeAndConstructionBusiness", "@id": BASE + "/#business", "name": "Car Wash Management", "url": BASE + "/",
     "image": BASE + "/assets/cwm/img/cwm-logo-horizontal.png", "telephone": "+1-808-465-2291", "email": EMAIL,
     "parentOrganization": {"@id": BASE + "/#org"}, "areaServed": {"@type": "Place", "name": "Southwest United States"},
     "openingHoursSpecification": {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "17:00"}}]}
def crumbs_ld(path, name):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
        {"@type": "ListItem", "position": 2, "name": name, "item": BASE + path}]}

def page(path, title, desc, body, extra_ld=(), noindex=False, canonical=True):
    assert len(title) <= 60, (path, len(title)); assert len(desc) <= 158, (path, len(desc))
    canon = f'<link rel="canonical" href="{BASE}{path}">' if canonical else ""
    robots = '<meta name="robots" content="noindex, follow">' if noindex else ""
    og = (f'<meta property="og:type" content="website"><meta property="og:site_name" content="Car Wash Management">'
          f'<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">'
          + (f'<meta property="og:url" content="{BASE}{path}">' if canonical else "")
          + f'<meta property="og:image" content="{BASE}/assets/cwm/img/cwm-logo-horizontal.png"><meta name="twitter:card" content="summary">')
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}">{canon}{robots}{og}
<meta name="theme-color" content="#0B1B2B"><link rel="icon" href="/assets/cwm/img/favicon.ico" sizes="48x48"><link rel="icon" type="image/png" href="/assets/cwm/img/favicon-32.png" sizes="32x32"><link rel="apple-touch-icon" href="/assets/cwm/img/apple-touch-icon.png">
<link rel="preload" href="/assets/cwm/fonts/archivo-cwm.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="/assets/cwm/fonts/inter-cwm.woff2" as="font" type="font/woff2" crossorigin>
<style>{CSS}</style>{ld(ORG, *extra_ld)}</head><body>
{header(path)}
<main id="main">{body}</main>
{footer()}
<script src="/forms-config.js" defer></script><script src="/events-config.js" defer></script><script src="/assets/js/site-forms.js" defer></script><script src="/assets/cwm/js/cwm.js" defer></script>
</body></html>
'''

def downtime():
    return f'''<section class="downtime" aria-labelledby="dt-h"><div class="wrap"><div class="pulse" aria-hidden="true"></div><div><h2 id="dt-h">Wash down? Call now.</h2><p>Every hour down costs you cars. Call or text and tell us what stopped. Call or text any time. Messages after hours are answered the next business morning. <a href="/urgent-car-wash-repair/">Urgent repair →</a></p></div>
<div class="acts">{call_btn("btn btn-ink", PHONE_D)}{text_btn()}</div></div></section>'''

def brand_chips(cls="bcats"):
    groups = "".join(f'<div class="bcat"><h3><a href="{BRANDS_URL}#{cid}">{short}</a></h3><ul class="chips sm">'
                     + "".join(f'<li><a class="chip" href="{BRANDS_URL}#{a}">{n}</a></li>' for n, a, *_ in bs) + '</ul></div>'
                     for cid, _, short, bs in BRAND_CATS)
    return f'<div class="{cls}">{groups}</div>'
def brands_block(h="h2"):
    return f'''<section class="brands" aria-labelledby="br-h"><div class="wrap"><div class="eyebrow">Brands &amp; equipment</div><{h} id="br-h">We service and repair any make and model.</{h}>
<p class="bintro">Tunnel, in-bay, self-serve, vacuum, pay station and water equipment from the brands below, and others too. Don’t see yours? Call or text {PHONE_D}.</p>
{brand_chips()}<p class="tm">{TM}</p><a class="lnk" href="{BRANDS_URL}">See all the brands we service →</a></div></section>'''

def final_cta():
    return f'''<section class="final" aria-labelledby="fin-h"><div class="wrap grid"><div><div class="eyebrow" style="color:var(--sky)">Get help today</div><h2 id="fin-h" style="margin-top:14px">Let’s get your wash running right.</h2><p>Call or text {PHONE_D}, or send the form. Tell us your equipment and what’s going on.</p>
<div style="display:flex;gap:12px;flex-wrap:wrap">{call_btn("btn btn-amber")}{text_btn()}</div><p class="em">Or email <a href="mailto:{EMAIL}">{EMAIL}</a> · Hours: {HOURS}</p></div>
<div><div class="form"><h3>Prefer the form?</h3><p class="sub">It takes about two minutes. Your details go straight to our team.</p><a class="btn btn-blue" href="#request">Go to the request form {I_ARR}</a><p class="alt">Or use the <a href="/contact/">Request Service page</a></p></div></div></div></section>'''

# ---------------- Home ----------------
def home():
    cards = [
        ("01", "Repair", "/car-wash-equipment-repair/", "Car wash equipment repair",
         "We service and repair any equipment on tunnels, in-bay automatics and self-serve bays, including equipment we didn’t install.",
         ["Conveyors, brushes, pumps and controls", "Equipment we didn’t install", "Any make, any age"]),
        ("02", "Installation", "/car-wash-equipment-installation/", "Car wash equipment installation",
         "Installation and replacement of equipment and components, from single parts to complete systems.",
         ["Replacement parts and components", "Pay stations and controllers", "Water, RO and reclaim components"]),
        ("03", "Support", "/car-wash-maintenance-plans/", "Car wash maintenance plans",
         "Ongoing support for your equipment, with one number to call or text when something isn’t right.",
         ["Scheduled preventive maintenance visits", "Priority scheduling", "A custom quote for each site"]),
    ]
    card_img = {"01": "card-repair", "02": "card-installation", "03": "card-support"}
    cardh = "".join(f'''<article class="card"><div class="media">{img(card_img[n], "(max-width:700px) calc(100vw - 40px), 369px")}</div><div class="bd"><h3><span class="n">{n}</span>{t}</h3><p>{d}</p><ul class="ticks">{"".join(f"<li>{x}</li>" for x in li)}</ul><a class="more" href="{u}">{a} {I_ARR}</a></div></article>''' for n, t, u, a, d, li in cards)
    jobs = "".join(f'<figure>{img(k, "(max-width:700px) calc(50vw - 27px), 360px")}<figcaption>{IMG[k][0].replace(" (no face visible)", "")}</figcaption></figure>' for k in ["job-01", "job-02", "job-03", "job-04", "job-05", "job-06"])
    pair = f'''<div class="pair"><div class="two">{ph("before (real job photo)", True)}{ph("after, same angle", True)}<span class="lbl lb">BEFORE</span><span class="lbl la">AFTER</span></div><p class="cap">{tag("PLACEHOLDER caption: equipment · what was wrong · what we did")}</p></div>'''
    rev = f'''<div class="rev">{tag("PLACEHOLDER REVIEW: real customer review, used with permission (Andrew to supply)")}<div class="q" aria-hidden="true">“</div><div class="ln"></div><div class="ln"></div><div class="ln" style="width:70%"></div><div class="who"><div class="av"></div><div><b>Customer name</b>Wash name · city</div></div></div>'''
    steps = [("Call, text or send the form", "Tell us your equipment and what’s happening. A photo of the problem helps."),
             ("We look at it", "We get eyes on the equipment and tell you plainly what it needs."),
             ("We repair, replace or set up a plan", "The work gets done, and your team knows what changed."),
             ("We’re still there after", "Same number, same team, every time your wash needs us.")]
    stp = "".join(f'<li class="st"><div class="num">{i}</div><h3>{a}</h3><p>{b}</p></li>' for i, (a, b) in enumerate(steps, 1))
    body = f'''<section class="hero home">{hero_bg("home-hero")}<div class="wrap grid"><div>
<h1>Car Wash Equipment Service, Installation &amp; Support for Any Brand Across the Southwest United States</h1>
<p class="hd head">Any equipment.<br>Any problem.<br><em>We’re there for you.</em></p>
<p class="lead">Car Wash Management services and repairs any car wash equipment, installs and replaces equipment and components, and supports your team, so your wash keeps running and your customers keep coming.</p>
<div class="btns">{call_btn()}<a class="btn btn-ghost" href="#request">Request Service {I_ARR}</a></div>
<p class="sms">Serving the Southwest United States. Or text a photo of the problem to <a href="sms:{PHONE_T}" data-evt="sms_click">{PHONE_D}</a> · {HOURS}</p>
<div class="photos">{img("job-04", "330px")}{img("job-03", "230px")}</div>
</div><div id="request">{form("home-request", "home-hero")}</div></div></section>
{downtime()}
<section class="s" aria-labelledby="wd-h"><div class="wrap"><div class="sh"><div><div class="eyebrow">What we do</div><h2 id="wd-h">Service, installation and support. One team for your whole wash.</h2></div><p>Aging equipment, a part that needs replacing, or a bay that just went down: call one number and we take it from there.</p></div><div class="cards">{cardh}</div></div></section>
{brands_block()}
<section class="area" aria-labelledby="ar-h"><div class="wrap"><div class="ahead"><div><div class="eyebrow">Service area</div><h2 id="ar-h">Serving the Southwest United States.</h2></div><p>We service car washes across the Southwest United States. Call or text and we’ll tell you straight whether we can reach your site.</p></div><a class="lnk" href="/service-area/">See our service area →</a></div></section>
<section class="s dark" aria-labelledby="ba-h"><div class="wrap"><div class="sh"><div><div class="eyebrow">Our work</div><h2 id="ba-h">Real jobs. Up close. Before and after.</h2></div><p style="color:var(--on-dark)">Close-ups of real repairs, and before/after pairs shot from the same spot.</p></div>
<h3 class="h3s">From real jobs</h3><div class="jobs">{jobs}</div><h3 class="h3s">Before &amp; after</h3><div class="pairs">{pair * 3}</div></div></section>
<section class="s" aria-labelledby="rv-h"><div class="wrap"><div class="sh"><div><div class="eyebrow">Reviews</div><h2 id="rv-h">What owners say after we leave.</h2></div><p>Real reviews from real wash owners, shared with their permission. {tag("Reviews: placeholder until real reviews exist")}</p></div><div class="rgrid">{rev * 3}</div></div></section>
<section class="chem" aria-labelledby="ch-h" style="background:var(--mist)"><div class="wrap cg"><div class="cimg">{img("chemistry", "(max-width:700px) calc(100vw - 40px), 552px")}</div><div><div class="eyebrow">Chemistry</div><h2 id="ch-h">Chemistry tailored to your wash by a real chemist.</h2><p>CWM Ceramic Wax, made by Car Wash Management.</p><p style="margin-top:10px">We also service chemical injectors and dosing equipment.</p><a class="lnk" href="/chemistry/">Car wash chemicals &amp; programs →</a></div></div></section>
<section class="s steps" aria-labelledby="hw-h"><div class="wrap"><div class="sh"><div><div class="eyebrow">How it works</div><h2 id="hw-h">From “it’s broken” to running, in four steps.</h2></div></div><ol class="sgrid">{stp}</ol></div></section>
{final_cta()}'''
    website = {"@context": "https://schema.org", "@type": "WebSite", "@id": BASE + "/#website", "name": "Car Wash Management", "url": BASE + "/", "publisher": {"@id": BASE + "/#org"}}
    return page("/", "Southwest Car Wash Equipment Service | Car Wash Management",
                "We service and repair any car wash equipment across the Southwest United States, and install from single parts to complete systems. Call or request a quote.",
                body, (website,))

# ---------------- Inner pages ----------------
def inner(path, crumb, title, desc, h1, lead, content, soon, form_heading="Request service or a quote", extra_ld=()):
    soon_html = f'<div class="soon"><b>Coming soon:</b> {soon}</div>' if soon else ""
    hk = PAGE_HERO.get(path)
    body = f'''<section class="phero{" photo" if hk else ""}">{hero_bg(hk) if hk else ""}<div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> › <span aria-current="page">{crumb}</span></nav>
<h1>{h1}</h1><p class="lead">{lead}</p><div class="btns">{call_btn()}{text_btn()}<a class="btn btn-ghost" href="#request">Request Service {I_ARR}</a></div></div></section>
{downtime() if path != "/urgent-car-wash-repair/" else ""}
<section class="body"><div class="wrap cols"><div class="txt">{content}{soon_html}</div><div id="request">{form(path.strip("/").replace("/", "-") + "-request", path, form_heading, "h2", True)}</div></div></section>'''
    return page(path, title, desc, body, (crumbs_ld(path, crumb), *extra_ld))

def facts():
    return f'''<ul class="facts"><li><b>Call or text:</b> <a href="tel:{PHONE_T}" data-evt="tel_click">{PHONE_D}</a> (<a href="sms:{PHONE_T}" data-evt="sms_click">text</a>)</li><li><b>Email:</b> <a href="mailto:{EMAIL}">{EMAIL}</a></li><li><b>Hours:</b> {HOURS}</li></ul>'''
def brand_list():
    return "<ul class='ticks'>" + "".join(f'<li><a href="{BRANDS_URL}#{cid}">{short}</a>: ' + ", ".join(f'<a href="{BRANDS_URL}#{a}">{n}</a>' for n, a, *_ in bs) + "</li>" for cid, _, short, bs in BRAND_CATS) + f"</ul><p class='tm'>{TM}</p>"
def service_ld(path, name, stype):
    return {"@context": "https://schema.org", "@type": "Service", "name": name, "serviceType": stype, "url": BASE + path, "provider": {"@id": BASE + "/#business"}}

PAGES = {}
PAGES["/car-wash-equipment-repair/"] = lambda: inner("/car-wash-equipment-repair/", "Repair",
    "Car Wash Equipment Repair | Car Wash Management",
    "Service and repair for any car wash equipment: tunnels, in-bay automatics and self-serve bays, from conveyors and brushes to pumps and pay stations.",
    "Car Wash Equipment Repair",
    "We service and repair any car wash equipment, on tunnels, in-bay automatics and self-serve bays, including equipment we didn’t install.",
    f'''<h2>What we work on</h2><p>Car Wash Management techs service and repair the equipment that keeps a wash running, whatever the make or age.</p>
<ul class="ticks"><li>Tunnel conveyors, brushes and gear drives</li><li>In-bay automatic wash systems</li><li>High-pressure and water pumps</li><li>Pay stations and wash controllers</li><li>Photo eyes and vehicle-position sensors</li><li>Chemical injectors and dosing equipment</li><li>Reverse osmosis, water and reclaim components</li></ul>
<h2>Brands we service</h2>{brand_list()}<h2>How to reach us</h2>{facts()}''',
    "repair job examples, photos and answers to common repair questions.",
    extra_ld=(service_ld("/car-wash-equipment-repair/", "Car wash equipment repair", "Car wash equipment repair"),))
PAGES["/car-wash-equipment-installation/"] = lambda: inner("/car-wash-equipment-installation/", "Installation",
    "Car Wash Equipment Installation | Car Wash Management",
    "Installation and replacement of car wash equipment and components, from single parts to complete systems. Request an installation quote today.",
    "Car Wash Equipment Installation &amp; Replacement",
    "Installation and replacement of equipment and components, from single parts to complete systems.",
    f'''<h2>What we install and replace</h2><ul class="ticks"><li>Replacement parts and components</li><li>Motors, gear drives and pumps</li><li>Pay stations and wash controllers</li><li>Reverse osmosis, water and reclaim components</li></ul>
<p>Not sure whether to repair or replace? Call or text and tell us what you’re working with.</p><p>Installation and replacement of equipment and components, from single parts to complete systems.</p><h2>How to reach us</h2>{facts()}''',
    "examples and photos from real installation jobs.", "Request an installation quote",
    extra_ld=(service_ld("/car-wash-equipment-installation/", "Car wash equipment installation and replacement", "Car wash equipment installation"),))
PAGES["/car-wash-maintenance-plans/"] = lambda: inner("/car-wash-maintenance-plans/", "Maintenance Plans",
    "Car Wash Preventive Maintenance Plans | Car Wash Management",
    "Scheduled preventive maintenance visits, priority scheduling and a custom quote for each site. Ask Car Wash Management about a plan for your wash.",
    "Car Wash Preventive Maintenance &amp; Support Plans",
    "Scheduled preventive maintenance visits, priority scheduling and a custom quote for each site.",
    f'''<h2>Talk to us about a plan</h2><p>Tell us your wash type and equipment, and we’ll talk through what ongoing maintenance and support could look like for your site.</p><ul class="ticks"><li>Scheduled preventive maintenance visits</li><li>Priority scheduling</li><li>A custom quote for each site</li></ul><h2>How to reach us</h2>{facts()}''',
    None, "Ask about a maintenance plan",
    extra_ld=(service_ld("/car-wash-maintenance-plans/", "Car wash preventive maintenance", "Car wash equipment maintenance"),))
PAGES["/urgent-car-wash-repair/"] = lambda: inner("/urgent-car-wash-repair/", "Wash Down? Urgent Car Wash Repair",
    "Wash Down? Urgent Car Wash Repair | Car Wash Management",
    f"Wash down? Call or text Car Wash Management at {PHONE_D} and tell us what stopped. Messages after hours are answered the next business morning.",
    "Wash Down? Urgent Car Wash Repair",
    f"Call or text {PHONE_D} and tell us what stopped. Call or text any time. Messages after hours are answered the next business morning.",
    f'''<h2>Call or text with what stopped</h2><p>Call or text <a href="tel:{PHONE_T}" data-evt="tel_click">{PHONE_D}</a> and tell us what stopped: the equipment, what it’s doing and when it stopped. A photo of the problem helps.</p>
<p>Call or text any time. Messages after hours are answered the next business morning.</p><h2>How to reach us</h2>{facts()}''',
    None, "Request urgent service",
    extra_ld=(service_ld("/urgent-car-wash-repair/", "Urgent car wash repair", "Car wash equipment repair"),))
PAGES["/equipment/"] = lambda: inner("/equipment/", "Equipment Types",
    "Car Wash Equipment Types We Service | Car Wash Management",
    "Car Wash Management services and repairs tunnel, in-bay automatic and self-serve equipment, plus dryers, vacuums, pay stations, water and dosing systems.",
    "Car Wash Equipment Types We Service",
    "We service and repair any make and model, across every part of the wash.",
    f'''<h2>Equipment types</h2><ul class="ticks"><li>Tunnel</li><li>In-bay automatic</li><li>Self-serve</li><li>Dryers &amp; blowers</li><li>Vacuums</li><li>Pay stations &amp; controllers</li><li>Water, RO &amp; reclaim</li><li>Chemistry &amp; dosing</li></ul><h2>Brands we service</h2><p>See the full list on our <a href="{BRANDS_URL}">brands we service</a> page.</p>{brand_list()}<h2>How to reach us</h2>{facts()}''',
    None)
def brands_page():
    jump = '<ul class="chips sm">' + "".join(f'<li><a class="chip" href="#{cid}">{short}</a></li>' for cid, _, short, _ in BRAND_CATS) + "</ul>"
    secs = "".join(f'<h2 id="{cid}">{name}</h2>' + "".join(f'<h3 id="{a}">{n}</h3><p>{txt}</p>' for n, a, _, txt, *_ in bs) for cid, name, _, bs in BRAND_CATS)
    content = f'''<p>We repair and service car wash equipment from the brands below, grouped by type. We work on other makes too, so if yours isn’t listed, call or text <a href="tel:{PHONE_T}" data-evt="tel_click">{PHONE_D}</a>.</p>
{jump}<p class="tm">{TM}</p>{secs}<p class="tm">{TM}</p><h2>How to reach us</h2>{facts()}'''
    svc = service_ld(BRANDS_URL, "Car wash equipment repair and service for all major brands", "Car wash equipment repair")
    svc["description"] = "Repair, troubleshooting, parts replacement and preventive maintenance for tunnel, in-bay automatic, self-serve, vacuum, pay station and water equipment."
    return inner(BRANDS_URL, "Brands We Service",
        "Car Wash Equipment Brands We Service | Car Wash Management",
        "We repair and service tunnel, in-bay, self-serve, vacuum, pay station and water equipment from Sonny’s, MacNeil, PDQ, Ryko, Washworld and more.",
        "Car Wash Equipment Brands We Service",
        "Repair, troubleshooting, parts replacement and preventive maintenance for the major car wash equipment brands.",
        content, None, extra_ld=(svc,))
PAGES[BRANDS_URL] = brands_page
PAGES["/service-area/"] = lambda: inner("/service-area/", "Service Area",
    "Southwest United States Service Area | Car Wash Management",
    f"Car Wash Management services car washes across the Southwest United States. Call or text {PHONE_D} to check whether we can reach your site.",
    "Car Wash Equipment Service Across the Southwest United States",
    "We service car washes across the Southwest United States. Call or text and we’ll tell you straight whether we can reach your site.",
    f'''<h2>Where we work</h2><p>We service car washes across the Southwest United States. Call or text and we’ll tell you straight whether we can reach your site.</p><h2>How to reach us</h2>{facts()}''',
    None)
PAGES["/chemistry/"] = lambda: inner("/chemistry/", "Chemistry",
    "Car Wash Chemicals & Chemical Programs | Car Wash Management",
    "Chemistry tailored to your wash by a real chemist. CWM Ceramic Wax, made by Car Wash Management. Call, text or request pricing.",
    "Car Wash Chemicals &amp; Chemical Programs",
    "Chemistry tailored to your wash by a real chemist.",
    f'''<div class="cimg inl">{img("chemistry", "(max-width:700px) calc(100vw - 40px), 560px")}</div><h2>Our own product</h2><p>CWM Ceramic Wax, made by Car Wash Management.</p><h2>Dosing equipment</h2><p>We service chemical injectors and dosing equipment as part of our repair work.</p><p>Ask us about the chemistry for your wash.</p><h2>How to reach us</h2>{facts()}''',
    None, "Ask about chemistry")
PAGES["/about/"] = lambda: inner("/about/", "About",
    "About Car Wash Management | Car Wash Equipment Service",
    "Car Wash Management services and repairs car wash equipment and installs and replaces components. Learn who we are and how to reach our team.",
    "About Car Wash Management",
    "Car Wash Management services and repairs any car wash equipment, installs and replaces equipment and components, and supports owners and their teams.",
    f'''<h2>What we do</h2><ul class="ticks"><li><a href="/car-wash-equipment-repair/">Car wash equipment repair</a></li><li><a href="/car-wash-equipment-installation/">Installation and replacement</a></li><li><a href="/car-wash-maintenance-plans/">Maintenance and support</a></li><li><a href="/chemistry/">Chemistry</a></li></ul><p>{tag("Company story, team and photos: Andrew to supply")}</p><h2>How to reach us</h2>{facts()}''',
    "our story, our team and photos from real jobs.",
    extra_ld=({"@context": "https://schema.org", "@type": "AboutPage", "url": BASE + "/about/", "name": "About Car Wash Management", "about": {"@id": BASE + "/#org"}},))
def contact():
    body = f'''<section class="phero"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> › <span aria-current="page">Request Service</span></nav>
<h1>Request Service or a Quote</h1><p class="lead">Call or text {PHONE_D}, or send the form. Tell us your wash type, equipment and what’s going on. We reply the same business day.</p></div></section>
<section class="body"><div class="wrap cols"><div id="request">{form("contact-request", "/contact/", "Service or quote request", "h2", True)}</div>
<div class="txt"><h2>Other ways to reach us</h2>{facts()}<div style="display:flex;gap:12px;flex-wrap:wrap;margin:6px 0 24px">{call_btn()}{text_btn("btn btn-white")}</div>
<h2>What to include</h2><ul class="ticks"><li>Your wash type (tunnel, in-bay automatic or self-serve)</li><li>The equipment and brand, if you know it</li><li>What it’s doing, and since when</li><li>A photo, texted to {PHONE_D}</li></ul>
<div class="soon"><b>Wash down right now?</b> Call or text <a href="tel:{PHONE_T}" data-evt="tel_click">{PHONE_D}</a> instead of using the form. Form requests: We reply the same business day.</div></div></div></section>'''
    cp = {"@context": "https://schema.org", "@type": "ContactPage", "url": BASE + "/contact/", "name": "Request Service or a Quote", "about": {"@id": BASE + "/#business"}}
    return page("/contact/", "Request Car Wash Service or a Quote | Car Wash Management",
                f"Call or send a service or quote request to Car Wash Management. Tell us your wash type, equipment and issue. Hours {HOURS}.",
                body, (crumbs_ld("/contact/", "Request Service"), cp))
def credits():
    stock = "".join(f'<li><b>{html.escape(IMG[k][0])}</b><br>Photo by {c[0]}, <a href="{c[1]}" rel="nofollow noopener">source</a>, used under the <a href="{c[3]}" rel="nofollow noopener">{c[2]}</a>.</li>'
                    for k in IMG if (c := IMG[k][5]))
    body = f'''<section class="phero"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> › <span aria-current="page">Photo Credits</span></nav>
<h1>Photo Credits</h1><p class="lead">Where the photos on this site come from.</p></div></section>
<section class="body"><div class="wrap"><div class="txt" style="max-width:820px"><h2>Our own photos</h2><p>Photos in the “From real jobs” strip, the service cards, the small photos in the homepage header and the headers of the repair, installation, maintenance plans and urgent repair pages were taken by Car Wash Management.</p>
<h2>Stock photos</h2><p>These are general car wash scenes from free stock libraries. They are not Car Wash Management jobs or sites.</p><ul class="ticks">{stock}</ul></div></div></section>'''
    return page("/credits/", "Photo Credits | Car Wash Management", "Credits and licenses for the stock photos used on carwashmgmt.com.", body, noindex=True)
def thank_you():
    body = f'''<section class="ty"><div class="wrap"><div class="eyebrow">Request sent</div><h1 style="margin-top:12px">Thanks. We got your request.</h1>
<p>Your details went to the Car Wash Management team. We reply the same business day.</p><p>If your wash is down right now, call or text {PHONE_D}. Hours: {HOURS}.</p>
<div class="btns">{call_btn()}{text_btn("btn btn-white")}<a class="btn btn-white" href="/">Back to the homepage</a></div></div></section>'''
    return page("/thank-you/", "Thank You | Car Wash Management", "Thanks for your request. We reply the same business day.", body, noindex=True)
def notfound():
    body = f'''<section class="ty"><div class="wrap"><div class="eyebrow">Error 404</div><h1 style="margin-top:12px">Page not found</h1>
<p>That page doesn’t exist or has moved. Try one of these, or call or text {PHONE_D}.</p>
<ul class="ticks" style="max-width:520px;margin-top:18px">{"".join(f'<li><a href="{u}">{t}</a></li>' for u, t in NAV)}<li><a href="/contact/">Request service</a></li></ul>
<div class="btns">{call_btn()}<a class="btn btn-white" href="/">Go to the homepage</a></div></div></section>'''
    return page("/404", "Page Not Found | Car Wash Management", "The page you were looking for could not be found.", body, noindex=True, canonical=False)

def write(path, content):
    out = ROOT / ("index.html" if path == "/" else path.strip("/") + "/index.html")
    out.parent.mkdir(parents=True, exist_ok=True); out.write_text(content)

def main():
    built = {"/": home(), "/contact/": contact(), "/thank-you/": thank_you(), "/credits/": credits()}
    for p, fn in PAGES.items(): built[p] = fn()
    for p, c in built.items(): write(p, c)
    (ROOT / "404.html").write_text(notfound())
    indexable = [p for p in built if p not in ("/thank-you/", "/credits/")]
    order = ["/", "/car-wash-equipment-repair/", "/car-wash-equipment-installation/", "/car-wash-maintenance-plans/", "/urgent-car-wash-repair/",
             "/car-wash-equipment-brands/", "/equipment/", "/service-area/", "/chemistry/", "/about/", "/contact/"]
    assert sorted(order) == sorted(indexable)
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f"  <url><loc>{BASE}{p}</loc><lastmod>{LASTMOD}</lastmod></url>\n" for p in order) + "</urlset>\n"
    (ROOT / "sitemap.xml").write_text(sm)
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
    R = [("/index.html", "/", 301), ("/emergency-car-wash-repair/", "/urgent-car-wash-repair/", 301), ("/emergency-car-wash-repair", "/urgent-car-wash-repair/", 301),
         ("/services.html", "/car-wash-equipment-repair/", 301), ("/services", "/car-wash-equipment-repair/", 301),
         ("/equipment.html", "/equipment/", 301),
         ("/preventive-maintenance.html", "/car-wash-maintenance-plans/", 301), ("/preventive-maintenance", "/car-wash-maintenance-plans/", 301),
         ("/chemistry.html", "/chemistry/", 301), ("/about.html", "/about/", 301),
         ("/contact.html", "/contact/", 301), ("/book-a-call.html", "/contact/", 301), ("/book-a-call", "/contact/", 301),
         # No new equivalent yet: temporary (302) so they can be repointed when /blog/, /projects/, consulting or the calculator exist.
         ("/solutions.html", "/", 302), ("/solutions", "/", 302), ("/results.html", "/about/", 302), ("/results", "/about/", 302),
         ("/blog.html", "/", 302), ("/blog", "/", 302), ("/calculator.html", "/car-wash-equipment-installation/", 302), ("/calculator", "/car-wash-equipment-installation/", 302),
         ("/blog/*", "/", 302), ("/Testimonials", "/about/", 302), ("/BlogPost", "/", 302), ("/ChemicalProduct", "/chemistry/", 302), ("/Contact", "/contact/", 301)]
    (ROOT / "_redirects").write_text("# Generated by _build/build.py. Old .html URLs -> new trailing-slash pages.\n" +
                                     "".join(f"{a} {b} {c}\n" for a, b, c in R))
    (ROOT / "_headers").write_text("""# Generated by _build/build.py
/thank-you/*
  X-Robots-Tag: noindex
/privacy-policy*
  X-Robots-Tag: noindex
/terms-and-conditions*
  X-Robots-Tag: noindex
/_build/*
  X-Robots-Tag: noindex
/assets/cwm/*
  Cache-Control: public, max-age=86400
""")
    print("built", len(built) + 1, "pages")

if __name__ == "__main__":
    main()
