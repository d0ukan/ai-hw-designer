<!-- Part of Hardware-Rules.md (index). Rule IDs are global. -->
## 01 · PCB manufacturing parameters

The values below are not the manufacturers' absolute manufacturing limits; they are the preferred **default design limits** for standard manufacturing. Last checked: 2026-11 (JLCPCB/PCBWay standard capabilities). Compare with the manufacturer's current page before ordering; if the date is stale, re-check.

| Parameter | Value | Condition |
| :--- | :---: | :--- |
| Minimum trace width | **0.20 mm** | Increase per power and impedance requirements |
| Minimum copper clearance | **0.20 mm** | Increase per voltage and isolation requirements |
| Minimum via hole | **0.30 mm** | Standard through-hole via |
| Minimum via pad diameter | **0.60 mm** | Ensure the annular ring requirement separately |
| Minimum copper-to-board-edge clearance | **0.30 mm** | Also verify manufacturer limits |
| CHASSIS_GND ring width | **≥ 1.50 mm** | Only for a user-approved ring |
| CHASSIS_GND stitching via hole | **0.80 mm** | Only if the ring is approved; verify pad diameter and technology suitability |
| CHASSIS_GND stitching via spacing | **3.00 mm** | Only if the ring is approved; nominal center-to-center spacing |
