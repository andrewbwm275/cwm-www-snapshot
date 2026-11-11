# Brands we service and support. Names only: no logos, no Washworld photos, no dealer or partner claims.
# Each brand: (name, anchor id, short equipment label, section text, notes, source_url)
# Washworld is name-only. ICS (Innovative Control Systems) is not DRB. Hanna is listed once, as Coleman Hanna.
P = "(619) 704-7719"

def _b(name, anchor, equip, url, extra=""):
    text = f"We service and support {name} {equip}."
    if extra:
        text += " " + extra
    return (name, anchor, equip, text, "", url)

CATS = [
 ("tunnel", "Tunnel and conveyor equipment", "Tunnel", [
  _b("Sonny's", "sonnys", "tunnel equipment", "https://www.sonnysdirect.com",
     "Conveyors, wraps, arches, and dryers."),
  _b("MacNeil", "macneil", "tunnel equipment", "https://macneilwash.com/equipment/",
     "Conveyors, wraps, brushes, and dryers."),
  _b("Belanger", "belanger", "tunnel and in-bay equipment", "https://www.opwvws.com/brands/belanger/company/about.html",
     "Tunnel equipment and in-bay automatics."),
  _b("Motor City", "motor-city", "tunnel equipment", "https://www.motorcitywashworks.com/systems/car-wash-tunnel-systems/",
     "Motor City Wash Works conveyors, arches, wraps, and dryers."),
  _b("AVW", "avw", "tunnel equipment", "https://avwequipment.com/",
     "AVW Equipment Company conveyors, arches, brushes, and dryers."),
  _b("Tommy", "tommy", "tunnel equipment", "https://tommycarwash.com/",
     "Tommy Car Wash Systems tunnel equipment, including the conveyor developed with AVW."),
  _b("Coleman Hanna", "coleman-hanna", "tunnel, in-bay, and self-serve equipment", "https://colemanhanna.com/about-coleman-hanna/",
     "Hanna tunnel equipment and Coleman in-bay and self-serve equipment are one company. Listed once here."),
  _b("PECO", "peco", "in-bay and tunnel equipment", "https://carwashbizcenter.com/suppliers-directory/car-wash-equipment-manufacturers/",
     "PECO car wash systems."),
  _b("innovateIT", "innovateit", "tunnel equipment", "https://innovateitcarwash.com/troubleshooting-conveyor-chain-slips/",
     "Tunnel equipment and conveyor components."),
  _b("Proto-Vest", "proto-vest", "dryer equipment", "https://www.carwash.com/nrcc-2024-exhibitor-list-floor-plan/",
     "Car wash dryers."),
  _b("Erie Brush", "erie-brush", "brush equipment", "https://www.carwash.com/nrcc-2024-exhibitor-list-floor-plan/",
     "Brushes used on tunnel and in-bay equipment."),
  _b("HECO", "heco", "conveyor gear drives", "https://www.hecogear.com/product/electric_drive.asp",
     "Gear drives and gearboxes used on tunnel conveyors."),
  _b("OPW Vehicle Wash Solutions", "opw", "vehicle wash equipment", "https://www.opwvws.com/",
     "The equipment group that includes PDQ, Belanger, and ICS, which are also listed in their own sections."),
 ]),
 ("in-bay", "In-bay automatic equipment", "In-bay automatic", [
  _b("PDQ", "pdq", "in-bay automatic equipment", "https://www.opwvws.com/brands/pdq/company/about.html",
     "Touch-free and soft-touch in-bay automatics."),
  _b("Ryko", "ryko", "in-bay automatic equipment", "https://ryko.com/systems/",
     "Friction and touch-free in-bay systems."),
  _b("Washworld", "washworld", "in-bay automatic equipment", "https://www.washworldinc.com/about-washworld",
     "Touch-free and soft-touch in-bay automatics. Name only on this site."),
  _b("Mark VII", "mark-vii", "in-bay, tunnel, and self-serve equipment", "https://www.markvii.com",
     "The North American WashTec company. Gantry, tunnel, and self-serve equipment."),
  _b("ISTOBAL", "istobal", "in-bay and tunnel equipment", "https://us.istobal.com/usa/about-us",
     "Rollover and tunnel wash equipment."),
  _b("WashTec", "washtec", "gantry, tunnel, and self-serve equipment", "https://www.carwash.com/partnership-worth-talking-about-mark-vii-washtec/",
     "WashTec AG, the parent of Mark VII."),
  _b("NCS", "ncs", "in-bay and tunnel equipment", "https://www.ncswash.com/car-wash-equipment/",
     "National Carwash Solutions equipment, including lines sold under other names on this page."),
  _b("AUTEC", "autec", "in-bay automatic equipment", "https://autec-carwash.com/our-systems/autec-car-wash-chemicals/",
     "AUTEC Car Wash Systems in-bay automatics. Not the same company as Etowah Valley Equipment."),
 ]),
 ("self-serve", "Self-serve equipment", "Self-serve", [
  _b("D&amp;S", "d-and-s", "self-serve and in-bay equipment", "https://dscarwash.com/support-products/system-add-ons/",
     "D&amp;S self-serve and in-bay equipment."),
  _b("Etowah Valley Equipment", "etowah", "self-serve meters and bay equipment", "https://www.etowahvalleyequipment.com/",
     "Meter boxes and self-serve bay equipment, made in Etowah, North Carolina. Not the same company as AUTEC."),
  _b("Ginsan", "ginsan", "self-serve equipment and vacuums", "https://ginsan-ivs.com/ivs-home/about-ginsan-ivs/",
     "Ginsan and Industrial Vacuum Systems wash equipment, meters, and vacuums."),
  _b("Mosmatic", "mosmatic", "self-serve booms and swivels", "https://www.carwash.com/nrcc-2024-exhibitor-list-floor-plan/",
     "Booms and swivels used on self-serve bays."),
 ]),
 ("vacuums", "Vacuum equipment", "Vacuums", [
  _b("Vacutech", "vacutech", "vacuum equipment", "https://www.ncswash.com/car-wash-vacuum-systems-vacutech/",
     "Central vacuums, separators, arches, and hoses."),
  _b("J.E. Adams", "je-adams", "vacuum equipment", "https://www.jeadams.com",
     "Self-serve and central vacuum equipment."),
 ]),
 ("controllers", "Pay stations and controls", "Pay stations and controls", [
  _b("ICS", "ics", "pay stations and wash controls", "https://www.opwvws.com/company/why-opw.html",
     "Innovative Control Systems payment terminals and wash controls. ICS is not DRB."),
  _b("Kesseltronics", "kesseltronics", "tunnel controls", "https://www.opwvws.com/",
     "Tunnel wash controls."),
  _b("DRB", "drb", "tunnel and site controls", "https://drb.com/in-bay_solutions",
     "DRB Systems site and tunnel controls. The Unitec pay-station line is listed separately."),
  _b("Unitec", "unitec", "pay stations and entry equipment", "https://drb.com/in-bay_solutions",
     "Unitec pay stations and entry equipment, now part of DRB."),
  _b("Hamilton", "hamilton", "payment equipment", "https://www.carwash.com/nrcc-2024-exhibitor-list-floor-plan/",
     "Hamilton Manufacturing payment equipment used at car washes."),
 ]),
 ("water", "Water reclaim, RO, and water treatment", "Water, reclaim, and RO", [
  _b("AXEON", "axeon", "reverse osmosis equipment", "https://www.axeonwater.com/products/systems/membrane/packaged-water-systems/",
     "Reverse osmosis systems, membranes, pumps, and pretreatment."),
  _b("Con-Serv", "con-serv", "water treatment equipment", "https://www.carwash.com/nrcc-2024-exhibitor-list-floor-plan/",
     "Con-Serv Manufacturing water treatment equipment."),
 ]),
 ("pumps", "Pumps, motors, and high-pressure components", "Pumps and motors", [
  _b("Cat Pumps", "cat-pumps", "high-pressure pumps", "https://www.catpumps.com/car-wash-pumps",
     "High-pressure plunger pumps for self-serve, in-bay, and tunnel washes."),
  _b("General Pump", "general-pump", "high-pressure pumps", "https://www.carwash.com/nrcc-2024-exhibitor-list-floor-plan/",
     "High-pressure pumps and pump components."),
  _b("Grundfos", "grundfos", "water, booster, and dosing pumps", "https://www.grundfos.com/us/about-us/cases/grundfos-new-mtre-booster-design-the-perfect-fit-for-car-wash-recycled-water-challenges",
     "Water, booster, and dosing pumps, including pumps on reclaim and chemical delivery."),
 ]),
 ("supplies", "Parts and supplies", "Parts and supplies", [
  ("Dultmeier", "dultmeier", "parts distribution",
   "Dultmeier is a distributor of car wash parts and supplies, not a wash-machine manufacturer. We service and support equipment that uses those parts.",
   "Distributor", "https://www.dultmeier.com/car-wash-equipment-supplies-parts"),
  ("Kleen-Rite", "kleen-rite", "parts and chemical supply",
   "Kleen-Rite is a distributor of car wash parts and chemicals, not a wash-machine manufacturer. We service and support equipment that uses those parts.",
   "Distributor", "https://www.kleen-ritecorp.com/c-1034-car-wash-chemicals.aspx"),
  ("Broadway Equipment", "broadway", "equipment distribution",
   "Broadway Equipment is a distributor, not a wash-machine manufacturer. We service and support equipment sold through that channel.",
   "Distributor", "https://www.broadwayequipment.com/repair-or-replace-your-car-wash-how-to-make-the-right-call/"),
  ("Blendco", "blendco", "car wash chemistry",
   "Blendco makes car wash chemistry, not wash machines. We service and support the dosing equipment that applies chemistry.",
   "Chemistry", ""),
  ("Lustra", "lustra", "car wash chemistry",
   "Lustra is a car wash chemistry line, not a wash machine. We service and support the dosing equipment that applies chemistry.",
   "Chemistry", ""),
 ]),
]

# Short representative list for home, repair, equipment pages, and guides. Full list lives on the brands page.
SHORT = [
 ("Sonny's", "sonnys"),
 ("MacNeil", "macneil"),
 ("Ryko", "ryko"),
 ("Washworld", "washworld"),
 ("Coleman Hanna", "coleman-hanna"),
 ("Cat Pumps", "cat-pumps"),
 ("Unitec", "unitec"),
]
