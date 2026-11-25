<!-- Part of Hardware-Rules.md (index). Rule IDs are global. -->
## 00B · PCB Intake — Pre-layout technical and mechanical decisions

> **MANDATORY — BEFORE MOVING TO PCB DESIGN (G0.5):** The Manager asks for missing PCB properties based on approved schematic inputs and known mechanical/manufacturing preferences. Do not re-ask decisions already explicitly approved and unchanged; get the user's approval with a single PCB design summary. Until this stage is complete, do not finalize the board outline, stack-up, placement and routing, or start PCB layout.

### A · PCB technology, material and quality

- [ ] **PCB-01** — What is the board's physical construction? Standard rigid, flex, rigid-flex or another special construction?
- [ ] **PCB-02** — Which PCB material/substrate is required? Standard FR-4, special/high-temperature FR-4, aluminum or copper metal-core (MCPCB/IMS), RF laminate, polyimide or other? Do not confuse a metal-core board with mere heavy copper foil.
- [ ] **PCB-03** — Are standard vias/lamination enough, or are HDI, microvias, blind/buried vias, a special layer structure or another special process required? Verify need and cost with the manufacturer; choose standard manufacturing unless needed.
- [ ] **PCB-04** — What is the quality/application class? Standard commercial, industrial, medical, automotive, aerospace/military or another special requirement? Is there a mandatory standard, quality class, test, material or traceability requirement? Do not treat the application class as the same choice as PCB material or construction; verify the manufacturer can meet the related requirements. The choice must be consistent with the INT-47 quality profile; under the Aerospace profile apply section 08.

### B · Board Outline & Mechanical

- [ ] **PCB-05** — What are the size, unit, board shape (rectangle, circle, custom profile), maximum thickness/height, any tolerances and enclosure/STEP reference?
- [ ] **PCB-06** — On a rectangular or cornered board, what will the corners be? **Sharp/square 90° corner, radius (R) rounded corner or chamfer**? Ask the radius value (mm), chamfer size/angle and which corners it applies to; if corner types differ, record them separately.
- [ ] **PCB-07** — What are the mounting hole positions and diameters, PTH/NPTH preference, slots/cutouts, edge clearance, connector orientations, enclosure contact and mechanical keepout areas? Verify inner corners, slots and profile details against the manufacturer's routing capability.
- [ ] **PCB-08** — Are there enclosure/heatsink contact, maximum component Z height, special mechanical or flex/bend constraints? Prefer existing mechanical files.
- [ ] **PCB-14** — In multi-PCB projects, get approval for each board's outline, layers, mounting and chassis ring preference; the boards' placement orientation, relative position, board-to-board distance and any cable routing/mechanical constraints. Ask only for changed or missing board inputs.
- [ ] **PCB-15** — Verify the approved STEP/CAD models of modules and connectors, mating connector match, mating direction, pin 1/orientation, placement and access limits. If a full CAD assembly is required, plan a collision/fit check between boards and related mechanical items.
- [ ] **PCB-16** — If on-board programming or debug is approved, verify placement, Pin 1, access and mechanical clearance requirements for the related connector/pad/fixture. Do not change the method set at G0; in a design with no programming or with off-board programming only, leave this check N/A as appropriate.

### C · Stack-up & Manufacturing

- [ ] **PCB-09** — Is there a special request for manufacturer, standard layer count/stack-up, finished PCB thickness, outer/inner copper weight, solder mask/silkscreen color and surface finish? Otherwise propose the price/performance defaults in section 03 to the user.
- [ ] **PCB-10** — Are controlled impedance, special vias, edge plating/castellation, panelization, stencil, single/double-sided assembly or special manufacturing tolerances required? If so, get only the related manufacturer and user information; apply section 05.

### D · Optional CHASSIS_GND perimeter ring

- [ ] **PCB-11** — Ask the user explicitly: **Do you want a CHASSIS_GND copper ring around the board? (Yes / No)** Do not create the ring automatically even if a chassis exists.
- [ ] **PCB-12** — If the user says yes, propose the default 1.50 mm ring, 3.00 mm via spacing, 0.80 mm via hole and open solder mask from sections 01–02; verify suitability for the selected PCB technology and manufacturer limits. Will the ring connect to main GND or stay separate? If the GND/isolation decision approved in section 00, part C still applies, do not ask again; clarify if missing.
- [ ] **PCB-13** — If the user says no, do not create the ring, its stitching vias or its solder mask opening; other circuit GND polygons and approved chassis connections still apply. If the preference is unclear, do not create the ring and wait for G0.5 approval.

### E · Silkscreen and marking (each question may be deferred per INT-51)

- [ ] **PCB-17** — **Logo/icon:** Will the user's own logo or symbol be placed? Top, bottom or both? The user provides the file (preferably SVG/PNG) and usage rights; no third-party brand is placed without permission.
- [ ] **PCB-18** — **Board code:** Should `<code>-<rev>` (e.g. `DR00627-R01`) be written on the board? Silkscreen or copper; top, bottom or both? Add the date too? Copper text stays away from nets, RF, high-voltage and impedance traces and is DRC-compliant.
- [ ] **PCB-19** — **Connector label:** Should connectors show pin numbers, net names or both? Top, bottom or both?
- [ ] **PCB-20** — **Designator:** Visible or hidden? If visible, size (default: manufacturer minimum, e.g. for JLCPCB ~0.8–1.0 mm height, 0.15 mm stroke) and position (inside the part or at its edge/corner). Hidden designators can shrink the board but make assembly and repair harder; in that case `_ASSY.pdf` is mandatory and designators stay on the Fab/Assembly layer. Remind the user of this risk for hobby/hand assembly and under the Aerospace profile.
- [ ] **PCB-21** — **Signature / easter egg:** If the user wants, a small signature or drawing may be placed. It does not break DRC; it is not placed in RF, antenna, high-voltage or test areas; no inappropriate content. Default off under the Aerospace profile.

### G0.5 · PCB Input Approval

- [ ] Record PCB properties and mechanical decisions in a single short summary in `Project-README.md`.
- [ ] If it conflicts with the schematic, re-evaluate only the affected requirement and design area. If needed, update the G0 approval and the related schematic review.
- [ ] Record the revision of the PCB inputs and the real user approval. Do not regenerate approved, unchanged decisions and verification evidence.
- [ ] Ask again the non-critical decisions deferred under INT-51 (PCB-17…21); if there is no answer, record the safe default.
- [ ] `python scripts/projectctl.py check-layout` must pass before starting layout.
