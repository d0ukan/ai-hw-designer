<!-- Part of Hardware-Rules.md (index). Rule IDs are global. -->
## 01 · PCB manufacturing parameters

The values below are not the manufacturers' absolute manufacturing limits; they are the preferred **default design limits** for standard manufacturing. Last checked: 2026-11-27 (JLCPCB pcb-capabilities and PCBWay capabilities pages, standard tier). Compare with the manufacturer's current page before ordering; if the date is stale, re-check.

| Parameter | Value | Condition |
| :--- | :---: | :--- |
| Minimum trace width | **0.20 mm** | Increase per power and impedance requirements |
| Minimum copper clearance | **0.20 mm** | Increase per voltage and isolation requirements |
| Minimum via hole | **0.30 mm** | Standard through-hole via |
| Minimum via pad diameter | **0.60 mm** | Ensure the annular ring requirement separately |
| Minimum copper-to-board-edge clearance | **0.30 mm** | Routed edge; **0.50 mm** to a V-cut. Also verify manufacturer limits |
| Via annular ring | **≥ 0.15 mm** | 0.30 mm hole + 0.60 mm pad |
| PTH (component) hole and ring | hole = lead + **0.2–0.3 mm**, ring **≥ 0.25 mm** | Datasheet hole size first |
| NPTH minimum hole | **0.50 mm** | Mounting and tooling holes |
| Hole-to-hole (edge to edge, different nets) | **≥ 0.50 mm** | Vias of the same net may be closer (≥ 0.25 mm) |
| Via to trace/copper | **≥ 0.25 mm** | All layers |
| PTH hole to trace/copper | **≥ 0.35 mm** | NPTH to copper ≥ 0.30 mm |
| Pad to pad (different nets) | **≥ 0.20 mm** | Fine-pitch IC pads follow the datasheet footprint |
| Solder mask expansion | **0–0.05 mm** per side | Use the manufacturer's setting (JLCPCB: 1:1) |
| Solder mask dam between pads | **≥ 0.10 mm** | 0.13 mm for black/white mask; 0.20 mm for 2 oz copper. If smaller, open the mask over the group |
| Silkscreen line / text height | **≥ 0.15 mm / ≥ 1.0 mm** | Width:height about 1:6 |
| Silkscreen to pad / mask opening | **≥ 0.15 mm** | LAY-30 |
| CHASSIS_GND ring width | **≥ 1.50 mm** | Only for a user-approved ring |
| CHASSIS_GND stitching via hole | **0.80 mm** | Only if the ring is approved; verify pad diameter and technology suitability |
| CHASSIS_GND stitching via spacing | **3.00 mm** | Only if the ring is approved; nominal center-to-center spacing |
