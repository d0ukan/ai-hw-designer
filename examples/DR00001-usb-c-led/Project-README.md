# Project README — DR00001 USB-C LED board (example)

| Field | Project information |
| :--- | :--- |
| Project name / purpose | USB-C LED board — take 5 V from USB-C and light a power LED |
| Project code / revision / variants (INT-49) | `DR00001` / `R01` / A (green LED) |
| Output prefix | `DR00001-R01`, `DR00001-AV-R01` |
| Quality profile | Hobby |
| Design target (INT-48) | Cost first |
| RF | N/A |
| Battery (INT-52) | N/A |
| Single PCB / multi-PCB | Single PCB |
| Power supply | USB-C sink, 5 V, < 50 mA |
| EDA / connection | KiCad 9 / GUI (no EDA files in the example) |
| Manufacturer / assembly | JLCPCB, single-sided PCBA. LCSC numbers are verified in the JLC catalog and written to the BOM before ordering (not made up in the example) |
| User explanation preference | Caveman |

## Approved requirements

| Requirement ID | Requirement / target | Priority | Source / approval | Verification |
| :--- | :--- | :--- | :--- | :--- |
| REQ-01 | Power from a USB-C 5 V source, CC 5.1 kΩ pull-down | Mandatory | User, G0 | VBUS with a multimeter |
| REQ-02 | Power LED, ~2 mA | Mandatory | User, G0 | Remove R4 and measure current |
| REQ-03 | Board ≤ 20 × 14 mm | Preferred | User, G0 | Mechanical measurement |

## Approved PCB inputs — G0.5

| Field | Decision |
| :--- | :--- |
| Construction / laminate | Rigid FR-4, 2 layers, 1.6 mm |
| Outline | 20 × 14 mm, corners R1.0 |
| CHASSIS_GND ring | No |
| Logo / icon — PCB-17 | None |
| Board code — PCB-18 | Silkscreen, bottom, `DR00001-R01` + date |
| Connector label — PCB-19 | None (single USB-C) |
| Designator — PCB-20 | Shown, 0.8 mm, at the part edge |
| Signature — PCB-21 | Decide later → "None" at G0.5 |

## Open decisions ("Decide later", INT-51)

| ID | Deferred decision | Latest by | Outcome |
| :--- | :--- | :--- | :--- |
| OD-01 | Signature / easter egg | G0.5 | User said "none", closed |

## Variants

| Variant | Prefix | Difference | BOM / PnP |
| :--- | :--- | :--- | :--- |
| — | `DR00001-R01` | Red LED | `DR00001-R01_BOM.csv` / `_PnP.csv` |
| A | `DR00001-AV-R01` | Green LED | `DR00001-AV-R01_BOM.csv` / `_PnP.csv` |

## Architecture and design decisions

| ID | Decision | Source |
| :--- | :--- | :--- |
| D-01 | LED current: (5.0 V − 2.0 V) / 1.5 kΩ ≈ 2.0 mA. Vf ≈ 2.0 V, the typical value in the LTST-C191KRKT/KGKT datasheet; verify Vf at 2 mA from the datasheet curve | Calculation |
| D-02 | R4 is a fitted 0 Ω series bridge: remove it and connect an ammeter in its place | SCH-07 |
| D-03 | C1 10 µF DNP: VBUS bulk option; fit it if needed for a long cable or ESD test | SCH-07 |
| D-04 | The green LED in variant A has no drop-in alternate part (different Vf); "no alternate" in the BOM | DFM-14 |
