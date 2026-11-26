<!-- Part of Hardware-Rules.md (index). Rule IDs are global. -->
## 03 · JLCPCB / PCBWay — DFM & Cost Optimization

> To reduce manufacturing cost, avoid special PCB technologies that are not required; "required" is decided by the INT-48 design target. The defaults below are for standard rigid FR-4 designs and the Hobby/Industrial profile; different material, technology and quality requirements approved in section 00B, and section 08 in the Aerospace profile, take precedence.

| PCB property | Default choice |
| :--- | :--- |
| PCB type | Standard rigid FR-4 |
| PCB thickness | 1.6 mm |
| Layer count | Lowest standard layer count that meets the requirements |
| Outer layer copper thickness | 1 oz |
| Solder mask | Standard green |
| Via type | Mechanically drilled through-hole via |
| Surface finish | Cost-effective standard option; based on pad and contact requirements |
| Stack-up | The manufacturer's standard stack-up options |

- [ ] **DFM-00** — If the user did not ask for medical, military/aviation, HDI, a custom stack-up or a specific manufacturer (Hobby, Industrial; INT-48 target Cost-first or Balanced), base the design on the standard capabilities and standard stack-up of JLCPCB and/or PCBWay; the goal is lowest cost. For a Performance-first target, standard manufacturing is still the first option; but if performance requires it, a special manufacturer, laminate or stack-up is proposed with justification. If there is a special request, section 00B decisions and, if needed, section 08 take precedence.
- [ ] **DFM-01** — Check the current standard manufacturing limits of JLCPCB and PCBWay.
- [ ] **DFM-02** — Keep design rules compatible with the standard manufacturing capabilities of both manufacturers where possible.
- [ ] **DFM-03** — Do not use blind vias, buried vias, microvias, HDI or via-in-pad unless required.
- [ ] **DFM-04** — Define standard signal and GND vias as tented vias. Do not apply this rule to CHASSIS_GND vias that must stay open.
- [ ] **DFM-05** — Unless required, do not choose special laminates, special copper thickness, special solder mask colors or extra manufacturing processes that increase cost.
- [ ] **DFM-06** — Keep footprints, solder mask dams, pad spacing and component placement compatible with PCB/PCBA manufacturing limits.
- [ ] **DFM-07** — Report to the user, with justification, every option outside standard manufacturing that increases cost.
- [ ] **DFM-08** — Select components according to the approved sourcing strategy and assembly method. Verify the real MPN, footprint, stock, lifecycle information and the manufacturer's PCBA assembly capability; state clearly any information that cannot be confirmed.
- [ ] **DFM-09** — If manual assembly or stencil + SMT was chosen, preserve the user-approved package size, pad access and rework requirements. If PCBA was chosen, verify the selected assembly service's component sourcing, package and assembly limits.
- [ ] **DFM-10** — Among options that meet the technical requirements, evaluate the total of BOM, PCB and assembly cost against the INT-48 design target; for a Performance-first target you may choose a more expensive option with measurable benefit. Where suitable, reuse standard, common and previously verified components, footprints and reference circuits. Do not run extensive price research for every standard passive; compare parts that carry significant cost or supply risk.
- [ ] **DFM-11** — For critical or expensive components, evaluate technically suitable, approvable alternatives. Record stock and price information as of the date you could verify it; do not invent unverified price or stock.
- [ ] **DFM-12** — Before researching a new component, check the `Hardware-Library/catalog/` records. Reuse verified symbols, footprints, CAD models and circuit blocks if the exact MPN and validity conditions match. Do not record new or changed assets as VERIFIED before an independent review is complete.
- [ ] **DFM-13** — Record approved off-the-shelf modules and connector pairs in the library with the exact part/revision. Verify that the module's pin/footprint/3D model matches the suitable mating connector and mounting method; do not remodel the same assets in every project.
- [ ] **DFM-14** — **Alternate part:** Where possible, define at least 1 **drop-in alternate part** for each component: same footprint and pinout, equal or better electrical/thermal ratings and temperature grade; preferably a different manufacturer (a true second source). If the part is unavailable, the alternate part must fit directly so assembly can continue. Write the alternate part into the BOM `Alternate MPN` field and the catalog `alternates` field; if none is found, mark it "no alternate". The Reviewer verifies the alternate part's footprint/pinout.
- [ ] **DFM-15** — **Footprint layer map:** Use only the common layer map in footprints: copper, solder mask, paste, silkscreen, courtyard, Fab/Assembly (body and designator) and 3D body. In KiCad, the KiCad Library Convention (KLC) layers apply; in Altium, a single mechanical layer map (or component layer type) defined at project start applies. Do not use custom layers outside the map, so the outputs contain no unnecessary layers (`Hardware-Library/README.md`).
- [ ] **DFM-16** — **User-supplied parts:** A part the PCBA house will not place (module bought locally, not stocked, through-hole by hand) is marked in the BOM: `Supplier` = where the user buys it (local shop/distributor and country), `Notes` = "USER-SUPPLIED — hand assembly". It is DNP in the BOM sent to the assembler (still marked USER-SUPPLIED), omitted from the PnP and listed in `_ASSY.pdf` with its orientation and Pin 1. Where possible the board carries only a stocked female header/socket that the PCBA house places, so the module plugs in. The footprint (pin order, pitch, row spacing, keying) follows the exact product the user buys (INT-57); if two sources differ, pick one and write it on the silkscreen (e.g. module name and Pin 1 / VCC / GND marks).