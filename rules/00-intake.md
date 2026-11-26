<!-- Part of Hardware-Rules.md (index). Rule IDs are global. -->
## 00 · Project Intake — Project start questionnaire

> **MANDATORY — BEFORE STARTING THE DESIGN:** Question order: communication preference (INT-46) → project idea (INT-55) → project identity (INT-49) → EDA tool and MCP offer (INT-04, INT-54) → project purpose (INT-01) → size limit (INT-19) → quality profile (INT-47) → design goal (INT-48) → relevant technical questions → review depth (INT-53, last before G0, once RF/battery/voltage are known). Ask the user the questions below according to the project scope. Do not re-ask information already given. Do not start component selection, schematic or PCB layout until critical requirements and design preferences are clear.

### Start · Communication preference

- [ ] **INT-46** — In the first session ask the user: **How should explanations be? Caveman (very short and plain), Balanced, or Detailed?** Record the choice in `Project-README.md` and apply it to later user replies. If a preference exists, do not ask again; the user may change it later. If there is no answer, use Balanced.

| Mode | Communication style toward the user |
| :--- | :--- |
| Caveman | Short, direct, plain sentences; only the necessary information and decisions. |
| Balanced | Concise explanation, key technical rationale and small comparisons when needed. |
| Detailed | Technical details, calculations, assumptions and rationale for alternatives. |

The communication preference does not reduce engineering verification, critical warnings, real evidence records or user approval gates. Inter-agent task and result summaries are stripped of unnecessary detail in every mode.

### Start · Project idea

- [ ] **INT-55** — Do not propose projects on your own. Ask in one question: **"What would you like to build? Or shall I suggest some project ideas?"** Only if the user wants ideas, suggest **3–5 ideas** tailored to the user. Base them only on what you can see: the user's earlier projects in this repo (`Project-README.md`, `REVISION-HISTORY.md`, `Hardware/`, `Manufacturing/`), interests the user mentioned, the EDA tool, experience level and budget if known. Do not search the user's other files, accounts or history without permission. For each idea give one line: what it does, difficulty (easy / medium / hard), rough cost and key parts; say which earlier project or interest it builds on. The user picks one, changes one or gives their own; do not start a project without the user's choice. Then continue with INT-49 and INT-04.

### Start · Project identity

- [ ] **INT-49** — Once the project idea is clear (INT-55), ask: **project name, project code and revision** (e.g. name "Sensor board", code `DR00627`, revision `R01`). The user defines the code format; do not impose the example format. If there is a variant, ask for its letter (A, B, …). Record the name with `projectctl.py set project_name`, the code with `set project_code`, the revision with `set design_revision`. This question cannot be deferred; no export without a code.
- [ ] **INT-50** — All outputs are named with this identity (section 09): `<code>-<rev>` → `DR00627-R01`, for a variant `<code>-<letter>V-<rev>` → `DR00627-AV-R01`. `python scripts/projectctl.py name [--variant A]` gives the prefix.

### Start · EDA tool and AI connection

- [ ] **INT-04** — Right after the project identity, ask: **Which EDA software and version will be used? (KiCad, Altium Designer, EasyEDA Pro, etc.)** Does the user have existing, authorized MCP server, native CLI, API/script or GUI access? Record existing integration preferences and real capabilities.
- [ ] **INT-54** — If the AI client can run tools and there is no working connection yet, offer the matching MCP server: KiCad → KiCAD-MCP-Server; Altium Designer → official Altium MCP Server or altium-mcp; EasyEDA Pro → Extension API (third-party MCP only on request). Ask: **"Shall I set up <server> for you? For this project only (recommended) or for all your projects?"** Install only after an explicit yes, show each command first, and let the user enter license keys and sign-ins. Follow `MCP-SETUP.md`. If the client loads new tools only after a restart, say so now and ask the user to restart and resume this same conversation (AI-10). Verify with a real read call and record server, version and scope in `Project-README.md` → "EDA & Tool Integration". If the user says no, or the client has no tool access (web chat), give manual steps or continue in manual mode. The Reviewer uses a read-only connection (REV-13).

### Start · "Decide later" option

- [ ] **INT-51** — For non-critical questions (e.g. logo/icon, silkscreen text, designator visibility, signature, color) offer the user a **"Decide later"** option. Write the deferred question as OPEN in the `Project-README.md` "Open decisions" table and ask again at the latest at the related gate: for everything on the board (logo, text, designator, signature; PCB-17…21) that is **G0.5**, i.e. before layout starts. If there is still no answer, use the safe default and record it (no logo, no signature, no copper text; designators visible). Critical questions (power, safety, isolation, connector/pinout, voltage/current, quality profile, review depth, project identity) do not have this option.

### Start · Quality profile

- [ ] **INT-47** — After learning the project purpose, ask: **What level will this board be? Hobby, Industrial or Aerospace?** Record the choice in `Project-README.md`. The profile only sets rule strictness and defaults; the user may override each default separately. Do not pick a profile by guessing; if there is no answer, present your recommendation with rationale and wait for approval.

| Profile | Typical use | Default approach |
| :--- | :--- | :--- |
| Hobby | Personal project, prototype, low cost | JLCPCB/PCBWay standard line, fewest layers, commercial temperature grade (e.g. 0…+70 °C) accepted if sufficient, affordable sourcing such as LCSC/JLC Parts, IPC Class 2 level manufacturing |
| Industrial | Long-term reliable operation in the field | Extended temperature (e.g. −40…+85 °C), input protection circuits, long-life and multi-source components, IPC Class 2 (Class 3 if needed) |
| Aerospace | Flight, military or similar high reliability | Section 08 profile mandatory; IPC Class 3, derating policy, traceability, user-specified standards and a suitably certified manufacturer |

Profile choice must not create unnecessary cost: do not apply Aerospace rules to a Hobby project or Hobby defaults to an Aerospace project. The RF and Aerospace sections are enabled only when relevant; otherwise they are left as N/A.

### Start · Review depth

- [ ] **INT-53** — Ask: **How thorough should the review be? Light, Medium or High?** Record the answer with `python scripts/projectctl.py set review_depth <Light|Medium|High>` before G0. Explain the choice in one line each:

| Depth | Reviewers | What is checked |
| :--- | :--- | :--- |
| Light | 1 | Critical checks only: power, pin mapping, footprints, manufacturability (VER-13) |
| Medium (default) | 1 | The full review checklist |
| High | 2, independent | Two separate Reviewers; both must PASS the schematic and the PCB before G1 (VER-13) |

Minimum depth: if the board is in the Aerospace profile, or has RF, a battery (INT-52), mains or voltage above SELV (AI-09), Light is not allowed; use at least Medium and recommend High. Tell the user why. Without an answer the depth is Medium. This is a critical question; "Decide later" does not apply.

### Start · Design goal (cost / performance)

- [ ] **INT-48** — After the profile, ask: **What is the design goal? Cost first, Balanced (price/performance) or Performance first?** If there is a target cost or budget, get it too (INT-03). Record the choice in `Project-README.md`. If there is no answer, propose the default by profile and get approval: Hobby → Cost first, Industrial → Balanced, Aerospace/military → Performance first (unless the user gave a separate cost target).

| Goal | Component, PCB and layout decisions |
| :--- | :--- |
| Cost first | Cheapest adequate solution that meets the requirement; standard manufacturing (DFM-00), fewest layers, common and cheap parts |
| Balanced | Best price/performance that meets the requirement with a safe margin; cost increase only if there is a measurable benefit |
| Performance first | Electrical performance, reliability, margin and long life first; if needed, better components, extra layers, special laminate, controlled impedance, wider derating. Cost is not a blocker, but no unnecessary luxury is added |

Under no goal are requirements, safety, reliability or verification cut for cost. Under Performance first, every choice that raises cost is still reported with rationale (AI-03, DFM-07); it just does not block approval. This goal applies only to hardware decisions; AI model/token efficiency always applies.

**Question strategy:** First review existing requirement documents and project information. After learning the general purpose, ask only the relevant technical question groups, as a single batched question list where possible. Record answers in `Project-README.md` as Mandatory / Preferred / Flexible / Unclear / N/A. Use the proposed economical defaults if the user explicitly accepts them. Learn PCB and mechanical constraints that affect the schematic or component selection before G0; clarify the remaining manufacturing and mechanical details in section 00B.

### A · Project purpose and scope

- [ ] **INT-01** — **What is the purpose of this project?** What will the PCB do, in which device or system will it be used, and what are its main functions?
- [ ] **INT-19** — Right after the purpose, ask: **"Is there a size limit?"** Get the maximum envelope as length × width × height in mm, including connectors, mating cables/plugs and the tallest part; or let the user say **"as small as possible"** or **"no limit"**. Also ask board shape, mounting holes and any enclosure (ask for its STEP/drawing). Size drives package size, module choice, single/double-sided assembly and layer count, so record it before G0; finalize the details at G0.5 (PCB-05…08). If there is no answer, assume "no limit" and say so.
- [ ] **INT-02** — Is the design from scratch, or a revision of an existing schematic/PCB? Is there a requirements document, reference design or existing file?
- [ ] **INT-03** — Is the design for prototype, series production or test/development? What is the estimated production quantity and target PCB/PCBA unit cost?
- [ ] **INT-27** — Are there written requirements, customer requirements, ICD, technical specification, reference board or mandatory component list for the project? Which requirements are fixed and which are left to the designer?
- [ ] **INT-40** — Does the user have additional project-specific design rules, preferences, acceptance criteria or prohibitions? Record them with source and approval in `Project-README.md`; clarify points that conflict with the general rules.
- [ ] **INT-28** — What is the board's main function/type? Power supply or power distribution, functional control/MCU, analog measurement, digital communication, RF, sensor/interface, motor driver or a mixed board? Open only the relevant technical question group.
- [ ] **INT-32** — **Is the project a single PCB or a multi-PCB system?** If there are multiple boards, what are the board count, board names/IDs, each board's function and any existing boards? Clarify power and signal distribution per board.
- [ ] **INT-33** — In a multi-PCB system, how will the boards connect? Board-to-board (mezzanine/header/backplane), cable-to-board/harness, flex connection or another method? Are there existing connectors, mating connectors, pinout, power/signal interfaces and mechanical connection constraints? Open the related questions only in a multi-PCB project.

### B · Electrical requirements

- [ ] **INT-05** — Is power supplied by AC, DC, battery, USB or multiple sources? What are the minimum / nominal / maximum input voltage, continuous and peak current/power values, required output rails and limits of the existing power source? If AC, ask frequency and phase; if DC, ask polarity, input ripple and any transient voltage conditions.
- [ ] **INT-06** — What are the inputs/outputs, connectors, communication interfaces and signal levels? Is there any line requiring differential or controlled impedance?
- [ ] **INT-07** — What are the measurement accuracy, frequency, sampling rate, current capacity or other performance requirements?
- [ ] **INT-08** — Is there any ESD, surge, reverse polarity, overvoltage/overcurrent, EMC/EMI or specific test/standard requirement?
- [ ] **INT-29** — For each input/output, what are the direction, count, normal and maximum values, load type, expected current, timing and power-up/power-down conditions? Is a specific connector and pinout mandatory?
- [ ] **INT-30** — Are the specifications of external cables, connected devices, power supply, sensors and loads defined? Is compatibility with a reference circuit or existing system required?
- [ ] **INT-34** — **Which interfaces will the system physically expose to the outside?** For power, data, sensor, RF and other I/O, what are the desired connector type, brand/MPN, pin count, pinout, panel/PCB mounting, cable exit direction and any mating connector/cable harness? Will the user select connectors, or will the AI propose them for approval?
- [ ] **INT-41** — Is there an RF, controlled-impedance or high-speed interface? If so, get the related datasheet/interface specification, frequency/data rate and edge time, target impedance, timing/skew/length limits, connection/termination and verification requirements. Do not ask for unneeded detail. **If there is no RF**, the RF part of section 05 is N/A and no RF question is asked. **If there is RF**, ask the operating frequency/band and set the RF tier (RF-A / RF-B / RF-C) in section 05.

#### Conditional technical questions by board type

| Board type | Ask only the applicable additional requirements |
| :--- | :--- |
| Power board | Output voltages/currents, continuous/peak load, efficiency, ripple, temperature limit, protection and isolation requirements |
| Functional / MCU control board | Functions, I/O count, logic levels, interfaces, processor preference, programming/debug, software compatibility |
| Analog / measurement board | Measurement range, accuracy, resolution, sampling rate, bandwidth, noise limit, sensor interface |
| Digital / communication board | Protocols, data rate, interface levels, connectors, differential impedance and timing requirements |
| RF board | Operating frequency/band, RX/TX function, output power/sensitivity, antenna or RF connector type, acceptance of certified modules, regulatory compliance (e.g. CE RED, FCC), material and controlled impedance requirement |
| Sensor / interface board | Sensor type, power, signal range, cable and calibration requirements |
| Motor / actuator control board | Load type, electrical interface, supply and current limits, duty cycle, feedback and protection requirements |
| Mixed board | Requirements above only for the functions used |

### C · Chassis, GND and isolation

- [ ] **INT-09** — Does the device have a metal chassis/enclosure, PE (Protective Earth) or a separate CHASSIS_GND connection? Define the grounding architecture; finalize use of a CHASSIS_GND ring around the board as a separate preference in section 00B.
- [ ] **INT-10** — Is galvanic isolation required? If so, which circuits, supplies and GND regions will be isolated from each other? Will circuit GND also be isolated from CHASSIS_GND?
- [ ] **INT-11** — **If there is no isolation and CHASSIS_GND exists:** May CHASSIS_GND be connected directly to the main circuit GND? If so, which connection method and point does the user prefer?
- [ ] **INT-12** — **If there is isolation:** What are the maximum working and transient voltages, the isolation type and any applicable standard? Based on these voltages, what minimum GND–CHASSIS_GND clearance and creepage distances in mm does the user require? Also ask for the distances between other isolated regions.
- [ ] **INT-13** — Which GND net will mounting holes, connector shields and the metal enclosure connect to? Do not create unspecified connections automatically.

| User's decision | AI's action |
| :--- | :--- |
| No isolation and direct connection approved | Join CHASSIS_GND and main GND according to the approved connection architecture. |
| No isolation but connection not approved | Keep the nets separate; wait for the connection preference to be defined. |
| GND–CHASSIS_GND isolation required | Apply the approved minimum clearance/creepage distances to all related copper and connections. |
| Isolation requirement or distances unknown | Ask the user for the required voltage and isolation information; do not pick an arbitrary distance. |
| No CHASSIS_GND ring | Do not create the perimeter ring or its stitching vias/mask openings. Keep the user-approved grounding architecture. This is a normal preference, not an exception. |

**Important:** The 0.20 mm copper clearance defined for normal nets must not be treated as a galvanic isolation distance. Isolation requirements must be verified separately per project and applicable standard.

### D · Component selection and sourcing strategy

- [ ] **INT-14** — From which sourcing channels will components be selected?

| Option | Sourcing approach |
| :--- | :--- |
| Global | DigiKey, Mouser, Farnell, RS, etc. |
| Asia / PCBA ecosystem | LCSC, JLCPCB Parts and other approved suppliers |
| Hybrid | Selection from both groups based on cost, stock, technical fit and availability |

- [ ] **INT-56** — With INT-14 ask: **Which country/region are you in?** Record it in `Project-README.md` → "Country / region". It decides which local shops count as "available" for parts the PCBA house does not stock. The assembly method is INT-18.

- [ ] **INT-15** — Is there a mandatory manufacturer/brand, approved component list, prohibited components, stock and lifecycle policy, or existing parts to use?
- [ ] **INT-16** — Which is the priority in component selection: cost, performance, quality/traceability, stock availability or long-term availability? If an INT-48 design goal exists, stay consistent with it; do not ask again, only clarify the difference.
- [ ] **INT-35** — **Are ready-made modules accepted?** For example, may ESP32, nRF, CC1101 or other ready communication/processor/sensor modules be used, or must the design consist of discrete ICs and components? If the user has or specifically prefers a module, ask for the exact MPN/model/revision and datasheet. Do not select a ready module without approval.
- [ ] **INT-57** — **Module and special-part sourcing:** When a ready module (INT-35), a header/pinned module or any part that the chosen PCBA house does not stock (e.g. not on LCSC/JLCPCB Parts) is decided, ask: **"Where will you buy this? Can you get it in your country (INT-56)?"** If the AI has web access, check local distributors/shops and the Asia channel and give 2–3 options with link, price and stock as of the check date (DFM-11); otherwise ask the user for a link. Offer the mounting choice: pin header / socket (user plugs or hand-solders the module) or castellated/SMD module (PCBA can place it if stocked). Ask for the **exact product the user will buy** (link, photo or pinout): local and clone modules often differ from the original in pin order, pin count, pitch or row spacing. Draw the footprint from that product (DFM-16).
- [ ] **INT-52** — Will the board run on a battery or charge a battery? If yes, get chemistry, cell count and capacity and enable section 10 (Battery and charging) rules; if no, section 10 is N/A.
- [ ] **INT-36** — If a ready module or predefined connector will be used, does the user have **STEP/3D CAD data, footprint, symbol and mechanical drawing**? Verify the module's connection method, pinout, mating connector/header, mounting and mechanical requirements. If there is no model, first search a verified library or the manufacturer source; if needed, ask the user for dimensions/drawing. An approximate envelope model may be used only with explicit approval and cannot be presented as a verified STEP model.

### E · PCB manufacturing, mechanical design and assembly

- [ ] **INT-17** — Which manufacturer will produce the PCB? JLCPCB, PCBWay, or a design compatible with both?
- [ ] **INT-18** — How will the PCB be assembled?

| Option | Assembly method |
| :--- | :--- |
| Manual | Hand soldering (THT / SMT) |
| Stencil + SMT | Solder paste via stencil, manual placement and reflow |
| PCBA | Manufacturer's automated component assembly service |
| Hybrid | Automated PCBA plus manual assembly of specific components |

- [ ] **INT-20** — Ask: **"Do you have a target layer count? Or shall I choose the suitable one (2, 4, 6, 8, 10, 12 …)?"** If the user names a count, use it and warn only if it cannot meet the requirements (e.g. 2 layers with USB 3 or a fine-pitch BGA). If the AI chooses, use the lowest standard count that meets the requirements (section 03) and give the reason in one line: routing density and BGA/fine-pitch parts, controlled impedance or RF needing a solid reference plane, high-speed interfaces, power/current and heat, EMC, and the size limit (INT-19). Even counts are standard; 1 layer only for very simple boards. Confirm the count at G0.5 (PCB-09). Also ask about special PCB thickness, copper thickness or surface finish; otherwise propose the economical defaults in section 03.
- [ ] **INT-21** — What are the operating environment and temperature range? Are there special requirements for humidity, vibration, dust/water, enclosure or cooling?
- [ ] **INT-22** — Is single- or double-sided component assembly preferred? Are there limits on the smallest component package, manual soldering and rework?
- [ ] **INT-31** — Is there a PCB technology, laminate, high power/heat dissipation, flex region, size, special quality or manufacturing constraint that affects the schematic/component selection? If so, record it before G0; finalize details before layout.

### F · Test, verification and delivery

- [ ] **INT-23** — Does the project have an MCU, FPGA or other programmable component? If so, complete the programming/debug selection below. For an analog design with no programming, leave this question group N/A; ask separately about test points, test fixtures and production test when needed.

#### Programming, flash and debug — only when needed

- [ ] **INT-42** — Will programming be done **on the board (in-system/on-board)**, or will the component be programmed off the board (off-board) and then fitted? Is a factory-programmed component, bootloader update, production/test fixture or another method required? Distinguish development, production and field update needs.
- [ ] **INT-43** — If on-board programming and/or debug is required, which interface will be used? JTAG, SWD, ISP/ICSP, UART/USB bootloader or another interface the target component supports? Flashing only, or debug too? Is a standard debugger/programmer (model and document) preferred?
- [ ] **INT-44** — What will the physical programming/debug connection be? Standard JTAG/SWD connector, vendor-specific header, custom connector, connectorless pad-fixture solution such as pogo-pin/test pad/Tag-Connect, or another option? Clarify connector MPN, pin count/pinout, pitch, Pin 1/orientation, mating connector and access requirements on the board/in the enclosure. If the user has no preference, propose one and get approval.
- [ ] **INT-45** — Based on the selected target component and programmer/debugger documents, record the required reference voltage/logic levels, the board's power method during programming, required reset/boot signals and any programming/test acceptance criteria. If off-board programming is selected, do not add an unnecessary programming connector unless the user also wants on-board debug/update.

#### Diagnostics, test and delivery

- [ ] **INT-37** — **Are diagnostics and status indicators required?** Which of these are needed: power LED, MCU/status/heartbeat LED, communication TX/RX or link LED, fault/error LED, debug LED, test points, reset/programming interface? Ask about indicator meaning, color preference, visibility to the user and, if needed, software behavior. If the user does not want them, do not add unnecessary LEDs or debug circuitry.
- [ ] **INT-58** — **Do you want test points?** Options: **No** · **Probe pads** (hand probing) · **Pogo-pin fixture** (bed-of-nails / programming jig). Then ask on which nets (default: every supply rail, GND, reset/boot, main buses) and the pad size. Probe pads: default SMD 1.5 × 1.5 mm (round Ø1.5 mm also fine), 1.0 mm on small boards. Pogo-pin fixture: ≥ 1.0 mm pads, ≥ 2.54 mm spacing, all on one side, 2–3 non-plated tooling holes for alignment; ask the pogo pin type if known. Record the answer in `Project-README.md`; the Designer adds them to the schematic as TP parts.
- [ ] **INT-24** — Which tests, measurements and acceptance criteria are needed to verify the design?
- [ ] **INT-25** — Which files will be delivered? Are native EDA project, PDF schematic, Gerber, drill, BOM, Pick & Place (CPL), JLCPCB BOM, detailed Excel BOM with price and stock, assembly drawing (`_ASSY.pdf`), fab note, stencil and/or 3D STEP needed? The default set and file names are in section 09.
- [ ] **INT-38** — Besides individual PCB 3D models, is a **combined STEP/CAD assembly of the complete system** required at project end? Which of the PCBs, ready modules, connectors, mating parts, any enclosure and mechanical references will be included in the model? Learn the user's existing CAD data and the desired delivery format from the start.

### Design start condition — Design Input Approval

- [ ] **INT-26** — Define a short system architecture, functional blocks, interfaces and, if needed, a power budget suited to the project complexity. For simple designs a few-bullet summary is enough; create a block diagram and separate reports only if they add value.
- [ ] **INT-39** — In multi-PCB projects, record board IDs and inter-board/external interfaces in a single short interface table. Get approval for module, connector and diagnostic preferences before starting schematic/component selection.
- [ ] Present project-specific requirements and decisions to the user as a single short project summary.
- [ ] Clearly state unanswered critical topics and proposed assumptions.
- [ ] Start the design after getting the user's approval. If approved information changes later, re-evaluate the related design decisions.
