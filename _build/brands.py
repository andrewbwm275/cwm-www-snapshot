# Brands we name, grouped by category. Andrew approved these 8 on 2026-10-20:
# Washworld (WashWorld), MacNeil, Unitec/DRB, AXEON, HECO, Ryko, Cat Pumps, Grundfos.
# 2026-10-28: techs service all brands, so copy says "all major brands"; AVW, Motor City, Vacutech and NCS added (names only).
# Name no other brand anywhere on the site beyond these 12.
# Text only: no logos, no photos of Washworld, and no dealer/partner claims.
# Each brand: (name, anchor id, short equipment label, section text, notes, source_url)
P = "(619) 704-7719"
CATS = [
 ("tunnel", "Tunnel &amp; conveyor equipment", "Tunnel", [
  ("MacNeil", "macneil", "tunnel equipment",
   "We service MacNeil tunnel equipment, including conveyors, side washers, wrap-arounds, top brushes, high-pressure systems and dryers. Repairs, parts replacement and scheduled maintenance.",
   "", "https://macneilwash.com/equipment/"),
  ("HECO", "heco", "conveyor gear drives",
   "Conveyor drive trouble? We service and replace HECO gear drives and gearboxes used on tunnel conveyors.",
   "", "https://www.hecogear.com/product/electric_drive.asp"),
  ("AVW", "avw", "tunnel systems",
   "We service AVW tunnel systems, including conveyors, arches, brushes and dryers. Troubleshooting, parts replacement and scheduled maintenance.",
   "AVW Equipment Company", "https://avwequipment.com/"),
  ("Motor City", "motor-city", "tunnel systems",
   f"We repair and service Motor City Wash Works tunnel equipment, including conveyors, arches, wraps and dryers. Call or text {P}.",
   "Motor City Wash Works", "https://www.motorcitywashworks.com/systems/car-wash-tunnel-systems/"),
 ]),
 ("in-bay", "In-bay automatic systems", "In-bay automatic", [
  ("Washworld", "washworld", "in-bay automatic systems",
   f"We repair and service Washworld in-bay automatics, including touch-free and soft-touch systems. Troubleshooting, parts replacement and preventive maintenance. Call or text {P}.",
   "Official spelling is Washworld", "https://www.washworldinc.com/about-washworld"),
  ("Ryko", "ryko", "in-bay automatic systems",
   "Ryko in-bay systems, both friction and touch-free: we troubleshoot, replace worn parts and keep up preventive maintenance.",
   "", "https://ryko.com/systems/"),
  ("NCS", "ncs", "in-bay and tunnel systems",
   "We service NCS (National Carwash Solutions) in-bay automatics and tunnel systems: troubleshooting, worn-part replacement and preventive maintenance.",
   "National Carwash Solutions", "https://www.ncswash.com/car-wash-equipment/"),
 ]),
 ("vacuums", "Vacuum systems", "Vacuums", [
  ("Vacutech", "vacutech", "vacuum systems",
   f"Weak suction or a producer down? We service Vacutech vacuum systems, including turbines, separators, arches and hoses. Call or text {P}.",
   "", "https://www.ncswash.com/car-wash-vacuum-systems-vacutech/"),
 ]),
 ("controllers", "Controllers, pay stations &amp; entry systems", "Controllers &amp; pay stations", [
  ("Unitec/DRB", "unitec-drb", "pay stations, controllers and point-of-sale",
   f"Pay station not taking payments or tunnel controller acting up? We troubleshoot and service Unitec/DRB pay stations, entry units, tunnel controllers and point-of-sale hardware, including parts replacement. Call or text {P}.",
   "", "https://drb.com/in-bay_solutions"),
 ]),
 ("chemistry-water", "Pumps, water, RO &amp; reclaim", "Pumps, water &amp; RO", [
  ("AXEON", "axeon", "reverse osmosis systems",
   f"We service AXEON reverse osmosis systems, including membranes, pumps and pretreatment. Call or text {P}.",
   "", "https://www.axeonwater.com/products/systems/membrane/packaged-water-systems/"),
  ("Cat Pumps", "cat-pumps", "high-pressure pumps",
   "We rebuild, repair and replace Cat Pumps high-pressure plunger pumps for self-serve, in-bay and tunnel washes.",
   "", "https://www.catpumps.com/car-wash-pumps"),
  ("Grundfos", "grundfos", "water pumps",
   f"We service and replace Grundfos water, booster and dosing pumps. Call or text {P}.",
   "", "https://www.grundfos.com/us/about-us/cases/grundfos-new-mtre-booster-design-the-perfect-fit-for-car-wash-recycled-water-challenges"),
 ]),
]
