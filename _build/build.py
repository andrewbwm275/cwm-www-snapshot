#!/usr/bin/env python3
"""Car Wash Management redesign (Design direction A): static HTML generator.
Run from the repo root:  python3 _build/build.py
Writes index.html, <page>/index.html, 404.html, sitemap.xml, robots.txt, _redirects, _headers.
Plain Python 3, no dependencies. Shared header/footer live here; page copy lives in PAGES below.
Rules: confirmed facts only. No invented stats, testimonials, reviews, or logos."""
import html, json, pathlib, re, datetime, sys, tempfile
sys.dont_write_bytecode = True
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from brands import CATS as BRAND_CATS, SHORT as BRAND_SHORT
from categories import CATEGORIES
import new_pages
import csv, shutil, struct
ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://www.carwashmgmt.com"
LASTMOD = "2026-11-11"
PHONE_D, PHONE_T = "(619) 704-7719", "+16197047719"
EMAIL = "info@carwashmgmt.com"
HOURS = "Mon–Fri 8 AM–5 PM PT"
AREA = "the Southwest United States and Hawaii"
AREA_LINE = f"We service car washes across {AREA}. Call or text and we’ll tell you straight whether we can reach your site."
BRANDS_URL = "/car-wash-equipment-brands/"
TM = ("Brand names are trademarks of their respective owners. Car Wash Management is an independent service company "
      "and is not affiliated with or endorsed by these manufacturers.")
# Keyword opt-in footer was removed 2026-10-20. Do not add a keyword opt-in line.
SMS_OPTIN = ""
# A2P 10DLC web opt-in: optional, never pre-checked, never required. Exact wording; cwm.js sends it as sms_consent / sms_consent_text.
SMS_CONSENT = ("I agree to receive text messages from Car Wash Management, LLC about my service requests, appointments and account. "
               "Message frequency varies. Msg & data rates may apply. Reply STOP to opt out, HELP for help. Consent is not a condition of purchase.")
PRIVACY_URL, TERMS_URL = "/privacy-policy.html", "/terms-and-conditions.html"
NAV = [("/", "Home"), ("/equipment/", "Equipment"), (BRANDS_URL, "Brands"),
       ("/chemistry/", "Chemistry"), ("/service-area/", "Service Area"),
       ("/about/", "About"), ("/blog/", "Blog"), ("/contact/", "Contact Us")]
SERVICES = [("/car-wash-equipment-repair/", "Repair"), ("/car-wash-equipment-installation/", "Installation"),
            ("/car-wash-maintenance-plans/", "Maintenance Plans"), ("/urgent-car-wash-repair/", "Urgent Repair"),
            ("/car-wash-management-services/", "Management Services")]
I_PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>'
I_SMS = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>'
I_ARR = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 5l7 7-7 7"/></svg>'
I_MENU = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'
CHEV = '<svg class="chev" viewBox="0 0 10 10" width="10" height="10" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><path d="M1.5 3.5 5 7l3.5-3.5"/></svg>'

def call_btn(cls="btn btn-blue", label=f"Call {PHONE_D}"):
    return f'<a class="{cls}" href="tel:{PHONE_T}" data-evt="tel_click">{I_PHONE} {label}</a>'
def text_btn(cls="btn btn-ghost", label="Text us"):
    return f'<a class="{cls}" href="sms:{PHONE_T}" data-evt="sms_click">{I_SMS} {label}</a>'
# Photos. Design delivery /workspace/brand/cwm-redesign/images/: manifest.csv PICK rows only (never _retired/, _pending-clearance/,
# manifest-v1.csv, DROPPED/RETIRED/ALT rows), categories/manifest.csv for the 7 category pages, plus Andrew's approved new-build picks
# (/workspace/website-photos/newbuild/web/, cleaned + EXIF-free). IMG key: (alt, large w, large h, small w, small h, credit, {w: source file}).
# credit None = our own photo. Otherwise (name, source page, license name, license url, kind)
# where kind is "stock" or "manufacturer". Credit goes in the alt text and on /credits/, never on the picture.
IMG_DIR = "/assets/cwm/img/photos/"
DESIGN = pathlib.Path("/workspace/brand/cwm-redesign/images")
NEWBUILD = pathlib.Path("/workspace/website-photos/newbuild/web")
IMG = {}
def _bad(fn, pick=""):
    return any(x in fn for x in ("_retired", "pending-clearance", "manifest-v1")) or re.search(r"DROP|RETIRE|ALT", pick or "", re.I)
def _credit(r):
    kind = (r.get("kind") or "").strip().lower()
    if kind == "own": return None
    src = (r.get("source") or "").strip(); page_url = src.split(" (")[0]
    if kind == "manufacturer": return ((r.get("photographer") or "AVW").strip(), page_url, "Manufacturer image", page_url, "manufacturer", src)
    lic = r.get("license") or ""; lm = re.match(r"\s*(.*?)\s*[—-]+\s*(https?://\S+)", lic)
    return ((r.get("photographer") or "").strip(), page_url, lm.group(1) if lm else lic, lm.group(2) if lm else page_url, "stock", src)
def webp_size(fp):
    b = fp.read_bytes()[:40]
    if b[12:16] == b"VP8X": return 1 + int.from_bytes(b[24:27], "little"), 1 + int.from_bytes(b[27:30], "little")
    if b[12:16] == b"VP8L":
        v = int.from_bytes(b[21:25], "little"); return (v & 0x3FFF) + 1, ((v >> 14) & 0x3FFF) + 1
    return struct.unpack("<H", b[26:28])[0] & 0x3FFF, struct.unpack("<H", b[28:30])[0] & 0x3FFF
def _register(rows, base_dir, key_for, alt_fix=None):
    groups = {}
    for r in rows: groups.setdefault(re.sub(r"-\d+w\.webp$", "", r["filename"]), []).append(r)
    keys = []
    for base, rs in groups.items():
        files = sorted(((webp_size(base_dir / r["filename"]), r) for r in rs), key=lambda t: t[0][0])
        (sw, sh), _ = files[0]; (w, h), r0 = files[-1]
        key = key_for(base, r0); alt = (r0.get("alt text") or "").strip()
        if alt_fix: alt = alt_fix(alt)
        IMG[key] = (alt, w, h, sw, sh, _credit(r0), {fw: base_dir / r["filename"] for (fw, _), r in files}, r0)
        keys.append(key)
    return keys
_ALT_FIX = lambda a: a.replace("red emergency-stop button", "red stop button")
def _design_sources_ready():
    return (DESIGN / "manifest.csv").is_file() and (DESIGN / "categories" / "manifest.csv").is_file() and NEWBUILD.is_dir()
def _load_shipped_photos():
    """Photos already shipped in assets/cwm/img/photos/, with alts and credits from the last build.
    Used when the Design and new-build source folders are not on this machine. Never reads _pending-clearance."""
    reg = json.loads((pathlib.Path(__file__).resolve().parent / "photo_registry.json").read_text())
    photo_dir = ROOT / "assets/cwm/img/photos"
    for rec in reg["images"]:
        files = {int(w): photo_dir / fn for w, fn in rec["files"].items()}
        missing = [str(p) for p in files.values() if not p.is_file()]
        if missing:
            raise SystemExit("missing shipped photo: " + ", ".join(missing))
        credit = tuple(rec["credit"]) if rec["credit"] else None
        IMG[rec["key"]] = (rec["alt"], rec["w"], rec["h"], rec["sw"], rec["sh"], credit, files,
                           {"filename": rec["key"], "kind": rec["kind"], "slot": "hero" if rec["key"].endswith("hero") else ""})
    return reg
PHOTO_REG = None
if _design_sources_ready():
    _main_rows = [r for r in csv.DictReader((DESIGN / "manifest.csv").open(encoding="utf-8"))
                  if (r.get("pick") or "").strip().upper() == "PICK" and not _bad(r["filename"]) and (DESIGN / r["filename"]).is_file()
                  and not r["filename"].startswith("hero-tile")]          # the 2 hero tiles are dropped
    _register(_main_rows, DESIGN, lambda base, r0: ("avw-" if r0["kind"].strip() == "manufacturer" else "") + pathlib.Path(base).name, _ALT_FIX)
    # Andrew's approved new-build picks (Our job). Alt text is descriptive; no customer or site names.
    NB_ALT = {
     "04": "New touch-free tunnel arch with lit signage over a clean conveyor, daylight at the exit",
     "01": "Finished tunnel with yellow wrap arches and brushes over a clean conveyor",
     "06": "Tunnel with new green brushes on stainless frames and a clean conveyor",
     "12": "Row of tunnel arches over the conveyor in a long white tunnel",
     "32": "Blue and red cloth curtain hanging over a tunnel conveyor",
     "15": "Touch-free in-bay automatic gantry in a clean wash bay",
     "16": "In-bay automatic with blowers and a wash-step sign, car inside (plate blurred)",
     "18": "Soft-touch in-bay wash with brushes and yellow tire guides",
     "28": "New chemical dosing panel with filters, valves and tubing on a tidy wall",
     "29": "Tidy equipment room with a controller, tubing and a tank",
     "30": "Two new reclaim holding tanks in a clean equipment room",
     "26": "Water treatment install: softener and RO panel with a new tank and pump",
     "25": "New stainless water treatment skid with tank and pump",
    }
    for n, alt in NB_ALT.items():
        big, small = (1600, 800) if n == "04" else (1200, 600)
        (w, h), (sw, sh) = webp_size(NEWBUILD / f"nb-{n}-{big}w.webp"), webp_size(NEWBUILD / f"nb-{n}-{small}w.webp")
        IMG[f"nb-{n}"] = (alt, w, h, sw, sh, None, {big: NEWBUILD / f"nb-{n}-{big}w.webp", small: NEWBUILD / f"nb-{n}-{small}w.webp"}, {"filename": f"nb-{n}", "kind": "own"})
else:
    PHOTO_REG = _load_shipped_photos()
# Owner pack 2026-11-10. Alt text is the manifest line. Credit is own-job (no third party).
OWNER_ALTS = {
 "job-tunnel-01": "Conveyor and rollers leading out of a car wash tunnel under a blue overhead arch",
 "job-tunnel-02": "Blue wrap brushes on stainless frames over a car wash tunnel conveyor",
 "job-tunnel-03": "Blue tunnel brushes spraying water over a conveyor, looking toward the exit",
 "job-tunnel-04": "Red wash brushes hanging over a tunnel conveyor in a white bay",
 "job-tunnel-05": "Stainless tunnel frames and conveyor in an open-air wash bay",
 "job-tunnel-06": "Red cloth wash curtain hanging from a stainless frame over a tunnel conveyor",
 "job-tunnel-07": "Red overhead brush and conveyor inside a car wash tunnel",
 "job-tunnel-08": "Yellow and black side brush beside a wet tunnel conveyor",
 "job-equip-01": "Chemical pump stand with valves, gauges and supply jugs on a diamond-plate panel",
}
def _register_owner_jobs():
    photo_dir = ROOT / "assets/cwm/img/photos"
    for key, alt in OWNER_ALTS.items():
        files, dims = {}, {}
        for width in (1200, 600):
            fp = photo_dir / f"{key}-{width}w.webp"
            if not fp.is_file():
                raise SystemExit(f"missing owner photo {fp}")
            files[width] = fp
            dims[width] = webp_size(fp)
        (w, h), (sw, sh) = dims[1200], dims[600]
        IMG[key] = (alt, w, h, sw, sh, None, files, {"filename": key, "kind": "own", "slot": ""})
_register_owner_jobs()
USED_IMG = {}            # key -> set of page paths
CUR_PAGE = ["/"]
def kind(key):
    c = IMG[key][5]; return "own" if c is None else c[4]
def credit_alt(key):
    """Credit stays in the alt text. Nothing is drawn on the picture."""
    alt = IMG[key][0]
    knd = kind(key)
    if knd == "manufacturer":
        who = IMG[key][5][0] if IMG[key][5] else "AVW"
        suffix = f" (manufacturer image: {who})"
    elif knd == "stock":
        suffix = " (stock photo)"
    else:
        suffix = " (our job)"
    if suffix.lower() in alt.lower():
        return alt
    return alt + suffix
def own_gallery(keys, sizes="(max-width:700px) calc(50vw - 27px), 260px"):
    figs = "".join(f'<figure>{img(k, sizes)}</figure>' for k in keys)
    return f'<div class="gal">{figs}</div>'
def img(key, sizes, cls="", lazy=True, prio=False):
    _alt, w, h, sw, _sh, _c, _f, _r = IMG[key]
    USED_IMG.setdefault(key, set()).add(CUR_PAGE[0])
    srcset = f"{IMG_DIR}{key}-{w}w.webp {w}w, {IMG_DIR}{key}-{sw}w.webp {sw}w"
    attrs = (' fetchpriority="high"' if prio else "") + (' loading="lazy" decoding="async"' if lazy else "")
    c = f' class="{cls}"' if cls else ""
    return f'<img{c} src="{IMG_DIR}{key}-{sw}w.webp" srcset="{srcset}" sizes="{sizes}" width="{w}" height="{h}" alt="{html.escape(credit_alt(key))}"{attrs}>'
def hero_bg(key):
    return f'<picture class="hbg">{img(key, "100vw", lazy=False, prio=True)}</picture>'
HOME_HERO = "avw-home-hero"  # Design AVW arch (v2b). Andrew's #4 "nb-04" passed AA but read weak at 1440/390 (arch hidden behind headline/form); it leads the jobs strip instead
PAGE_HERO = {"/car-wash-equipment-repair/": "avw-hero-repair", "/car-wash-equipment-installation/": "hero-installation",
             "/car-wash-maintenance-plans/": "hero-maintenance", "/urgent-car-wash-repair/": "hero-urgent", "/chemistry/": "chemistry-page-hero"}

CSS = (ROOT / "_build/site.css").read_text()
CSS = re.sub(r"/\*.*?\*/", "", CSS, flags=re.S); CSS = re.sub(r"\s*\n\s*", "", CSS)

def _cur(path, href):
    return ' aria-current="page"' if path == href else ""
def _mi(path, href, label, sub=False):
    cls = ' class="sub"' if sub else ""
    return f'<a href="{href}"{cls}{_cur(path, href)}>{label}</a>'
def header(path):
    svc = "".join(f'<a href="{u}"{_cur(path, u)}>{t}</a>' for u, t in SERVICES)
    cats = "".join(f'<a href="{c["path"]}"{_cur(path, c["path"])}>{c["short"]}</a>' for c in CATEGORIES)
    equip_cur = _cur(path, "/equipment/")
    panel = (
        _mi(path, "/", "Home")
        + '<p class="grp">Services</p>'
        + "".join(_mi(path, u, t, True) for u, t in SERVICES)
        + _mi(path, "/equipment/", "Equipment")
        + "".join(_mi(path, c["path"], c["short"], True) for c in CATEGORIES)
        + _mi(path, BRANDS_URL, "Brands")
        + _mi(path, "/chemistry/", "Chemistry")
        + _mi(path, "/service-area/", "Service Area")
        + _mi(path, "/about/", "About")
        + _mi(path, "/blog/", "Blog")
        + _mi(path, "/contact/", "Contact Us")
        + _mi(path, "/contact/", "Request Service")
        + f'<a href="tel:{PHONE_T}" data-evt="tel_click">Call {PHONE_D}</a>'
    )
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="hdr"><div class="wrap"><a class="logo" href="/"><img src="/assets/cwm/img/cwm-logo-horizontal-white.png" alt="Car Wash Management" width="133" height="44"></a>
<nav class="main" aria-label="Main"><a href="/"{_cur(path, "/")}>Home</a>
<div class="drop"><button type="button" class="drop-toggle" aria-expanded="false" aria-controls="menu-services">Services{CHEV}</button>
<div class="drop-panel" id="menu-services">{svc}</div></div>
<div class="drop"><a href="/equipment/"{equip_cur}>Equipment</a><button type="button" class="drop-toggle caret" aria-expanded="false" aria-controls="menu-equipment" aria-label="Equipment sections">{CHEV}</button>
<div class="drop-panel" id="menu-equipment"><a href="/equipment/"{equip_cur}>All equipment</a>{cats}</div></div>
<a href="{BRANDS_URL}"{_cur(path, BRANDS_URL)}>Brands</a>
<a href="/chemistry/"{_cur(path, "/chemistry/")}>Chemistry</a>
<a href="/service-area/"{_cur(path, "/service-area/")}>Service Area</a>
<a href="/about/"{_cur(path, "/about/")}>About</a>
<a href="/blog/"{_cur(path, "/blog/")}>Blog</a>
<a href="/contact/"{_cur(path, "/contact/")}>Contact Us</a></nav>
<div class="cta"><a class="btn btn-ghost ico" href="sms:{PHONE_T}" data-evt="sms_click" aria-label="Text us at {PHONE_D}">{I_SMS}</a><a class="btn btn-white btn-req" href="/contact/">Request Service</a><a class="btn btn-blue" href="tel:{PHONE_T}" data-evt="tel_click" aria-label="Call {PHONE_D}">{I_PHONE}<span><span class="t">Call </span>{PHONE_D}</span></a>
<button type="button" class="nav-toggle" aria-expanded="false" aria-controls="site-menu">{I_MENU}<span>Menu</span></button></div></div></header>
<nav id="site-menu" class="nav-panel" aria-label="Menu">{panel}</nav>'''

def footer():
    return f'''<footer class="foot"><div class="wrap fgrid">
<div><a class="logo" href="/"><img src="/assets/cwm/img/cwm-logo-stacked-white.png" alt="Car Wash Management" width="111" height="96"></a><p style="margin-top:14px;max-width:300px">Service and repair for any car wash equipment, plus installation and replacement of equipment and components.</p>
<p style="margin-top:16px"><a href="tel:{PHONE_T}" data-evt="tel_click">{PHONE_D}</a> · <a href="sms:{PHONE_T}" data-evt="sms_click">call or text</a></p><p><a href="mailto:{EMAIL}">{EMAIL}</a></p><p>Hours: {HOURS}</p><p>Serving the Southwest United States and Hawaii.</p></div>
<div><h2>Services</h2><p><a href="/car-wash-equipment-repair/">Car wash equipment repair</a></p><p><a href="/car-wash-equipment-installation/">Installation &amp; replacement</a></p><p><a href="/car-wash-maintenance-plans/">Maintenance plans</a></p><p><a href="/car-wash-management-services/">Full site management</a></p><p><a href="/urgent-car-wash-repair/">Urgent repair</a></p><p><a href="/chemistry/">Chemistry</a></p></div>
<div><h2>Company</h2><p><a href="/car-wash-equipment-brands/">Brands we service and support</a></p><p><a href="/equipment/">Equipment we service</a></p><p><a href="/service-area/">Service area</a></p><p><a href="/blog/">Blog</a></p><p><a href="/about/">About</a></p><p><a href="/contact/">Request service</a></p></div>
<div><h2>Equipment we service</h2>{"".join(f'<p><a href="/equipment/{c["slug"]}/">{c["short"]}</a></p>' for c in CATEGORIES)}<p><a href="{BRANDS_URL}">Brands we service and support →</a></p></div>
</div><div class="wrap">{SMS_OPTIN}
<div class="fbot">© 2026 Car Wash Management · carwashmgmt.com · <a href="{PRIVACY_URL}">Privacy Policy</a> · <a href="{TERMS_URL}">Terms &amp; Conditions</a> · <a href="/credits/">Photo credits</a><p class="tm-foot">{TM}</p></div></div></footer>
<div class="mbar">{call_btn("btn btn-blue", "Call")}{text_btn("btn btn-ghost", "Text")}<a class="btn btn-white" href="/contact/">Request</a></div>'''

REQ_TYPES = ["Repair", "Installation or replacement", "Maintenance plan", "Urgent / wash is down", "Chemistry", "Other"]
def form(fid, loc, heading="Request service or a quote", hlevel="h2", flat=False):
    opts = "".join(f"<option>{t}</option>" for t in REQ_TYPES)
    f = lambda n: f"{fid}-{n}"
    return f'''<form class="form{" flat" if flat else ""}" id="{fid}" data-cwm-request data-form-location="{loc}" action="/contact/" method="post">
<{hlevel}>{heading}</{hlevel}><p class="sub">Tell us what’s going on.</p>
<div class="row2"><div class="field"><label for="{f("name")}">Your name <span class="req">*</span></label><input id="{f("name")}" name="name" autocomplete="name" required maxlength="120" data-err="Please enter your name."><span class="err"></span></div>
<div class="field"><label for="{f("biz")}">Business / wash site <span class="req">*</span></label><input id="{f("biz")}" name="business_site" autocomplete="organization" required maxlength="160" data-err="Please enter your business or wash name."><span class="err"></span></div></div>
<div class="row2"><div class="field"><label for="{f("email")}">Email <span class="req">*</span></label><input id="{f("email")}" name="email" type="email" autocomplete="email" required maxlength="160" data-err="Please enter a valid email address."><span class="err"></span></div>
<div class="field"><label for="{f("phone")}">Phone</label><input id="{f("phone")}" name="phone" type="tel" autocomplete="tel" minlength="7" maxlength="40" pattern="[0-9+()\\-. ]{{7,40}}" aria-describedby="{f("phone-err")}" data-err="Please enter a valid phone number." data-sms-err="Please add a mobile number so we can text you."><span class="err" id="{f("phone-err")}" aria-live="polite"></span></div></div>
<div class="row2"><div class="field"><label for="{f("city")}">City</label><input id="{f("city")}" name="city" autocomplete="address-level2" maxlength="120"><span class="err"></span></div>
<div class="field"><label for="{f("type")}">Request type <span class="req">*</span></label><select id="{f("type")}" name="request_type" required data-err="Please choose a request type."><option value="">Choose one</option>{opts}</select><span class="err"></span></div></div>
<div class="field"><label for="{f("equip")}">Equipment or brand</label><input id="{f("equip")}" name="equipment_brand" maxlength="200" placeholder="e.g. tunnel conveyor, in-bay automatic, pay station"><span class="err"></span></div>
<div class="field"><label for="{f("msg")}">Message</label><textarea id="{f("msg")}" name="message" maxlength="4000" placeholder="What’s happening? A photo can be texted to {PHONE_D}."></textarea><span class="err"></span></div>
<div class="field"><fieldset><legend>Preferred contact</legend><div class="radios"><label><input type="radio" name="preferred_contact" value="Phone call" checked> Phone call</label><label><input type="radio" name="preferred_contact" value="Email"> Email</label></div></fieldset></div>
<div class="check"><label><input type="checkbox" name="consent" required data-err="Please tick the box so we can contact you about this request."> <span>I agree that Car Wash Management may contact me by phone or email about this request. This does not sign me up for text messages.</span></label><span class="err"></span></div>
<div class="check sms"><label><input type="checkbox" name="sms_consent" value="Yes"> <span>{html.escape(SMS_CONSENT)} See our <a href="{TERMS_URL}#sms">SMS Terms</a> and <a href="{PRIVACY_URL}">Privacy Policy</a>.</span></label></div>
<button class="btn btn-blue" type="submit">Send request {I_ARR}</button>
<p class="alt">Faster? Call or text <a href="tel:{PHONE_T}" data-evt="tel_click">{PHONE_D}</a></p></form>'''

def ld(*objs):
    return "".join(f'<script type="application/ld+json">{json.dumps(o, ensure_ascii=False, separators=(",", ":"))}</script>' for o in objs)
ORG = {"@context": "https://schema.org", "@graph": [
    {"@type": "Organization", "@id": BASE + "/#org", "name": "Car Wash Management", "url": BASE + "/",
     "logo": BASE + "/assets/cwm/img/cwm-logo-horizontal.png", "telephone": "+1-619-704-7719", "email": EMAIL},
    {"@type": "HomeAndConstructionBusiness", "@id": BASE + "/#business", "name": "Car Wash Management", "url": BASE + "/",
     "image": BASE + "/assets/cwm/img/cwm-logo-horizontal.png", "telephone": "+1-619-704-7719", "email": EMAIL,
     "parentOrganization": {"@id": BASE + "/#org"}, "areaServed": [{"@type": "Place", "name": "Southwest United States"}, {"@type": "Place", "name": "Hawaii"}],
     "openingHoursSpecification": {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "17:00"}}]}
def crumbs_ld(path, name, parent=None):
    trail = [("/", "Home")] + ([parent] if parent else []) + [(path, name)]
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i, "name": html.unescape(n), "item": BASE + u} for i, (u, n) in enumerate(trail, 1)]}

NAV_JS = """
(function(){
  var btn = document.querySelector(".nav-toggle");
  var panel = document.getElementById("site-menu");
  function setMenu(open){
    if (!btn || !panel) return;
    btn.setAttribute("aria-expanded", open ? "true" : "false");
    panel.classList.toggle("is-open", open);
  }
  if (btn && panel){
    btn.addEventListener("click", function(){ setMenu(btn.getAttribute("aria-expanded") !== "true"); });
    panel.addEventListener("click", function(e){ if (e.target.closest("a")) setMenu(false); });
  }
  document.addEventListener("keydown", function(e){
    if (e.key !== "Escape") return;
    setMenu(false);
    document.querySelectorAll(".drop.open").forEach(function(drop){
      drop.classList.remove("open");
      var t = drop.querySelector(".drop-toggle");
      if (t) t.setAttribute("aria-expanded", "false");
    });
  });
  document.querySelectorAll(".drop").forEach(function(drop){
    var t = drop.querySelector(".drop-toggle");
    if (!t) return;
    t.addEventListener("mousedown", function(){ t.dataset.wasOpen = drop.classList.contains("open") ? "1" : "0"; });
    t.addEventListener("click", function(){
      var open = t.dataset.wasOpen !== "1";
      drop.classList.toggle("open", open);
      t.setAttribute("aria-expanded", open ? "true" : "false");
    });
    drop.addEventListener("focusin", function(){ t.setAttribute("aria-expanded", "true"); });
    drop.addEventListener("focusout", function(e){
      if (!drop.contains(e.relatedTarget) && !drop.classList.contains("open")) t.setAttribute("aria-expanded", "false");
    });
  });
})();
"""
def page(path, title, desc, body, extra_ld=(), noindex=False, canonical=True):
    assert len(title) <= 60, (path, len(title)); assert len(desc) <= 158, (path, len(desc))
    canon = f'<link rel="canonical" href="{BASE}{path}">' if canonical else ""
    robots = '<meta name="robots" content="noindex, follow">' if noindex else ""
    og = (f'<meta property="og:type" content="website"><meta property="og:site_name" content="Car Wash Management">'
          f'<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">'
          + (f'<meta property="og:url" content="{BASE}{path}">' if canonical else "")
          + f'<meta property="og:image" content="{BASE}/assets/cwm/img/cwm-logo-horizontal.png"><meta name="twitter:card" content="summary">')
    return f'''<!doctype html><html lang="en"><head><script>document.documentElement.classList.add("js")</script><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}">{canon}{robots}{og}
<meta name="theme-color" content="#0B1B2B"><link rel="icon" href="/assets/cwm/img/favicon.ico" sizes="48x48"><link rel="icon" type="image/png" href="/assets/cwm/img/favicon-32.png" sizes="32x32"><link rel="apple-touch-icon" href="/assets/cwm/img/apple-touch-icon.png">
<link rel="preload" href="/assets/cwm/fonts/archivo-cwm.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="/assets/cwm/fonts/inter-cwm.woff2" as="font" type="font/woff2" crossorigin>
<style>{CSS}</style>{ld(ORG, *extra_ld)}</head><body>
{header(path)}
<main id="main">{body}</main>
{footer()}
<script src="/forms-config.js" defer></script><script src="/events-config.js" defer></script><script src="/assets/js/site-forms.js" defer></script><script src="/assets/cwm/js/cwm.js?v=20261028c" defer></script>
<script>{NAV_JS}</script>
</body></html>
'''

def downtime():
    return f'''<section class="downtime" aria-labelledby="dt-h"><div class="wrap"><div class="pulse" aria-hidden="true"></div><div><h2 id="dt-h">Wash down? Call now.</h2><p>Call or text <a href="tel:{PHONE_T}" data-evt="tel_click">{PHONE_D}</a>, {HOURS}. <a href="/urgent-car-wash-repair/">Urgent repair →</a></p></div>
<div class="acts">{call_btn("btn btn-ink", PHONE_D)}{text_btn()}</div></div></section>'''

def short_brand_chips():
    return "<ul class=\"chips sm\">" + "".join(
        f'<li><a class="chip" href="{BRANDS_URL}#{a}">{n}</a></li>' for n, a in BRAND_SHORT) + "</ul>"
def brands_block(h="h2"):
    return f'''<section class="brands" aria-labelledby="br-h"><div class="wrap"><div class="eyebrow">Brands and equipment</div><{h} id="br-h">Brands we service and support.</{h}>
<p class="bintro">Tunnel, in-bay, self-serve, vacuum, pay station, pump, and water equipment. A few of the names are below. Don’t see yours? Call or text {PHONE_D}.</p>
{short_brand_chips()}<p class="tm">{TM}</p><a class="lnk" href="{BRANDS_URL}">See all the brands we service and support →</a></div></section>'''

def final_cta():
    return f'''<section class="final" aria-labelledby="fin-h"><div class="wrap grid"><div><div class="eyebrow" style="color:var(--sky)">Get help today</div><h2 id="fin-h" style="margin-top:14px">Let’s get your wash running right.</h2><p>Call or text {PHONE_D}, or send the form. Tell us your equipment and what’s going on.</p>
<div style="display:flex;gap:12px;flex-wrap:wrap">{call_btn("btn btn-amber")}{text_btn()}</div><p class="em">Or email <a href="mailto:{EMAIL}">{EMAIL}</a> · Hours: {HOURS}</p></div>
<div><div class="form"><h3>Prefer the form?</h3><p class="sub">It takes about two minutes. Your details go straight to our team.</p><a class="btn btn-blue" href="#request">Go to the request form {I_ARR}</a><p class="alt">Or use the <a href="/contact/">Request Service page</a></p></div></div></div></section>'''

# ---------------- Home ----------------
# job-03 (cloth on the ground) is retired from pages. job-equip-01 replaces it.
# job-tunnel-01/02/03 are one job from different angles, so they are not placed together.
JOBS_STRIP = ["nb-04", "job-tunnel-01", "job-01", "job-tunnel-04", "job-02", "job-equip-01", "job-tunnel-06", "nb-28", "nb-26"]
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
    card_img = {"01": "avw-card-repair", "02": "avw-card-installation", "03": "avw-card-support"}
    cardh = "".join(f'''<article class="card"><div class="media">{img(card_img[n], "(max-width:700px) calc(100vw - 40px), 369px")}</div><div class="bd"><h3><span class="n">{n}</span>{t}</h3><p>{d}</p><ul class="ticks">{"".join(f"<li>{x}</li>" for x in li)}</ul><a class="more" href="{u}">{a} {I_ARR}</a></div></article>''' for n, t, u, a, d, li in cards)
    jobs = "".join(f'<figure>{img(k, "(max-width:700px) calc(50vw - 27px), 360px")}</figure>' for k in JOBS_STRIP)
    steps = [("Call, text or send the form", "Tell us your equipment and what’s happening. A photo of the problem helps."),
             ("We look at it", "We get eyes on the equipment and tell you plainly what it needs."),
             ("We repair, replace or set up a plan", "The work gets done, and your team knows what changed."),
             ("We’re still there after", "Same number, same team, every time your wash needs us.")]
    stp = "".join(f'<li class="st"><div class="num">{i}</div><h3>{a}</h3><p>{b}</p></li>' for i, (a, b) in enumerate(steps, 1))
    body = f'''<section class="hero home">{hero_bg(HOME_HERO)}<div class="wrap grid"><div>
<h1>Car Wash Equipment Service, Installation &amp; Support for Any Brand Across the Southwest United States and Hawaii</h1>
<p class="hd head">Any equipment.<br>Any problem.<br><em>We’re there for you.</em></p>
<p class="lead">Car Wash Management services and repairs any car wash equipment, installs and replaces equipment and components, and supports your team, so your wash keeps running and your customers keep coming.</p>
<div class="btns">{call_btn()}<a class="btn btn-ghost" href="#request">Request Service {I_ARR}</a></div>
<p class="sms">Serving the Southwest United States and Hawaii. Or text a photo of the problem to <a href="sms:{PHONE_T}" data-evt="sms_click">{PHONE_D}</a> · {HOURS}</p>
</div><div id="request">{form("home-request", "home-hero")}</div></div></section>
{downtime()}
<section class="s" aria-labelledby="wd-h"><div class="wrap"><div class="sh"><div><div class="eyebrow">What we do</div><h2 id="wd-h">Service, installation and support. One team for your whole wash.</h2></div><p>Aging equipment, a part that needs replacing, or a bay that just went down: call one number and we take it from there.</p></div><div class="cards">{cardh}</div></div></section>
{brands_block()}
<section class="area" aria-labelledby="ar-h"><div class="wrap"><div class="ahead"><div><div class="eyebrow">Service area</div><h2 id="ar-h">Serving the Southwest United States and Hawaii.</h2></div><p>{AREA_LINE}</p></div><a class="lnk" href="/service-area/">See our service area →</a></div></section>
<section class="s dark" aria-labelledby="ba-h"><div class="wrap"><div class="sh"><div><div class="eyebrow">Our work</div><h2 id="ba-h">Real jobs. Up close.</h2></div><p style="color:var(--on-dark)">Photos from work we have done.</p></div>
<div class="jobs">{jobs}</div></div></section>
<section class="chem" aria-labelledby="ch-h" style="background:var(--mist)"><div class="wrap cg"><div class="cimg">{img("chemistry", "(max-width:700px) calc(100vw - 40px), 552px")}</div><div><div class="eyebrow">Chemistry</div><h2 id="ch-h">Chemistry tailored to your wash by a real chemist.</h2><p>Car Wash Management supplies soaps and chemicals from the Car Wash Labs (Car Wash Laboratories) line.</p><p style="margin-top:10px">We also service chemical injectors and dosing equipment.</p><a class="lnk" href="/chemistry/">Car wash chemicals &amp; programs →</a></div></div></section>
<section class="s steps" aria-labelledby="hw-h"><div class="wrap"><div class="sh"><div><div class="eyebrow">How it works</div><h2 id="hw-h">From “it’s broken” to running, in four steps.</h2></div></div><ol class="sgrid">{stp}</ol></div></section>
{final_cta()}'''
    website = {"@context": "https://schema.org", "@type": "WebSite", "@id": BASE + "/#website", "name": "Car Wash Management", "url": BASE + "/", "publisher": {"@id": BASE + "/#org"}}
    return page("/", "Southwest & Hawaii Car Wash Service | Car Wash Management",
                "We service and repair car wash equipment across the Southwest United States and Hawaii, and install single parts to complete systems. Call or request a quote.",
                body, (website,))

# ---------------- Inner pages ----------------
def inner(path, crumb, title, desc, h1, lead, content, soon, form_heading="Request service or a quote", extra_ld=(), parent=None):
    soon_html = ""
    hk = PAGE_HERO.get(path)
    body = f'''<section class="phero{" photo" if hk else ""}">{hero_bg(hk) if hk else ""}<div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> › {f'<a href="{parent[0]}">{parent[1]}</a> › ' if parent else ""}<span aria-current="page">{crumb}</span></nav>
<h1>{h1}</h1><p class="lead">{lead}</p><div class="btns">{call_btn()}{text_btn()}<a class="btn btn-ghost" href="#request">Request Service {I_ARR}</a></div></div></section>
{downtime() if path != "/urgent-car-wash-repair/" else ""}
<section class="body"><div class="wrap cols"><div class="txt">{content}{soon_html}</div><div id="request">{form(path.strip("/").replace("/", "-") + "-request", path, form_heading, "h2", True)}</div></div></section>'''
    return page(path, title, desc, body, (crumbs_ld(path, crumb, parent), *extra_ld))

def facts():
    return f'''<ul class="facts"><li><b>Call or text:</b> <a href="tel:{PHONE_T}" data-evt="tel_click">{PHONE_D}</a> (<a href="sms:{PHONE_T}" data-evt="sms_click">text</a>)</li><li><b>Email:</b> <a href="mailto:{EMAIL}">{EMAIL}</a></li><li><b>Hours:</b> {HOURS}</li></ul>'''
def brand_list():
    return f'<p>We service and support all major brands, including the names below. <a href="{BRANDS_URL}">See every brand we service and support</a>.</p>{short_brand_chips()}<p class="tm">{TM}</p>'
def service_ld(path, name, stype):
    return {"@context": "https://schema.org", "@type": "Service", "name": name, "serviceType": stype, "url": BASE + path, "provider": {"@id": BASE + "/#business"}}
def repair_faq():
    return [
        ("What equipment do you repair?", "Tunnels, in-bay automatics and self-serve bays: conveyors, brushes, pumps, pay stations, sensors, chemical dosing, and water, RO and reclaim components. Hydraulic drives and gearboxes are rebuilt in-house."),
        ("Do you repair equipment you did not install?", "Yes. We service and repair equipment whether or not we installed it."),
        ("Can you troubleshoot it over the phone?", "Most car wash faults need a technician on site to diagnose properly, so the usual route is to book a visit. The safe checks in our <a href=\"/blog/\">guides</a> are general background, not a phone diagnosis."),
        ("How soon can you get there?", f"Call or text {PHONE_D}, {HOURS}. We aim to respond quickly. We do not promise an arrival window."),
        ("Where do you work?", "On-site repair is centered on Southern California. Outside California, across the Southwest United States and Hawaii, we provide full site management and on-site service by arrangement. Travel charges apply; we’ll tell you before we book."),
        ("Which brands do you work on?", f"All major brands. Named examples are on our <a href=\"{BRANDS_URL}\">brands</a> page, with the trademark line."),
    ]
def repair_faq_ld():
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in repair_faq()]}

PAGES = {}
PAGES["/car-wash-equipment-repair/"] = lambda: inner("/car-wash-equipment-repair/", "Repair",
    "Car Wash Equipment Repair | Car Wash Management",
    "Service and repair for any car wash equipment: tunnels, in-bay automatics and self-serve bays, from conveyors and brushes to pumps and pay stations.",
    "Car Wash Equipment Repair",
    "We service and repair any car wash equipment, on tunnels, in-bay automatics and self-serve bays, including equipment we didn’t install.",
    f'''<h2>What we work on</h2><p>Car Wash Management techs service and repair the equipment that keeps a wash running, whatever the make or age. Most car wash faults need a technician on site to diagnose properly, so the usual route is to book a visit.</p>
<ul class="ticks"><li>Tunnel conveyors, brushes and gear drives</li><li>In-bay automatic wash systems</li><li>High-pressure and water pumps</li><li>Pay stations and wash controllers</li><li>Photo eyes and vehicle-position sensors</li><li>Chemical injectors and dosing equipment</li><li>Reverse osmosis, water and reclaim components</li></ul>
<p>Hydraulic drives and gearboxes are rebuilt in-house.</p>
<h2>Photos from our jobs</h2><p>These photos are from our work.</p>
{own_gallery(["job-equip-01", "job-tunnel-01", "job-tunnel-04", "job-tunnel-02", "job-tunnel-07", "job-tunnel-08", "job-01"])}
<h2>Recent work</h2>
<ul class="ticks"><li>Tunnel conveyor drive repair in Laguna Niguel, Orange County, March 2024.</li><li>In-bay automatic limit-fault repair in Calabasas, Los Angeles County, October 2026.</li></ul>
<h2>Questions</h2><div class="faq">{"".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in repair_faq())}</div>
<h2>Brands we service and support</h2>{brand_list()}{new_pages.guides_for("/car-wash-equipment-repair/")}<h2>How to reach us</h2>{facts()}''',
    None,
    extra_ld=(service_ld("/car-wash-equipment-repair/", "Car wash equipment repair", "Car wash equipment repair"), repair_faq_ld()))
PAGES["/car-wash-equipment-installation/"] = lambda: inner("/car-wash-equipment-installation/", "Installation",
    "Car Wash Equipment Installation | Car Wash Management",
    "Installation and replacement of car wash equipment and components, from single parts to complete systems. Request an installation quote today.",
    "Car Wash Equipment Installation &amp; Replacement",
    "Installation and replacement of equipment and components, from single parts to complete systems.",
    f'''<h2>What we install and replace</h2><ul class="ticks"><li>Replacement parts and components</li><li>Motors, gear drives and pumps</li><li>Pay stations and wash controllers</li><li>Reverse osmosis, water and reclaim components</li></ul>
<p>Not sure whether to repair or replace? Call or text and tell us what you’re working with.</p><p>Installation and replacement of equipment and components, from single parts to complete systems. Travel charges apply to on-site visits; we’ll tell you before we book.</p>
<h2>Photos from our jobs</h2><p>These photos are from our work. They show equipment we have put in.</p>
{own_gallery(["job-tunnel-05", "job-equip-01", "nb-26", "nb-25", "nb-30", "nb-28"])}
<h2>Recent work</h2>
<p>In October 2023 we supplied and installed an RO booster pump in the Inland Empire.</p>
{new_pages.guides_for("/car-wash-equipment-installation/")}<h2>How to reach us</h2>{facts()}''',
    None, "Request an installation quote",
    extra_ld=(service_ld("/car-wash-equipment-installation/", "Car wash equipment installation and replacement", "Car wash equipment installation"),))
PAGES["/car-wash-maintenance-plans/"] = lambda: inner("/car-wash-maintenance-plans/", "Maintenance Plans",
    "Car Wash Preventive Maintenance Plans | Car Wash Management",
    "Scheduled preventive maintenance visits, priority scheduling and a custom quote for each site. Ask Car Wash Management about a plan for your wash.",
    "Car Wash Preventive Maintenance &amp; Support Plans",
    "Scheduled preventive maintenance visits, priority scheduling and a custom quote for each site.",
    f'''<h2>Talk to us about a plan</h2><p>Tell us your wash type and equipment, and we’ll talk through what ongoing maintenance and support could look like for your site. Plans are customized for each wash, including how often we visit. There are no fixed tiers or package names.</p><ul class="ticks"><li>Scheduled preventive maintenance visits</li><li>Priority scheduling</li><li>A custom quote for each site</li></ul>{new_pages.guides_for("/car-wash-maintenance-plans/")}<h2>How to reach us</h2>{facts()}''',
    None, "Ask about a maintenance plan",
    extra_ld=(service_ld("/car-wash-maintenance-plans/", "Car wash preventive maintenance", "Car wash equipment maintenance"),))
PAGES["/urgent-car-wash-repair/"] = lambda: inner("/urgent-car-wash-repair/", "Wash Down? Urgent Car Wash Repair",
    "Wash Down? Urgent Car Wash Repair | Car Wash Management",
    f"Wash down? Call or text Car Wash Management at {PHONE_D} and tell us what stopped.",
    "Wash Down? Urgent Car Wash Repair",
    f"Call or text {PHONE_D} and tell us what stopped. Hours: {HOURS}.",
    f'''<h2>Call or text with what stopped</h2><p>Call or text <a href="tel:{PHONE_T}" data-evt="tel_click">{PHONE_D}</a> and tell us what stopped: the equipment, what it’s doing and when it stopped. A photo of the problem helps.</p>
<p>Call or text {PHONE_D} and tell us what stopped. Hours: {HOURS}. We aim to respond quickly. Most faults need a technician on site to diagnose properly.</p>{new_pages.guides_for("/urgent-car-wash-repair/")}<h2>How to reach us</h2>{facts()}''',
    None, "Request urgent service",
    extra_ld=(service_ld("/urgent-car-wash-repair/", "Urgent car wash repair", "Car wash equipment repair"),))
# ---------------- Equipment hub + category pages ----------------
CAT_MANIFEST = DESIGN / "categories/manifest.csv"
# 01/02/03 are one tunnel from different angles, so they are separated in the gallery.
OWNER_TUNNEL = ["job-tunnel-01", "job-tunnel-04", "job-tunnel-06", "job-tunnel-02", "job-tunnel-07", "job-tunnel-05", "job-tunnel-03", "job-tunnel-08"]
CAT_OWN = {"tunnel": OWNER_TUNNEL + ["nb-12", "nb-06", "nb-01", "nb-32"], "in-bay-automatic": ["nb-15", "nb-16", "nb-18"],
           "chemical-dosing": ["job-equip-01", "nb-28", "nb-29"], "water-reclaim-ro": ["nb-30", "nb-26", "nb-25"]}   # Andrew's picks, shown first
_cat_rows = []
if _design_sources_ready():
    _cat_rows = [r for r in csv.DictReader(CAT_MANIFEST.open(encoding="utf-8")) if not r["filename"].startswith("avw/")
                 and not _bad(r["filename"], r.get("pick")) and (DESIGN / r["filename"]).is_file()]
def design_category(slug):
    """Design's set for one category from categories/manifest.csv (files under categories/<slug>/; AVW ones are copies of avw/categories/).
    Files go to assets/cwm/img/photos/ as cat-<slug>-<base>-<w>w.webp (avw-cat-... for manufacturer images)."""
    rows = [r for r in _cat_rows if r["category"] == slug]
    if not rows: return None
    keys = _register(rows, DESIGN, lambda base, r0: ("avw-" if r0["kind"].strip() == "manufacturer" else "") + "cat-" + slug + "-" + pathlib.Path(base).name.replace(slug + "-", ""), _ALT_FIX)
    hero = next((k for k in keys if IMG[k][7]["slot"].lower().endswith("hero")), None)
    return hero, CAT_OWN.get(slug, []) + [k for k in keys if k != hero]
for c in CATEGORIES:
    c["path"] = f"/equipment/{c['slug']}/"
    if _design_sources_ready():
        c["hero"], c["gallery"] = design_category(c["slug"]) or c["images"]
    else:
        lay = PHOTO_REG["categories"][c["slug"]]
        c["hero"], c["gallery"] = lay["hero"], lay["gallery"]
    if c["hero"]: PAGE_HERO[c["path"]] = c["hero"]
for c in CATEGORIES:
    if c["slug"] == "tunnel":
        rest = [k for k in c["gallery"] if k not in OWNER_TUNNEL]
        c["gallery"] = OWNER_TUNNEL + rest
    elif c["slug"] == "chemical-dosing" and "job-equip-01" not in c["gallery"]:
        c["gallery"] = ["job-equip-01"] + list(c["gallery"])
CAT_FOR_BRANDCAT = {"tunnel": "/equipment/tunnel/", "in-bay": "/equipment/in-bay-automatic/", "self-serve": "/equipment/self-serve/",
                    "vacuums": "/equipment/vacuums/", "controllers": "/equipment/controllers-pay-stations/", "chemistry-water": "/equipment/"}
CAT_LINKS = {"tunnel": '<p><a href="/equipment/tunnel/">Tunnel equipment service and repair →</a></p>',
             "in-bay": '<p><a href="/equipment/in-bay-automatic/">In-bay automatic service and repair →</a></p>',
             "self-serve": '<p><a href="/equipment/self-serve/">Self-serve equipment service and repair →</a></p>',
             "vacuums": '<p><a href="/equipment/vacuums/">Vacuum service and repair →</a></p>',
             "controllers": '<p><a href="/equipment/controllers-pay-stations/">Controller and pay station service and repair →</a></p>',
             "water": '<p><a href="/equipment/water-reclaim-ro/">Water, reclaim and RO service →</a></p>',
             "pumps": '<p><a href="/equipment/water-reclaim-ro/">Pumps on water, reclaim and RO equipment →</a></p>',
             "dosing": '<p><a href="/equipment/chemical-dosing/">Chemical dosing equipment →</a></p>',
             "supplies": '<p><a href="/chemistry/">Soaps and chemicals</a> · <a href="/equipment/chemical-dosing/">Chemical dosing equipment</a></p>'}
BRAND_BY_ANCHOR = {a: n for _, _, _, bs in BRAND_CATS for n, a, *_ in bs}
def cat_faq(c):
    n = c["name"]
    qs = [(f"How do I get my {n} equipment looked at?", f"Call or text {PHONE_D}, or send the request form on this page. Hours: {HOURS}."),
          (f"What if my {n} equipment goes down after hours?", f"Call or text {PHONE_D} and tell us what stopped, or send the request form. Hours: {HOURS}.")]
    qs.append((f"Do you install and replace {n} equipment?", "Yes. Installation and replacement of equipment and components, from single parts to complete systems.")
              if c["extra_q"] == "install" else
              (f"Do you offer maintenance plans for {n} equipment?", "Yes. Scheduled preventive maintenance visits, priority scheduling and a custom quote for each site."))
    qs.append((f"Where do you service {n} equipment?", AREA_LINE))
    return qs
def gallery(c):
    keys = c["gallery"]
    if not keys:
        return ""
    figs = [f'<figure>{img(k, "(max-width:700px) calc(50vw - 27px), 260px")}</figure>' for k in keys]
    return f'<div class="gal">{"".join(figs)}</div>'
def category_page(c):
    faq = cat_faq(c)
    brands = "".join(f'<li><a class="chip" href="{BRANDS_URL}#{a}">{BRAND_BY_ANCHOR[a]}</a></li>' for a in c["brands"])
    content = f'''<h2>What we service</h2><ul class="ticks">{"".join(f"<li>{x}</li>" for x in c["components"])}</ul>
<h2>Common faults we fix</h2><ul class="ticks">{"".join(f"<li>{x}</li>" for x in c["faults"])}</ul>
<h2>Photos</h2>{gallery(c)}
<h2>Brands we service and support</h2>{(f'<p>We service and support all major {c["name"]} equipment brands, including these. <a href="{BRANDS_URL}">See every brand we service and support</a>.</p><ul class="chips sm">{brands}</ul><p class="tm">{TM}</p>') if brands else f'<p>We service and support all major {c["name"]} equipment brands. Call or text {PHONE_D} with the make and model. <a href="{BRANDS_URL}">See every brand we service and support</a>.</p>'}
<h2>Questions</h2><div class="faq">{"".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in faq)}</div>
{new_pages.guides_for(c["path"])}<h2>How to reach us</h2>{facts()}'''
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": html.unescape(q), "acceptedAnswer": {"@type": "Answer", "text": html.unescape(a)}} for q, a in faq]}
    svc = service_ld(c["path"], html.unescape(c["short"]) + " car wash equipment service and repair", "Car wash equipment repair")
    return inner(c["path"], c["short"], c["title"], c["desc"], c["h1"], c["lead"], content, None,
                 "Request service or a quote",
                 extra_ld=(svc, faq_ld), parent=("/equipment/", "Equipment"))
for _c in CATEGORIES: PAGES[_c["path"]] = (lambda c=_c: category_page(c))
def equipment_hub():
    cards = ""
    for c in CATEGORIES:
        k = c["hero"] or (c["gallery"][0] if c["gallery"] else None)
        media = img(k, "(max-width:700px) calc(100vw - 40px), 270px") if k else ""
        cards += f'''<article class="card ecard"><div class="media">{media}</div><div class="bd"><h3><a href="{c["path"]}">{c["short"]}</a></h3><p>{c["card"]}</p><a class="more" href="{c["path"]}">Service &amp; repair {I_ARR}</a></div></article>'''
    content = f'''<p>We service and repair car wash equipment across every part of the wash. Pick a category to see what we work on, common faults we fix and the brands we see most.</p>
<div class="ecards">{cards}</div><h2>Brands we service and support</h2><p>See the full list on our <a href="{BRANDS_URL}">brands we service and support</a> page.</p>{brand_list()}<p>Practical answers are in the <a href="/blog/">equipment guides</a>.</p><h2>How to reach us</h2>{facts()}'''
    return inner("/equipment/", "Equipment",
        "Car Wash Equipment We Service | Car Wash Management",
        "Car Wash Management services and repairs in-bay automatic, tunnel, self-serve, vacuum, pay station, chemical dosing and water reclaim equipment.",
        "Car Wash Equipment We Service",
        "In-bay automatics, tunnels, self-serve bays, vacuums, controllers and pay stations, chemical dosing, and water, reclaim and RO.",
        content, None)
PAGES["/equipment/"] = equipment_hub
BRAND_PHOTO = {}
def BRAND_IMG(a):
    k = BRAND_PHOTO[a]
    return f'<figure class="bimg">{img(k, "(max-width:700px) calc(100vw - 40px), 560px")}</figure>'
def brands_page():
    jump = '<ul class="chips sm">' + "".join(f'<li><a class="chip" href="#{cid}">{short}</a></li>' for cid, _, short, _ in BRAND_CATS) + "</ul>"
    secs = "".join(f'<h2 id="{cid}">{name}</h2>' + CAT_LINKS.get(cid, "") + "".join(f'<h3 id="{a}">{n}</h3><p>{txt}</p>' + (BRAND_IMG(a) if a in BRAND_PHOTO else "") for n, a, _, txt, *_ in bs) for cid, name, _, bs in BRAND_CATS)
    content = f'''<p>We service and support car wash equipment from the manufacturers below, and from others not listed. If yours isn’t listed, call or text <a href="tel:{PHONE_T}" data-evt="tel_click">{PHONE_D}</a>.</p>
{jump}<p class="tm">{TM}</p>{secs}<p class="tm">{TM}</p><h2>How to reach us</h2>{facts()}'''
    svc = service_ld(BRANDS_URL, "Car wash equipment we service and support", "Car wash equipment repair")
    svc["description"] = "Service and support for tunnel, in-bay automatic, self-serve, vacuum, pay station, pump, and water equipment from the major manufacturers."
    return inner(BRANDS_URL, "Brands We Service and Support",
        "Brands We Service and Support | Car Wash Management",
        "Brands we service and support, from tunnel and in-bay equipment to pumps, pay stations, vacuums, and water treatment.",
        "Brands We Service and Support",
        "We service and support car wash equipment from the manufacturers below, and from others not listed.",
        content, None, extra_ld=(svc,))
PAGES[BRANDS_URL] = brands_page
PAGES["/service-area/"] = lambda: inner("/service-area/", "Service Area",
    "Service Area: Southwest US & Hawaii | Car Wash Management",
    f"Car Wash Management services car washes across the Southwest United States and Hawaii. Call or text {PHONE_D} to check if we can reach your site.",
    "Car Wash Equipment Service Across the Southwest United States and Hawaii",
    AREA_LINE,
    f'''<h2>Where we work</h2><p>On-site repair is centered on Southern California. Outside California, across the Southwest United States and Hawaii, we provide <a href="/car-wash-management-services/">full site management</a> and on-site service by arrangement. Travel charges apply to on-site visits; we’ll tell you before we book.</p>
<p>{AREA_LINE} We aim to respond quickly.</p>
{new_pages.state_cards()}
<p><a href="/blog/">Equipment guides</a> answer common faults before you call.</p>
<h2>How to reach us</h2>{facts()}''',
    None)
PAGES["/chemistry/"] = lambda: inner("/chemistry/", "Chemistry",
    "Car Wash Chemicals & Chemical Programs | Car Wash Management",
    "Soaps and chemicals from the Car Wash Labs line, plus dosing-equipment service. Call or text Car Wash Management.",
    "Car Wash Chemicals &amp; Chemical Programs",
    "Chemistry tailored to your wash by a real chemist.",
    f'''<div class="cimg inl">{img("chemistry", "(max-width:700px) calc(100vw - 40px), 560px")}</div><h2>Soaps and chemicals we supply</h2><p>Car Wash Management supplies soaps and chemicals from the Car Wash Labs (Car Wash Laboratories) line. We also clean tunnels and bays and supply the soaps and chemicals for that work.</p><h2>Dosing equipment</h2><p>We service chemical injectors and dosing equipment as part of our repair work. See <a href="/equipment/chemical-dosing/">chemical dosing equipment</a>.</p><p>Ask us about the chemistry for your wash.</p>{new_pages.guides_for("/chemistry/")}<h2>How to reach us</h2>{facts()}''',
    None, "Ask about chemistry")
PAGES["/about/"] = lambda: inner("/about/", "About",
    "About Car Wash Management | Car Wash Equipment Service",
    "Car Wash Management services and repairs car wash equipment and installs and replaces components. Learn who we are and how to reach our team.",
    "About Car Wash Management",
    "Car Wash Management services and repairs any car wash equipment, installs and replaces equipment and components, and supports owners and their teams.",
    f'''<h2>How the work started</h2><p>Car Wash Management started out washing cars in the back of a Honda Civic, and its car wash repair work grew through Marine Corps Base Hawaii. Today we repair, supply and install car wash equipment for all major brands across the Southwest United States and Hawaii.</p>
<h2>What we do</h2><ul class="ticks"><li><a href="/car-wash-equipment-repair/">Car wash equipment repair</a></li><li><a href="/car-wash-equipment-installation/">Installation and replacement</a></li><li><a href="/car-wash-maintenance-plans/">Maintenance and support</a></li><li><a href="/car-wash-management-services/">Full site management</a></li><li><a href="/chemistry/">Chemistry</a></li><li><a href="/blog/">Equipment guides</a></li></ul>
<h2>Photos from our jobs</h2><p>These photos are from our work.</p>{own_gallery(["nb-04", "job-01", "nb-15"])}
<h2>How to reach us</h2>{facts()}''',
    None,
    extra_ld=({"@context": "https://schema.org", "@type": "AboutPage", "url": BASE + "/about/", "name": "About Car Wash Management", "about": {"@id": BASE + "/#org"}},))
def contact():
    body = f'''<section class="phero"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> › <span aria-current="page">Request Service</span></nav>
<h1>Request Service or a Quote</h1><p class="lead">Call or text {PHONE_D}, or send the form. Tell us your wash type, equipment and what’s going on.</p></div></section>
<section class="body"><div class="wrap cols"><div id="request">{form("contact-request", "/contact/", "Service or quote request", "h2", True)}</div>
<div class="txt"><h2>Other ways to reach us</h2>{facts()}<div style="display:flex;gap:12px;flex-wrap:wrap;margin:6px 0 24px">{call_btn()}{text_btn("btn btn-white")}</div>
<h2>What to include</h2><ul class="ticks"><li>Your wash type (tunnel, in-bay automatic or self-serve)</li><li>The equipment and brand, if you know it</li><li>What it’s doing, and since when</li><li>A photo, texted to {PHONE_D}</li></ul>
<div class="note"><b>Wash down right now?</b> Call or text <a href="tel:{PHONE_T}" data-evt="tel_click">{PHONE_D}</a> instead of using the form.</div></div></div></section>'''
    cp = {"@context": "https://schema.org", "@type": "ContactPage", "url": BASE + "/contact/", "name": "Request Service or a Quote", "about": {"@id": BASE + "/#business"}}
    return page("/contact/", "Request Car Wash Service or a Quote | Car Wash Management",
                f"Call or send a service or quote request to Car Wash Management. Tell us your wash type, equipment and issue. Hours {HOURS}.",
                body, (crumbs_ld("/contact/", "Request Service"), cp))
def credits():
    used = [k for k in IMG if k in USED_IMG]
    own = "".join(f'<li>{html.escape(IMG[k][0])}</li>' for k in used if kind(k) == "own")
    man = "".join(f'<li><b>{html.escape(IMG[k][0])}</b><br>Manufacturer image from {c[0]}, <a href="{c[1]}" rel="nofollow noopener">source page</a>. Shown as a general example of the equipment; not a Car Wash Management job, site or install.</li>'
                  for k in used if (c := IMG[k][5]) and c[4] == "manufacturer")
    stock = "".join(f'<li><b>{html.escape(IMG[k][0])}</b><br>Photo by {c[0]}, <a href="{c[1]}" rel="nofollow noopener">source</a>, used under the <a href="{c[3]}" rel="nofollow noopener">{c[2]}</a>.</li>'
                    for k in used if (c := IMG[k][5]) and c[4] == "stock")
    body = f'''<section class="phero"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> › <span aria-current="page">Photo Credits</span></nav>
<h1>Photo Credits</h1><p class="lead">Where the photos on this site come from.</p></div></section>
<section class="body"><div class="wrap"><div class="txt" style="max-width:820px"><h2>Our own photos</h2><p>These photos were taken by Car Wash Management on our own jobs. The credit is in the image description, not printed on the picture. Customer names, sites, and license plates are left out or blurred.</p><ul class="ticks">{own}</ul>
<h2>Manufacturer images</h2><p>These are manufacturer images from AVW Equipment Company. They show the type of equipment we service. They are not our jobs, sites, or installs. The credit is in the image description, not printed on the picture. {TM}</p><ul class="ticks">{man}</ul>
<h2>Stock photos</h2><p>These are general car wash scenes from free stock libraries. They are not Car Wash Management jobs or sites. The credit is in the image description, not printed on the picture.</p><ul class="ticks">{stock}</ul></div></div></section>'''
    return page("/credits/", "Photo Credits | Car Wash Management", "Credits and licenses for the photos used on carwashmgmt.com: our own jobs, manufacturer images and stock.", body, noindex=True)
def thank_you():
    body = f'''<section class="ty"><div class="wrap"><div class="eyebrow">Request sent</div><h1 style="margin-top:12px">Thanks. We got your request.</h1>
<p>Your details went to the Car Wash Management team.</p><p>If your wash is down right now, call or text {PHONE_D}. Hours: {HOURS}.</p>
<div class="btns">{call_btn()}{text_btn("btn btn-white")}<a class="btn btn-white" href="/">Back to the homepage</a></div></div></section>'''
    return page("/thank-you/", "Thank You | Car Wash Management", "Thanks for your request. Car Wash Management received your details.", body, noindex=True)
def notfound():
    body = f'''<section class="ty"><div class="wrap"><div class="eyebrow">Error 404</div><h1 style="margin-top:12px">Page not found</h1>
<p>That page doesn’t exist or has moved. Try one of these, or call or text {PHONE_D}.</p>
<ul class="ticks" style="max-width:520px;margin-top:18px">{"".join(f'<li><a href="{u}">{t}</a></li>' for u, t in NAV)}<li><a href="/contact/">Request service</a></li></ul>
<div class="btns">{call_btn()}<a class="btn btn-white" href="/">Go to the homepage</a></div></div></section>'''
    return page("/404", "Page Not Found | Car Wash Management", "The page you were looking for could not be found.", body, noindex=True, canonical=False)

LEGAL = {PRIVACY_URL: ("privacy.html", "Privacy Policy", "Privacy Policy | Car Wash Management",
                       "How Car Wash Management collects, uses and protects your information, including text message (SMS) opt-in data.", "Last modified: November 11, 2026"),
         TERMS_URL: ("terms.html", "Terms &amp; Conditions", "Terms & Conditions | Car Wash Management",
                     "Terms for Car Wash Management services and our customer-care text message (SMS) program.", "Last updated: November 11, 2026")}
def legal(path):
    src, h1, title, desc, sub = LEGAL[path]
    txt = (ROOT / "_build/legal" / src).read_text()
    body = f'''<section class="phero"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> › <span aria-current="page">{h1}</span></nav>
<h1>{h1}</h1><p class="lead">Car Wash Management, LLC, a Delaware limited liability company. {sub}</p></div></section>
<section class="body"><div class="wrap"><div class="txt legal" style="max-width:820px">{txt}</div></div></section>'''
    return page(path, title, desc, body, (crumbs_ld(path, h1),), noindex=True)

def strip_comments(content):
    return re.sub(r"<!--.*?-->", "", content, flags=re.S)

def write(path, content):
    out = ROOT / ("index.html" if path == "/" else path.strip("/") + "/index.html")
    out.parent.mkdir(parents=True, exist_ok=True); out.write_text(strip_comments(content))

def stage_photo_sources():
    """Copy photo sources aside before assets/cwm/img/photos is rebuilt.
    Shipped-photo mode reads from that folder, so deleting it first would lose the files."""
    stage = pathlib.Path(tempfile.mkdtemp(prefix="cwm-photos-"))
    for k in list(IMG):
        alt, w, h, sw, sh, credit, files, meta = IMG[k]
        new = {}
        for width, src in files.items():
            dest = stage / f"{k}-{width}w.webp"
            shutil.copyfile(src, dest)
            new[width] = dest
        IMG[k] = (alt, w, h, sw, sh, credit, new, meta)

def main():
    new_pages.register(PAGES, {
        "inner": inner, "img": img, "facts": facts,
        "phone": PHONE_D, "tel": PHONE_T, "hours": HOURS, "tm": TM, "base": BASE,
        "service_ld": service_ld, "own_gallery": own_gallery,
    })
    built = {}
    for p, fn in [("/", home), ("/contact/", contact), ("/thank-you/", thank_you), *PAGES.items(), ("/credits/", credits)]:
        CUR_PAGE[0] = p; built[p] = fn()
    if _design_sources_ready():
        audit = pathlib.Path("/workspace/audit")
        if audit.is_dir():
            rows = []
            for k in USED_IMG:
                if kind(k) != "manufacturer": continue
                pages = sorted(p for p in USED_IMG[k] if p != "/credits/")
                for w, src in sorted(IMG[k][6].items(), reverse=True):
                    d = str(src).replace(str(DESIGN) + "/", ""); orig = d if d.startswith("avw/") else "avw/" + d
                    rows.append([f"{IMG_DIR}{k}-{w}w.webp", d, orig if (DESIGN / orig).is_file() else "", IMG[k][5][5], "; ".join(pages + ["/credits/"])])
            with open(audit / "avw-images.csv", "w", newline="") as fh:
                wr = csv.writer(fh); wr.writerow(["repo_path", "design_file", "avw_original_in_avw_files_txt", "source_url", "pages"]); wr.writerows(rows)
    stage_photo_sources()
    photos = ROOT / IMG_DIR.strip("/")
    shutil.rmtree(photos, ignore_errors=True); photos.mkdir(parents=True)
    # Copy photos the pages use, and keep retired job-03 files in the repo.
    for k in set(USED_IMG) | {"job-03"}:
        if k not in IMG:
            continue
        for w, src in IMG[k][6].items():
            assert not _bad(str(src)), src
            shutil.copyfile(src, photos / f"{k}-{w}w.webp")
    for p, c in built.items(): write(p, c)
    (ROOT / "404.html").write_text(strip_comments(notfound()))
    for lp in LEGAL: (ROOT / lp.strip("/")).write_text(strip_comments(legal(lp)))
    indexable = [p for p in built if p not in ("/thank-you/", "/credits/")]
    order = ["/", "/car-wash-equipment-repair/", "/car-wash-equipment-installation/", "/car-wash-maintenance-plans/", "/urgent-car-wash-repair/",
             "/car-wash-equipment-brands/", "/equipment/", *[f"/equipment/{c['slug']}/" for c in CATEGORIES],
             "/service-area/", *new_pages.STATE_PATHS, "/chemistry/", "/car-wash-management-services/", "/about/",
             "/blog/", *new_pages.POST_PATHS, "/contact/"]
    if sorted(order) != sorted(indexable):
        raise SystemExit(f"sitemap mismatch extra={sorted(set(indexable)-set(order))} missing={sorted(set(order)-set(indexable))}")
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
         # /blog/ now exists. Projects, consulting and the calculator still do not.
         ("/solutions.html", "/", 302), ("/solutions", "/", 302), ("/results.html", "/about/", 302), ("/results", "/about/", 302),
         ("/blog.html", "/blog/", 301), ("/blog", "/blog/", 301),
         ("/calculator.html", "/car-wash-equipment-installation/", 302), ("/calculator", "/car-wash-equipment-installation/", 302),
         ("/Testimonials", "/about/", 302), ("/BlogPost", "/blog/", 302), ("/ChemicalProduct", "/chemistry/", 302), ("/Contact", "/contact/", 301)]
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
