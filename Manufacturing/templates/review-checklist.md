# <prefix> — Stage review checklist (Reviewer)

Short checklist; details are in the relevant `rules/` section. Write findings in the `REVIEW_LOG.md` format and report the result as PASS / REWORK / BLOCKED.

## Schematic (rules/04, SCH)
- [ ] Pinout and footprint match the datasheet (SCH-02, VER-01)
- [ ] Power tree, decoupling, filters (SCH-03, SCH-04)
- [ ] Termination, pull-ups, ESD, strapping pins (SCH-05)
- [ ] Constraints and differential pairs marked (SCH-06); DNP/0 Ω options marked (SCH-07)
- [ ] ERC clean or exceptions justified (VER-02)

## PCB (rules/02, 04, 05)
- [ ] G0.5 decisions applied (outline, stack-up, ring, silkscreen PCB-17…21)
- [ ] Layout: reference layout, input protection, switching loop, crystal (LAY-08…13)
- [ ] Routing: shortest path, no split planes, power/HV rules (LAY-14…24)
- [ ] SI/PI: decoupling loop, impedance, length/delay matching (LAY-25…29, DIF/HS/RF)
- [ ] Silkscreen without overlaps (LAY-30); DRC clean (VER-02)

## Manufacturing (rules/09)
- [ ] File names match the prefix, each variant has its own BOM/PnP (REL-03)
- [ ] `projectctl.py check-bom` clean; alternate parts checked (DFM-14)
- [ ] Gerber/drill layers and board outline correct (VER-04); `_ASSY.pdf` and fab note present
- [ ] The `MANIFEST.sha256` written by the Designer matches the reviewed files; the Manager records the PASS, then `check-release` runs (REL-04)
