# Project README — Project-specific information, requirements and rules

> In a new project this file is an empty starting template. Manager keeps the real user answers, project-specific requirements, extra rules, decisions made and the current state here. This file is the single source of truth for the project; do not copy the full chat or long technical documents, record the relevant file/page reference. The machine approval record is in `project/workflow-state.json`, the independent review evidence in `REVIEW_LOG.md`.

| Field | Project information |
| :--- | :--- |
| Project name / purpose | TBD |
| Project code / revision / variants (INT-49) | TBD — e.g. `DR00627` / `R01` / A, B |
| Output prefix (`projectctl.py name`) | TBD — e.g. `DR00627-R01`, `DR00627-AV-R01` |
| Quality profile (Hobby / Industrial / Aerospace, INT-47) | TBD |
| Design goal (Cost / Balanced / Performance, INT-48) | TBD |
| Review depth (Light / Medium / High, INT-53) | TBD |
| Human engineer sign-off (AI-09) | No / Yes — reason |
| RF present? / band / tier (RF-A, RF-B, RF-C) | TBD / N/A |
| Battery / chemistry / cells (INT-52, section 10) | TBD / N/A |
| Board type / written requirements | TBD |
| Single PCB / multi-PCB and board IDs | TBD |
| Board-to-board connection method | TBD / N/A |
| Ready-made module use / existing STEP-CAD | TBD |
| External physical connectors / mating parts | TBD |
| Diagnostic / status / communication LEDs | TBD |
| Programming/flash/debug (on-board / off-board / N/A) | TBD |
| Full STEP/CAD assembly delivery | TBD |
| Supply type / min–nom–max | TBD |
| Size limit L × W × H mm (INT-19) / layer count (INT-20) | TBD |
| EDA software | TBD |
| EDA version / connection method | TBD |
| Requirements revision | TBD |
| PCB input revision | TBD |
| Manufacturer / assembly method (INT-17, INT-18) | TBD |
| Country / region (INT-56) | TBD |
| Target quantity / cost | TBD |
| Sourcing strategy | TBD |
| User-supplied parts: exact product, local source, mounting (DFM-16, INT-57) | TBD / N/A |
| Diff pairs: pair table in the review evidence (DIF-11) | TBD / N/A |
| Reference layout source (LAY-08) | TBD / N/A |
| Operating environment | TBD |
| AI budget / model preferences | Record if the user defines them |
| User communication preference | Caveman / Balanced / Detailed — TBD |
| Active role / execution environment | Manager / TBD |

## Approved requirements

Summarize the project-relevant answers from `Hardware-Rules.md` section 00 here. Cover supply, I/O, mechanical, chassis/isolation, standards, test and delivery requirements.

Classify requirements as Mandatory / Preferred / Flexible / Unclear / N/A. Record the electrical values and written sources needed for the board type; do not ask the same questions again.

| Requirement ID | Requirement / target | Priority | Source / approval | Verification / acceptance criterion |
| :--- | :--- | :--- | :--- | :--- |

## Project-specific extra rules

| Rule ID | Applies to board / area | User rule or approved exception | Source / approval |
| :--- | :--- | :--- | :--- |

Do not copy the general `Hardware-Rules.md` and `Hardware-Roles.md` files. Record project-specific extra rules here. If a preference conflicts with a general rule, record the reason and the user decision; never treat an exception that violates mandatory standards or safety requirements as accepted.

## EDA & Tool Integration

| Information | Verified value |
| :--- | :--- |
| EDA / version | TBD |
| Connection | MCP / native CLI / API-script / GUI / manual |
| Adapter name, version and trusted source | TBD / N/A |
| MCP scope (this project / all projects) and Reviewer read-only entry | TBD / N/A |
| File access and read/write permission | TBD |
| Schematic, PCB, library editing capabilities | TBD |
| ERC/DRC, export, STEP/CAD capabilities | TBD |
| Connection test and known limits | TBD |

Record only capabilities that were actually tested as usable. Do not write API keys or secrets to this file.

## Boards and physical interfaces

Fill in only if applicable. For a single PCB and simple interfaces a short summary is enough.

| Board ID | Function | Native EDA path / mechanical reference |
| :--- | :--- | :--- |

| Interface ID | Source → target | Connection type / pinout reference | Connector / mating connector / STEP reference |
| :--- | :--- | :--- | :--- |

Reference `Hardware-Library/catalog/components.csv` records for approved ready-made modules and required 3D models. Record diagnostic indicators and their meanings as a short requirement note.

## Programming and Debug — only if a programmable component exists

| Target component / board ID | On-board / off-board / factory programmed | Interface / programmer-debugger | Connector / pinout / supply / test reference |
| :--- | :--- | :--- | :--- |

Evaluate flash, debug and field update requirements separately. Record standard or custom connector, pads/fixture, Pin 1, supply method and mechanical access preferences with an approval reference. N/A for projects that need no programming.

## Approved PCB inputs — G0.5

| Field | Decision / approval reference |
| :--- | :--- |
| Physical PCB structure / laminate / technology | TBD |
| Quality class / special standards | TBD |
| Board outline / dimensions / radius / chamfer | TBD |
| Mounting holes / slots / keepout / height | TBD |
| Manufacturer / stack-up / copper weight / finish | TBD |
| CHASSIS_GND perimeter ring (Yes / No) | TBD — not created without explicit approval |
| GND connection / isolation | Reference the approved decision in section 00 |
| Logo / icon (side) — PCB-17 | TBD / Decide later / None |
| Board code text: silk/copper, side, date — PCB-18 | TBD / Decide later |
| Connector label: pin no / net name / both, side — PCB-19 | TBD / Decide later |
| Designator: visible/hidden, size, inside/edge — PCB-20 | TBD / Decide later |
| Signature / easter egg — PCB-21 | TBD / Decide later / None |

If available, add references to the relevant mechanical files and verified manufacturer parameters. Do not rewrite unchanged inputs.

In a multi-PCB project, record each board's properties by board ID. For full assembly scope and matching connector/mechanical references, reference the `Mechanical/` sources.

## PCB notes (SCH-17)

- TBD: critical loops, parts that sit together, diff pairs / controlled nets, hot parts, sensitive analog, connectors and test points.

## Architecture and design decisions

| ID | Decision / requirement | Source or user approval |
| :--- | :--- | :--- |

## RF / High-Speed / SI-PI — only if applicable

| Line / interface ID | Source requirement / standard | Approved impedance, timing and other limits | Stack-up / analysis / acceptance criterion reference |
| :--- | :--- | :--- | :--- |

State the source of the relevant manufacturer stack-up, material, line classes, models and measurement requirements. Leave this section N/A in unrelated projects.

## Aviation / Avionics — only in the Aerospace profile

| Field | Decision / source |
| :--- | :--- |
| Applicable standards and levels (DO-254 DAL, DO-160 categories, MIL-STD etc.) | TBD |
| PCB / assembly quality class (IPC-6012, IPC-A-610) and manufacturer certification | TBD |
| Derating policy | TBD |
| Temperature range / environmental conditions | TBD |
| Power input standard / transients | TBD / N/A |
| Coating / staking / solder and finish policy | TBD |
| Required analyses (FMEA, reliability, worst-case, thermal) | TBD |

Leave this section N/A in Hobby and Industrial projects.

## Current state and checkpoint

| Revision | Change / check | Short evidence or commit |
| :--- | :--- | :--- |

**Last completed stage:** TBD · **Next task / pending approval:** TBD.

When switching to another AI or client, continue from the current revision, only the relevant files, open findings and the next task. Do not re-analyze the old chat.

## Verified technical sources

Reference shared component/library records. Summarize new sources with MPN, revision, relevant page and validity condition.

## Open decisions ("Decide later", INT-51)

| ID | Deferred decision | Latest gate to ask | Safe default if no answer |
| :--- | :--- | :--- | :--- |

## Variants — only if any

| Variant | Prefix | Difference (fitted/unfitted parts, values) | BOM / PnP |
| :--- | :--- | :--- | :--- |

## Open issues

| ID | Open issue | Next step |
| :--- | :--- | :--- |
