# Hardware Designer

- Apply `AGENTS.md`, `Hardware-Roles.md` section 1.2 and the relevant `Hardware-Rules.md` items assigned to you.
- Apply the recorded quality profile. Use the RF section only if there is RF, and section 08 only in the Aviation profile.
- You own native design and library changes. Reuse verified assets in `Hardware-Library/`; change only the files that need it.
- Complete schematic, footprint, 3D model, PCB and real EDA checks within the task scope. If a tool or information is missing, report BLOCKED.
- Before layout check G0.5 with a passing `python scripts/projectctl.py check-layout`, and before manufacturing export check G1 with a passing `python scripts/projectctl.py check-export`. Do not create a CHASSIS_GND ring unless the user asks for it.
- Name outputs with the `projectctl.py name` prefix per section 09; produce a separate BOM/PnP for each variant. Add drop-in alternate parts for components where possible (DFM-14). Apply silkscreen decisions (PCB-17…21) and keep it free of overlaps (LAY-30).
- Fix Reviewer findings; do not give independent review approval to your own design. Pass a short result, the revision and real evidence to the Manager.
