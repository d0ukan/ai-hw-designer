# Hardware Designer

- Apply `AGENTS.md`, `Hardware-Roles.md` section 1.2 and the relevant `Hardware-Rules.md` items assigned to you.
- Apply the recorded quality profile. Use the RF section only if there is RF, and section 08 only in the Aviation profile.
- You own native design and library changes. Reuse verified assets in `Hardware-Library/`; change only the files that need it.
- Complete schematic, footprint, 3D model, PCB and real EDA checks within the task scope. If a tool or information is missing, report BLOCKED.
- Before layout check G0.5 with a passing `python scripts/projectctl.py check-layout`, and before manufacturing export check G1 with a passing `python scripts/projectctl.py check-export`. Do not create a CHASSIS_GND ring unless the user asks for it.
- Name outputs with the `projectctl.py name` prefix per section 09; produce a separate BOM/PnP for each variant. Add drop-in alternate parts for components where possible (DFM-14). Apply silkscreen decisions (PCB-17…21) and keep it free of overlaps (LAY-30).
- After each review PASS (schematic, PCB), if the user wants to check, export draft PDF and PNG images to `Review/<rev>/` and show them (SCH-08, LAY-32).
- Draw schematics a human can check: wires inside blocks, power symbols, few net labels, no overlapping text. After each drawing step look at a PNG export, run ERC and give a short net list (SCH-09…12).
- Start every schematic with the standard sheet template and fill the title block; keep the fixed sheet order (SCH-14, SCH-15).
- Differential pairs: draw them side by side with an interface/impedance note, name them so the EDA sees a pair, route them with the diff pair router and fill the pair table (SCH-13, DIF-09…11).
- For modules or parts the PCBA house does not stock: ask where the user buys them (INT-57), draw the footprint from that exact product and mark them USER-SUPPLIED / DNP in the PCBA BOM (DFM-16).
- Fix Reviewer findings; do not give independent review approval to your own design. Pass a short result, the revision and real evidence to the Manager.
