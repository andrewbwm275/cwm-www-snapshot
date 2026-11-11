"""New public pages for the unpublished redesign: guides, state service areas, full site management.
Copy is original, from the SEO briefs and the approved facts. Nothing here is a testimonial,
a price, a response-time promise, or a case study that was not in the approved job list."""
import html
import re

TM = ("Brand names are trademarks of their respective owners. Car Wash Management is an independent service company "
      "and is not affiliated with or endorsed by these manufacturers.")
MODIFIED = "2026-11-11"
BRANDS_LINE = "Sonny's, MacNeil, Ryko, Washworld, Coleman Hanna, Cat Pumps, and Unitec."

GUIDE_LINKS = {
    "/car-wash-equipment-repair/": [
        ("repair-or-replace-car-wash-equipment", "Should you repair or replace car wash equipment?"),
        ("conveyor-chain-slipping", "Why a conveyor chain slips"),
        ("in-bay-automatic-wont-detect-vehicle", "In-bay automatic will not detect the car"),
        ("car-wash-tunnel-cleaning-program", "Tunnel and bay cleaning program"),
        ("self-serve-no-soap-all-bays", "No soap in every self-serve bay"),
    ],
    "/car-wash-equipment-installation/": [
        ("repair-or-replace-car-wash-equipment", "Should you repair or replace car wash equipment?"),
    ],
    "/car-wash-maintenance-plans/": [
        ("repair-or-replace-car-wash-equipment", "Repair or replace, then keep it maintained"),
        ("car-wash-tunnel-cleaning-program", "Build cleaning into a maintenance plan"),
    ],
    "/urgent-car-wash-repair/": [
        ("conveyor-chain-slipping", "Conveyor chain slipping"),
        ("in-bay-automatic-wont-detect-vehicle", "In-bay automatic will not detect the car"),
        ("self-serve-no-soap-all-bays", "No soap in every self-serve bay"),
    ],
    "/equipment/tunnel/": [
        ("conveyor-chain-slipping", "Why a conveyor chain slips"),
        ("car-wash-tunnel-cleaning-program", "Tunnel and bay cleaning"),
    ],
    "/equipment/in-bay-automatic/": [
        ("in-bay-automatic-wont-detect-vehicle", "In-bay automatic will not detect the car"),
    ],
    "/equipment/self-serve/": [
        ("self-serve-no-soap-all-bays", "No soap in every bay"),
    ],
    "/equipment/chemical-dosing/": [
        ("self-serve-no-soap-all-bays", "No soap in every self-serve bay"),
        ("car-wash-tunnel-cleaning-program", "Cleaning chemistry and dosing"),
    ],
    "/equipment/water-reclaim-ro/": [
        ("car-wash-tunnel-cleaning-program", "Cleaning, pits and reclaim"),
    ],
    "/chemistry/": [
        ("car-wash-tunnel-cleaning-program", "Tunnel and bay cleaning chemistry"),
        ("self-serve-no-soap-all-bays", "No soap in every self-serve bay"),
    ],
}


def guides_for(path):
    items = GUIDE_LINKS.get(path)
    if not items:
        return ""
    lis = "".join(f'<li><a href="/blog/{slug}/">{html.escape(name)}</a></li>' for slug, name in items)
    return f'<h2>Guides</h2><ul class="ticks">{lis}</ul>'


def esc(text):
    return html.escape(text)


def plain(fragment):
    return html.unescape(re.sub(r"<[^>]+>", "", fragment))


def faq_html(faqs):
    return "<h2>FAQ</h2><div class=\"faq\">" + "".join(f"<h3>{esc(q)}</h3><p>{a}</p>" for q, a in faqs) + "</div>"


def faq_ld(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in faqs]}


def table(headers, rows):
    th = "".join(f"<th>{esc(h)}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{c if c.startswith('<') else esc(c)}</td>" for c in row) + "</tr>" for row in rows)
    return f'<div class="table-scroll"><table><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'


def related(links):
    lis = "".join(f'<li><a href="{href}">{esc(text)}</a></li>' for href, text in links)
    return f"<h2>Related pages</h2><ul class=\"ticks\">{lis}</ul>"


def sources(items):
    lis = "".join(f'<li><a href="{html.escape(href, quote=True)}" rel="noopener">{esc(text)}</a></li>' for href, text in items)
    return f"<h2>Sources</h2><ul class=\"ticks\">{lis}</ul>"


def coverage():
    return ("<p>On-site repair is centered on Southern California. Outside California, across the Southwest United States and Hawaii, "
            "Car Wash Management provides <a href=\"/car-wash-management-services/\">full site management</a> and on-site service by arrangement. "
            "Travel charges apply to on-site visits; we will tell you before we book.</p>")


def reach(H, lead):
    return (f"<p>{lead} Call or text <a href=\"tel:{H['tel']}\">{H['phone']}</a>, {H['hours']}. "
            "We aim to respond quickly. <a href=\"/contact/\">Request service</a>.</p>")


def brand_sentence():
    return f"<p>We work on all major brands. Named examples: {esc(BRANDS_LINE)}</p><p class=\"tm\">{TM}</p>"


def author(H):
    return {"@type": "Organization", "name": "Car Wash Management Service Team",
            "url": H["base"] + "/about/", "parentOrganization": {"@id": H["base"] + "/#org"}}


def posting_ld(H, spec, path, faqs):
    return {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": spec["h1"],
        "description": spec["desc"],
        "datePublished": MODIFIED,
        "dateModified": MODIFIED,
        "author": author(H),
        "publisher": {"@id": H["base"] + "/#org"},
        "image": f"{H['base']}/assets/cwm/img/photos/{spec['image']}-{spec['image_w']}w.webp",
        "mainEntityOfPage": H["base"] + path,
        "url": H["base"] + path,
        "about": {"@type": "Thing", "name": spec["about"]},
    }


# ---------- guides hub and posts ----------

POSTS = []  # filled after the builders, so lengths can be checked in order


def post_repair(H):
    faqs = [
        ("How old is too old for car wash equipment?",
         "Age alone is not the test. Look at repeat failures, parts you can no longer get, the frame, and whether the controls can run the wash menu and payment options you need. A full equipment inspection is how we sort that out."),
        ("Do you work on all brands?",
         "Yes, all major brands. Named examples: " + esc(BRANDS_LINE) + " " + TM),
        ("Can I replace just the controller?",
         "Often yes. Controllers, pay stations, dryers, pump stations, and RO or reclaim equipment can be replaced without replacing the whole wash. See <a href=\"/equipment/controllers-pay-stations/\">controllers and pay stations</a> and <a href=\"/equipment/water-reclaim-ro/\">water, reclaim and RO</a>."),
        ("Is remanufactured equipment reliable?",
         "Auto Laundry News discusses remanufacturing as a middle path between a parts repair and a full replacement. We do not publish a reliability rate. An inspection is what tells us whether a repair, a reman unit, or a replacement fits the wash."),
        ("What happens after the inspection?",
         "We replace the damaged parts. You then have a clear view of whether the rest of the equipment is worth keeping. Travel charges apply to on-site visits; we will tell you before we book."),
        ("Do you work in my state?",
         "On-site repair is centered on Southern California. Elsewhere in the Southwest United States and Hawaii we provide full site management and on-site service by arrangement. See the <a href=\"/service-area/\">service area</a>."),
    ]
    body = f"""
<h2>The quick decision checklist</h2>
<p>Use the pattern of the failures, not a dollar cutoff. We do not publish a price at which you should replace equipment.</p>
{table(["Signal", "Leans repair", "Leans replace"], [
    ["Failure type", "One part or one subsystem", "The same wash fails across several subsystems"],
    ["Parts", "The part is still available", "The model is discontinued and parts are gone"],
    ["Frame and structure", "Sound metal, no cracked welds", "Corrosion or cracked welds in the structure"],
    ["Controls", "The controller still runs the menu you sell", "It cannot take the payment or wash options you need"],
    ["Downtime", "Rare, and traced to one cause", "Repeat stops that keep taking the wash offline"],
    ["Wash quality", "Complaints track to a worn part", "Quality stays poor after worn parts are replaced"],
    ["Water and chemical use", "In line with the equipment you have", "Much heavier than newer equipment can run, with no parts path to close the gap"],
])}
<h2>Signs the equipment is near the end of its life</h2>
<p>Repeat failures, parts you cannot buy, structural corrosion, and controls that cannot run a current wash menu are the signs industry writers point to. Auto Laundry News walks through end-of-life questions in “Time to Upgrade?”, and Professional Carwashing &amp; Detailing covers the same decision for in-bay automatics in “Time to upgrade your IBA”.</p>
<h2>Repair, rebuild, or replace</h2>
<p>Repair means replacing the damaged parts and leaving the rest of the unit in service. A rebuild or remanufactured unit is the middle path Auto Laundry News describes in “Repair, Replace, or Reman?”: more than a single part, short of an all-new system. Replace the whole system when breakdowns repeat across subsystems, parts are obsolete, or the unit cannot support the packages, payment options, or throughput you need.</p>
<h2>You can replace one piece</h2>
<p>A controller, pay station, dryer, pump station, or RO and reclaim skid can be swapped without a whole new wash. Start with <a href="/equipment/controllers-pay-stations/">controller and pay station service</a> or <a href="/equipment/water-reclaim-ro/">water, reclaim and RO</a>, and the <a href="/equipment/">equipment hub</a> for tunnels, <a href="/equipment/in-bay-automatic/">in-bay automatics</a>, and <a href="/equipment/self-serve/">self-serve bays</a>.</p>
<h2>Count downtime, not just the repair bill</h2>
<p>A cheap part is not cheap if the wash sits idle. Fill in your own numbers. We will not invent them for you:</p>
<p>(days down per year × your typical cars per day × your average ticket) + what you spend on repairs in a year, compared with what replacement would cost.</p>
<p>That is a worksheet, not a quote.</p>
<h2>Start with a full equipment inspection</h2>
<p>Car Wash Management starts with a full equipment inspection, then replaces the damaged parts. You pay to fix what is actually failing, and you can see whether the rest is worth keeping. The inspection looks at the structure and frame, the drive or conveyor or gantry, hydraulics and pumps, electrical and controls, sensors, chemical delivery, water treatment, RO and reclaim, wear parts, and the service history. We do not state an inspection price here. Travel charges apply to on-site visits; we will tell you before we book.</p>
<p><a class="btn btn-blue" href="/contact/">Book a full equipment inspection</a></p>
<h2>Example from the field</h2>
<aside class="soon"><b>Real example.</b> In-bay automatic limit fault, Los Angeles County (Calabasas), October 2026. The job type on file is a repair of a limit fault. We are not adding a diagnosis, a parts list, or a customer name.</aside>
{H["confirm"]("an owned photo of the October 2026 Calabasas limit-fault job, and whether any further detail may be published")}
<h2>If you replace, we supply and install</h2>
<p>We supply and install car wash equipment: tunnel, in-bay automatic, self-serve, vacuums, controllers and pay stations, chemical dosing, and water, reclaim and RO. Read <a href="/car-wash-equipment-installation/">car wash equipment installation</a>. This page does not add permit, electrical, or other steps beyond that.</p>
<h2>If you repair, keep it from happening again</h2>
<p>A <a href="/car-wash-maintenance-plans/">preventive maintenance plan</a> is built for your wash, including how often we visit. There is no fixed tier list. Day-to-day repair stays on <a href="/car-wash-equipment-repair/">car wash equipment repair</a>.</p>
{faq_html(faqs)}
{reach(H, "Not sure which way to go? Start with a full equipment inspection.")}
<p>Wash down right now? Use <a href="/urgent-car-wash-repair/">urgent car wash repair</a>.</p>
{coverage()}
{brand_sentence()}
{related([
    ("/car-wash-equipment-installation/", "Car wash equipment installation"),
    ("/car-wash-equipment-repair/", "Car wash equipment repair"),
    ("/car-wash-maintenance-plans/", "Preventive maintenance plan"),
    ("/equipment/", "Equipment we service"),
    ("/equipment/tunnel/", "Tunnel equipment"),
    ("/equipment/in-bay-automatic/", "In-bay automatic equipment"),
    ("/equipment/self-serve/", "Self-serve equipment"),
    ("/equipment/controllers-pay-stations/", "Controllers and pay stations"),
    ("/equipment/water-reclaim-ro/", "Water, reclaim and RO"),
    ("/urgent-car-wash-repair/", "Urgent repair"),
    ("/service-area/", "Service area"),
    ("/contact/", "Request service"),
    ("/blog/conveyor-chain-slipping/", "Conveyor chain slipping"),
    ("/blog/in-bay-automatic-wont-detect-vehicle/", "In-bay automatic will not detect the car"),
])}
{sources([
    ("https://www.carwashmag.com/repair-replace-or-reman-making-smarter-maintenance-decisions/", "Auto Laundry News: Repair, Replace, or Reman?"),
    ("https://www.carwashmag.com/time-to-upgrade-determining-when-equipment-has-reached-end-of-life/", "Auto Laundry News: Time to Upgrade?"),
    ("https://www.carwashmag.com/modern-repair-maintenance-the-basics-havent-changed/", "Auto Laundry News: Modern Repair & Maintenance"),
    ("https://www.carwash.com/time-upgrade-iba/", "Professional Carwashing & Detailing: Time to upgrade your IBA"),
    ("https://www.carwashmag.com/every-operator-needs-a-maintenance-program-and-the-discipline-to-follow-it/", "Auto Laundry News: every operator needs a maintenance program"),
])}
"""
    return body, faqs


def post_chain(H):
    faqs = [
        ("How tight should the conveyor chain be?",
         "Use the manufacturer’s specification for your conveyor. A practical check is to look at the take-up and the slack in the trough with the conveyor locked out. Too loose and the chain can skip. Too tight and you load the sprocket, shaft, and bearings. We do not publish a universal tension number."),
        ("Should I grease the conveyor chain?",
         "Kleen-Rite’s tunnel roller-chain guidance says to flush the chain and rollers rather than grease them. Follow your own manufacturer’s manual if it says otherwise."),
        ("How often should I replace sprockets?",
         "When the teeth show wear: hooked, pointed, or shark-fin shapes that no longer match the chain. There is no interval we will invent here."),
        ("Can I keep running while the chain slips?",
         "No. A slipping chain can jump a tooth, damage the sprocket, and stop the tunnel. Lock it out and have it looked at."),
        ("Do you service all brands of tunnel equipment?",
         "Yes, all major brands. Named examples: " + esc(BRANDS_LINE) + " " + TM),
    ]
    body = f"""
<h2>Safety first: lock it out</h2>
<p>Lock out and tag out the conveyor before anyone touches the chain, the trough, or the drive. OSHA’s <a href="https://www.osha.gov/control-hazardous-energy" rel="noopener">control of hazardous energy</a> rules are the standard. Do not inspect a moving chain.</p>
<h2>The five common causes</h2>
<p>Most slipping comes down to tension, the sprocket, the chain itself, something binding in the trough, or a drive that is losing power. Industry troubleshooting write-ups, including InnovateIT on conveyor chain slips, sort the problem the same way.</p>
<h3>Take-up tension too loose or too tight</h3>
<p>What you will see: the chain jumps under load, or the drive sounds like it is straining. How to check: with the conveyor locked out, look at the take-up and the slack. Fix or call: a small take-up adjustment may be in your manual. If it slips again after that, stop and book a technician. <a href="/equipment/tunnel/">Tunnel car wash equipment repair</a> is the service page.</p>
<h3>Worn drive sprocket teeth</h3>
<p>What you will see: teeth that look hooked or pointed, and a chain that climbs them. How to check: locked out, look at the drive sprocket. Fix or call: a worn sprocket is a replacement, not a tension tweak. That is technician work.</p>
<h3>Chain stretch</h3>
<p>What you will see: the chain is long for the sprocket even when the take-up is set, or pins and bushings are worn through. How to check: compare a worn section with the sprocket tooth spacing, locked out. Fix or call: stretched chain is replaced, often with the sprocket, so the new chain is not run on a hooked tooth.</p>
<h3>Debris, a broken roller, or a binding dolly</h3>
<p>What you will see: the chain tightens in one spot, or you hear a knock each revolution. How to check: locked out, walk the trough for rags, broken rollers, and a dolly that will not roll. Fix or call: clearing a visible obstruction may be in your daily routine. If the chain still slips, call.</p>
<h3>Drive problems</h3>
<p>What you will see: the motor runs but the chain does not pull, the hydraulic unit is hot or noisy, or the gearbox sounds rough. How to check: do not open a live hydraulic or electrical panel. Note what you hear and whether the level sight, if you have one, is in range. Fix or call: hydraulic drives and gearboxes are rebuilt in-house. Book <a href="/car-wash-equipment-repair/">car wash equipment repair</a>.</p>
<h2>Should you grease the conveyor chain?</h2>
<p>Kleen-Rite’s roller-chain article says to flush the chain and rollers and not to grease them, because grease holds grit. Follow your manufacturer’s manual. If the manual and that article disagree, the manual for your conveyor wins.</p>
<h2>A simple conveyor check</h2>
<p>Plans are customized for each wash, including how often we visit. There is no fixed tier. A <a href="/car-wash-maintenance-plans/">preventive maintenance plan</a> can hold this list. It is a check, not a numbered how-to for repairs:</p>
<ul class="ticks"><li>Flush the trough.</li><li>Look for stuck or broken rollers.</li><li>Listen at the drive.</li><li>Look at the take-up.</li><li>Inspect the sprocket teeth with the conveyor locked out.</li><li>If the drive is hydraulic, check the level and whether it is running hot, without opening the system.</li><li>Write down what you found.</li></ul>
<h2>When to call a technician</h2>
<p>Call when slipping comes back after the take-up is set, when the sprocket or chain needs replacement, when the drive or hydraulics need diagnosis, or when anything structural is damaged. Most car wash faults need a technician on site to diagnose properly, so the usual route is to book a visit.</p>
{coverage()}
<p><a href="/car-wash-equipment-repair/">Car wash equipment repair</a> · <a href="/urgent-car-wash-repair/">Urgent repair</a> if the tunnel is down.</p>
<h2>Example from the field</h2>
<aside class="soon"><b>Real example.</b> Tunnel conveyor drive repair, Orange County (Laguna Niguel), March 2024. No customer name, and no extra diagnosis beyond the job type on file.</aside>
{H["confirm"]("an owned photo of the March 2024 Laguna Niguel conveyor-drive repair")}
<h2>Climate note for Southwest and Hawaii washes</h2>
<p>Heat can raise hydraulic oil temperature. Cold mornings in high desert and mountain areas can leave ice in a trough. Salt air along the California coast and in Hawaii speeds corrosion on chain and hardware. See the <a href="/service-area/">service area</a> for how on-site work is arranged. No counts are attached to that.</p>
{faq_html(faqs)}
{reach(H, "Conveyor acting up?")}
{related([
    ("/equipment/tunnel/", "Tunnel car wash equipment repair"),
    ("/car-wash-equipment-repair/", "Car wash equipment repair"),
    ("/urgent-car-wash-repair/", "Urgent repair"),
    ("/car-wash-maintenance-plans/", "Maintenance plans"),
    ("/service-area/", "Service area"),
    ("/contact/", "Request service"),
    ("/blog/", "All guides"),
    ("/blog/repair-or-replace-car-wash-equipment/", "Repair or replace"),
    ("/blog/car-wash-tunnel-cleaning-program/", "Tunnel and bay cleaning"),
])}
{sources([
    ("https://blog.kleen-ritecorp.com/car-wash-tunnel-roller-chain-maintenance/", "Kleen-Rite: tunnel roller chain maintenance"),
    ("https://ncswash.com/car-wash-tunnel-maintenance-the-what-when-and-why/", "NCS: tunnel maintenance, the what, when and why"),
    ("https://innovateitcarwash.com/troubleshooting-conveyor-chain-slips/", "InnovateIT: troubleshooting conveyor chain slips"),
    ("https://www.osha.gov/control-hazardous-energy", "OSHA: control of hazardous energy"),
    ("https://www.carwashmag.com/checks-and-balances-avoid-downtime-with-preventative-maintenance/", "Auto Laundry News: checks and balances"),
    ("https://www.carwash.com/preventative-maintenance-wash-equipment/", "Professional Carwashing: preventative maintenance"),
])}
"""
    return body, faqs


def post_detect(H):
    faqs = [
        ("Can I reset the photo-eye myself?",
         "You can clean the lens and the reflector and look for a beam that is obviously blocked, with the bay safe and the equipment stopped the way your manual describes. Alignment, wiring, and any reset that the manual does not spell out belong to a technician."),
        ("Why does it work in the morning and not in the afternoon?",
         "Sun glare on a photo-eye is a known pattern in bright Southwest bays, and heat can shift a marginal sensor. Treat that as a clue, not a diagnosis. If it keeps happening, book a visit."),
        ("Why does it start with no car in the bay?",
         "A sensor or loop that reads “vehicle” with an empty bay is a fault, not a quirk to live with. Keep the bay closed if the gantry moves when it should not, and book a technician."),
        ("Do you repair touchless and soft-touch in-bay automatics from any brand?",
         "Yes, all major brands, touchless and soft-touch. Named examples: " + esc(BRANDS_LINE) + " " + TM),
        ("Do you come to my state?",
         "On-site repair is centered on Southern California. Elsewhere in the Southwest United States and Hawaii we provide full site management and on-site service by arrangement. Travel charges apply. See the <a href=\"/service-area/\">service area</a>."),
    ]
    body = f"""
<h2>First, a short triage</h2>
<p>Stay out of the path of the gantry. These are look-and-read checks, not repairs:</p>
<ol class="ticks"><li>Read the controller or screen for a fault code, and write it down.</li><li>See whether the pay station shows the wash as paid or started. If it does not, the bay may be waiting on payment rather than on a sensor. See <a href="/equipment/controllers-pay-stations/">controllers and pay stations</a>.</li><li>Look for something in the way: a hose, a brush, debris, or a gantry that is not parked at home.</li><li>Clean the sensor lenses and reflectors. Film, water, and mineral spots block eyes.</li><li>Power-cycle only if your manufacturer’s procedure says to. Do not invent a reset.</li></ol>
<p>Stop there if the bay is still wrong. Most car wash faults need a technician on site to diagnose properly, so the usual route is to book a visit. We do not troubleshoot one-off callers over the phone.</p>
<h2>Photo-eyes and vehicle sensors</h2>
<p>Dirt, chemical film, hard-water spotting, a bumped bracket, and sun glare at one time of day are the usual reasons an eye stops seeing the car. Operators on car wash forums describe the same sequence: clean, check alignment, then look at wiring if it is still dead. Glare is worth noting in a bright Southwest bay. Do not adjust a live eye while the gantry can move.</p>
<h2>Ground loops and loop detectors</h2>
<p>A loop that detects with no car, or that misses cars at random, is often a cracked slab, a cut wire, or a failed detector. Operators describe that pattern when a proximity or loop input stops reading. Cutting a loop or chasing a wire in the concrete is technician work, not a bay-side fix.</p>
<h2>Proximity sensors, treadles, and positioning</h2>
<p>Ultrasonic or proximity sensors, treadles, and the signs that tell the driver where to stop all have to agree. A car parked short, a stuck treadle, or a sensor aimed at the wrong height will look like “it will not see the car.” Look for the obvious mis-park. Leave the adjustment to a technician. The equipment page is <a href="/equipment/in-bay-automatic/">in-bay automatic service and repair</a>.</p>
<h2>When it is not the sensor</h2>
<p>The pay station, the controller, or the wiring between them can withhold the start even when the eyes are clean. If the screen never shows a paid wash, start with the pay station. If it shows paid and the gantry still will not move, the fault is downstream. That is <a href="/equipment/controllers-pay-stations/">controller and pay station</a> work.</p>
<h2>Prevent the repeat fault</h2>
<p>Clean lenses on a rhythm that matches your volume, re-check alignment after any hit in the bay, and keep spot-free rinse from laying mineral film on the eyes. <a href="/equipment/water-reclaim-ro/">Water, reclaim and RO</a> service is the equipment side of that film. A <a href="/car-wash-maintenance-plans/">maintenance plan</a> sets the visit rhythm for your wash. There is no fixed package.</p>
<h2>When to call a technician</h2>
<p>Call for any electrical or loop work, any fault that returns after the lenses are clean, or a gantry that is unsafe to move. If the machine moves when it should not, keep the wash closed. <a href="/urgent-car-wash-repair/">Urgent repair</a> is the page for a bay that is down.</p>
<h2>Example from the field</h2>
{H["confirm"]("a confirmed vehicle-detection job, region and month and year only. The confirmed in-bay job on file is a limit fault in Los Angeles County (Calabasas), October 2026. That record does not describe a detection fault, so it is not used as this article’s example. No example is invented here.")}
{faq_html(faqs)}
{reach(H, "Bay not seeing cars?")}
{coverage()}
{related([
    ("/equipment/in-bay-automatic/", "In-bay automatic repair"),
    ("/urgent-car-wash-repair/", "Urgent repair"),
    ("/equipment/controllers-pay-stations/", "Controllers and pay stations"),
    ("/equipment/water-reclaim-ro/", "Water, reclaim and RO"),
    ("/car-wash-maintenance-plans/", "Maintenance plans"),
    ("/car-wash-equipment-repair/", "Car wash equipment repair"),
    ("/service-area/", "Service area"),
    ("/contact/", "Request service"),
    ("/blog/", "All guides"),
    ("/blog/conveyor-chain-slipping/", "Conveyor chain slipping"),
    ("/blog/repair-or-replace-car-wash-equipment/", "Repair or replace"),
])}
{sources([
    ("https://www.carwashforum.com/threads/your-troubleshooting-protocol.10720/", "CarWashForum: troubleshooting protocol"),
    ("https://www.reddit.com/r/carwash/comments/l0lgpu/xpt_proximity_sensor_not_reading/", "Operators discussing a proximity sensor that stopped reading"),
    ("https://www.reddit.com/r/carwash/comments/mogo0g/", "Operators discussing in-bay detection"),
    ("https://www.carwash.com/troubleshooting-common-carwash-problems/", "Professional Carwashing: troubleshooting common problems"),
    ("https://www.osha.gov/control-hazardous-energy", "OSHA: control of hazardous energy"),
])}
"""
    return body, faqs


def post_clean(H):
    faqs = [
        ("How often should I clean the tunnel?",
         "It depends on car count, soil, and season. A rinse and a look at opening and closing, plus a deeper clean when film and sludge build up, is the shape of a program. We do not state a fixed interval."),
        ("Can cleaning chemicals damage the equipment?",
         "Yes, if the product does not match the surface. Stainless, aluminum, glass, plastics, rubber, coated parts, wash media, and electronics do not all take the same cleaner. Read the label and the equipment maker’s guidance."),
        ("Do cleaning chemicals affect the reclaim system?",
         "They can. Everything you spray ends up in the pit. Check that the cleaner is compatible with the filters, pumps, and any biological treatment before you use it."),
        ("Do you clean tunnels and bays?",
         "Yes. Car Wash Management does tunnel and bay cleaning and supplies the soaps and chemicals for it from the Car Wash Labs (Car Wash Laboratories) line. Whether that covers every wash type as a standalone visit is still open: see the note below."),
        ("Do you sell car wash cleaning chemicals?",
         "Yes. We supply soaps and chemicals from the Car Wash Labs (Car Wash Laboratories) line. See <a href=\"/chemistry/\">car wash cleaning chemicals</a>."),
        ("Do you come to my state?",
         "On-site work is centered on Southern California. Elsewhere in the Southwest United States and Hawaii we provide <a href=\"/car-wash-management-services/\">full site management</a> and on-site service by arrangement. Travel charges apply."),
    ]
    body = f"""
<h2>Why cleaning is equipment maintenance</h2>
<p>Buildup around a conveyor, bearings, and gears adds wear. Scale and film on applicators and manifolds block nozzles and throw chemical off target. Dirty sensors cause faults, which is the same failure mode as a <a href="/blog/conveyor-chain-slipping/">slipping conveyor chain</a> or an <a href="/blog/in-bay-automatic-wont-detect-vehicle/">in-bay automatic that will not detect the car</a>. Sludge plus overspray is also a slip hazard. Professional Carwashing &amp; Detailing’s October 12, 2026 piece on a cleaning maintenance program makes that equipment case. We are not copying it, and we are not attaching any numbers to it.</p>
<h2>Where buildup collects</h2>
{table(["Area", "What collects"], [
    ["Tunnel entrance", "Silt and road grime"],
    ["Mid-tunnel and high pressure", "Reclaim mist on walls, lights, and arches"],
    ["Finishing", "Wax and protectant overspray"],
    ["Exit", "Film blown around by the dryers, including tire-dressing residue"],
    ["Pit", "Whatever the tunnel washed off, plus the cleaner"],
    ["In-bay and self-serve", "Film on eyes, nozzles, brushes, and bay walls"],
])}
<h2>A schedule your staff can follow</h2>
<p>Columns are types of work, not a promise of how often we visit. We set a cleaning schedule wash by wash.</p>
{table(["Every shift", "Periodic deep clean", "As conditions require"], [
    ["Rinse arches, applicators, and the exit area", "Walls, arches, and dryer housings", "After a dust storm, a heavy soil week, or a chemical change"],
    ["Look at sensors and nozzles", "Cloth and brush media, within the maker’s guidance", "When film or sludge shows up early"],
    ["Note leaks, worn media, and blocked screens", "A planned pass with the cleaner matched to each surface", "Before a busy holiday weekend if the wash is already dirty"],
])}
{H["confirm"]("whether to publish any cleaning frequency. Until then, the schedule is set wash by wash and no interval is stated as ours.")}
<h2>A basic wall and equipment wash-down</h2>
<ol class="ticks"><li>Wear the protection the product calls for: gloves, eye protection, and a respirator where the label or SDS says so.</li><li>Read the SDS. Never mix chemicals.</li><li>Lock out moving equipment before anyone is near it. OSHA’s <a href="https://www.osha.gov/control-hazardous-energy" rel="noopener">lockout/tagout</a> page is the reference.</li><li>Apply cleaner from the bottom up.</li><li>Let it dwell for the time on the product label. We do not publish our own dwell time.</li><li>Agitate with a long-handled brush where the label allows it.</li><li>Rinse from the top down.</li></ol>
<h2>Match the chemistry to the surface</h2>
<p>Stainless, aluminum, tinted or treated glass, plastics, rubber, coated surfaces, friction media, and electronics do not take the same product. The old approach of bathing everything in one strong acid is a good way to etch metal and haze plastic. Check the equipment maker’s guidance and the label. Car Wash Management supplies soaps and chemicals from the Car Wash Labs (Car Wash Laboratories) line, including chemistry for tunnel and bay cleaning. See <a href="/chemistry/">chemistry</a>. We supply that line rather than claiming the formulas are manufactured here.</p>
{H["confirm"]("names of specific Car Wash Labs cleaning products, if any should be listed")}
<h2>Pits, drains, and reclaim</h2>
<p>Cleaner ends up in the pit. Check it against reclaim filtration, pumps, and any biological treatment. Drive pit cleanouts by car count and conditions, not by a calendar we have not set. In California we service and install reclaim systems. See <a href="/equipment/water-reclaim-ro/">water, reclaim and RO</a>.</p>
<p>Pits and reclaim tanks can be permit-required confined spaces. Do not send staff in without the right procedure. OSHA’s <a href="https://www.osha.gov/confined-spaces" rel="noopener">confined spaces</a> page is the reference. We do not say we pump pits or do tank cleanouts.</p>
{H["confirm"]("whether Car Wash Management performs pit, trench, or reclaim-tank cleanouts. That work is left out until you say so.")}
<h2>Seasonal notes for the Southwest and Hawaii</h2>
<p>Summer heat and sun dry chemistry faster and favor algae in damp corners. Desert dust and monsoon storms load pits, filters, and sensors. Hard water lays scale on nozzles and applicators. Higher country sees salt and sand in winter. Hawaii adds salt air. See the <a href="/service-area/">service area</a>. No statistics are attached.</p>
<h2>Cleaning that catches problems early</h2>
<p>People who rinse cloth and clean arches are the first to see worn media, a blocked screen, a dirty sensor, or a leak. Put a “report it” line on the checklist. A cleaning crew is not a repair crew. If something looks worn, loose, or leaking, stop and have a technician look. <a href="/car-wash-equipment-repair/">Car wash equipment repair</a> and <a href="/urgent-car-wash-repair/">urgent repair</a> are the repair paths.</p>
<h2>Have us handle it</h2>
<p>Car Wash Management does tunnel and bay cleaning and supplies the soaps and chemicals for it. We can build cleaning into a <a href="/car-wash-maintenance-plans/">maintenance plan</a> made for your wash, and our technicians fix what they find. Most car wash faults need a technician on site to diagnose properly, so the usual route is to book a visit.</p>
{coverage()}
{H["confirm"]("whether cleaning is offered on its own or as a one-time deep clean, or only inside a maintenance plan or full site management")}
{H["confirm"]("whether cleaning is offered for tunnels, in-bay automatics, and self-serve bays, or only for some of those")}
{H["confirm"]("a real cleaning job for a Real example box: region and month and year only. None is on file, so none is written here.")}
{H["confirm"]("an owned photo of a tunnel or bay being cleaned, and of Car Wash Labs cleaning product in use. Pending-clearance chemistry photos are not used.")}
{faq_html(faqs)}
{reach(H, "Want a cleaning program built for your wash?")}
<p>The request form does not yet have a Cleaning type. Use Maintenance plan or Other until that is added.</p>
{H["confirm"]("whether the request form should add a Cleaning option")}
{related([
    ("/car-wash-maintenance-plans/", "Cleaning built into a maintenance plan"),
    ("/chemistry/", "Car wash cleaning chemicals"),
    ("/equipment/tunnel/", "Tunnel equipment"),
    ("/equipment/in-bay-automatic/", "In-bay automatic equipment"),
    ("/equipment/self-serve/", "Self-serve equipment"),
    ("/equipment/chemical-dosing/", "Chemical dosing"),
    ("/equipment/water-reclaim-ro/", "Water, reclaim and RO"),
    ("/equipment/", "Equipment hub"),
    ("/car-wash-equipment-repair/", "Car wash equipment repair"),
    ("/urgent-car-wash-repair/", "Urgent repair"),
    ("/car-wash-management-services/", "Full site management"),
    ("/service-area/", "Service area"),
    ("/contact/", "Request service"),
    ("/blog/conveyor-chain-slipping/", "Conveyor chain slipping"),
    ("/blog/in-bay-automatic-wont-detect-vehicle/", "In-bay detection"),
    ("/blog/repair-or-replace-car-wash-equipment/", "Repair or replace"),
    ("/blog/self-serve-no-soap-all-bays/", "No soap in every self-serve bay"),
])}
{sources([
    ("https://www.carwash.com/developing-cleaning-maintenance-program-carwash/", "Professional Carwashing & Detailing, October 12, 2026: developing a cleaning maintenance program"),
    ("https://www.carwash.com/fall-cleaning/", "Professional Carwashing & Detailing, October 26, 2026: fall cleaning"),
    ("https://www.osha.gov/control-hazardous-energy", "OSHA: control of hazardous energy"),
    ("https://www.osha.gov/confined-spaces", "OSHA: confined spaces"),
])}
"""
    return body, faqs


def post_soap(H):
    faqs = [
        ("Why do I have rinse but no soap in every bay?",
         "When every bay rinses and none of them soaps, the fault is usually something the bays share: the tank, the proportioner, the concentrate, or power to the soap solenoids. One dead bay points at that bay’s solenoid, check valve, pump, or line."),
        ("Why does my soap tank keep filling with water?",
         "A rising tank with no customers usually means water is getting in: a failing solenoid or check valve, or a proportioner that is leaking back. Have a technician find which one. Do not keep running a tank that is being diluted."),
        ("Do you service self-serve car washes?",
         "Yes. Car Wash Management services self-serve bays and equipment from all major brands. See <a href=\"/equipment/self-serve/\">self-serve car wash repair</a>. Named examples: Cat Pumps, Grundfos, and AXEON. " + TM),
        ("Can you talk me through it over the phone?",
         "Most car wash faults need a technician on site to diagnose properly, so the usual route is to book a visit. The safe checks above are worth doing first. If they do not restore soap, call or text to book a technician. We do not offer phone troubleshooting for one-off callers."),
        ("Do you come to my state?",
         "On-site repair is centered on Southern California. Elsewhere in the Southwest United States and Hawaii we provide <a href=\"/car-wash-management-services/\">full site management</a> and on-site service by arrangement. Travel charges apply. See the <a href=\"/service-area/\">service area</a>."),
    ]
    body = f"""
<h2>Every bay, or just one?</h2>
<p>That split is the first clue. All bays means a shared part. One bay means that bay’s own solenoid, check valve, pump, or line.</p>
{table(["What you see", "Where to look first"], [
    ["Every bay has rinse and no high-pressure soap", "Soap tank, proportioner, concentrate, common solenoid wiring, controller output"],
    ["One bay is dry of soap and the others are fine", "That bay’s solenoid, check valve, pump, or line"],
])}
<h2>Safe checks an owner can do</h2>
<p>Looking and a bucket. No panel, no manifold, no pump work.</p>
<ol class="ticks"><li>Is there concentrate in the drum, and is the pickup line and foot valve under the liquid and clear of sludge?</li><li>Is the soap tank at its normal level? Has it risen overnight with no traffic? A rising tank is water getting in.</li><li>Operators on Car Wash Forum describe a quick test: add a small amount of straight concentrate to the soap tank, run high-pressure soap in one bay for a short moment, and see if soap appears. If it does, the mix is too weak and the proportioner is the problem, not the high-pressure pump. Follow the chemical label and the SDS. That test is their report, not our instruction.</li><li>Is the water supply to the proportioner on? The manual for one common unit lists a flowing minimum of 25 PSI before it will draw concentrate. Check the manual for your unit. We are not naming that unit here.</li><li>Did anything change: a new chemical, a new metering tip, a valve that was opened, a freeze, or a power outage?</li></ol>
<p>Stop there. Opening an electrical panel, a pump room that is under pressure, or a solenoid manifold is technician work. Lock equipment out before anyone works on it. OSHA’s <a href="https://www.osha.gov/control-hazardous-energy" rel="noopener">lockout/tagout</a> page is the reference.</p>
{H["confirm"]("whether the common name hydrominder may be used once for the chemical proportioner. It is not used on this page until you say so.")}
<h2>Common causes, in plain terms</h2>
<h3>The proportioner is not drawing</h3>
<p>A clogged foot valve, a scaled or clogged metering tip, a tip that does not match the product, low water pressure, or a worn diaphragm will all stop the draw. Hard water in the Southwest speeds scale. We are explaining the fault, not telling you which tip to install.</p>
<h3>Rinse water is leaking back into the soap tank</h3>
<p>A failing solenoid or check valve can let rinse water flow backward and dilute the soap. Operators report the tank level creeping up overnight as the sign. Finding which valve is technician work.</p>
<h3>Tank outlet valves set wrong</h3>
<p>If the valves under the tank are wide open, some pumps will not pull soap into the line. The correct position depends on the system. A technician should set it. We are not giving a valve position.</p>
<h3>Weak or wrong chemical</h3>
<p>Diluted or mismatched concentrate will rinse like water. Car Wash Management supplies soaps and chemicals from the Car Wash Labs (Car Wash Laboratories) line. See <a href="/chemistry/">chemistry</a>. We supply that line rather than claiming the formulas are manufactured here.</p>
<h3>No power to the soap solenoids</h3>
<p>A lost common wire or a controller output can kill soap in every bay at once while rinse still works. Electrical work is technician-only. See <a href="/equipment/chemical-dosing/">chemical dosing equipment</a>.</p>
<h2>Bought a used self-serve?</h2>
<p>A used wash arrives with unknown settings and worn parts. We start with a full equipment inspection, then replace the damaged parts. A <a href="/car-wash-maintenance-plans/">maintenance plan</a> is customized per wash. The decision guide is <a href="/blog/repair-or-replace-car-wash-equipment/">repair or replace car wash equipment</a>.</p>
<h2>When to call a technician</h2>
<p>Call if soap is still missing after the safe checks, if the tank keeps filling with water, or if the work is electrical, a pump, or the manifold. Most car wash faults need a technician on site to diagnose properly, so the usual route is to book a visit.</p>
{coverage()}
<p>The equipment page is <a href="/equipment/self-serve/">self-serve car wash repair</a>. If the bays are down, see <a href="/urgent-car-wash-repair/">urgent repair</a>.</p>
{H["confirm"]("Coleman Hanna is not on the approved brand list, so it is not named. Say if it should be added to the example list with the trademark line.")}
{H["confirm"]("a real self-serve job for a Real example box: region and month and year only. None is on file, so none is written here.")}
{H["confirm"]("an owned photo of a self-serve equipment room (soap tank, proportioner, pump stand) and of a bay with soap. Stock and manufacturer photos are not used as our work.")}
{faq_html(faqs)}
{reach(H, "No soap in the bays?")}
{related([
    ("/equipment/self-serve/", "Self-serve car wash repair"),
    ("/equipment/chemical-dosing/", "Chemical dosing equipment"),
    ("/chemistry/", "Soaps and chemicals"),
    ("/car-wash-equipment-repair/", "Car wash equipment repair"),
    ("/urgent-car-wash-repair/", "Urgent repair"),
    ("/car-wash-maintenance-plans/", "Maintenance plans"),
    ("/car-wash-management-services/", "Full site management"),
    ("/service-area/", "Service area"),
    ("/contact/", "Request service"),
    ("/blog/", "All guides"),
    ("/blog/repair-or-replace-car-wash-equipment/", "Repair or replace"),
    ("/blog/car-wash-tunnel-cleaning-program/", "Tunnel and bay cleaning"),
])}
{sources([
    ("https://www.carwashforum.com/threads/i-have-a-coleman-hanna-r-o-power-pak-system-with-6-bays-no-soap-coming-out-where-do-i-need-to-start-please-help.27819/", "Car Wash Forum: an owner with no high-pressure soap in six bays"),
    ("https://www.carwashforum.com/threads/hydrominder-issues.19855/", "Car Wash Forum: proportioner backflow and low water pressure"),
    ("https://www.carwashforum.com/threads/no-high-pressure-soap.21934/", "Car Wash Forum: the add-concentrate-to-the-tank test"),
    ("https://www.manualslib.com/manual/1532887/Hydrominder-511.html?page=2", "A proportioner manual’s troubleshooting table, including a 25 PSI flowing minimum"),
    ("https://www.osha.gov/control-hazardous-energy", "OSHA: control of hazardous energy"),
])}
"""
    return body, faqs


POSTS = [
    {"slug": "self-serve-no-soap-all-bays", "title": "Self-Serve Car Wash Has No Soap? | Car Wash Management",
     "desc": "Every self-serve bay has rinse but no soap? Check the shared tank, proportioner, and concentrate first, then book a technician.",
     "h1": "Self-Serve Car Wash Has No Soap in Every Bay? Where to Start", "crumb": "No Soap in Every Bay",
     "lead": "When every bay has rinse but no high-pressure soap, the fault is usually something the bays share: an empty or diluted soap tank, a proportioner that is not drawing, rinse water backing into the tank, outlet valves set wrong, or lost power to the soap solenoids. Check the tank and the chemical first, then call a technician.",
     "image": "nb-28", "image_w": 1200, "category": "Self-serve & vacuums",
     "summary": "Rinse in every bay and no soap usually means a shared tank, proportioner, or solenoid feed, not six separate pumps.",
     "service": ("/equipment/self-serve/", "Self-serve car wash repair"),
     "equip": ("/equipment/chemical-dosing/", "Chemical dosing equipment"),
     "about": "Self-serve car wash soap systems", "build": post_soap},
    {"slug": "car-wash-tunnel-cleaning-program", "title": "Car Wash Tunnel Cleaning Program | Car Wash Management",
     "desc": "How to set up tunnel and bay cleaning that protects equipment: daily rinses, deeper cleans, and chemistry matched to each surface.",
     "h1": "How to Set Up a Tunnel and Bay Cleaning Program That Protects Your Equipment", "crumb": "Tunnel and Bay Cleaning",
     "lead": "A useful tunnel and bay cleaning program has three layers: a rinse and a look at opening and closing, a deeper clean of walls, arches, applicators, dryers, and sensors when film builds up, and pit and drain attention driven by car count and season. Match the chemistry to each surface, and keep it compatible with the reclaim system.",
     "image": "nb-01", "image_w": 1200, "category": "Water, reclaim & chemistry",
     "summary": "Cleaning is equipment maintenance: film blocks nozzles and sensors, and the chemistry has to match the surface and the reclaim system.",
     "service": ("/car-wash-maintenance-plans/", "Cleaning built into a maintenance plan"),
     "equip": ("/chemistry/", "Car wash cleaning chemicals"),
     "about": "Car wash tunnel and bay cleaning", "build": post_clean},
    {"slug": "in-bay-automatic-wont-detect-vehicle", "title": "In-Bay Automatic Won't Detect the Car? | Car Wash Management",
     "desc": "In-bay automatic will not detect the car? Check photo-eyes, sensors, the ground loop, and the start signal. Safe checks first, then call a tech.",
     "h1": "In-Bay Automatic Will Not Detect the Car? Causes and Fixes", "crumb": "In-Bay Detection",
     "lead": "If the in-bay automatic will not see the car, start with a fault code, a paid wash on the pay station, anything blocking the bay, and dirty photo-eye lenses. If those checks do not restore a normal start, book a technician. Most of these faults need someone on site.",
     "image": "nb-16", "image_w": 1200, "category": "In-bay automatic",
     "summary": "A bay that will not start is often a dirty or glaring photo-eye, a loop fault, or a pay station that never sent the start.",
     "service": ("/urgent-car-wash-repair/", "Urgent in-bay repair"),
     "equip": ("/equipment/in-bay-automatic/", "In-bay automatic equipment"),
     "about": "In-bay automatic vehicle detection", "build": post_detect},
    {"slug": "conveyor-chain-slipping", "title": "Car Wash Conveyor Chain Slipping? | Car Wash Management",
     "desc": "A slipping car wash conveyor chain usually means tension, a worn sprocket, chain stretch, debris, or a weak drive. Lock it out, then check each one.",
     "h1": "Why Is My Car Wash Conveyor Chain Slipping?", "crumb": "Conveyor Chain Slipping",
     "lead": "Most conveyor slipping comes down to five things: take-up tension, worn drive-sprocket teeth, a stretched chain, debris or a binding roller in the trough, or a drive that is losing power. Lock out the conveyor before anyone inspects it.",
     "image": "nb-12", "image_w": 1200, "category": "Tunnel & conveyor",
     "summary": "A chain that slips under load is usually tension, a hooked sprocket, stretch, debris in the trough, or a drive that is losing power.",
     "service": ("/car-wash-equipment-repair/", "Car wash equipment repair"),
     "equip": ("/equipment/tunnel/", "Tunnel car wash equipment repair"),
     "about": "Car wash conveyor chain", "build": post_chain},
    {"slug": "repair-or-replace-car-wash-equipment", "title": "Repair or Replace Car Wash Equipment? | Car Wash Management",
     "desc": "How to decide whether to repair, rebuild, or replace car wash equipment: failure patterns, parts, downtime, and what an inspection should cover.",
     "h1": "Should You Repair or Replace Your Car Wash Equipment?", "crumb": "Repair or Replace",
     "lead": "Start with a full equipment inspection. Repair, and replace the damaged parts, when the failure is isolated, parts are available, and the rest of the unit is sound. Replace the whole system when breakdowns repeat across subsystems, parts are obsolete, or the unit cannot run the wash packages, payment options, or throughput you need.",
     "image": "nb-04", "image_w": 1600, "category": "Planning: replace, install, buy",
     "summary": "Inspect first. Repair isolated failures when parts exist. Replace when the failures are widespread or the parts and controls are at the end of the line.",
     "service": ("/car-wash-equipment-installation/", "Car wash equipment installation"),
     "equip": ("/equipment/", "Equipment we service"),
     "about": "Car wash equipment replacement", "build": post_repair},
]


def blog_hub(H):
    cards = []
    for i, spec in enumerate(POSTS, 1):
        cards.append(f"""<article class="post-card"><p class="eyebrow">{esc(spec["category"])}</p>
<h2><a href="/blog/{spec["slug"]}/">{esc(spec["h1"])}</a></h2>
<p>{esc(spec["summary"])}</p>
<p class="byline">Published {MODIFIED}</p>
<p>Related service: <a href="{spec["service"][0]}">{esc(spec["service"][1])}</a></p></article>""")
    equip = [
        ("/equipment/", "All equipment we service"),
        ("/equipment/in-bay-automatic/", "In-bay automatic"),
        ("/equipment/tunnel/", "Tunnel"),
        ("/equipment/self-serve/", "Self-serve"),
        ("/equipment/vacuums/", "Vacuums"),
        ("/equipment/controllers-pay-stations/", "Controllers and pay stations"),
        ("/equipment/chemical-dosing/", "Chemical dosing"),
        ("/equipment/water-reclaim-ro/", "Water, reclaim and RO"),
    ]
    body = f"""<p class="byline">By the Car Wash Management Service Team</p>
<p>Wash down? Call or text <a href="tel:{H["tel"]}">{H["phone"]}</a>, {H["hours"]}. We aim to respond quickly. <a href="/urgent-car-wash-repair/">Urgent repair</a> · <a href="/contact/">Request service</a>.</p>
{"".join(cards)}
<h2>Browse by equipment</h2>
<ul class="ticks">{"".join(f'<li><a href="{h}">{esc(t)}</a></li>' for h, t in equip)}</ul>
<h2>Need it fixed, not explained?</h2>
<ul class="ticks"><li><a href="/car-wash-equipment-repair/">Car wash equipment repair</a></li>
<li><a href="/car-wash-equipment-installation/">Car wash equipment installation</a></li>
<li><a href="/car-wash-maintenance-plans/">Maintenance plans</a></li>
<li><a href="/service-area/">Service area</a></li>
<li><a href="/chemistry/">Soaps and chemicals</a> from the Car Wash Labs (Car Wash Laboratories) line</li></ul>
<div class="note"><h2>Who writes these guides</h2><p>Written by the Car Wash Management Service Team. We started out washing cars in the back of a Honda Civic, and our repair work grew through car washes at Marine Corps Base Hawaii. Today we repair, supply and install car wash equipment for all major brands across the Southwest United States and Hawaii.</p></div>
{reach(H, "Want a technician instead of a guide?")}
"""
    graph = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": H["base"] + "/blog/#page", "url": H["base"] + "/blog/",
         "name": "Car Wash Equipment Guides", "publisher": {"@id": H["base"] + "/#org"},
         "mainEntity": {"@type": "ItemList", "itemListElement": [
             {"@type": "ListItem", "position": i, "url": H["base"] + f"/blog/{spec['slug']}/", "name": spec["h1"]}
             for i, spec in enumerate(POSTS, 1)]}},
    ]}
    return H["inner"]("/blog/", "Guides",
                      "Car Wash Equipment Guides & Answers | Car Wash Management",
                      "Practical answers on car wash equipment repair, replacement and maintenance for tunnels, in-bay automatics and self-serve bays.",
                      "Car Wash Equipment Guides",
                      "Straight answers on keeping car wash equipment running: troubleshooting, repair-or-replace decisions, and maintenance for tunnels, in-bay automatics, and self-serve bays.",
                      body, None, "Request service or a quote", (graph,))


def render_post(H, spec):
    path = f"/blog/{spec['slug']}/"
    extra_body, faqs = spec["build"](H)
    content = (f'<p class="byline">By the Car Wash Management Service Team · November 11, 2026</p>'
               + H["own_gallery"]([spec["image"]])
               + "<p>This photo is from our work. It is not a photo of a specific example on this page.</p>"
               + extra_body)
    return H["inner"](path, spec["crumb"], spec["title"], spec["desc"], esc(spec["h1"]), spec["lead"],
                      content, None, "Request service or a quote",
                      (posting_ld(H, spec, path, faqs), faq_ld(faqs)),
                      parent=("/blog/", "Guides"))


# ---------- state pages ----------

def state_cards():
    cards = []
    for spec in STATES:
        cards.append(f'<a class="state-card" href="{spec["path"]}"><b>{esc(spec["name"])}</b><p>{esc(spec["card"])}</p><span>Read the {esc(spec["name"])} page</span></a>')
    return f'<div class="state-grid">{"".join(cards)}</div>'


def render_state(H, spec):
    body, faqs = spec["build"](H)
    svc = H["service_ld"](spec["path"], spec["service_name"], spec["service_type"])
    svc["description"] = spec["service_desc"]
    svc["areaServed"] = {"@type": "State", "name": spec["name"], "containedInPlace": {"@type": "Country", "name": "United States"}}
    return H["inner"](spec["path"], spec["name"], spec["title"], spec["desc"], spec["h1"], spec["lead"],
                      body, None, "Request service or a quote", (svc, faq_ld(faqs)),
                      parent=("/service-area/", "Service Area"))


def california(H):
    faqs = [
        ("Does California’s 60 percent recycling rule apply to my wash?",
         "California Water Code sections 10950 through 10953 apply to in-bay and conveyor car washes that were permitted and constructed after January 1, 2014. They must recycle at least 60 percent of wash and rinse water, or use recycled water from a supplier for at least 60 percent. Cities and counties can be stricter. Read the statute and check your permit. This is not legal advice."),
        ("Is a self-serve wash exempt from that 60 percent rule?",
         "The statute’s recycling requirement, as summarized from Water Code section 10951, exempts self-service washes. Confirm that against the code and your local rules before you rely on it."),
        ("Can you service my reclaim system so it keeps doing its job?",
         "In California we service and install reclaim systems. Whether a given system is meeting a percentage is a measurement question for your equipment and your permit. We do not certify compliance."),
        ("Do you install reclaim on an existing wash?",
         "In California we service and install reclaim systems. Travel charges apply outside the normal on-site area; we will tell you before we book. See <a href=\"/equipment/water-reclaim-ro/\">water, reclaim and RO</a>."),
        ("Do you work outside Southern California?",
         "On-site repair is centered on Southern California: Los Angeles and Orange County, the Inland Empire, and San Diego County. Elsewhere in California we provide full site management and on-site service by arrangement."),
    ]
    body = f"""
<h2>How we work in California</h2>
<p>On-site repair and fix work is centered on Southern California: Los Angeles and Orange County, the Inland Empire, and San Diego County. For the rest of California, full site management and on-site service by arrangement, with travel charges. We do not list other California metros as on-site repair areas.</p>
{reach(H, "Southern California wash down or due for service?")}
<h2>What we do on site</h2>
<ul class="ticks"><li><a href="/car-wash-equipment-repair/">Car wash equipment repair</a> for all major brands</li>
<li><a href="/car-wash-equipment-installation/">Installation and replacement</a> of equipment and components</li>
<li><a href="/car-wash-maintenance-plans/">Maintenance plans</a> customized per wash</li>
<li><a href="/equipment/water-reclaim-ro/">Water, reclaim and RO</a></li>
<li><a href="/chemistry/">Soaps and chemicals</a> from the Car Wash Labs line</li>
<li><a href="/car-wash-management-services/">Full site management</a> where you want the whole wash run for you</li></ul>
{brand_sentence()}
<h2>The 60 percent water rule</h2>
<p>California Water Code sections 10950 through 10953, from AB 2230, are the home for this rule on our site. In short: an in-bay or conveyor car wash permitted and constructed after January 1, 2014 has to recycle at least 60 percent of its wash and rinse water, or take at least 60 percent of that water as recycled water from a supplier. Self-service washes are exempt in the statute. A city or county can require more.</p>
<p>The practical equipment side is the reclaim system: filters, pumps, and tanks that have to keep working if the wash is counting on them. Coastal salt air corrodes frames, fasteners, and electrical boxes. Inland heat raises hydraulic and pump temperatures and dries chemistry faster. Either climate still needs the reclaim kept up if the permit depends on it. We service and install reclaim systems in California. We do not certify that a wash meets the percentage.</p>
<p>Read <a href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=WAT&amp;sectionNum=10951" rel="noopener">Water Code section 10951</a> and the definitions in <a href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=WAT&amp;sectionNum=10950" rel="noopener">section 10950</a>. Industry explainers of reclaim choices are at Professional Carwashing, linked below. This page is not a legal opinion.</p>
<h2>Examples from the field</h2>
<aside class="soon"><b>Real example.</b> Tunnel conveyor drive repair, Orange County (Laguna Niguel), March 2024.</aside>
<aside class="soon"><b>Real example.</b> In-bay automatic limit fault, Los Angeles County (Calabasas), October 2026.</aside>
<aside class="soon"><b>Real example.</b> RO booster pump supply and install, Inland Empire, October 2023. The region is the Inland Empire, not a city.</aside>
{H["confirm"]("owned photos of these three California jobs. No customer names are added.")}
{faq_html(faqs)}
{coverage()}
{related([
    ("/car-wash-equipment-repair/", "Car wash equipment repair"),
    ("/car-wash-equipment-installation/", "Installation and replacement"),
    ("/car-wash-maintenance-plans/", "Maintenance plans"),
    ("/equipment/", "Equipment we service"),
    ("/equipment/water-reclaim-ro/", "Water, reclaim and RO"),
    ("/chemistry/", "Chemistry"),
    ("/car-wash-management-services/", "Full site management"),
    ("/service-area/", "All states we cover"),
    ("/contact/", "Request service"),
    ("/blog/", "Equipment guides"),
])}
{sources([
    ("https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=WAT&sectionNum=10951", "California Water Code section 10951"),
    ("https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=WAT&sectionNum=10950", "California Water Code section 10950"),
    ("https://www.carwash.com/choosing-right-water-recycling-system/", "Professional Carwashing: choosing a water recycling system"),
    ("https://www.carwash.com/carwash-water-reclaim-technologies/", "Professional Carwashing: reclaim technologies"),
])}
"""
    return body, faqs


def arizona(H):
    faqs = [
        ("Does Phoenix hard water damage car wash equipment?",
         "Phoenix’s 2025 water quality report lists total hardness of roughly 172 to 302 mg/L, about 10 to 17.6 grains per gallon, which the report’s range puts in hard to very hard water. That hardness is what scales nozzles, heaters, and RO membranes. How often to service them depends on your water and your volume. We do not publish an interval."),
        ("Will my wash stay open during a Tucson water restriction?",
         "Tucson Code section 27-95 limits vehicle washing, when that section is in effect, to facilities that recirculate wash water. Check the current declaration with the city. We do not track declarations for you on this page."),
        ("How often should RO membranes be serviced in the desert?",
         "It depends on the water and the volume. Heat, dust, and hard water all shorten the comfortable gap between filter changes. We will not invent a number of weeks."),
    ]
    body = f"""
<h2>How we work in Arizona</h2>
<p>Arizona is full site management plus on-site service by arrangement. We do not claim a local crew, a local office, or statewide on-site repair. Phoenix, Tucson, and Flagstaff are context for the water and the weather, not a promise that a technician lives there.</p>
{reach(H, "Running a wash in Arizona?")}
{coverage()}
<h2>Water and equipment</h2>
<p>Phoenix’s 2025 water quality report lists total hardness of roughly 172 to 302 mg/L (about 10 to 17.6 grains per gallon). Hard water scales nozzles, heater coils, and RO membranes, so spot-free rinse and reclaim need more attention than they do on soft water. The report is linked below. Verify the current edition with the city.</p>
<p>Tucson Code section 27-95 says that when that restriction is in effect, vehicle washing is prohibited except at facilities with wash-water recirculation. If your wash depends on staying open in a shortage, the recirculation equipment has to actually run. Oro Valley, in the Tucson area, has been reported by Tucson Local Media as requiring car washes to reuse 70 percent of their water. That figure is the news report’s, not a number we measured. Verify it with the town.</p>
<h2>Heat, dust, and the high country</h2>
<p>Summer heat loads motors, hydraulic oil, and control cabinets, and ultraviolet light ages hoses, brushes, and plastics. Monsoon dust and storms load filters, sensors, and reclaim solids. Flagstaff and the high country add freeze risk that Phoenix does not have. Full site management can include scheduling the filter and RO work. The visit itself is on-site by arrangement, and travel is charged.</p>
<h2>Example</h2>
{H["confirm"]("a confirmed full-site-management example in Arizona, region and month and year only. None is on file, so none is invented.")}
{H["confirm"]("keep this Arizona page in the preview. Say if it should come off before any launch.")}
{faq_html(faqs)}
{related([
    ("/car-wash-management-services/", "Full site management"),
    ("/equipment/water-reclaim-ro/", "Water, reclaim and RO"),
    ("/car-wash-equipment-repair/", "Equipment repair"),
    ("/car-wash-maintenance-plans/", "Maintenance plans"),
    ("/service-area/", "Service area"),
    ("/service-area/california/", "Southern California, where on-site repair is centered"),
    ("/contact/", "Request service"),
])}
{sources([
    ("https://www.phoenix.gov/administration/departments/waterservices/water-quality/water-quality-reports.html", "City of Phoenix water quality reports"),
    ("https://codelibrary.amlegal.com/codes/tucson/latest/tucson_az/0-0-0-20697", "Tucson Code section 27-95"),
    ("https://www.tucsonlocalmedia.com/explorernews/car-wash-would-recycle-82-of-water/article_2b4932f8-ae45-11ed-a71d-532661525270.html", "Tucson Local Media report mentioning Oro Valley’s reuse figure"),
])}
"""
    return body, faqs


def nevada(H):
    faqs = [
        ("What are the Las Vegas car wash water rules?",
         "LVVWD service rules and SNWA say commercial vehicle washing is allowed where water goes to the sanitary sewer through approved methods, or with a high-pressure, low-volume sprayer using under 10 gallons per vehicle. Read the service rules before you rely on a paraphrase."),
        ("Can you help us qualify as a Water Smart Car Wash?",
         "No. The SNWA Water Smart Car Wash program is voluntary and run by SNWA. Car Wash Management does not offer help qualifying a wash for it. The program’s own page says reclaimed water must return to the sanitary sewer, and that mobile washes need a commercial reclaim system."),
        ("Why does spot-free rinse still spot in Las Vegas?",
         "LVVWD describes Las Vegas Valley water as very hard, about 280 mg/L or 16 grains per gallon in its water quality summary. Hard water is why spot-free systems and softeners work hard there. The fix is equipment diagnosis, not a phone guess."),
    ]
    body = f"""
<h2>How we work in Nevada</h2>
<p>Nevada is full site management plus on-site service by arrangement. Las Vegas Valley and Reno-Sparks are mentioned so the water rules make sense. They are not a claim that we keep a technician in either place.</p>
{reach(H, "Own a wash in Nevada?")}
{coverage()}
<h2>Las Vegas water rules</h2>
<p>Commercial vehicle washing in the Las Vegas Valley is tied to where the water goes. LVVWD’s service rules and SNWA’s conservation pages allow it when discharge goes to the sanitary sewer through approved methods, or when a high-pressure, low-volume sprayer uses under 10 gallons per vehicle. If the sewer connection or the reclaim return is down, the wash has a rules problem as well as an equipment problem.</p>
<p>SNWA’s Water Smart Car Wash program is voluntary. Its page says reclaimed water must be returned to the sanitary sewer, and mobile washes need a commercial reclaim system. We can talk about reclaim equipment. We do not help a wash qualify for that program.</p>
<p>LVVWD’s water quality summary lists Las Vegas Valley water at about 280 mg/L, about 16 grains per gallon. That is the utility’s figure. It is why nozzles, solenoids, and heaters scale, and why RO and softener demand is heavy.</p>
<h2>Example</h2>
{H["confirm"]("a confirmed full-site-management example in Nevada, region and month and year only. None is on file, so none is invented.")}
{H["confirm"]("keep this Nevada page in the preview. Say if it should come off before any launch.")}
{faq_html(faqs)}
{related([
    ("/car-wash-management-services/", "Full site management"),
    ("/equipment/water-reclaim-ro/", "Water, reclaim and RO"),
    ("/equipment/in-bay-automatic/", "In-bay automatic equipment"),
    ("/service-area/", "Service area"),
    ("/contact/", "Request service"),
])}
{sources([
    ("https://www.lvvwd.com/assets/pdf/service-rules-chapter10.pdf", "LVVWD service rules, chapter 10"),
    ("https://www.snwa.com/conservation/understand-laws-ordinances/index.html", "SNWA: laws and ordinances"),
    ("https://www.snwa.com/apps/watersmart-car-wash/index.cfml?lang=en", "SNWA Water Smart Car Wash program"),
    ("https://www.lvvwd.com/assets/pdf/water-quality-summary-las-vegas-valley.pdf", "LVVWD Las Vegas Valley water quality summary"),
])}
"""
    return body, faqs


def new_mexico(H):
    faqs = [
        ("Can wash water running onto the street get me cited in Albuquerque?",
         "The Albuquerque Bernalillo County Water Utility Authority water waste ordinance treats washing vehicles so that water flows onto adjacent property or the public right-of-way as water waste. It also counts water that causes ice on adjacent property or sidewalks as waste, and it requires shutoff nozzles on hoses used for vehicle washing. Read the ordinance."),
        ("Does New Mexico require car wash water recycling?",
         "We did not find a statewide recycling mandate for car washes in the sources used here. Albuquerque’s water conservation strategy lists commercial carwash recycling standards as a measure to evaluate, not as a current mandate. Check the city and county that permitted your wash."),
        ("Do you winterize washes in New Mexico?",
         "No. Car Wash Management does not offer winterizing visits in New Mexico. Freeze and thaw are real at this elevation. Follow the equipment maker’s guidance. We are not publishing a winterizing procedure."),
    ]
    body = f"""
<h2>How we work in New Mexico</h2>
<p>New Mexico is full site management plus on-site service by arrangement. Albuquerque, Las Cruces, and Santa Fe explain the climate. They are not on-site territories.</p>
{reach(H, "Own a wash in New Mexico?")}
{coverage()}
<h2>Runoff and what is not a mandate</h2>
<p>The Albuquerque Bernalillo County Water Utility Authority water waste ordinance treats wash water that reaches a neighbor’s property or the public right-of-way as waste. Water that ices a sidewalk counts too. Hoses used to wash vehicles need shutoff nozzles. That is a drainage and nozzle fact for self-serve and hand bays as much as for tunnels.</p>
<p>Albuquerque’s conservation strategy lists “commercial carwash recycling standards” as something to evaluate. It is not, in that document, a current statewide or citywide recycling mandate. Do not read this page as saying your wash must hit a percentage. Check locally.</p>
<h2>High desert, sun, and freeze</h2>
<p>Albuquerque’s elevation means freeze and thaw, strong sun, and dust. Ice at an exit is both a safety problem and, under the ordinance above, a water-waste problem if the water leaves your property. We do not offer winterizing visits in New Mexico. On-site visits for other work are by arrangement, and travel is charged.</p>
<h2>Example</h2>
{H["confirm"]("a confirmed full-site-management example in New Mexico, region and month and year only. None is on file, so none is invented. No winterizing visit will be offered.")}
{H["confirm"]("keep this New Mexico page in the preview. Say if it should come off before any launch.")}
{faq_html(faqs)}
{related([
    ("/car-wash-management-services/", "Full site management"),
    ("/equipment/self-serve/", "Self-serve equipment"),
    ("/equipment/water-reclaim-ro/", "Water, reclaim and RO"),
    ("/service-area/", "Service area"),
    ("/contact/", "Request service"),
])}
{sources([
    ("https://www.abcwua.org/wp-content/uploads/Ordinances_PDFs/Section_4_Water_Waste_Reduction_Ordinance.pdf", "ABCWUA water waste ordinance"),
    ("https://codelibrary.amlegal.com/codes/albuquerque/latest/albuquerque_nm_res/0-0-0-21957", "Albuquerque conservation strategy"),
])}
"""
    return body, faqs


def utah(H):
    faqs = [
        ("What is St. George’s 35-gallon car wash rule?",
         "St. George City Code section 10-17A-15 says car washes must be plumbed for wash-water and RO-reject recycling at construction. From July 1, 2022 through June 30, 2027, the code says no car wash is permitted unless it averages 35 gallons or less of culinary water per car, and recycling systems must be installed and used. Washington County’s water efficiency standards describe the same plumbing and the same 35-gallon average. Read both before you design or buy."),
        ("Do Salt Lake City car washes need a wastewater permit?",
         "Salt Lake City’s pretreatment program says car and truck washes that discharge non-domestic wastewater must submit a Commercial and Industrial User Questionnaire and may need a discharge permit. Ask the city. We do not file it for you from this page."),
        ("How do I keep a Utah wash running in winter?",
         "Wasatch Front winters load doors, heaters, exit ice, and salt and grit in the pit. St. George is a desert heat problem more than a deep-freeze problem. We do not publish a winterizing package or a response time. On-site work is by arrangement."),
    ]
    body = f"""
<h2>How we work in Utah</h2>
<p>Utah is full site management plus on-site service by arrangement. The Wasatch Front (Salt Lake City, Ogden, Provo) and St. George have different water rules and different winters. Neither is an on-site territory.</p>
{reach(H, "Own a wash in Utah?")}
{coverage()}
<h2>St. George’s gallons-per-car rule</h2>
<p>St. George City Code section 10-17A-15 requires car washes to be plumbed for wash-water and RO-reject recycling when they are built. For the window from July 1, 2022 through June 30, 2027, the code says a car wash is not permitted unless it averages 35 gallons or less of culinary water per car, and the recycling system has to be installed and kept in use. Washington County’s October 2023 water efficiency standards say the same thing about plumbing and the 35-gallon average. If you are buying or building in Washington County, those two documents are the ones to read. We do not track your gallons for you.</p>
<h2>Salt Lake discharge, and two winters</h2>
<p>Salt Lake City’s pretreatment program requires a questionnaire, and may require a discharge permit, for car and truck washes sending non-domestic wastewater to the sewer. That is a paperwork fact for a tunnel or in-bay that discharges process water.</p>
<p>Along the Wasatch Front, winter means freeze protection, door and heater equipment, ice at the exit, and salt and grit in the reclaim and the pit. St. George’s problem is desert heat and the gallons rule above, not a Wasatch winter. A maintenance rhythm has to follow the site. We do not sell a named winter package.</p>
<h2>Example</h2>
{H["confirm"]("a confirmed full-site-management example in Utah, region and month and year only. None is on file, so none is invented.")}
{H["confirm"]("keep this Utah page in the preview. Say if it should come off before any launch.")}
{faq_html(faqs)}
{related([
    ("/car-wash-management-services/", "Full site management"),
    ("/equipment/water-reclaim-ro/", "Water, reclaim and RO"),
    ("/equipment/tunnel/", "Tunnel equipment"),
    ("/service-area/", "Service area"),
    ("/contact/", "Request service"),
])}
{sources([
    ("https://stgeorge.municipal.codes/Code/10-17A-15", "St. George City Code section 10-17A-15"),
    ("https://www.wcwcd.gov/wp-content/uploads/2023/10/WaterEfficiency-Standards-Oct-2023.pdf", "Washington County water efficiency standards, October 2023"),
    ("https://www.slc.gov/utilities/wastewater-pretreatment/", "Salt Lake City wastewater pretreatment"),
])}
"""
    return body, faqs


def texas(H):
    faqs = [
        ("What does San Antonio require for car wash water reuse?",
         "San Antonio’s code, chapter 34, says vehicle washes that began operating on or after January 1, 2006 and use conveyor, touchless, or rollover in-bay equipment must reuse at least 50 percent of water from previous rinses. RO concentrate must be reused. The wash needs catchment and an oil-water separator. Self-serve wands are limited to 3 gallons per minute. Read the ordinance."),
        ("Is there a separate San Antonio recognition program?",
         "SAWS runs a WaterSaver Car Wash program with registration and best-practice materials, including nozzle replacement and leak repair. That is SAWS’s program. We do not enroll washes in it from this page."),
        ("What is El Paso’s gallons-per-car rule?",
         "El Paso’s code, chapter 15.13, says a new commercial car wash permitted after June 1, 2002 has to document use of no more than 50 gallons per vehicle. Confirm the current code section before you build."),
    ]
    body = f"""
<h2>How we work in Texas</h2>
<p>Texas is full site management plus on-site service by arrangement. El Paso and San Antonio are here because their ordinances are specific. This page does not claim statewide on-site coverage, and it does not claim a crew in Houston or Dallas.</p>
{reach(H, "Own a wash in Texas?")}
{coverage()}
<h2>San Antonio reuse, and El Paso’s cap</h2>
<p>San Antonio’s plumbing and water code chapter 34 sets a reuse rule for vehicle washes that began on or after January 1, 2006 and use a conveyor, a touchless machine, or a rollover in-bay: at least 50 percent of the water from previous rinses must be reused, RO concentrate must be reused, and the site needs catchment and an oil-water separator. Self-serve wands are limited to 3 gallons per minute. SAWS also publishes a WaterSaver Car Wash program and best practices. Those are the utility’s materials.</p>
<p>El Paso’s chapter 15.13 says a new commercial car wash permitted after June 1, 2002 must document that it uses no more than 50 gallons per vehicle. West Texas dust and hard water are the equipment backdrop. Gulf humidity around Houston is a corrosion backdrop. Both are qualitative. We are not citing a utility hardness number for Texas.</p>
<h2>Example</h2>
{H["confirm"]("a confirmed full-site-management example in Texas, region and month and year only. None is on file, so none is invented.")}
{H["confirm"]("keep this Texas page in the preview. Say if it should come off before any launch.")}
{faq_html(faqs)}
{related([
    ("/car-wash-management-services/", "Full site management"),
    ("/equipment/self-serve/", "Self-serve equipment"),
    ("/equipment/water-reclaim-ro/", "Water, reclaim and RO"),
    ("/equipment/in-bay-automatic/", "In-bay automatic equipment"),
    ("/service-area/", "Service area"),
    ("/contact/", "Request service"),
])}
{sources([
    ("https://library.municode.com/TX/san_antonio/codes/code_of_ordinances?nodeId=PTIICO_CH34WASE_ARTIVDRMAWACORE_DIV1REAC", "San Antonio Code chapter 34, water reuse"),
    ("https://www.saws.org/conservation/commercial-programs-rebates/watersaver-car-wash-program/car-wash-best-management-practices/", "SAWS WaterSaver car wash best practices"),
    ("https://library.municode.com/tx/el_paso/codes/code_of_ordinances?nodeId=TIT15PUSE_CH15.13WACO", "El Paso Code chapter 15.13"),
])}
"""
    return body, faqs


def hawaii(H):
    faqs = [
        ("How do I protect equipment from salt air?",
         "Salt air and humidity attack frames, fasteners, electrical enclosures, and sensors. Rinsing salt off, keeping enclosures closed, and catching corrosion early are the practical habits. We do not publish a coatings specification."),
        ("Where can Honolulu car wash water go?",
         "The City and County of Honolulu says vehicle wash water may not enter streets or storm drains. The city’s storm-water page for automotive businesses describes citations for discharges to the storm drain. Confirm the current penalty schedule with the city. Wash water belongs in the sewer or in a reclaim system, not in the gutter."),
        ("Do you service neighbor islands?",
         "On-site service in Hawaii is by arrangement, including neighbor islands. Travel charges apply, and we will tell you before we book. We handle parts and jobs in Hawaii. We do not keep a local parts inventory in Hawaii."),
    ]
    body = f"""
<h2>How we work in Hawaii</h2>
<p>Hawaii is full site management plus on-site service by arrangement. Oahu, including Honolulu, and the neighbor islands are all by arrangement. We do not claim island-wide on-site repair or a technician on every island.</p>
<p>Car Wash Management started out washing cars in the back of a Honda Civic, and its car wash repair work grew through Marine Corps Base Hawaii. That is the origin, not a claim of current work on any base.</p>
{reach(H, "Own a wash in Hawaii?")}
{coverage()}
<h2>Where the water goes</h2>
<p>The City and County of Honolulu tells businesses that vehicle wash water may not enter streets or storm drains, and its storm-water page for automotive businesses describes enforcement, including citations. The city’s industrial wastewater survey says car washes, self-serve, automated, or full-service, are required to install a water recycling system and a two-way valve if they sit where rainwater could enter the system. That sentence is the city’s, from the survey form. Confirm it with Environmental Services before you build or remodel. The Board of Water Supply also publishes voluntary conservation guidance. We are not quoting a savings percentage from it.</p>
<h2>Salt air and parts</h2>
<p>Salt air corrodes frames, fasteners, electrical enclosures, and sensors. Stainless and coatings help, and they are not magic. Island logistics mean parts take time. We handle parts and jobs in Hawaii. We do not keep a local parts stock or inventory in Hawaii. Plan critical spares with that in mind. We will not invent a stocking list here.</p>
{H["confirm"]("how parts should be ordered for Hawaii jobs, beyond the confirmed line that we handle parts and jobs and do not keep a local inventory")}
<h2>Example</h2>
{H["confirm"]("a confirmed full-site-management example in Hawaii, region and month and year only. None is on file, so none is invented.")}
{H["confirm"]("keep this Hawaii page in the preview. Say if it should come off before any launch.")}
{faq_html(faqs)}
{related([
    ("/car-wash-management-services/", "Full site management"),
    ("/car-wash-equipment-repair/", "Equipment repair"),
    ("/equipment/in-bay-automatic/", "In-bay automatic equipment"),
    ("/about/", "About Car Wash Management"),
    ("/service-area/", "Service area"),
    ("/contact/", "Request service"),
])}
{sources([
    ("https://www.honolulu.gov/swq/info-resources/businesses/automotive/", "Honolulu storm water: automotive businesses"),
    ("https://www.honolulu.gov/env/wp-content/uploads/sites/29/2025/05/IWDP_NON_Food_Service_Establishment_Survey_Application.pdf", "Honolulu industrial wastewater survey for non-food businesses"),
    ("https://www.boardofwatersupply.com/media/vl1lc42r/your-water-conservation-board-of-water-supply-booklet-2025-0624.pdf", "Honolulu Board of Water Supply conservation booklet"),
])}
"""
    return body, faqs


STATES = [
    {"path": "/service-area/california/", "name": "California",
     "title": "Southern California Car Wash Repair | Car Wash Management",
     "desc": "On-site car wash equipment repair centered on Southern California, plus maintenance, installation, and the 60% water recycling rule.",
     "h1": "Car Wash Equipment Repair and Service in Southern California",
     "lead": "Car Wash Management repairs, maintains, supplies, and installs car wash equipment for all major brands, with on-site repair centered on Southern California.",
     "card": "On-site repair centered on Southern California, plus what the 60 percent recycling rule means for reclaim equipment.",
     "service_name": "Car wash equipment repair, maintenance and installation in Southern California",
     "service_type": "Car wash equipment repair",
     "service_desc": "On-site car wash equipment repair is centered on Southern California. Elsewhere in California, full site management and on-site service are by arrangement.",
     "build": california},
    {"path": "/service-area/arizona/", "name": "Arizona",
     "title": "Arizona Car Wash Site Management | Car Wash Management",
     "desc": "Full site management for Arizona car washes, with on-site visits by arrangement. Phoenix hard water, Tucson water limits, and desert heat.",
     "h1": "Car Wash Site Management in Arizona",
     "lead": "Full site management for Arizona washes, with on-site equipment service by arrangement. Heat, dust, and hard water are the local equipment problems.",
     "card": "Full site management, with Phoenix hard water and Tucson’s recirculation limit explained. On-site visits by arrangement.",
     "service_name": "Car wash full site management and on-site service by arrangement in Arizona",
     "service_type": "Car wash site management",
     "service_desc": "Full site management for Arizona car washes, with on-site service by arrangement. No statewide on-site repair claim.",
     "build": arizona},
    {"path": "/service-area/nevada/", "name": "Nevada",
     "title": "Nevada Car Wash Site Management | Car Wash Management",
     "desc": "Full site management for Nevada car washes, on-site by arrangement, plus Las Vegas sewer-discharge rules and very hard water.",
     "h1": "Car Wash Site Management in Nevada",
     "lead": "Full site management for Nevada washes, with on-site visits by arrangement. Las Vegas sewer and hardness rules are the local equipment constraints.",
     "card": "Full site management for Las Vegas-area operators, plus sewer-discharge rules. We do not offer Water Smart qualification help.",
     "service_name": "Car wash full site management and on-site service by arrangement in Nevada",
     "service_type": "Car wash site management",
     "service_desc": "Full site management for Nevada car washes, with on-site service by arrangement. No statewide on-site repair claim.",
     "build": nevada},
    {"path": "/service-area/new-mexico/", "name": "New Mexico",
     "title": "New Mexico Car Wash Site Management | Car Wash Management",
     "desc": "Full site management for New Mexico car washes, on-site by arrangement. Albuquerque runoff rules, high-desert dust, and no winterizing visits.",
     "h1": "Car Wash Site Management in New Mexico",
     "lead": "Full site management for New Mexico washes, with on-site service by arrangement. Runoff rules and high-desert weather are the local constraints.",
     "card": "Full site management, Albuquerque runoff rules, and no winterizing visits. On-site work by arrangement.",
     "service_name": "Car wash full site management and on-site service by arrangement in New Mexico",
     "service_type": "Car wash site management",
     "service_desc": "Full site management for New Mexico car washes, with on-site service by arrangement. Winterizing visits are not offered.",
     "build": new_mexico},
    {"path": "/service-area/utah/", "name": "Utah",
     "title": "Utah Car Wash Site Management | Car Wash Management",
     "desc": "Full site management for Utah car washes, on-site by arrangement, including St. George’s 35-gallon rule and Wasatch Front winters.",
     "h1": "Car Wash Site Management in Utah",
     "lead": "Full site management for Utah washes, with on-site service by arrangement. St. George’s water cap and Wasatch Front winters are different problems.",
     "card": "Full site management, St. George’s 35-gallon rule, and Wasatch Front winters. On-site visits by arrangement.",
     "service_name": "Car wash full site management and on-site service by arrangement in Utah",
     "service_type": "Car wash site management",
     "service_desc": "Full site management for Utah car washes, with on-site service by arrangement. No statewide on-site repair claim.",
     "build": utah},
    {"path": "/service-area/texas/", "name": "Texas",
     "title": "Texas Car Wash Site Management | Car Wash Management",
     "desc": "Full site management for Texas car washes, on-site by arrangement, plus San Antonio’s 50% reuse rule and El Paso’s 50-gallon limit.",
     "h1": "Car Wash Site Management in Texas",
     "lead": "Full site management for Texas washes, with on-site service by arrangement. San Antonio and El Paso write gallons and reuse into the local code.",
     "card": "Full site management, San Antonio’s 50 percent reuse rule, and El Paso’s 50-gallon limit for new washes.",
     "service_name": "Car wash full site management and on-site service by arrangement in Texas",
     "service_type": "Car wash site management",
     "service_desc": "Full site management for Texas car washes, with on-site service by arrangement. No statewide on-site repair claim.",
     "build": texas},
    {"path": "/service-area/hawaii/", "name": "Hawaii",
     "title": "Hawaii Car Wash Site Management | Car Wash Management",
     "desc": "Full site management across Hawaii, with on-site service by arrangement. Salt air, Honolulu discharge rules, and parts planning without a local stock.",
     "h1": "Car Wash Site Management in Hawaii",
     "lead": "Full site management across Hawaii, with on-site service by arrangement. Salt air, Honolulu’s discharge rules, and island parts timing are the constraints.",
     "card": "Full site management, salt air, and Honolulu discharge rules. Parts and jobs are handled here. No local parts inventory.",
     "service_name": "Car wash full site management and on-site service by arrangement in Hawaii",
     "service_type": "Car wash site management",
     "service_desc": "Full site management for Hawaii car washes, with on-site service by arrangement. No local parts inventory is claimed.",
     "build": hawaii},
]

STATE_PATHS = [s["path"] for s in STATES]
POST_PATHS = [f"/blog/{s['slug']}/" for s in POSTS]


def services_page(H):
    faqs = [
        ("What is included in full site management?",
         "Accounting, operations, employment (hiring and firing), and repairs. That is the confirmed scope. A fuller weekly description is not published yet."),
        ("What does it cost?",
         "A custom quote after a site review. No prices, fees, or package rates are listed."),
        ("Is there a minimum site size?",
         "No minimum site size or wash type is set on this page."),
        ("How often do owners get reports?",
         "Regular reporting to owners. No cadence is stated, because none has been set."),
        ("Do you help with Nevada Water Smart or New Mexico winterizing?",
         "No. We do not offer help qualifying a wash for SNWA’s Water Smart program, and we do not offer winterizing visits in New Mexico."),
    ]
    body = f"""
<h2>What full site management covers</h2>
<p>Car Wash Management handles what it takes to run the car wash: accounting, operations, employment (hiring and firing), and repairs. The phrase we use is full site management.</p>
<p>Repair work still has a home on <a href="/car-wash-equipment-repair/">car wash equipment repair</a>. Chemistry we supply is the Car Wash Labs (Car Wash Laboratories) line, on the <a href="/chemistry/">chemistry</a> page. A <a href="/car-wash-maintenance-plans/">maintenance plan</a> can sit inside the operation or stand next to it. Plans are customized. There is no fixed tier.</p>
<h2>How a quote works</h2>
<p>Custom quote after a site review. This page has no prices, no fee schedule, and no contract terms. There is no minimum site size or wash type.</p>
<p>Owners get regular reporting. The contents of that report, and how often it goes out, are not set here.</p>
{H["confirm"]("what a report to owners contains, and any cadence you want named. None is stated until you set it.")}
{H["confirm"]("which states you will take full-site-management clients in. The pages exist for California, Arizona, Nevada, New Mexico, Utah, Texas, and Hawaii.")}
<h2>Where this is offered</h2>
{coverage()}
<p>On-site repair remains centered on Southern California. Read the <a href="/service-area/">service area</a> and the state pages before you assume a visit.</p>
<h2>What this page does not claim</h2>
<ul class="ticks"><li>No managed-site example, until one is confirmed.</li>
<li>No help qualifying a wash for SNWA’s Water Smart Car Wash program.</li>
<li>No winterizing visits in New Mexico.</li>
<li>Installation stays the plain line already used on the site: we supply and install equipment.</li></ul>
{H["confirm"]("a confirmed managed site: region and month and year only, with no customer name. None is on file, so none is invented.")}
{H["confirm"]("the rest of the full-site-management brief. The standalone brief file was missing, so this page is a scaffold from the confirmed facts only.")}
{faq_html(faqs)}
{reach(H, "Want the whole wash run, not only a repair call?")}
{related([
    ("/service-area/", "Service area"),
    ("/service-area/california/", "Southern California repair"),
    ("/car-wash-equipment-repair/", "Equipment repair"),
    ("/car-wash-equipment-installation/", "Installation and replacement"),
    ("/car-wash-maintenance-plans/", "Maintenance plans"),
    ("/chemistry/", "Chemistry"),
    ("/contact/", "Request service"),
    ("/about/", "About"),
    ("/blog/", "Guides"),
])}
"""
    svc = H["service_ld"]("/car-wash-management-services/", "Full car wash site management", "Car wash site management")
    svc["description"] = "Full site management for car wash owners: accounting, operations, employment, and repairs. Custom quote after a site review."
    return H["inner"]("/car-wash-management-services/", "Full Site Management",
                      "Full Car Wash Site Management | Car Wash Management",
                      "Full site management for car wash owners and investors: accounting, operations, employment, and repairs. Custom quote after a site review.",
                      "Full Car Wash Site Management",
                      "Car Wash Management runs the wash for owners and investors: accounting, operations, employment, and repairs. The quote is custom, after a site review.",
                      body, None, "Request a site review", (svc, faq_ld(faqs)))


def register(pages, H):
    pages["/blog/"] = lambda: blog_hub(H)
    for spec in POSTS:
        pages[f"/blog/{spec['slug']}/"] = (lambda spec=spec: render_post(H, spec))
    for spec in STATES:
        pages[spec["path"]] = (lambda spec=spec: render_state(H, spec))
    pages["/car-wash-management-services/"] = lambda: services_page(H)


def _check_lengths():
    rows = [
        ("Car Wash Equipment Guides & Answers | Car Wash Management",
         "Practical answers on car wash equipment repair, replacement and maintenance for tunnels, in-bay automatics and self-serve bays.",
         "/blog/"),
        ("Full Car Wash Site Management | Car Wash Management",
         "Full site management for car wash owners and investors: accounting, operations, employment, and repairs. Custom quote after a site review.",
         "/car-wash-management-services/"),
    ]
    for spec in POSTS:
        rows.append((spec["title"], spec["desc"], "/blog/" + spec["slug"] + "/"))
    for spec in STATES:
        rows.append((spec["title"], spec["desc"], spec["path"]))
    for title, desc, path in rows:
        if len(title) > 60 or len(desc) > 158:
            raise SystemExit(f"length {path} title={len(title)} desc={len(desc)}")


_check_lengths()
