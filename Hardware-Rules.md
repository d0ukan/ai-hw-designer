# Hardware Rules

**Hardware Design & PCB Layout Guidelines**

| Document | HW AI Design Rules |
| :--- | :--- |
| **Version** | v1.35 |
| **Scope** | Project Intake · Schematic Design · PCB Intake · PCB Layout · DFM · PCBA · Conditional RF and Aerospace (Aviation) rules · Revision, variants and outputs · Conditional battery/charging |
| **Target manufacturers** | JLCPCB / PCBWay (Hobby default); user-approved manufacturer for other profiles |
| **Design priority** | Reliability · Manufacturability · Cost/performance per project goal (INT-48) · Token efficiency |

> **Core instruction:** Apply this document to all hardware designs. Prefer standard, easy-to-manufacture PCBs; balance cost and performance according to the design goal chosen in INT-48. If a rule cannot be applied, explain why and do not create an exception without user approval.

> **How to read:** This file is an index; the rules live section by section in the `rules/` folder. Do not read all files up front: open only the section for the current stage. Rule IDs (e.g. `LAY-23`) are unique across the project; references like "section 05" point to the file in the table below. Conditional sections (05, 08, 10) are never read if they do not apply. In an AI chat with no file access, ask the user only for the relevant section file.

| Section | Rules | When to read |
| :--- | :--- | :--- |
| [00 · Project Intake — Project start questionnaire](rules/00-intake.md) | INT-01…INT-58 | First session of every new project (before G0) |
| [00B · PCB Intake — Technical and mechanical decisions before layout](rules/00b-pcb-intake.md) | PCB-01…PCB-21 | Before layout (G0.5) |
| [01 · PCB manufacturing parameters](rules/01-pcb-parameters.md) | Default limit table | When entering PCB rules into the EDA tool |
| [02 · Chassis, Ground & Polygon](rules/02-ground-polygon.md) | GND-01…GND-08 | For GND, chassis and polygon work |
| [03 · JLCPCB / PCBWay — DFM & Cost Optimization](rules/03-dfm-cost.md) | DFM-00…DFM-17 | For component selection, manufacturer and cost decisions |
| [04 · Schematic, Component Placement & Routing](rules/04-schematic-layout.md) | SCH-01…SCH-16, LAY-01…LAY-33 | Schematic, placement, routing, SI/PI and silkscreen |
| [05 · Differential Pairs, RF & High-Speed (SI/PI)](rules/05-diff-rf-hs.md) | DIF-01…DIF-11, HS-01…HS-05, RF-01…RF-09 | Only if differential, high-speed or RF is present |
| [06 · Design Review & Verification](rules/06-verification.md) | VER-01…VER-13 | During review and verification stages |
| [07 · AI working rules](rules/07-ai-rules.md) | AI-01…AI-11 | Once in the first session (short; AI-09 stop conditions) |
| [08 · Aviation / Avionics — conditional profile](rules/08-aviation.md) | AVI-01…AVI-10 | Only in the Aerospace profile |
| [09 · Revision, variants and outputs](rules/09-release.md) | REL-01…REL-04 | For revisions, variants and manufacturing outputs |
| [10 · Battery and charging — conditional](rules/10-battery.md) | BAT-01…BAT-08 | Only if the board runs on a battery/cell or charges a battery (INT-52) |


### Reading set by stage

At each stage read only these files; add conditional sections only if relevant. "Section NN" means the rule section in this index; "`Hardware-Roles.md` §NN" means the section in the roles file.

| Stage | Read | Conditional extra |
| :--- | :--- | :--- |
| Start (before G0) | `AGENTS.md`, this index, `rules/00-intake.md`, `rules/07-ai-rules.md` | — |
| Schematic | `rules/04-schematic-layout.md` (SCH), `rules/03-dfm-cost.md`, `Hardware-Library/sheet-templates/README.md` | 05, 08, 10 |
| G0.5 / PCB inputs | `rules/00b-pcb-intake.md`, `rules/01-pcb-parameters.md` | 08 |
| Layout | `rules/04-schematic-layout.md` (LAY), `rules/02-ground-polygon.md` | 05, 10 |
| Review | `rules/06-verification.md`, `Hardware-Roles.md` §1.3, `Manufacturing/templates/review-checklist.md`, relevant section | — |
| Outputs / release | `rules/09-release.md`, `rules/03-dfm-cost.md` (DFM-14, DFM-16), `Manufacturing/templates/README.md` | — |

To see the next step and its command: `python scripts/projectctl.py next`.

---

## Manufacturer references

| Manufacturer | PCB manufacturing capabilities | Impedance and stack-up |
| :--- | :--- | :--- |
| **JLCPCB** | [PCB Capabilities](https://jlcpcb.com/capabilities/Capabilities?type=1) | [Impedance Calculator](https://jlcpcb.com/pcb-impedance-calculator/) · [Stack-up](https://jlcpcb.com/impedance) |
| **PCBWay** | [PCB Capabilities](https://www.pcbway.com/capabilities.html) | [Impedance Calculator](https://www.pcbway.com/pcb_prototype/impedance_calculator.html) |

> **Note:** Manufacturers' options and pricing may change. Before ordering, use the chosen manufacturer's current capabilities and order page as the reference. The defaults in this document do not replace the electrical, mechanical or safety requirements of a specific board.
